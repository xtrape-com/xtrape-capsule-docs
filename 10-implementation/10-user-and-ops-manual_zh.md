# CE v0.1 使用与运维手册

- Status: 实现记录
- Edition: CE
- Priority: Current
- Audience: CE operators, evaluators, support engineers, AI coding agents

本文说明已实现的 CE v0.1 产品在安装后的使用和运维方式。

## 1. 角色

| 角色 | 适用用户 | 权限 |
| --- | --- | --- |
| `owner` | 系统管理员 | 全量权限，包括用户管理、备份、维护、Agent 生命周期、token、command。 |
| `operator` | 日常运维人员 | 可创建/撤销 registration token、执行/取消 command、disable/revoke Agent、运行维护任务。不能管理用户或创建备份。 |
| `viewer` | 只读观察者 | 可查看 dashboard、清单、command、audit、diagnostics。不能修改状态。 |

系统必须至少保留一个 active owner。Backend 会拒绝降级或禁用最后一个 active owner。

## 2. 首次启动

类生产环境必需配置：

```text
OPSTAGE_ADMIN_USERNAME
OPSTAGE_ADMIN_PASSWORD       # 至少 12 字符
OPSTAGE_SESSION_SECRET       # 至少 32 字符
DATABASE_URL                 # 默认 file:./data/opstage.db
OPSTAGE_STATIC_DIR           # 默认 apps/opstage-ui/dist
```

首次启动时，Backend 会创建默认 Workspace 和初始管理员用户。之后再修改 `OPSTAGE_ADMIN_USERNAME` / `OPSTAGE_ADMIN_PASSWORD` 不会覆盖已有用户。

## 3. 登录与 session 行为

1. 打开 CE console。
2. 使用启动时配置的管理员账号密码登录。
3. Backend 设置 HTTP-only signed `opstage_session` cookie，并返回 CSRF token。
4. UI 在所有会修改状态的 admin request 中发送 `X-CSRF-Token`。

Session 有效期由以下配置控制：

```text
OPSTAGE_SESSION_TTL_SECONDS=28800
```

轮换 `OPSTAGE_SESSION_SECRET` 会让所有活跃 session 失效。

## 4. 创建用户

owner 操作流程：

1. 打开 Settings / Users。
2. 创建 `owner`、`operator` 或 `viewer` 用户。
3. 密码至少 12 字符。
4. owner 可以重置密码和禁用用户。

建议运维模型：

- 至少保留两个 owner 作为 break-glass 访问。
- 日常执行 action 使用 operator 账号。
- 审计、产品、业务观察使用 viewer 账号。

## 5. 接入 Agent 或 demo service

1. 打开 Registration Tokens。
2. 创建 token，并立即复制 raw token；它只展示一次。
3. 使用以下配置启动 Agent：

```text
OPSTAGE_BACKEND_URL=http://localhost:8080
OPSTAGE_REGISTRATION_TOKEN=opstage_reg_...
OPSTAGE_AGENT_TOKEN_FILE=./data/agent-token.json
```

Agent 首次注册后会保存 Agent token 文件，后续重启复用该文件。如果 token 文件被删除，则需要新的 registration token，除非另有可用 Agent token。

## 6. 监控 Agent 和 Service

控制台页面：

- Dashboard：数量概览和最近活动。
- Agents：状态、heartbeat、runtime、disable/revoke 操作。
- Capsule Services：manifest、health、config、actions。
- Commands：action 执行历史和终态结果。
- Audit Events：安全与治理审计轨迹。

常见状态解释：

| 对象 | 状态 | 含义 |
| --- | --- | --- |
| Agent | `PENDING` | 已注册但尚未成功 heartbeat。 |
| Agent | `ONLINE` | 最近有 heartbeat。 |
| Agent | `OFFLINE` | 超过 stale threshold 未 heartbeat。 |
| Agent | `DISABLED` | 被 operator 暂停。 |
| Agent | `REVOKED` | Agent token 已失效。 |
| Service | `HEALTHY` | Agent 在线且最新 health 为 `UP`。 |
| Service | `UNHEALTHY` | 按 CE 规则最新 health 表示异常。 |
| Service | `OFFLINE` / `STALE` | Agent/service 不再新鲜。 |

