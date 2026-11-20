# 交易

签名写请求统一通过 `POST /v1/commands` 提交，签法见[认证指南](../developers/authentication.md)。可以提交哪些命令、由谁签名、走哪条 nonce 车道，见[命令总览](trading/commands.md)。

## POST /v1/commands

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/5bc3cf71888173be4aa5278dd98f425a94b51194/api/openapi-v1.zh.yaml" path="/v1/commands" method="post" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/5bc3cf71888173be4aa5278dd98f425a94b51194/api/openapi-v1.zh.yaml
{% endopenapi %}
