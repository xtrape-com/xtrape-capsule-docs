---
status: proposed
audience: architects
stability: evolving
last_reviewed: 2026-05-05
---

# Opstage Documents

- Status: Implementation Guidance
- Edition: Shared
- Priority: High
- Audience: architects, backend developers, frontend developers, agent SDK developers, product designers, AI coding agents

This directory contains the Opstage subsystem documents for the `xtrape-capsule` product family.

Opstage is the runtime governance platform for Capsule Services. It provides the UI, Backend, and Agent integration
model that makes lightweight services visible, operable, and auditable.

The current implementation focus is **Opstage CE**.

EE and Cloud documents are future planning references. They help keep the architecture extensible, but they must not expand the CE v0.1 implementation scope.

---

## 1. Purpose of This Directory

The purpose of this directory is to define the Opstage runtime governance subsystem.

It covers:

- what Opstage is;
- how Opstage UI works;
- how Opstage Backend works;
- how Agents connect Capsule Services to Opstage;
- how Commands and Actions work;
- how AuditEvents are modeled;
- how observability should evolve from CE to EE and Cloud.

This directory should be read after the higher-level Capsule and edition-boundary documents.

---

## 2. Opstage Positioning

Opstage is:

> The runtime governance platform for Capsule Services.

It is responsible for the core governance loop:

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

This governance loop is the CE product kernel.

---

## 3. What Opstage Includes

Opstage includes three main subsystem groups:

```text
Opstage UI
Opstage Backend
Opstage Agent Integration
```

It also includes shared operation models:

```text
Command and Action Model
Audit Model
Observability Roadmap
```

These models bind UI, Backend, and Agent together into one coherent governance system.

---

## 4. What Opstage Is Not

Opstage is not:

- a generic microservice framework;
- a Kubernetes replacement;
- a full observability platform;
- a full configuration center clone;
- a secret vault by default;
- a remote shell system;
- a browser automation framework by itself;
- a workflow engine as its first identity;
- a SaaS billing system in CE.

Future EE and Cloud may integrate with some of these areas, but the first product identity should remain Capsule Service governance.

---

## 5. Current CE Implementation Boundary

Opstage CE v0.1 should implement a lightweight but complete vertical slice.

CE should include:

- local admin login;
- Opstage Backend;
- Opstage UI;
- SQLite persistence;
- Node.js embedded Agent SDK;
- registration token;
- Agent token authentication;
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
- dashboard summary;
- system health endpoint;
- Docker quick start;
- demo Capsule Service.

CE should be useful without EE or Cloud.

---

## 6. CE Non-Goals

Opstage CE v0.1 should not implement:

- Tenant system;
- Organization system;
- billing;
- subscription;
- usage metering;
- enterprise RBAC;
- SSO / OIDC / LDAP / SAML;
- PostgreSQL/MySQL requirement;
- Redis requirement;
- Queue requirement;
- Kubernetes requirement;
- Agent Gateway;
- sidecar Agent;
- external Agent;
- Java/Python/Go Agent SDKs;
- full observability platform;
- alert rule engine;
- secret vault;
- license enforcement;
- arbitrary shell execution.

These are future EE or Cloud planning items.

---

## 7. Recommended Reading Order

Read the documents in this directory in the following order:

```text
04-opstage/README.md
04-opstage/00-opstage-overview.md
04-opstage/01-opstage-ui.md
04-opstage/02-opstage-backend.md
04-opstage/03-opstage-agent-integration.md
04-opstage/04-command-and-action-model.md
04-opstage/05-audit-model.md
04-opstage/06-observability-roadmap.md
```

This order moves from subsystem overview to concrete implementation models.

---

## 8. Document List

### 8.1 `00-opstage-overview.md`

Defines the Opstage subsystem as a whole.

Use it to understand:

- Opstage positioning;
- main components;
- shared concepts;
- CE scope;
- EE and Cloud extension directions;
- implementation guardrails.

### 8.2 `01-opstage-ui.md`

Defines the human-facing UI console.

