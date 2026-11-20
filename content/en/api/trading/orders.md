# Orders

Signed by: account or API wallet (only for the accounts, markets and operations its grant covers). Nonce lane: `trade`.

| Command | Use | Go SDK (`dexos` package) |
|---|---|---|
| `PlaceOrder` | Place an order: market, side, price, size, time in force, reduce-only, optional `clientOrderId` | `EncodePlaceOrder` |
| `CancelOrder` | Cancel a resting order | `EncodeCancelOrder` |
| `ModifyOrder` | Change a resting order's price, size or expiry | `EncodeModifyOrder` |
| `BatchPlace` | Place several orders at once | `EncodeBatchPlace` |
| `BatchCancel` | Cancel several orders at once | `EncodeBatchCancel` |
| `BatchReplace` | Cancel, then place, in one command | `EncodeBatchReplace` |
| `BatchReplace2` | Cancel, modify and place in one command | `EncodeBatchReplace2` |
| `BatchReplace3` | Like `BatchReplace2`; cancels and modifies can also reference this batch's new orders by position | `EncodeBatchReplace3` |
| `ScheduleCancel` | Cancel all orders at a set time (dead man's switch) | `EncodeScheduleCancel` |
| `PlaceConditional` | Place a conditional order: a limit order placed once the price crosses the trigger | `EncodePlaceConditional` |
| `CancelConditional` | Cancel an untriggered conditional order | `EncodeCancelConditional` |
| `PlaceTpslPair` | Attach a take-profit / stop-loss pair to a position or an order | `EncodePlaceTpslPair` |
| `PlaceTwap` | Place a TWAP order filled in slices at a fixed interval | `EncodePlaceTwap` |
| `CancelTwap` | Cancel a running TWAP order | `EncodeCancelTwap` |
| `SetLeverage` | Set the leverage for a market | `EncodeSetLeverage` |

- `clientOrderId` is optional; rules in [`POST /v1/commands`](../trading.md). TWAP and TP/SL orders have none; cancels and modifies use `orderId`.
- `wait=match` applies to order commands only: the response carries the outcome once matched.
- Orders routed through a builder pass the builder checks; error codes in [`POST /v1/commands`](../trading.md).
