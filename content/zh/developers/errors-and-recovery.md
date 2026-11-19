# 错误与恢复

REST 错误格式为 `{"error":{"code":"…","num":10000,"message":"…","details":{}}}`。这里的数字只示意结构，请以实际响应为准；`details` 可选。程序应按稳定的 `code` 和业务字段判断，同时保留 HTTP 状态、requestId 和响应正文用于排查。

## HTTP 状态码

| 状态 | 含义与处理 |
| --- | --- |
| 400 | 参数、精度、编码或分页边界无效，修正请求。`GatewayHistoryIncomplete` 表示历史尚未写完，稍后用相同边界重试。被 400 拒绝的命令没有定序 |
| 401 | 在网关预检签名的接口上，签名预检未通过 |
| 403 | 所有权、范围或 builder 预检拒绝；在这里被拒的命令没有定序 |
| 404 | 对象不存在；回执查询以 404 返回状态 `Unknown`（见下文） |
| 409 | 冲突：`clientOrderId` 重复、同一 actionId 被另一份不同 digest 的原件受理，或分页时账本纪元已变化 |
| 412 | 只读副本未达到你要求的 seq；保持该一致性要求重试 |
| 413 / 415 / 408 | 命令正文过大、不是 `application/json`，或读取正文超时；命令没有提交 |
| 421 | 节点只读或不是主节点；把同一条命令发到主节点入口 |
| 422 | 定序前的业务拒绝（如 `GatewayCollateralTokenMismatch`），nonce 没有消耗 |
| 429 | 请求预算耗尽；遵守 `retry-after` 并降低请求频率 |
| 5xx | 服务不可用。对命令而言，503 可能表示结果未知：先弄清结论，再发新的请求 |

## 命令的结论

`POST /v1/commands` 在命令定序后返回 202。这只证明已定序，不证明授权通过或已经执行：`executionKnown` 为 false，`nonceConsumed` 为 null。保存原命令字节、`requestId`（即 actionId）和 `digest`，然后查询：

```text
GET /v1/requests/<requestId>?digest=<digest>
```

| 回执状态 | 含义 |
| --- | --- |
| `Accepted` | 账本已受理；结果可能尚未落定（`resultsPending`） |
| `Executed` | 已执行。业务结果在 `events`，批量命令的逐项结论在 `items`，业务拒绝在 `businessRejected`；每一项都要检查 |
| `AuthorizationRejected` | 账本在授权环节拒绝了这条命令；没有执行，nonce 没有消耗 |
| `Unknown`（HTTP 404） | 读视图里没有这条命令的记录。单凭这一点不能证明它从未执行 |
| HTTP 409 | 同一 actionId 被另一份不同 digest 的原件受理，例如改了有效期后重签的副本 |

原样重发同一份命令字节是安全的：如果账本已受理，网关返回 200、第一次的回执和 `duplicate: true`，不会再次定序。改了有效期或 nonce 重新签名则是另一条命令，可能执行两次。

## 弄清未知结果

网络超时、5xx 或 `Unknown` 回执都不能证明写入失败。命令过了 `validUntilMs` 之后就不会再被受理，据此可以得到确定结论：

1. 等到 `GET /v1/time/certified` 给出的认证时间超过该命令的 `validUntilMs`。
2. 用同一次时间响应里的 `hostLogIndex` 作为 `x-dexos-min-seq` 查询回执。返回 412 表示副本还没追上，稍后重试。
3. `Executed` 表示已经执行，从回执读取结果；`Unknown` 或 `AuthorizationRejected` 表示这条命令没有执行、以后也不会执行，nonce 没有消耗。

确认之后再签替代命令。SDK 的 `Finalize` 实现了这一流程。

## HTTP 429 与限流

REST 预算以固定 60 秒窗口按请求权重计算。所有 `/v1/*` 请求都计入 IP 预算。签名者核实为所声明主体的命令另计入该账户的预算，子账户共享主钱包的预算。暂时无法核实签名者的命令改用一个独立的、额度更小的 IP 预算。

读取 `ratelimit` 和 `ratelimit-policy`；进入账户预算检查的写入还会带 `x-ratelimit-account`。429 响应带 `retry-after`，`error.details.bucket` 为 `ip`、`account` 或 `unverified`。按要求等待，避免并发重试集中爆发。运营方可以调整预算，不要把默认值当作固定的服务承诺。

## 写后读与历史分页

命令的 `seq` 是它在日志中的位置。后续 REST 读取必须包含这次写入时，带上 `x-dexos-min-seq`。副本落后会返回 412，重试时保留这个最低要求。

执行历史的第一页返回 `epoch` 和固定上界 `upper`。后续页把上一页的 `next` 作为 `after`，并原样带回同一个 `epoch` 和 `upper`；缺少边界会返回 400。翻页中途不要更换边界或排序方向。

409 `history_epoch_mismatch` 表示账本纪元已变化：旧游标失效，需要重新拉第一页并重建本地状态。400 `GatewayHistoryIncomplete` 表示请求边界内的历史尚未写完：稍后原样重试。其他参数错误先修正再重试。实时流的补拉见 [WebSocket](websocket.md)。
