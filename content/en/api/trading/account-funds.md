# Margin, funds and vaults

Every command on this page is signed by the account (main wallet); API wallets cannot submit them.

## Margin (nonce lane `trade`)

| Command | Use |
|---|---|
| `SetMarginMode` | Switch a market between cross and isolated margin |
| `UpdateIsolatedMargin` | Add margin to or remove margin from an isolated position |

## Funds (nonce lane `funds`)

| Command | Use |
|---|---|
| `RequestCashWithdrawal` | Withdraw to the custody chain, directly or over CCTP |
| `RequestCashWithdrawalCancel` | Cancel a withdrawal that has not completed |
| `RequestDepositRefund` | Request the refund of a deposit |
| `Transfer` | Move funds between your own accounts and subaccounts |
| `ApproveBuilderFee` | Approve the maximum fee rate a builder may charge |
| `FundDexInsurance` | Add funds to a DEX's insurance fund |

For a CCTP withdrawal, quote it first with `POST /v1/exchange/cctp/withdraw-quote` and copy the quote into the withdrawal route.

## Vaults (nonce lane `funds`)

| Command | Use |
|---|---|
| `VaultDeposit` | Deposit into a vault |
| `VaultRedeem` | Redeem shares |
| `VaultUnlockShares` | Unlock shares |
| `VaultAllocate` | Vault manager allocates funds to a market |
| `VaultRetrieve` | Vault manager pulls funds back from a market |
| `ClaimVaultManager` | Vault manager claims earned income |
| `CreateManagedVault` | Create a vault run by a manager |
| `CreateDexVault` | Create a vault for a DEX |

The vault manager trades the vault account with the trading commands; see [Orders](orders.md).

## Account settings (nonce lane `management`)

| Command | Use |
|---|---|
| `OpenSubaccount` | Open a subaccount |
| `SetMarketVaultStatus` | Vault manager sets the vault's status in a market |
| `SetVaultTradingConfig` | Vault manager changes the vault's trading configuration |
