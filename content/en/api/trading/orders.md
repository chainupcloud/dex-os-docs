# Orders

Each example below is the command's JSON form: the fields you choose. The SDK (or the [API playground](https://dex-preview.unibook.site/app/api-playground/)) adds the nonce and validity window, signs it and encodes it; the HTTP request is always `POST /v1/commands` with `{"command":"0x…"}`. The playground runs on the preview network with a throwaway key and test funds: it shows the nonce read, the EIP-712 typed data, the signed command, the response and the receipt, and copies the submission as curl.

## Place an order, end to end

A real run on the preview network (2026-11-23): one buy limit order on `PUMPDEX:BTC-USDC`, 1% below the best bid so it rests on the book. Responses are trimmed to the fields that matter.

**1. Read the market.** A perpetual and a spot market can share a name, so pass `kind`.

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

Price 60841.6 → `608416` ticks (`priceDecimals` 1, a multiple of `tickSize` 0.1). Size 0.0001 → `10` lots (`sizeDecimals` 5).

**2. Read the account id and nonce.**

```bash
curl -sS "$DEXOS_API_URL/v1/account/nonce?address=<main wallet address>&lane=trade"
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

`signingAccountId` goes into the command's `account`; `policyId`, `policyEpoch` and `nonce` go into the signature. The SDK reads these itself.

**3. Build and sign.** The command:

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

With the Go SDK, signed by an API wallet (see [Authentication](../../developers/authentication.md) for granting one):

```go
c := dexosv1.NewClient("https://dex-preview.unibook.site")
agent, _ := dexos.NewSigner("0x<API wallet private key>")
s, err := dexosv1.NewSession(ctx, c, agent, dexosv1.AccountRef{Address: owner, Subaccount: 0})
if err != nil { log.Fatal(err) }
cat, _ := c.Catalog(ctx)
btc, _ := cat.Lookup("PUMPDEX:BTC-USDC", dexosv1.KindPerp)
px, _ := btc.Scale.Ticks("60841.6")
sz, _ := btc.Scale.Lots("0.0001")
res, err := s.Place(ctx, dexosv1.OrderRequest{Market: btc, Side: dexos.Buy, Price: px, Lots: sz, TIF: dexos.GTC})
```

The signature covers EIP-712 typed data `AuthorizedAction` (domain `DEXOS/Account`) whose `payloadHash` commits to the command. The signed command, hex-encoded, is what you submit.

**4. Submit.**

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

202 means sequenced, not executed. Keep `requestId`.

**5. Read the receipt** until `status` is `Executed` (or `AuthorizationRejected`); 404 means not visible yet, ask again.

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

`OrderAccepted.orderSeq` is the order id; `resting: true` means it rests on the book. A business rejection shows up as `businessRejected` with the reason.

**6. See the open order.**

```bash
curl -sS "$DEXOS_API_URL/v1/account/orders?address=<main wallet address>"
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

To cancel it, sign `CancelOrder` with `"order": "6048070369280"` the same way. [Run this flow in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=PlaceOrder): it creates a throwaway account, claims test USDC, and lets you place and cancel.

## Fields

| Field | Meaning |
|---|---|
| `account` | Ledger account id: `signingAccountId` from `GET /v1/account/nonce` |
| `market` | Market id: `signingMarketId` from `GET /v1/markets` |
| `side` | `buy` or `sell` |
| `price` | Limit price in ticks: price × 10^`priceDecimals`, a multiple of `tickSize` scaled the same way. 60841.6 with `priceDecimals` 1 → `608416` |
| `lots` | Size in lots: size × 10^`sizeDecimals`, a multiple of `lotSize` scaled the same way. 0.0001 with `sizeDecimals` 5 → `10` |
| `tif` | Time in force: `gtc`, `ioc`, `post_only` or `fok` |
| `reduceOnly` | `true`: the order may only reduce a position |
| `clientOrderId` | Optional, 1–36 characters of `A-Z a-z 0-9 . _ : / -`, unique within the account |
| `order` | Order id: `orderId` from `GET /v1/account/orders`, or `orderSeq` of the `OrderAccepted` event in the receipt. A decimal string |

64-bit values (order ids, amounts, times) may be written as decimal strings.

## Orders

### PlaceOrder

Place a limit order.

Signed by: account or API wallet (within its grant) · nonce lane `trade`

`goodTilMs` (optional) is an expiry in Unix ms. `clientOrderId` is optional.

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

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=PlaceOrder)

### CancelOrder

Cancel a resting order.

Signed by: account or API wallet (within its grant) · nonce lane `trade`

