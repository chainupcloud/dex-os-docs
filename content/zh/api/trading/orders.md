# 订单

下面每个示例都是命令的 JSON 形态，即需要你填的字段。SDK（或 [API 调试台](https://dex-preview.unibook.site/app/api-playground/)）再补上 nonce 与有效期、签名并编码；HTTP 请求一律是 `POST /v1/commands`，请求体 `{"command":"0x…"}`。调试台在预览网络上运行，用临时私钥和测试资金，会逐步显示读 nonce、EIP-712 待签数据、签好的命令、响应与回执，并能把提交复制成 curl。

## 完整下单流程

下面是在预览网络上的一次真实运行（2026-11-23）：在 `PUMPDEX:BTC-USDC` 下一笔买入限价单，价格比买一低 1%，挂在簿上。响应只保留相关字段。

**1. 读市场。** 永续和现货可以同名，要带 `kind`。

```bash
export DEXOS_API_URL=https://dex-preview.unibook.site
curl -sS "$DEXOS_API_URL/v1/markets/PUMPDEX:BTC-USDC?kind=perp"
```

```json
{
  "symbol": "PUMPDEX:BTC-USDC",
  "kind": "perp",
  "signingMarketId": 0,
  "priceDecimals": 1,
  "sizeDecimals": 5,
  "tickSize": "0.1",
  "lotSize": "0.00001",
  "bestBid": "61456.2",
  "bestAsk": "61512.7"
}
```

价格 60841.6 → `608416` tick（`priceDecimals` 为 1，是 `tickSize` 0.1 的整数倍）。数量 0.0001 → `10` lot（`sizeDecimals` 为 5）。

**2. 读账户号与 nonce。**

```bash
curl -sS "$DEXOS_API_URL/v1/account/nonce?address=<主钱包地址>&lane=trade"
```

```json
{
  "signingAccountId": 22,
  "policyId": "21",
  "policyEpoch": "1",
  "lane": "trade",
  "nonce": 0
}
```

`signingAccountId` 填进命令的 `account`；`policyId`、`policyEpoch` 与 `nonce` 进签名。SDK 会自己读。

**3. 构造并签名。** 命令：

```json
{
  "kind": "PlaceOrder",
  "account": 22,
  "market": 0,
  "side": "buy",
  "price": 608416,
  "lots": 10,
  "tif": "gtc",
  "reduceOnly": false,
  "clientOrderId": "my-order-1"
}
```

用 Go SDK、由 API 钱包签名（授权 API 钱包见[签名与授权](../../developers/authentication.md)）：

```go
c := dexosv1.NewClient("https://dex-preview.unibook.site")
agent, _ := dexos.NewSigner("0x<API 钱包私钥>")
s, err := dexosv1.NewSession(ctx, c, agent, dexosv1.AccountRef{Address: owner, Subaccount: 0})
if err != nil { log.Fatal(err) }
cat, _ := c.Catalog(ctx)
btc, _ := cat.Lookup("PUMPDEX:BTC-USDC", dexosv1.KindPerp)
px, _ := btc.Scale.Ticks("60841.6")
sz, _ := btc.Scale.Lots("0.0001")
res, err := s.Place(ctx, dexosv1.OrderRequest{Market: btc, Side: dexos.Buy, Price: px, Lots: sz, TIF: dexos.GTC})
```

签名对象是 EIP-712 类型数据 `AuthorizedAction`（域 `DEXOS/Account`），其中 `payloadHash` 绑定命令内容。签好的命令按 hex 编码后提交。

**4. 提交。**

```bash
curl -sS -X POST "$DEXOS_API_URL/v1/commands" \
  -H 'content-type: application/json' \
  -d '{"command":"0x018b219989ec3b852c5c95abd1b78fee8af8414bf5f84da4d9bbad4b94fd3a23…"}'
```

```json
{
  "requestId": "0x995910d9c9ef28b83773bc70a520f18bb5bed0676fdf9ff770d9ee2e56eac081",
  "digest": "0xd28c37d529c380d55e4250bea574554d9e13978ffa3fb6b94379e103580cfd66",
  "seq": "92286230",
  "sub": 0,
  "status": "Accepted",
  "duplicate": false
}
```

202 只表示已定序，还没执行。记下 `requestId`。

**5. 查回执**，直到 `status` 为 `Executed`（或 `AuthorizationRejected`）；404 表示还查不到，稍后再问。

```bash
curl -sS "$DEXOS_API_URL/v1/requests/0x995910d9c9ef28b83773bc70a520f18bb5bed0676fdf9ff770d9ee2e56eac081"
```

```json
{
  "status": "Executed",
  "outcome": "Succeeded",
  "nonceConsumed": true,
  "events": [
    {
      "kind": "OrderAccepted",
      "data": {
        "account": 22,
        "filledLots": 0,
        "lots": 10,
        "market": 0,
        "orderSeq": 6048070369280,
        "price": 608416,
        "resting": true
      }
    }
  ]
}
```

`OrderAccepted.orderSeq` 就是单号；`resting: true` 表示挂在簿上。业务被拒时回执带 `businessRejected` 与拒因。

**6. 查挂单。**

```bash
curl -sS "$DEXOS_API_URL/v1/account/orders?address=<主钱包地址>"
```

```json
{
  "orders": [
    {
      "orderId": "6048070369280",
      "clientOrderId": "my-order-1",
      "symbol": "PUMPDEX:BTC-USDC",
      "kind": "perp",
      "side": "buy",
      "price": "60841.6",
      "size": "0.0001",
      "tif": "gtc",
      "status": "open"
    }
  ]
}
```

撤单时同样签一条 `CancelOrder`，`"order": "6048070369280"`。[在 API 调试台里跑一遍](https://dex-preview.unibook.site/app/api-playground/?cmd=PlaceOrder)：它会建临时账户、领测试 USDC，然后可以下单、撤单。

## 字段

| 字段 | 含义 |
|---|---|
| `account` | 账本账户号：`GET /v1/account/nonce` 返回的 `signingAccountId` |
| `market` | 市场号：`GET /v1/markets` 返回的 `signingMarketId` |
| `side` | `buy` 或 `sell` |
| `price` | 限价，以 tick 计：价格 × 10^`priceDecimals`，须是同样换算后 `tickSize` 的整数倍。60841.6、`priceDecimals` 为 1 → `608416` |
| `lots` | 数量，以 lot 计：数量 × 10^`sizeDecimals`，须是同样换算后 `lotSize` 的整数倍。0.0001、`sizeDecimals` 为 5 → `10` |
| `tif` | 有效方式：`gtc`、`ioc`、`post_only` 或 `fok` |
| `reduceOnly` | `true`：只减仓 |
| `clientOrderId` | 可选，1–36 个 `A-Z a-z 0-9 . _ : / -` 字符，账户内不可重复 |
| `order` | 单号：`GET /v1/account/orders` 的 `orderId`，或回执里 `OrderAccepted` 事件的 `orderSeq`。十进制字符串 |

64 位数值（单号、金额、时间）可以写成十进制字符串。

## 订单

### PlaceOrder

下一笔限价单。

签名：账户或 API 钱包（限授权范围内） · nonce 序列 `trade`

`goodTilMs`（可选）是到期时间，Unix 毫秒；`clientOrderId` 可选。

```json
{
  "kind": "PlaceOrder",
  "account": 1234,
  "market": 1,
  "side": "buy",
  "price": 6000000,
  "lots": 10,
  "tif": "gtc",
  "reduceOnly": false,
  "clientOrderId": "my-order-1"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=PlaceOrder)

### CancelOrder

撤销一笔挂单。

签名：账户或 API 钱包（限授权范围内） · nonce 序列 `trade`

```json
{
  "kind": "CancelOrder",
  "account": 1234,
  "order": "4294967297"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=CancelOrder)

### ModifyOrder

修改挂单的价格、数量、有效方式或只减仓标记。

签名：账户或 API 钱包（限授权范围内） · nonce 序列 `trade`

改单等于替换原单：新单被拒时原单也一并撤销。

```json
{
  "kind": "ModifyOrder",
  "account": 1234,
  "order": "4294967297",
  "price": 5999999,
  "lots": 10,
  "tif": "gtc",
  "reduceOnly": false
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=ModifyOrder)

### BatchPlace

一条命令下多笔单。

签名：账户或 API 钱包（限授权范围内） · nonce 序列 `trade`

`orders`：每项含 `market`、`side`、`price`、`lots`、`tif`、`reduceOnly`，可带 `clientOrderId`。回执的 `items` 里逐项给结果。

```json
{
  "kind": "BatchPlace",
  "account": 1234,
  "orders": [
    {
      "market": 1,
      "side": "buy",
      "price": 6000000,
      "lots": 10,
      "tif": "gtc",
      "reduceOnly": false
    },
    {
      "market": 1,
      "side": "buy",
      "price": 5999999,
      "lots": 10,
      "tif": "gtc",
      "reduceOnly": false
    }
  ]
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=BatchPlace)

### BatchCancel

一条命令撤多笔单。

签名：账户或 API 钱包（限授权范围内） · nonce 序列 `trade`

`orders`：单号列表。

```json
{
  "kind": "BatchCancel",
  "account": 1234,
  "orders": [
    "4294967297"
  ]
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=BatchCancel)

### BatchReplace

一条命令里先撤单、再下新单。

签名：账户或 API 钱包（限授权范围内） · nonce 序列 `trade`

`cancels`：先撤的单号；`orders`：新单，写法同 `BatchPlace`。

```json
{
  "kind": "BatchReplace",
  "account": 1234,
  "cancels": [
    "4294967297"
  ],
  "orders": [
    {
      "market": 1,
      "side": "buy",
      "price": 5999999,
      "lots": 10,
      "tif": "gtc",
      "reduceOnly": false
    }
  ]
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=BatchReplace)

### BatchReplace2

一条命令里撤单、改单、下新单。

签名：账户或 API 钱包（限授权范围内） · nonce 序列 `trade`

`modifies`：每项含 `order`、`price`、`lots`、`tif`、`reduceOnly`。

```json
{
  "kind": "BatchReplace2",
  "account": 1234,
  "cancels": [],
  "modifies": [
    {
      "order": "4294967297",
      "price": 5999998,
      "lots": 10,
      "tif": "gtc",
      "reduceOnly": false
    }
  ],
  "orders": [
    {
      "market": 1,
      "side": "buy",
      "price": 5999999,
      "lots": 10,
      "tif": "gtc",
      "reduceOnly": false
    }
  ]
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=BatchReplace2)

### BatchReplace3

同 `BatchReplace2`；撤单和改单还可以指向更早一笔 `BatchReplace3` 挂出、还不知道单号的单。

签名：账户或 API 钱包（限授权范围内） · nonce 序列 `trade`

`cancels` 的一项或改单的 `target` 可以是单号，也可以是 `{"market", "seq", "sub", "item"}`：`seq`、`sub` 取同一账户更早一笔 `BatchReplace3` 提交时 202 响应里的值，`item` 是新单在它 `orders` 里的位置。引用 60 秒内有效，过期返回 `ReferenceOutOfRange`。这里的 `orders` 不带 `clientOrderId`。

```json
{
  "kind": "BatchReplace3",
  "account": 1234,
  "cancels": [],
  "modifies": [
    {
      "target": "4294967297",
      "price": 5999998,
      "lots": 10,
      "tif": "gtc",
      "reduceOnly": false
    }
  ],
  "orders": [
    {
      "market": 1,
      "side": "buy",
      "price": 5999999,
      "lots": 10,
      "tif": "gtc",
      "reduceOnly": false
    }
  ]
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=BatchReplace3)

### ScheduleCancel

到指定时间撤掉全部挂单（断线保护）。重发一次就把时间往后推。

签名：账户或 API 钱包（限授权范围内） · nonce 序列 `trade`

`triggerMs`：按账本时间的 Unix 毫秒。

```json
{
  "kind": "ScheduleCancel",
  "account": 1234,
  "triggerMs": "1764000060000"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=ScheduleCancel)

### PlaceConditional

下条件单：价格穿过触发价后才挂出的限价单。

签名：账户或 API 钱包（限授权范围内） · nonce 序列 `trade`

`triggerPrice` 以 tick 计；`triggerAbove` 为 `true` 时价格涨到触发价才触发，`false` 为跌到。

```json
{
  "kind": "PlaceConditional",
  "account": 1234,
  "market": 1,
  "side": "buy",
  "price": 6000000,
  "lots": 10,
  "tif": "gtc",
  "reduceOnly": false,
  "triggerPrice": 6000000,
  "triggerAbove": true
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=PlaceConditional)

### CancelConditional

撤销还没触发的条件单。

签名：账户或 API 钱包（限授权范围内） · nonce 序列 `trade`

```json
{
  "kind": "CancelConditional",
  "account": 1234,
  "order": "4294967297"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=CancelConditional)

### PlaceTpslPair

给仓位或订单挂一对止盈止损。

签名：账户或 API 钱包（限授权范围内） · nonce 序列 `trade`

`closeSide` 是平仓方向。`tpTrigger` / `slTrigger` 是触发价，`tpPrice` / `slPrice` 是限价，都以 tick 计。`positionTpsl: true` 挂在仓位上；挂在订单上时设为 `false`，并用 `parent` 给出单号。

```json
{
  "kind": "PlaceTpslPair",
  "account": 1234,
  "market": 1,
  "closeSide": "sell",
  "lots": 10,
  "tpTrigger": 6000100,
  "tpPrice": 6000090,
  "slTrigger": 5999900,
  "slPrice": 5999890,
  "positionTpsl": true
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=PlaceTpslPair)

### PlaceTwap

下 TWAP 单：按固定间隔分成等份成交。

签名：账户或 API 钱包（限授权范围内） · nonce 序列 `trade`

`totalLots` 分成 `slices` 笔，每 `intervalMs` 一笔；每笔偏离参考价不超过 `priceTolerancePpm`（百万分比）。

```json
{
  "kind": "PlaceTwap",
  "account": 1234,
  "market": 1,
  "side": "buy",
  "totalLots": "40",
  "slices": 4,
  "intervalMs": 30000,
  "priceTolerancePpm": 5000,
  "reduceOnly": false
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=PlaceTwap)

### CancelTwap

撤销进行中的 TWAP 单。

签名：账户或 API 钱包（限授权范围内） · nonce 序列 `trade`

```json
{
  "kind": "CancelTwap",
  "account": 1234,
  "order": "4294967297"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=CancelTwap)

### SetLeverage

设置某个市场的杠杆，用初始保证金比例表示。

签名：账户或 API 钱包（限授权范围内） · nonce 序列 `trade`

`customImfPpm`：初始保证金比例，百万分比；100000 = 10%，即 10 倍。

```json
{
  "kind": "SetLeverage",
  "account": 1234,
  "market": 1,
  "customImfPpm": 100000
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=SetLeverage)

经 builder 下的单要过 builder 检查，错误码见 [`POST /v1/commands`](../trading.md)。
