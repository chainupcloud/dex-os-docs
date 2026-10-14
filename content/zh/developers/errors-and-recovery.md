# 错误与恢复

REST 错误格式为 `{"error":{"code":"…","num":10000,"message":"…","details":{}}}`；这里的数值仅示意格式，实际以响应为准。`details` 可省略。用稳定的 `code` 和业务字段判断处理方式；保留 HTTP 状态、requestId 和响应正文用于排查。

## HTTP 状态

| 状态 | 含义与处理 |
| --- | --- |
| 400 | 参数、精度、分页边界等不合法；修正请求。历史提示 `not yet complete` 时可保留原边界稍后重试 |
| 401 | 签名检查失败；核对环境 domain、签名者、字段和整数缩放 |
| 403 | 所有权或 API wallet 授权范围不符；检查授权及有效期，资金操作使用有权限的钱包 |
| 404 | 对象不存在；回执查询须同时检查 `details.status` 和查询水位 |
| 409 | 冲突或历史纪元变化；根据具体错误重新建立状态 |
| 412 | 读副本尚未达到请求的最小 seq；保留一致性要求稍后再读 |
| 421 | 请求到达错误节点；检查该环境的公开 API 入口 |
| 422 | 业务拒绝；根据拒因修正操作，不能假设 nonce 未消耗 |
| 429 | 请求额度耗尽；遵循 `retry-after`，降低频率 |
| 5xx | 服务暂不可用或历史不完整；读可延后重试，写须先查原请求结果 |

## 202 和不确定的写结果

默认 `ack=result` 等待执行结果；超时可返回 HTTP 202、`status: "sequenced"` 和 `requestId`。这表示请求已定序，**不要重新下单**。显式 `ack=sequenced` 也只确认定序，不证明成交或业务成功。

保存写响应的 `requestId`，查询：

```text
GET /v1/requests/<requestId>
```

200 响应的 `status` 为 `pending`、`executed` 或 `rejected`。pending 时继续等待；最终结果可能包含 `nonceConsumed`、`reason`、`items`，应检查每项业务结论。批量操作 HTTP 200 不代表所有项成功。

回执查询的非 2xx 情况需要单独处理：

- 404，`details.status: "not_found"`：在 `details.asOfSeq` 所示水位内未找到，不代表跨所有未来水位永久不存在。
- 409，`details.status: "conflict"`：指定 nonce 被另一请求占用，检查 `details.conflictingRequest`，不要继续使用原 nonce。
- 503，`details.status: "history_unavailable"`：历史有缺口，当前无法证明请求是否执行；不能据此重发。

提供成对的 `scope`、`nonce` 可检测 nonce 冲突。API wallet 请求还可提供签名时的 `commandHash`；参数须来自原请求，具体格式见 API Reference。网络超时没有拿到响应时，也不能假设写失败：应使用原始签名对应的 requestId/SDK 回执能力核对结果，不要创建新 nonce 的重复业务请求。

## 429 与限流

REST 使用固定 60 秒窗口，按请求权重计数。所有 `/v1/*` 请求计入 IP 额度；通过签名预检查的写请求还计入主钱包额度，子账户共用主钱包额度。

读取 `ratelimit`、`ratelimit-policy`；到达钱包额度检查的写响应还含 `x-ratelimit-account`。429 返回 `retry-after`，并通过 `error.details.bucket` 区分 `ip` 或 `account`。按该值等待后再请求，不要并发密集重试。部署方可以调整额度，客户端不要把默认值当作固定服务承诺。

## 写后读和历史分页

写响应的 `x-dexos-seq` 表示提交位置。需要读到此次写的后续 REST 请求发送 `x-dexos-min-seq`，副本落后时返回 412；重新读取时保留这个最小值。

执行历史第一页返回 `epoch` 和固定上界 `upper`。继续翻页的 `after` 使用上一页的 `next`，并原样带回 `epoch`、`upper`；缺少边界会返回 400。不要跨分页混用新的上界或排序方向。

409 `history_epoch_mismatch` 表示账本纪元已改变；旧游标不再可用，重新获取第一页并重建本地状态。400 消息含 `not yet complete` 表示该上界的历史尚未完整，可以保留原请求稍后重试；其他 400 应先修正参数。WebSocket 补拉流程见 [WebSocket](websocket.md)。
