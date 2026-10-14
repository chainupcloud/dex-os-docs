# REST API 使用约定

v1 使用 `/v1` 前缀、JSON、camelCase 字段和 Unix 毫秒时间戳。完整参数与响应以目标网关提供的 OpenAPI 为准；网关上的 Scalar 入口为 `/docs?spec=v1`，原始规格为 `/app/openapi-v1.json`。文档仓库提供[可下载的 OpenAPI 副本](https://raw.githubusercontent.com/chainupcloud/dex-os-docs/6a3f08872ba918fe24f0927fde0e4c08a9a4de79/api/openapi-v1.json)。本页解释调用流程，不复制整份接口定义。

## 接口选择

| 目的 | 入口 |
|---|---|
| 环境与签名配置 | `/v1/exchange`、`/v1/time` |
| 市场与行情 | `/v1/markets`、`/v1/prices`、`/v1/markets/{symbol}/book`、`/trades`、`/candles`、`/funding`（后面三项接在市场路径后） |
| 账户状态 | `/v1/account`、`/v1/account/positions`、`/v1/account/orders` |
| 成交与账本 | `/v1/account/fills`、`/v1/account/ledger`、`/v1/account/orders/history` |
| 订单写入 | `/v1/orders`、`/v1/orders/cancel`、`/v1/orders/replace` |
| 授权与资金 | `/v1/account/agents/*`、`/v1/account/withdraw`、`/v1/account/transfer` |
| 金库 | `/v1/vaults`、`/v1/vaults/{id}` 及对应动作端点 |
| 请求结论与补拉 | `/v1/requests/{requestId}`、`/v1/events` |

读取账户时使用 `address` 和可选 `subaccount`，或单独使用 `vault`。写入使用签名信封的 `account`；两种参数名不要混用。订单编号 `orderId` 是字符串。不要将所有数值字符串强制转为 JavaScript Number。

## 写请求的结果

默认 `ack=result` 等待执行结果。单笔订单返回业务结论；批量返回 `items`，每项可能成功或被拒绝，需要逐项检查。`ack=sequenced` 只确认定序位置，不代表业务成功。`waitMs` 只适用于 `ack=result`，范围为 0–5000 毫秒；0 表示不等待。

HTTP 202 表示已定序但等待期间未取得结论。保存 `requestId`、`seq`、`sub` 和原始请求，查询 `/v1/requests/{requestId}`。网络断开也可能发生在服务已接收之后，应先对账。回执查询返回历史缺口时，不能把“无法证明执行”当作“没有执行”。

`clientOrderId` 可用于客户端订单关联和重复检查。已定序但尚未取得结果的映射可在之后从执行历史解析；不要把最初的在途状态当作订单不存在。具体格式、重复提交语义和支持场景需查订单端点定义。

## 写后读的一致性

写回执携带 `x-dexos-seq`。紧接着读取这次写入的结果时，把该值放入 `x-dexos-min-seq`。副本未追上会返回 412，而不是静默提供旧结果。该头用于写后读，不应为所有行情轮询附加一个不断增长的水位。

412 可能来自执行账本 `ledger` 或异步分析投影 `projection`。执行层已经完成不代表分析数据已落库。检查错误详情，等待相应数据源追上；切换副本前也应确认目标副本的进度。

## 历史分页

成交、账本和事件等接口使用 `limit`、`after`，部分接口还使用 `upper` 与 `epoch`。先读取第一页，之后使用响应 `next` 作为 `after`，保留同一轮响应中的固定 `upper` 和 `epoch`，直到 `hasMore=false`。不要自行对游标加一，也不要从时间戳推导游标。

```bash
: "${DEXOS_API_URL:?请设置 API 基础地址}"
: "${DEXOS_ADDRESS:?请设置主钱包地址}"
curl --fail-with-body --silent --show-error --get \
  "$DEXOS_API_URL/v1/account/fills" \
  --data-urlencode "address=$DEXOS_ADDRESS" \
  --data-urlencode "limit=100"
```

后续页将第一轮响应中的值原样设置到 `DEXOS_AFTER`、`DEXOS_UPPER`、`DEXOS_EPOCH`：

```bash
: "${DEXOS_AFTER:?请设置响应中的 next}"
: "${DEXOS_UPPER:?请设置固定 upper}"
: "${DEXOS_EPOCH:?请设置响应中的 epoch}"
curl --fail-with-body --silent --show-error --get \
  "$DEXOS_API_URL/v1/account/fills" \
  --data-urlencode "address=$DEXOS_ADDRESS" \
  --data-urlencode "limit=100" \
  --data-urlencode "after=$DEXOS_AFTER" \
  --data-urlencode "upper=$DEXOS_UPPER" \
  --data-urlencode "epoch=$DEXOS_EPOCH"
```

WebSocket 断线后可通过成交或事件接口补拉。按稳定事件 id 去重，并处理历史不可用的显式错误。按 symbol 过滤的事件页可能为空，但仍有 `next` 和 `hasMore`；不要遇到空页就停止。

## 错误与限流

业务 API 错误使用 `{error:{code,num,message,details?}}`。程序按稳定的 `code` 分支，保留 HTTP 状态和 `details` 用于排查，不要解析英文 message。损坏的 HTTP 或 JSON 也可能由 HTTP 框架直接拒绝，客户端需要处理无法解析 JSON 的响应。

| 状态 | 处理方向 |
|---|---|
| 400 | 修正参数、类型或格式 |
| 401 | 检查签名与签名域 |
| 403 | 检查所有权、API 钱包授权和操作范围 |
| 404 | 核对账户、市场、订单或资源身份 |
| 409 | 检查冲突详情与已有请求 |
| 412 | 等待写后读需要的账本或投影水位 |
| 421 | 核对请求入口与节点角色 |
| 422 | 处理业务拒因；不要把它当网络故障 |
| 429 | 按 `retry-after` 等待，降低请求权重 |
| 5xx / 连接异常 | 写入先查回执和对账，再决定下一步 |

限流分 IP 和写入账户两层，以固定 60 秒窗口累计权重。普通读权重 1，盘口与价格 2，历史类 5；写请求基础权重 1，批量再加 `floor(n / 40)`。实际预算可由运营方调整，以响应 `ratelimit`、`ratelimit-policy`、`x-ratelimit-account` 为准。429 的 `details.bucket` 区分 IP 和账户预算。
