<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 05-audit-model.md
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

# Audit Model

- Status: 实施指南
- Edition: 共享
- Priority: 高
- Audience: backend developers, frontend developers, agent SDK developers, architects, security reviewers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/` (OpenAPI / Prisma) disagree, the ADRs and contracts win for CE（社区版） v0.1.

This document 定义 the **Audit Model** for Opstage（运维舞台）.

Audit is the traceability mechanism that records important governance operations performed by users, Agents, and the system.

The current implementation focus is **Opstage（运维舞台） CE（社区版）**. EE（企业版） and Cloud（云版） audit capabilities are future planning tracks and must not expand the CE（社区版） v0.1 implementation scope.

---

## 1. Purpose

The purpose of the Audit Model is to answer:

- who performed an operation;
- what operation was performed;
- which resource was affected;
- when the operation happened;
- whether the operation succeeded, failed, or was denied;
- what sanitized request and result details are available;
- how operational traceability is preserved without storing raw secrets.

Audit is not a general logging system.

Audit is not a metrics system.

Audit is not a full compliance suite in CE（社区版） v0.1.

---

## 2. Core Principle

The core audit principle is:

> Important governance operations must produce structured, sanitized, queryable AuditEvents.

AuditEvents should make the system explainable over time.

They should help operators answer:

```text
Who did what, on which resource, when, and with what result?
```

---

## 3. CE（社区版） Scope

CE（社区版） v0.1 should implement a basic but useful audit model.

Required CE（社区版） audit capabilities:

- create AuditEvents for important user actions;
- create AuditEvents for important Agent（代理） lifecycle actions;
- create AuditEvents for action requests and results;
- store AuditEvents in SQLite;
- expose AuditEvents through Admin API;
- show AuditEvents in UI;
- sanitize sensitive fields;
- avoid storing raw tokens or secrets;
- support basic filtering by time, actor, action, resource, and result if practical.

---

## 4. CE（社区版） Non-Goals

CE（社区版） v0.1 should not implement:

- immutable audit storage;
- signed audit records;
- audit hash chain;
- SIEM integration;
- audit export workflow;
- advanced audit search engine;
- audit retention policy engine;
- legal hold;
- compliance reports;
- support access audit workflow;
- organization-level audit;
- tenant-level audit;
- audit streaming;
- audit billing or metering.

These may be future EE（企业版） or Cloud（云版） capabilities.

---

## 5. AuditEvent

AuditEvent is the durable audit record. CE（社区版） v0.1 fields match Prisma `AuditEvent` and OpenAPI `AuditEvent`.

```text
id            aud_xxx
workspaceId   wks_xxx (default in CE v0.1, not exposed in API)
actorType     USER | AGENT | SYSTEM
actorId       string nullable
action        string
targetType    string nullable          (formerly `resourceType`)
targetId      string nullable          (formerly `resourceId`)
result        SUCCESS | FAILURE
message       string nullable          (formerly `description`)
metadataJson  TEXT (JSON serialized) nullable
createdAt     datetime
```

CE（社区版） v0.1 does NOT persist `actorDisplay`, `resourceDisplay`, `requestJson`, or `resultJson` — sanitized request/result fragments must be folded into `metadata`.

---

## 6. Actor Model

Actor identifies who or what performed the operation.

Recommended actor types:

```text
USER
AGENT
SYSTEM
```

### 6.1 USER

A human user operating through Opstage（运维舞台） UI or Admin API.

Examples:

```text
local admin
future EE user
future Cloud user
```

### 6.2 AGENT

An Agent（代理） operating through Agent（代理） API.

Examples:

```text
Agent registration
service report
CommandResult report
```

### 6.3 SYSTEM

The Backend or internal scheduler performing automatic operations.

Examples:

```text
Command expiration
status recalculation
retention cleanup in future EE
```

CE（社区版） v0.1 may use SYSTEM only for command expiration if implemented.

---

## 7. Actor Fields

CE（社区版） v0.1 actor fields:

```text
actorType   (USER | AGENT | SYSTEM)
actorId
```

Examples:

```json
{
  "actorType": "USER",
  "actorId": "usr_admin"
}
```

```json
{
  "actorType": "AGENT",
  "actorId": "agt_001"
}
```

Rules:

- `actorId` should be stable;
- if a readable display name is needed, store it in `metadata.actorName`;
- deleted users or Agents must not break existing audit records;
- `actorId` MAY be null only for `SYSTEM` events.

---

## 8. Target Model

Target identifies what was affected. The contract field names are `targetType` and `targetId` (not `resourceType` / `resourceId`).

Recommended `targetType` values (PascalCase string, free-form for forward-compat):

```text
Workspace
User
RegistrationToken
Agent
AgentToken
CapsuleService
ActionDefinition
Command
CommandResult
ConfigItem
HealthReport
SystemSetting
```

CE（社区版） should implement only target types it actually uses.

---

## 9. Target Fields

CE（社区版） v0.1 target fields:

```text
targetType
targetId
```

Examples:

```json
{
  "targetType": "CapsuleService",
  "targetId": "svc_001"
}
```

```json
{
  "targetType": "Command",
  "targetId": "cmd_001"
}
```

Rules:

- `targetId` should be stable;
- if a readable display name is needed, store it in `metadata.targetCode` or `metadata.targetName`;
- display fields must not contain secrets;
- deleted targets must not break existing audit records.

---

## 10. Action Naming

Audit action is the stable operation name.

Recommended naming style:

```text
<domain>.<operation>
```

Examples:

```text
auth.login.success
auth.login.failed
registrationToken.created
agent.registered
agent.heartbeat.rejected
capsuleService.reported
action.requested
command.created
command.dispatched
command.succeeded
command.failed
command.expired
system.setting.updated
```

Rules:

- use stable English identifiers;
- do not localize action codes;
- do not include resource IDs in action name;
- do not include user input in action name;
- prefer specific names over generic names.

---

## 11. Result Model

Audit result identifies operation outcome.

CE（社区版） v0.1 allowed values (must match OpenAPI `AuditResult`):

```text
SUCCESS
FAILURE
```

Map authorization rejections, validation failures, and unexpected runtime errors to `FAILURE` with `metadata.errorCode` (e.g. `FORBIDDEN`, `VALIDATION_FAILED`, `INTERNAL_ERROR`).

Reserved future values (not in CE（社区版） v0.1):

```text
PARTIAL
SKIPPED
DENIED
ERROR
PENDING
```

---

## 12. Message

`message` is a human-readable summary (formerly called `description`).

Examples:

```text
User admin requested action echo on demo-capsule-service.
Agent local-dev-agent reported command result successfully.
Registration token was created.
```

Rules:

- keep `message` concise;
- do not put raw secrets in `message`;
- do not rely on `message` for structured filtering;
- structured fields should carry actor, action, target, and result.

---

## 13. Metadata

CE（社区版） v0.1 stores all sanitized request, result, and contextual data inside a single `metadata` object (persisted as `metadataJson` TEXT column).

Recommended sub-keys (free-form, not validated by Backend):

```text
request    sanitized request fragment
result     sanitized result fragment
errorCode  short code if result is FAILURE
ip         client IP if available
userAgent  HTTP UA if available
source     "ui" | "admin-api" | "agent-api" | "system"
```

Example:

```json
{
  "request": {
    "actionName": "echo",
    "payload": { "message": "hello" }
  },
  "result": {
    "commandId": "cmd_001",
    "status": "SUCCEEDED"
  },
  "ip": "127.0.0.1",
  "userAgent": "browser",
  "source": "ui"
}
```

CE（社区版） may keep metadata minimal. The whole `metadata` blob is sanitized before storage (see §14).

---

## 14. Sensitive Data Sanitization

AuditEvents must not contain raw secrets.

Sensitive keys include:

```text
password
token
accessToken
refreshToken
cookie
apiKey
privateKey
credential
secret
authorization
registrationToken
agentToken
```

Recommended replacement:

```text
***REDACTED***
```

Sanitization should apply recursively to JSON objects where practical.

---

## 15. Audit Events to Create in CE（社区版）

CE（社区版） should create AuditEvents for these categories.

### 15.1 认证

Recommended events:

```text
auth.login.success
auth.login.failed
auth.logout.success
```

If failed login audit is implemented, avoid leaking whether username or password was incorrect.

### 15.2 Registration Token

Recommended events:

```text
registrationToken.created
registrationToken.used
registrationToken.revoked
registrationToken.expired
```

CE（社区版） v0.1 may implement created and used first.

### 15.3 Agent（代理） Lifecycle

Recommended events:

```text
agent.registered
agent.disabled
agent.enabled
agent.revoked
agent.token.invalid
```

CE（社区版） v0.1 may implement registered and token invalid/rejected if practical.

### 15.4 Service Report

Recommended events:

```text
capsuleService.reported
capsuleService.manifest.changed
capsuleService.removed
```

CE（社区版） should avoid creating noisy audit events for every identical report.

### 15.5 Action and Command

Recommended events:

```text
action.requested
command.created
command.completed     (matches CommandStatus.SUCCEEDED)
command.failed
command.expired
```

Minimum CE（社区版） events:

- `action.requested`;
- `command.completed`;
- `command.failed`.

### 15.6 System Settings

Recommended events:

```text
system.setting.updated
```

Only needed if CE（社区版） allows editing settings.

---

## 16. Events That Should Not Be Too Noisy

Do not create AuditEvent for every high-frequency operational signal.

Usually avoid auditing every:

- heartbeat;
- command poll;
- dashboard refresh;
- list query;
- health read;
- unchanged service report.

These belong to operational state or logs, not audit.

Audit should record meaningful governance operations.

---

## 17. Audit vs Logs

Audit and logs are different.

### 17.1 Audit

Audit answers:

```text
Who did what, to which resource, and with what result?
```

Audit is structured and user-visible.

### 17.2 Logs

Logs answer:

```text
What happened inside the application while processing?
```

Logs are operational and developer-facing.

### 17.3 Rule

Do not use AuditEvent as a general log store.

Do not put stack traces or large logs into AuditEvent.

---

## 18. Audit vs Metrics

Audit and metrics are different.

Metrics answer:

```text
How many, how often, how fast, how healthy?
```

Audit answers:

```text
Who, what, when, resource, result?
```

Do not use AuditEvent as a metrics time-series table.

Future EE（企业版） may derive metrics from audit data, but AuditEvent itself should remain an event record.

---

## 19. Audit API

Admin API should expose AuditEvents to UI.

Recommended endpoint:

```http
GET /api/admin/audit-events
```

CE（社区版） v0.1 filters (matches OpenAPI):

```text
actorType    USER | AGENT | SYSTEM
actorId
action
targetType
targetId
result       SUCCESS | FAILURE
from         ISO-8601
to           ISO-8601
page
pageSize
```

---

## 20. Audit UI

Audit UI should provide a readable event list.

Recommended columns:

```text
Time
Actor Type
Actor
Action
Target Type
Target
Result
Message
```

Audit detail should show:

```text
metadata (sanitized JSON)
```

Sensitive values must remain masked.

---

## 21. Audit Storage

CE（社区版） should store AuditEvents in SQLite.

Recommended storage rules:

- use structured columns for actor/action/target/result/time;
- store `metadataJson` as a single JSON text column;
- index `createdAt` if practical;
- index `action`/`result` if practical;
- keep schema portable for future PostgreSQL/MySQL.

CE（社区版） v0.1 does not need retention policy engine.

---

## 22. Audit Retention

CE（社区版） v0.1 may keep audit records indefinitely or provide simple manual cleanup later.

Future EE（企业版）/Cloud（云版） may add:

- retention policy;
- archive policy;
- export before deletion;
- immutable retention;
- legal hold;
- compliance retention.

Do not implement complex retention in CE（社区版） v0.1 unless necessary.

---

## 23. Audit Failure Handling

Backend should define what happens if AuditEvent creation fails.

CE（社区版） v0.1 may use a simple policy:

```text
If audit write fails, log error and continue for low-risk operations.
```

For security-critical operations, future EE（企业版） may use:

```text
fail closed if audit cannot be written
```

CE（社区版） does not need advanced audit failure policy, but errors should not be silently ignored in logs.

---

## 24. Audit and Commands

Command operations should be auditable.

Recommended mapping:

```text
User requests action          -> action.requested
Backend creates Command       -> command.created
Agent polls Command (RUNNING) -> (no audit by default; high-frequency)
Agent reports SUCCEEDED       -> command.completed
Agent reports FAILED          -> command.failed
Backend expires Command       -> command.expired
```

CE（社区版） may combine `command.created` with `action.requested` if necessary, but separate events are clearer.

---

## 25. Audit and Agent（代理） APIs

Agent（代理） API operations should create audit only for meaningful changes.

Recommended audit:

- Agent（代理） registered;
- registration token used;
- service first reported;
- manifest changed;
- CommandResult success/failure;
- invalid/revoked Agent（代理） token attempt if useful.

Avoid auditing every heartbeat and every command poll.

---

## 26. Audit and 安全

Audit model 支持 security but is not a replacement for authorization.

Rules:

- Backend must enforce authorization before action;
- denied operations create `FAILURE` AuditEvents with `metadata.errorCode = "FORBIDDEN"`;
- audit payloads must be sanitized;
- audit access should require admin authentication;
- future EE（企业版） may restrict audit visibility by role.

CE（社区版） may expose audit to local admin only.

---

## 27. Future EE（企业版） Extensions

Future EE（企业版） may add:

- audit export;
- audit retention policy;
- audit search;
- immutable audit storage;
- signed audit records;
- SIEM integration;
- support access audit;
- approval workflow audit;
- RBAC change audit;
- secret access audit;
- compliance reports.

These are not CE（社区版） v0.1 requirements.

---

## 28. Future Cloud（云版） Extensions

Future Cloud（云版） may add:

- organization-level audit;
- tenant-level audit;
- workspace audit views;
- audit retention by plan;
- audit export by plan;
- audit usage metering;
- Cloud（云版） support access audit;
- billing audit events;
- data export/deletion audit;
- multi-tenant audit isolation.

These are not CE（社区版） v0.1 requirements.

---

## 29. Anti-Patterns

Avoid these patterns.

### 29.1 Audit as application log

Do not store stack traces or high-volume logs in AuditEvent.

### 29.2 Audit with raw secrets

AuditEvents must not contain raw passwords, tokens, cookies, or credentials.

### 29.3 Noisy heartbeat audit

Heartbeat is operational state, not audit history.

### 29.4 UI-only audit

AuditEvents must be created by Backend, not trusted from UI.

### 29.5 Missing actor/target structure

Do not store only free-text audit messages.

### 29.6 Compliance claims too early

CE（社区版） audit is basic traceability, not a full compliance system.

---

## 30. Acceptance Criteria

The CE（社区版） Audit Model is acceptable when:

- Backend can create AuditEvents;
- AuditEvent has actor, action, target, result, and timestamp;
- action requests create audit records;
- command success/failure creates audit records;
- Agent（代理） registration creates audit record;
- registration token creation/use creates audit record if implemented;
- AuditEvents are visible in UI;
- AuditEvents are queryable through Admin API;
- sensitive values are redacted from `metadata`;
- heartbeat does not flood AuditEvents;
- raw tokens and secrets are not stored in audit;
- AuditEvent is not used as a general log store;
- `result` is one of `SUCCESS` or `FAILURE` (no extra values in CE（社区版） v0.1).

---

## 31. Summary

The Audit Model 提供 structured traceability for Opstage（运维舞台） governance operations.

It should be simple enough for CE（社区版）, but structured enough to support future EE（企业版） and Cloud（云版） audit capabilities.

The most important Audit rule is:

> Audit should record meaningful governance operations with structured actor, action, target, result, and sanitized metadata — not become a noisy log or secret store.
