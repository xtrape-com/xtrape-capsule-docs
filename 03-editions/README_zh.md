<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: README.md
翻译状态 / Translation Status: 已翻译 / Translated
生成时间 / Generated: 2026-05-01 09:28:53
================================================================================
注意 / Notes:
- 技术术语如 Capsule Service、Agent、Opstage 等保留英文或采用中英对照
- 代码块中的内容不翻译
- 文件路径和 URL 不翻译
- 保持原有的 Markdown 格式结构
================================================================================
-->

# 版本 Boundaries

- Status: 实施指南
- Edition: 共享
- Priority: 高
- Audience: founders, architects, product designers, backend developers, frontend developers, agent SDK developers, AI coding agents

This document 定义 the edition boundaries for the `xtrape-capsule` product family.

The product family is planned around three editions:

```text
CE      = Community Edition
EE      = Enterprise Edition
Cloud   = SaaS Cloud Edition
```

The current implementation focus is **CE（社区版）**.

EE（企业版） and Cloud（云版） are planning tracks. They help keep the architecture future-friendly, but they are not implementation requirements for CE（社区版） v0.1.

---

## 1. Purpose

The purpose of this document is to prevent edition confusion during design and implementation.

It 定义:

- what CE（社区版） is responsible for now;
- what EE（企业版） is allowed to plan for later;
- what Cloud（云版） is allowed to plan for later;
- which documents are implementation targets;
- which documents are planning references;
- how CE（社区版） should reserve extension points without becoming heavy.

The key rule is:

> Only CE（社区版） documents marked as `Implementation Target` are current development requirements.

---

## 2. 版本 概述

### 2.1 CE（社区版） — Community 版本

CE（社区版） is the open-source community edition.

CE（社区版） is the current implementation target.

CE（社区版） should be:

- lightweight;
- self-hosted;
- open-source;
- easy to run;
- SQLite-first;
- single-node friendly;
- safe by default;
- useful without EE（企业版） or Cloud（云版）.

