---
status: proposed
audience: founders
stability: evolving
last_reviewed: 2026-05-05
edition: cloud
phase: future
---

# Cloud Positioning

- Status: Planning
- Edition: Cloud
- Priority: Future
- Audience: founders, product designers, architects, cloud engineers, AI coding agents

This document defines the product positioning of **Opstage Cloud**.

Opstage Cloud is the future hosted SaaS edition of the `xtrape-capsule` product family. It should extend the same
Agent-based Capsule governance model used by CE and EE, but provide it as a managed cloud service.

Cloud is not a CE v0.1 implementation requirement.

---

## 1. Positioning Statement

Opstage Cloud is:

> A hosted SaaS control plane for Capsule Services.

It helps teams register, observe, configure, operate, and audit Capsule Services without self-hosting Opstage Backend and UI.

Cloud should preserve the core Capsule governance idea:

```text
Capsule Services stay in the customer's environment.
Agents connect outbound to Opstage Cloud.
Opstage Cloud provides visibility, operations, audit, and collaboration.
```

---

## 2. Product Category

Opstage Cloud belongs to a new product category:

```text
Managed runtime governance for lightweight services
```

It is related to, but different from:

- configuration centers;
- observability platforms;
- service meshes;
- Kubernetes control planes;
- workflow platforms;
- remote administration tools.

Opstage Cloud should not be positioned as a replacement for all of these tools.

Its core value is Capsule Service governance.

---

## 3. Cloud Product Goal

The product goal of Opstage Cloud is:

> Provide a managed, team-oriented, multi-tenant control plane for lightweight services, AI automation services, integration services, and operational workers.

Cloud should reduce the cost of operating Opstage itself while improving:

- team collaboration;
- centralized visibility;
- managed audit retention;
- managed alerting;
- easier onboarding;
- cross-environment governance;
- commercial support.

---

## 4. Core Value Proposition

Opstage Cloud provides value through five product promises.

### 4.1 Managed control plane

Users do not need to install, upgrade, back up, or monitor Opstage Backend.

The platform provider operates the control plane.

### 4.2 Outbound Agent connectivity

Customer-side Agents connect outbound to Cloud.

This avoids exposing customer service ports to the public internet.

### 4.3 Team-oriented governance

Cloud supports organizations, workspaces, teams, roles, and collaboration.

This makes Opstage useful beyond single-developer self-hosting.

### 4.4 Managed audit and reporting

Cloud can provide longer audit retention, search, export, and reporting as managed capabilities.

### 4.5 Commercial reliability

Cloud can provide managed upgrades, backups, monitoring, support, and eventually SLA commitments.

---

## 5. Target Users

Opstage Cloud is designed for:

- small teams that do not want to self-host;
- AI automation teams;
- integration service operators;
- agencies managing multiple customer environments;
- startups with many internal lightweight services;
- teams that need basic governance but lack dedicated platform engineers;
- organizations that prefer managed SaaS for operational tooling.

---

## 6. Target Use Cases

### 6.1 Managed integration governance

A team runs several integration services across different environments and wants a single hosted console for status, health, actions, commands, and audit.

### 6.2 AI automation operations

A team runs AI agents, browser automation workers, account/session services, or connector services and wants centralized operational visibility.

### 6.3 Agency operations

An agency manages automation services for several customers and needs workspace separation, auditability, and team access.

### 6.4 Distributed lightweight service fleet

A company runs many small services across VPS, home servers, private servers, and cloud instances. Cloud provides one control plane.

### 6.5 Managed audit and reporting

A team wants to know who executed which actions, on which services, with what result, without managing audit storage itself.

---

## 7. Cloud Differentiation

Cloud should differentiate through:

- Capsule Service model;
- Agent-based outbound governance;
- lightweight service focus;
- operational commands through predefined actions;
- safe `secretRef` boundary;
- hosted visibility and audit;
- future team and organization collaboration;
- managed experience without requiring Kubernetes.

Cloud should avoid competing directly as a full observability stack or Kubernetes platform in the first phase.

---

## 8. Relationship with CE

CE is the open-source self-hosted edition.

Cloud is the hosted managed edition.

### 8.1 CE value

CE provides:

- trust;
- self-hosting;
- open-source adoption;
- local control;
- lightweight single-node deployment;
- proof of the Capsule governance model.

### 8.2 Cloud value

Cloud provides:

- managed backend;
- managed UI;
- team collaboration;
- multi-tenant workspaces;
- managed audit retention;
- managed alerting;
- commercial support;
- lower operational burden.

### 8.3 Shared kernel

Both CE and Cloud should share the same core concepts:

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

Cloud should be a managed evolution of CE, not a different incompatible product.

---

## 9. Relationship with EE

EE is the future enterprise private deployment edition.

Cloud and EE should differ mainly by deployment and operating responsibility.

| Area | EE | Cloud |
|---|---|---|
| Deployment | customer private environment | hosted SaaS |
| Operations | customer or vendor support | provider-operated |
| Database | customer-managed | provider-managed |
| Identity | enterprise identity | SaaS organization/team identity |
| Billing | commercial license | subscription billing |
| Data boundary | customer-controlled | shared responsibility |

Both should preserve the same Capsule governance model.

---

## 10. Data Boundary Positioning

