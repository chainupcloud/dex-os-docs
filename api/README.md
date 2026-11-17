# API 规格发布副本

`openapi-v1.yaml` 原样复制自 dex-os 提交 `ffe6e182571258b93e8d26c2a496a4bb1a1ca48f` 的 `web/gitbook/openapi-v1.yaml`（chainupcloud/dex-os#633 的分支头，目标分支 `dev`，复制时尚未合入）。该 YAML 是 dex-os 用 `scripts/gen-gitbook-openapi.mjs` 从 `web/openapi-v1.json` 加覆盖层生成的 GitBook 版，接口契约与 JSON 相同，只改了服务器地址、tag 页面标题和给读者看的描述。

两种语言共用本文件，不手工修改字段或翻译协议。更新时从明确的上游提交重新复制，审查差异，在同一 PR 更新源提交和相关页面。

GitBook OpenAPI 导入地址：

https://raw.githubusercontent.com/chainupcloud/dex-os-docs/main/api/openapi-v1.yaml

正文中的 API 块固定引用本仓某个提交的规格，避免预览和回滚时读取不同版本。后续更新先提交规格，再在正文更新固定引用；上方 main 地址用于 GitBook 手动导入最新发布副本。

当前规格的 servers 是 `https://{host}`，`host` 缺省为占位域名 `api.dexos.invalid`，GitBook 上的交互请求要等运营方给出公开 API 地址、上游改覆盖层并重新生成后才能用。页面导入、语言切换和交互调用仍需 GitBook 验收。
