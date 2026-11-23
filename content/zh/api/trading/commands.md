# 命令总览

账本上的每一次改动都是一条签名命令，通过 [`POST /v1/commands`](../trading.md) 以 `{"command":"0x…"}` 提交。本组页面列出这个接口接受哪些命令、每条命令由谁签名、用哪条 nonce 序列。签名方法见[签名与授权](../../developers/authentication.md)。

后面几页的每条命令都有字段的 JSON 示例，并附 **Try it** 链接到 [API 调试台](https://dex-preview.unibook.site/app/api-playground/)：它在预览网络上用临时私钥和测试资金签名并提交。[订单](orders.md)页有一笔完整下单流程。

## 可以提交的命令

| 命令 | 作用 |
|---|---|
| `AuthenticatedCommand` | 由签名主体签名的一个操作。它内含下面分组表中的一条命令，几乎所有写入都用它 |
| `RegisterAccount` | 为一个地址创建账户（账户签名策略和退出地址） |

其他种类的命令只由平台服务提交，例如账本认证时间、预言机报价和托管链事件上报。除这两种外，提交别的命令返回 400 `unsupported_command`。

## `AuthenticatedCommand` 内含的命令

| 分组 | 签名方 | nonce 序列 | 详见 |
|---|---|---|---|
| 交易 | 账户或 API 钱包 | `trade` | [下单与撤单](orders.md) |
| 保证金 | 账户 | `trade` | [保证金、资金与金库](account-funds.md) |
| 资金 | 账户 | `funds` | [保证金、资金与金库](account-funds.md) |
| 金库 | 账户 | `funds` | [保证金、资金与金库](account-funds.md) |
| 账户设置 | 账户 | `management` | [保证金、资金与金库](account-funds.md) |
| 商户（DEX） | DEX 所有者或其 API 钱包；个别命令只能由所有者签 | `management` | [商户与 builder](merchants.md) |
| 商户保险金 | DEX 所有者 | `funds` | [商户与 builder](merchants.md) |
| builder | builder 所有者或其 API 钱包 | `management` | [商户与 builder](merchants.md) |
| 授权、注册与治理 | 按命令而定 | `management` | [授权、注册与治理](governance.md) |

- 「账户」指账户签名策略的成员（主钱包），按策略的门限签名。
- API 钱包只能签授权范围内的命令。授权没有覆盖的操作、账户或市场，以及 API 钱包不能签的分组，都会以 `CapabilityDenied` 拒绝。
- 每个签名主体按 `lane` 分成几条独立的 nonce 序列，每条序列各有一个 nonce 窗口，见[签名与授权](../../developers/authentication.md)。

## 怎么构造

- 用公开的 Go SDK [dex-sdk-go](https://github.com/chainupcloud/dex-sdk-go) 构造并签名，不要自己手写二进制编码。交易类命令在 `dexos` 包里有对应的 `Encode<命令名>` 函数，`dexosv1` 包负责签名、nonce 和提交。
- 命令中的价格、数量和金额都是缩放后的整数，市场用 `signingMarketId`，账户用 `signingAccountId`，见[签名与授权](../../developers/authentication.md)。
- 提交后轮询 `GET /v1/requests/{requestId}`，直到状态为 `Executed` 或 `AuthorizationRejected`。

本组页面按 dex-os `main` 分支的网关与账本代码整理。
