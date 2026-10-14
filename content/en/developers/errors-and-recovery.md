# Errors and recovery

REST errors have the form `{"error":{"code":"…","num":10000,"message":"…","details":{}}}`. The number here illustrates the structure; use the actual response value. `details` is optional. Make decisions using stable `code` values and business fields; retain the HTTP status, requestId, and response body for diagnosis.

## HTTP status codes

| Status | Meaning and action |
| --- | --- |
| 400 | Invalid parameters, precision, or pagination boundaries; correct the request. If history says `not yet complete`, retry later with the same boundaries |
| 401 | Signature check failed; check environment domain, signer, fields, and integer scaling |
| 403 | Ownership or API-wallet scope violation; check the grant and expiry, and use an authorized wallet for funds operations |
| 404 | Object not found; receipt lookups also require checking `details.status` and the query watermark |
| 409 | Conflict or ledger epoch change; rebuild state according to the specific error |
| 412 | The read replica has not reached your required seq; retry while preserving that consistency requirement |
| 421 | Wrong node; check the environment's public API entry point |
| 422 | Business rejection; correct the operation and do not assume the nonce is unconsumed |
| 429 | Request budget exhausted; respect `retry-after` and reduce request frequency |
| 5xx | Service unavailable or history incomplete; reads may be retried later, but first resolve the original outcome of writes |

## HTTP 202 and uncertain write outcomes

The default `ack=result` waits for execution. If the wait expires, HTTP 202 can return `status: "sequenced"` and a `requestId`. The request has been sequenced: **do not submit another order**. Explicit `ack=sequenced` also confirms sequencing only, not a fill or business success.

Save the write response's requestId and query:

```text
GET /v1/requests/<requestId>
```

A 200 response has `status` of `pending`, `executed`, or `rejected`. Continue waiting for pending requests. Final results can include `nonceConsumed`, `reason`, and `items`; inspect each business outcome. HTTP 200 on a batch does not mean every item succeeded.

Handle non-2xx receipt responses separately:

- 404 with `details.status: "not_found"`: no execution was found up to `details.asOfSeq`; this is not a permanent statement about every future watermark.
- 409 with `details.status: "conflict"`: another request consumed the supplied nonce. Inspect `details.conflictingRequest` and do not continue using that nonce.
- 503 with `details.status: "history_unavailable"`: history gaps prevent proving whether the request executed. This does not justify resubmission.

Supply `scope` and `nonce` together to detect nonce conflicts. API-wallet requests may also supply the original signed `commandHash`; use the original request values and consult API Reference for their formats. A network timeout without a response does not prove write failure either: resolve the outcome using the original signature's requestId or SDK receipt support before creating a duplicate business request with a new nonce.

## HTTP 429 and rate limits

REST budgets use fixed 60-second windows and request weights. Every `/v1/*` request counts against the IP budget. Writes that pass signature pre-check also count against the main-wallet budget; subaccounts share that budget.

Read `ratelimit` and `ratelimit-policy`. Writes reaching the account-budget check also include `x-ratelimit-account`. A 429 response supplies `retry-after`, with `error.details.bucket` identifying `ip` or `account`. Wait accordingly and avoid concurrent retry bursts. Operators can adjust budgets; do not treat defaults as fixed service guarantees.

## Read after write and history pagination

A write response's `x-dexos-seq` is its commit position. For a subsequent REST read that must include this write, send `x-dexos-min-seq`. A lagging replica returns 412; preserve that minimum when retrying.

The first execution-history page returns `epoch` and a fixed `upper` bound. For later pages, use the previous page's `next` as `after` and pass back the same `epoch` and `upper`; missing boundaries return 400. Do not switch bounds or sort direction halfway through pagination.

409 `history_epoch_mismatch` means the ledger epoch changed: old cursors are no longer valid, so fetch a new first page and rebuild local state. A 400 message containing `not yet complete` means history through the requested bound is incomplete: retry the same request later. Correct other invalid parameters before retrying. See [WebSocket](websocket.md) for live-stream backfill.
