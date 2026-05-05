---
status: draft
audience: architects
stability: unstable
last_reviewed: 2026-05-05
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 05-agent-permission-model.md
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

# Agent（代理） Permission Model

- Status: 实施指南
- Edition: 共享
- Priority: 高
- Audience: backend developers, agent SDK developers, Capsule Service（胶囊服务） developers, architects, security reviewers, AI coding agents

This document 定义 the **Agent（代理） Permission Model** for the `xtrape-capsule` product family.

Agent（代理） permission is the security boundary that decides what an authenticated Agent（代理） is allowed to report, poll, execute, and update in Opstage（运维舞台）.

The current implementation focus is **CE（社区版）**. CE（社区版） v0.1 implements a simple but strict Agent（代理） permission model
for the Node.js Embedded Agent（代理）. EE（企业版） and Cloud（云版） may later add workspace-scoped policies, Agent（代理） groups,
capability scopes, token rotation, and richer permission controls.

---

## 1. Purpose

The purpose of the Agent（代理） Permission Model is to ensure that an Agent（代理） can only operate within its own authorized governance boundary.

The model should answer:

- Which Agent（代理） is making the request?
- Which Capsule Services can this Agent（代理） report?
- Which Commands can this Agent（代理） poll?
- Which CommandResults can this Agent（代理） submit?
- Which health/config/action metadata can this Agent（代理） update?
- What happens if an Agent（代理） tries to access another Agent（代理）'s resources?
- How are disabled, revoked, or stale Agents handled?
- What extension points should CE（社区版） reserve for EE（企业版） and Cloud（云版）?

The key rule is:

> An Agent（代理） can only act for itself and for Capsule Services that are explicitly owned or reported by that Agent（代理）.

---

## 2. Core Principle

Agent（代理） permission is based on authenticated Agent（代理） identity.

Backend must derive Agent（代理） identity from the Agent（代理） token, not from untrusted request payload fields.

Recommended principle:

```text
Agent token -> authenticated Agent identity -> allowed Agent-owned resources
```

The Agent（代理） should not be able to choose its identity by sending `agentId`, `workspaceId`, or `serviceId` in request body.

---

## 3. CE（社区版） Scope

CE（社区版） v0.1 should implement a minimal but safe Agent（代理） permission model.

Required CE（社区版） rules:

- Agent（代理） API calls require Agent（代理） token except registration;
- Backend stores only Agent（代理） token hash;
- Backend derives Agent（代理） identity from token;
- Agent（代理） can heartbeat only for itself;
- Agent（代理） can report services only under itself;
- Agent（代理） can update health/config/action metadata only for its own services;
- Agent（代理） can poll only Commands assigned to itself;
- Agent（代理） can report CommandResults only for Commands assigned to itself;
- disabled or revoked Agents are rejected;
- invalid tokens are rejected;
- request body `agentId` must not override authenticated Agent（代理） identity;
- raw Agent（代理） token must not be logged.

---

## 4. CE（社区版） Non-Goals

CE（社区版） v0.1 should not implement:

- Agent（代理） groups;
- Agent（代理）-level RBAC;
- workspace-scoped Agent（代理） policies beyond default Workspace;
- capability-based authorization;
- per-action Agent（代理） permissions;
- Agent（代理） token rotation workflow;
- mTLS Agent（代理） identity;
- device attestation;
- IP allowlists;
- sidecar/external Agent（代理） policy engine;
- Cloud（云版） Agent（代理） Gateway routing policy;
- multi-tenant Agent（代理） isolation.

These are future EE（企业版） or Cloud（云版） capabilities.

---

## 5. Actor Types

For CE（社区版） Agent（代理） permission, there are two main authenticated actor types:

```text
USER
AGENT
```

### 5.1 USER

A human admin user operates through Admin API and UI.

A USER can request an action. Backend creates a Command assigned to an Agent（代理）.

### 5.2 AGENT

An Agent（代理） operates through Agent（代理） API.

An AGENT can:

- register using a registration token;
- heartbeat as itself;
- report its own services;
- poll Commands assigned to itself;
- report CommandResults for its assigned Commands.

The Agent（代理） cannot act as a USER.

