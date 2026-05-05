---
status: draft
audience: founders
stability: evolving
last_reviewed: 2026-05-05
---

# Roadmap Documents

- Status: Implementation Guidance
- Edition: Shared
- Priority: Medium
- Audience: founders, architects, product managers, backend developers, frontend developers, agent SDK developers, AI coding agents

This directory contains the roadmap documents for the `xtrape-capsule` product family.

The roadmap defines how the product should evolve from a lightweight open-source CE kernel into future EE private deployment and Cloud SaaS editions.

The current implementation focus is **CE v0.1**.

EE and Cloud are future commercialization tracks. They should influence extension-point design, but they must not expand the CE v0.1 implementation scope.

---

## 1. Purpose of This Directory

The purpose of this directory is to define implementation and product sequencing.

It covers:

- the overall version roadmap;
- the CE roadmap;
- the EE roadmap;
- the Cloud roadmap;
- roadmap guardrails;
- edition sequencing;
- version sequencing;
- Agent and runtime expansion sequencing;
- release and documentation direction.

Roadmap documents should prevent scope confusion during implementation.

---

## 2. Roadmap Principle

The roadmap follows this principle:

```text
Build CE first.
Stabilize the governance kernel.
Expand Agent modes and runtimes gradually.
Add EE when private enterprise demand is real.
Add Cloud when managed SaaS demand and operational readiness are real.
```

The most important rule is:

> Do not let future EE or Cloud planning become CE v0.1 requirements.

---

## 3. Product Evolution Path

Recommended product evolution:

```text
CE v0.1
  ↓
CE v0.2 / CE v0.3
  ↓
CE v1.0
  ↓
EE Alpha / EE Beta / EE v1.0
  ↓
Cloud Alpha / Cloud Beta / Cloud v1.0
```

This order may evolve, but the first milestone should remain fixed:

```text
CE v0.1 first
```

---

## 4. CE-First Boundary

CE v0.1 should prove the core governance loop:

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

CE v0.1 should be:

- lightweight;
- open-source;
- self-hosted;
- SQLite-first;
- single-node friendly;
- Node.js Embedded Agent-first;
- safe by default;
- useful without EE or Cloud.

---

## 5. CE v0.1 Implementation Boundary

CE v0.1 should include:

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

## 6. CE v0.1 Non-Goals

CE v0.1 should not include:

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

These belong to future roadmap stages or are intentionally excluded.

---

## 7. Recommended Reading Order

Read the roadmap documents in this order:

```text
07-roadmap/README.md
07-roadmap/00-version-roadmap.md
07-roadmap/01-ce-roadmap.md
07-roadmap/02-ee-roadmap.md
07-roadmap/03-cloud-roadmap.md
```

For current implementation work, focus on:

```text
00-version-roadmap.md
01-ce-roadmap.md
```

For future commercialization planning, read:

```text
02-ee-roadmap.md
03-cloud-roadmap.md
```

---

## 8. Document List

### 8.1 `00-version-roadmap.md`

Defines the overall version roadmap.

Use it to understand:

- CE v0.1 goal;
- CE v0.1 scope and non-goals;
- CE v0.2/v0.3 direction;
- CE v1.0 direction;
- Agent expansion sequence;
- runtime expansion sequence;
- EE direction;
- Cloud direction;
- version naming;
- release artifact direction;
- roadmap guardrails.

### 8.2 `01-ce-roadmap.md`

Defines the Community Edition roadmap.

Use it to guide current implementation:

- CE product positioning;
- CE governance kernel;
- CE v0.1 architecture;
- Backend scope;
- UI scope;
- Agent scope;
- demo Capsule Service scope;
- data model scope;
- API scope;
- security scope;
- observability scope;
- CE acceptance criteria.

This is the most important roadmap document for CE v0.1 implementation.

### 8.3 `02-ee-roadmap.md`

Defines the future Enterprise Edition roadmap.

Use it for future planning around:

- private deployment;
- production database;
- enterprise identity;
- RBAC;
- audit and compliance;
- observability and alerting;
- secret provider integration;
- Agent expansion;
- HA and scale;
- commercial packaging;
- support model.

This is not a CE v0.1 implementation target.

### 8.4 `03-cloud-roadmap.md`

Defines the future Cloud SaaS roadmap.

Use it for future planning around:

- hosted Opstage;
- SaaS tenancy;
- Organizations and Workspaces;
- team accounts;
- Cloud Agent connectivity;
- Agent Gateway;
- billing and metering;
- managed audit retention;
- managed alerting;
- data export/deletion;
- SaaS operations and support.

