# Opstage Backend

- Status: Implementation Guidance
- Edition: Shared
- Priority: High
- Audience: backend developers, frontend developers, agent SDK developers, architects, security reviewers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/` (OpenAPI / Prisma) disagree, the ADRs and contracts win for CE v0.1. Field names below should match Prisma; if they ever drift, follow Prisma `schema.prisma`.

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
Fastify
Zod or similar schema validation
Prisma
SQLite
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
GET  /api/admin/capsule-services
GET  /api/admin/capsule-services/{serviceId}
POST /api/admin/capsule-services/{serviceId}/actions/{actionName}
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

CE v0.1 fields (matches Prisma `Agent`):

```text
id              agt_xxx
workspaceId     wks_xxx
code            stable identifier (kebab-case, unique within workspace)
name            human-readable name nullable
mode            embedded | sidecar | external (CE v0.1: embedded only)
runtime         nodejs | java | python | go | other (CE v0.1: nodejs)
status          PENDING | ONLINE | OFFLINE | DISABLED | REVOKED
lastHeartbeatAt datetime nullable
disabledAt      datetime nullable
revokedAt       datetime nullable
createdAt       datetime
updatedAt       datetime
```

CE v0.1 does NOT persist `version`, `hostname`, `os`, `arch`, `registeredAt`, or `metadataJson`. EE/Cloud may add them later.

Status values (must match OpenAPI `AgentStatus`):

```text
PENDING      Agent record exists, has not yet sent successful heartbeat
ONLINE       within heartbeat freshness window
OFFLINE      missed heartbeat threshold (default 90s)
DISABLED     administratively disabled
REVOKED      token trust revoked
```

Agent status is calculated from heartbeat freshness and stored disabled/revoked state.

---

## 17. Capsule Service Model

CapsuleService represents a lightweight service reported by an Agent.

CE v0.1 fields (matches Prisma `CapsuleService`):

```text
id              svc_xxx
workspaceId     wks_xxx
agentId         agt_xxx
code            stable identifier (kebab-case)
name            human-readable name
description     nullable
version         from manifest
runtime         from manifest
status          UNKNOWN | HEALTHY | UNHEALTHY | STALE | OFFLINE   (effective)
healthStatus    UP | DOWN | DEGRADED | UNKNOWN | nullable          (latest reported)
lastReportedAt  datetime nullable
lastHealthAt    datetime nullable
manifestJson    TEXT (JSON) - the full reported manifest
metadataJson    TEXT (JSON) nullable
createdAt
updatedAt
```

Reported vs. effective status (CE v0.1 decision): the database persists only the **effective** `status`. The "last reported" view is derived from `lastReportedAt`, `lastHealthAt`, and the latest `HealthReport` row — there is no separate `reportedStatus` column. EE/Cloud may add one later.

Required uniqueness (CE v0.1 decision, matches Prisma `@@unique([workspaceId, code])`):

```text
(workspaceId, code)
```

Rationale: in CE v0.1, service code is globally unique within a workspace. The Agent is recorded via `agentId` but is not part of the uniqueness key. If the same service migrates between Agents, the row's `agentId` is updated in-place. EE/Cloud may revisit this if cross-Agent service multiplicity is needed.

Conflict handling: when `POST /api/agents/{agentId}/services/report` is called with a service code that already exists in the same workspace:

- if the existing row has the same `agentId`, upsert (update) in place;
- if the existing row has a different `agentId`, update `agentId` to the calling Agent and write an audit event `capsuleService.reassigned`.

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

CE v0.1 danger values (must match OpenAPI `DangerLevel`):

```text
LOW
MEDIUM
HIGH
```

`CRITICAL` is reserved for future EE/Cloud editions.

Backend must validate requested actions against stored ActionDefinitions and enforce confirmation when `requiresConfirmation = true`.

---

## 21. Command Model

Command represents a requested operation to be executed by an Agent.

CE v0.1 fields (matches Prisma `Command`):

```text
id                cmd_xxx
workspaceId       wks_xxx
agentId           agt_xxx
serviceId         svc_xxx
type              ACTION (CE v0.1 only)
actionName        string
status            PENDING | RUNNING | SUCCEEDED | FAILED | EXPIRED | CANCELLED
payloadJson       TEXT (JSON) nullable
createdByUserId   usr_xxx nullable
createdAt
startedAt         set when Agent polls (PENDING -> RUNNING)
completedAt       set when terminal (SUCCEEDED | FAILED | EXPIRED | CANCELLED)
expiresAt
```

CE v0.1 supports only `ACTION` as command type.

Status values (must match OpenAPI `CommandStatus`):

```text
PENDING       waiting for Agent poll
RUNNING       Agent has polled; execution started
SUCCEEDED     Agent reported success
FAILED        Agent reported failure
EXPIRED       not delivered or completed before expiresAt
CANCELLED     reserved for future use (no UI in CE v0.1)
```

There is no separate `DISPATCHED` state in CE v0.1 — polling transitions Commands directly from `PENDING` to `RUNNING`.

---

## 22. CommandResult Model

CommandResult stores the execution result reported by Agent.

CE v0.1 fields (matches Prisma `CommandResult`):

```text
id           crs_xxx
commandId    cmd_xxx (unique 1:1 with Command)
agentId      agt_xxx
success      boolean
message      string nullable
dataJson     TEXT (JSON) nullable    (serialized from `data`)
errorJson    TEXT (JSON) nullable    (serialized from `error`)
reportedAt   datetime
createdAt
```

The Agent's report body (`success` / `message` / `data` / `error`) maps directly to these columns. Backend records `Command.completedAt` separately (server clock).

Rules:

- result must belong to the authenticated Agent;
- result must be sanitized before persistence;
- raw secrets must not be stored;
- duplicate result reports MUST be rejected (Command already in terminal state).

---

## 23. AuditEvent Model

AuditEvent records important operations.

CE v0.1 fields (matches Prisma `AuditEvent`):

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
metadataJson  TEXT (JSON) nullable
createdAt
```

