# Merchants and builders

Each example below is the command's JSON form: the fields you choose. The SDK (or the [API playground](https://dex-preview.unibook.site/app/api-playground/)) adds the nonce and validity window, signs it and encodes it; the HTTP request is always `POST /v1/commands` with `{"command":"0x…"}`. The playground runs on the preview network with a throwaway key and test funds: it shows the nonce read, the EIP-712 typed data, the signed command, the response and the receipt, and copies the submission as curl.

## Fields

| Field | Meaning |
|---|---|
| `account` | Ledger account id: `signingAccountId` from `GET /v1/account/nonce` |
| `market` | Market id: `signingMarketId` from `GET /v1/markets` |
| `dex` | DEX id: `dex` in `GET /v1/markets` or `GET /v1/dexes` |
| `builder` | Builder id: see `GET /v1/builder` |
| `amount` | Token atoms as a decimal string (USDC has 6 decimals: `10000000` = 10 USDC) |

64-bit values (order ids, amounts, times) may be written as decimal strings.

## Merchant (DEX) management

### UpdateMarketStatus

Change a market's status.

Signed by: DEX owner, or an API wallet it granted · nonce lane `management`

`status`: `active`, `paused`, `cancel_only`, `post_only`, `reduce_only`, `halted`, `final_settlement`, `delisted` or `oracle_stale`.

```json
{
  "kind": "UpdateMarketStatus",
  "market": 1,
  "status": "active"
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=UpdateMarketStatus)

### HaltTrading

Halt or resume trading in a market.

Signed by: DEX owner only · nonce lane `management`

```json
{
  "kind": "HaltTrading",
  "dex": 1,
  "market": 1,
  "halted": true
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=HaltTrading)

### DisableDex

Disable the whole DEX.

Signed by: DEX owner only · nonce lane `management`

```json
{
  "kind": "DisableDex",
  "dex": 1
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=DisableDex)

### SetDexSpotStatus

Set a spot market's status.

Signed by: DEX owner, or an API wallet it granted · nonce lane `management`

```json
{
  "kind": "SetDexSpotStatus",
  "dex": 1,
  "market": 1,
  "status": "active"
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=SetDexSpotStatus)

### RequestMarketTickChange

Request a change of a market's price step.

Signed by: DEX owner, or an API wallet it granted · nonce lane `management`

```json
{
  "kind": "RequestMarketTickChange",
  "market": 1,
  "expectedRevision": "1",
  "expectedStep": 1,
  "newStep": 10
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=RequestMarketTickChange)

### InsertMarginTable

Add a margin tier table.

Signed by: DEX owner, or an API wallet it granted · nonce lane `management`

```json
{
  "kind": "InsertMarginTable",
  "dex": 1,
  "tableId": 1,
  "tiers": [
    {
      "lowerBoundNotional": "0",
      "maxLeverage": 20
    },
    {
      "lowerBoundNotional": "1000000000000",
      "maxLeverage": 10
    }
  ]
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=InsertMarginTable)

### SetAssetMarginTable

Assign a margin tier table to a market.

Signed by: DEX owner, or an API wallet it granted · nonce lane `management`

```json
{
  "kind": "SetAssetMarginTable",
  "dex": 1,
  "market": 1,
  "tableId": 1
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=SetAssetMarginTable)

### SetAssetMarginMode

Set a market's margin mode.

Signed by: DEX owner, or an API wallet it granted · nonce lane `management`

`mode`: `normal`, `no_cross` or `strict_isolated`.

```json
{
  "kind": "SetAssetMarginMode",
  "dex": 1,
  "market": 1,
  "mode": "normal"
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=SetAssetMarginMode)

### SetFundingPolicy

Set a market's funding policy.

Signed by: DEX owner, or an API wallet it granted · nonce lane `management`

```json
{
  "kind": "SetFundingPolicy",
  "dex": 1,
  "market": 1,
  "policy": {
    "multiplierPpm": 1000000,
    "interestRatePpm": 0,
    "clampPpm": 40000
  }
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=SetFundingPolicy)

### SetOpenInterestCaps

Set open-interest caps for the DEX and its markets.

Signed by: DEX owner, or an API wallet it granted · nonce lane `management`

```json
{
  "kind": "SetOpenInterestCaps",
  "dex": 1,
  "dexCapNotional": "100000000000000",
  "assets": [
    {
      "market": 1,
      "capNotional": "10000000000000",
      "capLots": "1000000"
    }
  ]
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=SetOpenInterestCaps)