This is not a CE v0.1 implementation target.

---

## 9. Roadmap Status Summary

| Area | Status | Current Requirement |
|---|---|---|
| CE v0.1 | Implementation Target | Yes |
| CE v0.2/v0.3 | Future CE improvement | No |
| CE v1.0 | Future stable release | No |
| EE | Planning | No |
| Cloud | Planning | No |
| Sidecar Agent | Future planning | No |
| External Agent | Future planning | No |
| Java/Python/Go SDKs | Future planning | No |
| Agent Gateway | Future Cloud planning | No |

Implementation agents should treat only CE v0.1 requirements as current tasks.

---

## 10. Agent Expansion Roadmap

Recommended Agent expansion sequence:

```text
1. Node.js Embedded Agent
2. Sidecar Agent prototype
3. External Agent prototype
4. Java Embedded Agent SDK
5. Python Embedded Agent SDK
6. Go SDK or Go-based Agent runtime
7. Kubernetes Agent
```

For CE v0.1, only the first item is in scope.

---

## 11. Runtime Expansion Roadmap

Recommended runtime expansion sequence:

```text
1. Node.js Runtime
2. Java Runtime planning and prototype
3. Python Runtime planning and prototype
4. Go Runtime planning and prototype
5. Sidecar/External runtime adapters
6. Kubernetes runtime integration
```

For CE v0.1, only Node.js Runtime is in scope.

---

## 12. Commercial Expansion Roadmap

Recommended commercial expansion sequence:

```text
1. CE proves product value.
2. CE stabilizes open-source adoption.
3. EE adds private enterprise deployment capabilities.
4. Cloud adds hosted SaaS capabilities.
```

Commercial editions should add value through scale, deployment, governance, support, and managed operations.

They should not rely on making CE intentionally incomplete.

---

## 13. Roadmap Guardrails

Follow these guardrails:

1. Build CE v0.1 first.
2. Keep CE useful as open source.
3. Do not implement EE/Cloud features in CE v0.1.
4. Do not add multiple runtimes before Node.js is stable.
5. Do not add Sidecar/External Agent before Embedded Agent is stable.
6. Do not add Agent Gateway before Cloud demand proves it.
7. Do not add billing before Cloud exists.
8. Do not add license enforcement before EE has real demand.
9. Do not add full observability before basic visibility is reliable.
10. Do not add remote shell or arbitrary script execution.
11. Do not store raw secrets by default.
12. Do not redefine the Capsule governance kernel per edition.

---

## 14. Decision Checkpoints

Before expanding beyond CE v0.1, ask:

- Does the full governance loop work?
- Is the Node Agent SDK usable?
- Is the Backend Agent API stable enough?
- Are status and freshness understandable?
- Can a user run demo actions successfully?
- Are CommandResults and AuditEvents visible?
- Is CE useful without EE or Cloud?

Before starting EE, ask:

- Is there real private deployment demand?
- Which enterprise feature is requested first?
- Which database/deployment model is required?
- What support scope is realistic?

Before starting Cloud, ask:

- Is there real demand for managed hosting?
- Is multi-tenancy worth the complexity?
- Can the service be operated reliably?
- Is Agent Gateway actually needed?
- What billing model is simple enough?

---

## 15. Anti-Patterns

Avoid these roadmap anti-patterns.

### 15.1 Building all editions at once

This slows the first useful release and increases confusion.

### 15.2 Treating CE as a crippled trial

CE should be useful and trustworthy.

### 15.3 Letting future planning drive current implementation

EE and Cloud planning should guide extension points, not CE v0.1 scope.

### 15.4 Adding runtimes too early

Node.js should prove the model first.

### 15.5 Adding Agent modes too early

Embedded Agent should prove the model first.

### 15.6 Adding commercial infrastructure too early

Billing, licensing, and support systems should come after product value is clear.

---

## 16. Acceptance Criteria

The roadmap document set is useful when:

- CE v0.1 is clearly the current implementation target;
- EE and Cloud are clearly future tracks;
- the reading order is clear;
- each roadmap document has a distinct purpose;
- CE scope and non-goals are clear;
- Agent and runtime expansion are sequenced;
- commercial expansion is sequenced;
- roadmap guardrails prevent scope creep;
- implementation agents can use the roadmap to avoid mixing current and future requirements.

---

## 17. Summary

This directory defines how `xtrape-capsule` should evolve from a lightweight open-source CE kernel into future EE and Cloud editions.

The most important roadmap directory rule is:

> Build CE v0.1 first as the smallest complete governance loop, then expand only after the kernel is proven and the next-stage demand is real.
