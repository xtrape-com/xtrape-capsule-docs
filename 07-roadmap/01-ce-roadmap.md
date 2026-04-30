# CE Roadmap

- Status: Draft
- Edition: Shared
- Priority: Medium

## Roadmap Principle

- 先完成 CE v0.1：轻量、开源、单镜像、SQLite、Node Embedded Agent。
- 再稳定 Capsule Spec 和 Agent Model。
- 后续扩展 Sidecar/External Agent。
- EE 和 Cloud 在 CE 稳定后作为商业化路线推进。

# CE Roadmap

- Status: Implementation Guidance
- Edition: CE
- Priority: High
- Audience: founders, architects, product managers, backend developers, frontend developers, agent SDK developers, AI coding agents

This document defines the roadmap for **Opstage CE / Community Edition**.

CE is the open-source, lightweight, self-hosted edition of the `xtrape-capsule` product family. It is the current implementation focus.

The first CE milestone is **CE v0.1**. CE v0.1 should prove the complete Capsule governance loop with Opstage Backend, Opstage UI, SQLite, and the Node.js Embedded Agent SDK.

EE and Cloud are future tracks. They may influence extension-point design, but they must not expand CE v0.1 implementation scope.

---

## 1. Purpose

The purpose of the CE roadmap is to define:

- what CE should deliver first;
- what CE v0.1 must include;
- what CE v0.1 must not include;
- how CE should evolve after v0.1;
- how CE should remain genuinely useful as open source;
- where CE should reserve extension points for EE and Cloud;
- how to avoid early scope creep.

The key rule is:

> CE must first prove the smallest complete governance loop before adding enterprise, Cloud, multi-runtime, or advanced observability features.

---

## 2. CE Product Positioning

CE is:

> A lightweight open-source runtime governance platform for Capsule Services.

CE should be:

- open-source;
- self-hosted;
- single-node friendly;
- easy to run locally;
- SQLite-first;
- Node.js Agent-first;
- safe by default;
- useful without EE or Cloud;
- simple enough for small teams and individual developers.

CE should not feel like a broken trial of EE.

---

## 3. CE Governance Kernel

The CE governance kernel is:

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

CE v0.1 should prove this kernel end to end.

All later CE improvements should strengthen this kernel, not distract from it.

---

## 4. CE v0.1 Goal

CE v0.1 goal:

> Deliver a working local prototype that demonstrates UI + Backend + Node Embedded Agent + demo Capsule Service from registration to audited action execution.

CE v0.1 should be optimized for:

- validation;
- demo;
- developer feedback;
- architecture verification;
- first open-source release;
- future implementation guidance.

CE v0.1 does not need to be enterprise-ready.

---

## 5. CE v0.1 Scope

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
single-container or simple Docker deployment
Docker Compose quick start
```

This is the implementation target.

---

## 6. CE v0.1 Non-Goals

CE v0.1 must not include:

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
Host Agent
Kubernetes Agent
Java Agent SDK
Python Agent SDK
Go Agent SDK
full observability platform
centralized log collection
metrics database
alert rule engine
secret vault
license enforcement
remote shell
arbitrary script execution
workflow designer
plugin marketplace
```

These are future roadmap items or out of scope.

---

## 7. CE v0.1 Architecture

Recommended CE v0.1 architecture:

```text
Browser
  ↓
Opstage UI
  ↓ Admin API
Opstage Backend
  ↓ SQLite
Local database file

Node.js Capsule Service
  ↓ embedded SDK outbound HTTP
Opstage Backend Agent API
```

Recommended deployment shape:

```text
single Opstage container
    ├── Backend API
    ├── built UI static files
    └── SQLite data volume

Node.js demo Capsule Service container
    └── Node Embedded Agent SDK
```

CE v0.1 should prefer fewer moving parts.

---

## 8. CE v0.1 Backend Scope

Backend should implement:

- project scaffold;
- API server;
- SQLite persistence;
- schema and migrations;
- local admin user;
- login/logout/session or token handling;
- registration token creation;
- Agent registration;
- Agent token hash storage;
- Agent authentication middleware;
- heartbeat API;
- service report API;
- command polling API;
- CommandResult API;
- Admin APIs for UI;
- AuditEvent creation;
- status and freshness calculation;
- system health endpoint;
- sensitive value sanitization;
- structured errors.

Backend should not implement EE/Cloud systems in v0.1.

---

## 9. CE v0.1 UI Scope

UI should implement:

- Login page;
- Dashboard page;
- Agents list;
- Agent detail;
- Capsule Services list;
- Capsule Service detail;
- Manifest viewer;
- Health viewer;
- Config metadata viewer;
- Actions tab;
- Command list;
- Command detail;
- Audit Logs page;
- System Settings page;
- registration token creation;
- sensitive value masking;
- stale/offline status display.

UI should be simple and table/detail-page oriented.

CE v0.1 UI should not show disabled EE/Cloud-only menus.

---

## 10. CE v0.1 Agent Scope

Agent scope is limited to:

```text
Node.js Embedded Agent SDK
```

The SDK should implement:

