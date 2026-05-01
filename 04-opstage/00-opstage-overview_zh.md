<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 00-opstage-overview.md
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

# Opstage（运维舞台） Subsystem 概述

- Status: 实施指南
- Edition: 共享
- Priority: 高
- Audience: architects, backend developers, frontend developers, agent SDK developers, product designers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/` (OpenAPI / Prisma) disagree, the ADRs and contracts win for CE（社区版） v0.1.

This document 定义 the subsystem overview for **Opstage（运维舞台）**.

Opstage（运维舞台） is the runtime governance platform under the `xtrape-capsule` domain. It is responsible for making Capsule Services visible, manageable, and auditable through a Backend, UI, and Agent（代理）-based integration model.

The current implementation focus is **Opstage（运维舞台） CE（社区版）**.

EE（企业版） and Cloud（云版） are future planning tracks and must not expand the CE（社区版） v0.1 implementation scope.

---

## 1. Positioning

`xtrape-capsule` is the domain and architecture concept for lightweight governable services.

Opstage（运维舞台） is the governance platform for that domain.

Recommended relationship:

```text
xtrape-capsule
    ↓ domain / architecture concept
Opstage
    ↓ runtime governance platform
Capsule Services
    ↓ lightweight services governed through Agents
```

Opstage（运维舞台） should not be treated as the whole `xtrape-capsule` domain. It is one major subsystem of the domain.

---

## 2. What Opstage（运维舞台） Is

Opstage（运维舞台） is:

> A runtime governance platform for Capsule Services.

It 提供:

- service registration visibility;
- Agent（代理） registration and connectivity;
- health and freshness visibility;
- configuration metadata visibility;
- predefined action execution;
- Command and CommandResult tracking;
- basic audit logs;
- operational UI;
- future extension points for enterprise and Cloud（云版） operations.

---

## 3. What Opstage（运维舞台） Is Not

Opstage（运维舞台） is not:

- a microservice framework;
- a Kubernetes replacement;
- a full observability platform;
- a full configuration center clone;
- a remote shell platform;
- a workflow engine as its first identity;
- a secret vault by default;
- a business application framework;
- a browser automation framework by itself.

Opstage（运维舞台） may integrate with some of these areas later, but its core identity should remain Capsule Service（胶囊服务） governance.

---

## 4. Core Problem

AI-era development will create more lightweight services, agents, automation workers, CAPI adapters, account/session managers, and connector services.

These services are usually easy to create but hard to govern over time.

Common problems:

- services are forgotten after creation;
- runtime status is unclear;
- config metadata is scattered;
- account/session services are hard to track;
- manual operations are not audited;
- small services lack admin UI;
- logs, health, and commands are inconsistent;
- long-term maintenance becomes unreliable.

Opstage（运维舞台） addresses this by giving lightweight services a common governance surface without forcing them into a heavy microservice platform.

---

## 5. Core Governance Loop

The Opstage（运维舞台） governance loop is:

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

This loop is the product kernel.

CE（社区版） v0.1 should prove this loop end to end.

---

## 6. Main Components

Opstage（运维舞台） consists of three main component groups:

```text
Opstage UI
Opstage Backend
Opstage Agent integration
```

### 6.1 Opstage（运维舞台） UI

The UI 提供 the human-facing console.

It allows operators to:

- log in;
- view dashboard summary;
- view Agents;
- view Capsule Services;
- inspect service manifests;
- inspect health reports;
- inspect config metadata;
- execute predefined actions;
- view Commands;
- view AuditEvents;
- create registration tokens.

### 6.2 Opstage（运维舞台） Backend

The Backend is the control-plane service.

It is responsible for:

- Admin APIs;
- Agent（代理） APIs;
- authentication;
- registration tokens;
- Agent（代理） tokens;
- Agent（代理） heartbeat processing;
- service report storage;
- Command creation;
- CommandResult storage;
- status and freshness calculation;
- AuditEvent creation;
- persistence;
- security enforcement.

### 6.3 Agent（代理） integration

Agent（代理） integration connects Capsule Services to Opstage（运维舞台）.

CE（社区版） v0.1 implements:

```text
Node.js embedded Agent SDK
```

Future editions may add:

```text
sidecar Agent
external Agent
host Agent
Kubernetes Agent
Java Agent SDK
Python Agent SDK
Go Agent SDK
Agent Gateway
```

These future modes are not CE（社区版） v0.1 requirements.

---

## 7. CE（社区版） Scope

Opstage（运维舞台） CE（社区版） is the current implementation target.

CE（社区版） should implement the minimum complete product kernel:

- local admin login;
- Backend;
- UI;
- SQLite persistence;
- Node.js embedded Agent（代理） SDK;
- registration token;
- Agent（代理） token authentication;
- heartbeat;
- service manifest report;
- health report;
- config metadata visibility;
- predefined action metadata;
- action request;
- Command creation;
- command polling;
- CommandResult reporting;
- basic AuditEvents;
- Docker quick start;
- demo Capsule Service（胶囊服务）.

CE（社区版） should be useful without EE（企业版） or Cloud（云版）.

---

## 8. EE（企业版） Extension Direction

Opstage（运维舞台） EE（企业版） is the future private enterprise commercial edition.

EE（企业版） may extend Opstage（运维舞台） with:

- production database support;
- PostgreSQL / MySQL;
- RBAC;
- SSO / OIDC / LDAP / SAML;
- audit retention and export;
- observability integrations;
- alert rules;
- secret provider integrations;
- sidecar / external Agents;
- Java / Python / Go Agent（代理） SDKs;
- high availability;
- cluster deployment;
- enterprise support;
- commercial packaging.

EE（企业版） must extend the CE（社区版） governance kernel, not redefine it.

---

## 9. Cloud（云版） Extension Direction

Opstage（运维舞台） Cloud（云版） is the future hosted SaaS edition.

Cloud（云版） may extend Opstage（运维舞台） with:

- hosted Backend and UI;
- Tenant / Organization / Workspace model;
- team collaboration;
- subscription billing;
- usage metering;
- Cloud（云版） Agent（代理） Gateway;
- managed audit retention;
- managed alerting;
- Cloud（云版） data export and deletion workflows;
- Cloud（云版） support and SLA;
- managed operations.

Cloud（云版） must remain compatible with the same Agent（代理）-based governance model.

---

## 10. 共享 Core Concepts

Opstage（运维舞台） should preserve these core concepts across CE（社区版）, EE（企业版）, and Cloud（云版）:

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

Future editions may add fields and capabilities, but they should not change the meaning of these concepts.

---

## 11. Data Boundary

Opstage（运维舞台） should store governance metadata by default.

It may store:

- Agent（代理） metadata;
- Capsule Service（胶囊服务） metadata;
- manifest metadata;
- health reports;
- config metadata;
- action metadata;
- Commands;
- CommandResults;
- AuditEvents.

It should not store raw operational secrets by default.

Sensitive values should use:

```text
secretRef
```

or be masked.

Recommended principle:

> Opstage（运维舞台） governs services through metadata, references, commands, results, and audit records; raw secrets should remain customer-controlled by default.

---

## 12. 安全 Boundary

Opstage（运维舞台） security is based on two authenticated actor types in CE（社区版）:

```text
Admin user
Agent
```

Admin users access Admin APIs through UI.

Agents access Agent（代理） APIs through Agent（代理） tokens.

The Backend must enforce:

- user authentication;
- Agent（代理） token authentication;
- Agent（代理） ownership of Commands;
- action validation;
- sensitive value masking;
- AuditEvent creation;
- no arbitrary shell execution.

Future EE（企业版） and Cloud（云版） may add stronger identity, RBAC, tenancy, SSO, and compliance security.

---

## 13. Command Model

Opstage（运维舞台） does not directly operate Capsule Services from the UI.

The operation path is:

```text
UI
    ↓ Admin API