### SetMarketFeeSplit

Set how a market's fees split between deployer and builder.

Signed by: DEX owner, or an API wallet it granted · nonce lane `management`

```json
{
  "kind": "SetMarketFeeSplit",
  "dex": 1,
  "market": 1,
  "deployerPpm": 100,
  "builderPpm": 100
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=SetMarketFeeSplit)

### SetMarketFeeSplitV2

Same, with a separate deployer rate for makers.

Signed by: DEX owner, or an API wallet it granted · nonce lane `management`

```json
{
  "kind": "SetMarketFeeSplitV2",
  "dex": 1,
  "market": 1,
  "deployerPpm": 100,
  "deployerMakerPpm": 0,
  "builderPpm": 100
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=SetMarketFeeSplitV2)

### SetDeployerFees

Set the deployer fee rates.

Signed by: DEX owner, or an API wallet it granted · nonce lane `management`

```json
{
  "kind": "SetDeployerFees",
  "dex": 1,
  "scalePpm": 1000000,
  "growthMode": false
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=SetDeployerFees)

### SetAccountDeployerFees

Set a deployer taker rate for one account.

Signed by: DEX owner, or an API wallet it granted · nonce lane `management`

```json
{
  "kind": "SetAccountDeployerFees",
  "dex": 1,
  "account": 1234,
  "market": 1,
  "enabled": true,
  "takerPpm": 200
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=SetAccountDeployerFees)

### SetAccountDeployerFeesV2

Same, with a maker rate as well.

Signed by: DEX owner, or an API wallet it granted · nonce lane `management`

```json
{
  "kind": "SetAccountDeployerFeesV2",
  "dex": 1,
  "account": 1234,
  "market": null,
  "enabled": true,
  "takerPpm": 200,
  "makerPpm": 0
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=SetAccountDeployerFeesV2)

### SetDexFeeRecipient

Set the DEX's fee recipient account.

Signed by: DEX owner only · nonce lane `management`

```json
{
  "kind": "SetDexFeeRecipient",
  "dex": 1,
  "recipient": 1234
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=SetDexFeeRecipient)

### CreateVault

Create a vault and name its operator.

Signed by: DEX owner, or an API wallet it granted · nonce lane `management`

```json
{
  "kind": "CreateVault",
  "operator": 1234
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=CreateVault)

## Merchant insurance

### RequestDexInsuranceWithdraw

Request a withdrawal from the DEX insurance fund to an account.

Signed by: DEX owner only · nonce lane `funds`

```json
{
  "kind": "RequestDexInsuranceWithdraw",
  "dex": 1,
  "to": 1234,
  "amount": "1000000"
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=RequestDexInsuranceWithdraw)

### ExecuteDexInsuranceWithdraw

Execute a requested insurance withdrawal.

Signed by: DEX owner only · nonce lane `funds`

```json
{
  "kind": "ExecuteDexInsuranceWithdraw",
  "dex": 1
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=ExecuteDexInsuranceWithdraw)

## Builders

### SetBuilderFees

Set the builder's taker / maker rates.

Signed by: builder owner, or an API wallet it granted · nonce lane `management`

```json
{
  "kind": "SetBuilderFees",
  "builder": 1,
  "takerPpm": 100,
  "makerPpm": 0
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=SetBuilderFees)

### SetBuilderMarketFees

Set builder rates for one market.

Signed by: builder owner, or an API wallet it granted · nonce lane `management`

```json
{
  "kind": "SetBuilderMarketFees",
  "builder": 1,
  "market": 1,
  "takerPpm": 100,
  "makerPpm": 0
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=SetBuilderMarketFees)

### SetBuilderUserFees

Set builder rates for one account, in one market or all (`market: null`).

Signed by: builder owner, or an API wallet it granted · nonce lane `management`

```json
{
  "kind": "SetBuilderUserFees",
  "builder": 1,
  "account": 1234,
  "market": null,
  "takerPpm": 50,
  "makerPpm": 0
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=SetBuilderUserFees)

A throwaway playground account is not a DEX or builder owner, so the ledger rejects these commands there (for example `ScopeMismatch`); the playground shows the real rejection.
