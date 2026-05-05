---
status: draft
audience: founders
stability: unstable
last_reviewed: 2026-05-05
edition: cloud
phase: future
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

# Opstage（运维舞台） Cloud（云版） 概述

- Status: Planning
- Edition: Cloud（云版）
- Priority: Future
- Audience: founders, product designers, architects, backend developers, cloud engineers, AI coding agents

This document 定义 the planning overview for **Opstage（运维舞台） Cloud（云版）**.

Opstage（运维舞台） Cloud（云版） is the future SaaS edition of the `xtrape-capsule` product family. It is not a CE（社区版） v0.1 implementation requirement.

---

## 1. Positioning

Opstage（运维舞台） Cloud（云版） is:

> A hosted SaaS control plane for Capsule Services, designed for teams that want managed governance without self-hosting Opstage（运维舞台） Backend.

Cloud（云版） should extend the same core governance model used by CE（社区版） and EE（企业版）:

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
Command delivery
    ↓
Command result
    ↓
Audit log
```

The difference is that Opstage（运维舞台） Backend and UI are hosted by the platform provider, while customer-side Agents connect outbound to the Cloud（云版） control plane.

---

## 2. Cloud（云版） Is Not CE（社区版） v0.1

Cloud（云版） is a future edition.

CE（社区版） v0.1 must not implement Cloud（云版）-only capabilities such as:

- multi-tenant SaaS control plane;
- subscription billing;
- organization and team management;
- cloud Agent（代理） gateway;
- managed alerting;
- managed audit retention;
- usage metering;
- Cloud（云版） SLA;
- customer onboarding automation;
- hosted compliance reports.

CE（社区版） should reserve extension points for Cloud（云版）, but Cloud（云版） must not become a dependency of CE（社区版） v0.1.

---

## 3. Cloud（云版） Product Goal

The goal of Opstage（运维舞台） Cloud（云版） is:

> Provide a managed, team-oriented, multi-tenant Opstage（运维舞台） service for customers who want to govern Capsule Services without operating the control plane themselves.

Cloud（云版） should reduce customer operational burden while preserving the same security principle:

> Customer-side Agents connect outbound to Cloud（云版）, and customer secrets should remain customer-controlled whenever possible.

---

## 4. Target Users

Opstage（运维舞台） Cloud（云版） is intended for:

- small teams that do not want to self-host;
- AI automation teams;
- integration service operators;
- agencies managing services for multiple customers;
- startups running many lightweight internal services;
- teams that need audit and visibility but not full enterprise private deployment;
- users who prefer managed upgrades, backups, and availability.

---

## 5. Target Scenarios

### 5.1 Managed governance for lightweight services

A team runs many Capsule Services across local servers, VPS instances, or private networks, and wants a hosted control plane.

### 5.2 Integration operations across environments

A team operates multiple integration services and wants centralized visibility for Agents, services, health, commands, and audits.

### 5.3 Agency or customer workspace management

An agency manages Capsule Services for multiple customers and needs workspace-level separation.

### 5.4 Remote Agent（代理） fleet visibility

Agents run in many customer-owned environments and connect outbound to Opstage（运维舞台） Cloud（云版）.

### 5.5 Managed audit and reporting

Teams want audit logs, reports, and operational history without maintaining their own database and backup process.

---

## 6. Cloud（云版） 架构 Direction

高-level Cloud（云版） architecture:

```text
Customer Environment
└── Capsule Services
    └── Agents
        ↓ outbound HTTPS

