# REST API conventions

v1 uses the `/v1` prefix, JSON, camelCase fields and Unix millisecond timestamps. Consult the target gateway's OpenAPI for complete parameters and responses. The gateway serves Scalar at `/docs?spec=v1` and the raw specification at `/app/openapi-v1.json`. The documentation repository provides a [downloadable OpenAPI copy](https://raw.githubusercontent.com/chainupcloud/dex-os-docs/6496bb9a2d9c33f3809ed74701b360d72865ca44/api/openapi-v1.yaml). This page explains integration behavior without duplicating the entire reference.

## Choose an endpoint

| Purpose | Entry points |
|---|---|
| Markets and prices | `/v1/markets`, `/v1/prices`, `/v1/markets/{symbol}/book`, `/trades`, `/candles`, `/funding` (append the last three to the market path) |
| Account state | `/v1/account`, `/v1/account/positions`, `/v1/account/orders` |
| Fills and ledger | `/v1/account/fills`, `/v1/account/ledger`, `/v1/account/orders/history` |
| Signed writes (orders, grants, funds, vaults) | `POST /v1/commands` |
| Deposit and withdrawal routes | `/v1/exchange/cctp/routes`, `/v1/exchange/cctp/quote`, `/v1/exchange/cctp/withdraw-quote` |
| Vaults | `/v1/vaults`, `/v1/vaults/{id}` |
| Request outcomes and backfill | `/v1/requests/{requestId}`, `/v1/events` |

Account reads select `address` plus optional `subaccount`, or `vault` alone; the two selectors are mutually exclusive. A perpetual and a spot market can share a name: add `kind` (`perp` or `spot`) where a name is ambiguous, otherwise the request is rejected rather than guessed. `orderId` and other 64-bit values are strings. Do not coerce every numeric string into a JavaScript Number.

## Write outcomes

All signed writes go through `POST /v1/commands` (see [Signing and authorization](authentication.md)). The endpoint does not wait for execution and has no `ack` or `waitMs` parameter. HTTP 202 returns `requestId`, `digest`, `seq` and `sub` and proves sequencing only. Save them with the original command bytes and query `/v1/requests/{requestId}?digest=` for the outcome; business results, including each item of a batch, are in the receipt. A connection can fail after the service accepts a command, so reconcile first, as described in [Errors and recovery](errors-and-recovery.md).

`clientOrderId` is optional on signed orders: 1–36 characters from `A-Z a-z 0-9 . _ : / -`. A value the account has already used is rejected with 409 `GatewayDuplicateClientOrderId` before sequencing. Order reads return it. TWAP and TP/SL orders have no `clientOrderId`, and orders cannot be canceled or modified by it.

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

After a WebSocket disconnect, backfill through fills or events. Deduplicate by stable event id and handle 400 `GatewayHistoryIncomplete` by retrying the same request later. Event pages filtered by symbol can be empty while still containing `next` and `hasMore`; do not stop on an empty page alone.

## Errors and limits

Business API errors use `{error:{code,num,message,details?}}`. Branch on stable `code`, retain HTTP status and `details`, and avoid parsing the English message. Malformed HTTP or JSON can also be rejected directly by the HTTP framework; clients must handle responses that cannot be parsed as JSON.

| Status | Response |
|---|---|
| 400 | Fix parameters, types or formatting |
| 401 | Check the signature pre-check on endpoints that verify signatures at the gateway |
| 403 | Check ownership, API wallet grants and scope |
| 404 | Verify account, market, order or resource identity |
| 409 | Inspect conflict details and existing requests |
| 412 | Wait for the ledger or projection watermark required by the write |
| 421 | Check the request entry point and node role |
| 422 | Handle the business rejection; it is not a network failure |
| 429 | Wait according to `retry-after` and reduce request weight |
| 5xx / connection failure | For commands, resolve the receipt before signing anything new |

Rate limits have IP and write-account budgets, counted by weight in fixed 60-second windows. Ordinary reads cost 1, books and prices 2, history requests 5. Commands cost a base weight of 1 plus `floor(n / 40)`, where `n` counts the orders, cancels and modifications in the command. Operators can adjust budgets; use the response `ratelimit`, `ratelimit-policy` and `x-ratelimit-account` headers. A 429 response's `details.bucket` is `ip`, `account` or `unverified`.
