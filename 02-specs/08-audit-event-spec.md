# Audit Event Specification

- Status: Specification
- Edition: Shared
- Priority: High
- Audience: backend developers, frontend developers, agent SDK developers, security reviewers, AI coding agents

This document defines the **Audit Event** specification for the `xtrape-capsule` domain.

An Audit Event records an important operation, state change, security-relevant action, or governance activity in Opstage.

Audit Events are required for making Capsule Service governance traceable and accountable.

---

## 1. Purpose

The Audit Event Specification defines:

- what should be audited;
- how audit events are structured;
- how audit action names should be formed;
- which actors can create audit events;
- which resources can be audited;
- how request and result data should be stored;
- how sensitive data should be handled;
- what CE v0.1 must implement;
- what EE and Cloud may extend later.

CE v0.1 should implement a lightweight audit log, not a full compliance platform.

---

## 2. Core Rule

Every important governance operation should create an Audit Event.

At minimum, CE v0.1 should audit:

- user login;
- Agent registration;
- Capsule Service report;
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

### 3.1 Minimum CE v0.1 AuditEvent

```json
{
  "id": "aud_001",
  "actorType": "user",
  "actorId": "usr_001",
  "action": "command.created",
  "resourceType": "Command",
  "resourceId": "cmd_001",
  "description": "User created command runHealthCheck for demo-capsule-service.",
  "result": "SUCCESS",
  "createdAt": "2026-04-30T10:22:00Z"
}
```

### 3.2 Recommended AuditEvent

```json
{
  "id": "aud_001",
  "workspaceId": "wks_default",
  "actorType": "user",
  "actorId": "usr_001",
  "actorName": "local-admin",
  "action": "service.action.requested",
  "resourceType": "CapsuleService",
  "resourceId": "svc_001",
  "resourceCode": "demo-capsule-service",
  "description": "User requested action runHealthCheck on demo-capsule-service.",
  "requestJson": {
    "actionName": "runHealthCheck",
    "payload": {}
  },
  "result": "SUCCESS",
  "resultJson": {
    "commandId": "cmd_001"
  },
  "ip": "127.0.0.1",
  "userAgent": "Mozilla/5.0",
  "createdAt": "2026-04-30T10:22:00Z",
  "metadata": {
    "source": "ui"
  }
}
```

---

## 4. Audit Event Fields

### 4.1 `id`

Unique Audit Event identifier.

Required.

Recommended prefix:

```text
aud_
```

### 4.2 `workspaceId`

Logical workspace boundary.

Recommended even in CE v0.1, where a default Workspace may be used.

### 4.3 `actorType`

Type of actor that caused the event.

Required.

Allowed values:

```text
user
agent
system
```

Future values may include:

```text
apiClient
scheduler
cloudSystem
```

### 4.4 `actorId`

Identifier of the actor.

Required when available.

Examples:

```text
usr_001
agt_001
system
```

### 4.5 `actorName`

Optional display name of the actor at the time of event creation.

This helps preserve readable audit history even if the user or Agent name changes later.

### 4.6 `action`

Stable audit action name.

Required.

Use dot-separated lower-case naming.

Examples:

```text
user.login
agent.registered
agent.heartbeat.received
agent.service.reported
service.action.requested
service.action.completed
command.created
command.completed
command.failed
```

### 4.7 `resourceType`

Type of resource affected by the event.

Recommended values:

```text
User
Agent
AgentToken
CapsuleService
Command
CommandResult
ConfigItem
AuditEvent
System
```

Future values may include:

```text
Workspace
Tenant
Organization
SecretRef
Capability
ResourceDefinition
AlertRule
```

### 4.8 `resourceId`

Identifier of the affected resource.

Optional for system-wide events.

### 4.9 `resourceCode`

Optional stable code of the resource.

Useful for Capsule Services and Agents.

Examples:

```text
demo-capsule-service
local-dev-agent
```

### 4.10 `description`

Human-readable description of the event.

Recommended for UI display.

### 4.11 `requestJson`

Optional structured request data.

Should be sanitized before storage.

Examples:

```json
{
  "actionName": "runHealthCheck",
  "payload": {}
}
```

### 4.12 `result`

Operation result summary.

Allowed values:

```text
SUCCESS
FAILED
DENIED
ERROR
PENDING
```

### 4.13 `resultJson`

Optional structured result data.

Should be sanitized before storage.

### 4.14 `ip`

Optional IP address of the user or client.

CE v0.1 may store it when available.

### 4.15 `userAgent`

Optional HTTP user-agent string for user-initiated operations.

### 4.16 `createdAt`

Timestamp when the event was created.

Required.

### 4.17 `metadata`

Optional free-form metadata.

Examples:

```json
{
  "source": "ui",
  "dangerLevel": "LOW"
}
```

---

## 5. Actor Types

### 5.1 `user`

A human operator using Opstage UI or Admin API.

Examples:

- login;
- create command;
- request action;
- disable Agent;
- revoke token.

### 5.2 `agent`

A registered Opstage Agent.

Examples:

- register itself;
- report heartbeat;
- report Capsule Service manifest;
- report CommandResult.

### 5.3 `system`

The Opstage Backend or system scheduler.

Examples:

- mark Agent offline;
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

CE v0.1 should implement at least:

```text
user.login
user.login.failed
```

### 7.2 Agent Events

```text
agent.registrationToken.created
agent.registered
agent.heartbeat.received
agent.disabled
agent.enabled
agent.revoked
```

CE v0.1 should implement at least:

```text
agent.registered
```

### 7.3 Capsule Service Events

