# CE Architecture

- Status: Implementation Target
- Edition: CE
- Priority: Current
- Audience: architects, backend developers, frontend developers, agent SDK developers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs (especially ADR 0005 — technology stack) or `09-contracts/` disagree, the ADRs and contracts win for CE v0.1.

This document defines the architecture of **Opstage CE v0.1**.

CE architecture should be lightweight, modular, self-hosted, and simple enough for the first open-source implementation, while preserving extension points for EE and Cloud.

---

## 1. Architecture Goal

The goal of CE architecture is to prove one complete governance loop:

```text
Node.js Capsule Service
    ↓ Embedded Agent SDK
Opstage Backend
    ↓
Opstage UI
```

The system should allow a developer to:

1. run Opstage CE locally;
2. start a demo Capsule Service;
3. register an embedded Agent;
4. view Agent and Capsule Service status;
5. view manifest, health, and config metadata;
6. trigger a predefined action;
7. see Command and CommandResult;
8. inspect Audit Events.

---

## 2. Architecture Principles

CE v0.1 architecture must follow these principles:

1. Keep CE lightweight.
2. Keep Capsule Services independently runnable.
3. Use Agent-based registration as the service onboarding path.
4. Use outbound-first Agent communication.
5. Use HTTP heartbeat and command polling.
6. Use SQLite by default.
7. Keep UI, Backend, Agent SDK, and Capsule Service responsibilities separated.
8. Avoid arbitrary remote shell execution.
9. Avoid EE and Cloud complexity in CE v0.1.
10. Preserve extension points for future databases, Agent modes, and editions.

---

## 3. High-Level Architecture

CE v0.1 consists of four main parts:

```text
+-----------------------------+
|        Opstage UI           |
|  Web console for operators  |
+-------------+---------------+
              |
              | Admin API
              v
+-------------+---------------+
|       Opstage Backend       |
|  Control plane and storage  |
+-------------+---------------+
              |
              | Agent API
              v
+-------------+---------------+
| Node.js Embedded Agent SDK  |
|  Governance bridge          |
+-------------+---------------+
              |
              | local in-process calls
              v
+-------------+---------------+
|    Capsule Service          |
|  Business / worker logic    |
+-----------------------------+
```

The Backend is the control plane.

The Agent SDK is the governance bridge.

The Capsule Service remains the owner of its business logic.

---

## 4. Runtime Topology

### 4.1 Local development topology

```text
Developer Machine
├── Opstage Backend
├── Opstage UI
├── SQLite database file
└── Demo Capsule Service
    └── Node.js Embedded Agent SDK
```

This topology should be easy to start during development.

### 4.2 Docker topology

Preferred CE user-facing deployment:

```text
Docker Host
├── opstage-ce container
│   ├── Backend
│   ├── static UI assets
│   └── SQLite data volume
└── demo-capsule-service container or local process
    └── Node.js Embedded Agent SDK
```

The first public deployment should be possible with:

```bash
docker run -p 8080:8080 -v ./data:/app/data xtrape/capsule-opstage-ce
```

A Docker Compose example may include both Opstage CE and demo service.

### 4.3 Future topology extension

Future EE/Cloud may split components:

```text
Opstage UI
Opstage Backend
Worker / Scheduler
Database
Message Queue
Log Storage
Metric Storage
Agent Gateway
```

CE v0.1 should not require these components.

---

## 5. Component Responsibilities

### 5.1 Opstage UI

Opstage UI is the human-facing Web console.

Responsibilities:

- login;
- dashboard;
- list Agents;
- show Agent detail;
- list Capsule Services;
- show Capsule Service detail;
- show manifest;
- show health;
- show configs;
- show actions;
- trigger predefined actions;
- show Commands and CommandResults;
- show Audit Events;
- display stale status clearly.

UI must not:

- call Agents directly;
- execute arbitrary commands;
- contain Capsule Service business logic;
- bypass Backend validation.

### 5.2 Opstage Backend

Opstage Backend is the control plane.

Responsibilities:

- authenticate UI users;
- create default Workspace;
- manage registration tokens;
- register Agents;
- issue and validate Agent tokens;
- receive heartbeats;
- receive service reports;
- store Capsule Service manifests;
- store health reports;
- store config metadata;
- store action metadata;
- create Commands;
- expose Commands to Agents through polling;
- receive CommandResults;
- write Audit Events;
- calculate effective statuses;
- expose Admin APIs to UI.

Backend must not:

- directly manage arbitrary services without Agent registration;
- execute Capsule Service business logic;
- expose arbitrary shell command execution;
- require Kubernetes, service mesh, or distributed queue in CE v0.1.

### 5.3 Node.js Embedded Agent SDK

The Node.js Embedded Agent SDK runs inside a Capsule Service process.

Responsibilities:

- register with Backend using registration token;
- store or expose Agent token persistence guidance;
- send heartbeat;
- report manifest;
- report health;
- report config metadata;
- report action definitions;
- poll Commands;
- invoke local action handlers;
- report CommandResults;
- retry when Backend is temporarily unavailable.

Agent SDK must not:

- prevent the Capsule Service from starting when Backend is unavailable;
- include a default arbitrary shell execution action;
- leak raw secrets in reports;
- invent custom status values outside shared specs.

### 5.4 Capsule Service

Capsule Service is the managed lightweight service.

Responsibilities:

- own business or worker logic;
- provide manifest metadata;
- provide health provider;
- provide config metadata provider;
- register predefined action handlers;
- continue core work even when Opstage is unavailable.

Capsule Service must not:

- depend on Opstage for basic startup;
- move its business logic into Opstage Backend;
- expose raw secrets in manifest, health, config, command, or audit payloads.

### 5.5 SQLite Database

SQLite is the default CE persistence layer.

Responsibilities:

- store users;
- store default Workspace;
- store Agents;
- store Agent tokens as hashes;
- store Capsule Services;
- store health snapshots;
- store config metadata or manifest JSON;
- store action metadata;
- store Commands;
- store CommandResults;
- store Audit Events.

SQLite should be replaceable by MySQL/PostgreSQL in future versions.

---

## 6. Logical Module Architecture

CE Backend should be organized around conceptual modules:

```text
auth
workspaces
agents
agent-tokens
capsule-services
health
configs
actions
commands
audit
system
```

Recommended dependencies:

```text
Admin API -> application services -> repositories
Agent API -> application services -> repositories
Status calculation -> agents + health + capsule-services
Command handling -> actions + agents + audit
Audit -> shared audit writer
```

Modules may be physically combined in CE v0.1 if implementation stays simple, but conceptual boundaries should remain clear.

---

## 7. Monorepo Architecture

Repository structure (must match `10-implementation/00-monorepo-structure.md`):

```text
xtrape-capsule-opstage/
├── apps/
│   ├── opstage-backend/
│   ├── opstage-ui/
│   └── demo-capsule-service/
├── packages/
│   ├── contracts/
│   ├── db/
│   ├── agent-node/
│   ├── shared/
│   └── test-utils/
├── deploy/
│   ├── docker/
│   └── compose/
└── README.md
```

### 7.1 `apps/opstage-backend`

Fastify backend application. Contains HTTP server, Admin APIs, Agent APIs, database access, auth, status calculation, command handling, audit writing.

### 7.2 `apps/opstage-ui`

React + Ant Design web UI application. Contains login page, dashboard, Agent pages, Capsule Service pages, Command pages, Audit pages.

### 7.3 `apps/demo-capsule-service`

Demo Capsule Service used to prove CE integration end-to-end.

### 7.4 `packages/agent-node`

Node.js embedded Agent SDK (formerly proposed as `agent-sdk-node`).

### 7.5 `packages/contracts`

Generated and hand-written TypeScript types derived from `09-contracts/openapi/opstage-ce-v0.1.yaml` (manifest, health, config, action, command, audit, status).

### 7.6 `packages/db`

Prisma schema, generated client, migration runner. Wraps `09-contracts/prisma/schema.prisma`.

### 7.7 `packages/shared`

Cross-cutting helpers: `newId(prefix)`, time/clock helpers, redaction utilities, shared error classes.

### 7.8 `packages/test-utils`

