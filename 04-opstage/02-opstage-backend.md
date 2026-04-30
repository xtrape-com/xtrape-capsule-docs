# Opstage Backend

- Status: Draft
- Edition: Shared
- Priority: Medium

本文件属于 `xtrape-capsule` 文档集。`xtrape-capsule` 是面向轻服务 / Capsule Service 的领域体系；`xtrape-capsule-opstage` 是该体系下的统一运行态治理平台。

当前实现重点是 CE 开源社区版。EE 私有化商业版与 Cloud SaaS 版属于未来规划，CE 需要保留扩展点，但不应在早期版本实现其完整能力。

Opstage 是 xtrape-capsule 的统一运行态治理平台，由 UI、Backend 和 Agent 接入机制组成。CE 实现轻量闭环，EE/Cloud 在此基础上扩展规模化能力。

# Opstage Backend

- Status: Implementation Guidance
- Edition: Shared
- Priority: High
- Audience: backend developers, frontend developers, agent SDK developers, architects, security reviewers, AI coding agents

This document defines the Backend subsystem of **Opstage**.

Opstage Backend is the control-plane service that coordinates UI users, Agents, Capsule Services, Commands, CommandResults, AuditEvents, and persistence.

The current implementation focus is **Opstage CE**. EE and Cloud Backend capabilities are future planning tracks and must not expand the CE v0.1 implementation scope.

---

## 1. Purpose

The purpose of Opstage Backend is to provide the runtime governance control plane for Capsule Services.

The Backend should answer and coordinate:

- who is using Opstage UI;
- which Agents are registered;
- which Agents are authenticated;
- which Capsule Services were reported;
- which services are healthy, unhealthy, stale, or offline;
- which configs and actions are visible;
- which predefined actions were requested;
- which Commands should be assigned to Agents;
- which CommandResults were reported;
- which important operations should be audited;
- which runtime state should be persisted.

Opstage Backend is the authoritative server-side boundary for CE governance.

---

## 2. Positioning

Opstage Backend is:

> The control-plane backend for Capsule Service governance.

It is not:

- a business service framework;
- a microservice runtime;
- a browser automation engine;
- a full observability backend;
- a full configuration center;
- a secret vault by default;
- a remote shell server;
- a workflow engine as its first identity;
- a SaaS billing platform in CE.

The first Backend identity should remain runtime governance for Capsule Services.

---

## 3. Relationship with Other Components

Recommended CE relationship:

```text
Opstage UI
    ↓ Admin API
Opstage Backend
    ↑ Agent API
Node.js Embedded Agent SDK
    ↔ Capsule Service
```

The UI communicates with Backend through Admin APIs.

Agents communicate with Backend through Agent APIs.

Capsule Services should not be directly operated by UI.

Backend creates durable Commands. Agents poll or receive Commands and report CommandResults.

---

## 4. Backend Responsibilities

Opstage Backend is responsible for:

- Admin API serving;
- Agent API serving;
- local user authentication;
- session or token handling;
- registration token creation and validation;
- Agent token issuing and validation;
- Agent registration;
- Agent heartbeat processing;
- Capsule Service report processing;
- manifest storage;
- health report storage;
- config metadata storage;
- action metadata storage;
- Command creation;
- Command dispatch state;
- CommandResult processing;
- effective status and freshness calculation;
- AuditEvent creation;
- persistence;
- structured errors;
- sensitive data sanitization;
- security enforcement.

---

## 5. Backend Non-Responsibilities

CE Backend should not be responsible for:

- executing business logic of Capsule Services;
- executing shell commands;
- storing raw secrets by default;
- scraping websites;
- managing browser automation directly;
- replacing application logs, metrics, and traces;
- replacing Nacos/Apollo-style full config publishing;
- managing tenants or organizations;
- enforcing SaaS billing;
- running multi-node HA infrastructure;
- managing enterprise SSO;
- acting as a Kubernetes controller.

Future EE/Cloud may add integrations, but CE Backend should stay focused.

---

## 6. CE Backend Scope

Opstage CE Backend should implement the minimum complete governance backend.

Required CE capabilities:

- local admin user authentication;
- Admin APIs for UI;
- Agent APIs for Agent SDK;
- SQLite persistence;
- default Workspace bootstrap;
- registration token model;
- Agent token model;
- Agent registration;
- Agent heartbeat;
- Capsule Service report;
- manifest storage;
- health report storage;
- config metadata storage;
- action metadata storage;
- Command creation;
- command polling;
- CommandResult reporting;
- basic AuditEvents;
- status and freshness calculation;
- system health endpoint;
- structured errors;
- sensitive value masking.

---

## 7. CE Backend Non-Goals

CE v0.1 Backend should not implement:

