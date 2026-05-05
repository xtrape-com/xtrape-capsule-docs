---
status: proposed
audience: architects
stability: evolving
last_reviewed: 2026-05-05
---

# Opstage Subsystem Overview

- Status: Implementation Guidance
- Edition: Shared
- Priority: High
- Audience: architects, backend developers, frontend developers, agent SDK developers, product designers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/` (OpenAPI / Prisma) disagree, the ADRs and contracts win for CE v0.1.

This document defines the subsystem overview for **Opstage**.

Opstage is the runtime governance platform under the `xtrape-capsule` domain. It is responsible for making Capsule
Services visible, manageable, and auditable through a Backend, UI, and Agent-based integration model.

The current implementation focus is **Opstage CE**.

EE and Cloud are future planning tracks and must not expand the CE v0.1 implementation scope.

---

## 1. Positioning

`xtrape-capsule` is the domain and architecture concept for lightweight governable services.

Opstage is the governance platform for that domain.

Recommended relationship:

```text
xtrape-capsule
    ↓ domain / architecture concept
Opstage
    ↓ runtime governance platform
Capsule Services
    ↓ lightweight services governed through Agents
```

Opstage should not be treated as the whole `xtrape-capsule` domain. It is one major subsystem of the domain.

---

## 2. What Opstage Is

Opstage is:

> A runtime governance platform for Capsule Services.

It provides:

- service registration visibility;
- Agent registration and connectivity;
- health and freshness visibility;
- configuration metadata visibility;
- predefined action execution;
- Command and CommandResult tracking;
- basic audit logs;
- operational UI;
- future extension points for enterprise and Cloud operations.

---

## 3. What Opstage Is Not

Opstage is not:

- a microservice framework;
- a Kubernetes replacement;
- a full observability platform;
- a full configuration center clone;
- a remote shell platform;
- a workflow engine as its first identity;
- a secret vault by default;
- a business application framework;
- a browser automation framework by itself.

Opstage may integrate with some of these areas later, but its core identity should remain Capsule Service governance.

---

## 4. Core Problem

AI-era development will create more lightweight services, agents, automation workers, integration adapters, account/session managers, and connector services.

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

Opstage addresses this by giving lightweight services a common governance surface without forcing them into a heavy microservice platform.

---

## 5. Core Governance Loop

The Opstage governance loop is:

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

CE v0.1 should prove this loop end to end.

---

## 6. Main Components

Opstage consists of three main component groups:

```text
Opstage UI
Opstage Backend
Opstage Agent integration
```

### 6.1 Opstage UI

The UI provides the human-facing console.

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

### 6.2 Opstage Backend

The Backend is the control-plane service.

It is responsible for:

- Admin APIs;
- Agent APIs;
- authentication;
- registration tokens;
- Agent tokens;
- Agent heartbeat processing;
- service report storage;
- Command creation;
- CommandResult storage;
- status and freshness calculation;
- AuditEvent creation;
- persistence;
- security enforcement.

### 6.3 Agent integration

Agent integration connects Capsule Services to Opstage.

CE v0.1 implements:

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

These future modes are not CE v0.1 requirements.

---

## 7. CE Scope

Opstage CE is the current implementation target.

CE should implement the minimum complete product kernel:

- local admin login;
- Backend;
- UI;
- SQLite persistence;
- Node.js embedded Agent SDK;
- registration token;
- Agent token authentication;
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
- demo Capsule Service.

CE should be useful without EE or Cloud.

---

## 8. EE Extension Direction

Opstage EE is the future private enterprise commercial edition.

EE may extend Opstage with:

- production database support;
- PostgreSQL / MySQL;
- RBAC;
- SSO / OIDC / LDAP / SAML;
- audit retention and export;
- observability integrations;
- alert rules;
- secret provider integrations;
- sidecar / external Agents;
- Java / Python / Go Agent SDKs;
- high availability;
- cluster deployment;
- enterprise support;
- commercial packaging.

EE must extend the CE governance kernel, not redefine it.

---

## 9. Cloud Extension Direction

Opstage Cloud is the future hosted SaaS edition.

Cloud may extend Opstage with:

- hosted Backend and UI;
- Tenant / Organization / Workspace model;
- team collaboration;
- subscription billing;
- usage metering;
- Cloud Agent Gateway;
- managed audit retention;
- managed alerting;
- Cloud data export and deletion workflows;
- Cloud support and SLA;
- managed operations.

Cloud must remain compatible with the same Agent-based governance model.

---

## 10. Shared Core Concepts

Opstage should preserve these core concepts across CE, EE, and Cloud:

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

Opstage should store governance metadata by default.

It may store:

- Agent metadata;
- Capsule Service metadata;
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

> Opstage governs services through metadata, references, commands, results, and audit records; raw secrets should remain customer-controlled by default.

---

## 12. Security Boundary

Opstage security is based on two authenticated actor types in CE:

```text
Admin user
Agent
```

Admin users access Admin APIs through UI.

Agents access Agent APIs through Agent tokens.

The Backend must enforce:

- user authentication;
- Agent token authentication;
- Agent ownership of Commands;
- action validation;
- sensitive value masking;
- AuditEvent creation;
- no arbitrary shell execution.

Future EE and Cloud may add stronger identity, RBAC, tenancy, SSO, and compliance security.

---

## 13. Command Model

Opstage does not directly operate Capsule Services from the UI.

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

## 14. Agent Connectivity Rule

The default connectivity rule is outbound-first:

```text
Agent -> Opstage Backend
```

Opstage should not require inbound access into customer Capsule Services by default.

CE uses HTTP polling.

Future EE/Cloud may add WebSocket, long polling, gRPC, or Agent Gateway, but simple HTTP polling remains the reliable baseline.

---

## 15. Implementation Guardrails

For CE v0.1, do not implement:

- Tenant system;
- Organization system;
- billing;
- enterprise RBAC;
- SSO;
- PostgreSQL/MySQL requirement;
- Redis requirement;
- Queue requirement;
- Kubernetes requirement;
- Agent Gateway;
- full observability platform;
- Secret Vault;
- license enforcement;
- arbitrary shell execution.

CE should stay focused on the vertical governance slice.

---

## 16. Acceptance Criteria

This overview is satisfied when:

- Opstage is clearly defined as a subsystem of `xtrape-capsule`;
- Opstage is positioned as a runtime governance platform;
- UI, Backend, and Agent integration responsibilities are clear;
- CE scope is clearly identified as the current implementation target;
- EE and Cloud are clearly identified as future extension tracks;
- shared core concepts are preserved;
- data and security boundaries are explicit;
- command and Agent connectivity rules are clear;
- CE implementation guardrails are explicit.

---

## 17. Summary

Opstage is the runtime governance platform for Capsule Services.

It should make lightweight services visible, operable, and auditable without forcing them into a heavy microservice or platform stack.

The most important Opstage subsystem rule is:

> Build Opstage CE as a complete lightweight governance loop first, then extend the same kernel for EE and Cloud without redefining the core model.
