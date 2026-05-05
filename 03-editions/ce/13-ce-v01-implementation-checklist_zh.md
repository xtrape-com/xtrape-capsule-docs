---
status: draft
audience: founders
stability: unstable
last_reviewed: 2026-05-05
edition: ce
phase: current
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 13-ce-v01-implementation-checklist.md
翻译状态 / Translation Status: 已翻译 / Translated
生成时间 / Generated: 2026-05-01 09:28:54
================================================================================
注意 / Notes:
- 技术术语如 Capsule Service、Agent、Opstage 等保留英文或采用中英对照
- 代码块中的内容不翻译
- 文件路径和 URL 不翻译
- 保持原有的 Markdown 格式结构
================================================================================
-->

# CE（社区版） v0.1 实现 Checklist

- Status: 实现 Target
- Edition: CE（社区版）
- Priority: Current
- Audience: product designers, architects, backend developers, frontend developers, agent SDK developers, test engineers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/` (OpenAPI / Prisma) disagree, the ADRs and contracts win for CE（社区版） v0.1.

This checklist 定义 the minimum implementation acceptance criteria for Opstage（运维舞台） CE（社区版） v0.1.

## 0. Planning Contracts

- [ ] ADRs in `08-decisions/` are reviewed.
- [ ] Contracts in `09-contracts/` are reviewed.
- [ ] 实现 plans in `10-implementation/` are reviewed.
- [ ] 实现 follows `10-implementation/05-implementation-sequence.md`.

## 1. Product Flow

- [ ] User can start Opstage（运维舞台） CE（社区版） locally.
- [ ] User can start Opstage（运维舞台） CE（社区版） with Docker and a persistent data volume.
- [ ] User can initialize or log in as a local admin.
- [ ] User can create a registration token.
- [ ] Demo Node.js Capsule Service（胶囊服务） can register through the Node Agent（代理） SDK.
- [ ] UI shows registered Agent（代理）.
- [ ] UI shows reported Capsule Service（胶囊服务）.
- [ ] UI shows manifest, health, configs, and actions.
- [ ] User can trigger a predefined action.
- [ ] Agent（代理） can poll and execute the Command.
- [ ] Agent（代理） can report CommandResult.
- [ ] UI shows Command result.
- [ ] Audit log records key operations.

## 2. Backend

- [ ] Fastify API server exists.
- [ ] Zod validation exists for request bodies.
- [ ] Backend routes conform to `09-contracts/openapi/opstage-ce-v0.1.yaml`.
- [ ] Prisma schema and migrations exist.
- [ ] Prisma schema conforms to `09-contracts/prisma/schema.prisma`.
- [ ] SQLite database is initialized under the configured data directory.
- [ ] Default Workspace is bootstrapped.
- [ ] Local admin user bootstrap exists.
- [ ] Admin authentication is enabled by default.
- [ ] Registration tokens are stored as hashes.
- [ ] Agent（代理） tokens are stored as hashes.
- [ ] Agent（代理） API rejects disabled or revoked Agents.
- [ ] Backend calculates online, stale, offline, and unhealthy statuses.
- [ ] Backend writes AuditEvents for login, failed login, token creation/revocation, Agent（代理） registration, Command creation, and Command completion.

## 3. API

- [ ] OpenAPI contract exists and parses successfully.
- [ ] Admin API uses `/api/admin/*`.
- [ ] Agent（代理） API uses `/api/agents/*`.
- [ ] System API uses `/api/system/*`.
- [ ] Capsule Service（胶囊服务） resource path uses `capsule-services`.
- [ ] `/api/system/health` does not expose sensitive data.
- [ ] `/api/system/version` does not expose sensitive data.

## 4. Command and Action

- [ ] ActionDefinition 支持 `name`, `label`, `description`, `dangerLevel` (LOW/MEDIUM/HIGH), `requiresConfirmation`, `inputSchemaJson`, and `timeoutSeconds`.
- [ ] Command 支持 `PENDING`, `RUNNING`, `SUCCEEDED`, `FAILED`, and `EXPIRED` states. (`CANCELLED` is reserved; no UI required in CE（社区版） v0.1.)
- [ ] Backend validates action existence before Command creation.
- [ ] Backend validates Agent（代理） ownership before Command polling and result submission.
- [ ] Backend prevents terminal Command states from being overwritten incorrectly.
- [ ] No shell, exec, bash, or arbitrary script action is exposed as a normal CE（社区版） feature.

## 5. UI

- [ ] Login page exists.
- [ ] Dashboard summary exists.
- [ ] Agent（代理） list and detail pages exist.
- [ ] Capsule Service（胶囊服务） list and detail pages exist.
- [ ] Service detail shows manifest, health, configs, actions, recent Commands, and recent AuditEvents.
- [ ] Command list and detail pages exist.
- [ ] AuditEvent list exists.
- [ ] Action execution UI shows danger level and confirmation when required.

## 6. Node Agent（代理） SDK

- [ ] SDK can register with registration token.
- [ ] SDK persists Agent（代理） token locally.
- [ ] SDK sends heartbeat.
- [ ] SDK reports service manifest.
- [ ] SDK reports health.
- [ ] SDK reports config metadata.
- [ ] SDK reports action metadata.
- [ ] SDK polls Commands.
- [ ] SDK dispatches Commands to local action handlers.
- [ ] SDK reports CommandResult.
- [ ] SDK uses retry/backoff for transient Backend failures.
- [ ] SDK logs do not leak tokens or secrets.

## 7. 安全

- [ ] No default weak admin credential exists.
- [ ] Passwords are hashed with argon2 or bcrypt.
- [ ] Session secret is configurable.
- [ ] Registration token raw value is shown only once.
- [ ] Agent（代理） token raw value is shown only once to the Agent（代理）.
- [ ] Tokens are never logged.
- [ ] Sensitive config values are masked or represented as `secretRef`.
- [ ] UI is not usable without authentication by default.

## 8. Non-Goals Check

- [ ] No tenant system.
- [ ] No billing or subscription system.
- [ ] No enterprise RBAC.
- [ ] No SSO/OIDC/LDAP/SAML.
- [ ] No Redis or queue requirement.
- [ ] No Kubernetes requirement.
- [ ] No Agent（代理） Gateway.
- [ ] No Sidecar or External Agent（代理） implementation.
- [ ] No Java/Python/Go SDK implementation.
- [ ] No full observability platform.
- [ ] No secret vault.
- [ ] No remote shell.
- [ ] No arbitrary script execution.