- Tenant system;
- Organization system;
- billing;
- subscription;
- usage metering;
- enterprise RBAC;
- SSO / OIDC / LDAP / SAML;
- PostgreSQL/MySQL requirement;
- Redis requirement;
- Queue requirement;
- Kubernetes deployment requirement;
- Agent Gateway;
- WebSocket command channel;
- full observability platform;
- alert rule engine;
- secret vault;
- config publishing workflow;
- license enforcement;
- arbitrary shell execution.

These are future EE or Cloud planning items.

---

## 8. Recommended Backend Stack

Recommended CE Backend stack:

```text
Node.js + TypeScript
Fastify or NestJS
Prisma
SQLite
Zod or similar schema validation
```

Recommended baseline:

```text
Fastify + TypeScript + Prisma + SQLite
```

Rationale:

- lightweight;
- fast to implement;
- good TypeScript support;
- suitable for single-node CE;
- can evolve toward PostgreSQL/MySQL later;
- easy to package with UI into one deployable artifact.

NestJS is acceptable if the team prefers a more structured framework, but it may be heavier for CE v0.1.

---

## 9. API Groups

Backend should expose two main API groups:

```text
Admin API
Agent API
```

Optional system API:

```text
System API
```

### 9.1 Admin API

Admin API is used by Opstage UI.

Examples:

```text
POST /api/admin/auth/login
POST /api/admin/auth/logout
GET  /api/admin/dashboard/summary
GET  /api/admin/agents
GET  /api/admin/agents/{agentId}
GET  /api/admin/services
GET  /api/admin/services/{serviceId}
POST /api/admin/services/{serviceId}/actions/{actionName}/commands
GET  /api/admin/commands
GET  /api/admin/commands/{commandId}
GET  /api/admin/audit-events
POST /api/admin/registration-tokens
```

### 9.2 Agent API

Agent API is used by Agent SDKs.

Examples:

```text
POST /api/agents/register
POST /api/agents/{agentId}/heartbeat
POST /api/agents/{agentId}/services/report
GET  /api/agents/{agentId}/commands
POST /api/agents/{agentId}/commands/{commandId}/result
```

### 9.3 System API

System API is used for runtime checks.

Examples:

```text
GET /api/system/health
GET /api/system/version
```

CE v0.1 may keep System API minimal.

---

## 10. Admin API Rules

Admin API must:

- require authenticated admin user;
- validate request payloads;
- enforce Backend-side authorization checks;
- create AuditEvents for important operations;
- sanitize sensitive data in responses;
- return structured errors;
- never expose raw stack traces to UI;
- never expose raw tokens after creation.

CE v0.1 may use one local owner/admin role.

Future EE may add RBAC and permission checks.

---

## 11. Agent API Rules

Agent API must:

- validate Agent token except registration endpoint;
- derive Agent identity from token;
- reject disabled or revoked Agents;
- ensure path `agentId` matches authenticated Agent;
- ensure Command belongs to authenticated Agent;
- validate service report payloads;
- sanitize sensitive values;
- avoid logging raw Agent token;
- return structured errors.

Agent API must not trust workspace or tenant fields from arbitrary payloads.

CE may use only default Workspace, but ownership validation should still be clean.

---

## 12. Authentication Model

CE Backend needs two authentication paths:

```text
Admin user authentication
Agent authentication
```

### 12.1 Admin authentication

Recommended CE approach:

```text
username + password
HTTP-only session cookie
```

Alternative:

```text
JWT bearer token
```

Password storage:

```text
argon2 preferred
bcrypt acceptable
```

Never store raw passwords.

### 12.2 Agent authentication

Agents use bearer token:

```http
Authorization: Bearer <agentToken>
```

Backend stores only Agent token hash.

Backend must never store or log raw Agent token after issuing it.

---

## 13. Token Model

CE Backend handles two token types:

```text
registration token
Agent token
```

### 13.1 Registration token

Registration token is used for initial Agent enrollment.

Rules:

- generated by Backend;
- shown only once;
- stored as hash;
- can expire;
- can be one-time use;
- can be revoked;
- scoped to default Workspace in CE;
- audited when created and used.

Recommended prefix:

```text
opstage_reg_
```

### 13.2 Agent token

Agent token is used after registration.

Rules:

- issued after successful registration;
- shown only in registration response;
- stored as hash in Backend;
- stored locally by Agent SDK;
- sent via Authorization header;
- can be revoked;
- should not be logged.

Recommended prefix:

```text
opstage_agent_
```

---

## 14. Core Data Model

CE Backend should persist these core models:

```text
Workspace
User
RegistrationToken
Agent
AgentToken
CapsuleService
HealthReport
ConfigItem
ActionDefinition
Command
CommandResult
AuditEvent
SystemSetting
```

