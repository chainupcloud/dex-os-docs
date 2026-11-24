# API 规格发布副本

`openapi-v1.yaml` 原样复制自 dex-os `main` 分支提交 `11d6c3b44df6f284e7a9348e0abd769309ab32d4` 的 `web/gitbook/openapi-v1.yaml`。该 YAML 是 dex-os 用 `scripts/gen-gitbook-openapi.mjs` 从 `web/openapi-v1.json` 加覆盖层生成的 GitBook 版，接口契约与 JSON 相同，只改了服务器地址、tag 页面标题和给读者看的描述。

`openapi-v1.zh.yaml` 原样复制自 dex-os `main` 分支提交 `11d6c3b44df6f284e7a9348e0abd769309ab32d4` 的 `web/gitbook/openapi-v1.zh.yaml`，是同一份规格的中文版：路径、字段、枚举和错误码与英文版完全相同，只翻译了给读者看的说明（译文在 dex-os 的 `web/gitbook/strings-v1.zh.json`）。

英文页面引用 `openapi-v1.yaml`，中文页面引用 `openapi-v1.zh.yaml`。两份都不手工修改字段或翻译；译文有误改上游的译文文件。上面两行的格式供同步工作流改写，不要改动句式。

GitBook OpenAPI 导入地址：

- 英文：https://raw.githubusercontent.com/chainupcloud/dex-os-docs/main/api/openapi-v1.yaml
- 中文：https://raw.githubusercontent.com/chainupcloud/dex-os-docs/main/api/openapi-v1.zh.yaml

API 参考页每个接口一节：二级标题 `METHOD path` 加一个 openapi 块，不另写摘要（块自带标题）。规格里的接口全部生成页面；不该对外的接口在上游规格里删除（dex-os#642、dex-os#819、dex-os builder 与 DEX 部署方读接口），不在本仓隐藏。进阶用法的接口（账本账户与授权、自托管与提款追踪、事件补数与异步结果）不按 tag 分页，由 `scripts/gen_pages.py` 的 `advanced` 表放进 `content/*/api/advanced/`，在目录里单独一节。

正文中的 API 块固定引用本仓某个提交的规格，避免预览和回滚时读取不同版本；上方 main 地址用于 GitBook 手动导入最新发布副本。

规格的 servers 是 `https://dex-preview.unibook.site`(预览网络,只有测试资金),并带 `x-enable-proxy: true`:网关不发跨域头,GitBook 的 Test it 经 GitBook 转发。签名命令(`POST /v1/commands`)要在浏览器里签名,Test it 发不了,交易页每条命令另给 API 调试台链接 `https://dex-preview.unibook.site/app/api-playground/?cmd=<命令>`。页面导入、语言切换和交互调用仍需 GitBook 验收。

## 同步

只跟 dex-os `main`。`.github/workflows/sync-openapi.yml` 每小时（也可手动触发）取 dex-os `main` 的 `web/gitbook/openapi-v1.yaml` 和 `openapi-v1.zh.yaml` 与本目录的两份副本比对，不同就在 `sync/openapi-<上游提交前 12 位>` 分支上：

1. 复制两份规格并改写上面的源提交，单独一个提交；
2. 用 `python3 scripts/gen_pages.py . <第 1 步的提交>` 重新生成接口页，并把正文里所有规格链接固定到该提交；
3. 开 PR，关闭被它取代的旧同步 PR。

合入即发布到 GitBook，须人审：看规格差异和 GitBook 预览检查。上游新增了生成脚本不认识的 tag，或者隐藏的接口在上游被删掉，脚本会直接报错，这时改 `scripts/gen_pages.py` 再重跑。

工作流用的配置（只由仓库管理员设置）：

- dex-os 的只读 deploy key，私钥存为本仓 Actions secret `DEXOS_DEPLOY_KEY`；
- 本仓 Settings → Actions → General 勾选 "Allow GitHub Actions to create and approve pull requests"。

当前副本取自 dex-os `dev`（含 dex-os#642 的对外描述清理），dex-os `main` 还没有 `web/gitbook/`；`main` 有了之后，第一次同步会换成 `main` 的版本。
