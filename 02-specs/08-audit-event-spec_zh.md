<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 08-audit-event-spec.md
翻译状态 / Translation Status: 已翻译 / Translated
生成时间 / Generated: 2026-05-01 09:28:53
================================================================================
注意 / Notes:
- 技术术语如 Capsule Service、Agent、Opstage 等保留英文或采用中英对照
- 代码块中的内容不翻译
- 文件路径和 URL 不翻译
- 保持原有的 Markdown 格式结构
================================================================================
-->

# Audit Event 规范

- Status: 规范
- Edition: 共享
- Priority: 高
- Audience: backend developers, frontend developers, agent SDK developers, security reviewers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/` (OpenAPI / Prisma) disagree, the ADRs and contracts win for CE（社区版） v0.1.

This document 定义 the **Audit Event** specification for the `xtrape-capsule` domain.

An Audit Event records an important operation, state change, security-relevant action, or governance activity in Opstage（运维舞台）.

Audit Events are required for making Capsule Service（胶囊服务） governance traceable and accountable.

---

## 1. Purpose

The Audit Event 规范 定义:

- what should be audited;
- how audit events are structured;
- how audit action names should be formed;
- which actors can create audit events;
- which resources can be audited;
- how request and result data should be stored;
- how sensitive data should be handled;
- what CE（社区版） v0.1 must implement;
- what EE（企业版） and Cloud（云版） may extend later.

CE（社区版） v0.1 should implement a lightweight audit log, not a full compliance platform.

---

## 2. Core Rule

Every important governance operation should create an Audit Event.

At minimum, CE（社区版） v0.1 should audit:

- user login;
- Agent（代理） registration;
- Capsule Service（胶囊服务） report;
- Command creation;
- Command completion or failure;
- Action request;
- Action completion or failure.

Audit Events should answer:

```text
Who did what, to which resource, when, with what result?
```

---

## 3. Audit Event Object

### 3.1 CE（社区版） v0.1 AuditEvent (must match OpenAPI `AuditEvent`)

```json
{
  "id": "aud_001",
  "actorType": "USER",
  "actorId": "usr_001",
  "action": "command.created",
  "targetType": "Command",
  "targetId": "cmd_001",
  "result": "SUCCESS",
  "message": "User created command runHealthCheck for demo-capsule-service.",
  "metadata": {
    "actionName": "runHealthCheck",
    "payload": {}
  },
  "createdAt": "2026-04-30T10:22:00Z"
}
```

### 3.2 Persisted columns (matches Prisma `AuditEvent`)

```text
id              aud_xxx
workspaceId     wks_xxx (default in CE v0.1, not exposed in API)
actorType       USER | AGENT | SYSTEM
actorId         string nullable
action          string
targetType      string nullable
targetId        string nullable
result          SUCCESS | FAILURE
message         string nullable
metadataJson    JSON text nullable    (serialized from `metadata`)
createdAt       datetime
```

CE（社区版） v0.1 does NOT persist `actorName`, `targetCode`, `ip`, or `userAgent`. Future EE（企业版）/Cloud（云版） editions may add them.

---

## 4. Audit Event Fields

### 4.1 `id`

Unique Audit Event identifier. Required. Prefix: `aud_`.

### 4.2 `actorType`

Type of actor that caused the event. Required.

CE（社区版） v0.1 allowed values (uppercase, must match OpenAPI `AuditActorType`):

```text
USER
AGENT
SYSTEM
```

### 4.3 `actorId`

Identifier of the actor. Required when available; null for purely system-generated events.

Examples: `usr_001`, `agt_001`. Null for events emitted by background sweeps.

### 4.4 `action`

Stable audit action name. Required. Use dot-separated lower-case naming.

Examples:

```text
user.login
agent.registered
agent.service.reported
service.action.requested
command.created
command.completed
command.failed
```

### 4.5 `targetType`

Type of resource affected by the event. String, nullable.

Recommended values:

```text
User
Agent
RegistrationToken
AgentToken
CapsuleService
Command
ConfigItem
ActionDefinition
AuditEvent
System
```

### 4.6 `targetId`

Identifier of the affected resource. Optional. For system-wide events, may be null.

### 4.7 `result`

Operation result summary. Required.

CE（社区版） v0.1 allowed values (must match OpenAPI `AuditResult`):

```text
SUCCESS
FAILURE
```

Map authorization rejections, validation failures, and unexpected errors to `FAILURE` with descriptive `message` and `metadata.errorCode`.

### 4.8 `message`

Human-readable summary. Recommended for UI display. Nullable.

### 4.9 `metadata`

Optional free-form structured payload. Sanitized before storage.

Examples:

```json
{
  "actionName": "runHealthCheck",
  "payload": {},
  "errorCode": "ACTION_NOT_FOUND"
}
```

### 4.10 `createdAt`

Timestamp when the event was created. Required.

---

## 5. Actor Types

### 5.1 `USER`

A human operator using Opstage（运维舞台） UI or Admin API.

Examples:

- login;
- create command;
- request action;
- disable Agent（代理）;
- revoke token.

### 5.2 `AGENT`

A registered Opstage（运维舞台） Agent（代理）.

Examples:

- register itself;
- report heartbeat;
- report Capsule Service（胶囊服务） manifest;
- report CommandResult.

### 5.3 `SYSTEM`

The Opstage（运维舞台） Backend or its background scheduler.

Examples:

- mark Agent（代理） offline;
- expire Command;
- create default Workspace;
- clean old records.

---

## 6. Action Naming Rules

Audit action names should be:

- lower-case;
- dot-separated;
- stable;
- explicit;
- event-like, not UI-label-like.

Recommended pattern:

```text
<domain>.<event>
<domain>.<resource>.<event>
```

Examples:

```text
user.login
agent.registered
agent.revoked
agent.service.reported
service.action.requested
service.action.completed
command.created
command.failed
config.reported
system.command.expired
```

Avoid vague action names:

```text
do
update
click
operation
process
```

---

## 7. Recommended Audit Actions

### 7.1 User Events

```text
user.login
user.logout
user.login.failed
```

CE（社区版） v0.1 should implement at least:

```text
user.login
user.login.failed
```

### 7.2 Agent（代理） Events

```text
agent.registrationToken.created
agent.registered
agent.heartbeat.received
agent.disabled
agent.enabled
agent.revoked
```

CE（社区版） v0.1 should implement at least:

```text
agent.registered
```

### 7.3 Capsule Service（胶囊服务） Events

```text
agent.service.reported
service.status.changed
service.health.reported
service.action.requested
service.action.completed
service.action.failed
```

CE（社区版） v0.1 should implement at least:

```text
agent.service.reported
service.action.requested
service.action.completed
service.action.failed
```

### 7.4 Command Events

```text
command.created
command.dispatched
command.completed
command.failed
command.expired
command.cancelled
```

CE（社区版） v0.1 should implement at least:

```text
command.created
command.completed
command.failed
```

### 7.5 Config Events

```text
config.reported
config.change.requested
config.change.applied
config.change.failed
config.rollback.completed
```

CE（社区版） v0.1 does not need config change events because config editing is not required.

### 7.6 安全 Events

```text
agent.token.revoked
agent.token.invalidUsed
permission.denied
secret.access.denied
```

CE（社区版） v0.1 may implement only basic denied or invalid token logging if easy.

---

## 8. Audit Triggers

### 8.1 User login

Trigger when a user successfully logs in.

Action:

```text
user.login
```

### 8.2 Failed login

Trigger when a login attempt fails.

Action:

```text
user.login.failed
```

Do not store raw password or password hash in audit event.

### 8.3 Agent（代理） registration

Trigger when an Agent（代理） successfully registers.

Action:

```text
agent.registered
```

### 8.4 Service report

Trigger when an Agent（代理） reports a new Capsule Service（胶囊服务） or material service metadata changes.

Action:

```text
agent.service.reported
```

CE（社区版） v0.1 does not need to create an audit event for every heartbeat.

### 8.5 Action request

Trigger when a user requests a service action.

Action:

```text
service.action.requested
```

### 8.6 Command creation

Trigger when Backend creates a Command.

Action:

```text
command.created
```

### 8.7 Command result

Trigger when Agent（代理） reports final CommandResult.

Actions:

```text
command.completed
command.failed
```

### 8.8 Command expiration

Trigger when Backend marks a Command as expired.

Action:

```text
command.expired
```

CE（社区版） v0.1 may implement this if expiration handling is implemented.

---

## 9. Request and Result Sanitization

Audit Events must not store raw secrets.

### 9.1 Sensitive fields

Sensitive fields include:

```text
password
token
accessToken
refreshToken
cookie
secret
credential
privateKey
apiKey
authorization
```

### 9.2 Sanitization behavior

If request or result 包含 sensitive fields, they should be:

- removed;
- masked;
- replaced with `secretRef`;
- summarized without raw values.

Recommended mask:

```text
***REDACTED***
```

Bad:

```json
{
  "password": "plain-text-password"
}
```

Good:

```json
{
  "password": "***REDACTED***"
}
```

Better:

```json
{
  "secretRef": "agent-local://agent-001/secrets/chatgpt/account-001"
}
```

### 9.3 CE（社区版） v0.1 requirement

CE（社区版） v0.1 should at least avoid intentionally writing raw tokens, passwords, cookies, or credentials to audit events.

---

## 10. Backend Storage

CE（社区版） v0.1 audit table columns (matches Prisma `AuditEvent`):

```text
id            aud_xxx
workspaceId   wks_xxx
actorType     USER | AGENT | SYSTEM
actorId       string nullable
action        string
targetType    string nullable
targetId      string nullable
result        SUCCESS | FAILURE
message       string nullable
metadataJson  TEXT (JSON serialized) nullable
createdAt     datetime
```

CE（社区版） v0.1 uses SQLite JSON/TEXT for `metadataJson`.

Recommended indexes:

```text
(createdAt)
(action)
(workspaceId, createdAt)
(actorType, actorId)
(targetType, targetId)
```

CE（社区版） v0.1 may implement only basic indexes.

---

## 11. UI Requirements

CE（社区版） v0.1 UI should provide an Audit Logs page or audit section.

Minimum list fields:

```text
Time
Actor
Action
Resource
Result
Description
```

Optional filters:

```text
Action
Actor
Target Type
Result
Time Range
```

CE（社区版） v0.1 may keep filters simple.

Service detail page may show recent audit events related to that service.

Command detail page may show related audit events.

---

## 12. Backend Requirements

CE（社区版） v0.1 Backend should:

1. provide an AuditEvent storage model;
2. write audit events for required triggers;
3. sanitize the `metadata` payload before storage;
4. expose audit list API for UI;
5. expose target-specific audit query if practical;
6. avoid storing raw secrets;
7. keep audit writes non-blocking where possible, but do not silently ignore critical audit failures without logging.

---

## 13. Agent（代理） SDK Requirements

CE（社区版） v0.1 Agent（代理） SDK usually does not write audit events directly to the database.

Instead, Agent（代理） operations trigger audit events when Backend receives:

- registration request;
- service report;
- command result.

Agent（代理） SDK should avoid sending raw secrets in payloads that may be audited.

---

## 14. Retention

CE（社区版） v0.1 may keep audit events indefinitely or provide simple cleanup later.

Future EE（企业版）/Cloud（云版） may support:

- retention policy;
- archive export;
- immutable audit storage;
- compliance reports;
- audit search;
- audit streaming;
- SIEM integration.

CE（社区版） v0.1 does not need advanced retention management.

---

## 15. Audit Result Values

CE（社区版） v0.1 allowed values (must match OpenAPI `AuditResult`):

```text
SUCCESS
FAILURE
```

`DENIED`, `ERROR`, and `PENDING` are reserved for future EE（企业版）/Cloud（云版） editions and are not part of CE（社区版） v0.1. Map authorization rejections, validation failures, and unexpected runtime errors to `FAILURE` with `metadata.errorCode`.

Examples:

- final command success → `SUCCESS`;
- command failure or expired command → `FAILURE`;
- permission denial → `FAILURE` with `metadata.errorCode = "FORBIDDEN"`.

---

## 16. Audit and Command Relationship

Commands and Audit Events are related but not identical.

Command records represent executable instructions.

Audit Events represent trace records.

Recommended mapping:

```text
User requests action
    ↓