Opstage Cloud
├── Agent Gateway
├── Cloud Backend
├── Cloud UI
├── Multi-tenant Database
├── Audit Storage
├── Metrics / Event Pipeline
├── Billing / Subscription System
└── Notification / Alerting System
```

Cloud（云版） should keep the same core model as CE（社区版）:

```text
UI talks to Backend
Agent talks to Backend or Agent Gateway
Backend creates Commands
Agent polls or receives Commands
Agent reports results
Audit records the operation
```

---

## 7. Agent（代理） Connectivity Model

Cloud（云版） should use an outbound-first Agent（代理） model.

Agents should connect from customer environments to Opstage（运维舞台） Cloud（云版）:

```text
Agent -> Opstage Cloud
```

Cloud（云版） should not require inbound access into customer private networks.

This 支持:

- NAT environments;
- home servers;
- private data centers;
- customer-controlled firewalls;
- fewer exposed ports;
- future managed Agent（代理） gateway.

---

## 8. Agent（代理） Gateway

Cloud（云版） may introduce an Agent（代理） Gateway layer.

Responsibilities may include:

- terminating Agent（代理） connections;
- validating Agent（代理） tokens;
- routing Agent（代理） traffic to tenant/workspace context;
- rate limiting;
- buffering command delivery;
- supporting WebSocket or streaming channels;
- collecting connection telemetry;
- isolating customer traffic.

CE（社区版） v0.1 does not need Agent（代理） Gateway.

CE（社区版）'s HTTP heartbeat and polling model should remain compatible with future Cloud（云版） gateway evolution.

---

## 9. Multi-Tenancy

Cloud（云版） requires a multi-tenant model.

Future Cloud（云版） concepts may include:

```text
Tenant
Organization
Workspace
Team
User
Role
Subscription
UsageRecord
BillingAccount
```

CE（社区版） v0.1 should not implement these first-class models.

However, CE（社区版） already reserving `workspaceId` helps future migration.

---

## 10. Organization and Workspace Model

Recommended Cloud（云版） hierarchy:

```text
Organization
    ↓
Workspace
    ↓
Agents
    ↓
