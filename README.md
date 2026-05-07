---
status: implemented
audience: ai-coding-agents
stability: stable
last_reviewed: 2026-05-05
canonical_language: en
repository_role: private-design-source-of-truth
---

# xtrape-capsule Design Documentation

> **Status:** Private design documentation and implementation guidance  
> **Audience:** founders, architects, maintainers, and AI coding agents  
> **Public documentation:** `xtrape-capsule-site`  
> **Stability:** Documents may include drafts, accepted decisions, implementation notes, roadmap ideas, and commercial planning. Public-facing content must be extracted and rewritten before being published.

This repository is the private design knowledge base for the Xtrape Capsule product family.

It contains architecture notes, ADRs, specification drafts, implementation guidance, internal planning materials, and AI coding agent context.

For public-facing product documentation, quick start guides, SDK guides, and product positioning, use `xtrape-capsule-site`.

English documents are canonical unless a document explicitly states otherwise. Chinese translation files marked as draft or machine-assisted are not authoritative.

## Repository Role

- **Private source of design truth:** architecture, ADRs, specs, implementation guidance, internal planning.
- **Not public product narrative:** do not copy private text directly into public docs.
- **Public extraction target:** stable, approved content should be rewritten into `xtrape-capsule-site` using `PUBLIC_EXTRACTION_GUIDE.md`.
- **AI coding context:** coding agents should start with `AI_READING_GUIDE.md` and follow the authority order defined there.


## Maintenance Guides

- `AI_READING_GUIDE.md` — authority order and required reading for AI coding agents.
- `PUBLIC_EXTRACTION_GUIDE.md` — safe process for rewriting private content into public docs.
- `SENSITIVE_CONTENT_CHECKLIST.md` — scan terms and review checklist before public extraction.
- `REPO_MAP.md` — directory roles and authority map.
- `DOCS_MAINTENANCE.md` — formatting, metadata, and link-check guidance.

## 1. Current Focus

The current implementation focus is:

```text
CE v0.1 / Community Edition Prototype
```

CE v0.1 should deliver a lightweight, open-source, self-hosted prototype that proves the core Capsule governance loop:

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

CE v0.1 should use:

- Opstage Backend;
- Opstage UI;
- SQLite persistence;
- local admin authentication;
- Node.js Embedded Agent SDK;
- Node.js demo Capsule Service;
- simple Docker or Docker Compose deployment.

EE and Cloud are future tracks. They should guide extension-point design, but they must not expand the CE v0.1 implementation scope.

## Current Planning Tracks

Implementation focus:

- `v0.1 Public Review / Public Preview readiness`

Near-term planning:

- `v0.2 Developer Experience & Runtime Maturity`

Future roadmap:

- `v0.3 Capsule Events and Capability Metadata`
- `v0.4 Capsule Bus Experimental`
- `v0.5 Capsule Catalog`
- `v0.6 Capsule Registry`
- `v0.7 Private Capsule Marketplace`
- `v1.0 CE Stable and Ecosystem Foundation`

These future roadmap items should guide extension-point design, but must not expand the current v0.1/v0.2 implementation scope unless explicitly promoted into an implementation issue.

---

## 2. Documentation Structure

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

Each directory has its own `README.md` that defines the local reading order and implementation relevance.

---

## 3. Directory Guide

### 3.1 `01-capsule/`

Defines the core domain concepts:

- Capsule Service overview;
- Capsule Service concept;
- Capsule Service vs. microservice;
- domain model;
- design principles.

Read this first to understand what a Capsule Service is and why Opstage governs it through Agents.

### 3.2 `02-specs/`

Defines shared cross-edition specifications:

- Capsule Manifest;
- Capsule Management Contract;
- Agent Registration;
- Health;
- Action;
- Config;
- Command;
- AuditEvent;
- Status Model.

These specifications should remain stable across CE, EE, and Cloud. CE v0.1 may implement only the required subset, but
it should not introduce concepts that conflict with the long-term specs.

### 3.3 `03-editions/`

Defines edition boundaries:

```text
03-editions/ce/      current implementation target
03-editions/ee/      future private enterprise edition
03-editions/cloud/   future hosted SaaS edition
```

Only CE documents marked as implementation target should be treated as current development requirements.

### 3.4 `04-opstage/`

Defines the Opstage runtime governance subsystem:

- Opstage overview;
- UI;
- Backend;
- Agent integration;
- Command and Action model;
- Audit model;
- Observability roadmap.