AuditEvent: service.action.requested
    ↓
Command: created
    ↓
AuditEvent: command.created
    ↓
Agent reports result
    ↓
CommandResult: stored
    ↓
AuditEvent: command.completed or command.failed
    ↓
AuditEvent: service.action.completed or service.action.failed
```

CE（社区版） v0.1 may reduce duplicate audit events if needed, but should keep enough traceability.

Minimum acceptable CE（社区版） v0.1 mapping:

```text
command.created
command.completed / command.failed
```

---

## 17. Audit and Health Relationship

Health reports do not need to create audit events every time.

Otherwise audit logs become noisy.

Recommended behavior:

- do not audit every heartbeat;
- do not audit every health report;
- audit major status changes if implemented;
- audit service report when a service is first registered or metadata changes materially.

Future EE（企业版）/Cloud（云版） may add status-change audit policies.

---

## 18. Audit and Config Relationship

CE（社区版） v0.1 implements config visibility only.

Therefore, CE（社区版） v0.1 does not need config change audit.

Future config editing must audit:

- requested change;
- validation result;
- approval result;
- applied result;
- rollback.

---

## 19. 安全 Rules

### 19.1 Do not store raw secrets

Audit Events must not contain raw passwords, tokens, cookies, API keys, or private keys.

### 19.2 Do not store full sensitive payloads

Action payloads and command results should be sanitized before storing.

### 19.3 Store enough context

Sanitization should not remove all operational meaning.

Good audit event:

```json
{
  "action": "service.action.requested",
  "metadata": {
    "actionName": "refreshSession",
    "sessionId": "ses_001"
  }
}
```

Bad audit event:

```json
{
  "action": "service.action.requested",
  "metadata": {}
}
```

if it removes all useful traceability.

### 19.4 Audit denied operations

授权 failures should be audited where practical.

### 19.5 Avoid audit recursion

Do not create an audit event for every audit event read unless future compliance mode requires it.

---

## 20. Compatibility Rules

- New optional fields may be added to AuditEvent.
- Existing action names should remain stable.
- Unknown metadata fields should be ignored by older clients.
- CE（社区版） may implement basic audit only.
- EE（企业版）/Cloud（云版） may add immutable logs, export, compliance, retention, and SIEM integration without changing basic AuditEvent shape.

Stable fields:

```text
actorType
actorId
action
targetType
targetId
result
createdAt
```

---

## 21. CE（社区版） v0.1 Required Subset

CE（社区版） v0.1 must implement:

- AuditEvent storage;
- audit creation for user login and failed login;
- audit creation for Agent（代理） registration;
- audit creation for service report when service is first registered;
- audit creation for Command creation;
- audit creation for Command success/failure;
- audit creation for Action request/result if implemented separately;
- audit list UI;
- basic sanitization;
- no raw secret storage.

CE（社区版） v0.1 does not need to implement:

- immutable audit storage;
- audit export;
- compliance reports;
- SIEM integration;
- retention policy UI;
- audit approval workflow;
- audit signing;
- audit read tracking;
- advanced search engine.

---

## 22. Example CE（社区版） v0.1 Audit Flow

```text
User logs in
    ↓
