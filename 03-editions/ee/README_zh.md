<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: README.md
翻译状态 / Translation Status: 已翻译 / Translated
生成时间 / Generated: 2026-05-01 09:28:54
================================================================================
注意 / Notes:
- 技术术语如 Capsule Service、Agent、Opstage 等保留英文或采用中英对照
- 代码块中的内容不翻译
- 文件路径和 URL 不翻译
- 保持原有的 Markdown 格式结构
================================================================================
-->

# Opstage（运维舞台） EE（企业版） 概述

- Status: Planning
- Edition: EE（企业版）
- Priority: Future
- Audience: founders, product designers, architects, enterprise engineers, backend developers, DevOps engineers, AI coding agents

This document 定义 the planning overview for **Opstage（运维舞台） EE（企业版） / Enterprise 版本**.

Opstage（运维舞台） EE（企业版） is the future private commercial edition of the `xtrape-capsule` product family. It is not a CE（社区版） v0.1 implementation requirement.

---

## 1. Positioning

Opstage（运维舞台） EE（企业版） is:

> A private enterprise deployment edition of Opstage（运维舞台） for organizations that need stronger security, identity, deployment, observability, audit, and support capabilities while keeping the control plane in their own environment.

EE（企业版） should extend the same Capsule governance model established by CE（社区版）:

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

The difference is that EE（企业版） is designed for enterprise private deployment and operational scale.

---

## 2. EE（企业版） Is Not CE（社区版） v0.1

EE（企业版） is a future edition.

CE（社区版） v0.1 must not implement EE（企业版）-only capabilities such as:

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
- sidecar / external Agent（代理） mode;
- Java / Python / Go Agent（代理） SDKs;
- enterprise upgrade and migration tooling;
- enterprise support workflow.

CE（社区版） should reserve extension points for EE（企业版）, but EE（企业版） must not become a dependency of CE（社区版） v0.1.

---

## 3. EE（企业版） Product Goal

The goal of Opstage（运维舞台） EE（企业版） is:

> Provide an enterprise-grade private Opstage（运维舞台） control plane for organizations that need to govern Capsule Services under stricter security, compliance, deployment, and operational requirements.

EE（企业版） should help enterprises:

- deploy Opstage（运维舞台） inside their own infrastructure;
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

Opstage（运维舞台） EE（企业版） is intended for:

- enterprises requiring private deployment;
- organizations with internal compliance requirements;
- teams that cannot use hosted Cloud（云版） for governance data;
- companies with existing identity providers;
- platform engineering teams;
- internal developer platform teams;
- AI automation teams operating many private services;
- Operators managing sensitive accounts with sensitive accounts and sessions;
- customers needing vendor support and upgrade guarantees.

---

## 5. Target Scenarios

### 5.1 Private enterprise deployment

An organization deploys Opstage（运维舞台） inside its own network or private cloud and connects internal Capsule Services through Agents.

### 5.2 Enterprise identity integration

A company needs Opstage（运维舞台） to integrate with SSO, OIDC, LDAP, or SAML so users can access the platform with enterprise accounts.

### 5.3 Larger Agent（代理） and service fleet

A team runs many Agents and Capsule Services and needs stronger database, deployment, and operations support than CE（社区版）.

### 5.4 Compliance-oriented audit

An organization needs longer audit retention, searchable audit events, export, and compliance reporting.

### 5.5 Enterprise observability integration

A company wants Opstage（运维舞台） to integrate with existing log, metric, trace, and alerting systems.

### 5.6 Secure secret integration

A company wants Capsule Services to reference secrets from Vault or enterprise secret managers without exposing raw secrets to Opstage（运维舞台） unnecessarily.

---

## 6. EE（企业版） 架构 Direction

高-level EE（企业版） architecture may include:

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

EE（企业版） should preserve the same core contracts as CE（社区版）:

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

## 7. 部署 Direction

EE（企业版） may support more deployment models than CE（社区版）.

Potential deployment models:

```text
Docker Compose
Kubernetes / Helm
VM-based installation
Private cloud deployment
Dedicated enterprise appliance style deployment
```

Potential EE（企业版） deployment components:

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

CE（社区版） v0.1 should remain single-container and SQLite-first.

---

## 8. Database Direction

CE（社区版） uses SQLite by default.

EE（企业版） should likely support enterprise-grade databases:

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

EE（企业版） database requirements may include:

- migrations;
- backup and restore guidance;
- connection pooling;
- retention policies;
- audit storage strategy;
- performance tuning;
- HA database deployment guidance.

---

## 9. Identity and Access Direction

EE（企业版） should support stronger identity and authorization than CE（社区版）.

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

CE（社区版） v0.1 may support only local admin authentication.

---

## 10. Agent（代理） Direction

CE（社区版） v0.1 implements only Node.js embedded Agent（代理） SDK.

EE（企业版） may add:

- sidecar Agent（代理）;
- external Agent（代理）;
- Java Agent（代理） SDK;
- Python Agent（代理） SDK;
- Go Agent（代理） SDK;
- host-level Agent（代理）;
- Docker host Agent（代理）;
- Kubernetes Agent（代理）;
- Agent（代理） version management;
- Agent（代理） upgrade guidance;
- Agent（代理） diagnostics.

EE（企业版） Agent（代理） expansion should not break CE（社区版） Agent（代理） contracts.

---

## 11. Command Delivery Direction

CE（社区版） v0.1 uses HTTP polling.

EE（企业版） may support:

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

EE（企业版） may provide stronger observability than CE（社区版）.

Potential capabilities:

