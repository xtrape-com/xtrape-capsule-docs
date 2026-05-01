<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: README.md
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

# Opstage（运维舞台） CE（社区版） 概述

- Status: 实现 Target
- Edition: CE（社区版）
- Priority: Current
- Audience: product designers, architects, backend developers, frontend developers, agent SDK developers, AI coding agents

This document 定义 the implementation overview of **Opstage（运维舞台） CE（社区版） / Community 版本**.

Opstage（运维舞台） CE（社区版） is the current implementation target of the `xtrape-capsule` project.

CE（社区版） should be lightweight, open-source, self-hosted, and practical enough to prove the core Capsule Service（胶囊服务） governance model without introducing unnecessary EE（企业版） or Cloud（云版） complexity.

---

## 1. Positioning

Opstage（运维舞台） CE（社区版） is the open-source community edition of the Capsule Service（胶囊服务） runtime governance platform.

Its purpose is to help developers and small teams manage growing numbers of lightweight services such as:

- CAPI services;
- account pool services;
- browser automation workers;
- OTP readers;
- connector services;
- session managers;
- AI agent runtimes;
- small operational workers.

CE（社区版） should solve the first real problem:

> Small services are easy to create, but hard to remember, observe, configure, audit, and operate over time.

CE（社区版） should provide a practical answer to this problem with minimal deployment cost.

---

## 2. Product Definition

Opstage（运维舞台） CE（社区版） is:

> A lightweight, self-hosted, open-source runtime governance platform for Capsule Services.

It 提供:

- a Web UI;
- a Backend control plane;
- a Node.js embedded Agent（代理） SDK;
- Agent（代理） registration;
- Capsule Service（胶囊服务） discovery through Agent（代理） reports;
- health visibility;
- config visibility;
- predefined action execution;
- command polling;
- command result tracking;
- basic audit logs;
- SQLite-first lightweight persistence;
- simple Docker-based deployment.

---

## 3. What CE（社区版） Is Not

CE（社区版） v0.1 is not:

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

CE（社区版） should remain intentionally small.

---

## 4. Current 实现 Target

The first target is **CE（社区版） v0.1 Prototype**.

CE（社区版） v0.1 should prove the following loop:

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

## 5. CE（社区版） v0.1 Scope

CE（社区版） v0.1 must implement:

- local admin login;
- default Workspace;
- registration token creation or bootstrap;
- Agent（代理） registration API;
- Agent（代理） token issuance and validation;
- Agent（代理） heartbeat;
- Capsule Service（胶囊服务） manifest report;
- latest health report;
- config metadata visibility;
- predefined action definitions;
- action request from UI;
- Command creation;
- Command polling by Agent（代理）;
- CommandResult reporting;
- Agent（代理） list UI;
- Capsule Service（胶囊服务） list UI;
- Capsule Service（胶囊服务） detail UI;
- Command list or recent command UI;
- Audit Logs UI;
- SQLite persistence;
- Docker-based local deployment;
- demo Capsule Service（胶囊服务）;
- Node.js embedded Agent（代理） SDK.

---

## 6. Out of Scope for CE（社区版） v0.1

CE（社区版） v0.1 must not implement unless explicitly added later:

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
- sidecar Agent（代理）;
- external Agent（代理）;
- Java Agent（代理） SDK;
- Python Agent（代理） SDK;
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

See ADR 0005 for the full technology stack decision. Fastify is the CE（社区版） v0.1 implementation baseline; NestJS is not in scope for CE（社区版） v0.1.

### 7.2 Database

CE（社区版） v0.1 should default to:

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
- prefer JSON/text fields for flexible metadata in CE（社区版） v0.1;
- avoid complex database-specific features.

### 7.3 UI

UI is a Web console. CE（社区版） v0.1 stack (decided by [ADR 0007](../../08-decisions/0007-ui-state-and-data-fetching.md)):

```text
Vue 3 + TypeScript + Ant Design Vue
+ TanStack Vue Query (server state)
+ Pinia (client UI state)
+ Vue Router (URL state)
+ Vee-Validate + Zod (forms)
+ Vite (build)
```

CE（社区版） UI should support responsive viewing for mobile, but it does not need to be a full mobile app.

### 7.4 Agent（代理） SDK

CE（社区版） v0.1 should ship:

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

CE（社区版） v0.1 should use:

```text
HTTP heartbeat + command polling
```

Do not implement WebSocket, gRPC, or queue-based command delivery in v0.1.

---

## 8. 部署 Model

CE（社区版） v0.1 should prioritize the simplest self-hosted deployment experience.

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

The CE（社区版） monorepo `xtrape-capsule-ce` (see [`10-implementation/00-repository-structure.md`](../../10-implementation/00-repository-structure.md)) 包含:

```text
apps/opstage-backend
apps/opstage-ui                   (Vue 3 + Ant Design Vue)
apps/demo-capsule-service
packages/db
packages/shared
packages/test-utils
```

`@xtrape/capsule-contracts-node` and `@xtrape/capsule-agent-node` come from npm (separate repos: `xtrape-capsule-contracts-node` and `xtrape-capsule-agent-node` — see [ADR 0008](../../08-decisions/0008-naming-and-repositories.md)).

