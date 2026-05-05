---
status: draft
audience: founders
stability: unstable
last_reviewed: 2026-05-05
edition: ee
phase: future
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 07-ee-commercial-packaging.md
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


# EE（企业版） Commercial Packaging

- Status: Planning
- Edition: EE（企业版）
- Priority: Future
- Audience: founders, product managers, architects, enterprise buyers, sales engineers, support engineers, AI coding agents

This document 定义 the planned commercial packaging model for **Opstage（运维舞台） EE（企业版） / Enterprise 版本**.

Opstage（运维舞台） EE（企业版） is the future private commercial edition of the `xtrape-capsule` product family. Commercial packaging is not a CE（社区版） v0.1 implementation requirement.

---

## 1. Purpose

The purpose of this document is to define:

- how Opstage（运维舞台） EE（企业版） may be packaged commercially;
- what value EE（企业版） should sell;
- what should remain available in CE（社区版）;
- how licensing, support, deployment packages, and enterprise features may be organized;
- how EE（企业版） differs from CE（社区版） and Cloud（云版） commercially;
- how to avoid damaging CE（社区版） trust with artificial restrictions;
- which commercial concepts CE（社区版） should not implement.

The key rule is:

> EE（企业版） should sell enterprise deployment, security, scale, integrations, compliance, and support — not artificial limitations of CE（社区版）.

---

## 2. Commercial Goal

The goal of EE（企业版） commercial packaging is:

> Create a sustainable private-deployment product for customers that need enterprise-grade Opstage（运维舞台） capabilities inside their own environment.

EE（企业版） should provide commercial value through:

- private enterprise deployment;
- production database support;
- enterprise identity and RBAC;
- stronger audit and compliance features;
- observability integrations;
- secret provider integrations;
- high availability and upgrade support;
- additional Agent（代理） modes and SDKs;
- deployment documentation and tooling;
- commercial support and accountability.

---

## 3. EE（企业版） Commercial Packaging Is Not CE（社区版） v0.1

CE（社区版） v0.1 must not implement commercial packaging capabilities.

Out of scope for CE（社区版） v0.1:

- license key enforcement;
- offline license file;
- subscription contract tracking;
- support entitlement checks;
- feature entitlement engine;
- enterprise installer access control;
- private registry authentication;
- paid plan enforcement;
- commercial telemetry;
- customer account portal;
- renewal workflow.

CE（社区版） should remain a genuinely useful open-source product.

---

## 4. Product Relationship

Recommended edition relationship:

```text
Opstage CE      = open-source community edition
Opstage EE      = private enterprise commercial edition
Opstage Cloud   = hosted SaaS edition
```

Commercial distinction:

||版本|Commercial Model|部署||
|---|---|---|
||CE（社区版）|open-source|self-hosted, lightweight||
||EE（企业版）|license / subscription / support contract|customer private environment||
||Cloud（云版）|SaaS subscription|provider-hosted||

EE（企业版） and Cloud（云版） may share some commercial features, but they solve different deployment needs.

---

## 5. What EE（企业版） Should Sell

EE（企业版） should sell enterprise value.

Primary value areas:

```text
private deployment
enterprise identity
RBAC and permissions
production database support
high availability
advanced audit
compliance-oriented exports
observability integrations
secret provider integrations
Agent expansion
upgrade and migration tooling
support and SLA
```

EE（企业版） should not sell basic governance by removing it from CE（社区版）.

---

## 6. What CE（社区版） Should Keep

CE（社区版） should keep the core governance loop:

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

CE（社区版） should include:

- SQLite default;
- local admin login;
- Node.js embedded Agent（代理） SDK;
- Agent（代理） registration;
- health visibility;
- config visibility;
- predefined actions;
- Commands and CommandResults;
- basic audit logs;
- Docker quick start;
- demo Capsule Service（胶囊服务）.

CE（社区版） should not feel like a broken trial.

---

## 7. Commercial Boundary Principle

Good EE（企业版） boundaries are based on enterprise needs:

```text
scale
security
identity
compliance
deployment
support
integration
reliability
```