Recommended actor types:

```text
USER
AGENT
SYSTEM
```

CE v0.1 result values (must match OpenAPI `AuditResult`):

```text
SUCCESS
FAILURE
```

`DENIED`, `ERROR`, and `PENDING` are reserved for future EE/Cloud editions. Map authorization rejections, validation failures, and runtime errors to `FAILURE` with `metadata.errorCode`.

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
healthStatus      (latest reported HealthStatus)
lastReportedAt
lastHealthAt
Agent status
freshness thresholds
```

Important rule:

> A stale service must not be shown as fresh online only because its last reported status was online.

### 27.1 Background Sweep Jobs (CE v0.1)

CE v0.1 runs three small in-process sweep jobs from a single scheduler. Defaults come from ADR 0001 §10. The scheduler MUST be:

- single-leader (no two backend instances may sweep concurrently — CE is single-process so a per-process `setInterval` is sufficient);
- idempotent (re-running the same sweep produces the same final state);
- bounded (each sweep MUST process at most `BACKGROUND_SWEEP_BATCH_SIZE` rows per tick, default 500, to avoid long transactions on SQLite);
- cancel-aware (the scheduler MUST stop the next tick when `app.close()` is called).

| Sweep                  | Trigger                                                  | Action                                                                                                | AuditEvent                                                |
|------------------------|----------------------------------------------------------|-------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| `agent-offline-sweep`  | every `BACKGROUND_SWEEP_INTERVAL_SECONDS` (default 30 s) | Mark Agents in `PENDING`/`ONLINE` whose `lastHeartbeatAt < now − AGENT_OFFLINE_THRESHOLD_SECONDS` (default 90 s) as `OFFLINE`. | `system.agent.offline` (actorType=`SYSTEM`, result=`SUCCESS`) |
| `service-stale-sweep`  | every `BACKGROUND_SWEEP_INTERVAL_SECONDS`                | Mark CapsuleServices whose `lastReportedAt < now − HEALTH_STALE_THRESHOLD_SECONDS` (default 120 s) as `STALE` (or `OFFLINE` if their Agent is `OFFLINE`). | `system.service.stale` / `system.service.offline`         |
| `command-ttl-sweep`    | every `BACKGROUND_SWEEP_INTERVAL_SECONDS`                | Transition Commands in `PENDING` or `RUNNING` whose `expiresAt < now` to `EXPIRED`, then write a synthetic `CommandResult` with `success=false`, `error.code=COMMAND_EXPIRED`. | `command.expired` (actorType=`SYSTEM`)                    |

Pseudocode for the scheduler:

```ts
// modules/system/sweeper.ts (pseudo-code)
export function startSweeper(app: FastifyInstance, deps: { prisma: PrismaClient; clock: () => Date; cfg: AppConfig }) {
  const tick = async () => {
    try {
      await runAgentOfflineSweep(deps);
      await runServiceStaleSweep(deps);
      await runCommandTtlSweep(deps);
    } catch (err) {
      app.log.error({ err }, "background sweep failed");
    }
  };
  const handle = setInterval(tick, deps.cfg.backgroundSweepIntervalSeconds * 1000);
  app.addHook("onClose", async () => clearInterval(handle));
  void tick(); // warmup tick on boot
}
```

```ts
async function runAgentOfflineSweep({ prisma, clock, cfg }: Deps) {
  const cutoff = new Date(clock().getTime() - cfg.agentOfflineThresholdSeconds * 1000);
  const stale = await prisma.agent.findMany({
    where: {
      status: { in: ["PENDING", "ONLINE"] },
      lastHeartbeatAt: { lt: cutoff },
    },
    take: cfg.backgroundSweepBatchSize,
    select: { id: true, workspaceId: true },
  });
  for (const agent of stale) {
    await prisma.$transaction([
      prisma.agent.update({ where: { id: agent.id }, data: { status: "OFFLINE" } }),
      prisma.auditEvent.create({
        data: {
          id: newId("aud_"),
          workspaceId: agent.workspaceId,
          actorType: "SYSTEM",
          actorId:   null,
          action:    "system.agent.offline",
          targetType:"Agent",
          targetId:  agent.id,
          result:    "SUCCESS",
          message:   "Agent crossed offline threshold.",
          createdAt: clock(),
        },
      }),
    ]);
  }
}
```

The other two sweeps follow the same shape, swapping table and audit action. `command-ttl-sweep` MUST also insert a synthetic `CommandResult` with `success=false`, `error: { code: "COMMAND_EXPIRED", message: "TTL elapsed before completion." }` so the UI sees a uniform terminal state.

CE v0.1 does NOT broadcast SSE/WebSocket from sweeps; UI polls. Push delivery is reserved for EE.

### 27.2 Effective Status Derivation

Read paths (`GET /api/admin/agents`, `GET /api/admin/capsule-services`) MUST return the persisted `effectiveStatus`/`status` column, not recompute on every request. This guarantees:

- consistent values across UI tabs and API consumers;
- a single audit trail for status transitions (sweeper-driven only);
- monotonic transitions (no flicker between requests).

If the persisted column is older than `2 × BACKGROUND_SWEEP_INTERVAL_SECONDS` (i.e. the sweeper hasn't run), Backend logs a warning at WARN level — this is the signal that the sweeper has crashed or fallen behind.

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
