# Audit Model

- Status: Implementation Guidance
- Edition: Shared
- Priority: High
- Audience: backend developers, frontend developers, agent SDK developers, architects, security reviewers, AI coding agents

This document defines the **Audit Model** for Opstage.

Audit is the traceability mechanism that records important governance operations performed by users, Agents, and the system.

The current implementation focus is **Opstage CE**. EE and Cloud audit capabilities are future planning tracks and must not expand the CE v0.1 implementation scope.

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

Audit is not a full compliance suite in CE v0.1.

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

## 3. CE Scope

CE v0.1 should implement a basic but useful audit model.

Required CE audit capabilities:

- create AuditEvents for important user actions;
- create AuditEvents for important Agent lifecycle actions;
- create AuditEvents for action requests and results;
- store AuditEvents in SQLite;
- expose AuditEvents through Admin API;
- show AuditEvents in UI;
- sanitize sensitive fields;
- avoid storing raw tokens or secrets;
- support basic filtering by time, actor, action, resource, and result if practical.

---

## 4. CE Non-Goals

CE v0.1 should not implement:

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

These may be future EE or Cloud capabilities.

---

## 5. AuditEvent

AuditEvent is the durable audit record.

Recommended fields:

```text
id
workspaceId
actorType
actorId
actorDisplay
action
resourceType
resourceId
resourceDisplay
result
description
requestJson
resultJson
metadataJson
createdAt
```

CE may implement a simplified version, but the model should preserve actor, action, resource, result, and timestamp.

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

A human user operating through Opstage UI or Admin API.

Examples:

```text
local admin
future EE user
future Cloud user
```

### 6.2 AGENT

An Agent operating through Agent API.

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

CE v0.1 may use SYSTEM only for command expiration if implemented.

---

## 7. Actor Fields

Recommended actor fields:

```text
actorType
actorId
actorDisplay
```

Examples:

```json
{
  "actorType": "USER",
  "actorId": "usr_admin",
  "actorDisplay": "admin"
}
```

```json
{
  "actorType": "AGENT",
  "actorId": "agt_001",
  "actorDisplay": "local-dev-agent"
}
```

Rules:

- actorId should be stable;
- actorDisplay is for readability;
- actorDisplay should not be the only identifier;
- deleted users or Agents should not break existing audit records.

---

## 8. Resource Model

Resource identifies what was affected.

Recommended resource types:

```text
WORKSPACE
USER
REGISTRATION_TOKEN
AGENT
CAPSULE_SERVICE
ACTION_DEFINITION
COMMAND
COMMAND_RESULT
CONFIG_ITEM
HEALTH_REPORT
SYSTEM_SETTING
```

Future editions may add:

```text
ORGANIZATION
TENANT
SUBSCRIPTION
ROLE
PERMISSION
ALERT_RULE
SECRET_PROVIDER
AUDIT_EXPORT
SUPPORT_SESSION
```

CE should implement only resource types it actually uses.

---

## 9. Resource Fields

Recommended resource fields:

```text
resourceType
resourceId
resourceDisplay
```

Examples:

```json
{
  "resourceType": "CAPSULE_SERVICE",
  "resourceId": "svc_001",
  "resourceDisplay": "demo-capsule-service"
}
```

```json
{
  "resourceType": "COMMAND",
  "resourceId": "cmd_001",
  "resourceDisplay": "echo"
}
```

Rules:

- resourceId should be stable;
- resourceDisplay is for readability;
- resourceDisplay should not contain secrets;
- deleted resources should not break existing audit records.

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

Recommended values:

```text
SUCCESS
FAILED
DENIED
```

Optional future values:

```text
PARTIAL
SKIPPED
EXPIRED
CANCELLED
```

CE v0.1 should implement at least:

```text
SUCCESS
FAILED
DENIED
```

---

## 12. Description

Description is a human-readable summary.

Examples:

```text
User admin requested action echo on demo-capsule-service.
Agent local-dev-agent reported command result successfully.
Registration token was created.
```

Rules:

- keep description concise;
- do not put raw secrets in description;
- do not rely on description for structured filtering;
- structured fields should carry actor, action, resource, and result.

---

## 13. Request and Result JSON

AuditEvent may include sanitized request and result details.

Recommended fields:

```text
requestJson
resultJson
metadataJson
```

### 13.1 requestJson

Sanitized request details.

Examples:

```json
{
  "actionName": "echo",
  "payload": {
    "message": "hello"
  }
}
```

### 13.2 resultJson

Sanitized result details.

Examples:

```json
{
  "commandStatus": "SUCCESS",
  "resultSummary": "Echo completed."
}
```

### 13.3 metadataJson

Additional metadata that does not belong to request or result.

Examples:

```json
{
  "ip": "127.0.0.1",
  "userAgent": "browser",
  "source": "admin-api"
}
```

CE may keep metadata minimal.

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

## 15. Audit Events to Create in CE

CE should create AuditEvents for these categories.

### 15.1 Authentication

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

CE v0.1 may implement created and used first.

### 15.3 Agent Lifecycle

