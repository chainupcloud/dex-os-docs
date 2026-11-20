# Merchants and builders

## Merchant (DEX) management (nonce lane `management`)

Signed by: the DEX owner, or an API wallet the owner granted. `SetDexFeeRecipient`, `DisableDex` and `HaltTrading` are owner-only.

| Command | Use |
|---|---|
| `UpdateMarketStatus` | Change a market's status |
| `UpdateMarketParams` | Change a market's parameters |
| `RequestMarketTickChange` | Request a change of a market's price step |
| `HaltTrading` | Halt or resume trading in a market |
| `DisableDex` | Disable the whole DEX |
| `SetDexSpotStatus` | Set a spot market's status |
| `InsertMarginTable` | Add a margin tier table |
| `SetAssetMarginTable` | Assign a margin tier table to a market |
| `SetAssetMarginMode` | Set a market's margin mode |
| `SetFundingPolicy` | Set a market's funding policy |
| `SetOpenInterestCaps` | Set open-interest caps for the DEX and its assets |
| `SetMarketFeeSplit` | Set how a market's fees split between deployer and builder |
| `SetMarketFeeSplitV2` | Same, with a separate deployer rate for makers |
| `SetDeployerFees` | Set the deployer fee rates |
| `SetAccountDeployerFees` | Set a deployer taker rate for one account |
| `SetAccountDeployerFeesV2` | Same, with a maker rate as well |
| `SetDexFeeRecipient` | Set the DEX's fee recipient account |
| `CreateVault` | Create a vault and name its operator |

## Merchant insurance (nonce lane `funds`)

Signed by: the DEX owner only.

| Command | Use |
|---|---|
| `RequestDexInsuranceWithdraw` | Request a withdrawal from the DEX insurance fund to an account |
| `ExecuteDexInsuranceWithdraw` | Execute a requested insurance withdrawal |

## Builders (nonce lane `management`)

Signed by: the builder owner, or an API wallet it granted.

| Command | Use |
|---|---|
| `SetBuilderFees` | Set the builder's taker / maker rates |
| `SetBuilderMarketFees` | Set builder rates for one market |
| `SetBuilderUserFees` | Set builder rates for one account in one market |

Registering a DEX or a builder: see [Grants, registration and governance](governance.md). Merchant reads: see [Merchants](../merchants.md).
