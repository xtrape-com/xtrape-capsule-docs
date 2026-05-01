# CE v0.1 API 与安全实现说明

- Status: 实现记录
- Edition: CE
- Priority: Current
- Audience: backend developers, frontend developers, security reviewers, AI coding agents

本文记录 CE v0.1 已实现的 HTTP API 边界和安全行为。

## 1. API 命名空间

| Namespace | 调用方 | 认证方式 |
| --- | --- | --- |
| `/api/system/*` | health check、探针 | Public，不需要 session。 |
| `/api/admin/*` | React console / admin automation | Signed session cookie；修改请求需要 CSRF。 |
| `/api/agents/*` | Capsule Agent | 除首次注册外，使用 Bearer Agent token。 |

正常响应使用 envelope：

```json
{ "success": true, "data": {} }
```

错误响应使用：

```json
{ "success": false, "error": { "code": "...", "message": "..." } }
```

## 2. Admin 认证

已实现流程：

1. `POST /api/admin/auth/login` 校验用户名和密码。
2. Backend 创建内存 session 和 CSRF token。
3. Backend 设置 signed HTTP-only cookie `opstage_session`。
4. `GET /api/admin/auth/me` 返回当前用户和 CSRF token。
5. `POST /api/admin/auth/logout` 删除 session 并清理 cookie。

Cookie 属性：

```text
httpOnly: true
sameSite: lax
secure: NODE_ENV === production
path: /
maxAge: OPSTAGE_SESSION_TTL_SECONDS
```

CE v0.1 的 session 保存在内存中，因此进程重启会使 session 失效。

## 3. CSRF 校验

对 `/api/admin/*` 请求，在以下条件同时满足时要求 CSRF：

- URL 以 `/api/admin/` 开头。
- URL 不是 `/api/admin/auth/login`。
- Method 不是 `GET`、`HEAD`、`OPTIONS`。

调用方必须发送：

```text
X-CSRF-Token: <csrfToken from login/me>
```

CSRF 失败返回 `403 CSRF_INVALID`。

## 4. RBAC

已实现角色：

| 角色 | 读 API | operator 类修改 API | 用户管理 | 备份 |
| --- | --- | --- | --- | --- |
| owner | yes | yes | yes | yes |
| operator | yes | yes | no | no |
| viewer | yes | no | no | no |

owner-only 操作包括用户创建/更新/重置密码和 SQLite 备份。operator-or-owner 操作包括 registration token 创建/撤销、command 创建/取消、Agent disable/revoke、维护任务触发。

## 5. Admin API 路由清单

| Method/path | 用途 | 最低角色 |
| --- | --- | --- |
| `GET /api/system/health` | 健康检查。 | public |
| `GET /api/system/version` | 版本信息。 | public |
| `POST /api/admin/auth/login` | 登录。 | public |
| `POST /api/admin/auth/logout` | 登出。 | authenticated |
| `GET /api/admin/auth/me` | 当前 session。 | authenticated |
| `GET /api/admin/dashboard/summary` | Dashboard 聚合。 | viewer |
| `GET /api/admin/users` | 用户列表。 | owner |
| `POST /api/admin/users` | 创建用户。 | owner |
| `PATCH /api/admin/users/:userId` | 更新用户角色/状态/display name。 | owner |
| `POST /api/admin/users/:userId/reset-password` | 重置密码。 | owner |
| `GET /api/admin/registration-tokens` | Registration token 列表。 | viewer |
| `POST /api/admin/registration-tokens` | 创建 token，并一次性返回明文。 | operator |
| `POST /api/admin/registration-tokens/:tokenId/revoke` | 撤销 token。 | operator |
| `GET /api/admin/agents` | Agent 列表/过滤。 | viewer |
| `GET /api/admin/agents/:agentId` | Agent 详情。 | viewer |
| `POST /api/admin/agents/:agentId/disable` | Disable Agent。 | operator |
| `POST /api/admin/agents/:agentId/revoke` | Revoke Agent 和活跃 token。 | operator |
| `GET /api/admin/capsule-services` | Service 列表/过滤。 | viewer |
| `GET /api/admin/capsule-services/:serviceId` | Service 详情。 | viewer |
| `POST /api/admin/capsule-services/:serviceId/actions/:actionName` | 创建 action command。 | operator |
| `GET /api/admin/commands` | Command 列表/过滤。 | viewer |
| `GET /api/admin/commands/:commandId` | Command 详情。 | viewer |
| `POST /api/admin/commands/:commandId/cancel` | 取消 pending/running command。 | operator |
| `GET /api/admin/audit-events` | Audit event 列表/过滤。 | viewer |
| `GET /api/admin/audit-events/export` | 导出 audit CSV/JSON。 | viewer |
| `GET /api/admin/settings/maintenance` | 维护配置。 | viewer |
| `POST /api/admin/maintenance/run` | 立即运行维护任务。 | operator |
| `GET /api/admin/metrics` | Metrics 汇总。 | viewer |
| `GET /api/admin/diagnostics/runtime` | Runtime diagnostics。 | viewer |
| `POST /api/admin/backup/sqlite` | 创建/下载 SQLite 备份。 | owner |

## 6. Agent API 路由清单

| Method/path | 用途 | 认证方式 |
| --- | --- | --- |
| `POST /api/agents/register` | 用 registration token 换 Agent token；可携带首次 service report。 | Body 中的 raw registration token。 |
| `POST /api/agents/:agentId/heartbeat` | 更新 heartbeat 和可选 health。 | `Authorization: Bearer opstage_agent_*` |
| `POST /api/agents/:agentId/services/report` | 上报当前 services/config/actions/health。 | Agent bearer token |
| `GET /api/agents/:agentId/commands` | Poll pending command；Backend 标记为 running。 | Agent bearer token |
| `POST /api/agents/:agentId/commands/:commandId/result` | 回报 command 终态结果。 | Agent bearer token |

## 7. 敏感数据处理

已实现默认规则：

- 密码 hash 后持久化。
- Registration token 和 Agent token hash 后持久化。
- 当 `sensitive=true` 时，不保存 config preview/default。
- Audit metadata 不应包含密码或 raw token。
- Agent SDK 会在日志中 redacts token-like 字符串和 secret-like 字段。

## 8. Proxy/TLS 说明

生产类环境中 CE v0.1 应放在 TLS 后面。Backend 仅在 `NODE_ENV=production` 时设置 Secure cookie；部署时必须确保浏览器通过 HTTPS 访问，并且反向代理保留：

```text
Cookie
Set-Cookie
X-CSRF-Token
Authorization
```
