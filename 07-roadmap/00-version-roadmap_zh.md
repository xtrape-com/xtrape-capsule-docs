---
status: draft
audience: founders
stability: unstable
last_reviewed: 2026-05-05
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 00-version-roadmap.md
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

# Version Roadmap

- Status: 实施指南
- Edition: 共享
- Priority: Medium
- Audience: founders, architects, product managers, backend developers, frontend developers, agent SDK developers, AI coding agents

This document 定义 the version roadmap for the `xtrape-capsule` product family.

The current implementation focus is **CE（社区版） v0.1**. CE（社区版） v0.1 should prove the complete lightweight Capsule
governance loop with Opstage（运维舞台） Backend, Opstage（运维舞台） UI, SQLite, and the Node.js Embedded Agent（代理） SDK.

EE（企业版） and Cloud（云版） are future commercialization tracks. They should influence extension-point design, but they must not expand the CE（社区版） v0.1 implementation scope.

---

## 1. Purpose

The purpose of this roadmap is to define:

- what should be built first;
- what belongs to CE（社区版） v0.1;
- what belongs to later CE（社区版） stabilization;
- when Agent（代理） modes should expand;
- when EE（企业版） private deployment should become relevant;
- when Cloud（云版） SaaS should become relevant;
- how to avoid mixing future roadmap items into the current implementation.

The key rule is:

> Build CE（社区版） v0.1 as a complete lightweight governance kernel before expanding editions, runtimes, Agent（代理） modes, and commercial packaging.

---

## 2. Roadmap Principle

The roadmap follows this sequence:

```text
1. CE v0.1 — prove the governance loop
2. CE v0.2/v0.3 — stabilize and improve the open-source kernel
3. CE v1.0 — publish a reliable community edition
4. EE — add enterprise private-deployment capabilities
5. Cloud — add hosted SaaS capabilities
```

Do not build EE（企业版） or Cloud（云版） infrastructure before CE（社区版） proves the product kernel.

---

## 3. Product Kernel

The product kernel is the Capsule governance loop:

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

Every roadmap stage should preserve this kernel.

Future versions may add scale, security, identity, observability, and commercialization, but they should not redefine the kernel.

---

## 4. CE（社区版） v0.1 Goal

CE（社区版） v0.1 goal:

> Deliver a lightweight, open-source, self-hosted, single-node Opstage（运维舞台） prototype that proves the full Capsule governance loop.

CE（社区版） v0.1 should be good enough for:

- local development;
- demo use;
- early open-source feedback;
- validating the Capsule/Agent（代理） model;
- proving the UI + Backend + Agent（代理） vertical slice;
- guiding future architecture decisions.