Cloud must be very clear about what data it stores.

Cloud may store governance metadata:

- Agent metadata;
- Capsule Service metadata;
- health reports;
- config metadata;
- action metadata;
- command metadata;
- command results;
- audit events;
- usage records.

Cloud should avoid storing raw operational secrets by default.

Recommended positioning:

> Opstage Cloud stores governance metadata and secret references, not raw customer secrets by default.

Sensitive data should stay in:

- customer environment;
- Agent-local secret store;
- customer-managed Vault;
- customer cloud secret manager.

---

## 11. Secret Boundary

Cloud should use `secretRef` as the main secret boundary.

Examples:

```text
agent-local://agent-001/secrets/chatgpt/account-001
customer-vault://prod/integration-worker/account-001
cloud-secret://org/workspace/secret-key
```

Cloud may later provide managed secrets as an optional paid capability, but this should be explicit.

The default product message should be conservative:

> Your secrets can remain in your environment. Cloud only needs references and operational metadata.

---

## 12. Agent Connectivity Positioning

Cloud should emphasize outbound Agent connectivity.

Recommended message:

> Agents connect outbound to Opstage Cloud over HTTPS. You do not need to expose your Capsule Services to the public internet.

This is especially important for users running services behind NAT, firewalls, home networks, or private cloud environments.

---

## 13. Commercial Positioning

Cloud commercial value should come from managed service convenience and team features, not from disabling CE.

Good commercial value areas:

- managed hosting;
- backups;
- upgrades;
- audit retention;
- alerting;
- team collaboration;
- organization management;
- usage dashboards;
- support;
- SLA;
- managed Agent gateway.

Bad commercial strategy:

- CE cannot run actions;
- CE cannot view audit logs;
- CE Agent SDK is intentionally incomplete;
- CE is only a marketing shell.

Cloud should monetize convenience, scale, collaboration, and reliability.

---

## 14. Cloud Messaging

### 14.1 Short description

```text
Hosted control plane for Capsule Services.
```

### 14.2 Longer description

```text
Opstage Cloud helps teams manage Capsule Services across environments with hosted visibility, predefined operations, command tracking, and audit logs through outbound Agents.
```

### 14.3 Developer-facing message

```text
Install an Agent SDK or Agent runtime, connect it to Opstage Cloud, and make your lightweight services visible and operable without hosting the control plane yourself.
```

### 14.4 Security-facing message

```text
Agents connect outbound, and operational secrets can remain in your environment through secret references.
```

---

## 15. What Cloud Is Not

Cloud should not be positioned as:

- a full Kubernetes platform;
- a full observability replacement;
- a full configuration center;
- a remote shell service;
- a browser automation platform by itself;
- a secret vault by default;
- a workflow engine as its first identity.

Cloud may integrate with some of these areas later, but its first identity should remain Capsule governance.

---

## 16. Cloud MVP Positioning

A future Cloud MVP should be positioned as:

> Hosted CE-like governance with team and workspace support.

Possible Cloud MVP capabilities:

- hosted UI and Backend;
- user registration;
- organization/workspace creation;
- Agent registration token creation;
- remote Agent heartbeat;
- Capsule Service visibility;
- health visibility;
- predefined action execution;
- command results;
- audit logs;
- basic plan limits or private beta access.

Cloud MVP should not start as a full enterprise platform.

---

## 17. Competitive Framing

Cloud should be framed around the specific pain of many small services.

Problem statement:

```text
AI-era teams will create more lightweight services, agents, workers, connectors, and account/session services. These services are easy to create but hard to govern over time.
```

Opstage Cloud answer:

```text
Use a hosted Agent-based control plane to make these services visible, operable, and auditable across environments.
```

This positioning is narrower and sharper than generic DevOps tooling.

---

## 18. Risks in Positioning

### 18.1 Too broad

If Cloud is positioned as observability + config + workflow + Kubernetes + agent platform, users will not understand its core value.

Mitigation:

- keep the message focused on Capsule governance.

### 18.2 Too close to CE

If Cloud only looks like hosted CE without team, retention, alerting, or managed value, users may not pay.

Mitigation:

- emphasize managed operations, collaboration, retention, and reliability.

### 18.3 Trust concerns

Users may worry about sending service metadata to Cloud.

Mitigation:

- document data boundary;
- keep secrets customer-controlled by default;
- provide CE and EE alternatives.

### 18.4 Premature enterprise complexity

Cloud may become too complex before product-market fit.

Mitigation:

- start with hosted CE-like governance and iterate.

---

## 19. Success Criteria

Cloud positioning is successful when users understand that:

- Cloud is hosted Opstage, not a separate product;
- Agents connect outbound from customer environments;
- Capsule Services can remain customer-side;
- Cloud provides managed visibility, actions, commands, and audit;
- Cloud is suitable for teams and multiple environments;
- CE remains available for self-hosted users;
- EE is available later for private enterprise deployment;
- raw secrets are not required by default.

---

## 20. Summary

Opstage Cloud should be positioned as the hosted SaaS evolution of the Capsule governance model.

It should make lightweight services visible, operable, and auditable across environments without requiring users to self-host the control plane.

The most important Cloud positioning rule is:

> Cloud sells managed governance and collaboration, not control over customer secrets or a crippled replacement for CE.