Stale 检测使用：

```text
OPSTAGE_AGENT_OFFLINE_THRESHOLD_SECONDS=90
OPSTAGE_MAINTENANCE_INTERVAL_SECONDS=60
```

## 7. 执行 Action

1. 打开 Capsule Service。
2. 选择一个 action。
3. UI 打开 action panel，并向 Agent 请求动态 prepare metadata。
4. 通过 schema-driven form 或 JSON override 提供 payload。
5. 如果 action 需要 confirmation 或 danger 较高，点击确认。
6. 提交后创建 Command。
7. Agent poll command、执行 handler、回报 result。

操作员需要了解的 action panel 行为：

- 打开 action 会创建一条 `ACTION_PREPARE` Command。这是正常行为，用于加载动态字段、默认值和当前状态。
- 如果 prepare 超时或失败，面板会保持打开，并展示 `commandId`、`commandStatus`、`agentId`、`serviceId` 等诊断信息。可以用这些信息到 Commands 页面和 Agent 日志中排查。
- 长任务 action 会在后台继续执行。Action panel 会自动轮询 Command，并在进入终态后刷新 service/account 状态。
- List action 可以在原始 JSON result 上方展示表格；原始 JSON 仍保留用于排障。
- List 表格中的行级 action 会创建普通 Command。操作运行时对应行会显示 loading，完成后列表会自动刷新。

已实现的 demo service 暴露：

- `echo`：返回提交的 payload。
- `runHealthCheck`：返回当前 health provider 结果。

## 8. 维护任务

当 `OPSTAGE_MAINTENANCE_INTERVAL_SECONDS > 0` 时，维护任务会周期性运行。operator 和 owner 也可以手动触发。

当前维护任务包括：

- 过期超过 `expiresAt` 的 registration token。
- 过期超过 `expiresAt` 的 pending/running command。
- 将 stale 的 online Agent 标记为 offline。
- 更新关联 service 的新鲜度状态。
- 按 `OPSTAGE_AUDIT_RETENTION_DAYS` 清理旧 audit event。

将 interval 设置为 `0` 可关闭后台定时器；授权用户仍可通过 API/UI 手动触发。

## 9. 备份和审计导出

owner 可以在 Settings 中创建 SQLite 备份。Backend 会将备份写入：

```text
OPSTAGE_BACKUP_DIR=./data/backups
```

Audit Events 页面/API 支持 CSV 或 JSON 导出。

运维建议：

- 备份 `/app/data` 或 `DATABASE_URL` 背后的宿主路径。
- 将备份保存到容器宿主机以外的位置。
- 正式依赖备份前先演练恢复。

## 10. Diagnostics

控制台提供 runtime diagnostics 和 metrics：

- Node/runtime 元数据。
- uptime 和环境摘要。
- 用于 dashboard/状态检查的计数指标。

不要在无认证和 TLS 的情况下公开 diagnostics。

## 11. 快速排障表

| 现象 | 可能原因 | 修复 |
| --- | --- | --- |
| 重启后登录失败 | Session secret 已轮换 | 重新登录；如果密码未知，需要恢复 DB 或补充 admin recovery 流程。 |
| Registration token 不可用 | token 已使用/撤销/过期 | 创建新的 registration token。 |
| Agent 显示 offline | heartbeat 停止或 stale threshold 太低 | 检查 Agent 日志、网络和 `OPSTAGE_AGENT_OFFLINE_THRESHOLD_SECONDS`。 |
| Action 一直 pending | Agent 未 polling 或 token 被 revoke | 检查 Agent 状态和 token 文件。 |
| Action prepare 超时 | Agent 离线、繁忙或没有 polling prepare command | 使用 prepare diagnostics 中的 `commandId` 和 Commands 页面排查；检查 Agent 日志和 polling interval。 |
| Row action 成功但列表看起来未更新 | list refresh 失败或 service 状态尚未更新 | 点击 Refresh 或重新执行 list action；检查 row action Command。 |
| POST 返回 `CSRF_INVALID` | 缺少 `X-CSRF-Token` 或 cookie 问题 | 确保代理保留 cookie 和请求头。 |
| Backup endpoint forbidden | 当前用户不是 owner | 使用 owner 角色登录。 |