```text
agent.service.reported
service.status.changed
service.health.reported
service.action.requested
service.action.completed
service.action.failed
```

CE v0.1 should implement at least:

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

CE v0.1 should implement at least:

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

CE v0.1 does not need config change events because config editing is not required.

### 7.6 Security Events

```text
agent.token.revoked
agent.token.invalidUsed
permission.denied
secret.access.denied
```

CE v0.1 may implement only basic denied or invalid token logging if easy.

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

### 8.3 Agent registration

Trigger when an Agent successfully registers.

Action:

```text
agent.registered
```

### 8.4 Service report

Trigger when an Agent reports a new Capsule Service or material service metadata changes.

Action:

```text
agent.service.reported
```

CE v0.1 does not need to create an audit event for every heartbeat.

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

Trigger when Agent reports final CommandResult.

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

CE v0.1 may implement this if expiration handling is implemented.

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

If request or result contains sensitive fields, they should be:

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

### 9.3 CE v0.1 requirement

CE v0.1 should at least avoid intentionally writing raw tokens, passwords, cookies, or credentials to audit events.

---

## 10. Backend Storage

Recommended audit table fields:

```text
id
workspaceId
actorType
actorId
actorName
action
resourceType
resourceId
resourceCode
description
requestJson
result
resultJson
ip
userAgent
metadataJson
createdAt
```

CE v0.1 may use SQLite JSON/text fields for request and result data.

Recommended indexes:

```text
createdAt
action
actorType + actorId
resourceType + resourceId
workspaceId + createdAt
```

CE v0.1 may implement only basic indexes.

---

## 11. UI Requirements

CE v0.1 UI should provide an Audit Logs page or audit section.

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
Resource Type
Result
Time Range
```

CE v0.1 may keep filters simple.

Service detail page may show recent audit events related to that service.

Command detail page may show related audit events.

---

## 12. Backend Requirements

CE v0.1 Backend should:

1. provide an AuditEvent storage model;
2. write audit events for required triggers;
3. sanitize request and result JSON;
4. expose audit list API for UI;
5. expose resource-specific audit query if practical;
6. avoid storing raw secrets;
7. keep audit writes non-blocking where possible, but do not silently ignore critical audit failures without logging.

---

## 13. Agent SDK Requirements

CE v0.1 Agent SDK usually does not write audit events directly to the database.

Instead, Agent operations trigger audit events when Backend receives:

- registration request;
- service report;
- command result.

Agent SDK should avoid sending raw secrets in payloads that may be audited.

---

## 14. Retention

CE v0.1 may keep audit events indefinitely or provide simple cleanup later.

Future EE/Cloud may support:

- retention policy;
- archive export;
- immutable audit storage;
- compliance reports;
- audit search;
- audit streaming;
- SIEM integration.

CE v0.1 does not need advanced retention management.

---

## 15. Audit Result Values

Allowed result values:

```text
SUCCESS
FAILED
DENIED
ERROR
PENDING
```

Recommended meaning:

| Result | Meaning |
|---|---|
| SUCCESS | Operation completed successfully |
| FAILED | Operation attempted but failed in normal business or runtime flow |
| DENIED | Operation was rejected by authorization or policy |
| ERROR | Unexpected system error occurred |
| PENDING | Operation was accepted but not completed yet |

Examples:

- action request creates `PENDING` or `SUCCESS` depending on whether the event is for request acceptance;
- final command result creates `SUCCESS` or `FAILED`;
- permission failure creates `DENIED`.

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

CE v0.1 may reduce duplicate audit events if needed, but should keep enough traceability.

Minimum acceptable CE v0.1 mapping:

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

Future EE/Cloud may add status-change audit policies.

---

## 18. Audit and Config Relationship

CE v0.1 implements config visibility only.

Therefore, CE v0.1 does not need config change audit.

Future config editing must audit:

- requested change;
- validation result;
- approval result;
- applied result;
- rollback.

---

## 19. Security Rules

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
  "requestJson": {
    "actionName": "refreshSession",
    "sessionId": "ses_001"
  }
}
```

Bad audit event:

```json
{
  "action": "service.action.requested",
  "requestJson": {}
}
```

if it removes all useful traceability.

### 19.4 Audit denied operations

Authorization failures should be audited where practical.

### 19.5 Avoid audit recursion

Do not create an audit event for every audit event read unless future compliance mode requires it.

---

## 20. Compatibility Rules

- New optional fields may be added to AuditEvent.
- Existing action names should remain stable.
- Unknown metadata fields should be ignored by older clients.
- CE may implement basic audit only.
- EE/Cloud may add immutable logs, export, compliance, retention, and SIEM integration without changing basic AuditEvent shape.

Stable fields:

```text
actorType
actorId
action
resourceType
resourceId
result
createdAt
```

---

## 21. CE v0.1 Required Subset

CE v0.1 must implement:

- AuditEvent storage;
- audit creation for user login and failed login;
- audit creation for Agent registration;
- audit creation for service report when service is first registered;
- audit creation for Command creation;
- audit creation for Command success/failure;
- audit creation for Action request/result if implemented separately;
- audit list UI;
- basic sanitization;
- no raw secret storage.

CE v0.1 does not need to implement:

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

## 22. Example CE v0.1 Audit Flow

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

CE may simplify this flow but must preserve traceability.

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

Audit Events make Capsule Service governance traceable.

CE v0.1 should implement a lightweight but useful audit loop:

```text
User / Agent / System operation
    ↓
Backend creates AuditEvent
    ↓
UI displays Audit Logs
```

The audit model should remain simple in CE, but its structure should be stable enough for future EE and Cloud compliance extensions.
