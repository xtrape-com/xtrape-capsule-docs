---
status: proposed
audience: founders
stability: evolving
last_reviewed: 2026-05-05
---

# Edition Boundaries

- Status: Implementation Guidance
- Edition: Shared
- Priority: High
- Audience: founders, architects, product designers, backend developers, frontend developers, agent SDK developers, AI coding agents

This document defines the edition boundaries for the `xtrape-capsule` product family.

The product family is planned around three editions:

```text
CE      = Community Edition
EE      = Enterprise Edition
Cloud   = SaaS Cloud Edition
```

The current implementation focus is **CE**.

EE and Cloud are planning tracks. They help keep the architecture future-friendly, but they are not implementation requirements for CE v0.1.

---

## 1. Purpose

The purpose of this document is to prevent edition confusion during design and implementation.

It defines:

- what CE is responsible for now;
- what EE is allowed to plan for later;
- what Cloud is allowed to plan for later;
- which documents are implementation targets;
- which documents are planning references;
- how CE should reserve extension points without becoming heavy.

The key rule is:

> Only CE documents marked as `Implementation Target` are current development requirements.

---

## 2. Edition Overview

### 2.1 CE — Community Edition

CE is the open-source community edition.

CE is the current implementation target.

CE should be:

- lightweight;
- self-hosted;
- open-source;
- easy to run;
- SQLite-first;
- single-node friendly;
- safe by default;
- useful without EE or Cloud.