- configuration from code and environment variables;
- file-based Agent token store;
- registration with registration token;
- Agent token reuse;
- heartbeat loop;
- manifest report;
- health provider;
- config provider;
- action registry;
- command polling loop;
- action execution;
- CommandResult reporting;
- retry/backoff;
- sanitized logging;
- safe Backend downtime behavior.

No Sidecar or External Agent in CE v0.1.

---

## 11. CE v0.1 Demo Capsule Service

CE v0.1 should include a Node.js demo Capsule Service.

The demo should prove:

- SDK import works;
- Agent registration works;
- token persistence works;
- heartbeat works;
- manifest report works;
- health provider works;
- config provider works;
- actions are visible;
- `echo` action works;
- `runHealthCheck` action works;
- CommandResult reporting works;
- AuditEvent appears in UI.

The demo should be intentionally simple.

It should not become a business application.

---

## 12. CE v0.1 Data Model Scope

CE v0.1 should include these core models:

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

Simplifications are acceptable, but the model should preserve future compatibility through fields such as:

```text
workspaceId
agentMode
runtime
metadataJson
secretRef
createdAt
updatedAt
```

CE should not implement Tenant or Organization models.

---

## 13. CE v0.1 API Scope

CE v0.1 should expose:

```text
Admin API
Agent API
System API
```

Admin API supports UI.

Agent API supports Node Embedded Agent SDK.

System API supports health/version checks.

Recommended API identity design:

```text
/api/admin/*
/api/agents/*
/api/system/*
```

Where practical, Agent APIs should use `me` instead of trusting path `agentId`:

```text
POST /api/agents/me/heartbeat
GET  /api/agents/me/commands
```

Backend must derive Agent identity from token.

---

## 14. CE v0.1 Security Scope

CE v0.1 must implement basic safety:

- admin authentication;
- Agent token authentication;
- registration token hash storage;
- Agent token hash storage;
- registration token shown only once;
- Agent token not logged;
- raw secrets not stored by default;
- sensitive config masking;
- Agent can only access its own resources;
- Commands assigned only to owning Agent;
- CommandResults accepted only from owning Agent;
- predefined actions only;
- no arbitrary shell execution;
- AuditEvents for important operations.

This is mandatory for CE trust.

---

## 15. CE v0.1 Observability Scope

CE v0.1 observability is basic visibility, not a full observability platform.

CE should show:

- Agent online/offline status;
- last heartbeat time;
- Capsule Service effective status;
- latest health;
- stale/offline reason;
- Command status;
- CommandResult;
- recent AuditEvents;
- system health.

CE should not implement logs/metrics/traces/alerts platform in v0.1.

---

## 16. CE v0.1 Implementation Order

Recommended implementation order:

```text
1. Backend scaffold
2. UI scaffold
3. SQLite schema and migrations
4. Local admin login
5. Registration token model and UI
6. Agent registration API
7. Agent token authentication
8. Node Agent SDK scaffold
9. Agent heartbeat
10. Agent/service UI visibility
11. Service manifest report
12. Health and config metadata report
13. Capsule Service detail UI
14. ActionDefinition model
15. Action request UI
16. Command creation
17. Command polling from SDK
18. Action execution in SDK
19. CommandResult reporting
20. Command UI
21. AuditEvent model
22. Audit UI
23. Dashboard summary
24. System health endpoint
25. Node demo Capsule Service
26. Docker quick start
27. Documentation polish
```

This order keeps the vertical loop visible as early as possible.

---

## 17. CE v0.1 Acceptance Criteria

CE v0.1 is acceptable when:

- Opstage can start locally;
- user can log in as local admin;
- user can create a registration token;
- Node demo Capsule Service can register;
- Agent token is stored as hash in Backend;
- Agent token is stored locally by SDK;
- Agent appears in UI;
- Agent heartbeat updates status;
- Capsule Service appears in UI;
- manifest is visible;
- health is visible;
- config metadata is visible;
- actions are visible;
- user can run `echo`;
- user can run `runHealthCheck`;
- Backend creates Command;
- SDK polls Command;
- SDK executes action;
- SDK reports CommandResult;
- UI displays Command and CommandResult;
- AuditEvents are visible;
- stale/offline state is visible;
- sensitive values are masked;
- raw tokens are not logged;
- no arbitrary shell execution exists;
- Docker quick start demonstrates the full loop.

---

## 18. CE v0.2 Direction

CE v0.2 should improve product quality after v0.1 feedback.

Possible improvements:

- better UI layout;
- better empty states;
- better error messages;
- better status/freshness explanation;
- better audit filtering;
- better command lifecycle display;
- better SDK logs;
- better retry/backoff behavior;
- improved Docker Compose demo;
- more test coverage;
- improved quick start;
- initial API reference;
- better troubleshooting docs.

CE v0.2 should still avoid EE/Cloud scope.

---

## 19. CE v0.3 Direction

CE v0.3 may add selected kernel improvements.

Possible improvements:

- Command expiration cleanup;
- simple health history if needed;
- better system settings page;
- improved dashboard summary;
- improved SDK diagnostics;
- explicit Agent disable/revoke if simple;
- more robust migration process;
- better release packaging;
- optional experimental database adapter only if strongly justified.

