<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: README.md
翻译状态 / Translation Status: 已翻译 / Translated
生成时间 / Generated: 2026-05-01 09:28:55
================================================================================
注意 / Notes:
- 技术术语如 Capsule Service、Agent、Opstage 等保留英文或采用中英对照
- 代码块中的内容不翻译
- 文件路径和 URL 不翻译
- 保持原有的 Markdown 格式结构
================================================================================
-->

# xtrape-capsule 文档

- Status: 实施指南
- Edition: 共享
- Priority: 高
- Audience: founders, architects, product designers, backend developers, frontend developers, agent SDK developers, AI coding agents

This repository 包含 the documentation set for the `xtrape-capsule` product family.

`xtrape-capsule` 定义 the lightweight Capsule Service（胶囊服务） architecture domain in the Xtrape ecosystem. It 涵盖 the Capsule Service（胶囊服务） concept, shared specifications, edition boundaries, Opstage（运维舞台） runtime governance, Agent（代理） integration, runtime support, and the CE（社区版）/EE（企业版）/Cloud（云版） roadmap.

This documentation is for the whole `xtrape-capsule` domain, not only for `xtrape-capsule-opstage`. Opstage（运维舞台） is the first major runtime governance subsystem under this domain.

---

## 1. Current Focus

The current implementation focus is:

```text
CE v0.1 / Community Edition Prototype
```

CE（社区版） v0.1 should deliver a lightweight, open-source, self-hosted prototype that proves the core Capsule governance loop:

```text
Agent registration
    ↓
Service report
    ↓
Heartbeat and health
    ↓
Config visibility
    ↓
Predefined action request
    ↓
Command polling
    ↓
Command result
    ↓
Audit log
```

CE（社区版） v0.1 should use:

- Opstage（运维舞台） Backend;
- Opstage（运维舞台） UI;
- SQLite persistence;
- local admin authentication;
- Node.js Embedded Agent（代理） SDK;
- Node.js demo Capsule Service（胶囊服务）;
- simple Docker or Docker Compose deployment.

EE（企业版） and Cloud（云版） are future tracks. They should guide extension-point design, but they must not expand the CE（社区版） v0.1 implementation scope.

---

## 2. 文档 Structure

Recommended reading order:

```text
xtrape-capsule-docs/
├── README.md
├── 01-capsule/
├── 02-specs/
├── 03-editions/
├── 04-opstage/
├── 05-agents/
├── 06-runtimes/
├── 07-roadmap/
├── 08-decisions/
├── 09-contracts/
└── 10-implementation/
```

Each directory has its own `README.md` that 定义 the local reading order and implementation relevance.

---

## 3. Directory Guide

### 3.1 `01-capsule/`

Defines the core domain concepts:

- Capsule Service（胶囊服务） overview;
- Capsule Service（胶囊服务） concept;
- Capsule Service（胶囊服务） vs. microservice;
- domain model;
- design principles.

Read this first to understand what a Capsule Service（胶囊服务） is and why Opstage（运维舞台） governs it through Agents.

### 3.2 `02-specs/`

Defines shared cross-edition specifications:

- Capsule Manifest;
- Capsule Management Contract;
- Agent（代理） Registration;
- Health;
- Action;
- Config;
- Command;
- AuditEvent;
- 状态 Model.

These specifications should remain stable across CE（社区版）, EE（企业版）, and Cloud（云版）. CE（社区版） v0.1 may implement only the required subset, but it should not introduce concepts that conflict with the long-term specs.

### 3.3 `03-editions/`

Defines edition boundaries:

```text
03-editions/ce/      current implementation target
03-editions/ee/      future private enterprise edition
03-editions/cloud/   future hosted SaaS edition
```

Only CE（社区版） documents marked as implementation target should be treated as current development requirements.

### 3.4 `04-opstage/`

Defines the Opstage（运维舞台） runtime governance subsystem:

- Opstage（运维舞台） overview;
- UI;
- Backend;
- Agent（代理） integration;
- Command and Action model;
- Audit model;
- Observability roadmap.