CE should prove the core Capsule governance loop:

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
Basic audit log
```

### 2.2 EE — Enterprise Edition

EE is the future private commercial edition.

EE is not a CE v0.1 implementation requirement.

EE may plan for:

- enterprise identity;
- RBAC;
- SSO / OIDC / LDAP / SAML;
- production database support;
- high availability;
- cluster deployment;
- advanced audit;
- observability integrations;
- secret provider integrations;
- additional Agent modes;
- commercial support.

EE should extend CE, not replace it with an incompatible product.

### 2.3 Cloud — SaaS Cloud Edition

Cloud is the future hosted SaaS edition.

Cloud is not a CE v0.1 implementation requirement.

Cloud may plan for:

- hosted Opstage Backend and UI;
- multi-tenant organizations and workspaces;
- user signup and team collaboration;
- subscription billing;
- Agent Gateway;
- managed audit retention;
- managed alerting;
- usage metering;
- Cloud support and SLA.

Cloud should be a hosted evolution of the same Capsule governance model.

---

## 3. Current Implementation Rule

Current implementation should follow this priority:

```text
1. Accepted ADRs in 08-decisions/
2. Implementation contracts in 09-contracts/
3. Implementation plans in 10-implementation/
4. CE Implementation Target documents
5. Shared specifications used by CE
6. CE extension-point documents
7. EE / Cloud planning documents only as future context
```

Implementation agents and developers must not treat EE or Cloud planning documents as required work for CE v0.1.

---

## 4. Document Status Meaning

### 4.1 Implementation Target

A document marked as:

```text
Status: Implementation Target
```

means:

- it is part of the current CE development target;
- implementation should follow it unless a later design decision changes it;
- acceptance criteria in the document should guide development and review.

### 4.2 Implementation Guidance

A document marked as:

```text
Status: Implementation Guidance
```

means:

- it guides how implementation documents should be interpreted;
- it may define boundaries, principles, or reading order;
- it may not define concrete feature requirements by itself.

### 4.3 Planning

A document marked as:

```text
Status: Planning
```

means:

- it is future-facing;
- it is not required for CE v0.1;
- it may define extension points;
- it should not increase CE v0.1 implementation scope.

---

## 5. CE Boundary

CE should include the minimum complete product kernel.

CE should implement:

- local admin login;
- Opstage Backend;
- Opstage UI;
- SQLite persistence;
- Node.js embedded Agent SDK;
- Agent registration token;
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
- Docker quick start;
- demo Capsule Service.

CE should not implement enterprise or SaaS systems in v0.1.

---

## 6. EE Boundary

EE planning may define stronger enterprise capabilities.

EE may include in the future:

- RBAC;
- SSO / OIDC / LDAP / SAML;
- PostgreSQL / MySQL official support;
- high availability;
- Kubernetes / Helm deployment;
- advanced audit retention and export;
- alert rules;
- observability integrations;
- enterprise secret provider integrations;
- sidecar Agent;
- external Agent;
- Java / Python / Go Agent SDKs;
- license and commercial support packaging.

These are not CE v0.1 requirements.

---

## 7. Cloud Boundary

Cloud planning may define hosted SaaS capabilities.

Cloud may include in the future:

- Tenant;
- Organization;
- Workspace management;
- SaaS user accounts;
- team invitations;
- subscription billing;
- usage metering;
- Cloud Agent Gateway;
- managed audit retention;
- managed alerting;
- Cloud support access;
- hosted data export and deletion workflows;
- Cloud SLA and operational controls.

These are not CE v0.1 requirements.

---

## 8. Extension-Point Rule

CE should reserve extension points where they are cheap and clean.

Good CE reservations:

```text
workspaceId
agentMode
runtime
secretRef
metadataJson
AuditEvent actor/resource fields
Command as durable record
CommandResult as durable record
Agent token hash
registration token hash
status and freshness calculation
```

Bad CE scope expansion:

```text
Tenant system
Organization system
Billing system
Full RBAC
SSO
Cluster mode
Cloud Agent Gateway
Secret Vault
Metrics platform
Log platform
Alert engine
License enforcement
```

The rule is:

> Reserve space for the future, but do not make the future a dependency of CE v0.1.

---

## 9. Edition Compatibility Rule

CE, EE, and Cloud should share the same conceptual kernel:

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

Future editions may add capabilities, but they should not redefine the meaning of these core concepts.

---

## 10. Commercial Boundary Rule

Commercial editions should add value through scale, governance, support, deployment, and managed operations.

They should not depend on intentionally breaking CE.

Good commercial boundaries:

```text
enterprise identity
advanced audit
production database
HA deployment
managed Cloud hosting
team collaboration
support
SLA
secret provider integration
observability integration
```

Bad commercial boundaries:

```text
CE cannot register Agents
CE cannot run predefined actions
CE cannot view basic audit logs
CE cannot persist data
CE Agent SDK is intentionally incomplete
```

---

## 11. Recommended Reading Order

Recommended edition reading order:

```text
03-editions/README.md
03-editions/ce/README.md
03-editions/ce/*
03-editions/ee/README.md
03-editions/ee/*
03-editions/cloud/README.md
03-editions/cloud/*
```

For implementation work, read CE first.

For product planning, read EE and Cloud after CE.

---

## 12. Implementation Guardrails

When implementing CE v0.1, avoid these mistakes:

- do not implement Cloud tenancy;
- do not implement billing;
- do not implement enterprise RBAC;
- do not implement SSO;
- do not require PostgreSQL/MySQL;
- do not require Redis or Queue;
- do not require Kubernetes;
- do not implement Agent Gateway;
- do not implement full observability platform;
- do not implement secret vault;
- do not implement license enforcement;
- do not expose arbitrary shell execution.

CE should stay focused on the vertical slice.

---

## 13. Acceptance Criteria

Edition boundaries are clear when:

- CE is recognized as the current implementation target;
- EE is recognized as future private commercial planning;
- Cloud is recognized as future SaaS planning;
- `Implementation Target` documents are treated as current requirements;
- `Planning` documents are not treated as CE v0.1 requirements;
- CE reserves extension points without implementing future editions;
- CE remains useful and open-source;
- EE and Cloud remain compatible with the CE governance kernel.

---

## 14. Summary

The `xtrape-capsule` product family should grow through editions without confusing the current implementation scope.

The most important edition boundary rule is:

> Build CE first as a complete lightweight governance kernel, then let EE and Cloud extend it without redefining it.