Bad EE（企业版） boundaries are based on crippling CE（社区版）:

```text
CE cannot run actions
CE cannot view audit logs
CE cannot use Agent SDK
CE cannot persist data
CE cannot register real Agents
```

The commercial boundary should preserve open-source trust.

---

## 8. Packaging Options

EE（企业版） may be packaged in several ways.

### 8.1 Annual enterprise license

Customer pays an annual license for private deployment.

Useful for:

- enterprise procurement;
- predictable revenue;
- support contracts;
- offline deployment.

### 8.2 Subscription license

Customer pays recurring subscription for EE（企业版） access and support.

Useful for:

- mid-size companies;
- renewal-based commercial model;
- feature entitlement updates.

### 8.3 Support contract

Customer may pay for support around EE（企业版） deployment.

Useful for:

- customers who need help deploying and operating;
- private environment onboarding;
- upgrade assistance.

### 8.4 Professional services

Optional services may include:

- deployment setup;
- custom Agent（代理） integration;
- enterprise identity integration;
- observability integration;
- secret provider integration;
- migration support;
- security review support.

### 8.5 Private build or appliance

Long-term EE（企业版） may provide:

- private container registry;
- offline package;
- air-gapped bundle;
- appliance-style deployment.

---

## 9. License Model

EE（企业版） may use a license mechanism.

Possible license forms:

```text
online license check
offline signed license file
license key
support entitlement token
private registry access
contract-only license without runtime enforcement
```

### 9.1 Recommended early approach

For early EE（企业版）, avoid heavy license enforcement until real enterprise customers exist.

Recommended early path:

```text
commercial contract + private distribution + support entitlement
```

Runtime license enforcement can be added later if needed.

### 9.2 Offline license

Enterprise customers may require offline deployment.

Offline license file may contain:

```text
customer ID
license ID
edition
features
expiration
support level
signature
issuedAt
```

### 9.3 License safety

License enforcement must not:

- delete customer data;
- hide audit logs completely;
- block data export needed for compliance;
- expose customer secrets;
- break Agent（代理） communication silently.

---

## 10. Entitlement Model

EE（企业版） may use feature entitlements.

Possible entitlements:

```text
rbac.enabled
sso.enabled
auditExport.enabled
ha.enabled
postgres.enabled
mysql.enabled
alerting.enabled
secretProviders.enabled
agent.sidecar.enabled
agent.java.enabled
supportBundle.enabled
```

Entitlements should be simple and understandable.

Avoid deeply fragmented feature flags that make the product confusing.

---

## 11. Capacity-Based Packaging

EE（企业版） packaging may include capacity dimensions.

Possible dimensions:

```text
number of Agents
number of Capsule Services
number of Workspaces
number of users
number of command executions
amount of retained audit data
support level
```

### 11.1 Recommended primary dimensions

Recommended primary dimensions:

```text
Agents
Capsule Services
Support level
```

These are easiest to understand and map to product scale.

### 11.2 Avoid excessive metering

EE（企业版） private deployment should not feel like overly granular SaaS billing.

Avoid charging for every small event too early.

---

## 12. Candidate EE（企业版） Packages

This is planning only and not final pricing.

### 12.1 EE（企业版） Standard

Purpose:

- private deployment for small to mid-size teams.

Possible capabilities:

- PostgreSQL/MySQL support;
- Docker Compose deployment;
- RBAC;
- OIDC login;
- audit export;
- basic alerting;
- support bundle;
- standard support.

### 12.2 EE（企业版） Business

Purpose:

- larger private deployments and stronger operations.

Possible capabilities:

- higher Agent（代理） and service capacity;
- advanced audit retention;
- observability integrations;
- secret provider integration;
- sidecar Agent（代理）;
- backup and restore tooling;
- priority support.

### 12.3 EE（企业版） Enterprise

Purpose:

- large enterprises, regulated environments, and custom needs.

Possible capabilities:

- custom capacity;
- SAML/LDAP/SCIM;
- HA deployment;
- Kubernetes / Helm support;
- compliance reports;
- SIEM integration;
- air-gapped package;
- custom SLA;
- professional services.