Use it to implement:

- Login;
- Dashboard;
- Agents pages;
- Capsule Services pages;
- Commands pages;
- Audit Logs pages;
- System Settings page;
- action execution UX;
- sensitive value display rules.

### 8.3 `02-opstage-backend.md`

Defines the Backend control plane.

Use it to implement:

- Admin APIs;
- Agent APIs;
- authentication;
- token handling;
- persistence;
- core data models;
- Command flow;
- status and freshness calculation;
- AuditEvent creation.

### 8.4 `03-opstage-agent-integration.md`

Defines how Agents connect Capsule Services to Opstage.

Use it to implement:

- Node.js embedded Agent SDK;
- registration flow;
- heartbeat flow;
- service manifest report;
- health provider;
- config provider;
- action registry;
- command polling;
- CommandResult reporting.

### 8.5 `04-command-and-action-model.md`

Defines the safe operation mechanism.

Use it to implement:

- ActionDefinition;
- Command;
- CommandResult;
- action request flow;
- action danger levels;
- command statuses;
- validation rules;
- no arbitrary shell execution rule.

### 8.6 `05-audit-model.md`

Defines structured operation traceability.

Use it to implement:

- AuditEvent;
- actor model;
- resource model;
- action naming;
- result values;
- audit sanitization;
- audit API;
- audit UI.

### 8.7 `06-observability-roadmap.md`

Defines the observability evolution path.

Use it to implement CE visibility and avoid premature observability complexity.

It clarifies:

- CE basic visibility;
- Agent status;
- Capsule Service effective status;
- freshness;
- command visibility;
- audit visibility;
- future EE/Cloud logs, metrics, traces, alerts, and dashboards.

---

## 9. Shared Core Concepts

All documents in this directory should use the same core concepts:

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

Future editions may extend these concepts, but they should not redefine them.

---

## 10. Implementation Priority

For CE v0.1, recommended implementation priority is:

```text
1. Backend persistence and auth
2. Registration token and Agent registration
3. Node.js embedded Agent SDK
4. Heartbeat and service report
5. UI Agent and Service visibility
6. Health and config metadata visibility
7. ActionDefinition and Command flow
8. CommandResult reporting
9. AuditEvent model and UI
10. Dashboard and system health
11. Docker quick start and demo service
```

This order proves the core governance loop step by step.

---

## 11. Safety Rules

Opstage CE must follow these safety rules:

1. UI never calls Agent directly.
2. Backend creates durable Commands.
3. Agents execute only predefined actions.
4. Arbitrary shell execution is not part of CE.
5. Agent tokens are stored as hashes in Backend.
6. Registration tokens are shown only once.
7. Raw secrets are not stored by default.
8. Sensitive values are masked.
9. `secretRef` is used for sensitive references.
10. Important governance operations create AuditEvents.
11. Stale services must not be shown as fresh healthy services.

---

## 12. Extension Rules

CE should reserve clean extension points where cheap:

```text
workspaceId
agentMode
runtime
secretRef
metadataJson
AuditEvent actor/resource fields
Command as durable record
CommandResult as durable record
status and freshness calculation
```

CE should not implement future systems just because extension fields exist.

The rule is:

> Reserve space for EE and Cloud, but do not let EE and Cloud become CE dependencies.

---

## 13. Acceptance Criteria

The Opstage document set is useful when:

- the role of Opstage is clear;
- UI, Backend, and Agent responsibilities are separated;
- Command and Action flow is explicit;
- AuditEvent model is explicit;
- CE implementation scope is clear;
- CE non-goals are explicit;
- EE and Cloud extensions are clearly future planning;
- safety rules prevent arbitrary execution and secret leakage;
- implementation agents can follow the reading order and build the CE vertical slice.

---

## 14. Summary

This directory defines the Opstage runtime governance subsystem.

The most important Opstage directory rule is:

> Build the CE governance loop first through UI, Backend, Agent, Commands, Results, and AuditEvents; keep future EE and Cloud capabilities as extension tracks, not current requirements.
