<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 03-cloud-roadmap.md
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

# Cloud（云版） Roadmap

- Status: Planning
- Edition: Cloud（云版）
- Priority: Future
- Audience: founders, architects, product managers, SaaS platform engineers, backend developers, frontend developers, agent SDK developers, security reviewers, AI coding agents

This document 定义 the roadmap for **Opstage（运维舞台） Cloud（云版） / SaaS Cloud（云版） 版本**.

Cloud（云版） is the future hosted SaaS edition of the `xtrape-capsule` product family. It should provide managed Opstage（运维舞台） hosting, multi-tenant organizations and workspaces, Cloud（云版） Agent（代理） connectivity, billing, usage metering, managed audit retention, managed alerting, and SaaS support workflows.

Cloud（云版） is not a CE（社区版） v0.1 implementation requirement.

---

## 1. Purpose

The purpose of the Cloud（云版） roadmap is to define:

- when Cloud（云版） should start;
- what Cloud（云版） should add beyond CE（社区版） and EE（企业版）;
- how Cloud（云版） should preserve the same Capsule governance kernel;
- how multi-tenancy should be introduced;
- how Cloud（云版） Agent（代理） connectivity may work;
- what billing and usage metering may include;
- what data boundaries must be respected;
- how to avoid building SaaS infrastructure too early.

The key rule is:

> Cloud（云版） should host and operate the proven Capsule governance model as a managed SaaS, not redefine the model before CE（社区版） is stable.

---

## 2. Cloud（云版） Product Positioning

Cloud（云版） is:

> A hosted SaaS edition of Opstage（运维舞台） for users who want managed Capsule Service（胶囊服务） governance without operating Opstage（运维舞台） themselves.

Cloud（云版） should be suitable for:

- teams that do not want self-hosting;
- small companies that want quick onboarding;
- users who prefer managed upgrades;
- multi-user collaboration;
- managed audit retention;
- managed alerting;
- Cloud（云版）-based support workflows;
- usage-based or subscription-based commercial plans.

Cloud（云版） should remain compatible with the same Agent（代理）-based governance model used by CE（社区版） and EE（企业版）.

---

## 3. Relationship with CE（社区版） and EE（企业版）

CE（社区版） proves the open-source governance kernel.

EE（企业版） strengthens private enterprise deployment.

Cloud（云版） hosts the governance kernel as SaaS.

Recommended relationship:

```text
CE
  open-source self-hosted kernel

EE
  private enterprise deployment of the kernel

Cloud
  hosted SaaS operation of the kernel
```

Cloud（云版） should not force a different Agent（代理） model unless Cloud（云版）-specific connectivity requires additional gateway components.

---

## 4. Cloud（云版） Start Conditions

Cloud（云版） should not start too early.

Recommended start conditions:

- CE（社区版） proves the full governance loop;
- Agent（代理） API is reasonably stable;
- Node Agent（代理） SDK is usable;
- Command and Action model is validated;
- basic security boundary is clear;
- real users want managed hosting;
- onboarding flow is understood;
- operating the service is feasible;
- billing/support responsibilities are acceptable.

Before these conditions, engineering should remain focused on CE（社区版） and possibly EE（企业版）.

---

## 5. Cloud（云版） Non-Goals During CE（社区版） v0.1

During CE（社区版） v0.1, do not implement:

```text
Tenant system
Organization system
Cloud workspace management
team invitations
subscription billing
usage metering
Cloud Agent Gateway
multi-tenant rate limiting
Cloud support portal
Cloud onboarding wizard
managed audit retention
managed alerting
SaaS data export/deletion workflow
Cloud operational telemetry
```

These are Cloud（云版） roadmap items, not CE（社区版） v0.1 tasks.

---

## 6. Cloud（云版） Capability Areas

Cloud（云版） may add capabilities in these areas:

```text
SaaS tenancy
Organizations and Workspaces
User accounts and teams
Cloud Agent connectivity
Agent Gateway
Billing and subscriptions
Usage metering
Managed audit retention
Managed alerting
Cloud support workflows
Data export and deletion
Operational monitoring
SaaS security controls
```

Each capability should be added only after the governance kernel is stable.

---

## 7. Cloud（云版） Phase 0 — Kernel and Demand Validation

Before Cloud（云版） implementation starts, validate:

- CE（社区版） governance kernel works;
- users understand Agent（代理） registration;
- users can run predefined actions safely;
- users understand CommandResult and AuditEvents;
- Agent（代理） token model is stable;
- secretRef boundary is clear;
- there is demand for hosted Opstage（运维舞台）;
- Cloud（云版） operation cost is acceptable.

Cloud（云版） should not be built only because SaaS is commercially attractive. The hosted product must solve a real operational problem.

---

