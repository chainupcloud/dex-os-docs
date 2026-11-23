# 商户与 builder

下面每个示例都是命令的 JSON 形态，即需要你填的字段。SDK（或 [API 调试台](https://dex-preview.unibook.site/app/api-playground/)）再补上 nonce 与有效期、签名并编码；HTTP 请求一律是 `POST /v1/commands`，请求体 `{"command":"0x…"}`。调试台在预览网络上运行，用临时私钥和测试资金，会逐步显示读 nonce、EIP-712 待签数据、签好的命令、响应与回执，并能把提交复制成 curl。

## 字段

| 字段 | 含义 |
|---|---|
| `account` | 账本账户号：`GET /v1/account/nonce` 返回的 `signingAccountId` |
| `market` | 市场号：`GET /v1/markets` 返回的 `signingMarketId` |
| `dex` | DEX 号：`GET /v1/markets` 或 `GET /v1/dexes` 里的 `dex` |
| `builder` | builder 号：见 `GET /v1/builder` |
| `amount` | 以最小单位计的十进制字符串（USDC 6 位小数：`10000000` = 10 USDC） |

64 位数值（单号、金额、时间）可以写成十进制字符串。

## 商户（DEX）管理

### UpdateMarketStatus

修改市场状态。

签名：DEX 所有者，或其授权的 API 钱包 · nonce 序列 `management`

`status`：`active`、`paused`、`cancel_only`、`post_only`、`reduce_only`、`halted`、`final_settlement`、`delisted` 或 `oracle_stale`。

```json
{
  "kind": "UpdateMarketStatus",
  "market": 1,
  "status": "active"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=UpdateMarketStatus)

### HaltTrading

暂停或恢复某个市场的交易。

签名：仅 DEX 所有者 · nonce 序列 `management`

```json
{
  "kind": "HaltTrading",
  "dex": 1,
  "market": 1,
  "halted": true
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=HaltTrading)

### DisableDex

停用整个 DEX。

签名：仅 DEX 所有者 · nonce 序列 `management`

```json
{
  "kind": "DisableDex",
  "dex": 1
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=DisableDex)

### SetDexSpotStatus

设置现货市场的状态。

签名：DEX 所有者，或其授权的 API 钱包 · nonce 序列 `management`

```json
{
  "kind": "SetDexSpotStatus",
  "dex": 1,
  "market": 1,
  "status": "active"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=SetDexSpotStatus)

### RequestMarketTickChange

申请修改市场的价格步长。

签名：DEX 所有者，或其授权的 API 钱包 · nonce 序列 `management`

```json
{
  "kind": "RequestMarketTickChange",
  "market": 1,
  "expectedRevision": "1",
  "expectedStep": 1,
  "newStep": 10
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=RequestMarketTickChange)

### InsertMarginTable

新增一张保证金分档表。

签名：DEX 所有者，或其授权的 API 钱包 · nonce 序列 `management`

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

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=InsertMarginTable)

### SetAssetMarginTable

给市场指定保证金分档表。

签名：DEX 所有者，或其授权的 API 钱包 · nonce 序列 `management`

```json
{
  "kind": "SetAssetMarginTable",
  "dex": 1,
  "market": 1,
  "tableId": 1
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=SetAssetMarginTable)

### SetAssetMarginMode

设置市场的保证金模式。

签名：DEX 所有者，或其授权的 API 钱包 · nonce 序列 `management`

`mode`：`normal`、`no_cross` 或 `strict_isolated`。

```json
{
  "kind": "SetAssetMarginMode",
  "dex": 1,
  "market": 1,
  "mode": "normal"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=SetAssetMarginMode)

### SetFundingPolicy

设置市场的资金费策略。

签名：DEX 所有者，或其授权的 API 钱包 · nonce 序列 `management`

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

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=SetFundingPolicy)

### SetOpenInterestCaps

设置 DEX 与各市场的持仓量上限。

签名：DEX 所有者，或其授权的 API 钱包 · nonce 序列 `management`

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

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=SetOpenInterestCaps)

### SetMarketFeeSplit

设置市场手续费在部署方与 builder 之间的分成。

签名：DEX 所有者，或其授权的 API 钱包 · nonce 序列 `management`

```json
{
  "kind": "SetMarketFeeSplit",
  "dex": 1,
  "market": 1,
  "deployerPpm": 100,
  "builderPpm": 100
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=SetMarketFeeSplit)

### SetMarketFeeSplitV2

同上，另设部署方的挂单费率。

签名：DEX 所有者，或其授权的 API 钱包 · nonce 序列 `management`

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

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=SetMarketFeeSplitV2)

### SetDeployerFees

设置部署方费率。

签名：DEX 所有者，或其授权的 API 钱包 · nonce 序列 `management`

```json
{
  "kind": "SetDeployerFees",
  "dex": 1,
  "scalePpm": 1000000,
  "growthMode": false
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=SetDeployerFees)

### SetAccountDeployerFees

给单个账户设置部署方吃单费率。

签名：DEX 所有者，或其授权的 API 钱包 · nonce 序列 `management`

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

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=SetAccountDeployerFees)

### SetAccountDeployerFeesV2

同上，另设挂单费率。

签名：DEX 所有者，或其授权的 API 钱包 · nonce 序列 `management`

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

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=SetAccountDeployerFeesV2)

### SetDexFeeRecipient

设置 DEX 的手续费收款账户。

签名：仅 DEX 所有者 · nonce 序列 `management`

```json
{
  "kind": "SetDexFeeRecipient",
  "dex": 1,
  "recipient": 1234
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=SetDexFeeRecipient)

### CreateVault

创建金库并指定运营账户。

签名：DEX 所有者，或其授权的 API 钱包 · nonce 序列 `management`

```json
{
  "kind": "CreateVault",
  "operator": 1234
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=CreateVault)

## 商户保险金

### RequestDexInsuranceWithdraw

申请把 DEX 保险金提到某个账户。

签名：仅 DEX 所有者 · nonce 序列 `funds`

```json
{
  "kind": "RequestDexInsuranceWithdraw",
  "dex": 1,
  "to": 1234,
  "amount": "1000000"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=RequestDexInsuranceWithdraw)

### ExecuteDexInsuranceWithdraw

执行已申请的保险金提取。

签名：仅 DEX 所有者 · nonce 序列 `funds`

```json
{
  "kind": "ExecuteDexInsuranceWithdraw",
  "dex": 1
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=ExecuteDexInsuranceWithdraw)

## Builder

### SetBuilderFees

设置 builder 的吃单 / 挂单费率。

签名：builder 所有者，或其授权的 API 钱包 · nonce 序列 `management`

```json
{
  "kind": "SetBuilderFees",
  "builder": 1,
  "takerPpm": 100,
  "makerPpm": 0
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=SetBuilderFees)

### SetBuilderMarketFees

设置 builder 在单个市场的费率。

签名：builder 所有者，或其授权的 API 钱包 · nonce 序列 `management`

```json
{
  "kind": "SetBuilderMarketFees",
  "builder": 1,
  "market": 1,
  "takerPpm": 100,
  "makerPpm": 0
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=SetBuilderMarketFees)

### SetBuilderUserFees

设置 builder 对单个账户的费率，可限定市场（`market: null` 为全部）。

签名：builder 所有者，或其授权的 API 钱包 · nonce 序列 `management`

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

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=SetBuilderUserFees)

调试台的临时账户不是 DEX 或 builder 的所有者，账本会拒绝这些命令（例如 `ScopeMismatch`），页面显示的是真实拒因。
