# 保证金、资金与金库

本页的命令都只能由账户（主钱包）签名，API 钱包不能提交。

## 保证金（nonce 车道 `trade`）

| 命令 | 作用 |
|---|---|
| `SetMarginMode` | 切换某个市场的全仓 / 逐仓模式 |
| `UpdateIsolatedMargin` | 给逐仓仓位追加或减少保证金 |

## 资金（nonce 车道 `funds`）

| 命令 | 作用 |
|---|---|
| `RequestCashWithdrawal` | 申请提现到托管链，直接到账或经 CCTP 跨链 |
| `RequestCashWithdrawalCancel` | 取消一笔尚未完成的提现 |
| `RequestDepositRefund` | 申请退回一笔入金 |
| `Transfer` | 在自己的账户和子账户之间划转 |
| `ApproveBuilderFee` | 批准某个 builder 可收取的最高费率 |
| `FundDexInsurance` | 向某个 DEX 的保险金注资 |

CCTP 提现先用 `POST /v1/exchange/cctp/withdraw-quote` 报价，再把报价结果填进提现路由。

## 金库（nonce 车道 `funds`）

| 命令 | 作用 |
|---|---|
| `VaultDeposit` | 存入金库 |
| `VaultRedeem` | 按份额赎回 |
| `VaultUnlockShares` | 解锁份额 |
| `VaultAllocate` | 金库经理把资金分配到某个市场 |
| `VaultRetrieve` | 金库经理从某个市场收回资金 |
| `ClaimVaultManager` | 金库经理提取应得的收益 |
| `CreateManagedVault` | 创建由经理管理的金库 |
| `CreateDexVault` | 为某个 DEX 创建金库 |

金库账户的交易由金库经理用交易类命令完成，见[下单与撤单](orders.md)。

## 账户设置（nonce 车道 `management`）

| 命令 | 作用 |
|---|---|
| `OpenSubaccount` | 开一个子账户 |
| `SetMarketVaultStatus` | 金库经理设置金库在某个市场的状态 |
| `SetVaultTradingConfig` | 金库经理修改金库的交易配置 |