CE（社区版） v0.1 does not need to be enterprise-grade.

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
Docker quick start
```

This is the current implementation target.

---

## 6. CE（社区版） v0.1 Non-Goals

CE（社区版） v0.1 should not include:

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

These are future roadmap items.

---

## 7. CE（社区版） v0.1 Recommended 实现 Order

Recommended implementation order:

```text
1. Backend project scaffold
2. UI project scaffold
3. SQLite schema and persistence
4. Local admin authentication
5. Registration token model
6. Agent registration API
7. Agent token authentication
8. Node.js Agent SDK scaffold
9. Agent heartbeat
10. Service manifest report
11. Agent and service UI pages
12. Health and config metadata visibility
13. ActionDefinition model
14. Command creation from UI
15. Command polling from SDK
16. CommandResult reporting
17. AuditEvent model and UI
18. Dashboard summary
19. System health endpoint
20. Node.js demo Capsule Service
21. Docker quick start
22. Minimal documentation and release notes
```

The order may be adjusted during implementation, but the vertical governance loop should remain the priority.

---

## 8. CE（社区版） v0.1 Acceptance Criteria

CE（社区版） v0.1 is acceptable when:

- user can start Opstage（运维舞台） locally;
- user can log in as local admin;
- user can create a registration token;
- Node.js demo Capsule Service（胶囊服务） can register;
- Agent（代理） appears in UI;
- Capsule Service（胶囊服务） appears in UI;
- heartbeat status is visible;
- health status is visible;
- config metadata is visible;
- predefined actions are visible;
- user can run `echo` action;
- user can run `runHealthCheck` action;
- Backend creates Commands;
- Agent（代理） polls Commands;
- Agent（代理） reports CommandResults;
- UI displays CommandResult;
- AuditEvents are created and visible;
- stale/offline state is visible;
- sensitive values are masked;
- raw tokens are not logged;
- no arbitrary shell execution exists;
- Docker quick start can demonstrate the loop.

---

## 9. CE（社区版） v0.2 Direction

CE（社区版） v0.2 should stabilize the CE（社区版） kernel after v0.1 feedback.

Possible focus areas:

- improve UI usability;
- improve error handling;
- improve SDK developer experience;
- improve dashboard clarity;
- improve status and freshness calculation;
- improve audit filtering;
- improve Docker packaging;
- add better local development scripts;
- add more tests;
- add migration discipline;
- improve documentation.

CE（社区版） v0.2 should still avoid EE（企业版）/Cloud（云版） complexity.

---

## 10. CE（社区版） v0.3 Direction

CE（社区版） v0.3 may add selected open-source improvements if the kernel is stable.

Possible focus areas:

- better command lifecycle handling;
- simple Command expiration cleanup;
- simple health history if needed;
- better demo service examples;
- improved SDK logging and diagnostics;
- improved local settings page;
- optional PostgreSQL/MySQL experimental adapter only if strongly justified;
- better release packaging.

CE（社区版） v0.3 should remain lightweight.

---

## 11. CE（社区版） v1.0 Direction

CE（社区版） v1.0 should be a reliable community release.

Expected qualities:

- stable core concepts;
- stable Agent（代理） API;
- stable Node.js SDK API;
- stable SQLite deployment path;
- documented upgrade path;
- meaningful test coverage;
- reliable Docker quick start;
- clear security notes;
- clear CE（社区版）/EE（企业版）/Cloud（云版） boundaries;
- useful open-source experience.

CE（社区版） v1.0 should still be self-hosted and lightweight.

---

## 12. Agent（代理） Expansion Roadmap

Agent（代理） expansion should happen after the CE（社区版） Embedded Agent（代理） model is validated.

Recommended order:

```text
1. Node.js Embedded Agent
2. Sidecar Agent prototype
3. External Agent prototype
4. Java Embedded Agent SDK
5. Python Embedded Agent SDK
6. Go SDK or Go-based Agent runtime
7. Kubernetes Agent
```

This order is not fixed, but the first step is fixed:

```text
Node.js Embedded Agent first
```

---

## 13. Runtime Expansion Roadmap

Runtime expansion should happen after Node.js is stable.

Recommended order:

```text
1. Node.js Runtime
2. Java Runtime planning and prototype
3. Python Runtime planning and prototype
4. Go Runtime planning and prototype
5. Sidecar/External runtime adapters
6. Kubernetes runtime integration
```

Runtime expansion should preserve the same governance contract.

---

## 14. EE（企业版） Roadmap Direction

EE（企业版） should start after CE（社区版） has a stable kernel and real usage signals.

Potential EE（企业版） focus areas:

- PostgreSQL/MySQL official support;
- enterprise RBAC;
- SSO / OIDC / LDAP / SAML;
- audit export;
- audit retention configuration;
- alert rules;
- observability integrations;
- secret provider integrations;
- Sidecar Agent（代理）;
- External Agent（代理）;
- Java/Python/Go Agent（代理） SDKs;
- backup and restore tooling;
- high availability;
- Kubernetes / Helm deployment;
- support bundle;
- private deployment package;
- commercial support.

EE（企业版） should sell enterprise value, not cripple CE（社区版）.

---

## 15. Cloud（云版） Roadmap Direction

Cloud（云版） should start after CE（社区版）/EE（企业版） concepts are sufficiently validated.

Potential Cloud（云版） focus areas:

- hosted Backend and UI;
- Tenant / Organization / Workspace model;
- team invitations;
- subscription billing;
- usage metering;
- Cloud（云版） Agent（代理） Gateway;
- workspace-scoped registration tokens;
- managed audit retention;
- managed alerting;
- Cloud（云版） support workflows;
- data export and deletion workflows;
- Cloud（云版） operational monitoring;
- SaaS onboarding UX.

Cloud（云版） should remain compatible with the same Agent（代理） governance model.

---

## 16. Version Naming

Recommended version naming:

```text
CE v0.1
CE v0.2
CE v0.3
CE v1.0
EE Alpha
EE Beta
EE v1.0
Cloud Alpha
Cloud Beta
Cloud v1.0
```

Avoid using enterprise or Cloud（云版） version names before the CE（社区版） kernel is stable.

---

## 17. Release Artifact Direction

CE（社区版） release artifacts may include:

```text
source code
Docker image
Docker Compose example
Node Agent SDK package
Node demo Capsule Service
migration files
quick start guide
release notes
```

Future EE（企业版） artifacts may include:

```text
private Docker images
private deployment package
Helm chart
backup/restore scripts
support bundle tool
security hardening guide
upgrade guide
license or entitlement package if needed
```

Future Cloud（云版） artifacts are mainly hosted service releases and customer-facing onboarding flows.

---

## 18. 文档 Roadmap

文档 should evolve with versions.

### CE（社区版） v0.1 documentation

Required:

- quick start;
- architecture overview;
- Opstage（运维舞台） UI/Backend/Agent（代理） docs;
- Node Agent（代理） SDK guide;
- Node demo service guide;
- Docker quick start;
- security notes;
- troubleshooting.

### CE（社区版） v1.0 documentation

Add:

- upgrade guide;
- API reference;
- SDK reference;
- deployment guide;
- contribution guide;
- release process.

### EE（企业版） documentation

Add:

- enterprise deployment guide;
- RBAC guide;
- SSO guide;
- audit/compliance guide;
- observability integration guide;
- secret provider integration guide;
- backup/restore guide;
- support guide.

### Cloud（云版） documentation

Add:

- signup/onboarding guide;
- organization/workspace guide;
- Agent（代理） enrollment guide;
- billing guide;
- data export/deletion guide;
- Cloud（云版） support guide.

---

## 19. Roadmap Guardrails

Follow these guardrails:

1. Do not implement EE（企业版）/Cloud（云版） features in CE（社区版） v0.1.
2. Do not add multiple runtimes before Node.js is stable.
3. Do not add Sidecar/External Agent（代理） before Embedded Agent（代理） is stable.
4. Do not add alerting before status and freshness are reliable.
5. Do not add billing before Cloud（云版） exists.
6. Do not add license enforcement before EE（企业版） has real commercial demand.
7. Do not add arbitrary shell execution.
8. Do not store raw secrets by default.
9. Do not break CE（社区版） trust with artificial limitations.
10. Do not redefine the Capsule governance kernel per edition.

---

## 20. Decision Checkpoints

Before moving from CE（社区版） v0.1 to later roadmap stages, review these checkpoints.

### Before CE（社区版） v0.2

Ask:

- Does the full governance loop work?
- Is the Agent（代理） API usable?
- Is the Node SDK developer experience acceptable?
- Are status and freshness understandable?
- Are users able to run demo actions successfully?

### Before CE（社区版） v1.0

Ask:

- Are core APIs stable enough?
- Is upgrade/migration acceptable?
- Is documentation sufficient?
- Is the security boundary clear?
- Is CE（社区版） useful as an open-source product?

### Before EE（企业版）

Ask:

- Is there real private deployment demand?
- Which enterprise features are actually requested?
- Which database/deployment mode is required first?
- Which Agent（代理） expansion has the strongest demand?
- What support burden is acceptable?

### Before Cloud（云版）

Ask:

- Is there SaaS demand?
- Is multi-tenancy worth the added complexity?
- Is Agent（代理） Gateway required?
- Are billing and support workflows ready?
- Is operational responsibility acceptable?

---

## 21. Anti-Patterns

Avoid these roadmap anti-patterns.

### 21.1 Building all future editions at once

This slows CE（社区版） and makes the product unclear.

### 21.2 CE（社区版） as a broken demo

CE（社区版） should be genuinely useful.

### 21.3 Agent（代理） expansion before Agent（代理） basics

Embedded Agent（代理） should be stable before Sidecar/External Agent（代理）.

### 21.4 Runtime expansion before Node.js is stable

More runtimes should not come before a validated governance contract.

### 21.5 Commercial packaging before product value

License and entitlement systems should not consume early engineering capacity.

### 21.6 Observability platform before governance visibility

First make Agents, services, health, Commands, and AuditEvents visible.

---

## 22. Summary Roadmap

Recommended roadmap summary:

```text
CE v0.1
  Build the lightweight governance loop with Node.js Embedded Agent.

CE v0.2/v0.3
  Stabilize CE, improve DX, UI, tests, packaging, and docs.

CE v1.0
  Publish a reliable open-source community edition.

EE
  Add enterprise private-deployment capabilities based on real demand.

Cloud
  Add hosted SaaS capabilities after the governance model is mature.
```

---

## 23. Acceptance Criteria

This roadmap is acceptable when:

- CE（社区版） v0.1 scope is clear;
- CE（社区版） v0.1 non-goals are clear;
- Node.js Embedded Agent（代理） is clearly first;
- future Agent（代理） and runtime expansion is sequenced;
- EE（企业版） and Cloud（云版） are clearly future tracks;
- roadmap guardrails prevent scope creep;
- release and documentation directions are clear;
- CE（社区版） remains useful and open-source;
- future editions extend the same governance kernel.

---

## 24. Summary

The `xtrape-capsule` roadmap should prioritize a working, lightweight, open-source CE（社区版） kernel before expanding into enterprise and SaaS editions.

The most important roadmap rule is:

> Build the smallest complete governance loop first, then expand scale, runtime coverage, Agent（代理） modes, enterprise features, and Cloud（云版） hosting only after the kernel is proven.
