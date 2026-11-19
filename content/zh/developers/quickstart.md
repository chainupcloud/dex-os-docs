# 快速接入

先用公开只读接口确认网络、市场和精度，再接签名交易。下面的请求不需要私钥，也不会创建订单或移动资金。

## 设置 API 地址

向运营方取得目标环境的 HTTPS API 基础地址，并设置 `DEXOS_API_URL`，末尾不要带 `/`。本页不预设测试网或主网域名；不同环境的钱包余额、签名域和市场可能不同。示例需要 Bash 和 curl。

```bash
: "${DEXOS_API_URL:?请设置目标环境的 API 基础地址}"
curl --fail-with-body --silent --show-error "$DEXOS_API_URL/v1/time"
curl --fail-with-body --silent --show-error "$DEXOS_API_URL/v1/exchange"
```

`/v1/time` 返回毫秒时间戳 `serverTime`。`/v1/exchange` 返回 EIP-712 签名域、入金系统地址、资产表、版本、金库创建费与最低存入额，以及数值约定。签名命令要绑定的网络身份取自 `/v1/network`。每个环境都应重新读取这些信息；不要把示例中的签名域或合约地址写死。

## 获取可交易市场

```bash
curl --fail-with-body --silent --show-error "$DEXOS_API_URL/v1/markets"
```

从结果选择一个 `symbol`，再运行：

```bash
: "${DEXOS_SYMBOL:?请设置市场列表中的 symbol}"
curl --fail-with-body --silent --show-error \
  "$DEXOS_API_URL/v1/markets/$DEXOS_SYMBOL"
curl --fail-with-body --silent --show-error \
  "$DEXOS_API_URL/v1/markets/$DEXOS_SYMBOL/book"
```

记录市场的 `priceDecimals`、`sizeDecimals`、`tickSize`、`lotSize`、`signingMarketId` 和交易状态。业务请求使用 `symbol`；`signingMarketId` 仅用于签名结构中的市场编号。价格、数量和金额用十进制字符串处理，避免经过浮点数。

## 查询自己的账户

已注册账户可使用公开只读接口查余额和下一个 nonce。设置主钱包地址；查询不需要连接钱包。

```bash
: "${DEXOS_ADDRESS:?请设置自己的主钱包地址}"
curl --fail-with-body --silent --show-error --get \
  "$DEXOS_API_URL/v1/account" \
  --data-urlencode "address=$DEXOS_ADDRESS"
curl --fail-with-body --silent --show-error --get \
  "$DEXOS_API_URL/v1/account/nonce" \
  --data-urlencode "address=$DEXOS_ADDRESS"
```

地址不存在时可能返回 404；这不表示 API 离线。子账户查询加 `subaccount`，其中 `0` 表示主账户。金库账户查询改用 `vault`，与 `address`、`subaccount` 互斥。

nonce 缺省是 `trade` 车道；其他车道加 `lane=funds` 或 `lane=management`。每条车道的窗口各自独立。

## 接下来接交易

阅读[签名与授权](authentication.md)，然后用 [dex-sdk-go](https://github.com/chainupcloud/dex-sdk-go) SDK 构造并签名命令。在测试环境验证完整流程：读取网络身份和认证时间 → 读取 nonce → 签名 → `POST /v1/commands` → 查询回执 → 查询订单或成交。本文不提供可直接执行的资金写请求。

`POST /v1/commands` 返回 HTTP 202 表示命令已定序，不代表已执行或已成交。应查询其 `requestId` 并逐项检查回执，不要盲目重发。回执、分页和错误处理见 [REST API 使用约定](rest-api.md)和[错误与恢复](errors-and-recovery.md)。
