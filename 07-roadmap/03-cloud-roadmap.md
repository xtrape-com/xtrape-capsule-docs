# Cloud Roadmap

- Status: Planning
- Edition: Cloud
- Priority: Future
- Audience: founders, architects, product managers, SaaS platform engineers, backend developers, frontend developers, agent SDK developers, security reviewers, AI coding agents

This document defines the roadmap for **Opstage Cloud / SaaS Cloud Edition**.

Cloud is the future hosted SaaS edition of the `xtrape-capsule` product family. It should provide managed Opstage hosting, multi-tenant organizations and workspaces, Cloud Agent connectivity, billing, usage metering, managed audit retention, managed alerting, and SaaS support workflows.

Cloud is not a CE v0.1 implementation requirement.

---

## 1. Purpose

The purpose of the Cloud roadmap is to define:

- when Cloud should start;
- what Cloud should add beyond CE and EE;
- how Cloud should preserve the same Capsule governance kernel;
- how multi-tenancy should be introduced;
- how Cloud Agent connectivity may work;
- what billing and usage metering may include;
- what data boundaries must be respected;
- how to avoid building SaaS infrastructure too early.

The key rule is:

> Cloud should host and operate the proven Capsule governance model as a managed SaaS, not redefine the model before CE is stable.

---

## 2. Cloud Product Positioning

Cloud is:

> A hosted SaaS edition of Opstage for users who want managed Capsule Service governance without operating Opstage themselves.

Cloud should be suitable for:

- teams that do not want self-hosting;
- small companies that want quick onboarding;
- users who prefer managed upgrades;
- multi-user collaboration;
- managed audit retention;
- managed alerting;
- Cloud-based support workflows;
- usage-based or subscription-based commercial plans.

Cloud should remain compatible with the same Agent-based governance model used by CE and EE.

---

## 3. Relationship with CE and EE

CE proves the open-source governance kernel.

EE strengthens private enterprise deployment.

Cloud hosts the governance kernel as SaaS.

Recommended relationship:

```text
CE
  open-source self-hosted kernel

EE
  private enterprise deployment of the kernel

Cloud
  hosted SaaS operation of the kernel
```

Cloud should not force a different Agent model unless Cloud-specific connectivity requires additional gateway components.

---

## 4. Cloud Start Conditions

Cloud should not start too early.

Recommended start conditions:

- CE proves the full governance loop;
- Agent API is reasonably stable;
- Node Agent SDK is usable;
- Command and Action model is validated;
- basic security boundary is clear;
- real users want managed hosting;
- onboarding flow is understood;
- operating the service is feasible;
- billing/support responsibilities are acceptable.

Before these conditions, engineering should remain focused on CE and possibly EE.

---

## 5. Cloud Non-Goals During CE v0.1

During CE v0.1, do not implement:

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

These are Cloud roadmap items, not CE v0.1 tasks.

---

## 6. Cloud Capability Areas

Cloud may add capabilities in these areas:

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

## 7. Cloud Phase 0 — Kernel and Demand Validation

Before Cloud implementation starts, validate:

- CE governance kernel works;
- users understand Agent registration;
- users can run predefined actions safely;
- users understand CommandResult and AuditEvents;
- Agent token model is stable;
- secretRef boundary is clear;
- there is demand for hosted Opstage;
- Cloud operation cost is acceptable.

Cloud should not be built only because SaaS is commercially attractive. The hosted product must solve a real operational problem.

---

## 8. Cloud Phase 1 — SaaS Foundation

Cloud Phase 1 should establish SaaS foundations.

Possible capabilities:

- hosted Opstage Backend;
- hosted Opstage UI;
- user signup/login;
- Organization model;
- Workspace model;
- default organization/workspace creation;
- user profile;
- team invitation basics;
- Cloud-safe configuration;
- SaaS deployment pipeline;
- production database;
- SaaS monitoring and backups;
- basic support contact flow.

Goal:

> Make Opstage usable as a hosted multi-user service.

---

## 9. Cloud Phase 2 — Agent Enrollment and Connectivity

