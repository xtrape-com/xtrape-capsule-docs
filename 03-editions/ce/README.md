# Opstage CE Overview

- Status: Implementation Target
- Edition: CE
- Priority: Current
- Audience: product designers, architects, backend developers, frontend developers, agent SDK developers, AI coding agents

This document defines the implementation overview of **Opstage CE / Community Edition**.

Opstage CE is the current implementation target of the `xtrape-capsule` project.

CE should be lightweight, open-source, self-hosted, and practical enough to prove the core Capsule Service governance model without introducing unnecessary EE or Cloud complexity.

---

## 1. Positioning

Opstage CE is the open-source community edition of the Capsule Service runtime governance platform.

Its purpose is to help developers and small teams manage growing numbers of lightweight services such as:

- CAPI services;
- account pool services;
- browser automation workers;
- OTP readers;
- connector services;
- session managers;
- AI agent runtimes;
- small operational workers.

CE should solve the first real problem:

> Small services are easy to create, but hard to remember, observe, configure, audit, and operate over time.

CE should provide a practical answer to this problem with minimal deployment cost.

---

## 2. Product Definition

Opstage CE is:

> A lightweight, self-hosted, open-source runtime governance platform for Capsule Services.

It provides:

- a Web UI;
- a Backend control plane;
- a Node.js embedded Agent SDK;
- Agent registration;
- Capsule Service discovery through Agent reports;
- health visibility;
- config visibility;
- predefined action execution;
- command polling;
- command result tracking;
- basic audit logs;
- SQLite-first lightweight persistence;
- simple Docker-based deployment.

---

## 3. What CE Is Not

CE v0.1 is not:

- a full enterprise operations platform;
- a full configuration center like Nacos or Apollo;
- a full observability platform;
- a log analysis platform;
- a Kubernetes platform;
- a service mesh;
- a multi-tenant SaaS control plane;
- an enterprise RBAC and SSO platform;
- a billing system;
- a remote shell execution platform.

CE should remain intentionally small.

---

## 4. Current Implementation Target

The first target is **CE v0.1 Prototype**.

CE v0.1 should prove the following loop:

```text
Node.js Capsule Service
    ↓ embedded Agent SDK
Opstage Backend
    ↓
Opstage UI
```

Minimum working flow:

```text
Agent starts
    ↓
Agent registers with registration token
    ↓
Backend issues Agent token
    ↓
Agent reports Capsule Service manifest
    ↓
Agent sends heartbeat and health
    ↓
UI shows Agent and Capsule Service status
    ↓
User triggers predefined action
    ↓
Backend creates Command
    ↓
Agent polls Command
    ↓
Agent executes local action handler
    ↓
Agent reports CommandResult
    ↓
UI shows result and audit trail
```

---

## 5. CE v0.1 Scope

CE v0.1 must implement:

- local admin login;
- default Workspace;
- registration token creation or bootstrap;
- Agent registration API;
- Agent token issuance and validation;
- Agent heartbeat;
- Capsule Service manifest report;
- latest health report;
- config metadata visibility;
- predefined action definitions;
- action request from UI;
- Command creation;
- Command polling by Agent;
- CommandResult reporting;
- Agent list UI;
- Capsule Service list UI;
- Capsule Service detail UI;
- Command list or recent command UI;
- Audit Logs UI;
- SQLite persistence;
- Docker-based local deployment;
- demo Capsule Service;
- Node.js embedded Agent SDK.

---

## 6. Out of Scope for CE v0.1

CE v0.1 must not implement unless explicitly added later:

- multi-tenant model;
- billing;
- SSO / OIDC / LDAP;
- full RBAC;
- Kubernetes deployment;
- high availability;
- distributed queues;
- WebSocket command channel;
- gRPC streaming;
- centralized log collection;
- metrics dashboard;
- alert rules;
- secret vault integration;
- config publishing workflow;
- config approval workflow;
- config rollback;
- sidecar Agent;
- external Agent;
- Java Agent SDK;
- Python Agent SDK;
- arbitrary shell execution.

---

## 7. Technical Constraints

### 7.1 Backend

Backend should use:

```text
Node.js + TypeScript
```

Recommended implementation options:

```text
NestJS + Prisma
```

or a lighter alternative:

```text
Fastify + TypeScript + Prisma
```

Current preferred direction:

```text
Fastify + TypeScript + Prisma
```

See ADR 0005 for the full technology stack decision. Fastify is the CE v0.1 implementation baseline; NestJS is not in scope for CE v0.1.

### 7.2 Database

CE v0.1 should default to:

```text
SQLite
```

Future storage should reserve extension points for:

```text
MySQL
PostgreSQL
```

Rules:

- do not use SQLite-only assumptions in domain model;
- keep schema portable where practical;
- prefer JSON/text fields for flexible metadata in CE v0.1;
- avoid complex database-specific features.

### 7.3 UI

UI is a Web console. CE v0.1 stack (decided by [ADR 0007](../../08-decisions/0007-ui-state-and-data-fetching.md)):

```text
React 18 + TypeScript + Ant Design (antd 5.x)
+ TanStack React Query (server state)
+ React Router 7.x (URL state)
+ Vite (build)
```

CE UI should support responsive viewing for mobile, but it does not need to be a full mobile app.

### 7.4 Agent SDK

CE v0.1 should ship:

```text
Node.js Embedded Agent SDK
```

The SDK should support:

- registration;
- heartbeat;
- manifest reporting;
- health provider;
- config provider;
- action definitions;
- action handlers;
- command polling;
- command result reporting.

### 7.5 Communication

CE v0.1 should use:

```text
HTTP heartbeat + command polling
```

Do not implement WebSocket, gRPC, or queue-based command delivery in v0.1.

---

## 8. Deployment Model

CE v0.1 should prioritize the simplest self-hosted deployment experience.

Preferred user-facing deployment:

```text
single container
single exposed port
SQLite data volume
```

Recommended target:

```bash
docker run -p 8080:8080 -v ./data:/app/data ghcr.io/xtrape/opstage-ce:v0.1.0
```

The CE monorepo `xtrape-capsule-ce` (see [`10-implementation/00-repository-structure.md`](../../10-implementation/00-repository-structure.md)) contains:

```text
apps/opstage-backend
apps/opstage-ui                   (React 18 + Ant Design)
apps/demo-capsule-service
packages/db
packages/shared
packages/test-utils
```

`@xtrape/capsule-contracts-node` and `@xtrape/capsule-agent-node` come from npm (separate repos: `xtrape-capsule-contracts-node` and `xtrape-capsule-agent-node` — see [ADR 0008](../../08-decisions/0008-naming-and-repositories.md)).

The first user experience should feel simple.

---

## 9. Repository Expectations

CE v0.1 ships across **four repositories** (see [ADR 0008 — Naming and Repositories](../../08-decisions/0008-naming-and-repositories.md) for the authoritative decision):

| Repo | Edition | Purpose |
|---|---|---|
| `xtrape-capsule-docs` | shared | Design docs, ADRs, Layer 1 contract SSOT |
| `xtrape-capsule-contracts-node` | shared | Node bindings of the contracts (Layer 2). Published as `@xtrape/capsule-contracts-node` (npm). |
| `xtrape-capsule-agent-node` | shared | Node Agent SDK. Published as `@xtrape/capsule-agent-node` (npm). |
| `xtrape-capsule-ce` | **CE** | Backend + UI + demo + deploy (only edition-bound code repo). |

Each repository should exhibit:

- clear README;
- simple setup;
- demo service included (in `xtrape-capsule-ce/apps/demo-capsule-service`);
- Docker-based quick start (`xtrape-capsule-ce/deploy/compose/`);
- documented APIs;
- documented Agent SDK usage;
- clean project structure;
- no hidden commercial dependency;
- no required external SaaS dependency;
- safe defaults.

`xtrape-capsule-ce` monorepo internal layout (matches [`10-implementation/00-repository-structure.md`](../../10-implementation/00-repository-structure.md)):

```text
xtrape-capsule-ce/
├── apps/
│   ├── opstage-backend/
│   ├── opstage-ui/                   (React 18 + Ant Design)
│   └── demo-capsule-service/
├── packages/
│   ├── db/
│   ├── shared/
│   └── test-utils/
├── deploy/
└── README.md
```

There is **no** `packages/contracts/` and **no** `packages/agent-node/` here — both come from npm.

---

## 10. CE Extension Principles

CE should stay lightweight, but it must not block future EE and Cloud evolution.

CE should reserve extension points for:

- MySQL and PostgreSQL;
- multiple Workspaces;
- RBAC;
- SSO;
- sidecar Agent;
- external Agent;
- Java and Python Agent SDKs;
- centralized logs;
- metrics;
- alert rules;
- secret references;
- Cloud-hosted Backend;
- enterprise deployment.

However, these extension points should not make CE v0.1 heavy.

The guiding rule is:

> CE should be small but not short-sighted.

---

## 11. Security Requirements

CE v0.1 must enforce the following safety rules:

- store only token hashes;
- never store raw registration tokens or Agent tokens;
- do not expose raw secrets in manifest, config, health, command, or audit payloads;
- use `secretRef` for sensitive references where possible;
- require Agent token for Agent APIs;
- reject revoked or disabled Agents;
- execute only predefined actions;
- do not provide arbitrary shell execution;
- audit important operations;
- mask sensitive UI values.