Opstage is the first concrete governance platform for Capsule Services.

### 3.5 `05-agents/`

Defines the Agent system:

- Agent overview;
- Embedded Agent;
- future Sidecar Agent;
- future External Agent;
- Node Agent SDK;
- Agent permission model.

CE v0.1 focuses only on the Node.js Embedded Agent SDK.

### 3.6 `06-runtimes/`

Defines runtime integration:

- runtime overview;
- Node.js Runtime as the CE implementation target;
- Java Runtime planning;
- Python Runtime planning.

CE v0.1 focuses only on Node.js. Java and Python are future planning tracks.

### 3.7 `07-roadmap/`

Defines product and engineering sequencing:

- version roadmap;
- CE roadmap;
- EE roadmap;
- Cloud roadmap.

Use this section to avoid mixing current CE requirements with future commercialization plans.

### 3.8 `08-decisions/`

Defines accepted architecture and product decisions:

- CE v0.1 implementation baseline;
- API namespace convention;
- Command and Action lifecycle;
- security defaults;
- technology stack decision.

Accepted decision records should be treated as current implementation constraints when older documents still contain conflicting planning details.

### 3.9 `09-contracts/`

Defines CE v0.1 implementation contracts:

- OpenAPI contract for Admin, Agent, and System APIs;
- Prisma schema baseline for persistence;
- contract priority rules for implementation.

Use this section when building Backend, UI API clients, Agent SDK clients, tests, and database migrations.


### 3.10 `10-implementation/`

Defines CE v0.1 implementation planning:

- monorepo structure;
- Backend scaffold plan;
- UI scaffold plan;
- Node Agent SDK scaffold plan;
- demo Capsule Service plan;
- implementation sequence.

Use this section after ADRs and contracts are accepted, when starting implementation work.

---

## 4. CE v0.1 Implementation Target

CE v0.1 should include:

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

CE v0.1 should be useful as open source. It should not be an intentionally crippled trial.

---

## 5. CE v0.1 Non-Goals

CE v0.1 should not implement:

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

## 6. Development Rules

### 6.1 Build CE first

Current development should serve CE v0.1 unless a document explicitly marks a feature as current scope.

### 6.2 Keep CE lightweight

CE v0.1 should prefer:

- SQLite by default;
- local admin authentication;
- HTTP heartbeat;
- command polling;
- Node.js Embedded Agent SDK;
- single default Workspace;
- single-node deployment;
- basic AuditEvents;
- basic governance visibility.

Avoid Kubernetes, distributed queues, full observability stacks, enterprise RBAC, SSO, tenancy, and billing in CE v0.1.

### 6.3 Reserve extension points without implementing future systems

CE should reserve low-cost extension fields and concepts such as:

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

### 6.4 Use Agent-based governance

Opstage should not directly control arbitrary services.

Capsule Services enter governance through registered, authenticated Agents.

CE v0.1 actual flow:

```text
Node.js Capsule Service
    ↓ Node.js Embedded Agent SDK
Opstage Backend
    ↓ Admin API
Opstage UI
```

### 6.5 Execute only predefined actions

Operations must be modeled as predefined actions, durable Commands, CommandResults, and AuditEvents.

CE v0.1 must not provide remote shell or arbitrary script execution.

### 6.6 Protect secrets

Opstage should store governance metadata, not raw secrets by default.

Use:

```text
secretRef
masked values
sanitized summaries
```

Do not log or store raw registration tokens, Agent tokens, passwords, cookies, OAuth tokens, API keys, private keys, or browser sessions.

---

## 7. Recommended Reading Path for CE v0.1

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

## 8. Edition Status

| Edition | Status | Purpose |
|---|---|---|
| CE | Current implementation target | Lightweight open-source self-hosted edition |
| EE | Future planning | Private enterprise commercial edition |
| Cloud | Future planning | Hosted SaaS edition |

---

## 9. First Milestone

The first milestone is:

```text
CE v0.1 Prototype
```

It should demonstrate:

- local Opstage startup;
- local admin login;
- registration token creation;
- Node.js demo service registration;
- Agent heartbeat;
- Capsule Service visibility;
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

This documentation set should guide implementation toward a small, useful, safe, and extensible CE v0.1 first.

The most important repository-level rule is:

> Build the CE governance kernel first, keep future EE and Cloud as extension tracks, and preserve the Agent-based, predefined-action, secretRef-safe model across all editions.
