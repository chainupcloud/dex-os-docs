# 授权、注册与治理

本页命令都走 nonce 车道 `management`。签名方按命令而定：账户、DEX 所有者、builder 或治理成员。

## 授权

| 命令 | 作用 |
|---|---|
| `GrantCapability` | 给 API 钱包发授权：可操作的子账户、操作、市场、价格区间和到期时间 |
| `RevokeCapability` | 撤销一条授权 |
| `SetGrantPaused` | 暂停或恢复一条授权 |

主钱包给 API 钱包授权的流程见[签名与授权](../../developers/authentication.md)。Go SDK 的 `dexosv1` 包提供 `ApproveAgent`、`RevokeAgent` 等封装。

## 注册

| 命令 | 作用 |
|---|---|
| `RegisterDexV2` | 注册一个 DEX：所有者账户、简称和结算资产 |
| `AcceptDexOwner` | 新所有者接受 DEX 所有权转移 |
| `RegisterBuilder` | 注册 builder：所有者账户和收款账户 |
| `RegisterBuilderLinked` | 注册绑定到某个 DEX 的 builder |

## 治理

| 命令 | 作用 |
|---|---|
| `Propose` | 发起治理提案 |
| `SubmitAndExecute` | 提交提案并立即执行 |
| `ExecuteProposal` | 执行已通过的提案 |
| `CancelProposal` | 取消提案 |
| `FreezeMarket` | 冻结市场 |
| `ReleaseMarketLock` | 解除市场锁定 |
| `PauseTimeSet` | 暂停当前的认证时间签名方集合 |
| `RestorePausedTimeSet` | 恢复被暂停的认证时间签名方集合 |

提案的查询接口见[治理](../governance.md)。