Recommended events:

```text
agent.registered
agent.disabled
agent.enabled
agent.revoked
agent.token.invalid
```

CE v0.1 may implement registered and token invalid/rejected if practical.

### 15.4 Service Report

Recommended events:

```text
capsuleService.reported
capsuleService.manifest.changed
capsuleService.removed
```

CE should avoid creating noisy audit events for every identical report.

### 15.5 Action and Command

Recommended events:

```text
action.requested
command.created
command.dispatched
command.succeeded
command.failed
command.expired
```

Minimum CE events:

- action.requested;
- command.succeeded;
- command.failed.

### 15.6 System Settings

Recommended events:

```text
system.setting.updated
```

Only needed if CE allows editing settings.

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

Future EE may derive metrics from audit data, but AuditEvent itself should remain an event record.

---

## 19. Audit API

Admin API should expose AuditEvents to UI.

Recommended endpoint:

```http
GET /api/admin/audit-events
```

Recommended filters:

```text
actorType
actorId
action
resourceType
resourceId
result
startTime
endTime
limit
offset or cursor
```

CE v0.1 may implement simple pagination and a subset of filters.

---

## 20. Audit UI

Audit UI should provide a readable event list.

Recommended columns:

```text
Time
Actor Type
Actor
Action
Resource Type
Resource
Result
Description
```

Audit detail should show:

```text
requestJson
resultJson
metadataJson
```

Sensitive values must remain masked.

---

## 21. Audit Storage

CE should store AuditEvents in SQLite.

Recommended storage rules:

- use structured columns for actor/action/resource/result/time;
- store requestJson/resultJson/metadataJson as JSON text;
- index createdAt if practical;
- index action/result if practical;
- keep schema portable for future PostgreSQL/MySQL.

CE v0.1 does not need retention policy engine.

---

## 22. Audit Retention

CE v0.1 may keep audit records indefinitely or provide simple manual cleanup later.

Future EE/Cloud may add:

- retention policy;
- archive policy;
- export before deletion;
- immutable retention;
- legal hold;
- compliance retention.

Do not implement complex retention in CE v0.1 unless necessary.

---

## 23. Audit Failure Handling

Backend should define what happens if AuditEvent creation fails.

CE v0.1 may use a simple policy:

```text
If audit write fails, log error and continue for low-risk operations.
```

For security-critical operations, future EE may use:

```text
fail closed if audit cannot be written
```

CE does not need advanced audit failure policy, but errors should not be silently ignored in logs.

---

## 24. Audit and Commands

Command operations should be auditable.

Recommended mapping:

```text
User requests action         -> action.requested
Backend creates Command      -> command.created
Agent receives Command       -> command.dispatched
Agent reports SUCCESS        -> command.succeeded
Agent reports FAILED         -> command.failed
Backend expires Command      -> command.expired
```

CE may combine command.created with action.requested if necessary, but separate events are clearer.

---

## 25. Audit and Agent APIs

Agent API operations should create audit only for meaningful changes.

Recommended audit:

- Agent registered;
- registration token used;
- service first reported;
- manifest changed;
- CommandResult success/failure;
- invalid/revoked Agent token attempt if useful.

Avoid auditing every heartbeat and every command poll.

---

## 26. Audit and Security

Audit model supports security but is not a replacement for authorization.

Rules:

- Backend must enforce authorization before action;
- denied operations may create `DENIED` AuditEvents;
- audit payloads must be sanitized;
- audit access should require admin authentication;
- future EE may restrict audit visibility by role.

CE may expose audit to local admin only.

---

## 27. Future EE Extensions

Future EE may add:

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

These are not CE v0.1 requirements.

---

## 28. Future Cloud Extensions

Future Cloud may add:

- organization-level audit;
- tenant-level audit;
- workspace audit views;
- audit retention by plan;
- audit export by plan;
- audit usage metering;
- Cloud support access audit;
- billing audit events;
- data export/deletion audit;
- multi-tenant audit isolation.

These are not CE v0.1 requirements.

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

### 29.5 Missing actor/resource structure

Do not store only free-text audit messages.

### 29.6 Compliance claims too early

CE audit is basic traceability, not a full compliance system.

---

## 30. Acceptance Criteria

The CE Audit Model is acceptable when:

- Backend can create AuditEvents;
- AuditEvent has actor, action, resource, result, and timestamp;
- action requests create audit records;
- command success/failure creates audit records;
- Agent registration creates audit record;
- registration token creation/use creates audit record if implemented;
- AuditEvents are visible in UI;
- AuditEvents are queryable through Admin API;
- sensitive values are redacted;
- heartbeat does not flood AuditEvents;
- raw tokens and secrets are not stored in audit;
- AuditEvent is not used as a general log store.

---

## 31. Summary

The Audit Model provides structured traceability for Opstage governance operations.

It should be simple enough for CE, but structured enough to support future EE and Cloud audit capabilities.

The most important Audit rule is:

> Audit should record meaningful governance operations with structured actor, action, resource, result, and sanitized details — not become a noisy log or secret store.
