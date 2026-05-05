---
status: proposed
audience: founders
stability: evolving
last_reviewed: 2026-05-05
edition: ee
phase: future
---

# Opstage EE Overview

- Status: Planning
- Edition: EE
- Priority: Future
- Audience: founders, product designers, architects, enterprise engineers, backend developers, DevOps engineers, AI coding agents

This document defines the planning overview for **Opstage EE / Enterprise Edition**.

Opstage EE is the future private commercial edition of the `xtrape-capsule` product family. It is not a CE v0.1 implementation requirement.

---

## 1. Positioning

Opstage EE is:

> A private enterprise deployment edition of Opstage for organizations that need stronger security, identity, deployment, observability, audit, and support capabilities while keeping the control plane in their own environment.

EE should extend the same Capsule governance model established by CE:

```text
Agent registration
    ↓
Service report
    ↓
Heartbeat and health
    ↓
Config visibility or management
    ↓
Predefined action request
    ↓
Command delivery
    ↓
Command result
    ↓
Audit log
```

The difference is that EE is designed for enterprise private deployment and operational scale.

---

## 2. EE Is Not CE v0.1

EE is a future edition.

CE v0.1 must not implement EE-only capabilities such as:

- enterprise RBAC;
- SSO / OIDC / LDAP / SAML;
- high availability;
- cluster deployment;
- enterprise installer;
- centralized log platform;
- metrics dashboards;
- alert rules;
- Secret Vault integration;
- compliance-grade audit;
- commercial license enforcement;
- sidecar / external Agent mode;
- Java / Python / Go Agent SDKs;
- enterprise upgrade and migration tooling;
- enterprise support workflow.

CE should reserve extension points for EE, but EE must not become a dependency of CE v0.1.

---

## 3. EE Product Goal

The goal of Opstage EE is:

> Provide an enterprise-grade private Opstage control plane for organizations that need to govern Capsule Services under stricter security, compliance, deployment, and operational requirements.

EE should help enterprises:

- deploy Opstage inside their own infrastructure;
- connect Capsule Services through Agents;
- manage users and permissions;
- integrate enterprise identity providers;
- store data in enterprise databases;
- operate at higher scale;
- retain audit records longer;
- integrate logs, metrics, alerts, and secrets;
- receive commercial support.

---

## 4. Target Users

Opstage EE is intended for:

- enterprises requiring private deployment;
- organizations with internal compliance requirements;
- teams that cannot use hosted Cloud for governance data;
- companies with existing identity providers;
- platform engineering teams;
- internal developer platform teams;
- AI automation teams operating many private services;
- Operators managing sensitive accounts with sensitive accounts and sessions;
- customers needing vendor support and upgrade guarantees.

---

## 5. Target Scenarios

### 5.1 Private enterprise deployment

An organization deploys Opstage inside its own network or private cloud and connects internal Capsule Services through Agents.

### 5.2 Enterprise identity integration

A company needs Opstage to integrate with SSO, OIDC, LDAP, or SAML so users can access the platform with enterprise accounts.

### 5.3 Larger Agent and service fleet

A team runs many Agents and Capsule Services and needs stronger database, deployment, and operations support than CE.

### 5.4 Compliance-oriented audit

An organization needs longer audit retention, searchable audit events, export, and compliance reporting.

### 5.5 Enterprise observability integration

A company wants Opstage to integrate with existing log, metric, trace, and alerting systems.

### 5.6 Secure secret integration

A company wants Capsule Services to reference secrets from Vault or enterprise secret managers without exposing raw secrets to Opstage unnecessarily.

---

## 6. EE Architecture Direction

High-level EE architecture may include:

```text
Enterprise Environment
├── Opstage UI
├── Opstage Backend
├── Worker / Scheduler
├── Database
├── Cache / Queue
├── Log / Metric / Audit integrations
├── Secret provider integration
└── Agents
    ├── Embedded Agents
    ├── Sidecar Agents
    └── External Agents
```

EE should preserve the same core contracts as CE:

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

---

## 7. Deployment Direction

EE may support more deployment models than CE.

Potential deployment models:

```text
Docker Compose
Kubernetes / Helm
VM-based installation
Private cloud deployment
Dedicated enterprise appliance style deployment
```

Potential EE deployment components:

```text
UI
Backend API
Worker
Scheduler
Database
Redis / Queue
Object storage
Log integration
Metric integration
Secret integration
```

CE v0.1 should remain single-container and SQLite-first.

---

## 8. Database Direction

CE uses SQLite by default.

EE should likely support enterprise-grade databases:

```text
PostgreSQL
MySQL
```

Possible future options:

```text
Oracle
SQL Server
```

only if enterprise demand justifies them.

EE database requirements may include:

- migrations;
- backup and restore guidance;
- connection pooling;
- retention policies;
- audit storage strategy;
- performance tuning;
- HA database deployment guidance.

---

## 9. Identity and Access Direction

EE should support stronger identity and authorization than CE.

Potential capabilities:

- RBAC;
- workspace-level roles;
- service-level permissions;
- action-level permissions;
- approval workflows;
- SSO;
- OIDC;
- LDAP;
- SAML;
- SCIM;
- service accounts;
- API keys;
- audit of permission changes.

CE v0.1 may support only local admin authentication.

---

## 10. Agent Direction

CE v0.1 implements only Node.js embedded Agent SDK.

EE may add:

- sidecar Agent;
- external Agent;
- Java Agent SDK;
- Python Agent SDK;
- Go Agent SDK;
- host-level Agent;
- Docker host Agent;
- Kubernetes Agent;
- Agent version management;
- Agent upgrade guidance;
- Agent diagnostics.

EE Agent expansion should not break CE Agent contracts.

---

## 11. Command Delivery Direction

CE v0.1 uses HTTP polling.

