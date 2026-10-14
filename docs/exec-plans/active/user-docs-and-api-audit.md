# DEXOS 用户文档与 v1 API 审查

> owner 已确认：2026-10-14 会话，文档使用独立仓库 chainupcloud/dex-os-docs；按推荐执行审查与文档建设，GitBook 已创建。

## 目标与验收

面向交易用户、金库参与者和 API 接入开发者建设中英双语文档，使用 GitBook 展示，GitHub 保存可审查的内容。

- 中文为默认入口，英文提供对应页面；两种语言保持相同文件路径、导航层级及业务语义，变更在同一 PR 更新。
- API 路径、字段、错误码、签名类型和代码示例不翻译；两种语言共用同一份上游 OpenAPI，不分别维护两份接口契约。API Reference 的说明文本本地化须另行验证 GitBook 能力，不宣称已有双语自动翻译。

- 独立审查固定 dex-os main 提交上的 v1 实现、OpenAPI、Scalar 和相关 SDK 契约；结论附源码或测试证据。
- 所有发现区分已知问题、新问题、正在实现和未部署；已有问题关联 dex-liquidity #826，不重复开卡或实现。
- 用户可以按指南完成测试环境首次接入，理解交易、保证金、资金费、金库及出入金规则。
- API 示例覆盖公共读取、签名写请求、回执查询、WS 订阅及断线恢复；测试环境写操作另行明确授权和账户归属。
- GitBook 预览能呈现导航和 API 文档；从 GitHub 更新内容及 API 规格后，能验证同步结果。
- 发布、GitBook 组织连接及域名需要 owner 提供目标并确认；不发布未验证的环境地址或能力。

## 技术方案

- 用户文档位于独立 docs 仓库；不复制 dex-os 内部部署、设计和工程手册。
- API 唯一事实源为 dex-os 的 web/openapi-v1.json；文档仓库如需保存发布副本，必须记录源提交并在更新 PR 中核对，不手工维护第二份规格。
- Markdown 内容通过 Git Sync 接 GitBook；OpenAPI 的导入和更新独立验收，不假设 Git Sync 自动更新 API 引用。
- GitBook 使用的凭据不得入库。公开仓库只收对外内容；不得出现管理员接口、内部地址、凭据或用户账户数据。
- 当前 #826 负责接口补齐、SDK/前端/做市适配及规格修复。本任务仅审查、反馈和编写用户文档；不修改其业务文件，不运行共享账户 live 测试，不部署服务。
- 审查基准使用独立 checkout 固定提交，交付前对照 #826 新合入提交复核变化；代码已合入与环境已部署分别表述。

## 协作约定

允许使用 agent，先完成只读审查，再写文档，避免文档建立在未核实的行为上。

| 角色 | 负责范围 | 文件归属 |
|---|---|---|
| API 审查 agent | REST 路由、请求响应、签名、错误及测试覆盖 | 只读 dex-os / SDK，结论交协调方 |
| Scalar 与 WS 审查 agent | 页面可用性、示例、订阅、恢复及 OpenAPI 展示 | 只读源码和页面，结论交协调方 |
| 用户文档 agent | 用户流程、概念、常见问题 | guides/ 下的用户内容 |
| 协调方 | 计划、开发者文档、导航、同步与最终复核 | README.md、SUMMARY.md、developers/、api/、GitBook 配置 |

审查结果进入本计划或 PR，不另建台账。合入顺序：审查与结构确认 → 用户和开发者文档 → API 规格引用 → GitBook 预览验收 → 发布。

## 步骤

- [x] 确认独立仓库，按 zerohacker666 SSH 别名克隆空仓库。
- [x] 读取 #826 当前范围，明确业务修复归属。
- [x] owner 确认本计划的目标、验收和风险边界。
- [x] 固定 dex-os 最新 main 基准，派只读审查 agent；验证路由与 schema、金额精度、身份、签名、nonce、回执、分页、限流、WS 恢复。
- [ ] 汇总发现，与 #826 去重；区分发布阻塞和文档补充。
- [x] 建文档导航，编写用户指南及开发者指南；每个行为注明核实来源，未完成能力不写成可用。
- [ ] 复用现有契约测试验证示例，必要的新检查使用 Go/TS 测试；仅纯文档变更不运行交易栈全量门禁。
- [ ] 配置 GitBook Git Sync 和 OpenAPI，验证预览、链接、示例及更新同步。
- [ ] 对照最新 main 复核差异，提交 PR 附验证结果和人工尾项，确认后发布。