Backend creates Command
    ↓ Agent API
Agent polls or receives Command
    ↓ local predefined action handler
Capsule Service action executes
    ↓
Agent reports CommandResult
    ↓
Backend stores result and audit
```

This indirection is important for safety, auditability, and future scalability.

---

## 14. Agent（代理） Connectivity Rule

The default connectivity rule is outbound-first:

```text
Agent -> Opstage Backend
```

Opstage（运维舞台） should not require inbound access into customer Capsule Services by default.

CE（社区版） uses HTTP polling.

Future EE（企业版）/Cloud（云版） may add WebSocket, long polling, gRPC, or Agent（代理） Gateway, but simple HTTP polling remains the reliable baseline.

---

## 15. 实现 Guardrails

For CE（社区版） v0.1, do not implement:

- Tenant system;
- Organization system;
- billing;
- enterprise RBAC;
- SSO;
- PostgreSQL/MySQL requirement;
- Redis requirement;
- Queue requirement;
- Kubernetes requirement;
- Agent（代理） Gateway;
- full observability platform;
- Secret Vault;
- license enforcement;
- arbitrary shell execution.

CE（社区版） should stay focused on the vertical governance slice.

---

## 16. Acceptance Criteria

This overview is satisfied when:

- Opstage（运维舞台） is clearly defined as a subsystem of `xtrape-capsule`;
- Opstage（运维舞台） is positioned as a runtime governance platform;
- UI, Backend, and Agent（代理） integration responsibilities are clear;
- CE（社区版） scope is clearly identified as the current implementation target;
- EE（企业版） and Cloud（云版） are clearly identified as future extension tracks;
- shared core concepts are preserved;
- data and security boundaries are explicit;
- command and Agent（代理） connectivity rules are clear;
- CE（社区版） implementation guardrails are explicit.

---

## 17. Summary

Opstage（运维舞台） is the runtime governance platform for Capsule Services.

It should make lightweight services visible, operable, and auditable without forcing them into a heavy microservice or platform stack.

The most important Opstage（运维舞台） subsystem rule is:

> Build Opstage（运维舞台） CE（社区版） as a complete lightweight governance loop first, then extend the same kernel for EE（企业版） and Cloud（云版） without redefining the core model.