Cloud Phase 2 should focus on connecting customer Agents to Cloud.

Possible capabilities:

- workspace-scoped registration tokens;
- Agent enrollment instructions;
- Cloud Agent connection diagnostics;
- Agent token management;
- Agent status visibility;
- outbound-first Agent connectivity;
- Cloud-safe command polling;
- Agent connection troubleshooting;
- optional Agent Gateway planning.

Initial Cloud can still use HTTP polling if it is reliable enough.

Agent Gateway should be added only if required.

---

## 10. Cloud Phase 3 — Cloud Agent Gateway

Cloud Agent Gateway may be needed for scalable, secure, and observable Agent connectivity.

Possible responsibilities:

- Agent connection termination;
- workspace routing;
- Agent authentication;
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

## 11. Cloud Phase 4 — Billing and Usage Metering

Cloud Phase 4 may add billing and usage metering.

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

## 12. Cloud Phase 5 — Managed Audit and Alerting

Cloud may provide managed audit and alerting.

Possible capabilities:

- audit retention by plan;
- audit export by plan;
- audit search;
- managed alert rules;
- Agent offline alerts;
- service DOWN alerts;
- command failure alerts;
- notification channels;
- alert delivery history;
- alert usage limits.

Managed audit and alerting are strong SaaS values because customers do not need to operate these systems themselves.

---

## 13. Cloud Phase 6 — Data Management and Compliance Workflows

Cloud must provide customer data control workflows.

Possible capabilities:

- workspace data export;
- organization data export;
- audit export;
- Agent metadata export;
- account deletion workflow;
- workspace deletion workflow;
- data retention controls;
- support access audit;
- privacy documentation;
- regional data planning if needed.

Cloud data control should be designed before serious commercial launch.

---

## 14. Cloud Phase 7 — SaaS Operations and Support Maturity

Cloud operation requires product and engineering maturity.

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

Cloud means the provider owns runtime responsibility.

---

## 15. Cloud Tenancy Model

Cloud likely needs a tenancy model.

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

Recommended early Cloud hierarchy:

```text
Organization
  ↓
Workspace
  ↓
Agents / Capsule Services
```

Do not add full tenancy to CE v0.1.

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

Organization is Cloud scope, not CE v0.1 scope.

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

CE may reserve `workspaceId`, but Cloud gives it real multi-workspace semantics.

---

## 18. User and Team Model

Cloud should support team collaboration.

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

Cloud user accounts differ from CE local admin.

---

## 19. Cloud Identity Direction

Cloud identity may start simple and evolve.

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

Cloud identity is not CE v0.1 scope.

---

## 20. Agent Connectivity Boundary

Cloud Agent connectivity must remain outbound-first from customer environments where possible.

Recommended rule:

```text
Agent -> Cloud
```

Cloud should not require inbound network access into customer services.

This is especially important for private networks, NAT, and security-sensitive environments.

---

## 21. Cloud Security Boundary

Cloud must be stricter than CE because it is multi-tenant.

Security requirements:

- tenant/workspace isolation;
- Agent token isolation;
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

Cloud must not rely on UI-only enforcement.

---

## 22. Cloud Data Boundary

Cloud should store governance metadata, not raw customer secrets by default.

Cloud may store:

- organization metadata;
- user metadata;
- workspace metadata;
- Agent metadata;
- Capsule Service metadata;
- health reports;
- config metadata;
- action metadata;
- Commands;
- CommandResults;
- AuditEvents;
- alert rules;
- billing metadata.

Cloud should not store by default:

- raw passwords for customer systems;
- raw OAuth tokens for third-party accounts;
- raw browser cookies;
- private keys;
- account credentials;
- customer business records;
- raw browser sessions.

Use `secretRef`, customer-side secret storage, or enterprise secret provider integration where needed.

---

## 23. Cloud Plans

Cloud may use simple commercial plans.

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

## 24. CE/EE/Cloud Compatibility

Cloud should remain conceptually compatible with CE and EE.

Shared concepts:

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

Cloud may add:

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

## 25. Cloud Migration Paths