## 8. Cloud（云版） Phase 1 — SaaS Foundation

Cloud（云版） Phase 1 should establish SaaS foundations.

Possible capabilities:

- hosted Opstage（运维舞台） Backend;
- hosted Opstage（运维舞台） UI;
- user signup/login;
- Organization model;
- Workspace model;
- default organization/workspace creation;
- user profile;
- team invitation basics;
- Cloud（云版）-safe configuration;
- SaaS deployment pipeline;
- production database;
- SaaS monitoring and backups;
- basic support contact flow.

Goal:

> Make Opstage（运维舞台） usable as a hosted multi-user service.

---

## 9. Cloud（云版） Phase 2 — Agent（代理） Enrollment and Connectivity

Cloud（云版） Phase 2 should focus on connecting customer Agents to Cloud（云版）.

Possible capabilities:

- workspace-scoped registration tokens;
- Agent（代理） enrollment instructions;
- Cloud（云版） Agent（代理） connection diagnostics;
- Agent（代理） token management;
- Agent（代理） status visibility;
- outbound-first Agent（代理） connectivity;
- Cloud（云版）-safe command polling;
- Agent（代理） connection troubleshooting;
- optional Agent（代理） Gateway planning.

Initial Cloud（云版） can still use HTTP polling if it is reliable enough.

Agent（代理） Gateway should be added only if required.

---

## 10. Cloud（云版） Phase 3 — Cloud（云版） Agent（代理） Gateway

Cloud（云版） Agent（代理） Gateway may be needed for scalable, secure, and observable Agent（代理） connectivity.

Possible responsibilities:

- Agent（代理） connection termination;
- workspace routing;
- Agent（代理） authentication;
- rate limiting;
- connection diagnostics;
- command delivery optimization;
- WebSocket or streaming connection support;
- traffic isolation;
- usage metering hooks;
- abuse protection.

Possible protocols:

```text
HTTP polling
long polling
WebSocket
gRPC streaming
message queue-backed delivery
```

Recommended approach:

```text
Start with HTTP polling. Add Gateway and streaming only after need is proven.
```

---

## 11. Cloud（云版） Phase 4 — Billing and Usage Metering

Cloud（云版） Phase 4 may add billing and usage metering.

Possible billing dimensions:

```text
number of Organizations
number of Workspaces
number of users
number of Agents
number of Capsule Services
Command execution count
AuditEvent retention
alert rule count
notification volume
support tier
```

Recommended initial billing model:

```text
subscription tier + Agent/Service capacity limits
```

Avoid overly granular billing too early.

---

## 12. Cloud（云版） Phase 5 — Managed Audit and Alerting

Cloud（云版） may provide managed audit and alerting.

Possible capabilities:

- audit retention by plan;
- audit export by plan;
- audit search;
- managed alert rules;
- Agent（代理） offline alerts;
- service DOWN alerts;
- command failure alerts;
- notification channels;
- alert delivery history;
- alert usage limits.

Managed audit and alerting are strong SaaS values because customers do not need to operate these systems themselves.

---

## 13. Cloud（云版） Phase 6 — Data Management and Compliance Workflows

Cloud（云版） must provide customer data control workflows.

Possible capabilities:

- workspace data export;
- organization data export;
- audit export;
- Agent（代理） metadata export;
- account deletion workflow;
- workspace deletion workflow;
- data retention controls;
- support access audit;
- privacy documentation;
- regional data planning if needed.

Cloud（云版） data control should be designed before serious commercial launch.

---

## 14. Cloud（云版） Phase 7 — SaaS Operations and Support Maturity

Cloud（云版） operation requires product and engineering maturity.

Possible capabilities:

- service-level monitoring;
- uptime reporting;
- incident response process;
- support portal;
- customer support access audit;
- status page;
- backup verification;
- disaster recovery plan;
- release management;
- feature flag management;
- security review process.

Cloud（云版） means the provider owns runtime responsibility.

---

## 15. Cloud（云版） Tenancy Model

Cloud（云版） likely needs a tenancy model.

Recommended hierarchy:

```text
Tenant or Account
  ↓
Organization
  ↓
Workspace
  ↓
Agents
  ↓
Capsule Services
```

Depending on product complexity, `Tenant` and `Organization` may be merged early.

Recommended early Cloud（云版） hierarchy:

```text
Organization
  ↓
Workspace
  ↓
Agents / Capsule Services
```

Do not add full tenancy to CE（社区版） v0.1.

---

## 16. Organization Model

Organization represents a customer or team.

Possible fields:

```text
organizationId
name
slug
plan
billingStatus
createdAt
updatedAt
```

Organization may own:

- users;
- workspaces;
- billing account;
- plan limits;
- audit retention policy;
- support tier.