Shared test fixtures, factory builders, and HTTP test client used by backend, UI, and Agent SDK test suites.

---

## 8. Backend Architecture

### 8.1 Backend stack

CE v0.1 Backend stack (decided by ADR 0005):

```text
Node.js + TypeScript + Fastify + Zod + Prisma + SQLite
```

Rationale:

- TypeScript matches Agent SDK and UI types;
- Fastify is lightweight, fast, and easy to embed in Docker images;
- Zod provides shared request/response validation with TypeScript inference;
- Prisma supports SQLite now and MySQL/PostgreSQL later;
- SQLite keeps CE deployment lightweight.

NestJS was considered but rejected for CE v0.1 due to its larger runtime footprint and steeper learning curve. See ADR 0005 for the full evaluation.

### 8.2 API groups

Backend should expose two API surfaces:

```text
Admin APIs
Agent APIs
```

Admin APIs are called by UI.

Agent APIs are called by Agents.

### 8.3 Admin APIs

Admin APIs include:

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
```

Exact paths may change, but these capability groups must exist.

### 8.4 Agent APIs

Agent APIs include:

```text
POST /api/agents/register
POST /api/agents/{agentId}/heartbeat
POST /api/agents/{agentId}/services/report
GET  /api/agents/{agentId}/commands
POST /api/agents/{agentId}/commands/{commandId}/result
```

Agent APIs must require Agent token after registration.

---

## 9. UI Architecture

### 9.1 Recommended UI shape

UI should be a single-page Web console.

It may use:

```text
React + TypeScript + Ant Design
```

or:

```text
Vue 3 + TypeScript + Naive UI / Element Plus
```

The final decision should be documented in `04-ce-technology-stack.md`.

### 9.2 UI pages

Required pages:

```text
Login
Dashboard
Agents
Agent Detail
Capsule Services
Capsule Service Detail
Commands
Audit Logs
System Settings or Setup
```

### 9.3 Service detail layout

Required tabs:

```text
Overview
Manifest
Health
Configs
Actions
Commands
Audit
```

### 9.4 UI status behavior

UI must display effective status prominently.

It should show:

```text
Effective Status
Reported Status
Health Status
Freshness
Agent Status
Last Heartbeat At
Last Reported At
Reason
```

Do not show stale services as confidently online.

---

## 10. Agent SDK Architecture

### 10.1 SDK role

The Agent SDK is a small client-side runtime library embedded in a Node.js Capsule Service.

It is responsible for governance communication, not business logic.

### 10.2 SDK internal parts

Recommended internal parts:

```text
AgentClient
RegistrationManager
HeartbeatLoop
ServiceReporter
CommandPoller
ActionRegistry
HealthProviderRegistry
ConfigProviderRegistry
TokenStore
Logger
```

### 10.3 SDK startup flow

```text
Capsule Service starts
    ↓
Agent SDK initializes
    ↓
Agent SDK loads stored Agent token if available
    ↓
If no token, register with registration token
    ↓
Start heartbeat loop
    ↓
Report manifest and service metadata
    ↓
Start command polling loop
```

If Backend is unavailable, the SDK should retry in the background and not block the service startup.

---

## 11. Data Architecture

CE v0.1 should use a simple relational schema with JSON fields for flexible metadata.

Required data objects:

```text
User
Workspace
Agent
AgentToken
CapsuleService
HealthReport
ConfigItem
ActionDefinition
Command
CommandResult
AuditEvent
```

Recommended flexible JSON fields:

```text
manifestJson
health.detailsJson
health.dependenciesJson
config.metadataJson
action.inputSchemaJson
action.resultSchemaJson
command.payloadJson
command.resultJson
audit.requestJson
audit.resultJson
audit.metadataJson
```

Avoid over-normalizing resources, capabilities, and future dynamic models in CE v0.1.

---

## 12. Core Data Flows

### 12.1 Registration flow

```text
Agent SDK
    ↓ POST /api/agents/register with registration token
Backend
    ↓ validate registration token
Backend
    ↓ create Agent and Agent token
Agent SDK
    ↓ store Agent token
UI
    ↓ shows Agent
