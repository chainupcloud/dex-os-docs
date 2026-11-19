# WebSocket

连接与 REST 同一环境的 `/v1/ws`。HTTPS 环境使用 `wss://<API 主机>/v1/ws`。连接建立后发送 JSON 文本帧；一个连接可以订阅多个频道。WebSocket 不支持下单。

## 订阅和心跳

以下示例的 `BTC-USD` 需替换为该环境实际存在的市场符号。

```json
{"method":"subscribe","params":{"channel":"book","symbol":"BTC-USD","depth":50},"id":1}
```

服务端确认订阅并回显 `id`，确认帧携带当前账本纪元 `epoch` 和起始位置 `seq`。`seq` 之后的每个事件都会在这个订阅上推送，除非随后收到 `lagged` 帧：

```json
{"channel":"subscribed","data":{"channel":"book","symbol":"BTC-USD","depth":50},"epoch":"<当前纪元>","seq":593504256,"id":1}
```

取消时发送 `method: "unsubscribe"` 和相同的 `params`；确认帧的 `channel` 是 `unsubscribed`。取消一个本连接上不存在的订阅会返回错误帧，错误码为 `GatewayNotFound`。每连接最多 200 个订阅。服务端在 60 秒没有收到客户端任何帧后关闭连接；即使行情持续到达，也要主动发送心跳，例如每 20 秒发送：

```json
{"method":"ping"}
```

回复为 `{"channel":"pong","data":{"ts":<Unix 毫秒>}}`。协议错误返回 `channel: "error"`，`data` 含 `code` 和 `message`。回应订阅或取消订阅的错误帧还会回显请求 `id`（如有）、`data.method` 和 `data.subscription`（原样的请求 `params`），便于判断哪个请求被拒。协议错误本身不会关闭连接。

## 频道和账户选择

| 频道 | 订阅参数 | 更新方式 |
| --- | --- | --- |
| `prices` | 无 | 全市场价格快照；按块合并更新 |
| `book` | `symbol`, `kind?`, `depth?`, `aggTicks?` | 订单簿快照；按块合并更新 |
| `bbo` | `symbol`, `kind?` | 最优买卖价快照；按块合并更新 |
| `trades` | `symbol`, `kind?` | 每笔成交 |
| `candles` | `symbol`, `kind?`, `interval` | 每笔成交更新当前 K 线 |
| `funding` | `symbol`, `kind?` | 每次资金费结算 |
| `orders` | 账户选择 | 挂单快照，随后逐笔订单事件 |
| `fills` | 账户选择 | 每笔账户成交 |
| `positions` | 账户选择 | 仓位快照；按块合并更新 |
| `account` | 账户选择 | 账户快照；按块合并更新 |
| `ledger` | 账户选择 | 每条命令一帧，流水在 `data.entries[]` |
| `events` | `symbol?`, `address?` | 原始执行事件 |

账户选择是 `address` 加可选 `subaccount`（默认 0），或单独使用 `vault`。`vault` 与 `address`、`subaccount` 互斥。例如，订阅金库订单的参数为 `{"channel":"orders","vault":"<金库号>"}`。账户频道无需签名；这些数据同样可通过公开 REST 接口查询，并非保密数据。

永续和现货市场同名时加 `kind`（`perp` 或 `spot`）。`book.depth` 默认 20，范围 1–100；REST 订单簿的深度上限不同。`candles.interval` 使用 REST K 线相同的取值。价格和数量为十进制字符串。

## 应用快照和增量

`prices`、`book`、`bbo`、`account`、`positions`、`orders` 在订阅后发送 `isSnapshot: true` 的当前快照。前五类之后在块边界按需推送变化；不要假设每个撮合事件都会产生一帧。

订单快照整体替换本地挂单集合，未触发的条件单也在快照里（带 `trigger` 的行）。后续订单事件按 `orderId` 幂等应用：`status: "open"` 时保留或更新订单，`filled`、`canceled`、`expired` 时移除。条件单下单、触发、被拒或被自动撤销时，服务端改发一份新快照。K 线频道每次发送当前根的最新状态，应覆盖同一根 K 线，而非累加帧中的成交量。

`seq` 是账本日志位置，不是连续的频道消息编号；不可仅凭 `seq` 跳号判定丢帧。私有频道帧还携带 `epoch`。`fills` 的 `data.id` 和每个 `ledger` 帧最后一条 `data.entries[].id` 分别是 `/v1/account/fills`、`/v1/account/ledger` 的 `after` 游标，应分别持久化。

## 丢帧与重连

服务端跟不上广播时发送：

```json
{"channel":"lagged","data":{"dropped":128,"epoch":"<当前纪元>","upper":"<seq>-<sub>-4294967295","reason":"buffer"}}
```

`reason: "buffer"` 表示服务端广播落后，丢弃了 `dropped` 个事件；`reason: "render"` 表示该连接无法生成流水类帧，此时 `dropped` 为 0。没有发出的帧永远不会补发。收到该帧后：

1. 快照类频道会收到新的 `isSnapshot: true`，用它替换本地状态。
2. 为 `fills` 和 `ledger` 分别从最后已处理的 `data.id` 补拉 REST；带上 `lagged` 帧提供的 `epoch` 和 `upper`，以及原账户选择参数。
3. 使用响应的 `next` 继续翻页，始终保持同一 `epoch`、`upper`，直到 `hasMore` 为 `false`。遇到 400 `GatewayHistoryIncomplete`，等待历史写入后用同样边界重试。
4. 此连接随后不再发送位置小于等于该 `upper` 的 `fills` / `ledger` 频道帧，补拉结果与后续直播可以无缺无重地衔接。

请求形式（尖括号内容需替换，并对查询参数编码）：

```text
GET /v1/account/fills?address=<钱包地址>&after=<最后成交id>&epoch=<纪元>&upper=<上界>
GET /v1/account/ledger?vault=<金库号>&after=<最后流水id>&epoch=<纪元>&upper=<上界>
```

若从未保存游标，先请求不带 `after` 的历史第一页，保存它返回的 `epoch`、`upper` 后分页；不能凭空构造一个“最后收到的 `id`”。

网络断开后建立新连接并重新订阅。先比较订阅确认的 `epoch`：纪元变化时丢弃旧游标并重建状态。纪元不变时，从最后处理的 `id` 补拉流水类数据，上界取 `upper=<seq>-65535-4294967295`（`seq` 用新确认帧里的值），并带同一个 `epoch`；补拉结果与直播帧合并时按 `id` 去重。新连接本身不会重放历史。