Organization is Cloud（云版） scope, not CE（社区版） v0.1 scope.

---

## 17. Workspace Model

Workspace groups Agents and Capsule Services.

Possible fields:

```text
workspaceId
organizationId
name
slug
region if needed
createdAt
updatedAt
```

Workspace may own:

- registration tokens;
- Agents;
- Capsule Services;
- Commands;
- CommandResults;
- AuditEvents;
- alert rules;
- settings.

CE（社区版） may reserve `workspaceId`, but Cloud（云版） gives it real multi-workspace semantics.

---

## 18. User and Team Model

Cloud（云版） should support team collaboration.

Possible capabilities:

- user signup;
- organization membership;
- invitation workflow;
- roles;
- workspace access;
- user profile;
- password reset;
- optional SSO in later paid tiers;
- audit for membership changes.

Cloud（云版） user accounts differ from CE（社区版） local admin.

---

## 19. Cloud（云版） Identity Direction

Cloud（云版） identity may start simple and evolve.

Possible stages:

```text
email/password login
email verification
password reset
team invitations
OAuth login
organization roles
SSO for enterprise plans
SCIM if needed
```

Cloud（云版） identity is not CE（社区版） v0.1 scope.

---

## 20. Agent（代理） Connectivity Boundary

Cloud（云版） Agent（代理） connectivity must remain outbound-first from customer environments where possible.

Recommended rule:

```text
Agent -> Cloud
```

Cloud（云版） should not require inbound network access into customer services.

This is especially important for private networks, NAT, and security-sensitive environments.

---

## 21. Cloud（云版） 安全 Boundary

Cloud（云版） must be stricter than CE（社区版） because it is multi-tenant.

安全 requirements:

- tenant/workspace isolation;
- Agent（代理） token isolation;
- user authentication;
- authorization checks;
- rate limiting;
- audit logging;
- sensitive value masking;
- secretRef boundary;
- no raw secret storage by default;
- abuse protection;
- support access auditing;
- secure session handling;
- secure billing integration.

Cloud（云版） must not rely on UI-only enforcement.

---

## 22. Cloud（云版） Data Boundary

Cloud（云版） should store governance metadata, not raw customer secrets by default.

Cloud（云版） may store:

- organization metadata;
- user metadata;
- workspace metadata;
- Agent（代理） metadata;
- Capsule Service（胶囊服务） metadata;
- health reports;
- config metadata;
- action metadata;
- Commands;
- CommandResults;
- AuditEvents;
- alert rules;
- billing metadata.

Cloud（云版） should not store by default:

- raw passwords for customer systems;
- raw OAuth tokens for third-party accounts;
- raw browser cookies;
- private keys;
- account credentials;
- customer business records;
- raw browser sessions.

Use `secretRef`, customer-side secret storage, or enterprise secret provider integration where needed.

---

## 23. Cloud（云版） Plans

Cloud（云版） may use simple commercial plans.

Candidate plans:

```text
Free
Team
Business
Enterprise
```

### 23.1 Free

Possible focus:

- small number of Agents;
- limited audit retention;
- basic actions;
- community support.

### 23.2 Team

Possible focus:

- more Agents and services;
- team members;
- longer audit retention;
- basic alerts.

### 23.3 Business

Possible focus:

- larger capacity;
- advanced alerts;
- audit export;
- priority support;
- SSO option.

### 23.4 Enterprise

Possible focus:

- custom limits;
- enterprise SSO;
- compliance support;
- dedicated support;
- data residency if needed;
- custom SLA.

Plans should remain simple until usage patterns are known.

---

## 24. CE（社区版）/EE（企业版）/Cloud（云版） Compatibility

Cloud（云版） should remain conceptually compatible with CE（社区版） and EE（企业版）.

