<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 01-ce-roadmap.md
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

# CE（社区版） Roadmap

- Status: 实施指南
- Edition: CE（社区版）
- Priority: 高
- Audience: founders, architects, product managers, backend developers, frontend developers, agent SDK developers, AI coding agents

This document 定义 the roadmap for **Opstage（运维舞台） CE（社区版） / Community 版本**.

CE（社区版） is the open-source, lightweight, self-hosted edition of the `xtrape-capsule` product family. It is the current implementation focus.

The first CE（社区版） milestone is **CE（社区版） v0.1**. CE（社区版） v0.1 should prove the complete Capsule governance loop with Opstage（运维舞台） Backend, Opstage（运维舞台） UI, SQLite, and the Node.js Embedded Agent（代理） SDK.

EE（企业版） and Cloud（云版） are future tracks. They may influence extension-point design, but they must not expand CE（社区版） v0.1 implementation scope.

---

## 1. Purpose

The purpose of the CE（社区版） roadmap is to define:

- what CE（社区版） should deliver first;
- what CE（社区版） v0.1 must include;
- what CE（社区版） v0.1 must not include;
- how CE（社区版） should evolve after v0.1;
- how CE（社区版） should remain genuinely useful as open source;
- where CE（社区版） should reserve extension points for EE（企业版） and Cloud（云版）;
- how to avoid early scope creep.

The key rule is:

> CE（社区版） must first prove the smallest complete governance loop before adding enterprise, Cloud（云版）, multi-runtime, or advanced observability features.

---

## 2. CE（社区版） Product Positioning

CE（社区版） is:

> A lightweight open-source runtime governance platform for Capsule Services.

CE（社区版） should be:

- open-source;
- self-hosted;
- single-node friendly;
- easy to run locally;
- SQLite-first;
- Node.js Agent（代理）-first;
- safe by default;
- useful without EE（企业版） or Cloud（云版）;
- simple enough for small teams and individual developers.

CE（社区版） should not feel like a broken trial of EE（企业版）.

---

## 3. CE（社区版） Governance Kernel

The CE（社区版） governance kernel is:

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

CE（社区版） v0.1 should prove this kernel end to end.

All later CE（社区版） improvements should strengthen this kernel, not distract from it.

---

## 4. CE（社区版） v0.1 Goal

CE（社区版） v0.1 goal:

> Deliver a working local prototype that 演示 UI + Backend + Node Embedded Agent（代理） + demo Capsule Service（胶囊服务） from registration to audited action execution.

CE（社区版） v0.1 should be optimized for:

- validation;
- demo;
- developer feedback;
- architecture verification;
- first open-source release;
- future implementation guidance.

CE（社区版） v0.1 does not need to be enterprise-ready.

---