The Agent（代理） cannot call Admin APIs.

---

## 6. Agent（代理） 认证

Agent（代理） authentication uses Agent（代理） token.

Header:

```http
Authorization: Bearer <agentToken>
```

Backend should:

1. extract bearer token;
2. hash token using the configured token hash method;
3. look up active Agent（代理） token hash;
4. load Agent（代理） identity;
5. verify Agent（代理） status;
6. attach authenticated Agent（代理） identity to request context.

Backend must not store raw Agent（代理） token.

Backend must not log raw Agent（代理） token.

---

## 7. Agent（代理） Identity Context

After authentication, Backend should create an Agent（代理） identity context.

Recommended context fields:

```text
agentId
workspaceId
agentCode
agentStatus
agentMode
runtime
tokenId if modeled
```

All Agent（代理） API permission checks should use this context.

Do not trust these fields from request body when token identity is available.

---

## 8. Workspace Boundary

CE（社区版） v0.1 has one default Workspace.

Recommended default:

```text
workspaceId = wks_default
```

Even in CE（社区版）, records should include `workspaceId` where practical to keep future compatibility.

Agent（代理） permission checks should still ensure:

```text
resource.workspaceId == authenticatedAgent.workspaceId
```

This prepares the model for EE（企业版） and Cloud（云版） without implementing full multi-workspace management.

---

## 9. Agent（代理） 状态 and Permission

Agent（代理） status affects permission.

Recommended Agent（代理） statuses:

```text
ONLINE
OFFLINE
DISABLED
REVOKED
UNKNOWN
```

Permission rules:

||状态|Agent（代理） API Access||
|---|---|
||ONLINE|allowed||
||OFFLINE|allowed when request arrives, status may become ONLINE after heartbeat||
||UNKNOWN|allowed if token is valid, but status should be recalculated||
||DISABLED|denied||
||REVOKED|denied||

`DISABLED` and `REVOKED` are explicit administrative states.

`OFFLINE` is usually derived from heartbeat timeout and should not permanently block an Agent（代理） if a valid request arrives.

---

## 10. Registration Permission

Registration is the only Agent（代理）-related API that does not use Agent（代理） token.

Registration requires a valid registration token.

Rules:

- registration token must be valid;
- registration token must not be expired;
- registration token must not be revoked;
- registration token usage limits must be respected if implemented;
- registration token determines Workspace in CE（社区版） and future editions;
- registration request must not choose arbitrary Workspace;
- Backend issues Agent（代理） token after successful registration;
- registration event should be audited.

Registration token must be stored as hash.

Raw registration token must be shown only once when created.

---

## 11. Heartbeat Permission

Agent（代理） heartbeat updates the authenticated Agent（代理）'s runtime state.

Endpoint example:

```http
POST /api/agents/{agentId}/heartbeat
Authorization: Bearer <agentToken>
```

Permission rules:

- token must authenticate an Agent（代理）;
- path `agentId` must match authenticated Agent（代理） identity, or path `agentId` should be ignored in favor of token identity;
- disabled/revoked Agents are denied;
- heartbeat may update only the authenticated Agent（代理）;
- heartbeat must not update another Agent（代理）;
- heartbeat payload must not contain raw secrets.

Recommended safer API design:

```http
POST /api/agents/me/heartbeat
```

This avoids path identity mismatch.

---

## 12. Service Report Permission

Agent（代理） can report Capsule Services under its own Agent（代理） identity.

Endpoint example:

```http
POST /api/agents/{agentId}/services/report
Authorization: Bearer <agentToken>
```

Permission rules:

- token must authenticate an Agent（代理）;
- Agent（代理） status must allow API access;
- reported services are owned by authenticated Agent（代理） unless explicit transfer exists;
- payload `agentId` must not override authenticated Agent（代理） identity;
- service identity must be stable;
- Backend must prevent an Agent（代理） from overwriting another Agent（代理）'s service unexpectedly;
- service report must not include raw secrets.

For CE（社区版）, service ownership can be:

```text
CapsuleService.agentId = authenticatedAgent.agentId
```

---

## 13. Service Identity Collision

Service code collision can happen when two Agents report the same service code.

Possible CE（社区版） strategies:

