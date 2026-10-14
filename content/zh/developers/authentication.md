# 签名与授权

公开读取不需要 API key。写请求通过 EIP-712 签名验证身份；私钥只用于本地签名，不能作为请求字段发送给网关。

## 签名前需要的信息

从 `/v1/exchange` 获取当前环境的 `domain`、`chainId` 和资产表，从 `/v1/markets/{symbol}` 获取市场精度和 `signingMarketId`，从 `/v1/account/nonce` 获取 `nonce` 和 `signingAccountId`。每个写接口的 OpenAPI `x-eip712.typeString` 指明签名结构。JSON 业务参数不等于 EIP-712 message；不要直接把请求 JSON 哈希后签名。

签名中的价格与数量使用整数：`ticks = price × 10^priceDecimals`，`lots = size × 10^sizeDecimals`。换算必须精确，同时满足市场的 tick、lot 和业务限制。资产金额按对应资产的小数位换算；USDC 为 6 位，不要将所有资产都当作 USDC。

## 主钱包签名

共享请求信封包含 `account`、`nonce`、`signature`，以及适用时的 `subaccount`、`vault`、`signer`、`expiresAt`、`nowMs`。`account` 是主钱包地址；子账户以 `subaccount` 指定。不要将 `signingAccountId` 填进地址字段。

未提供 `signer` 时走主钱包签名路径。`expiresAt` 只在相应签名结构支持时生效；当前 Order 的 `expiry` 来自该字段，0 或省略表示不设到期时间。不要假定信封中的可选字段会影响每一种操作。

nonce 查询返回的 `scope` 区分账户与 API 钱包。当前使用递增 nonce；不要按时间戳窗口 nonce 编写客户端。多个写入者共享同一 scope 时需协调分配和提交顺序，不能让并发请求各自读取同一个 nonce 后独立提交。请求结果不明时先查回执，不能仅凭再次读取 nonce 判断是否成功。

## API 钱包

主钱包通过 `POST /v1/account/agents/approve` 授权 API 钱包，并可通过 `/v1/account/agents/revoke` 撤销。API 钱包用于交易，不能提款、转账或管理授权。撤销和有效期必须纳入密钥管理流程。

API 钱包写请求带 `signer`，签名对象是 `AgentExec(bytes32 commandHash,uint64 nonce)`；`commandHash` 是内层命令的规范字节哈希，不是任意 JSON 的哈希。应使用与当前服务匹配、已验证的编码实现。批量下单、换单、定时撤单等命令涉及 `nowMs`；逐端点核对必填项及参与哈希的字段。

查询 API 钱包 nonce：

```bash
: "${DEXOS_API_URL:?请设置 API 基础地址}"
: "${DEXOS_ADDRESS:?请设置被代表账户的主钱包地址}"
: "${DEXOS_SIGNER:?请设置 API 钱包地址}"
curl --fail-with-body --silent --show-error --get \
  "$DEXOS_API_URL/v1/account/nonce" \
  --data-urlencode "address=$DEXOS_ADDRESS" \
  --data-urlencode "signer=$DEXOS_SIGNER"
```

该 nonce 属于 API 钱包 scope，不能拿主钱包账户 nonce 代替。授权刚成功时，首次写请求带 `x-dexos-min-seq`，值取授权回执的 `seq`，确保网关能看到授权。

## 金库交易身份

读取金库账户使用 `vault` 查询参数。代表金库写入时，信封同时带 `vault` 和 manager 的主钱包 `account`，不能带 `subaccount`。主钱包签名使用金库账户自己的 nonce 与 `signingAccountId`。API 钱包须授权在 manager 认领金库时使用的账户上。

金库身份允许下单、撤单、换单、cancel-all、schedule-cancel 和调整杠杆；其他操作会被拒绝。金库入金、赎回等通过各自的 `/v1/vaults/*` 接口，由对应参与者签名，不使用“代表金库交易”的身份。

## 排查签名失败

先检查环境及 domain，再检查账户身份和 nonce scope、整数换算、字段顺序和类型，以及 API 钱包的 command hash。错误码为 `GatewayBadSignature` 的请求未通过预检；`UnknownAgent`、`AgentExpired` 表示授权问题。不要用不断更换 nonce 的方式绕过根因。