AuditEvent: user.login

Agent registers
    ↓
AuditEvent: agent.registered

User requests runHealthCheck
    ↓
AuditEvent: service.action.requested
    ↓
Command created
    ↓
AuditEvent: command.created

Agent reports command success
    ↓
AuditEvent: command.completed
    ↓
AuditEvent: service.action.completed
```

CE（社区版） may simplify this flow but must preserve traceability.

---

## 23. Anti-Patterns

Avoid these patterns.

### 23.1 No audit for operations

Do not execute important operations without audit trace.

### 23.2 Raw secrets in audit

Do not store tokens, cookies, passwords, or credentials in audit events.

### 23.3 Auditing every heartbeat

Do not create noisy audit records for every heartbeat.

### 23.4 Audit event as log storage

Do not use AuditEvent as a general log system.

Large logs belong to future log collection capabilities.

### 23.5 Unstable action names

Do not rename audit action names casually after they are used.

### 23.6 Missing actor identity

Audit Events should include actor information whenever possible.

---

## 24. Summary

Audit Events make Capsule Service（胶囊服务） governance traceable.

CE（社区版） v0.1 should implement a lightweight but useful audit loop:

```text
User / Agent / System operation
    ↓
Backend creates AuditEvent
    ↓
UI displays Audit Logs
```

The audit model should remain simple in CE（社区版）, but its structure should be stable enough for future EE（企业版） and Cloud（云版） compliance extensions.
