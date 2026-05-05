---
status: proposed
audience: founders
stability: evolving
last_reviewed: 2026-05-05
edition: cloud
phase: future
---

# Opstage Cloud Overview

- Status: Planning
- Edition: Cloud
- Priority: Future
- Audience: founders, product designers, architects, backend developers, cloud engineers, AI coding agents

This document defines the planning overview for **Opstage Cloud**.

Opstage Cloud is the future SaaS edition of the `xtrape-capsule` product family. It is not a CE v0.1 implementation requirement.

---

## 1. Positioning

Opstage Cloud is:

> A hosted SaaS control plane for Capsule Services, designed for teams that want managed governance without self-hosting Opstage Backend.

Cloud should extend the same core governance model used by CE and EE:

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

The difference is that Opstage Backend and UI are hosted by the platform provider, while customer-side Agents connect outbound to the Cloud control plane.

---

## 2. Cloud Is Not CE v0.1

Cloud is a future edition.

CE v0.1 must not implement Cloud-only capabilities such as:

- multi-tenant SaaS control plane;
- subscription billing;
- organization and team management;
- cloud Agent gateway;
- managed alerting;
- managed audit retention;
- usage metering;
- Cloud SLA;
- customer onboarding automation;
- hosted compliance reports.

CE should reserve extension points for Cloud, but Cloud must not become a dependency of CE v0.1.

---

## 3. Cloud Product Goal

The goal of Opstage Cloud is:

> Provide a managed, team-oriented, multi-tenant Opstage service for customers who want to govern Capsule Services without operating the control plane themselves.

Cloud should reduce customer operational burden while preserving the same security principle:

> Customer-side Agents connect outbound to Cloud, and customer secrets should remain customer-controlled whenever possible.

---

## 4. Target Users

Opstage Cloud is intended for:

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

### 5.4 Remote Agent fleet visibility

Agents run in many customer-owned environments and connect outbound to Opstage Cloud.

### 5.5 Managed audit and reporting

Teams want audit logs, reports, and operational history without maintaining their own database and backup process.

---

## 6. Cloud Architecture Direction

High-level Cloud architecture:

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

Cloud should keep the same core model as CE:

```text
UI talks to Backend
Agent talks to Backend or Agent Gateway
Backend creates Commands
Agent polls or receives Commands
Agent reports results
Audit records the operation
```

---

## 7. Agent Connectivity Model

Cloud should use an outbound-first Agent model.

Agents should connect from customer environments to Opstage Cloud:

```text
Agent -> Opstage Cloud
```

Cloud should not require inbound access into customer private networks.

This supports:

- NAT environments;
- home servers;
- private data centers;
- customer-controlled firewalls;
- fewer exposed ports;
- future managed Agent gateway.

---

## 8. Agent Gateway

Cloud may introduce an Agent Gateway layer.

Responsibilities may include:

- terminating Agent connections;
- validating Agent tokens;
- routing Agent traffic to tenant/workspace context;
- rate limiting;
- buffering command delivery;
- supporting WebSocket or streaming channels;
- collecting connection telemetry;
- isolating customer traffic.

CE v0.1 does not need Agent Gateway.

CE's HTTP heartbeat and polling model should remain compatible with future Cloud gateway evolution.

---

## 9. Multi-Tenancy

Cloud requires a multi-tenant model.

Future Cloud concepts may include:

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

CE v0.1 should not implement these first-class models.

However, CE already reserving `workspaceId` helps future migration.

---

## 10. Organization and Workspace Model

Recommended Cloud hierarchy:

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

Cloud should support stronger identity than CE.

Potential Cloud features:

- email/password login;
- OAuth login;
- team invites;
- organization roles;
- workspace roles;
- service accounts;
- API keys;
- optional SSO for higher plans;
- audit of user access.

CE v0.1 should only implement local admin authentication.

---

## 12. Billing and Subscription

Cloud may include subscription billing.

Possible billing dimensions:

- number of Agents;
- number of Capsule Services;
- command volume;
- health/report retention;
- audit retention;
- alerting volume;
- team seats;
- premium Agent modes;
- enterprise support.

Billing is not part of CE v0.1.

Cloud billing should not change the core Agent and Command contracts.

---

## 13. Data Boundary

Cloud must define a clear data boundary.

Cloud may store:

- Agent metadata;
- Capsule Service metadata;
- manifest metadata;
- health reports;
- config metadata;
- command metadata;
- command results;
- audit events;
- usage records;
- alert records.

Cloud should avoid storing raw customer secrets by default.

Sensitive values should use:

```text
secretRef
```

or remain in:

- customer environment;
- Agent-local secret store;
- customer-managed Vault;
- customer cloud secret manager.

---

## 14. Secret Strategy

