---
status: implemented
audience: ai-coding-agents
stability: evolving
last_reviewed: 2026-05-05
edition: ce
phase: current
---

# CE v0.1 API and Security Implementation

- Status: Implementation Record
- Edition: CE
- Priority: Current
- Audience: backend developers, frontend developers, security reviewers, AI coding agents

This document records the implemented HTTP surface and security behavior for CE v0.1.

## 1. API namespaces

| Namespace | Caller | Authentication |
| --- | --- | --- |
| `/api/system/*` | health checks, diagnostics probes | Public. No session required. |
| `/api/admin/*` | React console / admin automation | Signed session cookie; CSRF required for mutating requests. |
| `/api/agents/*` | Capsule Agents | Bearer Agent token, except initial registration. |

All normal responses are envelopes:

```json
{ "success": true, "data": {} }
```

Errors use:

```json
{ "success": false, "error": { "code": "...", "message": "..." } }
```

## 2. Admin authentication

Implemented flow:

1. `POST /api/admin/auth/login` validates username/password.
2. Backend creates an in-memory session and CSRF token.
3. Backend sets signed HTTP-only cookie `opstage_session`.
4. `GET /api/admin/auth/me` returns current user and CSRF token.
5. `POST /api/admin/auth/logout` deletes the session and clears cookie.

Cookie attributes:

```text
httpOnly: true
sameSite: lax
secure: NODE_ENV === production
path: /
maxAge: OPSTAGE_SESSION_TTL_SECONDS
```

Sessions are in memory in CE v0.1, so process restart invalidates sessions.

## 3. CSRF enforcement

For `/api/admin/*` requests, CSRF is required when all are true:

- URL starts with `/api/admin/`.
- URL is not `/api/admin/auth/login`.
- Method is not `GET`, `HEAD`, or `OPTIONS`.

The caller must send:

```text
X-CSRF-Token: <csrfToken from login/me>
```

CSRF failure returns `403 CSRF_INVALID`.

## 4. RBAC

Implemented roles:

| Role | Read APIs | Mutating operator APIs | User management | Backup |
| --- | --- | --- | --- | --- |
| owner | yes | yes | yes | yes |
| operator | yes | yes | no | no |
| viewer | yes | no | no | no |

Owner-only operations include user create/update/reset-password and SQLite backup. Operator-or-owner operations include
registration token creation/revocation, command creation/cancel, Agent disable/revoke, and maintenance trigger.

## 5. Admin API route inventory

| Method/path | Purpose | Min role |
| --- | --- | --- |
| `GET /api/system/health` | Health check. | public |
| `GET /api/system/version` | Version info. | public |
| `POST /api/admin/auth/login` | Login. | public |
| `POST /api/admin/auth/logout` | Logout. | authenticated |
| `GET /api/admin/auth/me` | Current session. | authenticated |
| `GET /api/admin/dashboard/summary` | Dashboard aggregate. | viewer |
| `GET /api/admin/users` | List users. | owner |
| `POST /api/admin/users` | Create user. | owner |
| `PATCH /api/admin/users/:userId` | Update user role/status/display name. | owner |
| `POST /api/admin/users/:userId/reset-password` | Reset password. | owner |
| `GET /api/admin/registration-tokens` | List registration tokens. | viewer |
| `POST /api/admin/registration-tokens` | Create token and return raw value once. | operator |
| `POST /api/admin/registration-tokens/:tokenId/revoke` | Revoke token. | operator |
| `GET /api/admin/agents` | List/filter Agents. | viewer |
| `GET /api/admin/agents/:agentId` | Agent detail. | viewer |
| `POST /api/admin/agents/:agentId/disable` | Disable Agent. | operator |
| `POST /api/admin/agents/:agentId/revoke` | Revoke Agent and active tokens. | operator |
| `GET /api/admin/capsule-services` | List/filter services. | viewer |
| `GET /api/admin/capsule-services/:serviceId` | Service detail. | viewer |
| `POST /api/admin/capsule-services/:serviceId/actions/:actionName` | Create action command. | operator |
| `GET /api/admin/commands` | List/filter commands. | viewer |
| `GET /api/admin/commands/:commandId` | Command detail. | viewer |
| `POST /api/admin/commands/:commandId/cancel` | Cancel pending/running command. | operator |
| `GET /api/admin/audit-events` | List/filter audit events. | viewer |
| `GET /api/admin/audit-events/export` | Export audit CSV/JSON. | viewer |
| `GET /api/admin/settings/maintenance` | Maintenance config. | viewer |
| `POST /api/admin/maintenance/run` | Run maintenance now. | operator |
| `GET /api/admin/metrics` | Metrics summary. | viewer |
| `GET /api/admin/diagnostics/runtime` | Runtime diagnostics. | viewer |
| `POST /api/admin/backup/sqlite` | Create/download SQLite backup. | owner |

## 6. Agent API route inventory

| Method/path | Purpose | Authentication |
| --- | --- | --- |
| `POST /api/agents/register` | Exchange registration token for Agent token; optionally report first service. | Raw registration token in body. |
| `POST /api/agents/:agentId/heartbeat` | Update heartbeat and optional health. | `Authorization: Bearer opstage_agent_*` |
| `POST /api/agents/:agentId/services/report` | Report current services/config/actions/health. | Agent bearer token |
| `GET /api/agents/:agentId/commands` | Poll pending commands; backend marks them running. | Agent bearer token |
| `POST /api/agents/:agentId/commands/:commandId/result` | Report terminal command result. | Agent bearer token |

## 7. Sensitive data handling

Implemented defaults:

- Passwords are hashed before persistence.
- Registration and Agent tokens are hashed before persistence.
- Sensitive config previews/defaults are not stored when `sensitive=true`.
- Audit metadata should not include passwords or raw tokens.
- Agent SDK redacts token-like strings and secret-like fields in logs.

## 8. Proxy/TLS notes

CE v0.1 should be served behind TLS in production-like environments. The backend sets `Secure` cookie only when
`NODE_ENV=production`; deployments must ensure browser access uses HTTPS and the reverse proxy preserves:

```text
Cookie
Set-Cookie
X-CSRF-Token
Authorization
```
