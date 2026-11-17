# Errors and recovery

REST errors have the form `{"error":{"code":"…","num":10000,"message":"…","details":{}}}`. The number here illustrates the structure; use the actual response value. `details` is optional. Make decisions using stable `code` values and business fields; retain the HTTP status, requestId, and response body for diagnosis.

## HTTP status codes

| Status | Meaning and action |
| --- | --- |
| 400 | Invalid parameters, precision, encoding or pagination boundaries; correct the request. `GatewayHistoryIncomplete` means history is not yet written: retry later with the same boundaries. A command rejected with 400 was not sequenced |
| 401 | Signature pre-check failed on an endpoint that verifies signatures at the gateway |
| 403 | Ownership, scope or builder pre-check rejection; a command rejected here was not sequenced |
| 404 | Object not found; a receipt lookup answers 404 with status `Unknown` (see below) |
| 409 | Conflict: a duplicate `clientOrderId`, a receipt whose actionId was accepted with a different digest, or a ledger epoch change in history pagination |
| 412 | The read replica has not reached your required seq; retry while preserving that consistency requirement |
| 413 / 415 / 408 | Command body too large, not `application/json`, or body read timed out; the command was not submitted |
| 421 | The node is read-only or not the leader; send the same command to the leader entry point |
| 422 | Business rejection before sequencing (for example `GatewayCollateralTokenMismatch`); the nonce was not consumed |
| 429 | Request budget exhausted; respect `retry-after` and reduce request frequency |
| 5xx | Service unavailable. For a command, 503 can mean the outcome is unknown: resolve it before sending anything new |

## Command outcomes

`POST /v1/commands` answers 202 once a command is sequenced. That proves only sequencing, not authorization or execution: `executionKnown` is false and `nonceConsumed` is null. Keep the original command bytes, its `requestId` (the actionId) and its `digest`, then query:

```text
GET /v1/requests/<requestId>?digest=<digest>
```

| Receipt status | Meaning |
| --- | --- |
| `Accepted` | Accepted by the ledger; results may still be pending (`resultsPending`) |
| `Executed` | Executed. Business results are in `events`, per-item results of a batch in `items`, and a business rejection in `businessRejected`; check every item |
| `AuthorizationRejected` | The ledger refused the command's authorization; it was not executed and the nonce was not consumed |
| `Unknown` (HTTP 404) | The read view has no record of this command. On its own this does not prove it never executed |
| HTTP 409 | The same actionId was accepted with a different digest, for example a copy re-signed with another validity |

Resubmitting exactly the same command bytes is safe: if the ledger already accepted it, the gateway answers 200 with the first receipt and `duplicate: true` and does not sequence it again. Re-signing the action with a new validity or nonce creates a different command and can execute twice.

## Resolving an unknown outcome

A network timeout, a 5xx or an `Unknown` receipt does not prove that a write failed. A command can never be accepted after its `validUntilMs`, which gives a definite answer:

1. Wait until the certified time from `GET /v1/security/time` passes the command's `validUntilMs`.
2. Query the receipt with `x-dexos-min-seq` set to the `hostLogIndex` from that same time response. A 412 means the replica has not caught up; retry.
3. `Executed` means the command executed; read the results from the receipt. `Unknown` or `AuthorizationRejected` means this command was not and will never be executed, and its nonce was not consumed.

Only then sign a replacement. The SDK's `Finalize` implements this procedure.

## HTTP 429 and rate limits

REST budgets use fixed 60-second windows and request weights. Every `/v1/*` request counts against the IP budget. Commands whose signer is verified as the stated principal also count against that account's budget; subaccounts share their main wallet's budget. Commands whose signer cannot be verified yet use a separate, smaller IP budget.

Read `ratelimit` and `ratelimit-policy`. Writes reaching the account-budget check also include `x-ratelimit-account`. A 429 response supplies `retry-after`, with `error.details.bucket` identifying `ip`, `account` or `unverified`. Wait accordingly and avoid concurrent retry bursts. Operators can adjust budgets; do not treat defaults as fixed service guarantees.

## Read after write and history pagination

A command's `seq` is its log position. For a subsequent REST read that must include this write, send `x-dexos-min-seq`. A lagging replica returns 412; preserve that minimum when retrying.

The first execution-history page returns `epoch` and a fixed `upper` bound. For later pages, use the previous page's `next` as `after` and pass back the same `epoch` and `upper`; missing boundaries return 400. Do not switch bounds or sort direction halfway through pagination.

409 `history_epoch_mismatch` means the ledger epoch changed: old cursors are no longer valid, so fetch a new first page and rebuild local state. 400 `GatewayHistoryIncomplete` means history through the requested bound is incomplete: retry the same request later. Correct other invalid parameters before retrying. See [WebSocket](websocket.md) for live-stream backfill.