---

## 12. Required UI Pages

CE v0.1 should provide at least:

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

Minimum service detail tabs:

```text
Overview
Manifest
Health
Configs
Actions
Commands
Audit
```

The UI should make stale status visible.

Example:

```text
Current: Stale
Last reported: Online
Reason: Agent offline
```

---

## 13. Required Backend Modules

CE v0.1 Backend should include modules for:

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

The implementation may combine some modules internally, but the conceptual boundaries should remain clear.

---

## 14. Required Demo

CE v0.1 must include a demo Capsule Service.

The demo should prove:

- Agent registration;
- manifest reporting;
- heartbeat;
- health reporting;
- config visibility;
- predefined action execution;
- command polling;
- command result reporting;
- audit trail.

Required demo actions:

```text
runHealthCheck
echo
```

Required demo config:

```text
demo.message
```

---

## 15. Development Order

Recommended CE v0.1 implementation order:

1. repository structure;
2. shared types;
3. SQLite schema;
4. Backend basic server;
5. local admin authentication;
6. registration token model;
7. Agent registration API;
8. Agent heartbeat API;
9. Capsule Service report API;
10. Node.js embedded Agent SDK;
11. demo Capsule Service;
12. command creation API;
13. command polling API;
14. command result API;
15. basic audit events;
16. UI shell;
17. dashboard;
18. Agent pages;
19. Capsule Service pages;
20. command and audit pages;
21. Docker packaging;
22. quick-start documentation.

---

## 16. CE Acceptance Criteria

CE v0.1 is acceptable when:

- a user can start Opstage CE locally;
- a default admin can log in;
- a registration token can be created or bootstrapped;
- demo Capsule Service can register through Node.js embedded Agent SDK;
- UI shows the Agent as online;
- UI shows the demo Capsule Service;
- health status is visible;
- config metadata is visible;
- user can trigger `runHealthCheck` or `echo` action;
- Backend creates a Command;
- Agent polls and executes the Command;
- Agent reports CommandResult;
- UI shows command result;
- audit logs show the operation;
- when the Agent stops, UI eventually shows Agent offline and service stale;
- deployment can run with SQLite and Docker.

---

## 17. Documents to Read Before Implementation

Before implementing CE v0.1, read:

```text
README.md
08-decisions/README.md
08-decisions/0001-ce-v01-implementation-baseline.md
08-decisions/0002-api-namespace-convention.md
08-decisions/0003-command-action-lifecycle.md
08-decisions/0004-security-defaults.md
08-decisions/0005-technology-stack-decision.md
08-decisions/0006-logging-and-observability.md
08-decisions/0007-ui-state-and-data-fetching.md
08-decisions/0008-naming-and-repositories.md
08-decisions/0009-contracts-spec-and-bindings.md
09-contracts/README.md
09-contracts/errors.json
09-contracts/errors.md
09-contracts/enums/status-enums.json
09-contracts/enums/audit-actions.json
09-contracts/enums/id-prefixes.json
09-contracts/openapi/opstage-ce-v0.1.yaml
09-contracts/prisma/schema.prisma
09-contracts/prisma/prisma.config.ts
10-implementation/README.md
10-implementation/00-repository-structure.md
10-implementation/01-backend-scaffold-plan.md
10-implementation/02-ui-scaffold-plan.md
10-implementation/03-agent-sdk-scaffold-plan.md
10-implementation/04-demo-service-plan.md
10-implementation/05-implementation-sequence.md
10-implementation/06-ci-cd-pipelines.md
10-implementation/07-quickstart.md
10-implementation/08-supply-chain.md
01-capsule/00-overview.md
01-capsule/01-capsule-service-concept.md
01-capsule/03-domain-model.md
01-capsule/04-design-principles.md
02-specs/README.md
02-specs/01-capsule-manifest-spec.md
02-specs/02-capsule-management-contract.md
02-specs/03-agent-registration-spec.md
02-specs/04-health-spec.md
02-specs/05-action-spec.md
02-specs/06-config-spec.md
02-specs/07-command-spec.md
02-specs/08-audit-event-spec.md
02-specs/09-status-model-spec.md
03-editions/ce/01-ce-scope.md
03-editions/ce/02-ce-mvp.md
03-editions/ce/03-ce-architecture.md
03-editions/ce/04-ce-technology-stack.md
03-editions/ce/12-ce-extension-points.md
03-editions/ce/13-ce-v01-implementation-checklist.md
```

---

## 18. Summary

Opstage CE is the first practical implementation of the `xtrape-capsule` governance model.

It should prove that many lightweight services can be made visible, manageable, and auditable through a simple Agent-based control plane.

The most important rule is:

> Build CE as a real usable open-source tool, not as a disabled preview of EE or Cloud.
