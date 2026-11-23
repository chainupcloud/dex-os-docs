# 保证金、资金与金库

下面每个示例都是命令的 JSON 形态，即需要你填的字段。SDK（或 [API 调试台](https://dex-preview.unibook.site/app/api-playground/)）再补上 nonce 与有效期、签名并编码；HTTP 请求一律是 `POST /v1/commands`，请求体 `{"command":"0x…"}`。调试台在预览网络上运行，用临时私钥和测试资金，会逐步显示读 nonce、EIP-712 待签数据、签好的命令、响应与回执，并能把提交复制成 curl。

## 字段

| 字段 | 含义 |
|---|---|
| `account` | 账本账户号：`GET /v1/account/nonce` 返回的 `signingAccountId` |
| `market` | 市场号：`GET /v1/markets` 返回的 `signingMarketId` |
| `dex` | DEX 号：`GET /v1/markets` 或 `GET /v1/dexes` 里的 `dex` |
| `builder` | builder 号：见 `GET /v1/builder` |
| `vault` | 金库号：`GET /v1/vaults` |
| `actor` | 金库管理人的账户号 |
| `amount` | 以最小单位计的十进制字符串（USDC 6 位小数：`10000000` = 10 USDC） |

64 位数值（单号、金额、时间）可以写成十进制字符串。

## 保证金

### SetMarginMode

切换某个市场的全仓 / 逐仓。

签名：账户（主钱包）；API 钱包不能签 · nonce 序列 `trade`

`isolated: true` 为逐仓；`customImfPpm` 同 `SetLeverage`。

```json
{
  "kind": "SetMarginMode",
  "account": 1234,
  "market": 1,
  "isolated": true,
  "customImfPpm": 100000
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=SetMarginMode)

### UpdateIsolatedMargin

给逐仓仓位追加或减少保证金。

签名：账户（主钱包）；API 钱包不能签 · nonce 序列 `trade`

`add: false` 为减少。`amount` 以结算币最小单位计（USDC 6 位小数，10000000 = 10 USDC）。

```json
{
  "kind": "UpdateIsolatedMargin",
  "account": 1234,
  "market": 1,
  "add": true,
  "amount": "10000000"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=UpdateIsolatedMargin)

## 资金

### Transfer

在自己的账户与子账户之间划转。

签名：账户（主钱包）；API 钱包不能签 · nonce 序列 `funds`

`from` / `to`：账户号。`token`：币种号（`GET /v1/markets` 里的 `settleToken.id`）。`amount` 以最小单位计。

```json
{
  "kind": "Transfer",
  "from": 1234,
  "to": 1235,
  "token": 0,
  "amount": "1000000"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=Transfer)

### ApproveBuilderFee

批准某个 builder 可以收取的最高费率；`null` 为撤销。

签名：账户（主钱包）；API 钱包不能签 · nonce 序列 `funds`

`maxFeePpm` 为百万分比。

```json
{
  "kind": "ApproveBuilderFee",
  "account": 1234,
  "builder": 1,
  "maxFeePpm": 1000
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=ApproveBuilderFee)

### FundDexInsurance

向某个 DEX 的保险金注资。

签名：账户（主钱包）；API 钱包不能签 · nonce 序列 `funds`

```json
{
  "kind": "FundDexInsurance",
  "account": 1234,
  "dex": 1,
  "amount": "1000000"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=FundDexInsurance)

### RequestDepositRefund

申请退回无法入账的入金。

签名：账户（主钱包）；API 钱包不能签 · nonce 序列 `funds`

```json
{
  "kind": "RequestDepositRefund",
  "custodyKeyHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "accountId": 1234,
  "assetId": 1,
  "assetVersion": "1",
  "depositId": "1",
  "receiptHash": "0x0000000000000000000000000000000000000000000000000000000000000000"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=RequestDepositRefund)

### RequestCashWithdrawalCancel

取消尚未完成的提款。

签名：账户（主钱包）；API 钱包不能签 · nonce 序列 `funds`

```json
{
  "kind": "RequestCashWithdrawalCancel",
  "custodyKeyHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "accountId": 1234,
  "ticketId": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "ticketPayloadHash": "0x0000000000000000000000000000000000000000000000000000000000000000"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=RequestCashWithdrawalCancel)

## 金库

### VaultDeposit

存入金库。

签名：账户（主钱包）；API 钱包不能签 · nonce 序列 `funds`

`vault`：`GET /v1/vaults` 里的金库号；`lp`：自己的账户号；`amount` 以结算币最小单位计。

```json
{
  "kind": "VaultDeposit",
  "vault": 1,
  "lp": 1234,
  "amount": "10000000"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=VaultDeposit)

### VaultRedeem

赎回金库份额。

签名：账户（主钱包）；API 钱包不能签 · nonce 序列 `funds`

```json
{
  "kind": "VaultRedeem",
  "vault": 1,
  "lp": 1234,
  "shares": "1000000"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=VaultRedeem)

### VaultUnlockShares

解锁锁定期已过的份额。

签名：账户（主钱包）；API 钱包不能签 · nonce 序列 `funds`

```json
{
  "kind": "VaultUnlockShares",
  "vault": 1,
  "lp": 1234
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=VaultUnlockShares)

### CreateDexVault

为某个 DEX 创建金库，可附带初始存入。

签名：账户（主钱包）；API 钱包不能签 · nonce 序列 `funds`

`manager: null` 表示创建者即管理人。`cfg` 可选（业绩分成，百万分比等）。`seedAmount` 以结算币最小单位计。

```json
{
  "kind": "CreateDexVault",
  "dex": 1,
  "creator": 1234,
  "manager": null,
  "cfg": {
    "profitSharePpm": 100000
  },
  "depositorWhitelist": [],
  "seedAmount": "100000000"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=CreateDexVault)

### ClaimVaultManager

金库管理人领取收益。

签名：金库管理人的账户 · nonce 序列 `funds`

```json
{
  "kind": "ClaimVaultManager",
  "vault": 1,
  "claimer": 1234,
  "amount": "1000000"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=ClaimVaultManager)

### VaultAllocate

金库管理人把资金分配到某个市场。

签名：金库管理人的账户 · nonce 序列 `funds`

```json
{
  "kind": "VaultAllocate",
  "vault": 1,
  "actor": 1234,
  "market": 1,
  "amount": "1000000"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=VaultAllocate)

### VaultRetrieve

金库管理人从某个市场收回资金。

签名：金库管理人的账户 · nonce 序列 `funds`

```json
{
  "kind": "VaultRetrieve",
  "vault": 1,
  "actor": 1234,
  "market": 1,
  "amount": "1000000"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=VaultRetrieve)

## 账户设置

### OpenSubaccount

开一个子账户。

签名：账户（主钱包）；API 钱包不能签 · nonce 序列 `management`

```json
{
  "kind": "OpenSubaccount",
  "account": 1234,
  "index": 1
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=OpenSubaccount)

### SetMarketVaultStatus

金库管理人设置金库在某个市场的状态。

签名：金库管理人的账户 · nonce 序列 `management`

`status`：`quoting`、`stand_by`、`close_only` 或 `deactivated`。

```json
{
  "kind": "SetMarketVaultStatus",
  "vault": 1,
  "actor": 1234,
  "market": 1,
  "status": "quoting"
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=SetMarketVaultStatus)

### SetVaultTradingConfig

金库管理人修改金库的交易配置。

签名：金库管理人的账户 · nonce 序列 `management`

`change.kind`：`DepositCap`、`AddWhitelist`、`RemoveWhitelist`、`ClearWhitelist`、`AddBlacklist`、`RemoveBlacklist`、`SetMaxLeverage` 或 `RemoveMaxLeverage`。

```json
{
  "kind": "SetVaultTradingConfig",
  "vault": 1,
  "actor": 1234,
  "change": {
    "kind": "SetMaxLeverage",
    "markets": [
      1
    ],
    "maxLeverage": 5
  }
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=SetVaultTradingConfig)

## 用 SDK 构造

### RequestCashWithdrawal

提款到托管链，直接提或经 CCTP。提款意图里的托管、手续费与路由字段由 SDK 按 `GET /v1/custody`（CCTP 另加 `POST /v1/exchange/cctp/withdraw-quote`）填好，请用 SDK 构造。

### CreateManagedVault

创建由管理人运营的金库。请用 SDK 构造。
