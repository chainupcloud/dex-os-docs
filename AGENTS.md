# Unibook 文档维护约定

- 本仓面向交易用户、金库参与者和 API 开发者。正文中英双语，分别位于 `content/zh` 与 `content/en`；文件相对路径、目录层级及业务含义保持一致，同一 PR 同步更新。
- 中文正文说人话，英文使用业内标准术语。API 路径、字段、枚举、错误码和代码标识符不翻译。
- 所有能力说明必须核对 dex-os 已合入代码或具名契约测试。明确区分已实现、已部署和已验收；不虚构界面操作、公开环境地址或测试结果。
- API 唯一事实源为 dex-os 的 `web/openapi-v1.json`；GitBook 用其生成版 `web/gitbook/openapi-v1.yaml`。`api/openapi-v1.yaml` 与中文版 `api/openapi-v1.zh.yaml`（同一规格、只翻译读者说明，取自 `web/gitbook/openapi-v1.zh.yaml`）是原样发布副本；英文页引用前者，中文页引用后者，只跟 dex-os `main`（测试环境只部署 `main`），源提交记录在 `api/README.md`。不在副本修补协议或翻译字段。
- 同步由 `.github/workflows/sync-openapi.yml` 每小时比对 dex-os `main`，有变化就复制规格、用 `scripts/gen_pages.py` 重新生成 `content/*/api/` 下的接口页并开 PR；合入即发布，须人审。接口页不手改，要调整页面分组或隐藏接口就改生成脚本。
- 仅同步公开 v1 API。不得提交凭据、私钥、真实账户数据、内部部署地址或管理 API。文档不会改变业务行为；发现实现问题交回上游对应任务。
- GitBook 站点配置为根目录 `gitbook-docs.yaml`，每种语言由自己的 `.gitbook.yaml` 与 `SUMMARY.md` 指定内容。执行计划不进入对外导航。
- 提交前检查中英文文件对应、全部本地链接、API 块与规格的 operation 对应及规格副本一致性。GitBook 页面渲染、语言切换和交互请求必须实际验收，静态检查不能代替。
- 纯文档变更不跑交易栈全量门禁。交易、资金写请求和公开发布需要明确授权；不得为验证文档擅自操作共享账户。
