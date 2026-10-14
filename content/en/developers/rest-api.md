# REST API conventions

v1 uses the `/v1` prefix, JSON, camelCase fields and Unix millisecond timestamps. Consult the target gateway's OpenAPI for complete parameters and responses. The gateway serves Scalar at `/docs?spec=v1` and the raw specification at `/app/openapi-v1.json`. The documentation repository provides a [downloadable OpenAPI copy](https://raw.githubusercontent.com/chainupcloud/dex-os-docs/6a3f08872ba918fe24f0927fde0e4c08a9a4de79/api/openapi-v1.json). This page explains integration behavior without duplicating the entire reference.

## Choose an endpoint

| Purpose | Entry points |
|---|---|
| Environment and signing configuration | `/v1/exchange`, `/v1/time` |
| Markets and prices | `/v1/markets`, `/v1/prices`, `/v1/markets/{symbol}/book`, `/trades`, `/candles`, `/funding` (append the last three to the market path) |
| Account state | `/v1/account`, `/v1/account/positions`, `/v1/account/orders` |
| Fills and ledger | `/v1/account/fills`, `/v1/account/ledger`, `/v1/account/orders/history` |
| Order writes | `/v1/orders`, `/v1/orders/cancel`, `/v1/orders/replace` |
| Grants and funds | `/v1/account/agents/*`, `/v1/account/withdraw`, `/v1/account/transfer` |
| Vaults | `/v1/vaults`, `/v1/vaults/{id}` and their action endpoints |
| Request outcomes and backfill | `/v1/requests/{requestId}`, `/v1/events` |

Account reads select `address` plus optional `subaccount`, or `vault` alone. Writes use `account` in the signed envelope; do not interchange these parameter names. `orderId` is a string. Do not coerce every numeric string into a JavaScript Number.

## Write outcomes

The default `ack=result` waits for execution. Single orders return a business outcome; batches return `items`, each of which may succeed or be rejected and must be checked individually. `ack=sequenced` confirms a sequencing position only, not business success. `waitMs` applies only to `ack=result` and accepts 0–5000 milliseconds; 0 means no waiting.

HTTP 202 means the request was sequenced but no outcome arrived within the waiting budget. Save `requestId`, `seq`, `sub` and the original request, then query `/v1/requests/{requestId}`. A connection can fail after the service accepts a write, so reconcile first. If receipt lookup reports a history gap, “cannot prove execution” does not mean “did not execute.”

`clientOrderId` supports client correlation and duplicate checks. Mappings for requests sequenced without an immediate result can later be resolved from execution history. Do not treat an initially pending mapping as proof that no order exists. Consult the order endpoint for its format, duplicate semantics and supported cases.

## Read after write

Write receipts carry `x-dexos-seq`. When reading the result of that write, send its value as `x-dexos-min-seq`. A replica that has not caught up returns 412 instead of silently returning old data. This header is for read-after-write operations; do not attach an ever-growing watermark to every market poll.

A 412 may concern the execution `ledger` or the asynchronous analytics `projection`. Execution completing does not mean analytics has been persisted. Inspect the error details and wait for the relevant data source. Check the target replica's progress before switching replicas.

## History pagination

Fills, ledger entries and events use `limit` and `after`; some also use `upper` and `epoch`. Fetch the first page, then pass response `next` as `after`, preserving the fixed `upper` and `epoch` for the same traversal, until `hasMore=false`. Do not increment cursors yourself or derive them from timestamps.

```bash
: "${DEXOS_API_URL:?Set the API base URL}"
: "${DEXOS_ADDRESS:?Set the main wallet address}"
curl --fail-with-body --silent --show-error --get \
  "$DEXOS_API_URL/v1/account/fills" \
  --data-urlencode "address=$DEXOS_ADDRESS" \
  --data-urlencode "limit=100"
```

For subsequent pages, set `DEXOS_AFTER`, `DEXOS_UPPER` and `DEXOS_EPOCH` to the values from the first traversal response:

```bash
: "${DEXOS_AFTER:?Set next from the response}"
: "${DEXOS_UPPER:?Set the fixed upper bound}"
: "${DEXOS_EPOCH:?Set epoch from the response}"
curl --fail-with-body --silent --show-error --get \
  "$DEXOS_API_URL/v1/account/fills" \
  --data-urlencode "address=$DEXOS_ADDRESS" \
  --data-urlencode "limit=100" \
  --data-urlencode "after=$DEXOS_AFTER" \
  --data-urlencode "upper=$DEXOS_UPPER" \
  --data-urlencode "epoch=$DEXOS_EPOCH"
```

After a WebSocket disconnect, backfill through fills or events. Deduplicate by stable event id and handle explicit history-unavailable errors. Event pages filtered by symbol can be empty while still containing `next` and `hasMore`; do not stop on an empty page alone.

## Errors and limits

Business API errors use `{error:{code,num,message,details?}}`. Branch on stable `code`, retain HTTP status and `details`, and avoid parsing the English message. Malformed HTTP or JSON can also be rejected directly by the HTTP framework; clients must handle responses that cannot be parsed as JSON.

| Status | Response |
|---|---|
| 400 | Fix parameters, types or formatting |
| 401 | Check signatures and the signing domain |
| 403 | Check ownership, API wallet grants and scope |
| 404 | Verify account, market, order or resource identity |
| 409 | Inspect conflict details and existing requests |
| 412 | Wait for the ledger or projection watermark required by the write |
| 421 | Check the request entry point and node role |
| 422 | Handle the business rejection; it is not a network failure |
| 429 | Wait according to `retry-after` and reduce request weight |
| 5xx / connection failure | For writes, inspect receipts and reconcile before proceeding |

Rate limits have IP and write-account budgets, counted by weight in fixed 60-second windows. Ordinary reads cost 1, books and prices 2, history requests 5. Writes cost a base weight of 1 plus `floor(n / 40)` for batches. Operators can adjust budgets; use the response `ratelimit`, `ratelimit-policy` and `x-ratelimit-account` headers. A 429 response's `details.bucket` identifies the IP or account budget.
