# API 参考

本参考使用同一份公开 v1 OpenAPI 规格。API 字段与协议保持英文；中文指南解释接入流程。

价格、数量和金额的缩放、签名以及回执处理请先阅读开发者指南。账户数据频道不代表保密访问。

**Test it** 的请求发往预览网络 `https://dex-preview.unibook.site`（只有测试资金）。签名写请求要先在客户端签名，统一通过 `POST /v1/commands` 提交；想在浏览器里直接签名提交，用 [API 调试台](https://dex-preview.unibook.site/app/api-playground/)。[交易](trading/commands.md)下每条命令都有对应链接。

[OpenAPI YAML](https://raw.githubusercontent.com/chainupcloud/dex-os-docs/421ecf0450369486ffcd175e3d0de399b1958539/api/openapi-v1.zh.yaml)

- [市场行情](market-data.md)
- [账户](account.md)
- [金库](vaults.md)
- [订阅](subscriptions.md)
- [资金](funds.md)
- [交易](trading.md)
