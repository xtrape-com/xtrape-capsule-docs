---
status: in-progress
audience: ai-coding-agents
stability: evolving
last_reviewed: 2026-05-14
edition: ce
phase: v0.2
translation: machine-assisted
---

# CE v0.2 实施进展日志

本日志记录 Public Preview 周期中四个公开仓库 `v0.2` 分支实际交付的内容。它是 `07-roadmap/01-ce-roadmap.md` § 18(CE v0.2 方向)在实施侧的对应物。

## 日志记录时刻的仓库状态

| 仓库 | 分支 | PR | 状态 |
| --- | --- | --- | --- |
| `xtrape-capsule-ce` | `v0.2` | [#16](https://github.com/xtrape-com/xtrape-capsule-ce/pull/16) | open |
| `xtrape-capsule-agent-node` | `v0.2` | [#7](https://github.com/xtrape-com/xtrape-capsule-agent-node/pull/7) | open |
| `xtrape-capsule-contracts-node` | `v0.2` | [#9](https://github.com/xtrape-com/xtrape-capsule-contracts-node/pull/9) | open |
| `xtrape-capsule-site` | `v0.2` | [#6](https://github.com/xtrape-com/xtrape-capsule-site/pull/6) | open |

## 已交付 surface

### 运行时成熟度(CE)

- **effectiveStatus 实时性。** 现在 `effectiveStatus` 折合了 agent 在线/离线状态和心跳新鲜度,不再只看最后上报的 `healthStatus`。Service 响应额外携带 `storedStatus`,供历史/工具消费者读取最后一次持久化值。
- **心跳写入节流。** 心跳处理不再每次都写 `agents.status`,仅在 `OFFLINE → ONLINE` 转换时写。新鲜度仅从 `lastHeartbeatAt` 读取,每个 agent 每次心跳少一次行写。
- **系统端点。** `/api/system/health`(SQLite 探针 + uptime + version + edition)和 `/api/system/version`(commit + 构建时间戳,来自 OCI 标签)已完整接线。Docker 镜像构建时内嵌 OCI 元数据。
- **命令失败 surface。** 当 agent 上报 `success: false`,后端将 `errorCode` / `errorMessage` 直接抬到 `commands` 行。命令列表端点和 UI 都能渲染这些字段,无需 join `command_results`。`durationMs` 在序列化时由 `completedAt - startedAt` 计算。
- **Metrics 增强。** `/api/admin/metrics` 现在报告 `commandDurations.{p50Ms,p95Ms,maxMs,meanMs,sampleSize}`、`topErrorCodes` 数组和 `agents.{total,online,offline,stale}` 分布,旁列于已有的 operational counters。

### UI 重构(CE)

- **ADR-0007 一致性达成。** `apps/opstage-ui/src/App.tsx` 渐进式从 1193 行拆到 124 行。新的模块布局在 `apps/opstage-ui/src/`:
  - `lib/` — `types.ts`、`list-helpers.ts`、`format.ts`、`metrics.ts`。
  - `pages/` — 每条路由一个组件:`LoginPage`、`DashboardPage`、`UsersPage`、`RegistrationTokensPage`、`AgentsPage`、`CommandsPage`、`AuditEventsPage`、`SettingsPage`、`LanguageSwitcher`。
  - `pages/services/` — `helpers.tsx`(schema/result/payload/account 工具)、`SchemaPayloadFields.tsx`、`ActionResult.tsx`(四个 action-result 组件)、`ServiceDrawer.tsx`、`ServicesPage.tsx`。
- `App.tsx` 仍保留 `action-result-list.test.tsx` 所需的回向兼容重导出(`formatBytes`、`formatDurationMs`、`diagnosticRows`、`hasMetricWarning`、`metricRows`、`formatRelativeTime`、`renderListCell`、`resolveRowPayload`、`resultRowKey`)。
- 验证:`pnpm typecheck` 通过,8/8 UI 测试通过,`pnpm build` 通过。

### Agent SDK(`xtrape-capsule-agent-node`)

- **类型化错误。** 新增 `RegistrationError`、`AgentAuthError`、`NetworkError` 子类。注册/认证失败不可重试(直接抛出);传输失败在 SDK backoff 预算内可重试,超出后以 `NetworkError` 浮出。替代此前的无类型 `Error` surface。
- **结构化日志 sink。** 可选 `onLog` 回调接收 `{ level, event, context, data }` 记录,适合日志聚合器。未提供时回落到现有 console-shaped sink——纯增量,对现有消费者无破坏。
- **`examples/` 目录。** 注册、心跳、命令执行的可运行脚本,服务于新接入者。

### Contracts(`xtrape-capsule-contracts-node`)

- **删除 `newId()` 辅助函数。** 一并移除其引入的 `nanoid` runtime 依赖。刻意 breaking change——已验证 CE 不引用 `newId`。外部消费者如使用该辅助函数生成本地 ID,需自行接入 ID 工厂。

### Site(`xtrape-capsule-site`)

- 新增 `docs/version-compatibility.md`(minor 版本固定矩阵)、`docs/troubleshooting.md`(失败 runbook)、`docs/agents/lifecycle.md`(register → heartbeat → token rotation → revoke)。
- `docs/releases/v0.2.0.md` 草案 + Releases 导航重构。
- v0.2 surface 文档新增:`node-embedded-agent.md` 加 `Typed errors` + `Structured logging` 章节,`concepts/management-contract.md` 加 system + metrics 端点规范,`opstage-ce/admin-ui.md` 加一次性 `generatedKey` 操作员段落。

## 横切决策记录

- **ADR-0010**(本语料):一次性 action 密钥临时缓存。镜像至公开 CE ADR `docs/adr/0001-ephemeral-action-secrets.md`。
- **审计元数据 redactor 拆分** — `redactAuditMetadata`(基于值)取代 `writeAudit` 内部基于键名的 pass;`revokedTokens` 等合法字段名不再被错误地置为 `"[REDACTED]"`。
- **重注册时 agent token 轮换** — 重新注册已存在的 agent 时,直接吊销此前 ACTIVE token 并写 `agent.token.rotated` 审计。此前老 token 一直 ACTIVE 直到显式 Revoke Agent。
- **Cookie `Secure` 默认开启** — 严格的 `SESSION_SECRET` schema(≥ 32 字符)现已强制。

## 从 v0.2 推迟项

- **CE #13**(UI 的 `apiList` 改走 `apiFetch`)。本次切线之外,推迟到 v0.3。Release notes 已同步更新。
- 新 v0.2 页面的 **zh-CN 站点翻译**。已 track,本次不交付。

## 日志记录时刻的验证

```
xtrape-capsule-ce/apps/opstage-ui:        pnpm typecheck ✅  pnpm test 8/8 ✅  pnpm build ✅
xtrape-capsule-ce/apps/opstage-backend:   pnpm test 24/24 ✅
xtrape-capsule-agent-node:                pnpm test 30/30 ✅
xtrape-capsule-contracts-node:            pnpm test 33/33 ✅
xtrape-capsule-site:                      pnpm docs:build ✅
```