共享 concepts:

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
secretRef
```

Cloud（云版） may add:

```text
Organization
Workspace
Subscription
UsageRecord
PlanLimit
CloudAgentConnection
AlertRule
NotificationChannel
```

but it should not redefine the shared concepts.

---

## 25. Cloud（云版） Migration Paths

Potential migration paths:

```text
CE -> Cloud
EE -> Cloud
Cloud -> EE
Cloud -> CE export
```

Not all paths need to be automated early.

Cloud（云版） should at least support data export for customer control.

Important export data:

- Agents;
- Capsule Services;
- manifests;
- Commands;
- CommandResults;
- AuditEvents;
- settings;
- alert rules if implemented.

SecretRefs may require customer-specific handling.

---

## 26. Cloud（云版） 文档 Requirements

Cloud（云版） documentation should include:

- Cloud（云版） overview;
- signup and onboarding guide;
- organization/workspace guide;
- Agent（代理） enrollment guide;
- Node Agent（代理） SDK Cloud（云版） guide;
- registration token guide;
- security and data boundary guide;
- billing guide;
- audit retention guide;
- alerting guide;
- data export/deletion guide;
- troubleshooting guide;
- support guide.

Cloud（云版） documentation should be user-facing and operationally clear.

---

## 27. Cloud（云版） Risks

### 27.1 Building Cloud（云版） too early

Risk:

- CE（社区版） remains unfinished and SaaS complexity slows product validation.

Mitigation:

- require CE（社区版） kernel validation first.

### 27.2 Multi-tenancy complexity

Risk:

- tenancy bugs create security and data isolation risks.

Mitigation:

- design isolation carefully;
- test tenant boundaries;
- keep early hierarchy simple.

### 27.3 Agent（代理） connectivity complexity

Risk:

- customer environments differ widely.

Mitigation:

- keep outbound-first model;
- start with simple polling;
- add Gateway only after need is proven.

### 27.4 Data and privacy risk

Risk:

- Cloud（云版） stores more data than necessary.

Mitigation:

- store governance metadata only;
- preserve secretRef boundary;
- provide export/deletion workflows.

### 27.5 Operational responsibility

Risk:

- SaaS requires monitoring, support, backups, incident response, and reliability.

Mitigation:

- do not launch Cloud（云版） before operational readiness.

---

## 28. Cloud（云版） Roadmap Guardrails

Guardrails:

1. Do not start Cloud（云版） before CE（社区版） kernel works.
2. Do not add Cloud（云版） tenancy to CE（社区版） v0.1.
3. Do not redefine Agent（代理） and Command concepts for Cloud（云版）.
4. Keep Agent（代理） connectivity outbound-first.
5. Start with HTTP polling before Gateway/streaming unless clearly needed.
6. Do not store raw customer secrets by default.
7. Do not build complex billing before usage model is clear.
8. Do not overcomplicate plans before product-market fit.
9. Do not launch Cloud（云版） without backup and incident basics.
10. Do not let Cloud（云版） planning expand CE（社区版） v0.1 scope.

---

## 29. Decision Checkpoints

Before starting Cloud（云版）, ask:

- Is CE（社区版） v0.1 working end to end?
- Is there demand for managed hosting?
- Is the Agent（代理） API stable enough?
- Is the Node Agent（代理） SDK easy enough for onboarding?
- Is multi-tenancy worth the complexity?
- Can we operate the service reliably?
- What data will Cloud（云版） store?
- What data must never be stored?
- What billing model is simple enough?
- What support commitment is realistic?

Before adding Agent（代理） Gateway, ask:

- Is HTTP polling insufficient?
- Are connection counts too high?
- Is command latency a real problem?
- Are diagnostics insufficient?
- Is the added operational complexity justified?

---

## 30. Cloud（云版） Roadmap Summary

Recommended Cloud（云版） roadmap summary:

```text
Cloud Phase 0
  Validate CE kernel and managed-hosting demand.

Cloud Phase 1
  Build SaaS foundation: hosted UI/Backend, users, organizations, workspaces.

Cloud Phase 2
  Build Agent enrollment and outbound connectivity.

Cloud Phase 3
  Add Agent Gateway only if required.

Cloud Phase 4
  Add billing and usage metering.

Cloud Phase 5
  Add managed audit and alerting.

Cloud Phase 6
  Add data export, deletion, and compliance workflows.

Cloud Phase 7
  Mature SaaS operations and support.
```

The exact order may change, but Cloud（云版） must not precede CE（社区版） kernel validation.

---

## 31. Acceptance Criteria

This Cloud（云版） roadmap is acceptable when:

- Cloud（云版） is clearly future, not CE（社区版） v0.1;
- Cloud（云版） is positioned as hosted SaaS;
- Cloud（云版） preserves the same Capsule governance kernel;
- Cloud（云版） start conditions are clear;
- multi-tenancy is introduced deliberately;
- Agent（代理） Gateway is optional and demand-driven;
- billing and metering are future staged capabilities;
- data boundary and secretRef rules are explicit;
- Cloud（云版） operational responsibilities are acknowledged;
- Cloud（云版） guardrails prevent CE（社区版） scope creep.

---

## 32. Summary

Cloud（云版） should become the hosted SaaS edition after the CE（社区版） governance kernel is proven and managed-hosting demand is clear.

It should provide hosted Opstage（运维舞台）, organizations, workspaces, managed Agent（代理） connectivity, billing, audit retention, alerting, support, and operational reliability while preserving the same Capsule governance model.

The most important Cloud（云版） roadmap rule is:

> Build Cloud（云版） only after the kernel is proven, keep Agent（代理） connectivity outbound-first, and store governance metadata without taking ownership of customer secrets.