CE（社区版） should prove the core Capsule governance loop:

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
Basic audit log
```

### 2.2 EE（企业版） — Enterprise 版本

EE（企业版） is the future private commercial edition.

EE（企业版） is not a CE（社区版） v0.1 implementation requirement.

EE（企业版） may plan for:

- enterprise identity;
- RBAC;
- SSO / OIDC / LDAP / SAML;
- production database support;
- high availability;
- cluster deployment;
- advanced audit;
- observability integrations;
- secret provider integrations;
- additional Agent（代理） modes;
- commercial support.

EE（企业版） should extend CE（社区版）, not replace it with an incompatible product.

### 2.3 Cloud（云版） — SaaS Cloud（云版） 版本

Cloud（云版） is the future hosted SaaS edition.

Cloud（云版） is not a CE（社区版） v0.1 implementation requirement.

Cloud（云版） may plan for:

- hosted Opstage（运维舞台） Backend and UI;
- multi-tenant organizations and workspaces;
- user signup and team collaboration;
- subscription billing;
- Agent（代理） Gateway;
- managed audit retention;
- managed alerting;
- usage metering;
- Cloud（云版） support and SLA.

Cloud（云版） should be a hosted evolution of the same Capsule governance model.

---

## 3. Current 实现 Rule

Current implementation should follow this priority:

```text
1. Accepted ADRs in 08-decisions/
2. Implementation contracts in 09-contracts/
3. Implementation plans in 10-implementation/
4. CE Implementation Target documents
5. Shared specifications used by CE
6. CE extension-point documents
7. EE / Cloud planning documents only as future context
```

实现 agents and developers must not treat EE（企业版） or Cloud（云版） planning documents as required work for CE（社区版） v0.1.

---

## 4. Document 状态 Meaning

### 4.1 实现 Target

A document marked as:

```text
Status: Implementation Target
```

means:

- it is part of the current CE（社区版） development target;
- implementation should follow it unless a later design decision changes it;
- acceptance criteria in the document should guide development and review.

### 4.2 实施指南

A document marked as:

```text
Status: Implementation Guidance
```

means:

- it guides how implementation documents should be interpreted;
- it may define boundaries, principles, or reading order;
- it may not define concrete feature requirements by itself.

### 4.3 Planning

A document marked as:

```text
Status: Planning
```

means:

- it is future-facing;
- it is not required for CE（社区版） v0.1;
- it may define extension points;
- it should not increase CE（社区版） v0.1 implementation scope.

---

## 5. CE（社区版） Boundary

CE（社区版） should include the minimum complete product kernel.

CE（社区版） should implement:

- local admin login;
- Opstage（运维舞台） Backend;
- Opstage（运维舞台） UI;
- SQLite persistence;
- Node.js embedded Agent（代理） SDK;
- Agent（代理） registration token;
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
- Docker quick start;
- demo Capsule Service（胶囊服务）.

CE（社区版） should not implement enterprise or SaaS systems in v0.1.

---

## 6. EE（企业版） Boundary

EE（企业版） planning may define stronger enterprise capabilities.

EE（企业版） may include in the future:

- RBAC;
- SSO / OIDC / LDAP / SAML;
- PostgreSQL / MySQL official support;
- high availability;
- Kubernetes / Helm deployment;
- advanced audit retention and export;
- alert rules;
- observability integrations;
- enterprise secret provider integrations;
- sidecar Agent（代理）;
- external Agent（代理）;
- Java / Python / Go Agent（代理） SDKs;
- license and commercial support packaging.

These are not CE（社区版） v0.1 requirements.

---

## 7. Cloud（云版） Boundary

Cloud（云版） planning may define hosted SaaS capabilities.

Cloud（云版） may include in the future:

- Tenant;
- Organization;
- Workspace management;
- SaaS user accounts;
- team invitations;
- subscription billing;
- usage metering;
- Cloud（云版） Agent（代理） Gateway;
- managed audit retention;
- managed alerting;
- Cloud（云版） support access;
- hosted data export and deletion workflows;
- Cloud（云版） SLA and operational controls.

These are not CE（社区版） v0.1 requirements.

---

## 8. Extension-Point Rule

CE（社区版） should reserve extension points where they are cheap and clean.

Good CE（社区版） reservations:

```text
workspaceId
agentMode
runtime
secretRef
metadataJson
AuditEvent actor/resource fields
Command as durable record
CommandResult as durable record
Agent token hash
registration token hash
status and freshness calculation
```

Bad CE（社区版） scope expansion:

```text
Tenant system
Organization system
Billing system
Full RBAC
SSO
Cluster mode
Cloud Agent Gateway
Secret Vault
Metrics platform
Log platform
Alert engine
License enforcement
```

The rule is:

> Reserve space for the future, but do not make the future a dependency of CE（社区版） v0.1.

---

## 9. 版本 Compatibility Rule

CE（社区版）, EE（企业版）, and Cloud（云版） should share the same conceptual kernel:

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

Future editions may add capabilities, but they should not redefine the meaning of these core concepts.

---

## 10. Commercial Boundary Rule

Commercial editions should add value through scale, governance, support, deployment, and managed operations.

They should not depend on intentionally breaking CE（社区版）.

Good commercial boundaries:

```text
enterprise identity
advanced audit
production database
HA deployment
managed Cloud hosting
team collaboration
support
SLA
secret provider integration
observability integration
```

Bad commercial boundaries:

```text
CE cannot register Agents
CE cannot run predefined actions
CE cannot view basic audit logs
CE cannot persist data
CE Agent SDK is intentionally incomplete
```

---

## 11. Recommended Reading Order

Recommended edition reading order:

```text
03-editions/README.md
03-editions/ce/README.md
03-editions/ce/*
03-editions/ee/README.md
03-editions/ee/*
03-editions/cloud/README.md
03-editions/cloud/*
```

For implementation work, read CE（社区版） first.

For product planning, read EE（企业版） and Cloud（云版） after CE（社区版）.

---

## 12. 实现 Guardrails

When implementing CE（社区版） v0.1, avoid these mistakes:

- do not implement Cloud（云版） tenancy;
- do not implement billing;
- do not implement enterprise RBAC;
- do not implement SSO;
- do not require PostgreSQL/MySQL;
- do not require Redis or Queue;
- do not require Kubernetes;
- do not implement Agent（代理） Gateway;
- do not implement full observability platform;
- do not implement secret vault;
- do not implement license enforcement;
- do not expose arbitrary shell execution.

CE（社区版） should stay focused on the vertical slice.

---

## 13. Acceptance Criteria

版本 boundaries are clear when:

- CE（社区版） is recognized as the current implementation target;
- EE（企业版） is recognized as future private commercial planning;
- Cloud（云版） is recognized as future SaaS planning;
- `Implementation Target` documents are treated as current requirements;
- `Planning` documents are not treated as CE（社区版） v0.1 requirements;
- CE（社区版） reserves extension points without implementing future editions;
- CE（社区版） remains useful and open-source;
- EE（企业版） and Cloud（云版） remain compatible with the CE（社区版） governance kernel.

---

## 14. Summary

The `xtrape-capsule` product family should grow through editions without confusing the current implementation scope.

The most important edition boundary rule is:

> Build CE（社区版） first as a complete lightweight governance kernel, then let EE（企业版） and Cloud（云版） extend it without redefining it.
