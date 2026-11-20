# 下单与撤单

签名方：账户或 API 钱包（只限授权范围内的账户、市场和操作）。nonce 车道：`trade`。

| 命令 | 作用 | Go SDK（`dexos` 包） |
|---|---|---|
| `PlaceOrder` | 下单：市场、方向、价格、数量、有效方式、是否只减仓，可带 `clientOrderId` | `EncodePlaceOrder` |
| `CancelOrder` | 撤一笔挂单 | `EncodeCancelOrder` |
| `ModifyOrder` | 改一笔挂单的价格、数量或有效期 | `EncodeModifyOrder` |
| `BatchPlace` | 一次下多笔单 | `EncodeBatchPlace` |
| `BatchCancel` | 一次撤多笔单 | `EncodeBatchCancel` |
| `BatchReplace` | 一条命令里先撤后下 | `EncodeBatchReplace` |
| `BatchReplace2` | 一条命令里撤单、改单、下单 | `EncodeBatchReplace2` |
| `BatchReplace3` | 同 `BatchReplace2`，撤单和改单还可以按位置引用本批次新下的订单 | `EncodeBatchReplace3` |
| `ScheduleCancel` | 定时全部撤单（死人开关） | `EncodeScheduleCancel` |
| `PlaceConditional` | 下条件单：价格越过触发价后按限价下单 | `EncodePlaceConditional` |
| `CancelConditional` | 撤一笔未触发的条件单 | `EncodeCancelConditional` |
| `PlaceTpslPair` | 为仓位或某笔订单挂一对止盈止损 | `EncodePlaceTpslPair` |
| `PlaceTwap` | 下 TWAP 单，按固定间隔分片成交 | `EncodePlaceTwap` |
| `CancelTwap` | 撤一笔进行中的 TWAP 单 | `EncodeCancelTwap` |
| `SetLeverage` | 设置某个市场的杠杆 | `EncodeSetLeverage` |

- `clientOrderId` 是可选项，规则见 [`POST /v1/commands`](../trading.md)。TWAP 和止盈止损单没有这一项；撤单和改单用 `orderId`。
- `wait=match` 只适用于下单类命令：撮合完成后直接返回结果。
- 经 builder 下的单要通过 builder 的检查，错误码见 [`POST /v1/commands`](../trading.md)。