---

## 13. Support Packaging

Support is a major EE（企业版） commercial value.

Possible support tiers:

```text
Standard
Priority
Enterprise
Custom
```

### 13.1 Standard support

May include:

- documentation-based support;
- issue response within business days;
- deployment guidance;
- upgrade notes.

### 13.2 优先级 support

May include:

- faster response;
- private support channel;
- upgrade planning assistance;
- troubleshooting sessions;
- support bundle review.

### 13.3 Enterprise support

May include:

- SLA-backed support;
- named support contacts;
- architecture review;
- security review assistance;
- custom integration guidance;
- incident support.

---

## 14. 部署 Package

EE（企业版） should provide a private deployment package.

Possible deliverables:

```text
container images
Docker Compose templates
Helm chart
configuration examples
migration scripts
backup/restore scripts
support bundle tool
installation guide
upgrade guide
security hardening guide
```

Early EE（企业版） may start with Docker Compose and external database support.

Kubernetes and air-gapped packages can come later.

---

## 15. Private Registry and Distribution

EE（企业版） may be distributed through:

- private container registry;
- private Git repository;
- downloadable release bundle;
- customer portal;
- offline package.

Distribution should support enterprise controls such as:

- versioned releases;
- checksums;
- signed artifacts;
- release notes;
- upgrade instructions;
- security advisories.

---

## 16. 文档 Package

EE（企业版） should include enterprise documentation.

Required docs may include:

```text
installation guide
configuration reference
upgrade guide
backup and restore guide
security hardening guide
SSO setup guide
RBAC guide
audit and compliance guide
secret provider integration guide
Agent deployment guide
troubleshooting guide
support bundle guide
```

文档 is part of the commercial product.

---

## 17. Professional Services Packaging

Professional services may be sold separately or bundled.

Possible services:

- installation assistance;
- enterprise identity setup;
- database setup review;
- observability integration;
- secret provider integration;
- Agent（代理） SDK integration;
- sidecar/external Agent（代理） design;
- migration from CE（社区版）;
- training workshop;
- architecture review.

Professional services should not be required for normal installation, but can accelerate enterprise adoption.

---

## 18. CE（社区版） to EE（企业版） Upgrade Path

A clear CE（社区版）-to-EE（企业版） upgrade path is important.

Possible upgrade steps:

```text
1. Backup CE data.
2. Export or migrate SQLite data.
3. Provision PostgreSQL/MySQL.
4. Run migration tool.
5. Deploy EE Backend/UI.
6. Configure identity and security.
7. Reuse or rotate Agent tokens.
8. Validate Agents and Capsule Services.
9. Validate audit and command history.
```

Early EE（企业版） may not support full automated migration, but the path should be designed.

---

## 19. EE（企业版） to Cloud（云版） Relationship

Some customers may later move between EE（企业版） and Cloud（云版）.

Potential paths:

```text
CE -> EE
CE -> Cloud
EE -> Cloud
Cloud -> EE
```

Not all paths need to be fully automated early.

Data portability should be considered:

- Agents;
- Capsule Services;
- manifests;
- commands;
- audit logs;
- configs;
- users and permissions.

SecretRefs may require customer-specific migration handling.

---

## 20. Commercial Feature Matrix

A public or sales-facing feature matrix may compare editions.

Example categories:

```text
Core governance
Agent SDKs
Deployment
Database
Identity
Security
Audit
Observability
Secrets
Support
Commercial terms
```

Feature matrix should be honest.

Do not overpromise future features as already available.

---

## 21. Sales Qualification

EE（企业版） is suitable when customer needs include:

- private deployment;
- enterprise identity;
- more Agents or services than CE（社区版） comfortably 支持;
- production database;
- audit retention/export;
- secret provider integration;
- compliance review;
- vendor support;
- high availability;
- controlled upgrades.

Cloud（云版） is more suitable when the customer prefers managed SaaS and can send governance metadata to a hosted control plane.

CE（社区版） is suitable for individuals, small teams, prototypes, and open-source self-hosted use.

---

## 22. Pricing Direction