## 变更记录

- 2026-10-14：owner 要求中英双语，内容分为 content/zh 与 content/en，GitBook 同一 section 下配置两个语言 space；保留中文 space key。
- 2026-10-14：owner 指定已创建的 chainupcloud/dex-os-docs，要求使用与做市仓库相同的 zerohacker666 GitHub 账号方式克隆；已完成。仓库当前公开且为空。

## 首轮审查结果（2026-10-14）

审查基准从 `3c1ce22` 更新到 `0fece24ad5255d19b921af1bff8510f26a9d7666`，由独立克隆读取。未修改 dex-os / SDK，未跑 live、未部署。静态审查不代表页面或真实 HTTP 验收。

| 发现 | 证据 | 归属与处置 |
|---|---|---|
| WS 金库订阅说明同时写支持和不支持 | openapi-v1.json 的 x-websocket.rules；v1.rs 的 vault 订阅解析 | #826 已知问题，不另改规格副本；指南按实现说明 |
| vault、DEX 与部分写回执 schema 为空 object，required 不完整 | openapi-v1.json：vaults、dexes、leverage、transfer | vault / required 已知归 #826；DEX 与写回执作为补充发现 |
| operation responses 无 429 | 所有 operation responses；v1.rs 限流中间件实际会返回 GatewayRateLimited | 新发现，指南补处理说明；上游修复后重新复制规格 |
| clientOrderId 说明仍限于 ack=result | openapi-v1.json Order.clientOrderId；v1.rs order_by_client_id 支持执行历史映射 | 新发现，指南不沿用旧限制 |
| v1 签名类型串未做权威自动对照 | scripts/check-openapi.mjs 只检查 planned POST 的扩展存在 | 新发现；应在上游加测试，文档仓库不复制签名常量 |
| nowMs 共享信封说明漏 ScheduleCancel | openapi-v1.json；v1_write.rs ScheduleCancel / cancel-all | 新发现，签名指南按具体命令解释 |
| 快速开始恢复指引漏 epoch / upper | OpenAPI info.description 与 x-websocket.rules / 实现对照 | 指南补完整流程 |
| Scalar 默认 legacy 含 admin 路径 | web/docs.html 默认规格；v1 规格无 admin 路径 | 对外只引用 v1；默认入口问题留上游 |
| 缺完整可运行签名示例 | 写操作没有标准 requestBody examples；x-eip712 是自定义扩展 | 不宣称 Scalar 可自动签名，SDK 示例需进一步验证 |

GitBook 待验收：OpenAPI 块实际渲染、自定义签名扩展可见性、语言切换、公开 API 服务器地址及交互请求。dex-os 源仓库为 private，因此公开 v1 规格原样发布至本仓 api/openapi-v1.json，api/README.md 记录源提交；协议字段不手工翻译或修改。

2026-10-14 实施：中英各 5 篇用户指南、5 篇开发者指南、8 篇 API 概览/分类页已编写。静态验证通过：21 个文件逐语言对应，全部本地链接存在，54 个 operation 每语言完整且不重复，规格与上游字节一致，curl 示例 Bash 语法通过。尚未验证签名成功路径、真实 HTTP、Scalar/GitBook 页面与交互请求；任务保留 active。

2026-10-14 同步修复：GitHub status 证明 10d46a8 单语言成功、d5fc7af 增加 section 后出现站点更新 Internal server error，正文合入前已失败。官方套餐说明 section 需 Ultimate，而语言 variant 各套餐支持；未确认实际套餐。去掉不必要 section，将中文、英文直接作为顶层 spaces，保留稳定 key 和全部内容。官方 schema 兼容校验、唯一 key、唯一默认语言及目录检查通过，实际同步结果另验。
