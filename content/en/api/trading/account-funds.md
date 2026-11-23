# Margin, funds and vaults

Each example below is the command's JSON form: the fields you choose. The SDK (or the [API playground](https://dex-preview.unibook.site/app/api-playground/)) adds the nonce and validity window, signs it and encodes it; the HTTP request is always `POST /v1/commands` with `{"command":"0x…"}`. The playground runs on the preview network with a throwaway key and test funds: it shows the nonce read, the EIP-712 typed data, the signed command, the response and the receipt, and copies the submission as curl.

## Fields

| Field | Meaning |
|---|---|
| `account` | Ledger account id: `signingAccountId` from `GET /v1/account/nonce` |
| `market` | Market id: `signingMarketId` from `GET /v1/markets` |
| `dex` | DEX id: `dex` in `GET /v1/markets` or `GET /v1/dexes` |
| `builder` | Builder id: see `GET /v1/builder` |
| `vault` | Vault id: `GET /v1/vaults` |
| `actor` | The vault manager's account id |
| `amount` | Token atoms as a decimal string (USDC has 6 decimals: `10000000` = 10 USDC) |

64-bit values (order ids, amounts, times) may be written as decimal strings.

## Margin

### SetMarginMode

Switch a market between cross and isolated margin.

Signed by: account (main wallet); API wallets cannot · nonce lane `trade`

`isolated: true` for isolated margin; `customImfPpm` as in `SetLeverage`.

```json
{
  "kind": "SetMarginMode",
  "account": 1234,
  "market": 1,
  "isolated": true,
  "customImfPpm": 100000
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=SetMarginMode)

### UpdateIsolatedMargin

Add margin to or remove margin from an isolated position.

Signed by: account (main wallet); API wallets cannot · nonce lane `trade`

`add: false` removes margin. `amount` in settlement-token atoms (USDC: 6 decimals, so 10000000 = 10 USDC).

```json
{
  "kind": "UpdateIsolatedMargin",
  "account": 1234,
  "market": 1,
  "add": true,
  "amount": "10000000"
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=UpdateIsolatedMargin)

## Funds

### Transfer

Move funds between your own accounts and subaccounts.

Signed by: account (main wallet); API wallets cannot · nonce lane `funds`

`from` / `to`: account ids. `token`: token id (`settleToken.id` in `GET /v1/markets`). `amount` in token atoms.

```json
{
  "kind": "Transfer",
  "from": 1234,
  "to": 1235,
  "token": 0,
  "amount": "1000000"
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=Transfer)

### ApproveBuilderFee

Approve the maximum fee rate a builder may charge you; `null` revokes.

Signed by: account (main wallet); API wallets cannot · nonce lane `funds`

`maxFeePpm` in parts per million.

```json
{
  "kind": "ApproveBuilderFee",
  "account": 1234,
  "builder": 1,
  "maxFeePpm": 1000
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=ApproveBuilderFee)

### FundDexInsurance

Add funds to a DEX's insurance fund.

Signed by: account (main wallet); API wallets cannot · nonce lane `funds`

```json
{
  "kind": "FundDexInsurance",
  "account": 1234,
  "dex": 1,
  "amount": "1000000"
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=FundDexInsurance)

### RequestDepositRefund

Request the refund of a deposit that cannot be credited.

Signed by: account (main wallet); API wallets cannot · nonce lane `funds`

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

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=RequestDepositRefund)

### RequestCashWithdrawalCancel

Cancel a withdrawal that has not completed.

Signed by: account (main wallet); API wallets cannot · nonce lane `funds`

```json
{
  "kind": "RequestCashWithdrawalCancel",
  "custodyKeyHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "accountId": 1234,
  "ticketId": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "ticketPayloadHash": "0x0000000000000000000000000000000000000000000000000000000000000000"
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=RequestCashWithdrawalCancel)

## Vaults

### VaultDeposit

Deposit into a vault.

Signed by: account (main wallet); API wallets cannot · nonce lane `funds`

`vault`: vault id from `GET /v1/vaults`. `lp`: your account id. `amount` in settlement-token atoms.

```json
{
  "kind": "VaultDeposit",
  "vault": 1,
  "lp": 1234,
  "amount": "10000000"
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=VaultDeposit)

### VaultRedeem

Redeem vault shares.

Signed by: account (main wallet); API wallets cannot · nonce lane `funds`

```json
{
  "kind": "VaultRedeem",
  "vault": 1,
  "lp": 1234,
  "shares": "1000000"
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=VaultRedeem)

### VaultUnlockShares

Unlock shares whose lock-up has ended.

Signed by: account (main wallet); API wallets cannot · nonce lane `funds`

```json
{
  "kind": "VaultUnlockShares",
  "vault": 1,
  "lp": 1234
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=VaultUnlockShares)

### CreateDexVault

Create a vault for a DEX, with an optional seed deposit.

Signed by: account (main wallet); API wallets cannot · nonce lane `funds`

`manager: null` makes the creator the manager. `cfg` is optional (profit share in ppm and other settings). `seedAmount` in settlement-token atoms.

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

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=CreateDexVault)

### ClaimVaultManager

Vault manager claims earned income.

Signed by: the vault manager's account · nonce lane `funds`

```json
{
  "kind": "ClaimVaultManager",
  "vault": 1,
  "claimer": 1234,
  "amount": "1000000"
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=ClaimVaultManager)

### VaultAllocate

Vault manager allocates funds to a market.

Signed by: the vault manager's account · nonce lane `funds`

```json
{
  "kind": "VaultAllocate",
  "vault": 1,
  "actor": 1234,
  "market": 1,
  "amount": "1000000"
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=VaultAllocate)

### VaultRetrieve

Vault manager pulls funds back from a market.

Signed by: the vault manager's account · nonce lane `funds`

```json
{
  "kind": "VaultRetrieve",
  "vault": 1,
  "actor": 1234,
  "market": 1,
  "amount": "1000000"
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=VaultRetrieve)

## Account settings

### OpenSubaccount

Open a subaccount.

Signed by: account (main wallet); API wallets cannot · nonce lane `management`

```json
{
  "kind": "OpenSubaccount",
  "account": 1234,
  "index": 1
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=OpenSubaccount)

### SetMarketVaultStatus

Vault manager sets the vault's status in a market.

Signed by: the vault manager's account · nonce lane `management`

`status`: `quoting`, `stand_by`, `close_only` or `deactivated`.

```json
{
  "kind": "SetMarketVaultStatus",
  "vault": 1,
  "actor": 1234,
  "market": 1,
  "status": "quoting"
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=SetMarketVaultStatus)

### SetVaultTradingConfig

Vault manager changes the vault's trading configuration.

Signed by: the vault manager's account · nonce lane `management`

`change.kind`: `DepositCap`, `AddWhitelist`, `RemoveWhitelist`, `ClearWhitelist`, `AddBlacklist`, `RemoveBlacklist`, `SetMaxLeverage` or `RemoveMaxLeverage`.

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

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=SetVaultTradingConfig)

## Built with the SDK

### RequestCashWithdrawal

Withdraw to the custody chain, directly or over CCTP. The withdrawal intent carries custody, fee and route fields that the SDK fills from `GET /v1/custody` (and, for CCTP, `POST /v1/exchange/cctp/withdraw-quote`); build it with the SDK.

### CreateManagedVault

Create a vault run by a manager. Build it with the SDK.
