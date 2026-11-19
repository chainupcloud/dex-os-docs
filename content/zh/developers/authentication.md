# 签名与授权

公开只读接口不需要 API Key。所有签名写入都是一条命令，以 `{"command":"0x…"}` 提交到 `POST /v1/commands`，内容是签好名的命令规范字节的小写十六进制。被签名的不是请求 JSON；网关也不会代签、不会补 nonce、不会延长有效期。私钥只用于本地签名，不要发给网关。

请用公开的 Go SDK [dex-sdk-go](https://github.com/chainupcloud/dex-sdk-go)（`dexosv1` 包）构造命令；其中 `examples/commands` 演示了授权、下单、重发、撤单、过期和撤销授权的完整流程。不要自己手写二进制编码。

## 命令绑定了什么

| 组成部分 | 从哪里取 |
|---|---|
| 网络身份：`networkId`、`genesisHash`、`ledgerEpoch`、链 ID、验证合约、`manifestHash` | `GET /v1/network`。每个环境单独读取，不要写死 |
| 签名主体 | 账户根（账户签名策略的成员，即主钱包），或持有授权的 API 钱包 |
| nonce 车道与 nonce | `trade` 用于下单撤单；`funds` 用于提现、转账和金库存取；`management` 用于授权、子账户等管理设置 |
| 有效期 | `validUntilMs`，按 `GET /v1/time/certified` 给出的账本认证时间判断，不看本机时钟 |
| 内层命令 | 业务动作的规范编码；价格和数量是缩放后的整数，市场用 `signingMarketId`，账户用 `signingAccountId` |

签名是对覆盖以上全部内容的 `AuthorizedAction` 结构做 EIP-712 签名。命令的 `actionId` 同时就是查询回执用的 `requestId`。

账本重建后网络身份会变化。签在旧网络上的命令会被 503 `upstream_manifest_mismatch` 拒绝；提交时带上 `x-dexos-expect-manifest`（签名时用的 Manifest 哈希），不一致时就能明确发现。重新读取网络身份后再签。

## 账户与签名主体

`GET /v1/accounts?member=<地址>` 列出成员里包含该地址的账户策略，含策略号、纪元、门限和成员。`soleSigner: true` 表示该地址自己的单签账户。子账户沿用主账户的策略；`GET /v1/account/subaccounts?address=` 返回每个子账户的 `signingAccountId`。

## 整数缩放

签名中的价格和数量是整数：`ticks = price × 10^priceDecimals`，`lots = size × 10^sizeDecimals`，`priceDecimals`、`sizeDecimals` 取自 `/v1/markets/{symbol}`。换算必须整除，并满足市场的价格步长、数量步长和业务限制。资产金额按该资产自己的小数位缩放，不要对所有资产套用 USDC 的精度。

## nonce

每个签名主体在每条车道上各有一个 nonce 窗口。用 `GET /v1/nonces?principal=account&policy=<策略号>&lane=<车道>` 读取（API 钱包另带 `grant` 和 `grantEpoch`），也可以用 `GET /v1/account/nonce?address=…&lane=…`。窗口返回下界 `floor`、已用最高值 `high`（没用过为 null）和建议值 `next`：低于 `floor` 或已经用过的值会被拒绝，`next` 及以上的值一定没用过。

共用同一主体和车道的多个写入方必须协调分配 nonce。写入被拒或结果未知时，不要马上用新 nonce 把同一个动作重签一遍：先弄清原命令的结论（见[错误与恢复](errors-and-recovery.md)）。

## API 钱包

主钱包用一条 `management` 车道的命令给 API 钱包发授权。授权写明被授权的 API 钱包、覆盖哪些子账户、允许哪些操作和到期时间，还可以限定市场和价格区间。撤销授权也是一条 `management` 车道的命令。API 钱包不能使用 `funds` 车道，因此不能提现、转账，也不能做金库存取。

授权生效后 API 钱包才能签名：在 `GET /v1/grants?policy=<策略号>` 查看该授权的 `status` 和 `epoch`，或查 `GET /v1/account/agents?address=` 和 `GET /v1/agents/{address}`，其中 `executable: true` 表示按当前认证时间账本会接受这条授权。这些列表只是清单；命令仍可能因操作、账户、市场或额度超出授权范围而被拒。

API 钱包以代理主体签名，带上授权 ID 和授权纪元，使用自己的 nonce 窗口，与主钱包的互不相干。

## 金库

读取金库账户用查询参数 `vault`。金库账户的交易由金库经理完成，可以用经理的主钱包，也可以用经理授权的 API 钱包。金库存入和赎回是 `funds` 车道的命令，由存入人的主钱包签名；API 钱包不能提交。

## 排查拒绝

先核对环境和网络身份，再依次检查签名主体及其纪元、车道和 nonce 窗口、有效期是否已按认证时间过期、整数缩放。账本在授权环节拒绝的命令，回执状态为 `AuthorizationRejected` 并带稳定错误码，nonce 不会被消耗。反复更换 nonce 解决不了根本问题。