```

### 12.2 Heartbeat flow

```text
Agent SDK
    ↓ POST /api/agents/{agentId}/heartbeat
Backend
    ↓ update lastHeartbeatAt
Backend
    ↓ calculate Agent status
UI
    ↓ shows Agent online/offline
```

### 12.3 Service report flow

```text
Agent SDK
    ↓ report manifest, configs, actions
Backend
    ↓ validate and upsert CapsuleService
Backend
    ↓ store manifest and extracted fields
UI
    ↓ shows service detail
```

### 12.4 Health flow

```text
Capsule Service health provider
    ↓ Agent SDK
Backend
    ↓ store latest HealthReport
Backend
    ↓ calculate effective service status
UI
    ↓ shows health and freshness
```

### 12.5 Action and Command flow

```text
User clicks action in UI
    ↓
Backend creates Command
    ↓
Agent polls Command
    ↓
Agent invokes local action handler
    ↓
Agent reports CommandResult
    ↓
Backend updates Command and AuditEvent
    ↓
UI shows result
```

### 12.6 Offline detection flow

```text
Agent stops heartbeat
    ↓
Backend detects heartbeat timeout
    ↓
Agent effective status = OFFLINE
    ↓
Services managed by Agent become STALE
    ↓
UI displays stale status
```

---

## 13. Packaging Architecture

CE v0.1 should support two packaging modes.

### 13.1 Development mode

```text
Backend dev server
UI dev server
Demo Capsule Service process
SQLite local file
```

### 13.2 Production-like single container mode

```text
Single container
├── Backend server
├── built UI static assets
└── SQLite data volume
```

The Backend can serve UI static assets in the single-container mode.

---

## 14. Security Architecture

CE v0.1 security architecture includes:

- local admin authentication;
- Agent registration token;
- Agent token;
- token hash storage;
- Agent token validation on Agent APIs;
- Agent disabled/revoked checks;
- no arbitrary shell execution;
- sensitive value masking;
- audit for important operations.

CE v0.1 does not include:

- SSO;
- RBAC policy engine;
- secret vault;
- mTLS;
- device attestation;
- compliance-grade audit immutability.

---

## 15. Extension Points

CE architecture should preserve extension points for future editions.

| Area | CE v0.1 | Future |
|---|---|---|
| Database | SQLite | MySQL, PostgreSQL |
| Agent mode | Node.js embedded | sidecar, external |
| Runtime | Node.js | Java, Python, Go |
| Command delivery | polling | WebSocket, gRPC, queue |
| Auth | local admin | RBAC, SSO, OIDC, LDAP |
| Deployment | single node | cluster, HA |
| Observability | health only | logs, metrics, traces, alerts |
| Config | visibility | publishing, rollback, approval |
| Secrets | secretRef-ready | Vault, managed secret store |
| Cloud | none | multi-tenant SaaS |

Extension points must not make CE v0.1 heavy.

---

## 16. Explicit Non-Architecture Goals

CE v0.1 architecture should not include:

- Kubernetes as a requirement;
- service mesh;
- distributed queue;
- distributed lock;
- multi-tenant isolation;
- billing subsystem;
- full config center;
- full observability platform;
- arbitrary remote shell terminal;
- Java/Spring dependency;
- Cloud-only Agent gateway.

---

## 17. Architecture Acceptance Criteria

The architecture is acceptable when:

- each component has a clear responsibility;
- Opstage Backend is the control plane;
- Capsule Service business logic stays outside Backend;
- Agent SDK is the only CE v0.1 service onboarding path;
- UI only talks to Backend;
- Agent only talks to Backend;
- Backend stores enough state to display Agents, Services, Commands, and Audit Events;
- stale status can be calculated;
- the system runs with SQLite;
- the system can be packaged into a simple Docker deployment;
- future EE/Cloud evolution is not blocked.

---

## 18. Summary

Opstage CE architecture is a lightweight control-plane architecture.

It should prove one complete vertical slice before adding breadth:

```text
UI
    ↓
Backend
    ↓
Agent SDK
    ↓
Capsule Service
```

The most important architecture rule is:

> Keep CE simple enough to run easily, but structured enough to evolve.
