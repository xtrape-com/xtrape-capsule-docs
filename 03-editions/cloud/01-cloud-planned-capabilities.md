# Cloud Planned Capabilities

- Status: Planning
- Edition: Cloud
- Priority: Future
- Audience: founders, product designers, architects, cloud engineers, backend developers, AI coding agents

This document defines the planned capabilities for **Opstage Cloud**.

Opstage Cloud is the future hosted SaaS edition of the `xtrape-capsule` product family. It is not a CE v0.1 implementation requirement.

---

## 1. Purpose

The purpose of this document is to define:

- what capabilities Opstage Cloud may provide;
- how Cloud capabilities relate to the CE governance kernel;
- which Cloud capabilities may become MVP candidates;
- which capabilities should remain long-term planning items;
- which Cloud capabilities must not be pulled into CE v0.1;
- how Cloud should preserve compatibility with CE and EE.

The core rule is:

> Cloud extends the Capsule governance model as a managed SaaS service, but CE v0.1 must remain lightweight and self-hosted.

---

## 2. Capability Layers

Opstage Cloud capabilities can be grouped into layers:

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

Cloud does not need to implement all layers in the first release.

---

## 3. Core Governance Layer

The Core Governance Layer is inherited from CE.

It includes:

- Agent registration;
- Agent token authentication;
- Capsule Service report;
- manifest storage;
- heartbeat;
- health visibility;
- config visibility;
- predefined actions;
- Commands;
- CommandResults;
- AuditEvents;
- status and freshness calculation.

These capabilities should remain compatible with CE contracts.

Cloud may extend implementation, but should not break the shared concepts:

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

Cloud requires team-oriented SaaS capabilities.

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

### 4.4 CE relationship

CE v0.1 should not implement full organization, tenant, team, or billing models.

CE may reserve `workspaceId`, but Cloud owns the full multi-tenant model.

---

## 5. Identity and Access Capabilities

Cloud should support stronger identity than CE.

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

Future enterprise-oriented Cloud plans may include:

- OIDC;
- SAML;
- SCIM;
- MFA enforcement;
- domain verification;
- enterprise user lifecycle controls.

CE v0.1 should only implement local admin login.

---

## 6. Agent Connectivity Layer

Cloud should provide robust outbound Agent connectivity.

### 6.1 Basic Agent connectivity

Minimum Cloud-compatible model:

```text
Agent -> Opstage Cloud over HTTPS
```

Agents should not require inbound access from Cloud to customer networks.

### 6.2 Agent Gateway

Cloud may introduce Agent Gateway.

Possible capabilities:

- terminate Agent connections;
- validate Agent tokens;
- route traffic by tenant and workspace;
- support HTTP polling compatibility;
- support WebSocket or streaming mode;
- rate-limit Agent traffic;
- provide Agent connection diagnostics;
- buffer delivery metadata;
- isolate customer traffic.

### 6.3 Agent connection diagnostics

Possible diagnostics:

- last connected time;
- last heartbeat time;
- connection region;
- token status;
- error count;
- latency estimate;
- rejected requests;
- version compatibility warnings.

### 6.4 Agent token management

Possible capabilities:

- token rotation;
- token revocation;
- scoped Agent tokens;
- expiration policies;
- Agent enrollment policies;
- registration token expiration and one-time use.

CE v0.1 should support basic registration token and Agent token, but not Cloud Agent Gateway.

---

## 7. Command Delivery Capabilities

CE uses HTTP polling.

Cloud may support more delivery modes.

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

Possible Cloud capabilities:

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

Cloud should still use:

```text
Command
CommandResult
CommandStatus
AuditEvent
```

---

## 8. Managed Operations Layer

Cloud may provide managed operational capabilities beyond CE.

Possible capabilities:

- managed Backend upgrades;
- managed database backups;
- managed audit retention;
- system health checks;
- Agent fleet overview;
- version compatibility checks;
- operational reports;
- customer support diagnostics;
- service inventory history.

Cloud should reduce operational burden for users who do not want to self-host Opstage.

---

## 9. Observability and Alerting Layer

Cloud may provide managed observability focused on Capsule governance data.

### 9.1 Health history