EE may support:

- HTTP polling;
- long polling;
- WebSocket;
- gRPC streaming;
- queue-backed delivery;
- command scheduling;
- command cancellation;
- command approval workflow;
- command concurrency controls;
- long-running command progress.

The durable Command / CommandResult model should remain stable.

---

## 12. Observability Direction

EE may provide stronger observability than CE.

Potential capabilities:

- centralized log integration;
- log search integration;
- metrics dashboards;
- health history;
- Agent uptime history;
- command success/failure analytics;
- alert rules;
- notification channels;
- OpenTelemetry integration;
- Prometheus/Grafana integration;
- Loki / Elasticsearch integration.

EE should not necessarily become a full observability platform, but it can integrate with enterprise observability systems.

---

## 13. Audit and Compliance Direction

EE may support stronger audit and compliance features.

Potential capabilities:

- configurable audit retention;
- audit export;
- audit search;
- immutable audit storage option;
- compliance reports;
- approval records;
- permission change audit;
- support access audit;
- SIEM integration.

CE v0.1 only needs lightweight audit logs.

---

## 14. Secret Management Direction

EE may integrate with enterprise secret providers.

Potential integrations:

```text
HashiCorp Vault
AWS Secrets Manager
Azure Key Vault
Google Secret Manager
Kubernetes Secrets
enterprise internal secret service
```

EE should continue to support the `secretRef` boundary.

Recommended principle:

> EE should integrate with enterprise secret systems without requiring raw secrets to be stored in Opstage by default.

---

## 15. Configuration Management Direction

CE v0.1 supports config visibility only.

EE may support stronger configuration management:

- config editing;
- config publishing;
- approval workflow;
- versioning;
- rollback;
- environment promotion;
- config drift detection;
- config reload actions;
- integration with external config centers.

EE should avoid becoming merely another Nacos/Apollo clone. Its config features should be tied to Capsule governance and Agent-based operations.

---

## 16. Licensing and Commercial Direction

EE is a commercial private deployment edition.

Potential commercial mechanisms:

- license key;
- offline license file;
- subscription contract;
- support contract;
- enterprise installer access;
- private registry access;
- feature entitlements;
- support SLA.

CE should not include license enforcement.

EE commercial value should come from enterprise capabilities, scale, deployment, compliance, and support.

---

## 17. EE vs CE

| Area | CE | EE |
|---|---|---|
| License | open-source | commercial |
| Deployment | single-node self-hosted | private enterprise deployment |
| Database | SQLite default | PostgreSQL/MySQL official support |
| Identity | local admin | RBAC, SSO, OIDC/LDAP/SAML |
| Agent | Node.js embedded | embedded, sidecar, external, multi-language |
| Command delivery | polling | polling, streaming, queue-backed |
| Observability | health visibility | logs, metrics, alerts, integrations |
| Audit | basic audit | advanced audit, retention, export, compliance |
| Secrets | secretRef-ready | enterprise secret integrations |
| Support | community | commercial support |

---

## 18. EE vs Cloud

| Area | EE | Cloud |
|---|---|---|
| Deployment | customer private environment | hosted by provider |
| Operations | customer/vendor supported | provider-operated |
| Database | customer-managed | provider-managed |
| Identity | enterprise-controlled | SaaS organization/team model |
| Billing | commercial license/support contract | SaaS subscription |
| Data boundary | customer-controlled | shared responsibility |
| Agent connection | private/customer network | outbound to Cloud gateway |
| Upgrades | customer-controlled | provider-managed |

EE and Cloud should share core contracts but differ in operating model.

---

## 19. CE Reservations for EE

CE should reserve these EE-compatible extension points:

```text
workspaceId
agentMode
runtime
database provider
command delivery abstraction
secretRef
AuditEvent
Command
CommandResult
Status values
metadataJson
createdBy
actorType
actorId
resourceType
resourceId
```

CE should not implement EE systems directly in v0.1.

---

## 20. EE MVP Candidate

A future EE MVP may include:

- CE-compatible core governance;
- PostgreSQL or MySQL support;
- private Docker Compose deployment;
- local RBAC;
- OIDC login;
- advanced audit retention;
- basic alert rules;
- sidecar Agent prototype;
- enterprise backup and restore guide;
- commercial license or entitlement mechanism;
- enterprise documentation.

This is not part of CE v0.1.

---

## 21. Risks

### 21.1 EE becomes too heavy too early

Mitigation:

- keep CE kernel stable first;
- add EE capabilities based on real enterprise demand.

### 21.2 EE duplicates existing platforms

Mitigation:

- integrate with enterprise observability, config, and secret systems rather than replacing all of them.

### 21.3 EE diverges from CE

Mitigation:

- preserve shared contracts;
- keep Agent and Command model compatible.

### 21.4 Commercial boundary damages CE trust

Mitigation:

- keep CE genuinely useful;
- charge for enterprise scale, deployment, compliance, and support.

### 21.5 Enterprise deployment complexity

Mitigation:

- provide clear deployment patterns;
- support PostgreSQL/MySQL first;
- document backup, restore, upgrade, and monitoring.

---

## 22. EE Planning Non-Goals

This document does not define final EE implementation details for:

- exact license enforcement mechanism;
- final installer format;
- final HA architecture;
- final database support matrix;
- final RBAC permission matrix;
- final SSO provider list;
- final observability integration list;
- final support SLA.

These require separate design documents when EE becomes an active target.

---

## 23. Summary

Opstage EE is the future private enterprise deployment edition of the Capsule governance model.

It should extend CE with enterprise identity, deployment, observability, audit, secret integration, Agent diversity, and support capabilities.

The most important EE planning rule is:

> EE should be an enterprise-strength extension of the CE governance kernel, not a separate product that breaks CE compatibility.
