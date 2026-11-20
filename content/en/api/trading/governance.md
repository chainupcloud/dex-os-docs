# Grants, registration and governance

Every command on this page uses nonce lane `management`. The signer depends on the command: an account, a DEX owner, a builder or governance members.

## Grants

| Command | Use |
|---|---|
| `GrantCapability` | Grant an API wallet: subaccounts, operations, markets, price band and expiry |
| `RevokeCapability` | Revoke a grant |
| `SetGrantPaused` | Pause or resume a grant |

How the main wallet grants an API wallet: see [Authentication](../../developers/authentication.md). The Go SDK `dexosv1` package wraps this as `ApproveAgent`, `RevokeAgent` and related calls.

## Registration

| Command | Use |
|---|---|
| `RegisterDexV2` | Register a DEX: owner account, short name and settlement asset |
| `AcceptDexOwner` | The new owner accepts a DEX ownership transfer |
| `RegisterBuilder` | Register a builder: owner account and payout account |
| `RegisterBuilderLinked` | Register a builder linked to a DEX |

## Governance

| Command | Use |
|---|---|
| `Propose` | Submit a governance proposal |
| `SubmitAndExecute` | Submit a proposal and execute it at once |
| `ExecuteProposal` | Execute an approved proposal |
| `CancelProposal` | Cancel a proposal |
| `FreezeMarket` | Freeze a market |
| `ReleaseMarketLock` | Release a market lock |
| `PauseTimeSet` | Pause the current certified-time signer set |
| `RestorePausedTimeSet` | Restore a paused certified-time signer set |

Proposal reads: see [Governance](../governance.md).