Opstage（运维舞台） is the first concrete governance platform for Capsule Services.

### 3.5 `05-agents/`

Defines the Agent（代理） system:

- Agent（代理） overview;
- Embedded Agent（代理）;
- future Sidecar Agent（代理）;
- future External Agent（代理）;
- Node Agent（代理） SDK;
- Agent（代理） permission model.

CE（社区版） v0.1 focuses only on the Node.js Embedded Agent（代理） SDK.

### 3.6 `06-runtimes/`

Defines runtime integration:

- runtime overview;
- Node.js Runtime as the CE（社区版） implementation target;
- Java Runtime planning;
- Python Runtime planning.

CE（社区版） v0.1 focuses only on Node.js. Java and Python are future planning tracks.

### 3.7 `07-roadmap/`

Defines product and engineering sequencing:

- version roadmap;
- CE（社区版） roadmap;
- EE（企业版） roadmap;
- Cloud（云版） roadmap.

Use this section to avoid mixing current CE（社区版） requirements with future commercialization plans.

### 3.8 `08-decisions/`

Defines accepted architecture and product decisions:

- CE（社区版） v0.1 implementation baseline;
- API namespace convention;
- Command and Action lifecycle;
- security defaults;
- technology stack decision.

Accepted decision records should be treated as current implementation constraints when older documents still contain conflicting planning details.

### 3.9 `09-contracts/`

Defines CE（社区版） v0.1 implementation contracts:

- OpenAPI contract for Admin, Agent（代理）, and System APIs;
- Prisma schema baseline for persistence;
- contract priority rules for implementation.

Use this section when building Backend, UI API clients, Agent（代理） SDK clients, tests, and database migrations.

### 3.10 `10-implementation/`

Defines CE（社区版） v0.1 implementation planning:

- monorepo structure;
- Backend scaffold plan;
- UI scaffold plan;
- Node Agent（代理） SDK scaffold plan;
- demo Capsule Service（胶囊服务） plan;
- implementation sequence.

Use this section after ADRs and contracts are accepted, when starting implementation work.

---

## 4. CE（社区版） v0.1 实现 Target

CE（社区版） v0.1 should include:

```text
Opstage Backend
Opstage UI
SQLite persistence
local admin login
registration token
Agent token authentication
Node.js Embedded Agent SDK
Node.js demo Capsule Service
Agent heartbeat
service manifest report
health report
config metadata visibility
predefined action metadata
action request from UI
Command creation
command polling
CommandResult reporting
basic AuditEvents
Dashboard summary
System health endpoint
Docker quick start
```

CE（社区版） v0.1 should be useful as open source. It should not be an intentionally crippled trial.

---

## 5. CE（社区版） v0.1 Non-Goals

CE（社区版） v0.1 should not implement:

```text
Tenant system
Organization system
billing
subscription
usage metering
enterprise RBAC
SSO / OIDC / LDAP / SAML
PostgreSQL/MySQL requirement
Redis requirement
Queue requirement
Kubernetes requirement
Agent Gateway
Sidecar Agent
External Agent
Java Agent SDK
Python Agent SDK
Go Agent SDK
full observability platform
alert rule engine
secret vault
license enforcement
remote shell
arbitrary script execution
```

These are future roadmap items or intentionally excluded from the first implementation.

---

## 6. 开发 Rules

### 6.1 Build CE（社区版） first

Current development should serve CE（社区版） v0.1 unless a document explicitly marks a feature as current scope.

### 6.2 Keep CE（社区版） lightweight

CE（社区版） v0.1 should prefer:

- SQLite by default;
- local admin authentication;
- HTTP heartbeat;
- command polling;
- Node.js Embedded Agent（代理） SDK;
- single default Workspace;
- single-node deployment;
- basic AuditEvents;
- basic governance visibility.

Avoid Kubernetes, distributed queues, full observability stacks, enterprise RBAC, SSO, tenancy, and billing in CE（社区版） v0.1.

### 6.3 Reserve extension points without implementing future systems