- centralized log integration;
- log search integration;
- metrics dashboards;
- health history;
- Agent（代理） uptime history;
- command success/failure analytics;
- alert rules;
- notification channels;
- OpenTelemetry integration;
- Prometheus/Grafana integration;
- Loki / Elasticsearch integration.

EE（企业版） should not necessarily become a full observability platform, but it can integrate with enterprise observability systems.

---

## 13. Audit and Compliance Direction

EE（企业版） may support stronger audit and compliance features.

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

CE（社区版） v0.1 only needs lightweight audit logs.

---

## 14. Secret Management Direction

EE（企业版） may integrate with enterprise secret providers.

Potential integrations:

```text
HashiCorp Vault
AWS Secrets Manager
Azure Key Vault
Google Secret Manager
Kubernetes Secrets
enterprise internal secret service
```

EE（企业版） should continue to support the `secretRef` boundary.

Recommended principle:

> EE（企业版） should integrate with enterprise secret systems without requiring raw secrets to be stored in Opstage（运维舞台） by default.

---

## 15. 配置 Management Direction

CE（社区版） v0.1 支持 config visibility only.

EE（企业版） may support stronger configuration management:

- config editing;
- config publishing;
- approval workflow;
- versioning;
- rollback;
- environment promotion;
- config drift detection;
- config reload actions;
- integration with external config centers.

EE（企业版） should avoid becoming merely another Nacos/Apollo clone. Its config features should be tied to Capsule governance and Agent（代理）-based operations.

---

## 16. Licensing and Commercial Direction

EE（企业版） is a commercial private deployment edition.

Potential commercial mechanisms:

- license key;
- offline license file;
- subscription contract;
- support contract;
- enterprise installer access;
- private registry access;
- feature entitlements;
- support SLA.

CE（社区版） should not include license enforcement.

EE（企业版） commercial value should come from enterprise capabilities, scale, deployment, compliance, and support.

---

## 17. EE（企业版） vs CE（社区版）

||Area|CE（社区版）|EE（企业版）||
|---|---|---|
||License|open-source|commercial||
||部署|single-node self-hosted|private enterprise deployment||
||Database|SQLite default|PostgreSQL/MySQL official support||
||Identity|local admin|RBAC, SSO, OIDC/LDAP/SAML||
||Agent（代理）|Node.js embedded|embedded, sidecar, external, multi-language||
||Command delivery|polling|polling, streaming, queue-backed||
||Observability|health visibility|logs, metrics, alerts, integrations||
||Audit|basic audit|advanced audit, retention, export, compliance||
||Secrets|secretRef-ready|enterprise secret integrations||
||Support|community|commercial support||

---

## 18. EE（企业版） vs Cloud（云版）

||Area|EE（企业版）|Cloud（云版）||
|---|---|---|
||部署|customer private environment|hosted by provider||
||Operations|customer/vendor supported|provider-operated||
||Database|customer-managed|provider-managed||
||Identity|enterprise-controlled|SaaS organization/team model||
||Billing|commercial license/support contract|SaaS subscription||
||Data boundary|customer-controlled|shared responsibility||
||Agent（代理） connection|private/customer network|outbound to Cloud（云版） gateway||
||Upgrades|customer-controlled|provider-managed||

EE（企业版） and Cloud（云版） should share core contracts but differ in operating model.

---

## 19. CE（社区版） Reservations for EE（企业版）

CE（社区版） should reserve these EE（企业版）-compatible extension points:

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

CE（社区版） should not implement EE（企业版） systems directly in v0.1.

---

## 20. EE（企业版） MVP Candidate

A future EE（企业版） MVP may include:

- CE（社区版）-compatible core governance;
- PostgreSQL or MySQL support;
- private Docker Compose deployment;
- local RBAC;
- OIDC login;
- advanced audit retention;
- basic alert rules;
- sidecar Agent（代理） prototype;
- enterprise backup and restore guide;
- commercial license or entitlement mechanism;
- enterprise documentation.

This is not part of CE（社区版） v0.1.

---

## 21. Risks

### 21.1 EE（企业版） becomes too heavy too early

Mitigation:

- keep CE（社区版） kernel stable first;
- add EE（企业版） capabilities based on real enterprise demand.

### 21.2 EE（企业版） duplicates existing platforms

Mitigation:

- integrate with enterprise observability, config, and secret systems rather than replacing all of them.

### 21.3 EE（企业版） diverges from CE（社区版）

Mitigation:

- preserve shared contracts;
- keep Agent（代理） and Command model compatible.

### 21.4 Commercial boundary damages CE（社区版） trust

Mitigation:

- keep CE（社区版） genuinely useful;
- charge for enterprise scale, deployment, compliance, and support.

### 21.5 Enterprise deployment complexity

Mitigation:

- provide clear deployment patterns;
- support PostgreSQL/MySQL first;
- document backup, restore, upgrade, and monitoring.

---

## 22. EE（企业版） Planning Non-Goals

This document does not define final EE（企业版） implementation details for:

- exact license enforcement mechanism;
- final installer format;
- final HA architecture;
- final database support matrix;
- final RBAC permission matrix;
- final SSO provider list;
- final observability integration list;
- final support SLA.

These require separate design documents when EE（企业版） becomes an active target.

---

## 23. Summary

Opstage（运维舞台） EE（企业版） is the future private enterprise deployment edition of the Capsule governance model.

It should extend CE（社区版） with enterprise identity, deployment, observability, audit, secret integration, Agent（代理） diversity, and support capabilities.

The most important EE（企业版） planning rule is:

> EE（企业版） should be an enterprise-strength extension of the CE（社区版） governance kernel, not a separate product that breaks CE（社区版） compatibility.
