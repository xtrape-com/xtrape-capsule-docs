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
原始文件 / Original File: 01-cloud-planned-capabilities.md
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

# Cloud（云版） Planned Capabilities

- Status: Planning
- Edition: Cloud（云版）
- Priority: Future
- Audience: founders, product designers, architects, cloud engineers, backend developers, AI coding agents

This document 定义 the planned capabilities for **Opstage（运维舞台） Cloud（云版）**.

Opstage（运维舞台） Cloud（云版） is the future hosted SaaS edition of the `xtrape-capsule` product family. It is not a CE（社区版） v0.1 implementation requirement.

---

## 1. Purpose

The purpose of this document is to define:

- what capabilities Opstage（运维舞台） Cloud（云版） may provide;
- how Cloud（云版） capabilities relate to the CE（社区版） governance kernel;
- which Cloud（云版） capabilities may become MVP candidates;
- which capabilities should remain long-term planning items;
- which Cloud（云版） capabilities must not be pulled into CE（社区版） v0.1;
- how Cloud（云版） should preserve compatibility with CE（社区版） and EE（企业版）.

The core rule is:

> Cloud（云版） extends the Capsule governance model as a managed SaaS service, but CE（社区版） v0.1 must remain lightweight and self-hosted.

---

## 2. Capability Layers

Opstage（运维舞台） Cloud（云版） capabilities can be grouped into layers:

```text
Core Governance Layer
Team and Tenant Layer
Agent Connectivity Layer
Managed Operations Layer
Observability and Alerting Layer
Audit and Compliance Layer
Billing and Commercial Layer
Integration Layer
Platform Operations Layer
```

Cloud（云版） does not need to implement all layers in the first release.

---

## 3. Core Governance Layer

The Core Governance Layer is inherited from CE（社区版）.

It 包括:

- Agent（代理） registration;
- Agent（代理） token authentication;
- Capsule Service（胶囊服务） report;
- manifest storage;
- heartbeat;
- health visibility;
- config visibility;
- predefined actions;
- Commands;
- CommandResults;
- AuditEvents;
- status and freshness calculation.

These capabilities should remain compatible with CE（社区版） contracts.

