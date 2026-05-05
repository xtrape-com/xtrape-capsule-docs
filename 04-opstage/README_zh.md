---
status: draft
audience: architects
stability: unstable
last_reviewed: 2026-05-05
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

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

# Opstage（运维舞台） Documents

- Status: 实施指南
- Edition: 共享
- Priority: 高
- Audience: architects, backend developers, frontend developers, agent SDK developers, product designers, AI coding agents

This directory 包含 the Opstage（运维舞台） subsystem documents for the `xtrape-capsule` product family.

Opstage（运维舞台） is the runtime governance platform for Capsule Services. It 提供 the UI, Backend, and Agent（代理） integration
model that makes lightweight services visible, operable, and auditable.

The current implementation focus is **Opstage（运维舞台） CE（社区版）**.

EE（企业版） and Cloud（云版） documents are future planning references. They help keep the architecture extensible, but they must not expand the CE（社区版） v0.1 implementation scope.

---

## 1. Purpose of This Directory

The purpose of this directory is to define the Opstage（运维舞台） runtime governance subsystem.

It 涵盖:

- what Opstage（运维舞台） is;
- how Opstage（运维舞台） UI works;
- how Opstage（运维舞台） Backend works;
- how Agents connect Capsule Services to Opstage（运维舞台）;
- how Commands and Actions work;
- how AuditEvents are modeled;
- how observability should evolve from CE（社区版） to EE（企业版） and Cloud（云版）.

This directory should be read after the higher-level Capsule and edition-boundary documents.

---

## 2. Opstage（运维舞台） Positioning

Opstage（运维舞台） is:

> The runtime governance platform for Capsule Services.

It is responsible for the core governance loop:

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

This governance loop is the CE（社区版） product kernel.

---

## 3. What Opstage（运维舞台） Includes

Opstage（运维舞台） 包括 three main subsystem groups:

```text
Opstage UI
Opstage Backend
Opstage Agent Integration
```

It also 包括 shared operation models:

```text
Command and Action Model
Audit Model
Observability Roadmap
```

These models bind UI, Backend, and Agent（代理） together into one coherent governance system.

---

## 4. What Opstage（运维舞台） Is Not

Opstage（运维舞台） is not:

- a generic microservice framework;
- a Kubernetes replacement;
- a full observability platform;
- a full configuration center clone;
- a secret vault by default;
- a remote shell system;
- a browser automation framework by itself;
- a workflow engine as its first identity;
- a SaaS billing system in CE（社区版）.

Future EE（企业版） and Cloud（云版） may integrate with some of these areas, but the first product identity should remain Capsule Service（胶囊服务） governance.

---

## 5. Current CE（社区版） 实现 Boundary

Opstage（运维舞台） CE（社区版） v0.1 should implement a lightweight but complete vertical slice.

CE（社区版） should include:

- local admin login;
- Opstage（运维舞台） Backend;
- Opstage（运维舞台） UI;
- SQLite persistence;
- Node.js embedded Agent（代理） SDK;
- registration token;
- Agent（代理） token authentication;
- heartbeat;
- service manifest report;
- health report;
- config metadata visibility;
- predefined action metadata;
- action request from UI;
- Command creation;
- command polling;
- CommandResult reporting;
- basic AuditEvents;
- dashboard summary;
- system health endpoint;
- Docker quick start;
- demo Capsule Service（胶囊服务）.

CE（社区版） should be useful without EE（企业版） or Cloud（云版）.

---

## 6. CE（社区版） Non-Goals

Opstage（运维舞台） CE（社区版） v0.1 should not implement:

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
- Kubernetes requirement;
- Agent（代理） Gateway;
- sidecar Agent（代理）;
- external Agent（代理）;
- Java/Python/Go Agent（代理） SDKs;
- full observability platform;
- alert rule engine;
- secret vault;
- license enforcement;
- arbitrary shell execution.

These are future EE（企业版） or Cloud（云版） planning items.

---

## 7. Recommended Reading Order

Read the documents in this directory in the following order:

```text
04-opstage/README.md
04-opstage/00-opstage-overview.md
04-opstage/01-opstage-ui.md
04-opstage/02-opstage-backend.md
04-opstage/03-opstage-agent-integration.md
04-opstage/04-command-and-action-model.md
04-opstage/05-audit-model.md
04-opstage/06-observability-roadmap.md
```

This order moves from subsystem overview to concrete implementation models.

---

## 8. Document List

### 8.1 `00-opstage-overview.md`

Defines the Opstage（运维舞台） subsystem as a whole.

Use it to understand:

- Opstage（运维舞台） positioning;
- main components;
- shared concepts;
- CE（社区版） scope;
- EE（企业版） and Cloud（云版） extension directions;
- implementation guardrails.