CE（社区版） should reserve low-cost extension fields and concepts such as:

```text
workspaceId
agentMode
runtime
protocolVersion
capabilities
metadataJson
secretRef
CommandType
AuditEvent actor/resource fields
```

The rule is:

```text
Reserve shape, not scope.
```

### 6.4 Use Agent（代理）-based governance

Opstage（运维舞台） should not directly control arbitrary services.

Capsule Services enter governance through registered, authenticated Agents.

CE（社区版） v0.1 actual flow:

```text
Node.js Capsule Service
    ↓ Node.js Embedded Agent SDK
Opstage Backend
    ↓ Admin API
Opstage UI
```

### 6.5 Execute only predefined actions

Operations must be modeled as predefined actions, durable Commands, CommandResults, and AuditEvents.

CE（社区版） v0.1 must not provide remote shell or arbitrary script execution.

### 6.6 Protect secrets

Opstage（运维舞台） should store governance metadata, not raw secrets by default.

Use:

```text
secretRef
masked values
sanitized summaries
```

Do not log or store raw registration tokens, Agent（代理） tokens, passwords, cookies, OAuth tokens, API keys, private keys, or browser sessions.

---

## 7. Recommended Reading Path for CE（社区版） v0.1

Recommended path for developers and AI coding agents:

```text
README.md
01-capsule/README.md if present, otherwise 01-capsule/00-overview.md
01-capsule/01-capsule-service-concept.md
08-decisions/README.md
08-decisions/0001-ce-v01-implementation-baseline.md
08-decisions/0002-api-namespace-convention.md
08-decisions/0003-command-action-lifecycle.md
08-decisions/0004-security-defaults.md
08-decisions/0005-technology-stack-decision.md
09-contracts/README.md
09-contracts/openapi/opstage-ce-v0.1.yaml
09-contracts/prisma/schema.prisma
09-contracts/prisma/prisma.config.ts
10-implementation/README.md
10-implementation/00-repository-structure.md
10-implementation/05-implementation-sequence.md
02-specs/README.md
02-specs/03-agent-registration-spec.md
02-specs/07-command-spec.md
03-editions/README.md
03-editions/ce/README.md
03-editions/ce/01-ce-scope.md
03-editions/ce/02-ce-mvp.md
03-editions/ce/03-ce-architecture.md
03-editions/ce/13-ce-v01-implementation-checklist.md
04-opstage/README.md
04-opstage/02-opstage-backend.md
04-opstage/01-opstage-ui.md
04-opstage/04-command-and-action-model.md
05-agents/README.md
05-agents/04-node-agent-sdk.md
05-agents/05-agent-permission-model.md
06-runtimes/README.md
06-runtimes/01-node-runtime.md
07-roadmap/README.md
07-roadmap/01-ce-roadmap.md
```

---

## 8. 版本 状态

||版本|状态|Purpose||
|---|---|---|
||CE（社区版）|Current implementation target|Lightweight open-source self-hosted edition||
||EE（企业版）|Future planning|Private enterprise commercial edition||
||Cloud（云版）|Future planning|Hosted SaaS edition||

---

## 9. First Milestone

The first milestone is:

```text
CE v0.1 Prototype
```

It should demonstrate:

- local Opstage（运维舞台） startup;
- local admin login;
- registration token creation;
- Node.js demo service registration;
- Agent（代理） heartbeat;
- Capsule Service（胶囊服务） visibility;
- health visibility;
- config metadata visibility;
- predefined action visibility;
- `echo` action execution;
- `runHealthCheck` action execution;
- CommandResult visibility;
- AuditEvent visibility;
- Docker quick start.

---

## 10. Summary

This documentation set should guide implementation toward a small, useful, safe, and extensible CE（社区版） v0.1 first.

The most important repository-level rule is:

> Build the CE（社区版） governance kernel first, keep future EE（企业版） and Cloud（云版） as extension tracks, and preserve the Agent（代理）-based, predefined-action, secretRef-safe model across all editions.