Possible capabilities:

- health timeline;
- uptime history;
- stale duration;
- Agent connection history;
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

- Agent offline;
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

Cloud should not try to replace full observability platforms in the first phase.

The first observability scope should be Capsule governance data, not arbitrary logs, metrics, and traces.

---

## 10. Audit and Compliance Layer

Cloud may provide stronger audit capabilities than CE.

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

Cloud audit should preserve the same base AuditEvent shape used by CE.

CE v0.1 only needs lightweight audit logs.

---

## 11. Billing and Commercial Layer

Cloud may include commercial SaaS capabilities.

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
- premium Agent modes;
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

CE v0.1 should not implement billing.

---

## 12. Data Boundary Capabilities

Cloud must provide clear data boundary controls.

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

> Cloud stores governance metadata and secret references, not raw operational secrets.

---

## 13. Secret Capabilities

Cloud should start with secret references, not raw secrets.

### 13.1 Initial secret capability

Initial Cloud-compatible capability:

```text
Display and preserve secretRef safely.
```

### 13.2 Future managed secrets

Future optional capabilities:

- Cloud-managed secret store;
- integration with customer Vault;
- integration with cloud secret managers;
- secret access audit;
- secret rotation workflows;
- Agent-local secret resolver;
- secret permission policies.

### 13.3 Boundary

Managed secrets should be optional and explicit.

Cloud should not require raw secrets for basic governance.

---

## 14. Integration Layer

Cloud may add integrations over time.

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

CE v0.1 should not depend on these integrations.

---

## 15. Platform Operations Layer

Cloud itself requires internal platform operations.

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

These capabilities are for operating Cloud, not CE.

---

## 16. Cloud MVP Candidate Capabilities

A future Cloud MVP should likely include:

- hosted UI and Backend;
- user signup or private beta access;
- organization creation;
- workspace creation;
- registration token creation;
- remote Agent registration;
- Agent heartbeat;
- Capsule Service list;
- service detail;
- health visibility;
- config visibility;
- predefined action execution;
- command result display;
- audit logs;
- basic plan limits or manual entitlement;
- basic email notification for critical events.

Cloud MVP should not include full enterprise complexity.

---

## 17. Long-Term Cloud Capabilities

Long-term Cloud may include:

- multi-region Agent Gateway;
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
- official hosted Agent diagnostics;
- usage analytics;
- customer success dashboards;
- SLA reporting.

These should be planned after core Cloud value is validated.

---

## 18. Capabilities Explicitly Not for CE v0.1

The following Cloud capabilities must not be required by CE v0.1:

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

CE v0.1 may reserve compatible fields, but should not implement these systems.

---

## 19. Capability Dependency Rules

Cloud capabilities should be layered carefully.

### 19.1 Core first

Cloud must preserve core governance capabilities before adding commercial complexity.

### 19.2 Billing after value

Billing should not be designed before the Cloud MVP value is clear.

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

- Cloud becomes observability + config + workflow + billing + Kubernetes + agent platform too early.

Mitigation:

- focus on managed Capsule governance first.

### 20.2 CE pollution

Risk:

- Cloud planning forces CE v0.1 to implement tenant, billing, or gateway complexity.

Mitigation:

- keep CE v0.1 scope strict.

### 20.3 Data trust risk

Risk:

- users hesitate to send governance metadata to Cloud.

Mitigation:

- keep CE and EE alternatives;
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

Cloud capability planning is acceptable when:

- Cloud capabilities extend the CE kernel instead of replacing it;
- Cloud MVP candidate is smaller than full enterprise platform;
- data boundary is clear;
- secretRef remains central;
- Agent outbound connectivity remains central;
- CE v0.1 is not burdened by Cloud-only features;
- billing and tenant capabilities are clearly future planning;
- observability scope stays focused on Capsule governance first.

---

## 22. Summary

Opstage Cloud may eventually provide many managed SaaS capabilities, but its first product value should remain clear:

```text
Hosted governance for Capsule Services through outbound Agents.
```

The most important Cloud capability rule is:

> Build Cloud as a managed extension of the CE governance kernel, not as a broad platform that loses the Capsule focus.
