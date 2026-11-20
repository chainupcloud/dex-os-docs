# 商户与 builder

## 商户（DEX）管理（nonce 车道 `management`）

签名方：DEX 所有者，或所有者授权的 API 钱包。`SetDexFeeRecipient`、`DisableDex`、`HaltTrading` 只能由所有者签。

| 命令 | 作用 |
|---|---|
| `UpdateMarketStatus` | 修改市场状态 |
| `UpdateMarketParams` | 修改市场参数 |
| `RequestMarketTickChange` | 申请修改市场的价格步长 |
| `HaltTrading` | 暂停或恢复某个市场的交易 |
| `DisableDex` | 停用整个 DEX |
| `SetDexSpotStatus` | 设置现货市场状态 |
| `InsertMarginTable` | 新增一张保证金档位表 |
| `SetAssetMarginTable` | 为市场指定保证金档位表 |
| `SetAssetMarginMode` | 设置市场的保证金模式 |
| `SetFundingPolicy` | 设置市场的资金费政策 |
| `SetOpenInterestCaps` | 设置 DEX 与各资产的持仓上限 |
| `SetMarketFeeSplit` | 设置市场手续费在部署者与 builder 之间的分成 |
| `SetMarketFeeSplitV2` | 同上，另可单独设置挂单方向的部署者费率 |
| `SetDeployerFees` | 设置部署者费率 |
| `SetAccountDeployerFees` | 为指定账户单独设置部署者吃单费率 |
| `SetAccountDeployerFeesV2` | 同上，另可设置挂单费率 |
| `SetDexFeeRecipient` | 设置 DEX 的手续费收款账户 |
| `CreateVault` | 创建金库并指定运营方 |

## 商户保险金（nonce 车道 `funds`）

签名方：只能是 DEX 所有者。

| 命令 | 作用 |
|---|---|
| `RequestDexInsuranceWithdraw` | 申请从 DEX 保险金提取到指定账户 |
| `ExecuteDexInsuranceWithdraw` | 执行已申请的保险金提取 |

## builder（nonce 车道 `management`）

签名方：builder 所有者，或其授权的 API 钱包。

| 命令 | 作用 |
|---|---|
| `SetBuilderFees` | 设置 builder 的吃单 / 挂单费率 |
| `SetBuilderMarketFees` | 为某个市场单独设置 builder 费率 |
| `SetBuilderUserFees` | 为某个账户在某个市场单独设置 builder 费率 |

DEX 与 builder 的注册见[授权、注册与治理](governance.md)。商户相关的只读接口见[商户](../merchants.md)。