The first user experience should feel simple.

---

## 9. Repository Expectations

CE（社区版） v0.1 ships across **four repositories** (see [ADR 0008 — Naming and Repositories](../../08-decisions/0008-naming-and-repositories.md) for the authoritative decision):

||Repo|版本|Purpose||
|---|---|---|
||`xtrape-capsule-docs`|shared|设计 docs, ADRs, Layer 1 contract SSOT||
||`xtrape-capsule-contracts-node`|shared|Node bindings of the contracts (Layer 2). Published as `@xtrape/capsule-contracts-node` (npm).||
||`xtrape-capsule-agent-node`|shared|Node Agent（代理） SDK. Published as `@xtrape/capsule-agent-node` (npm).||
||`xtrape-capsule-ce`|**CE（社区版）**|Backend + UI + demo + deploy (only edition-bound code repo).||

Each repository should exhibit:

- clear README;
- simple setup;
- demo service included (in `xtrape-capsule-ce/apps/demo-capsule-service`);
- Docker-based quick start (`xtrape-capsule-ce/deploy/compose/`);
- documented APIs;
- documented Agent（代理） SDK usage;
- clean project structure;
- no hidden commercial dependency;
- no required external SaaS dependency;
- safe defaults.

`xtrape-capsule-ce` monorepo internal layout (matches [`10-implementation/00-repository-structure.md`](../../10-implementation/00-repository-structure.md)):

```text
xtrape-capsule-ce/
├── apps/
│   ├── opstage-backend/
│   ├── opstage-ui/                   (Vue 3 + Ant Design Vue)
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

## 10. CE（社区版） Extension Principles

CE（社区版） should stay lightweight, but it must not block future EE（企业版） and Cloud（云版） evolution.

CE（社区版） should reserve extension points for:

- MySQL and PostgreSQL;
- multiple Workspaces;
- RBAC;
- SSO;
- sidecar Agent（代理）;
- external Agent（代理）;
- Java and Python Agent（代理） SDKs;
- centralized logs;
- metrics;
- alert rules;
- secret references;
- Cloud（云版）-hosted Backend;
- enterprise deployment.

However, these extension points should not make CE（社区版） v0.1 heavy.

The guiding rule is:

> CE（社区版） should be small but not short-sighted.

---

## 11. 安全 Requirements

CE（社区版） v0.1 must enforce the following safety rules:

- store only token hashes;
- never store raw registration tokens or Agent（代理） tokens;
- do not expose raw secrets in manifest, config, health, command, or audit payloads;
- use `secretRef` for sensitive references where possible;
- require Agent（代理） token for Agent（代理） APIs;
- reject revoked or disabled Agents;
- execute only predefined actions;
- do not provide arbitrary shell execution;
- audit important operations;
- mask sensitive UI values.

---

## 12. Required UI Pages

CE（社区版） v0.1 should provide at least:

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

CE（社区版） v0.1 Backend should include modules for:

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

CE（社区版） v0.1 must include a demo Capsule Service（胶囊服务）.

The demo should prove:

- Agent（代理） registration;
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

## 15. 开发 Order

Recommended CE（社区版） v0.1 implementation order:

1. repository structure;
2. shared types;
3. SQLite schema;
4. Backend basic server;
5. local admin authentication;
6. registration token model;
7. Agent（代理） registration API;
8. Agent（代理） heartbeat API;
9. Capsule Service（胶囊服务） report API;
10. Node.js embedded Agent（代理） SDK;
11. demo Capsule Service（胶囊服务）;
12. command creation API;
13. command polling API;
14. command result API;
15. basic audit events;
16. UI shell;
17. dashboard;
18. Agent（代理） pages;
19. Capsule Service（胶囊服务） pages;
20. command and audit pages;
21. Docker packaging;
22. quick-start documentation.

---

## 16. CE（社区版） Acceptance Criteria

CE（社区版） v0.1 is acceptable when:

- a user can start Opstage（运维舞台） CE（社区版） locally;
- a default admin can log in;
- a registration token can be created or bootstrapped;
- demo Capsule Service（胶囊服务） can register through Node.js embedded Agent（代理） SDK;
- UI shows the Agent（代理） as online;
- UI shows the demo Capsule Service（胶囊服务）;
- health status is visible;
- config metadata is visible;
- user can trigger `runHealthCheck` or `echo` action;
- Backend creates a Command;
- Agent（代理） polls and executes the Command;
- Agent（代理） reports CommandResult;
- UI shows command result;
- audit logs show the operation;
- when the Agent（代理） stops, UI eventually shows Agent（代理） offline and service stale;
- deployment can run with SQLite and Docker.

---

## 17. Documents to Read Before 实现

Before implementing CE（社区版） v0.1, read:

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

Opstage（运维舞台） CE（社区版） is the first practical implementation of the `xtrape-capsule` governance model.

It should prove that many lightweight services can be made visible, manageable, and auditable through a simple Agent（代理）-based control plane.

The most important rule is:

> Build CE（社区版） as a real usable open-source tool, not as a disabled preview of EE（企业版） or Cloud（云版）.
