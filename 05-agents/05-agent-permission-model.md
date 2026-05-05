---
status: proposed
audience: architects
stability: evolving
last_reviewed: 2026-05-05
---

# Agent Permission Model

- Status: Implementation Guidance
- Edition: Shared
- Priority: High
- Audience: backend developers, agent SDK developers, Capsule Service developers, architects, security reviewers, AI coding agents

This document defines the **Agent Permission Model** for the `xtrape-capsule` product family.

Agent permission is the security boundary that decides what an authenticated Agent is allowed to report, poll, execute, and update in Opstage.

The current implementation focus is **CE**. CE v0.1 implements a simple but strict Agent permission model for the
Node.js Embedded Agent. EE and Cloud may later add workspace-scoped policies, Agent groups, capability scopes, token
rotation, and richer permission controls.

---

## 1. Purpose

The purpose of the Agent Permission Model is to ensure that an Agent can only operate within its own authorized governance boundary.

The model should answer:

- Which Agent is making the request?
- Which Capsule Services can this Agent report?
- Which Commands can this Agent poll?
- Which CommandResults can this Agent submit?
- Which health/config/action metadata can this Agent update?
- What happens if an Agent tries to access another Agent's resources?
- How are disabled, revoked, or stale Agents handled?
- What extension points should CE reserve for EE and Cloud?

The key rule is:

> An Agent can only act for itself and for Capsule Services that are explicitly owned or reported by that Agent.

---

## 2. Core Principle

Agent permission is based on authenticated Agent identity.

Backend must derive Agent identity from the Agent token, not from untrusted request payload fields.

Recommended principle:

```text
Agent token -> authenticated Agent identity -> allowed Agent-owned resources
```

The Agent should not be able to choose its identity by sending `agentId`, `workspaceId`, or `serviceId` in request body.

---

## 3. CE Scope

CE v0.1 should implement a minimal but safe Agent permission model.

Required CE rules:

- Agent API calls require Agent token except registration;
- Backend stores only Agent token hash;
- Backend derives Agent identity from token;
- Agent can heartbeat only for itself;
- Agent can report services only under itself;
- Agent can update health/config/action metadata only for its own services;
- Agent can poll only Commands assigned to itself;
- Agent can report CommandResults only for Commands assigned to itself;
- disabled or revoked Agents are rejected;
- invalid tokens are rejected;
- request body `agentId` must not override authenticated Agent identity;
- raw Agent token must not be logged.

---

## 4. CE Non-Goals

CE v0.1 should not implement:

- Agent groups;
- Agent-level RBAC;
- workspace-scoped Agent policies beyond default Workspace;
- capability-based authorization;
- per-action Agent permissions;
- Agent token rotation workflow;
- mTLS Agent identity;
- device attestation;
- IP allowlists;
- sidecar/external Agent policy engine;
- Cloud Agent Gateway routing policy;
- multi-tenant Agent isolation.

These are future EE or Cloud capabilities.

---

## 5. Actor Types

For CE Agent permission, there are two main authenticated actor types:

```text
USER
AGENT
```

### 5.1 USER

A human admin user operates through Admin API and UI.

A USER can request an action. Backend creates a Command assigned to an Agent.

### 5.2 AGENT

An Agent operates through Agent API.

An AGENT can:

- register using a registration token;
- heartbeat as itself;
- report its own services;
- poll Commands assigned to itself;
- report CommandResults for its assigned Commands.

The Agent cannot act as a USER.

The Agent cannot call Admin APIs.

---

## 6. Agent Authentication

Agent authentication uses Agent token.

Header:

```http
Authorization: Bearer <agentToken>
```

Backend should:

1. extract bearer token;
2. hash token using the configured token hash method;
3. look up active Agent token hash;
4. load Agent identity;
5. verify Agent status;
6. attach authenticated Agent identity to request context.

Backend must not store raw Agent token.

Backend must not log raw Agent token.

---

## 7. Agent Identity Context