```json
{
  "kind": "CancelOrder",
  "account": 1234,
  "order": "4294967297"
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=CancelOrder)

### ModifyOrder

Change a resting order's price, size, time in force or reduce-only flag.

Signed by: account or API wallet (within its grant) · nonce lane `trade`

A modify replaces the order: if the new order is rejected, the original is canceled as well.

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

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=ModifyOrder)

### BatchPlace

Place several orders in one command.

Signed by: account or API wallet (within its grant) · nonce lane `trade`

`orders`: items with `market`, `side`, `price`, `lots`, `tif`, `reduceOnly` and an optional `clientOrderId`. Each item gets its own result in the receipt's `items`.

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

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=BatchPlace)

### BatchCancel

Cancel several orders in one command.

Signed by: account or API wallet (within its grant) · nonce lane `trade`

`orders`: order ids.

```json
{
  "kind": "BatchCancel",
  "account": 1234,
  "orders": [
    "4294967297"
  ]
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=BatchCancel)

### BatchReplace

Cancel orders, then place new ones, in one command.

Signed by: account or API wallet (within its grant) · nonce lane `trade`

`cancels`: order ids, canceled first. `orders`: new orders, as in `BatchPlace`.

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

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=BatchReplace)

### BatchReplace2

Cancel, modify and place in one command.

Signed by: account or API wallet (within its grant) · nonce lane `trade`

`modifies`: items with `order`, `price`, `lots`, `tif`, `reduceOnly`.

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

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=BatchReplace2)

### BatchReplace3

Like `BatchReplace2`; a cancel or modify can also point at an order that an earlier `BatchReplace3` placed, before its order id is known.

Signed by: account or API wallet (within its grant) · nonce lane `trade`

A `cancels` entry or a modify's `target` is an order id, or `{"market", "seq", "sub", "item"}`: `seq` and `sub` from the 202 response of an earlier `BatchReplace3` by the same account, `item` the position in its `orders`. References last 60 seconds; an expired one is rejected with `ReferenceOutOfRange`. `orders` here take no `clientOrderId`.

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

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=BatchReplace3)

### ScheduleCancel

Cancel all open orders at a set time (dead man's switch). Send it again to push the time back.

Signed by: account or API wallet (within its grant) · nonce lane `trade`

`triggerMs`: Unix ms by ledger time.

```json
{
  "kind": "ScheduleCancel",
  "account": 1234,
  "triggerMs": "1764000060000"
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=ScheduleCancel)

### PlaceConditional

Place a conditional order: a limit order placed once the price crosses the trigger.

Signed by: account or API wallet (within its grant) · nonce lane `trade`

`triggerPrice` in ticks; `triggerAbove: true` fires when the price rises to it, `false` when it falls to it.

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

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=PlaceConditional)

### CancelConditional

Cancel a conditional order that has not triggered.

Signed by: account or API wallet (within its grant) · nonce lane `trade`

```json
{
  "kind": "CancelConditional",
  "account": 1234,
  "order": "4294967297"
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=CancelConditional)

### PlaceTpslPair

Attach a take-profit / stop-loss pair to a position or an order.

Signed by: account or API wallet (within its grant) · nonce lane `trade`

`closeSide` is the side that closes the position. `tpTrigger` / `slTrigger` are trigger prices and `tpPrice` / `slPrice` the limit prices, all in ticks. `positionTpsl: true` attaches to the position; for an order, set it to `false` and give the order id as `parent`.

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

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=PlaceTpslPair)

### PlaceTwap

Place a TWAP order filled in equal slices at a fixed interval.

Signed by: account or API wallet (within its grant) · nonce lane `trade`

`totalLots` split into `slices` orders, one every `intervalMs`; each slice may deviate from the reference price by at most `priceTolerancePpm` (parts per million).

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

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=PlaceTwap)

### CancelTwap

Cancel a running TWAP order.

Signed by: account or API wallet (within its grant) · nonce lane `trade`

```json
{
  "kind": "CancelTwap",
  "account": 1234,
  "order": "4294967297"
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=CancelTwap)

### SetLeverage

Set the leverage for a market, as an initial margin fraction.

Signed by: account or API wallet (within its grant) · nonce lane `trade`

`customImfPpm`: initial margin fraction in parts per million; 100000 = 10%, that is 10x.

```json
{
  "kind": "SetLeverage",
  "account": 1234,
  "market": 1,
  "customImfPpm": 100000
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=SetLeverage)

Orders routed through a builder pass the builder checks; error codes in [`POST /v1/commands`](../trading.md).
