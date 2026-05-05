---
status: draft
audience: ai-coding-agents
stability: unstable
last_reviewed: 2026-05-05
edition: ce
phase: current
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

# CE v0.1 数据库实现说明

- Status: 实现记录
- Edition: CE
- Priority: Current
- Audience: backend developers, operators, architects, AI coding agents

本文记录 CE v0.1 已实现的持久化模型，用于补充 `02-specs/` 中的概念规格和 `09-contracts/` 中的 API 合约。

## 1. 运行时数据库

CE v0.1 运行时使用 SQLite，并通过 `better-sqlite3` 访问。`packages/db/schema.prisma` 中的 Prisma schema 作为关系模型契约和校验参考保留。

默认运行配置：

```text
DATABASE_URL=file:./data/opstage.db
OPSTAGE_DATA_DIR=./data
OPSTAGE_BACKUP_DIR=./data/backups
```

Docker 部署时，`/app/data` 必须挂载为持久化 volume。该目录丢失会导致所有状态丢失，包括管理员用户、Agent token、服务清单、Command、审计日志和备份文件。

## 2. Workspace 模型

CE v0.1 产品行为上是单 Workspace。数据库仍然保留 `Workspace` 行，方便未来演进到多 Workspace 或 EE 能力。

默认 Workspace：

```text
id:  wks_default
code: default
name: Default Workspace
```

所有 Workspace 维度的数据表都会保存 `workspaceId`。

## 3. 核心表

| 表 | 用途 | 关键约束/索引 |
| --- | --- | --- |
| `workspaces` | 逻辑租户边界。 | `code` 唯一。 |
| `users` | 管理控制台账户。 | `username` 唯一；`role` 为 `owner`、`operator`、`viewer`；`status` 为 `ACTIVE` 或 `DISABLED`。 |
| `registration_tokens` | Agent 首次注册使用的一次性 token。 | `tokenHash` 唯一；明文 token 只展示一次，不入库。 |
| `agents` | 已注册的 embedded/sidecar/external Agent。 | `(workspaceId, code)` 唯一；按 status 建索引。 |
| `agent_tokens` | Agent 后续访问使用的长期 bearer token。 | `tokenHash` 唯一；Agent revoke 时会撤销活跃 token。 |
| `capsule_services` | Agent 上报的 Capsule Service 最新清单。 | `(workspaceId, code)` 唯一；关联当前 Agent。 |
| `health_reports` | 健康状态快照。 | 按 `serviceId, reportedAt` 和 `agentId, reportedAt` 建索引。 |
| `config_items` | 配置元数据。 | `(serviceId, configKey)` 唯一；敏感配置不持久化 preview/default。 |
| `action_definitions` | Action 定义目录。 | `(serviceId, name)` 唯一；保存 danger/confirmation 元信息。 |
| `commands` | 管理端发起的 Action 执行请求。 | 按 workspace/status、agent/status、service/create time 建索引。 |
| `command_results` | Agent 回报的终态执行结果。 | 每个 Command 最多一条结果。 |
| `audit_events` | 安全与治理审计日志。 | 按时间、actor、target 建索引。 |
| `system_settings` | 预留 key/value 设置表。 | `(workspaceId, key)` 唯一。 |

## 4. Token 存储规则

明文密钥不入库：

- Registration token 格式为 `opstage_reg_*`，数据库只保存 `tokenHash`。
- Agent token 格式为 `opstage_agent_*`，数据库只保存 `tokenHash`。
- Node Agent SDK 在 Agent 侧本地保存 token 文件，结构为：

```json
{
  "agentId": "agt_...",
  "agentToken": "opstage_agent_...",
  "savedAt": "..."
}
```

该文件必须视为敏感文件；宿主文件系统支持时应使用 `0600` 权限。

## 5. 注册与服务上报流程

1. operator 或 owner 创建 registration token。
2. Backend 只保存 token hash，并一次性返回明文 token。
3. Agent 调用 `POST /api/agents/register`，提交明文 registration token 和可选的首次 service report。
4. Backend 将 registration token 标记为 `USED`，创建/更新 `agents`，创建 active `agent_tokens`，并返回明文 Agent token。
5. Agent 后续使用 Agent token 进行 heartbeat、service report、command polling、command result reporting。
6. Service report 会 upsert `capsule_services`，替换该 service 当前的 `config_items` 和 `action_definitions`，并在包含 health 时追加 `health_reports`。

## 6. 状态持久化

Agent 状态存储在 `agents.status`：

```text
PENDING, ONLINE, OFFLINE, DISABLED, REVOKED
```

Service 有效状态存储在 `capsule_services.status`：

```text
UNKNOWN, HEALTHY, UNHEALTHY, STALE, OFFLINE
```

Health 状态单独存储在 `capsule_services.healthStatus` 和 `health_reports.status`：

```text
UP, DEGRADED, DOWN, UNKNOWN
```

维护任务会把超时未 heartbeat 的在线 Agent 转为 `OFFLINE`，并按 CE 已实现规则更新其服务状态。

## 7. Command 生命周期持久化

Command 由管理端 API 创建，由 Agent 消费：

```text
PENDING -> RUNNING -> SUCCEEDED
PENDING -> RUNNING -> FAILED
PENDING/RUNNING -> CANCELLED
PENDING/RUNNING -> EXPIRED
```

创建 Command 时会设置 `commands.expiresAt`。维护任务会过期 pending/running Command。Agent 成功回报结果时创建一条 `command_results` 并把 Command 标记为 `SUCCEEDED`；失败结果则标记为 `FAILED`。

## 8. 审计保留

Audit event 正常情况下只追加。维护任务会清理早于以下保留期的记录：

```text
OPSTAGE_AUDIT_RETENTION_DAYS=90
```

设置为 `0` 时，维护任务会清理早于当前时间的审计记录，请谨慎使用。

## 9. 备份与恢复说明

owner 可以通过 UI 或 `POST /api/admin/backup/sqlite` 触发 SQLite 备份。Backend 会先把备份写入 `OPSTAGE_BACKUP_DIR`，再返回给调用方。

建议恢复步骤：

1. 停止 Opstage container/process。
2. 将备份数据库文件复制到 `DATABASE_URL` 指定路径。
3. 启动 Opstage。
4. 检查 `/api/system/health` 并登录验证。

CE v0.1 不支持降级恢复。
