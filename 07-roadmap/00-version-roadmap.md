---
status: draft
audience: founders
stability: evolving
last_reviewed: 2026-05-05
---

# Version Roadmap

- Status: Implementation Guidance
- Edition: Shared
- Priority: Medium
- Audience: founders, architects, product managers, backend developers, frontend developers, agent SDK developers, AI coding agents

This document defines the version roadmap for the `xtrape-capsule` product family.

The current implementation focus is **CE v0.1**. CE v0.1 should prove the complete lightweight Capsule governance loop
with Opstage Backend, Opstage UI, SQLite, and the Node.js Embedded Agent SDK.

EE and Cloud are future commercialization tracks. They should influence extension-point design, but they must not expand the CE v0.1 implementation scope.

---

## 1. Purpose

The purpose of this roadmap is to define:

- what should be built first;
- what belongs to CE v0.1;
- what belongs to later CE stabilization;
- when Agent modes should expand;
- when EE private deployment should become relevant;
- when Cloud SaaS should become relevant;
- how to avoid mixing future roadmap items into the current implementation.

The key rule is:

> Build CE v0.1 as a complete lightweight governance kernel before expanding editions, runtimes, Agent modes, and commercial packaging.

---

## 2. Roadmap Principle

The roadmap follows this sequence:

```text
1. CE v0.1 — prove the governance loop
2. CE v0.2/v0.3 — stabilize and improve the open-source kernel
3. CE v1.0 — publish a reliable community edition
4. EE — add enterprise private-deployment capabilities
5. Cloud — add hosted SaaS capabilities
```

Do not build EE or Cloud infrastructure before CE proves the product kernel.

---

## 3. Product Kernel

The product kernel is the Capsule governance loop:

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

Every roadmap stage should preserve this kernel.

Future versions may add scale, security, identity, observability, and commercialization, but they should not redefine the kernel.

---

## 4. CE v0.1 Goal

CE v0.1 goal:

> Deliver a lightweight, open-source, self-hosted, single-node Opstage prototype that proves the full Capsule governance loop.

CE v0.1 should be good enough for:

- local development;
- demo use;
- early open-source feedback;
- validating the Capsule/Agent model;
- proving the UI + Backend + Agent vertical slice;
- guiding future architecture decisions.

CE v0.1 does not need to be enterprise-grade.

---

## 5. CE v0.1 Scope

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

These are future roadmap items.

---

## 7. CE v0.1 Recommended Implementation Order

Recommended implementation order:

```text
1. Backend project scaffold
2. UI project scaffold
3. SQLite schema and persistence
4. Local admin authentication
5. Registration token model
6. Agent registration API
7. Agent token authentication
8. Node.js Agent SDK scaffold
9. Agent heartbeat
10. Service manifest report
11. Agent and service UI pages
12. Health and config metadata visibility
13. ActionDefinition model
14. Command creation from UI
15. Command polling from SDK
16. CommandResult reporting
17. AuditEvent model and UI
18. Dashboard summary
19. System health endpoint
20. Node.js demo Capsule Service
21. Docker quick start
22. Minimal documentation and release notes
```

The order may be adjusted during implementation, but the vertical governance loop should remain the priority.

---

## 8. CE v0.1 Acceptance Criteria

CE v0.1 is acceptable when:

- user can start Opstage locally;
- user can log in as local admin;
- user can create a registration token;
- Node.js demo Capsule Service can register;
- Agent appears in UI;
- Capsule Service appears in UI;
- heartbeat status is visible;
- health status is visible;
- config metadata is visible;
- predefined actions are visible;
- user can run `echo` action;
- user can run `runHealthCheck` action;
- Backend creates Commands;
- Agent polls Commands;
- Agent reports CommandResults;
- UI displays CommandResult;
- AuditEvents are created and visible;
- stale/offline state is visible;
- sensitive values are masked;
- raw tokens are not logged;
- no arbitrary shell execution exists;
- Docker quick start can demonstrate the loop.

---

## 9. CE v0.2 Direction

CE v0.2 should stabilize the CE kernel after v0.1 feedback.

Possible focus areas:

- improve UI usability;
- improve error handling;
- improve SDK developer experience;
- improve dashboard clarity;
- improve status and freshness calculation;
- improve audit filtering;
- improve Docker packaging;
- add better local development scripts;
- add more tests;
- add migration discipline;
- improve documentation.

CE v0.2 should still avoid EE/Cloud complexity.

---

## 10. CE v0.3 Direction

CE v0.3 may add selected open-source improvements if the kernel is stable.

Possible focus areas:

- better command lifecycle handling;
- simple Command expiration cleanup;
- simple health history if needed;
- better demo service examples;
- improved SDK logging and diagnostics;
- improved local settings page;
- optional PostgreSQL/MySQL experimental adapter only if strongly justified;
- better release packaging.

CE v0.3 should remain lightweight.

---

## 11. CE v1.0 Direction

CE v1.0 should be a reliable community release.

Expected qualities:

- stable core concepts;
- stable Agent API;
- stable Node.js SDK API;
- stable SQLite deployment path;
- documented upgrade path;
- meaningful test coverage;
- reliable Docker quick start;
- clear security notes;
- clear CE/EE/Cloud boundaries;
- useful open-source experience.

CE v1.0 should still be self-hosted and lightweight.

---

## 12. Agent Expansion Roadmap

Agent expansion should happen after the CE Embedded Agent model is validated.

Recommended order:

```text
1. Node.js Embedded Agent
2. Sidecar Agent prototype
3. External Agent prototype
4. Java Embedded Agent SDK
5. Python Embedded Agent SDK
6. Go SDK or Go-based Agent runtime
7. Kubernetes Agent
```

This order is not fixed, but the first step is fixed:

```text
Node.js Embedded Agent first
```

---

## 13. Runtime Expansion Roadmap

Runtime expansion should happen after Node.js is stable.

Recommended order:

```text
1. Node.js Runtime
2. Java Runtime planning and prototype
3. Python Runtime planning and prototype
4. Go Runtime planning and prototype
5. Sidecar/External runtime adapters
6. Kubernetes runtime integration
```

Runtime expansion should preserve the same governance contract.

---

## 14. EE Roadmap Direction

EE should start after CE has a stable kernel and real usage signals.

Potential EE focus areas:

- PostgreSQL/MySQL official support;
- enterprise RBAC;
- SSO / OIDC / LDAP / SAML;
- audit export;
- audit retention configuration;
- alert rules;
- observability integrations;
- secret provider integrations;
- Sidecar Agent;
- External Agent;
- Java/Python/Go Agent SDKs;
- backup and restore tooling;
- high availability;
- Kubernetes / Helm deployment;
- support bundle;
- private deployment package;
- commercial support.

EE should sell enterprise value, not cripple CE.

---

## 15. Cloud Roadmap Direction

Cloud should start after CE/EE concepts are sufficiently validated.

Potential Cloud focus areas:

- hosted Backend and UI;
- Tenant / Organization / Workspace model;
- team invitations;
- subscription billing;
- usage metering;
- Cloud Agent Gateway;
- workspace-scoped registration tokens;
- managed audit retention;
- managed alerting;
- Cloud support workflows;
- data export and deletion workflows;
- Cloud operational monitoring;
- SaaS onboarding UX.

Cloud should remain compatible with the same Agent governance model.

---

## 16. Version Naming

Recommended version naming:

```text
CE v0.1
CE v0.2
CE v0.3
CE v1.0
EE Alpha
EE Beta
EE v1.0
Cloud Alpha
Cloud Beta
Cloud v1.0
```

Avoid using enterprise or Cloud version names before the CE kernel is stable.

---

## 17. Release Artifact Direction

CE release artifacts may include:

```text
source code
Docker image
Docker Compose example
Node Agent SDK package
Node demo Capsule Service
migration files
quick start guide
release notes
```

Future EE artifacts may include:

```text
private Docker images
private deployment package
Helm chart
backup/restore scripts
support bundle tool
security hardening guide
upgrade guide
license or entitlement package if needed
```

Future Cloud artifacts are mainly hosted service releases and customer-facing onboarding flows.

---

## 18. Documentation Roadmap

Documentation should evolve with versions.

### CE v0.1 documentation

Required:

- quick start;
- architecture overview;
- Opstage UI/Backend/Agent docs;
- Node Agent SDK guide;
- Node demo service guide;
- Docker quick start;
- security notes;
- troubleshooting.

### CE v1.0 documentation

Add:

- upgrade guide;
- API reference;
- SDK reference;
- deployment guide;
- contribution guide;
- release process.

### EE documentation

Add:

- enterprise deployment guide;
- RBAC guide;
- SSO guide;
- audit/compliance guide;
- observability integration guide;
- secret provider integration guide;
- backup/restore guide;
- support guide.

### Cloud documentation

Add:

- signup/onboarding guide;
- organization/workspace guide;
- Agent enrollment guide;
- billing guide;
- data export/deletion guide;
- Cloud support guide.

---

## 19. Roadmap Guardrails

Follow these guardrails:

1. Do not implement EE/Cloud features in CE v0.1.
2. Do not add multiple runtimes before Node.js is stable.
3. Do not add Sidecar/External Agent before Embedded Agent is stable.
4. Do not add alerting before status and freshness are reliable.
5. Do not add billing before Cloud exists.
6. Do not add license enforcement before EE has real commercial demand.
7. Do not add arbitrary shell execution.
8. Do not store raw secrets by default.
9. Do not break CE trust with artificial limitations.
10. Do not redefine the Capsule governance kernel per edition.

---

## 20. Decision Checkpoints

Before moving from CE v0.1 to later roadmap stages, review these checkpoints.

### Before CE v0.2

Ask:

- Does the full governance loop work?
- Is the Agent API usable?
- Is the Node SDK developer experience acceptable?
- Are status and freshness understandable?
- Are users able to run demo actions successfully?

### Before CE v1.0

Ask:

- Are core APIs stable enough?
- Is upgrade/migration acceptable?
- Is documentation sufficient?
- Is the security boundary clear?
- Is CE useful as an open-source product?

### Before EE

Ask:

- Is there real private deployment demand?
- Which enterprise features are actually requested?
- Which database/deployment mode is required first?
- Which Agent expansion has the strongest demand?
- What support burden is acceptable?

### Before Cloud

Ask:

- Is there SaaS demand?
- Is multi-tenancy worth the added complexity?
- Is Agent Gateway required?
- Are billing and support workflows ready?
- Is operational responsibility acceptable?

---

## 21. Anti-Patterns

Avoid these roadmap anti-patterns.

### 21.1 Building all future editions at once

This slows CE and makes the product unclear.

### 21.2 CE as a broken demo

CE should be genuinely useful.

### 21.3 Agent expansion before Agent basics

Embedded Agent should be stable before Sidecar/External Agent.

### 21.4 Runtime expansion before Node.js is stable

More runtimes should not come before a validated governance contract.

### 21.5 Commercial packaging before product value

License and entitlement systems should not consume early engineering capacity.

### 21.6 Observability platform before governance visibility

First make Agents, services, health, Commands, and AuditEvents visible.

---

## 22. Summary Roadmap

Recommended roadmap summary:

```text
CE v0.1
  Build the lightweight governance loop with Node.js Embedded Agent.

CE v0.2/v0.3
  Stabilize CE, improve DX, UI, tests, packaging, and docs.

CE v1.0
  Publish a reliable open-source community edition.

EE
  Add enterprise private-deployment capabilities based on real demand.

Cloud
  Add hosted SaaS capabilities after the governance model is mature.
```

---

## 23. Acceptance Criteria

This roadmap is acceptable when:

- CE v0.1 scope is clear;
- CE v0.1 non-goals are clear;
- Node.js Embedded Agent is clearly first;
- future Agent and runtime expansion is sequenced;
- EE and Cloud are clearly future tracks;
- roadmap guardrails prevent scope creep;
- release and documentation directions are clear;
- CE remains useful and open-source;
- future editions extend the same governance kernel.

---

## 24. Summary

The `xtrape-capsule` roadmap should prioritize a working, lightweight, open-source CE kernel before expanding into enterprise and SaaS editions.

The most important roadmap rule is:

> Build the smallest complete governance loop first, then expand scale, runtime coverage, Agent modes, enterprise features, and Cloud hosting only after the kernel is proven.