After authentication, Backend should create an Agent identity context.

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

All Agent API permission checks should use this context.

Do not trust these fields from request body when token identity is available.

---

## 8. Workspace Boundary

CE v0.1 has one default Workspace.

Recommended default:

```text
workspaceId = wks_default
```

Even in CE, records should include `workspaceId` where practical to keep future compatibility.

Agent permission checks should still ensure:

```text
resource.workspaceId == authenticatedAgent.workspaceId
```

This prepares the model for EE and Cloud without implementing full multi-workspace management.

---

## 9. Agent Status and Permission

Agent status affects permission.

Recommended Agent statuses:

```text
ONLINE
OFFLINE
DISABLED
REVOKED
UNKNOWN
```

Permission rules:

| Status | Agent API Access |
|---|---|
| ONLINE | allowed |
| OFFLINE | allowed when request arrives, status may become ONLINE after heartbeat |
| UNKNOWN | allowed if token is valid, but status should be recalculated |
| DISABLED | denied |
| REVOKED | denied |

`DISABLED` and `REVOKED` are explicit administrative states.

`OFFLINE` is usually derived from heartbeat timeout and should not permanently block an Agent if a valid request arrives.

---

## 10. Registration Permission

Registration is the only Agent-related API that does not use Agent token.

Registration requires a valid registration token.

Rules:

- registration token must be valid;
- registration token must not be expired;
- registration token must not be revoked;
- registration token usage limits must be respected if implemented;
- registration token determines Workspace in CE and future editions;
- registration request must not choose arbitrary Workspace;
- Backend issues Agent token after successful registration;
- registration event should be audited.

Registration token must be stored as hash.

Raw registration token must be shown only once when created.

---

## 11. Heartbeat Permission

Agent heartbeat updates the authenticated Agent's runtime state.

Endpoint example:

```http
POST /api/agents/{agentId}/heartbeat
Authorization: Bearer <agentToken>
```

Permission rules:

- token must authenticate an Agent;
- path `agentId` must match authenticated Agent identity, or path `agentId` should be ignored in favor of token identity;
- disabled/revoked Agents are denied;
- heartbeat may update only the authenticated Agent;
- heartbeat must not update another Agent;
- heartbeat payload must not contain raw secrets.

Recommended safer API design:

```http
POST /api/agents/me/heartbeat
```

This avoids path identity mismatch.

---

## 12. Service Report Permission

Agent can report Capsule Services under its own Agent identity.

Endpoint example:

```http
POST /api/agents/{agentId}/services/report
Authorization: Bearer <agentToken>
```

Permission rules:

- token must authenticate an Agent;
- Agent status must allow API access;
- reported services are owned by authenticated Agent unless explicit transfer exists;
- payload `agentId` must not override authenticated Agent identity;
- service identity must be stable;
- Backend must prevent an Agent from overwriting another Agent's service unexpectedly;
- service report must not include raw secrets.

For CE, service ownership can be:

```text
CapsuleService.agentId = authenticatedAgent.agentId
```

---

## 13. Service Identity Collision

Service code collision can happen when two Agents report the same service code.

Possible CE strategies:

### 13.1 Agent-scoped service identity

Uniqueness:

```text
workspaceId + agentId + serviceCode
```

Pros:

- simple;
- prevents cross-Agent overwrite;
- suitable for CE.

Cons:

- same service moving between Agents creates a new service record.

### 13.2 Workspace-scoped service identity

Uniqueness:

```text
workspaceId + serviceCode
```

Pros:

- stable service identity across Agent migration.

Cons:

- requires transfer/claim policy;
- more complex permission checks.

Recommended CE v0.1 strategy:

```text
workspaceId + agentId + serviceCode
```

Future EE may introduce explicit service transfer or ownership claim workflow.

---

## 14. Health Report Permission

Agent can report health only for services it owns.

Permission rules:

- token authenticates Agent;
- service must belong to authenticated Agent;
- health report must not update another Agent's service;
- health payload must not include raw secrets;
- invalid service reference should be rejected or treated as service report mismatch.

If health is included in service report or heartbeat, Backend must still associate it only with authenticated Agent-owned services.

---

## 15. Config Metadata Permission

Agent can report config metadata only for services it owns.

Rules:

- configs belong to authenticated Agent-owned service;
- sensitive values must be masked or represented as `secretRef`;
- raw secrets should be rejected or sanitized where practical;
- Agent cannot update config metadata for another Agent's service;
- CE supports visibility only, not config publishing.

Config editing and publishing are future EE capabilities and require separate permission design.

---

## 16. ActionDefinition Permission

Agent can report ActionDefinitions only for services it owns.

Rules:

- action definitions belong to authenticated Agent-owned service;
- action names must be stable and unique per service;
- Agent cannot define actions for another Agent's service;
- disabled actions must be respected by Backend and Agent;
- action metadata must not include raw secrets.

Backend should validate action definition shape before storing.

---

## 17. Command Polling Permission

Agent can poll only Commands assigned to itself.

Endpoint example:

```http
GET /api/agents/{agentId}/commands
Authorization: Bearer <agentToken>
```

Permission rules:

- token authenticates Agent;
- disabled/revoked Agents are denied;
- query returns only Commands where `command.agentId == authenticatedAgent.agentId`;
- command workspace must match Agent workspace;
- expired Commands should not be dispatched;
- Backend must not return Commands assigned to another Agent.

Recommended safer API design:

```http
GET /api/agents/me/commands
```

---

## 18. Command Dispatch Ownership

When Backend creates a Command from Admin API, it must assign it to the Agent that owns the target service.

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

Agent can report CommandResult only for Commands assigned to itself.

Endpoint example:

```http
POST /api/agents/{agentId}/commands/{commandId}/result
Authorization: Bearer <agentToken>
```

Permission rules:

- token authenticates Agent;
- command must exist;
- command.agentId must equal authenticated Agent ID;
- command.workspaceId must equal authenticated Agent workspace;
- command status must allow result reporting;
- duplicate final results should be handled safely;
- result payload must be sanitized;
- raw secrets must not be stored.

If an Agent reports a result for another Agent's Command, Backend must return denied or not found.

Recommended behavior:

```text
Return 404 or 403 without leaking whether the command exists.
```

---

## 20. Agent API Resource Access Matrix

Recommended CE matrix:

| Operation | Allowed Resource Scope |
|---|---|
| register | valid registration token scope |
| heartbeat | authenticated Agent only |
| report service | authenticated Agent only |
| report health | services owned by authenticated Agent |
| report configs | services owned by authenticated Agent |
| report actions | services owned by authenticated Agent |
| poll commands | Commands assigned to authenticated Agent |
| report command result | Commands assigned to authenticated Agent |
| read admin data | not allowed |
| create command | not allowed through Agent API |
| create registration token | not allowed through Agent API |

---

## 21. Agent Cannot Call Admin API

Agent token must not grant Admin API access.

Rules:

- Admin API requires user session or user token;
- Agent API requires Agent token;
- Agent token is rejected by Admin API;
- user token/session is rejected by Agent API unless explicitly allowed for internal testing, which should be avoided in production;
- API groups should have clear authentication guards.

This prevents Agent token from becoming a general control-plane credential.

---

## 22. Payload Trust Rules

Agent API payloads are untrusted even after authentication.

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

CE may support basic Agent revocation if included in Backend scope.

Revocation means:

- Agent status becomes `REVOKED`;
- Agent token is rejected;
- Agent cannot heartbeat;
- Agent cannot poll Commands;
- Agent cannot report CommandResults;
- UI shows Agent as revoked;
- AuditEvent is created.

If CE v0.1 does not include revoke UI, the model should still allow future token invalidation.

---

## 24. Agent Disable

Disable is a softer administrative state than revoke.

Disabled Agent:

- cannot use Agent API;
- may be re-enabled later;
- retains identity and history;
- should not receive Commands;
- should be visible in UI;
- should create AuditEvent when changed.

CE v0.1 may defer disable/enable UI, but schema can reserve status.

---

## 25. Offline Agent

Offline is derived from heartbeat freshness.

Offline Agent:

- may become online again when it sends valid heartbeat;
- should not be treated the same as revoked;
- may still have pending Commands, but Backend should consider whether to create or dispatch Commands to stale/offline Agents;
- should make related Capsule Services appear stale or offline effectively.

Recommended CE behavior:

- allow valid offline Agent to reconnect;
- avoid dispatching expired Commands;
- show service freshness clearly.

---

## 26. Audit Events

Agent permission-related operations should create AuditEvents where meaningful.

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

CE should avoid auditing every heartbeat success because that would be too noisy.

Minimum CE events:

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

For cross-Agent resource access, consider returning:

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

Backend derives Agent identity from token.

If path-based `agentId` is used, Backend must validate it matches token identity.

---

## 29. Future EE Direction

Future EE may extend Agent permissions with:

- Agent groups;
- workspace-scoped Agent policies;
- Agent capability scopes;
- token rotation;
- Agent disable/re-enable workflow;
- per-Agent action policies;
- sidecar/external Agent target policies;
- IP allowlists;
- mTLS;
- device identity;
- approval workflow for sensitive Agent operations;
- service ownership transfer.

These are not CE v0.1 requirements.

---

## 30. Future Cloud Direction

Future Cloud may extend Agent permissions with:

- tenant isolation;
- organization/workspace-scoped Agent tokens;
- Cloud Agent Gateway routing policy;
- Agent connection rate limiting;
- plan-based Agent limits;
- usage metering by Agent;
- Cloud-managed registration tokens;
- workspace-specific Agent enrollment;
- multi-tenant command isolation;
- hosted audit retention for Agent operations.

These are not CE v0.1 requirements.

---

## 31. CE Reservations

CE should reserve these permission-compatible concepts:

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

CE should not implement full EE/Cloud policy systems in v0.1.

---

## 32. Anti-Patterns

Avoid these patterns.

### 32.1 Trusting request body agentId

Agent identity must come from token authentication.

### 32.2 Agent can poll all Commands

Agent must only receive Commands assigned to itself.

### 32.3 Agent can report result for any Command

CommandResult must be ownership-checked.

### 32.4 Agent token grants Admin API access

Agent token is not a user credential.

### 32.5 Offline equals revoked

Offline is freshness-derived and recoverable; revoked is administrative and permanent unless explicitly restored.

### 32.6 Service code overwrite by another Agent

CE should avoid cross-Agent service overwrite by using Agent-scoped identity or explicit transfer design.

### 32.7 Logging Agent token

Agent token must never be logged.

---

## 33. Acceptance Criteria

The CE Agent Permission Model is acceptable when:

- Agent API authenticates using Agent token;
- Backend stores only token hash;
- Backend derives Agent identity from token;
- Agent heartbeat updates only authenticated Agent;
- Agent service report creates or updates services under authenticated Agent;
- Agent cannot overwrite another Agent's service;
- Agent can poll only Commands assigned to itself;
- Agent cannot receive Commands assigned to another Agent;
- Agent can report CommandResult only for assigned Commands;
- Agent token cannot call Admin API;
- disabled/revoked Agents are rejected;
- offline Agents can reconnect if token is valid;
- raw tokens are not logged;
- permission failures return structured errors;
- audit events are created for meaningful Agent lifecycle and command-result events.

---

## 34. Summary

The Agent Permission Model keeps Opstage's runtime governance boundary safe.

It ensures that each Agent can only report its own services, poll its own Commands, and submit results for its own Commands.

The most important Agent permission rule is:

> Derive Agent authority from the authenticated token, then restrict every Agent API operation to resources owned by that Agent and its Workspace.