This document does not define final pricing.

Potential pricing basis:

```text
annual base fee
Agent capacity tier
Capsule Service capacity tier
support tier
professional services
custom enterprise contract
```

Pricing should be validated through real customer conversations.

Avoid complex pricing before product-market fit.

---

## 23. Commercial Risks

### 23.1 CE（社区版） trust damage

Risk:

- users feel CE（社区版） is intentionally crippled.

Mitigation:

- keep CE（社区版） genuinely useful;
- sell enterprise capabilities.

### 23.2 Over-fragmented packages

Risk:

- too many packages and entitlements confuse customers.

Mitigation:

- start with simple package tiers.

### 23.3 Heavy license enforcement too early

Risk:

- license system consumes engineering effort before product value is validated.

Mitigation:

- start with contract and distribution control.

### 23.4 Support burden

Risk:

- private deployment support becomes expensive.

Mitigation:

- define supported deployment patterns clearly;
- provide strong docs and support bundle tools.

### 23.5 Enterprise sales cycle risk

Risk:

- EE（企业版） sales cycles are long.

Mitigation:

- use CE（社区版） adoption and Cloud（云版） trials to generate demand;
- target focused early enterprise scenarios.

---

## 24. Commercial Anti-Patterns

Avoid these patterns.

### 24.1 CE（社区版） as broken demo

CE（社区版） should not be reduced to a marketing shell.

### 24.2 Charging for basic safety

Basic audit and safe predefined actions should exist in CE（社区版）.

### 24.3 License failure deletes or hides data

License enforcement must not compromise customer data access or audit integrity.

### 24.4 Too many micro-entitlements

Enterprise packaging should be understandable.

### 24.5 Selling unsupported future features

Roadmap items should not be presented as delivered features.

### 24.6 Professional services required for basic deployment

Normal EE（企业版） installation should be documented and repeatable.

---

## 25. EE（企业版） Commercial MVP Candidate

A future EE（企业版） commercial MVP may include:

- private Docker Compose deployment package;
- PostgreSQL or MySQL support;
- OIDC login;
- basic RBAC;
- audit export;
- configurable audit retention;
- support bundle tool;
- installation guide;
- upgrade guide;
- backup and restore guide;
- security hardening guide;
- commercial support contract;
- private distribution channel.

This candidate should be validated before implementation.

---

## 26. Long-Term Commercial Capabilities

Long-term EE（企业版） commercial packaging may include:

- offline license file;
- private customer portal;
- signed release artifacts;
- air-gapped package;
- Helm chart;
- HA deployment package;
- SAML/LDAP/SCIM;
- SIEM integration;
- enterprise secret provider packs;
- premium Agent（代理） packs;
- custom SLA;
- professional services catalog.

---

## 27. CE（社区版） Reservations

CE（社区版） may reserve technical extension points such as:

```text
workspaceId
agentMode
runtime
database provider abstraction
command delivery abstraction
secretRef
AuditEvent
metadataJson
createdBy
actorType
actorId
resourceType
resourceId
```

CE（社区版） must not implement commercial packaging concepts:

```text
license key
license server
offline license file
support entitlement
feature entitlement engine
paid plan enforcement
private registry auth
customer portal
commercial telemetry
```

---

## 28. Acceptance Criteria

EE（企业版） commercial packaging planning is acceptable when:

- EE（企业版） commercial value is based on enterprise capabilities;
- CE（社区版） remains genuinely useful;
- license and entitlement models are optional future work;
- deployment package and support package are clearly defined;
- CE（社区版）-to-EE（企业版） upgrade path is considered;
- support tiers and professional services are identified;
- commercial anti-patterns are explicit;
- CE（社区版） v0.1 is not required to implement commercial restrictions.

---

## 29. Summary

Opstage（运维舞台） EE（企业版） commercial packaging should make private enterprise deployment sustainable without weakening the open-source CE（社区版） foundation.

The most important commercial packaging rule is:

> Package EE（企业版） around enterprise control, security, deployment, integrations, compliance, and support — while keeping CE（社区版） a real open-source product.
