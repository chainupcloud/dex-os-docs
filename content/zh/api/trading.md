# 交易

签名写请求统一通过 `POST /v1/commands` 提交，签法见[认证指南](../developers/authentication.md)。可以提交哪些命令、由谁签名、用哪条 nonce 序列，见[命令总览](trading/commands.md)。

## POST /v1/commands

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/421ecf0450369486ffcd175e3d0de399b1958539/api/openapi-v1.zh.yaml" path="/v1/commands" method="post" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/421ecf0450369486ffcd175e3d0de399b1958539/api/openapi-v1.zh.yaml
{% endopenapi %}