These models may be implemented in a simplified way for CE.

Future EE/Cloud may extend them, but should not redefine their meaning.

---

## 15. Workspace Model

CE should create one default Workspace.

Recommended default ID or code:

```text
wks_default
```

CE does not need Workspace management UI.

However, storing `workspaceId` on core records helps future EE/Cloud compatibility.

Core records that may include `workspaceId`:

```text
Agent
CapsuleService
Command
CommandResult
AuditEvent
RegistrationToken
```

---

## 16. Agent Model

Agent represents the governance bridge between Backend and Capsule Services.

Recommended fields:

```text
id
workspaceId
code
name
status
mode
runtime
version
hostname
os
arch
lastHeartbeatAt
registeredAt
metadataJson
createdAt
updatedAt
```

Recommended status values:

```text
ONLINE
OFFLINE
DISABLED
REVOKED
UNKNOWN
```

Agent status may be calculated from heartbeat freshness and stored disabled/revoked state.

---

## 17. Capsule Service Model

CapsuleService represents a lightweight service reported by an Agent.

Recommended fields:

```text
id
workspaceId
agentId
code
name
description
runtime
version
agentMode
reportedStatus
effectiveStatus
healthStatus
lastReportedAt
lastHealthAt
manifestJson
metadataJson
createdAt
updatedAt
```

Recommended uniqueness:

```text
workspaceId + code
```

or, if service identity is Agent-scoped in early CE:

```text
workspaceId + agentId + code
```

The decision should be consistent with service migration expectations.

---

## 18. HealthReport Model

HealthReport stores latest or historical service health.

CE v0.1 may store only latest health or limited history.

Recommended fields:

```text
id
workspaceId
agentId
serviceId
status
message
checkedAt
receivedAt
dependenciesJson
detailsJson
createdAt
```

Recommended status values:

```text
UP
DOWN
DEGRADED
UNKNOWN
```

---

## 19. ConfigItem Model

ConfigItem stores config metadata reported by the service.

Recommended fields:

```text
id
workspaceId
serviceId
key
label
type
value
 defaultValue
editable
sensitive
source
description
validationJson
metadataJson
updatedAt
```

Sensitive config values must be masked or represented as `secretRef`.

CE v0.1 should support visibility only, not config publishing.

---

## 20. ActionDefinition Model

ActionDefinition stores predefined actions reported by the service.

Recommended fields:

```text
id
workspaceId
serviceId
name
label
description
dangerLevel
enabled
inputSchemaJson
resultSchemaJson
metadataJson
updatedAt
```

Recommended danger values:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Backend must validate requested actions against stored ActionDefinitions.

---

## 21. Command Model

Command represents a requested operation to be executed by an Agent.

Recommended fields:

```text
id
workspaceId
agentId
serviceId
commandType
actionName
status
payloadJson
createdByActorType
createdByActorId
createdAt
dispatchedAt
startedAt
finishedAt
expiresAt
metadataJson
```

CE v0.1 supports only:

```text
ACTION
```

as command type.

Recommended status values:

```text
PENDING
DISPATCHED
RUNNING
SUCCESS
FAILED
EXPIRED
CANCELLED
```

CE may not need all statuses, but should avoid a design that blocks them later.

---

## 22. CommandResult Model

CommandResult stores execution result reported by Agent.

Recommended fields:

```text
id
workspaceId
commandId
agentId
serviceId
status
outputText
errorMessage
resultJson
startedAt
finishedAt
reportedAt
metadataJson
```

Rules:

- result must belong to the authenticated Agent;
- result should be sanitized;
- raw secrets must not be stored;
- duplicate final result reports should be handled safely.

---

## 23. AuditEvent Model

AuditEvent records important operations.

Recommended fields:

```text
id
workspaceId
actorType
actorId
action
resourceType
resourceId
result
description
requestJson
resultJson
metadataJson
createdAt
```

Recommended actor types:

```text
USER
AGENT
SYSTEM
```

Recommended results:

```text
SUCCESS
FAILED
DENIED
```

AuditEvents should be sanitized and should not contain raw secrets.

---

## 24. Command Flow

The core command flow is:

```text
UI requests action execution
    ↓
Backend validates user authentication
    ↓
Backend validates service and action
    ↓
Backend creates Command
    ↓
Agent polls Commands
    ↓
Backend returns assigned Command
    ↓
Agent executes local predefined action
    ↓
Agent reports CommandResult
    ↓
Backend stores result and updates Command status
    ↓
Backend creates AuditEvent
```

This flow keeps operations durable and auditable.

---

## 25. Service Report Flow

Service report flow:

```text
Agent starts or reconnects
    ↓
Agent reports service manifest
    ↓
Backend validates Agent token
    ↓
Backend upserts CapsuleService
    ↓
Backend stores manifest
    ↓
Backend stores config metadata
    ↓
Backend stores action definitions
    ↓
Backend updates lastReportedAt
    ↓
Backend creates AuditEvent if material change occurs
```

CE may audit first service report and major changes only, not every identical report.

---

## 26. Heartbeat Flow

Heartbeat flow:

```text
Agent sends heartbeat periodically
    ↓
Backend validates Agent token
    ↓
Backend updates Agent.lastHeartbeatAt
    ↓
Backend updates latest health if included
    ↓
Backend recalculates or enables calculation of effective status
```

Do not create AuditEvent for every heartbeat.

Heartbeat is operational state, not audit history.

---

## 27. Status and Freshness Calculation

Backend should calculate effective status from multiple sources.

Agent status depends on:

```text
disabled/revoked state
lastHeartbeatAt
offline threshold
```

Capsule Service effective status depends on:

```text
reportedStatus
healthStatus
lastReportedAt
lastHealthAt
Agent status
freshness thresholds
```

Important rule:

> A stale service must not be shown as fresh online only because its last reported status was online.

---

## 28. Sensitive Data Handling

Backend must sanitize sensitive data.

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
```

Backend should:

- hash passwords;
- hash tokens;
- mask sensitive config values;
- avoid storing raw secrets;
- sanitize AuditEvent payloads;
- sanitize CommandResult payloads;
- avoid logging secrets.

Use `secretRef` for references to raw secrets stored elsewhere.

---

## 29. Error Handling

Backend should return structured errors.

Example:

```json
{
  "success": false,
  "error": {
    "code": "AGENT_TOKEN_INVALID",
    "message": "Agent token is invalid."
  }
}
```

Do not return raw stack traces to UI or Agent.

Logs may include internal details, but must not include raw secrets.

---

## 30. Persistence Strategy

CE v0.1 should use SQLite by default.

Recommended persistence stack:

```text
Prisma + SQLite
```

Design should remain reasonably portable toward:

```text
PostgreSQL
MySQL
```

for future EE.

Avoid unnecessary SQLite-specific assumptions in core design.

---

## 31. Packaging Strategy

CE may package Backend and UI together.

Recommended CE deployment:

```text
single container
Backend serves API
Backend serves built UI static assets
SQLite data volume
single exposed port
```

This keeps deployment lightweight.

Future EE may split UI, Backend, Worker, Scheduler, Database, Cache, and Queue.

---

## 32. System Health

Backend should expose a system health endpoint.

Minimum CE endpoint:

```text
GET /api/system/health
```

Response should include:

```text
status
version
database status
current time
```

Future EE may add readiness/liveness endpoints.

---

## 33. EE Backend Extension Direction

Future EE Backend may add:

- PostgreSQL/MySQL support;
- RBAC;
- SSO/OIDC/LDAP/SAML;
- audit retention and export;
- alert rule engine;
- observability integrations;
- secret provider integrations;
- sidecar/external Agent support;
- WebSocket or queue-backed command delivery;
- worker and scheduler processes;
- high availability;
- license and support entitlement.

These are not CE v0.1 requirements.

---

## 34. Cloud Backend Extension Direction

Future Cloud Backend may add:

- Tenant model;
- Organization model;
- multi-workspace management;
- team invitations;
- subscription billing;
- usage metering;
- Agent Gateway;
- managed alerting;
- Cloud data export/deletion workflows;
- Cloud support access;
- multi-tenant rate limiting;
- Cloud operational telemetry.

These are not CE v0.1 requirements.

---

## 35. Acceptance Criteria

Opstage CE Backend is acceptable when:

- local admin user can log in;
- UI can call authenticated Admin APIs;
- registration token can be created and shown once;
- Agent can register with registration token;
- Agent token is stored as hash;
- Agent can heartbeat;
- Agent can report Capsule Service manifest;
- Backend stores service, health, configs, and actions;
- UI can request predefined action execution;
- Backend creates Command;
- Agent can poll Command;
- Agent can report CommandResult;
- Backend stores CommandResult;
- AuditEvents are created for important operations;
- sensitive values are masked;
- stale status is calculated correctly;
- arbitrary shell execution is not exposed;
- Backend runs with SQLite in a lightweight deployment.

---

## 36. Summary

Opstage Backend is the control-plane service for Capsule Service governance.

It should provide a simple but complete CE governance loop first, then leave clean extension points for EE and Cloud.

The most important Backend rule is:

> Keep Backend authoritative for identity, validation, persistence, commands, results, status, and audit while keeping CE lightweight and free from future-edition complexity.