Cloud（云版） may extend implementation, but should not break the shared concepts:

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
```

---

## 4. Team and Tenant Layer

Cloud（云版） requires team-oriented SaaS capabilities.

Planned concepts:

```text
Tenant
Organization
Workspace
Team
User
Role
Membership
Invitation
```

### 4.1 Organization management

Possible capabilities:

- create organization;
- invite users;
- manage members;
- manage organization settings;
- view organization audit;
- manage billing ownership.

### 4.2 Workspace management

Possible capabilities:

- create workspaces;
- switch workspace;
- assign Agents to workspace;
- view workspace services;
- workspace-level audit;
- workspace-level settings;
- workspace-level quotas.

### 4.3 Team collaboration

Possible capabilities:

- user invites;
- role assignment;
- activity feed;
- shared dashboards;
- command history visibility;
- audit visibility by workspace.

### 4.4 CE（社区版） relationship

CE（社区版） v0.1 should not implement full organization, tenant, team, or billing models.

CE（社区版） may reserve `workspaceId`, but Cloud（云版） owns the full multi-tenant model.

---

## 5. Identity and Access Capabilities

Cloud（云版） should support stronger identity than CE（社区版）.

Planned capabilities:

- email/password login;
- OAuth login;
- user invitations;
- organization roles;
- workspace roles;
- service accounts;
- API keys;
- optional SSO for higher plans;
- audit of identity operations.

Future enterprise-oriented Cloud（云版） plans may include:

- OIDC;
- SAML;
- SCIM;
- MFA enforcement;
- domain verification;
- enterprise user lifecycle controls.

CE（社区版） v0.1 should only implement local admin login.

---

## 6. Agent（代理） Connectivity Layer

Cloud（云版） should provide robust outbound Agent（代理） connectivity.

### 6.1 Basic Agent（代理） connectivity

Minimum Cloud（云版）-compatible model:

```text
Agent -> Opstage Cloud over HTTPS
```

Agents should not require inbound access from Cloud（云版） to customer networks.

### 6.2 Agent（代理） Gateway

Cloud（云版） may introduce Agent（代理） Gateway.

Possible capabilities:

- terminate Agent（代理） connections;
- validate Agent（代理） tokens;
- route traffic by tenant and workspace;
- support HTTP polling compatibility;
- support WebSocket or streaming mode;
- rate-limit Agent（代理） traffic;
- provide Agent（代理） connection diagnostics;
- buffer delivery metadata;
- isolate customer traffic.

### 6.3 Agent（代理） connection diagnostics

Possible diagnostics:

- last connected time;
- last heartbeat time;
- connection region;
- token status;
- error count;
- latency estimate;
- rejected requests;
- version compatibility warnings.

### 6.4 Agent（代理） token management

Possible capabilities:

- token rotation;
- token revocation;
- scoped Agent（代理） tokens;
- expiration policies;
- Agent（代理） enrollment policies;
- registration token expiration and one-time use.

CE（社区版） v0.1 should support basic registration token and Agent（代理） token, but not Cloud（云版） Agent（代理） Gateway.

---

## 7. Command Delivery Capabilities

CE（社区版） uses HTTP polling.

Cloud（云版） may support more delivery modes.

### 7.1 Planned delivery modes

Possible delivery modes:

```text
HTTP polling
long polling
WebSocket
Server-Sent Events
gRPC streaming
queue-backed delivery
Agent Gateway channel
```

### 7.2 Command reliability

Possible Cloud（云版） capabilities:

- delivery acknowledgement;
- retry policy;
- command timeout policy;
- command cancellation;
- command priority;
- command scheduling;
- per-service command concurrency limits;
- per-resource locks;
- long-running command progress.

### 7.3 Compatibility rule

Transport may change, but the Command model should remain stable.

Cloud（云版） should still use:

```text
Command
CommandResult
CommandStatus
AuditEvent
```

---

## 8. Managed Operations Layer

Cloud（云版） may provide managed operational capabilities beyond CE（社区版）.

Possible capabilities:

- managed Backend upgrades;
- managed database backups;
- managed audit retention;
- system health checks;
- Agent（代理） fleet overview;
- version compatibility checks;
- operational reports;
- customer support diagnostics;
- service inventory history.

Cloud（云版） should reduce operational burden for users who do not want to self-host Opstage（运维舞台）.

---

## 9. Observability and Alerting Layer

Cloud（云版） may provide managed observability focused on Capsule governance data.

### 9.1 Health history

Possible capabilities:

- health timeline;
- uptime history;
- stale duration;
- Agent（代理） connection history;
- service status trend.

### 9.2 Command analytics

Possible capabilities:

- command success rate;
- command failure rate;
- average execution time;
- most frequent actions;
- failed action trends;
- command volume by workspace.

### 9.3 Alerting

Possible alert rules:

- Agent（代理） offline;
- service stale;
- service unhealthy;
- command failed;
- command timeout;
- registration token used;
- abnormal command volume.

### 9.4 Notification channels

Possible channels:

- email;
- Slack;
- Telegram;
- webhook;
- SMS for higher plans;
- incident management integrations.

### 9.5 Boundary

Cloud（云版） should not try to replace full observability platforms in the first phase.

The first observability scope should be Capsule governance data, not arbitrary logs, metrics, and traces.

---

## 10. Audit and Compliance Layer

Cloud（云版） may provide stronger audit capabilities than CE（社区版）.

Possible capabilities:

- audit retention tiers;
- audit export;
- immutable audit storage option;
- actor/resource filters;
- audit search;
- audit reports;
- workspace-level audit views;
- organization-level audit views;
- audit event streaming;
- SIEM integration;
- compliance report packages.

Cloud（云版） audit should preserve the same base AuditEvent shape used by CE（社区版）.

CE（社区版） v0.1 only needs lightweight audit logs.

---

## 11. Billing and Commercial Layer

Cloud（云版） may include commercial SaaS capabilities.

### 11.1 Billing concepts

Possible concepts:

```text
Plan
Subscription
BillingAccount
UsageRecord
Invoice
PaymentMethod
Entitlement
Quota
```

### 11.2 Possible billing dimensions

Possible billing dimensions:

- number of Agents;
- number of Capsule Services;
- number of Workspaces;
- number of users;
- command volume;
- health history retention;
- audit retention;
- alert volume;
- notification volume;
- premium Agent（代理） modes;
- support tier.

### 11.3 Plan examples

Possible future plan structure:

```text
Free / Developer
Team
Business
Enterprise
```

This is planning only.

CE（社区版） v0.1 should not implement billing.

---

## 12. Data Boundary Capabilities

Cloud（云版） must provide clear data boundary controls.

Possible capabilities:

- workspace data export;
- audit export;
- data deletion request;
- retention settings;
- secret handling documentation;
- metadata classification;
- customer-controlled secretRef model;
- optional managed secret store.

Recommended default:

> Cloud（云版） stores governance metadata and secret references, not raw operational secrets.

---

## 13. Secret Capabilities

Cloud（云版） should start with secret references, not raw secrets.

### 13.1 Initial secret capability

Initial Cloud（云版）-compatible capability:

```text
Display and preserve secretRef safely.
```

### 13.2 Future managed secrets

Future optional capabilities:

- Cloud（云版）-managed secret store;
- integration with customer Vault;
- integration with cloud secret managers;
- secret access audit;
- secret rotation workflows;
- Agent（代理）-local secret resolver;
- secret permission policies.

### 13.3 Boundary

Managed secrets should be optional and explicit.

Cloud（云版） should not require raw secrets for basic governance.

---

## 14. Integration Layer

Cloud（云版） may add integrations over time.

Possible integrations:

- Slack notification;
- Telegram notification;
- email notification;
- webhook outbound integration;
- GitHub integration;
- GitLab integration;
- SSO providers;
- Vault providers;
- Prometheus/Grafana integration;
- SIEM integration;
- incident management tools.

Integrations should be added based on real customer demand.

CE（社区版） v0.1 should not depend on these integrations.

---

## 15. Platform Operations Layer

Cloud（云版） itself requires internal platform operations.

Possible internal capabilities:

- deployment automation;
- database migrations;
- monitoring;
- logging;
- incident response;
- backups;
- restore testing;
- rate limiting;
- abuse detection;
- tenant isolation verification;
- support tooling;
- operational dashboards.

These capabilities are for operating Cloud（云版）, not CE（社区版）.

---

## 16. Cloud（云版） MVP Candidate Capabilities

A future Cloud（云版） MVP should likely include:

- hosted UI and Backend;
- user signup or private beta access;
- organization creation;
- workspace creation;
- registration token creation;
- remote Agent（代理） registration;
- Agent（代理） heartbeat;
- Capsule Service（胶囊服务） list;
- service detail;
- health visibility;
- config visibility;
- predefined action execution;
- command result display;
- audit logs;
- basic plan limits or manual entitlement;
- basic email notification for critical events.

Cloud（云版） MVP should not include full enterprise complexity.

---

## 17. Long-Term Cloud（云版） Capabilities

Long-term Cloud（云版） may include:

- multi-region Agent（代理） Gateway;
- advanced RBAC;
- enterprise SSO;
- SCIM;
- managed secrets;
- advanced audit compliance;
- custom retention policies;
- alert routing;
- command approval workflows;
- workflow automation;
- marketplace for Capsule templates;
- official hosted Agent（代理） diagnostics;
- usage analytics;
- customer success dashboards;
- SLA reporting.

These should be planned after core Cloud（云版） value is validated.

---

## 18. Capabilities Explicitly Not for CE（社区版） v0.1

The following Cloud（云版） capabilities must not be required by CE（社区版） v0.1:

```text
Tenant
Organization
Subscription
BillingAccount
UsageRecord
Cloud Agent Gateway
Cloud multi-tenant database
Cloud alerting system
Cloud notification service
Cloud compliance reports
Cloud data export workflow
Cloud user invitation system
Cloud team management
Cloud SSO
Cloud SLA tooling
```

CE（社区版） v0.1 may reserve compatible fields, but should not implement these systems.

---

## 19. Capability Dependency Rules

Cloud（云版） capabilities should be layered carefully.

### 19.1 Core first

Cloud（云版） must preserve core governance capabilities before adding commercial complexity.

### 19.2 Billing after value

Billing should not be designed before the Cloud（云版） MVP value is clear.

### 19.3 Alerting after reliable status

Alerting should be added only after health, heartbeat, and stale calculation are reliable.

### 19.4 SSO after team model

SSO should be added after organization and workspace models are stable.

### 19.5 Managed secrets after secretRef

Managed secrets should be added after secretRef boundary is proven.

---

## 20. Risks

### 20.1 Capability sprawl

Risk:

- Cloud（云版） becomes observability + config + workflow + billing + Kubernetes + agent platform too early.

Mitigation:

- focus on managed Capsule governance first.

### 20.2 CE（社区版） pollution

Risk:

- Cloud（云版） planning forces CE（社区版） v0.1 to implement tenant, billing, or gateway complexity.

Mitigation:

- keep CE（社区版） v0.1 scope strict.

### 20.3 Data trust risk

Risk:

- users hesitate to send governance metadata to Cloud（云版）.

Mitigation:

- keep CE（社区版） and EE（企业版） alternatives;
- document data boundary;
- avoid raw secrets;
- support data export and deletion later.

### 20.4 Commercial timing risk

Risk:

- billing is introduced before users see enough value.

Mitigation:

- start with beta access or simple plan limits.

---

## 21. Capability Acceptance Criteria

Cloud（云版） capability planning is acceptable when:

- Cloud（云版） capabilities extend the CE（社区版） kernel instead of replacing it;
- Cloud（云版） MVP candidate is smaller than full enterprise platform;
- data boundary is clear;
- secretRef remains central;
- Agent（代理） outbound connectivity remains central;
- CE（社区版） v0.1 is not burdened by Cloud（云版）-only features;
- billing and tenant capabilities are clearly future planning;
- observability scope stays focused on Capsule governance first.

---

## 22. Summary

Opstage（运维舞台） Cloud（云版） may eventually provide many managed SaaS capabilities, but its first product value should remain clear:

```text
Hosted governance for Capsule Services through outbound Agents.
```

The most important Cloud（云版） capability rule is:

> Build Cloud（云版） as a managed extension of the CE（社区版） governance kernel, not as a broad platform that loses the Capsule focus.