CE v0.3 should remain lightweight.

---

## 20. CE v1.0 Direction

CE v1.0 should be a reliable open-source release.

Expected qualities:

- stable core concepts;
- stable Backend Agent API;
- stable Admin API for UI;
- stable Node Agent SDK API;
- documented SQLite deployment;
- documented backup approach;
- documented upgrade path;
- meaningful test coverage;
- clear security notes;
- reliable Docker quick start;
- useful UI;
- useful demo;
- clear contribution guidance.

CE v1.0 should be valuable without EE.

---

## 21. CE Extension Reservations

CE should reserve low-cost extension points:

```text
workspaceId
agentMode
runtime
agentVersion
sdkVersion
protocolVersion
capabilities
secretRef
metadataJson
CommandType
AuditEvent actor/resource fields
```

CE should not implement future systems merely because extension fields exist.

The rule is:

> Reserve shape, not scope.

---

## 22. CE to EE Path

CE should leave a future path to EE.

Future EE may add:

- PostgreSQL/MySQL official support;
- RBAC;
- SSO;
- audit export;
- audit retention;
- alert rules;
- observability integrations;
- secret provider integrations;
- Sidecar Agent;
- External Agent;
- Java/Python/Go SDKs;
- HA deployment;
- commercial support.

CE should not block these, but CE should not implement them in v0.1.

---

## 23. CE to Cloud Path

CE should leave a future path to Cloud.

Future Cloud may add:

- Tenant;
- Organization;
- Workspace management;
- team invitations;
- subscription billing;
- usage metering;
- Cloud Agent Gateway;
- managed audit retention;
- managed alerting;
- Cloud support workflows.

CE should not implement Cloud tenancy or billing in v0.1.

---

## 24. CE Release Artifacts

CE v0.1 release artifacts should include:

```text
source repository
Opstage Docker image or build instructions
Docker Compose quick start
Node Agent SDK package or workspace package
Node demo Capsule Service
SQLite migration files
quick start guide
security notes
troubleshooting guide
release notes
```

If npm publishing is not ready, the Node SDK can first be used as a workspace package.

---

## 25. CE Documentation Requirements

CE v0.1 documentation should include:

- project overview;
- quick start;
- local development guide;
- Docker quick start;
- Opstage UI guide;
- Backend API overview;
- Node Agent SDK guide;
- demo Capsule Service guide;
- security notes;
- troubleshooting;
- roadmap notes.

The documentation should be enough for an AI coding agent and a human developer to build and run the first version.

---

## 26. CE Roadmap Guardrails

Guardrails:

1. Build CE first.
2. Keep CE useful.
3. Keep CE lightweight.
4. Keep CE single-node friendly.
5. Use SQLite by default.
6. Use Node Embedded Agent first.
7. Do not add Sidecar/External Agent in v0.1.
8. Do not add Java/Python/Go SDKs in v0.1.
9. Do not add tenancy or billing.
10. Do not add enterprise RBAC or SSO.
11. Do not add full observability platform.
12. Do not add secret vault.
13. Do not add license enforcement.
14. Do not add remote shell.
15. Do not store raw secrets by default.

---

## 27. Anti-Patterns

Avoid these CE roadmap anti-patterns.

### 27.1 CE as a crippled trial

CE must be useful as open source.

### 27.2 Too many future features in v0.1

CE v0.1 should prove the kernel, not the whole future product.

### 27.3 Multiple runtimes before Node.js is stable

Runtime expansion should wait.

### 27.4 Sidecar/External Agent before Embedded Agent is stable

Agent expansion should wait.

### 27.5 Full observability before basic visibility

First show Agents, services, health, Commands, and AuditEvents.

### 27.6 Remote shell as shortcut

Operations must be predefined actions, not arbitrary commands.

### 27.7 Raw secrets in config/action/result data

Use `secretRef` and masking.

---

## 28. Summary Roadmap

Recommended CE roadmap summary:

```text
CE v0.1
  Build the full governance loop with SQLite and Node Embedded Agent.

CE v0.2
  Improve usability, errors, SDK DX, audit filters, packaging, and docs.

CE v0.3
  Add selected kernel improvements without becoming enterprise-heavy.

CE v1.0
  Publish a reliable open-source community edition.
```

---

## 29. Acceptance Criteria

This CE roadmap is acceptable when:

- CE v0.1 scope is explicit;
- CE v0.1 non-goals are explicit;
- Node.js Embedded Agent is clearly first;
- SQLite-first deployment is clear;
- CE remains useful without EE or Cloud;
- future EE and Cloud paths are reserved but not implemented;
- roadmap guardrails prevent scope creep;
- acceptance criteria can guide implementation and review.

---

## 30. Summary

CE should be the first real proof of `xtrape-capsule`.

It should deliver a small but complete governance platform that makes lightweight Capsule Services visible, healthy, operable through predefined actions, and auditable.

The most important CE roadmap rule is:

> Build a useful open-source CE around the complete governance kernel first, then stabilize it before expanding into enterprise, Cloud, more runtimes, or advanced Agent modes.