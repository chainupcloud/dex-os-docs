# WebSocket

Connect to `/v1/ws` in the same environment as your REST API. Use `wss://<API host>/v1/ws` for HTTPS environments. Send JSON text frames after connecting. One connection supports multiple channel subscriptions; order submission over WebSocket is not supported.

## Subscriptions and heartbeat

Replace `BTC-USD` with an actual market symbol from your environment.

```json
{"method":"subscribe","params":{"channel":"book","symbol":"BTC-USD","depth":50},"id":1}
```

The acknowledgement echoes `id` and includes the current ledger `epoch` and the start position `seq`. Every event after `seq` is sent on this subscription unless a `lagged` frame follows:

```json
{"channel":"subscribed","data":{"channel":"book","symbol":"BTC-USD","depth":50},"epoch":"<current epoch>","seq":593504256,"id":1}
```

To unsubscribe, send `method: "unsubscribe"` with the same `params`; the acknowledgement channel is `unsubscribed`. Unsubscribing a subscription the connection does not have returns an error frame with code `GatewayNotFound`. Each connection permits up to 200 subscriptions. The server closes a connection after 60 seconds without any client frame. Incoming market updates do not keep it alive: send a heartbeat, for example every 20 seconds:

```json
{"method":"ping"}
```

The response is `{"channel":"pong","data":{"ts":<Unix milliseconds>}}`. Protocol errors use `channel: "error"` with `data.code` and `data.message`. Errors answering a subscribe or unsubscribe also carry the request `id` (when provided), `data.method` and `data.subscription` (the request's `params` verbatim), so you can tell which request was refused. A protocol error alone does not close the connection.

## Channels and account selection

| Channel | Subscription parameters | Updates |
| --- | --- | --- |
| `prices` | None | All-market snapshot; changes coalesced per block |
| `book` | `symbol`, `kind?`, `depth?`, `aggTicks?` | Order book snapshot; changes coalesced per block |
| `bbo` | `symbol`, `kind?` | Best bid/ask snapshot; changes coalesced per block |
| `trades` | `symbol`, `kind?` | Each trade |
| `candles` | `symbol`, `kind?`, `interval` | Current candle updated on each fill |
| `funding` | `symbol`, `kind?` | Each funding settlement |
| `orders` | Account selection | Open-order snapshot, then individual order events |
| `fills` | Account selection | Each account fill |
| `positions` | Account selection | Position snapshot; changes coalesced per block |
| `account` | Account selection | Account snapshot; changes coalesced per block |
| `ledger` | Account selection | One frame per command, with its entries in `data.entries[]` |
| `events` | `symbol?`, `address?` | Raw execution events |

Select an account with `address` and optional `subaccount` (default 0), or with `vault` alone. `vault` is mutually exclusive with `address` and `subaccount`. For example, vault order subscription parameters are `{"channel":"orders","vault":"<vault id>"}`. Account channels require no signature: the same data is publicly readable through REST and is not confidential.

Add `kind` (`perp` or `spot`) when a perpetual and a spot market share a symbol. `book.depth` defaults to 20 and accepts 1–100; the REST book endpoint has a different maximum. `candles.interval` accepts the REST candle intervals. Prices and sizes are decimal strings.

## Snapshots and updates

`prices`, `book`, `bbo`, `account`, `positions`, and `orders` send an initial frame with `isSnapshot: true`. The first five then send changed state at block boundaries; do not expect a frame for every matching event.

Replace your entire open-order set with an orders snapshot; pending conditional orders are included as rows with `trigger`. Apply later order events idempotently by `orderId`: retain or update an order with `status: "open"`, and remove it for `filled`, `canceled`, or `expired`. When a conditional order is placed, triggered, rejected or auto-canceled, a fresh snapshot is sent instead. Candle frames contain the latest state of the current bar: replace that bar rather than adding each frame's volume.

`seq` is a ledger log position, not a consecutive channel message counter. A jump in seq alone does not prove packet loss. Private channel frames also carry `epoch`. Persist the fills `data.id` and the last `data.entries[].id` of each ledger frame: these are the `after` cursors for `/v1/account/fills` and `/v1/account/ledger`.

## Dropped frames and reconnecting

If the server falls behind its broadcast, it sends:

```json
{"channel":"lagged","data":{"dropped":128,"epoch":"<current epoch>","upper":"<seq>-<sub>-4294967295","reason":"buffer"}}
```

`reason: "buffer"` means the server-side broadcast fell behind and `dropped` events were dropped. `reason: "render"` means the connection could not render time-series frames, and `dropped` is 0. Frames that were not sent are never resent:

1. Replace local snapshot state with the new `isSnapshot: true` frames that follow.
2. Backfill fills and ledger separately from their last processed `data.id`, using the lagged frame's `epoch` and `upper` plus the original account selection.
3. Continue using each response's `next`, keeping the same `epoch` and `upper`, until `hasMore` is false. On 400 `GatewayHistoryIncomplete`, wait for history to be written and retry with the same boundaries.
4. This connection no longer sends fills/ledger frames at or below that upper bound, so the backfill and later live frames join without gaps or duplicates.

Request shapes (replace placeholders and URL-encode query values):

```text
GET /v1/account/fills?address=<wallet>&after=<last fill id>&epoch=<epoch>&upper=<upper>
GET /v1/account/ledger?vault=<vault id>&after=<last ledger id>&epoch=<epoch>&upper=<upper>
```

Without a saved cursor, first request a history page without `after`, save its returned `epoch` and `upper`, and paginate from there. Do not invent a last-received id.

After a network disconnect, reconnect and resubscribe. Compare the acknowledgement `epoch`: if it changed, discard old cursors and rebuild state. Otherwise, backfill time series from your last processed id up to `upper=<seq>-65535-4294967295`, using the `seq` from the new acknowledgement and the same `epoch`, and deduplicate by `id` when joining the backfill with the live frames. A new connection does not replay history by itself.
