# WebSocket

连接与 REST 同一环境的 `/v1/ws`。HTTPS 环境使用 `wss://<API 主机>/v1/ws`。连接建立后发送 JSON 文本帧；一个连接可以订阅多个频道。WebSocket 不支持下单。

## 订阅和心跳

以下示例的 `BTC-USD` 需替换为该环境实际存在的市场符号。

```json
{"method":"subscribe","params":{"channel":"book","symbol":"BTC-USD","depth":50},"id":1}
```

服务端确认订阅并回显 `id`，确认帧携带当前账本纪元 `epoch`：

```json
{"channel":"subscribed","data":{"channel":"book","symbol":"BTC-USD","depth":50},"epoch":"<当前纪元>","id":1}
```

取消时发送 `method: "unsubscribe"` 和相同的 `params`；确认帧的 `channel` 是 `unsubscribed`。每连接最多 200 个订阅。服务端在 60 秒没有收到客户端任何帧后关闭连接；即使行情持续到达，也要主动发送心跳，例如每 20 秒发送：

```json
{"method":"ping"}
```

回复为 `{"channel":"pong","data":{"ts":<Unix 毫秒>}}`。协议错误返回 `channel: "error"`，`data` 含 `code` 和 `message`，有请求 `id` 时回显该值；协议错误本身不会关闭连接。

## 频道和账户选择

| 频道 | 订阅参数 | 更新方式 |
| --- | --- | --- |
| `prices` | 无 | 全市场价格快照；按块合并更新 |
| `book` | `symbol`, `depth?` | 订单簿快照；按块合并更新 |
| `bbo` | `symbol` | 最优买卖价快照；按块合并更新 |
| `trades` | `symbol` | 每笔成交 |
| `candles` | `symbol`, `interval` | 每笔成交更新当前 K 线 |
| `funding` | `symbol` | 每次资金费结算 |
| `orders` | 账户选择 | 挂单快照，随后逐笔订单事件 |
| `fills` | 账户选择 | 每笔账户成交 |
| `positions` | 账户选择 | 仓位快照；按块合并更新 |
| `account` | 账户选择 | 账户快照；按块合并更新 |
| `ledger` | 账户选择 | 每条资金流水 |
| `events` | `symbol?`, `address?` | 原始执行事件 |

账户选择是 `address` 加可选 `subaccount`（默认 0），或单独使用 `vault`。`vault` 与 `address`、`subaccount` 互斥。例如，订阅金库订单的参数为 `{"channel":"orders","vault":"<金库号>"}`。账户频道无需签名；这些数据同样可通过公开 REST 接口查询，并非保密数据。

`book.depth` 默认 20，范围 1–100；REST 订单簿的深度上限不同。`candles.interval` 使用 REST K 线相同的取值。价格和数量为十进制字符串。

## 应用快照和增量

`prices`、`book`、`bbo`、`account`、`positions`、`orders` 在订阅后发送 `isSnapshot: true` 的当前快照。前五类之后在块边界按需推送变化；不要假设每个撮合事件都会产生一帧。

订单快照整体替换本地挂单集合。后续订单事件按 `orderId` 幂等应用：`status: "open"` 时保留或更新订单，`filled`、`canceled`、`expired` 时移除。K 线频道每次发送当前根的最新状态，应覆盖同一根 K 线，而非累加帧中的成交量。

`seq` 是账本日志位置，不是连续的频道消息编号；不可仅凭 seq 跳号判定丢帧。私有频道帧还携带 `epoch`。账户 `fills`、`ledger` 的 `data.id` 是对应 REST 历史接口使用的游标，应分别持久化。

## 丢帧与重连

服务端跟不上广播时发送：

```json
{"channel":"lagged","data":{"dropped":128,"epoch":"<当前纪元>","upper":"<seq>-<sub>-4294967295"}}
```

服务端不会重发被丢弃的流水。收到该帧后：

1. 快照类频道会收到新的 `isSnapshot: true`，用它替换本地状态。
2. 为 `fills` 和 `ledger` 分别从最后已处理的 `data.id` 补拉 REST；带上 lagged 提供的 `epoch` 和 `upper`，以及原账户选择参数。
3. 使用响应的 `next` 继续翻页，始终保持同一 `epoch`、`upper`，直到 `hasMore` 为 false。遇到 400 且消息含 `not yet complete`，等待历史写入后用同样边界重试。
4. 此连接随后不再发送位置小于等于该 `upper` 的 fills/ledger 帧；补拉与后续直播可据此衔接，并按 `data.id` 去重。

请求形式（尖括号内容需替换，并对查询参数编码）：

```text
GET /v1/account/fills?address=<钱包地址>&after=<最后成交id>&epoch=<纪元>&upper=<上界>
GET /v1/account/ledger?vault=<金库号>&after=<最后流水id>&epoch=<纪元>&upper=<上界>
```

若从未保存游标，先请求不带 `after` 的历史第一页，保存它返回的 `epoch`、`upper` 后分页；不能凭空构造一个“最后收到的 id”。

网络断开后建立新连接并重新订阅。先比较订阅确认的 `epoch`：纪元变化时丢弃旧游标并重建状态；相同时保留每个流水频道最后处理的 id。新连接没有自动历史重放，也没有提供历史上界的 reconnect 参数：可先请求不带 `after` 的 REST 第一页获取当前 `epoch`、`upper`，再以旧 id、该固定边界补拉，同时缓存新连接的流水帧，合并时按 id 去重。这个客户端流程仍需结合实际 SDK 做端到端验证。`lagged` 的无缺无重边界只适用于 fills/ledger，不应推广到所有频道。