Capsule Services
```

Potential concepts:

- Organization owns billing and members;
- Workspace groups Agents and Capsule Services;
- User may belong to multiple Organizations;
- Role assignments may be scoped to Organization or Workspace.

This is future planning only.

---

## 11. Identity and Access Management

Cloud（云版） should support stronger identity than CE（社区版）.

Potential Cloud（云版） features:

- email/password login;
- OAuth login;
- team invites;
- organization roles;
- workspace roles;
- service accounts;
- API keys;
- optional SSO for higher plans;
- audit of user access.

CE（社区版） v0.1 should only implement local admin authentication.

---

## 12. Billing and Subscription

Cloud（云版） may include subscription billing.

Possible billing dimensions:

- number of Agents;
- number of Capsule Services;
- command volume;
- health/report retention;
- audit retention;
- alerting volume;
- team seats;
- premium Agent（代理） modes;
- enterprise support.

Billing is not part of CE（社区版） v0.1.

Cloud（云版） billing should not change the core Agent（代理） and Command contracts.

---

## 13. Data Boundary

Cloud（云版） must define a clear data boundary.

Cloud（云版） may store:

- Agent（代理） metadata;
- Capsule Service（胶囊服务） metadata;
- manifest metadata;
- health reports;
- config metadata;
- command metadata;
- command results;
- audit events;
- usage records;
- alert records.

Cloud（云版） should avoid storing raw customer secrets by default.

Sensitive values should use:

```text
secretRef
```

or remain in:

- customer environment;
- Agent（代理）-local secret store;
- customer-managed Vault;
- customer cloud secret manager.

---

## 14. Secret Strategy

Cloud（云版） should prefer customer-controlled secrets.

Recommended principle:

> Cloud（云版） stores governance metadata and secret references, not raw operational secrets.

Future Cloud（云版） may support optional managed secrets, but this should be explicit and plan-dependent.

Possible secretRef forms:

```text
agent-local://agent-001/secrets/chatgpt/account-001
customer-vault://path/to/secret
cloud-secret://org/workspace/key
```

CE（社区版） v0.1 only needs to recognize and display `secretRef` safely.

---

## 15. Command Delivery Evolution

CE（社区版） v0.1 uses HTTP polling.

Cloud（云版） may evolve command delivery to:

- WebSocket;
- Server-Sent Events;
- gRPC streaming;
- long polling;
- message queue backed delivery;
- Agent（代理） Gateway channels.

The Command model should remain stable across editions.

Transport may change, but these concepts should remain:

```text
Command
CommandResult
Agent
CapsuleService
ActionDefinition
AuditEvent
```

---

## 16. Observability and Alerts

Cloud（云版） may provide managed observability beyond CE（社区版）.

Potential Cloud（云版） capabilities:

- health history;
- uptime history;
- command success rate;
- Agent（代理） connection history;
- audit trends;
- alert rules;
- notification channels;
- dashboards;
- customer reports.

Cloud（云版） should not try to replace all specialized observability platforms at first.

The first Cloud（云版） observability value should be focused on Capsule governance data.

---

## 17. Audit and Retention

Cloud（云版） may provide managed audit retention and export.

Potential features:

- configurable retention periods;
- audit export;
- compliance-oriented reports;
- immutable storage option;
- audit search;
- actor and resource filters;
- workspace-level audit views.

CE（社区版） v0.1 only needs lightweight audit logs.

---

## 18. Cloud（云版） 部署 架构

Possible Cloud（云版） deployment components:

```text
Cloud UI
Cloud Backend API
Agent Gateway
Worker / Scheduler
Database
Cache
Queue
Object Storage
Audit Storage
Metrics Storage
Billing Service
Notification Service
```

Cloud（云版） may require:

- horizontal scaling;
- database migrations;
- tenant isolation;
- backup and restore;
- monitoring;
- incident response;
- rate limiting;
- abuse prevention.

None of these should be required by CE（社区版） v0.1.

---

## 19. Cloud（云版） 安全 Direction

Cloud（云版） security requirements are stronger than CE（社区版）.

Future Cloud（云版） should consider:

- tenant isolation;
- organization-level access control;
- workspace-level roles;
- Agent（代理） token rotation;
- rate limiting;
- audit retention;
- secure secret boundary;
- secure Agent（代理） Gateway;
- encrypted transport;
- encrypted storage;
- incident logging;
- abuse prevention;
- data export and deletion controls.

Cloud（云版） security design should be documented separately before implementation.

---

## 20. Cloud（云版） vs EE（企业版）

Cloud（云版） and EE（企业版） should share the same core contracts but differ in delivery model.

||Area|EE（企业版）|Cloud（云版）||
|---|---|---|
||部署|customer private environment|hosted by provider||
||Database|customer-managed|provider-managed||
||Identity|enterprise-controlled|hosted organization/team model||
||Billing|license/subscription contract|SaaS subscription||
||Agent（代理） connection|customer private network|outbound to Cloud（云版） gateway||
||Operations|customer or vendor support|provider-operated||
||Data boundary|customer-controlled|shared responsibility||

Both should preserve the CE（社区版） governance kernel.

---

## 21. CE（社区版） Reservations for Cloud（云版）

CE（社区版） should reserve these Cloud（云版）-compatible ideas:

```text
workspaceId
Agent outbound communication
Agent registration token
Agent token
Command model
CommandResult model
AuditEvent model
secretRef
runtime
agentMode
metadataJson
status values
```

CE（社区版） should not implement:

```text
Tenant
Organization
Billing
Subscription
Agent Gateway
Cloud plans
Usage metering
Cloud user invites
Cloud team management
```

---

## 22. Cloud（云版） MVP Candidate

A future Cloud（云版） MVP may include:

- hosted Opstage（运维舞台） Backend and UI;
- user account registration;
- organization creation;
- one or more workspaces;
- Agent（代理） registration token creation;
- remote Agent（代理） heartbeat;
- Capsule Service（胶囊服务） list;
- health visibility;
- command execution;
- audit logs;
- basic subscription plan or private beta access.

This is not part of CE（社区版） v0.1.

---

## 23. Risks

### 23.1 Data trust risk

Customers may not want governance metadata in Cloud（云版）.

Mitigation:

- keep CE（社区版） and EE（企业版） available;
- document data boundary;
- avoid raw secrets;
- provide export and deletion controls.

### 23.2 Agent（代理） connectivity risk

Customer networks may block outbound connections.

Mitigation:

- use standard HTTPS;
- support proxy configuration;
- provide clear connectivity diagnostics.

### 23.3 Cost risk

Cloud（云版） telemetry and audit retention can become expensive.

Mitigation:

- plan retention tiers;
- summarize where possible;
- avoid storing large logs in command/audit payloads.

### 23.4 Scope risk

Cloud（云版） can become too broad too quickly.

Mitigation:

- start with hosted CE（社区版）-like governance;
- add multi-tenant and billing carefully;
- avoid becoming a full observability platform too early.

---

## 24. Cloud（云版） Planning Non-Goals

This document does not define final Cloud（云版） implementation details for:

- billing provider;
- tenant isolation architecture;
- production database choice;
- cloud infrastructure provider;
- exact Agent（代理） Gateway protocol;
- exact subscription plans;
- exact compliance commitments;
- exact SLA.

These require separate design documents when Cloud（云版） becomes an active target.

---

## 25. Summary

Opstage（运维舞台） Cloud（云版） is the future hosted SaaS edition of the Capsule governance model.

It should extend the CE（社区版） kernel into a managed, team-oriented, multi-tenant control plane.

The most important Cloud（云版） planning rule is:

> Cloud（云版） should be a managed evolution of the same Agent（代理）-based governance model, not a different product that breaks CE（社区版） compatibility.
