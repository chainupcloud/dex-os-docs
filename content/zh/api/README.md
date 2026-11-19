# API 参考

本参考使用同一份公开 v1 OpenAPI 规格。API 字段与协议保持英文；中文指南解释接入流程。

价格、数量和金额的缩放、签名以及回执处理请先阅读开发者指南。账户数据频道不代表保密访问。

交互请求需要实际交易网关地址；公开网关地址发布前，本规格的服务器主机是占位域名 `api.dexos.invalid`。签名写请求需要先在客户端生成签名，统一通过 `POST /v1/commands` 提交。

[OpenAPI YAML](https://raw.githubusercontent.com/chainupcloud/dex-os-docs/243267520f937019b36af85dc41a6a4887ac4fe4/api/openapi-v1.zh.yaml)

- [交易所信息](exchange.md)
- [市场行情](market-data.md)
- [账户](account.md)
- [金库](vaults.md)
- [订阅](subscriptions.md)
- [资金](funds.md)
- [交易](trading.md)
- [预言机](oracle.md)
- [商户](merchants.md)
- [治理](governance.md)
