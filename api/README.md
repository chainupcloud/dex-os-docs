# API 规格发布副本

`openapi-v1.json` 原样复制自 dex-os main 提交 `0fece24ad5255d19b921af1bff8510f26a9d7666` 的 `web/openapi-v1.json`。

两种语言共用本文件，不手工修改字段或翻译协议。更新时从明确的上游提交重新复制，审查差异，在同一 PR 更新源提交和相关指南。

GitBook OpenAPI 导入地址：

https://raw.githubusercontent.com/chainupcloud/dex-os-docs/main/api/openapi-v1.json

当前规格的 servers 为相对路径 `/`，只适合与网关同源的 Scalar。GitBook 上的交互请求需要运营方确认公开 API 地址并配置服务器；不能把 GitBook 域名当作交易网关。页面导入、语言切换和交互调用仍需 GitBook 验收。