## 5. CE（社区版） v0.1 Scope

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
single-container or simple Docker deployment
Docker Compose quick start
```

This is the implementation target.

---

## 6. CE（社区版） v0.1 Non-Goals

CE（社区版） v0.1 must not include:

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

## 7. CE（社区版） v0.1 架构

Recommended CE（社区版） v0.1 architecture:

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

CE（社区版） v0.1 should prefer fewer moving parts.

---

## 8. CE（社区版） v0.1 Backend Scope

Backend should implement:

- project scaffold;
- API server;
- SQLite persistence;
- schema and migrations;
- local admin user;
- login/logout/session or token handling;
- registration token creation;
- Agent（代理） registration;
- Agent（代理） token hash storage;
- Agent（代理） authentication middleware;
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

Backend should not implement EE（企业版）/Cloud（云版） systems in v0.1.

---

## 9. CE（社区版） v0.1 UI Scope

UI should implement:

- Login page;
- Dashboard page;
- Agents list;
- Agent（代理） detail;
- Capsule Services list;
- Capsule Service（胶囊服务） detail;
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

CE（社区版） v0.1 UI should not show disabled EE（企业版）/Cloud（云版）-only menus.

---

## 10. CE（社区版） v0.1 Agent（代理） Scope

Agent（代理） scope is limited to:

```text
Node.js Embedded Agent SDK
```

The SDK should implement:

- configuration from code and environment variables;
- file-based Agent（代理） token store;
- registration with registration token;
- Agent（代理） token reuse;
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

No Sidecar or External Agent（代理） in CE（社区版） v0.1.

---

## 11. CE（社区版） v0.1 Demo Capsule Service（胶囊服务）

CE（社区版） v0.1 should include a Node.js demo Capsule Service（胶囊服务）.

The demo should prove:

- SDK import works;
- Agent（代理） registration works;
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

## 12. CE（社区版） v0.1 Data Model Scope

CE（社区版） v0.1 should include these core models:

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

CE（社区版） should not implement Tenant or Organization models.

---

## 13. CE（社区版） v0.1 API Scope

CE（社区版） v0.1 should expose:

```text
Admin API
Agent API
System API
```

Admin API 支持 UI.

Agent（代理） API 支持 Node Embedded Agent（代理） SDK.

System API 支持 health/version checks.

Recommended API identity design:

```text
/api/admin/*
/api/agents/*
/api/system/*
```

Where practical, Agent（代理） APIs should use `me` instead of trusting path `agentId`:

```text
POST /api/agents/me/heartbeat
GET  /api/agents/me/commands
```

Backend must derive Agent（代理） identity from token.

---

## 14. CE（社区版） v0.1 安全 Scope

CE（社区版） v0.1 must implement basic safety:

- admin authentication;
- Agent（代理） token authentication;
- registration token hash storage;
- Agent（代理） token hash storage;
- registration token shown only once;
- Agent（代理） token not logged;
- raw secrets not stored by default;
- sensitive config masking;
- Agent（代理） can only access its own resources;
- Commands assigned only to owning Agent（代理）;
- CommandResults accepted only from owning Agent（代理）;
- predefined actions only;
- no arbitrary shell execution;
- AuditEvents for important operations.

This is mandatory for CE（社区版） trust.

---

## 15. CE（社区版） v0.1 Observability Scope

CE（社区版） v0.1 observability is basic visibility, not a full observability platform.

CE（社区版） should show:

- Agent（代理） online/offline status;
- last heartbeat time;
- Capsule Service（胶囊服务） effective status;
- latest health;
- stale/offline reason;
- Command status;
- CommandResult;
- recent AuditEvents;
- system health.

CE（社区版） should not implement logs/metrics/traces/alerts platform in v0.1.

---

## 16. CE（社区版） v0.1 实现 Order

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

## 17. CE（社区版） v0.1 Acceptance Criteria

CE（社区版） v0.1 is acceptable when:

- Opstage（运维舞台） can start locally;
- user can log in as local admin;
- user can create a registration token;
- Node demo Capsule Service（胶囊服务） can register;
- Agent（代理） token is stored as hash in Backend;
- Agent（代理） token is stored locally by SDK;
- Agent（代理） appears in UI;
- Agent（代理） heartbeat updates status;
- Capsule Service（胶囊服务） appears in UI;
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
- Docker quick start 演示 the full loop.

---

## 18. CE（社区版） v0.2 Direction

CE（社区版） v0.2 should improve product quality after v0.1 feedback.

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

CE（社区版） v0.2 should still avoid EE（企业版）/Cloud（云版） scope.

---

## 19. CE（社区版） v0.3 Direction

CE（社区版） v0.3 may add selected kernel improvements.

Possible improvements:

- Command expiration cleanup;
- simple health history if needed;
- better system settings page;
- improved dashboard summary;
- improved SDK diagnostics;
- explicit Agent（代理） disable/revoke if simple;
- more robust migration process;
- better release packaging;
- optional experimental database adapter only if strongly justified.

CE（社区版） v0.3 should remain lightweight.

---

## 20. CE（社区版） v1.0 Direction

CE（社区版） v1.0 should be a reliable open-source release.

Expected qualities:

- stable core concepts;
- stable Backend Agent（代理） API;
- stable Admin API for UI;
- stable Node Agent（代理） SDK API;
- documented SQLite deployment;
- documented backup approach;
- documented upgrade path;
- meaningful test coverage;
- clear security notes;
- reliable Docker quick start;
- useful UI;
- useful demo;
- clear contribution guidance.

CE（社区版） v1.0 should be valuable without EE（企业版）.

---

## 21. CE（社区版） Extension Reservations

CE（社区版） should reserve low-cost extension points:

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

CE（社区版） should not implement future systems merely because extension fields exist.

The rule is:

> Reserve shape, not scope.

---

## 22. CE（社区版） to EE（企业版） Path

CE（社区版） should leave a future path to EE（企业版）.

Future EE（企业版） may add:

- PostgreSQL/MySQL official support;
- RBAC;
- SSO;
- audit export;
- audit retention;
- alert rules;
- observability integrations;
- secret provider integrations;
- Sidecar Agent（代理）;
- External Agent（代理）;
- Java/Python/Go SDKs;
- HA deployment;
- commercial support.

CE（社区版） should not block these, but CE（社区版） should not implement them in v0.1.

---

## 23. CE（社区版） to Cloud（云版） Path

CE（社区版） should leave a future path to Cloud（云版）.

Future Cloud（云版） may add:

- Tenant;
- Organization;
- Workspace management;
- team invitations;
- subscription billing;
- usage metering;
- Cloud（云版） Agent（代理） Gateway;
- managed audit retention;
- managed alerting;
- Cloud（云版） support workflows.

CE（社区版） should not implement Cloud（云版） tenancy or billing in v0.1.

---

## 24. CE（社区版） Release Artifacts

CE（社区版） v0.1 release artifacts should include:

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

## 25. CE（社区版） 文档 Requirements

CE（社区版） v0.1 documentation should include:

- project overview;
- quick start;
- local development guide;
- Docker quick start;
- Opstage（运维舞台） UI guide;
- Backend API overview;
- Node Agent（代理） SDK guide;
- demo Capsule Service（胶囊服务） guide;
- security notes;
- troubleshooting;
- roadmap notes.

The documentation should be enough for an AI coding agent and a human developer to build and run the first version.

---

## 26. CE（社区版） Roadmap Guardrails

Guardrails:

1. Build CE（社区版） first.
2. Keep CE（社区版） useful.
3. Keep CE（社区版） lightweight.
4. Keep CE（社区版） single-node friendly.
5. Use SQLite by default.
6. Use Node Embedded Agent（代理） first.
7. Do not add Sidecar/External Agent（代理） in v0.1.
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

Avoid these CE（社区版） roadmap anti-patterns.

### 27.1 CE（社区版） as a crippled trial

CE（社区版） must be useful as open source.

### 27.2 Too many future features in v0.1

CE（社区版） v0.1 should prove the kernel, not the whole future product.

### 27.3 Multiple runtimes before Node.js is stable

Runtime expansion should wait.

### 27.4 Sidecar/External Agent（代理） before Embedded Agent（代理） is stable

Agent（代理） expansion should wait.

### 27.5 Full observability before basic visibility

First show Agents, services, health, Commands, and AuditEvents.

### 27.6 Remote shell as shortcut

Operations must be predefined actions, not arbitrary commands.

### 27.7 Raw secrets in config/action/result data

Use `secretRef` and masking.

---

## 28. Summary Roadmap

Recommended CE（社区版） roadmap summary:

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

This CE（社区版） roadmap is acceptable when:

- CE（社区版） v0.1 scope is explicit;
- CE（社区版） v0.1 non-goals are explicit;
- Node.js Embedded Agent（代理） is clearly first;
- SQLite-first deployment is clear;
- CE（社区版） remains useful without EE（企业版） or Cloud（云版）;
- future EE（企业版） and Cloud（云版） paths are reserved but not implemented;
- roadmap guardrails prevent scope creep;
- acceptance criteria can guide implementation and review.

---

## 30. Summary

CE（社区版） should be the first real proof of `xtrape-capsule`.

It should deliver a small but complete governance platform that makes lightweight Capsule Services visible, healthy, operable through predefined actions, and auditable.

The most important CE（社区版） roadmap rule is:

> Build a useful open-source CE（社区版） around the complete governance kernel first, then stabilize it before expanding into enterprise, Cloud（云版）, more runtimes, or advanced Agent（代理） modes.
