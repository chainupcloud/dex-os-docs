# Unibook 用户文档

面向交易用户、金库参与者和 API 开发者的中英双语文档。

- GitBook 站点配置：`gitbook-docs.yaml`。
- 对外内容：`content/zh/` 与 `content/en/`，各自由 `SUMMARY.md` 定义导航。
- 执行计划：`docs/exec-plans/`，不属于站点内容。
- API 规格事实源：`chainupcloud/dex-os` 的 `web/openapi-v1.json`；发布副本 `api/openapi-v1.yaml` 取自其 `main` 分支的 GitBook 生成版 `web/gitbook/openapi-v1.yaml`，由 `.github/workflows/sync-openapi.yml` 自动开 PR 同步，接口页由 `scripts/gen_pages.py` 生成。

正文与示例经审查后逐步补齐。