### 13.1 Agent（代理）-scoped service identity

Uniqueness:

```text
workspaceId + agentId + serviceCode
```

Pros:

- simple;
- prevents cross-Agent（代理） overwrite;
- suitable for CE（社区版）.

Cons:

- same service moving between Agents creates a new service record.

### 13.2 Workspace-scoped service identity

Uniqueness:

```text
workspaceId + serviceCode
```

Pros:

- stable service identity across Agent（代理） migration.

Cons:

- requires transfer/claim policy;
- more complex permission checks.

Recommended CE（社区版） v0.1 strategy:

```text
workspaceId + agentId + serviceCode
```

Future EE（企业版） may introduce explicit service transfer or ownership claim workflow.

---

## 14. Health Report Permission

Agent（代理） can report health only for services it owns.

Permission rules:

- token authenticates Agent（代理）;
- service must belong to authenticated Agent（代理）;
- health report must not update another Agent（代理）'s service;
- health payload must not include raw secrets;
- invalid service reference should be rejected or treated as service report mismatch.

If health is included in service report or heartbeat, Backend must still associate it only with authenticated Agent（代理）-owned services.

---

## 15. Config Metadata Permission

Agent（代理） can report config metadata only for services it owns.

Rules:

- configs belong to authenticated Agent（代理）-owned service;
- sensitive values must be masked or represented as `secretRef`;
- raw secrets should be rejected or sanitized where practical;
- Agent（代理） cannot update config metadata for another Agent（代理）'s service;
- CE（社区版） 支持 visibility only, not config publishing.

Config editing and publishing are future EE（企业版） capabilities and require separate permission design.

---

## 16. ActionDefinition Permission

Agent（代理） can report ActionDefinitions only for services it owns.

Rules:

- action definitions belong to authenticated Agent（代理）-owned service;
- action names must be stable and unique per service;
- Agent（代理） cannot define actions for another Agent（代理）'s service;
- disabled actions must be respected by Backend and Agent（代理）;
- action metadata must not include raw secrets.

Backend should validate action definition shape before storing.

---

## 17. Command Polling Permission

Agent（代理） can poll only Commands assigned to itself.

Endpoint example:

```http
GET /api/agents/{agentId}/commands
Authorization: Bearer <agentToken>
```

Permission rules:

- token authenticates Agent（代理）;
- disabled/revoked Agents are denied;
- query returns only Commands where `command.agentId == authenticatedAgent.agentId`;
- command workspace must match Agent（代理） workspace;
- expired Commands should not be dispatched;
- Backend must not return Commands assigned to another Agent（代理）.

Recommended safer API design:

```http
GET /api/agents/me/commands
```

---

## 18. Command Dispatch Ownership

When Backend creates a Command from Admin API, it must assign it to the Agent（代理） that owns the target service.

Flow:

```text
User requests action on CapsuleService
    ↓
Backend loads CapsuleService
    ↓
Backend reads CapsuleService.agentId
    ↓
Backend creates Command assigned to that agentId
    ↓
Only that Agent can poll the Command
```

Backend must not let UI choose arbitrary `agentId` if the selected service has a different owner.

---

## 19. CommandResult Permission

Agent（代理） can report CommandResult only for Commands assigned to itself.

Endpoint example:

```http
POST /api/agents/{agentId}/commands/{commandId}/result
Authorization: Bearer <agentToken>
```

Permission rules:

- token authenticates Agent（代理）;
- command must exist;
- command.agentId must equal authenticated Agent（代理） ID;
- command.workspaceId must equal authenticated Agent（代理） workspace;
- command status must allow result reporting;
- duplicate final results should be handled safely;
- result payload must be sanitized;
- raw secrets must not be stored.

If an Agent（代理） reports a result for another Agent（代理）'s Command, Backend must return denied or not found.

Recommended behavior:

```text
Return 404 or 403 without leaking whether the command exists.
```

---

## 20. Agent（代理） API Resource Access Matrix

Recommended CE（社区版） matrix:

||Operation|Allowed Resource Scope||
|---|---|
||register|valid registration token scope||
||heartbeat|authenticated Agent（代理） only||
||report service|authenticated Agent（代理） only||
||report health|services owned by authenticated Agent（代理）||
||report configs|services owned by authenticated Agent（代理）||
||report actions|services owned by authenticated Agent（代理）||
||poll commands|Commands assigned to authenticated Agent（代理）||
||report command result|Commands assigned to authenticated Agent（代理）||
||read admin data|not allowed||
||create command|not allowed through Agent（代理） API||
||create registration token|not allowed through Agent（代理） API||

---

## 21. Agent（代理） Cannot Call Admin API

Agent（代理） token must not grant Admin API access.

Rules:

- Admin API requires user session or user token;
- Agent（代理） API requires Agent（代理） token;
- Agent（代理） token is rejected by Admin API;
- user token/session is rejected by Agent（代理） API unless explicitly allowed for internal testing, which should be avoided in production;
- API groups should have clear authentication guards.

This prevents Agent（代理） token from becoming a general control-plane credential.

---

## 22. Payload Trust Rules

Agent（代理） API payloads are untrusted even after authentication.

Backend must validate:

- schema;
- service ownership;
- workspace ownership;
- action names;
- config item shape;
- health status values;
- CommandResult target;
- sensitive fields;
- size limits if practical.

Never trust payload fields such as:

```text
agentId
workspaceId
serviceId
commandId ownership
actorType
actorId
```

without checking against authenticated context and database state.

---

## 23. Token Revocation

CE（社区版） may support basic Agent（代理） revocation if included in Backend scope.

Revocation means:

- Agent（代理） status becomes `REVOKED`;
- Agent（代理） token is rejected;
- Agent（代理） cannot heartbeat;
- Agent（代理） cannot poll Commands;
- Agent（代理） cannot report CommandResults;
- UI shows Agent（代理） as revoked;
- AuditEvent is created.

If CE（社区版） v0.1 does not include revoke UI, the model should still allow future token invalidation.

---

## 24. Agent（代理） Disable

Disable is a softer administrative state than revoke.

Disabled Agent（代理）:

- cannot use Agent（代理） API;
- may be re-enabled later;
- retains identity and history;
- should not receive Commands;
- should be visible in UI;
- should create AuditEvent when changed.

CE（社区版） v0.1 may defer disable/enable UI, but schema can reserve status.

---

## 25. Offline Agent（代理）

Offline is derived from heartbeat freshness.

Offline Agent（代理）:

- may become online again when it sends valid heartbeat;
- should not be treated the same as revoked;
- may still have pending Commands, but Backend should consider whether to create or dispatch Commands to stale/offline Agents;
- should make related Capsule Services appear stale or offline effectively.

Recommended CE（社区版） behavior:

- allow valid offline Agent（代理） to reconnect;
- avoid dispatching expired Commands;
- show service freshness clearly.

---

## 26. Audit Events

Agent（代理） permission-related operations should create AuditEvents where meaningful.

Recommended events:

```text
agent.registered
agent.heartbeat.rejected
agent.token.invalid
agent.disabled
agent.enabled
agent.revoked
capsuleService.reported
command.dispatched
command.result.accepted
command.result.denied
```

CE（社区版） should avoid auditing every heartbeat success because that would be too noisy.

Minimum CE（社区版） events:

- agent.registered;
- service first reported or changed;
- command result success/failure;
- denied command result if practical.

---

## 27. Error Handling

Permission errors should be clear but not leak sensitive information.

Recommended error codes:

```text
AGENT_TOKEN_MISSING
AGENT_TOKEN_INVALID
AGENT_DISABLED
AGENT_REVOKED
AGENT_ID_MISMATCH
AGENT_SERVICE_FORBIDDEN
COMMAND_NOT_FOUND
COMMAND_FORBIDDEN
COMMAND_RESULT_FORBIDDEN
REGISTRATION_TOKEN_INVALID
REGISTRATION_TOKEN_EXPIRED
```

For cross-Agent（代理） resource access, consider returning:

```text
404 Not Found
```

instead of:

```text
403 Forbidden
```

to avoid leaking resource existence.

---

## 28. Recommended API Shape

Identity-safe APIs can reduce mistakes.

Instead of:

```http
POST /api/agents/{agentId}/heartbeat
GET  /api/agents/{agentId}/commands
```

consider:

```http
POST /api/agents/me/heartbeat
GET  /api/agents/me/commands
```

Backend derives Agent（代理） identity from token.

If path-based `agentId` is used, Backend must validate it matches token identity.

---

## 29. Future EE（企业版） Direction

Future EE（企业版） may extend Agent（代理） permissions with:

- Agent（代理） groups;
- workspace-scoped Agent（代理） policies;
- Agent（代理） capability scopes;
- token rotation;
- Agent（代理） disable/re-enable workflow;
- per-Agent（代理） action policies;
- sidecar/external Agent（代理） target policies;
- IP allowlists;
- mTLS;
- device identity;
- approval workflow for sensitive Agent（代理） operations;
- service ownership transfer.

These are not CE（社区版） v0.1 requirements.

---

## 30. Future Cloud（云版） Direction

Future Cloud（云版） may extend Agent（代理） permissions with:

- tenant isolation;
- organization/workspace-scoped Agent（代理） tokens;
- Cloud（云版） Agent（代理） Gateway routing policy;
- Agent（代理） connection rate limiting;
- plan-based Agent（代理） limits;
- usage metering by Agent（代理）;
- Cloud（云版）-managed registration tokens;
- workspace-specific Agent（代理） enrollment;
- multi-tenant command isolation;
- hosted audit retention for Agent（代理） operations.

These are not CE（社区版） v0.1 requirements.

---

## 31. CE（社区版） Reservations

CE（社区版） should reserve these permission-compatible concepts:

```text
workspaceId
agentId
agentMode
runtime
Agent.status
Agent token hash
registration token hash
CapsuleService.agentId
Command.agentId
CommandResult.agentId
AuditEvent.actorType
AuditEvent.actorId
AuditEvent.resourceType
AuditEvent.resourceId
metadataJson
```

CE（社区版） should not implement full EE（企业版）/Cloud（云版） policy systems in v0.1.

---

## 32. Anti-Patterns

Avoid these patterns.

### 32.1 Trusting request body agentId

Agent（代理） identity must come from token authentication.

### 32.2 Agent（代理） can poll all Commands

Agent（代理） must only receive Commands assigned to itself.

### 32.3 Agent（代理） can report result for any Command

CommandResult must be ownership-checked.

### 32.4 Agent（代理） token grants Admin API access

Agent（代理） token is not a user credential.

### 32.5 Offline equals revoked

Offline is freshness-derived and recoverable; revoked is administrative and permanent unless explicitly restored.

### 32.6 Service code overwrite by another Agent（代理）

CE（社区版） should avoid cross-Agent（代理） service overwrite by using Agent（代理）-scoped identity or explicit transfer design.

### 32.7 日志 Agent（代理） token

Agent（代理） token must never be logged.

---

## 33. Acceptance Criteria

The CE（社区版） Agent（代理） Permission Model is acceptable when:

- Agent（代理） API authenticates using Agent（代理） token;
- Backend stores only token hash;
- Backend derives Agent（代理） identity from token;
- Agent（代理） heartbeat updates only authenticated Agent（代理）;
- Agent（代理） service report creates or updates services under authenticated Agent（代理）;
- Agent（代理） cannot overwrite another Agent（代理）'s service;
- Agent（代理） can poll only Commands assigned to itself;
- Agent（代理） cannot receive Commands assigned to another Agent（代理）;
- Agent（代理） can report CommandResult only for assigned Commands;
- Agent（代理） token cannot call Admin API;
- disabled/revoked Agents are rejected;
- offline Agents can reconnect if token is valid;
- raw tokens are not logged;
- permission failures return structured errors;
- audit events are created for meaningful Agent（代理） lifecycle and command-result events.

---

## 34. Summary

The Agent（代理） Permission Model keeps Opstage（运维舞台）'s runtime governance boundary safe.

It ensures that each Agent（代理） can only report its own services, poll its own Commands, and submit results for its own Commands.

The most important Agent（代理） permission rule is:

> Derive Agent（代理） authority from the authenticated token, then restrict every Agent（代理） API operation to resources owned by that Agent（代理） and its Workspace.