### 8.2 `01-opstage-ui.md`

Defines the human-facing UI console.

Use it to implement:

- Login;
- Dashboard;
- Agents pages;
- Capsule Services pages;
- Commands pages;
- Audit Logs pages;
- System Settings page;
- action execution UX;
- sensitive value display rules.

### 8.3 `02-opstage-backend.md`

Defines the Backend control plane.

Use it to implement:

- Admin APIs;
- Agent（代理） APIs;
- authentication;
- token handling;
- persistence;
- core data models;
- Command flow;
- status and freshness calculation;
- AuditEvent creation.

### 8.4 `03-opstage-agent-integration.md`

Defines how Agents connect Capsule Services to Opstage（运维舞台）.

Use it to implement:

- Node.js embedded Agent（代理） SDK;
- registration flow;
- heartbeat flow;
- service manifest report;
- health provider;
- config provider;
- action registry;
- command polling;
- CommandResult reporting.

### 8.5 `04-command-and-action-model.md`

Defines the safe operation mechanism.

Use it to implement:

- ActionDefinition;
- Command;
- CommandResult;
- action request flow;
- action danger levels;
- command statuses;
- validation rules;
- no arbitrary shell execution rule.

### 8.6 `05-audit-model.md`

Defines structured operation traceability.

Use it to implement:

- AuditEvent;
- actor model;
- resource model;
- action naming;
- result values;
- audit sanitization;
- audit API;
- audit UI.

### 8.7 `06-observability-roadmap.md`

Defines the observability evolution path.

Use it to implement CE（社区版） visibility and avoid premature observability complexity.

It clarifies:

- CE（社区版） basic visibility;
- Agent（代理） status;
- Capsule Service（胶囊服务） effective status;
- freshness;
- command visibility;
- audit visibility;
- future EE（企业版）/Cloud（云版） logs, metrics, traces, alerts, and dashboards.

---

## 9. 共享 Core Concepts

All documents in this directory should use the same core concepts:

```text
Agent
CapsuleService
Manifest
HealthReport
ConfigItem
ActionDefinition
Command
CommandResult
AuditEvent
Status values
secretRef
```

Future editions may extend these concepts, but they should not redefine them.

---

## 10. 实现 优先级

For CE（社区版） v0.1, recommended implementation priority is:

```text
1. Backend persistence and auth
2. Registration token and Agent registration
3. Node.js embedded Agent SDK
4. Heartbeat and service report
5. UI Agent and Service visibility
6. Health and config metadata visibility
7. ActionDefinition and Command flow
8. CommandResult reporting
9. AuditEvent model and UI
10. Dashboard and system health
11. Docker quick start and demo service
```

This order proves the core governance loop step by step.

---

## 11. Safety Rules

Opstage（运维舞台） CE（社区版） must follow these safety rules:

1. UI never calls Agent（代理） directly.
2. Backend creates durable Commands.
3. Agents execute only predefined actions.
4. Arbitrary shell execution is not part of CE（社区版）.
5. Agent（代理） tokens are stored as hashes in Backend.
6. Registration tokens are shown only once.
7. Raw secrets are not stored by default.
8. Sensitive values are masked.
9. `secretRef` is used for sensitive references.
10. Important governance operations create AuditEvents.
11. Stale services must not be shown as fresh healthy services.

---

## 12. Extension Rules

CE（社区版） should reserve clean extension points where cheap:

```text
workspaceId
agentMode
runtime
secretRef
metadataJson
AuditEvent actor/resource fields
Command as durable record
CommandResult as durable record
status and freshness calculation
```

CE（社区版） should not implement future systems just because extension fields exist.

The rule is:

> Reserve space for EE（企业版） and Cloud（云版）, but do not let EE（企业版） and Cloud（云版） become CE（社区版） dependencies.

---

## 13. Acceptance Criteria

The Opstage（运维舞台） document set is useful when:

- the role of Opstage（运维舞台） is clear;
- UI, Backend, and Agent（代理） responsibilities are separated;
- Command and Action flow is explicit;
- AuditEvent model is explicit;
- CE（社区版） implementation scope is clear;
- CE（社区版） non-goals are explicit;
- EE（企业版） and Cloud（云版） extensions are clearly future planning;
- safety rules prevent arbitrary execution and secret leakage;
- implementation agents can follow the reading order and build the CE（社区版） vertical slice.

---

## 14. Summary

This directory 定义 the Opstage（运维舞台） runtime governance subsystem.

The most important Opstage（运维舞台） directory rule is:

> Build the CE（社区版） governance loop first through UI, Backend, Agent（代理）, Commands, Results, and AuditEvents; keep future EE（企业版） and Cloud（云版） capabilities as extension tracks, not current requirements.