Cloud should prefer customer-controlled secrets.

Recommended principle:

> Cloud stores governance metadata and secret references, not raw operational secrets.

Future Cloud may support optional managed secrets, but this should be explicit and plan-dependent.

Possible secretRef forms:

```text
agent-local://agent-001/secrets/chatgpt/account-001
customer-vault://path/to/secret
cloud-secret://org/workspace/key
```

CE v0.1 only needs to recognize and display `secretRef` safely.

---

## 15. Command Delivery Evolution

CE v0.1 uses HTTP polling.

Cloud may evolve command delivery to:

- WebSocket;
- Server-Sent Events;
- gRPC streaming;
- long polling;
- message queue backed delivery;
- Agent Gateway channels.

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

Cloud may provide managed observability beyond CE.

Potential Cloud capabilities:

- health history;
- uptime history;
- command success rate;
- Agent connection history;
- audit trends;
- alert rules;
- notification channels;
- dashboards;
- customer reports.

Cloud should not try to replace all specialized observability platforms at first.

The first Cloud observability value should be focused on Capsule governance data.

---

## 17. Audit and Retention

Cloud may provide managed audit retention and export.

Potential features:

- configurable retention periods;
- audit export;
- compliance-oriented reports;
- immutable storage option;
- audit search;
- actor and resource filters;
- workspace-level audit views.

CE v0.1 only needs lightweight audit logs.

---

## 18. Cloud Deployment Architecture

Possible Cloud deployment components:

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

Cloud may require:

- horizontal scaling;
- database migrations;
- tenant isolation;
- backup and restore;
- monitoring;
- incident response;
- rate limiting;
- abuse prevention.

None of these should be required by CE v0.1.

---

## 19. Cloud Security Direction

Cloud security requirements are stronger than CE.

Future Cloud should consider:

- tenant isolation;
- organization-level access control;
- workspace-level roles;
- Agent token rotation;
- rate limiting;
- audit retention;
- secure secret boundary;
- secure Agent Gateway;
- encrypted transport;
- encrypted storage;
- incident logging;
- abuse prevention;
- data export and deletion controls.

Cloud security design should be documented separately before implementation.

---

## 20. Cloud vs EE

Cloud and EE should share the same core contracts but differ in delivery model.

| Area | EE | Cloud |
|---|---|---|
| Deployment | customer private environment | hosted by provider |
| Database | customer-managed | provider-managed |
| Identity | enterprise-controlled | hosted organization/team model |
| Billing | license/subscription contract | SaaS subscription |
| Agent connection | customer private network | outbound to Cloud gateway |
| Operations | customer or vendor support | provider-operated |
| Data boundary | customer-controlled | shared responsibility |

Both should preserve the CE governance kernel.

---

## 21. CE Reservations for Cloud

CE should reserve these Cloud-compatible ideas:

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

CE should not implement:

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

## 22. Cloud MVP Candidate

A future Cloud MVP may include:

- hosted Opstage Backend and UI;
- user account registration;
- organization creation;
- one or more workspaces;
- Agent registration token creation;
- remote Agent heartbeat;
- Capsule Service list;
- health visibility;
- command execution;
- audit logs;
- basic subscription plan or private beta access.

This is not part of CE v0.1.

---

## 23. Risks

### 23.1 Data trust risk

Customers may not want governance metadata in Cloud.

Mitigation:

- keep CE and EE available;
- document data boundary;
- avoid raw secrets;
- provide export and deletion controls.

### 23.2 Agent connectivity risk

Customer networks may block outbound connections.

Mitigation:

- use standard HTTPS;
- support proxy configuration;
- provide clear connectivity diagnostics.

### 23.3 Cost risk

Cloud telemetry and audit retention can become expensive.

Mitigation:

- plan retention tiers;
- summarize where possible;
- avoid storing large logs in command/audit payloads.

### 23.4 Scope risk

Cloud can become too broad too quickly.

Mitigation:

- start with hosted CE-like governance;
- add multi-tenant and billing carefully;
- avoid becoming a full observability platform too early.

---

## 24. Cloud Planning Non-Goals

This document does not define final Cloud implementation details for:

- billing provider;
- tenant isolation architecture;
- production database choice;
- cloud infrastructure provider;
- exact Agent Gateway protocol;
- exact subscription plans;
- exact compliance commitments;
- exact SLA.

These require separate design documents when Cloud becomes an active target.

---

## 25. Summary

Opstage Cloud is the future hosted SaaS edition of the Capsule governance model.

It should extend the CE kernel into a managed, team-oriented, multi-tenant control plane.

The most important Cloud planning rule is:

> Cloud should be a managed evolution of the same Agent-based governance model, not a different product that breaks CE compatibility.
