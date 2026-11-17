# API 规格发布副本

`openapi-v1.yaml` 原样复制自 dex-os `dev` 分支提交 `edfa7dea009ae12d51be5f0ca2aa5e6f3d7549e6` 的 `web/gitbook/openapi-v1.yaml`。该 YAML 是 dex-os 用 `scripts/gen-gitbook-openapi.mjs` 从 `web/openapi-v1.json` 加覆盖层生成的 GitBook 版，接口契约与 JSON 相同，只改了服务器地址、tag 页面标题和给读者看的描述。

两种语言共用本文件，不手工修改字段或翻译协议。上面这一行的格式供同步工作流改写，不要改动句式。

GitBook OpenAPI 导入地址：

https://raw.githubusercontent.com/chainupcloud/dex-os-docs/main/api/openapi-v1.yaml

API 参考页每个接口一节：二级标题 `METHOD path` 加一个 openapi 块，不另写摘要（块自带标题）。以下接口在生产环境不可用，规格里保留、不生成页面：已退役只返回 410 的 `POST /v1/orders/paired`（成对成交改经 `POST /v1/commands`，网关白名单开放，生产网络禁用）和 `POST /v1/account/cctp/deposit`，以及只在模拟网络存在的 `GET /v1/testnet/markets/{id}/oracle`、`GET /v1/testnet/mint-policy`。

正文中的 API 块固定引用本仓某个提交的规格，避免预览和回滚时读取不同版本；上方 main 地址用于 GitBook 手动导入最新发布副本。

当前规格的 servers 是 `https://{host}`，`host` 缺省为占位域名 `api.dexos.invalid`，GitBook 上的交互请求要等运营方给出公开 API 地址、上游改覆盖层并重新生成后才能用。页面导入、语言切换和交互调用仍需 GitBook 验收。

## 同步

只跟 dex-os `main`。`.github/workflows/sync-openapi.yml` 每小时（也可手动触发）取 dex-os `main` 的 `web/gitbook/openapi-v1.yaml` 与本文件比对，不同就在 `sync/openapi-<上游提交前 12 位>` 分支上：

1. 复制规格并改写上面的源提交，单独一个提交；
2. 用 `python3 scripts/gen_pages.py . <第 1 步的提交>` 重新生成接口页，并把正文里所有规格链接固定到该提交；
3. 开 PR，关闭被它取代的旧同步 PR。

合入即发布到 GitBook，须人审：看规格差异和 GitBook 预览检查。上游新增了生成脚本不认识的 tag，或者隐藏的接口在上游被删掉，脚本会直接报错，这时改 `scripts/gen_pages.py` 再重跑。

工作流用的配置（只由仓库管理员设置）：

- dex-os 的只读 deploy key，私钥存为本仓 Actions secret `DEXOS_DEPLOY_KEY`；
- 本仓 Settings → Actions → General 勾选 "Allow GitHub Actions to create and approve pull requests"。

当前副本取自 dex-os `dev`，早于本工作流；dex-os `main` 有了 `web/gitbook/openapi-v1.yaml` 之后，第一次同步会换成 `main` 的版本。