Potential migration paths:

```text
CE -> Cloud
EE -> Cloud
Cloud -> EE
Cloud -> CE export
```

Not all paths need to be automated early.

Cloud should at least support data export for customer control.

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

## 26. Cloud Documentation Requirements

Cloud documentation should include:

- Cloud overview;
- signup and onboarding guide;
- organization/workspace guide;
- Agent enrollment guide;
- Node Agent SDK Cloud guide;
- registration token guide;
- security and data boundary guide;
- billing guide;
- audit retention guide;
- alerting guide;
- data export/deletion guide;
- troubleshooting guide;
- support guide.

Cloud documentation should be user-facing and operationally clear.

---

## 27. Cloud Risks

### 27.1 Building Cloud too early

Risk:

- CE remains unfinished and SaaS complexity slows product validation.

Mitigation:

- require CE kernel validation first.

### 27.2 Multi-tenancy complexity

Risk:

- tenancy bugs create security and data isolation risks.

Mitigation:

- design isolation carefully;
- test tenant boundaries;
- keep early hierarchy simple.

### 27.3 Agent connectivity complexity

Risk:

- customer environments differ widely.

Mitigation:

- keep outbound-first model;
- start with simple polling;
- add Gateway only after need is proven.

### 27.4 Data and privacy risk

Risk:

- Cloud stores more data than necessary.

Mitigation:

- store governance metadata only;
- preserve secretRef boundary;
- provide export/deletion workflows.

### 27.5 Operational responsibility

Risk:

- SaaS requires monitoring, support, backups, incident response, and reliability.

Mitigation:

- do not launch Cloud before operational readiness.

---

## 28. Cloud Roadmap Guardrails

Guardrails:

1. Do not start Cloud before CE kernel works.
2. Do not add Cloud tenancy to CE v0.1.
3. Do not redefine Agent and Command concepts for Cloud.
4. Keep Agent connectivity outbound-first.
5. Start with HTTP polling before Gateway/streaming unless clearly needed.
6. Do not store raw customer secrets by default.
7. Do not build complex billing before usage model is clear.
8. Do not overcomplicate plans before product-market fit.
9. Do not launch Cloud without backup and incident basics.
10. Do not let Cloud planning expand CE v0.1 scope.

---

## 29. Decision Checkpoints

Before starting Cloud, ask:

- Is CE v0.1 working end to end?
- Is there demand for managed hosting?
- Is the Agent API stable enough?
- Is the Node Agent SDK easy enough for onboarding?
- Is multi-tenancy worth the complexity?
- Can we operate the service reliably?
- What data will Cloud store?
- What data must never be stored?
- What billing model is simple enough?
- What support commitment is realistic?

Before adding Agent Gateway, ask:

- Is HTTP polling insufficient?
- Are connection counts too high?
- Is command latency a real problem?
- Are diagnostics insufficient?
- Is the added operational complexity justified?

---

## 30. Cloud Roadmap Summary

Recommended Cloud roadmap summary:

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

The exact order may change, but Cloud must not precede CE kernel validation.

---

## 31. Acceptance Criteria

This Cloud roadmap is acceptable when:

- Cloud is clearly future, not CE v0.1;
- Cloud is positioned as hosted SaaS;
- Cloud preserves the same Capsule governance kernel;
- Cloud start conditions are clear;
- multi-tenancy is introduced deliberately;
- Agent Gateway is optional and demand-driven;
- billing and metering are future staged capabilities;
- data boundary and secretRef rules are explicit;
- Cloud operational responsibilities are acknowledged;
- Cloud guardrails prevent CE scope creep.

---

## 32. Summary

Cloud should become the hosted SaaS edition after the CE governance kernel is proven and managed-hosting demand is clear.

It should provide hosted Opstage, organizations, workspaces, managed Agent connectivity, billing, audit retention, alerting, support, and operational reliability while preserving the same Capsule governance model.

The most important Cloud roadmap rule is:

> Build Cloud only after the kernel is proven, keep Agent connectivity outbound-first, and store governance metadata without taking ownership of customer secrets.
