
# EE Commercial Packaging

- Status: Planning
- Edition: EE
- Priority: Future
- Audience: founders, product managers, architects, enterprise buyers, sales engineers, support engineers, AI coding agents

This document defines the planned commercial packaging model for **Opstage EE / Enterprise Edition**.

Opstage EE is the future private commercial edition of the `xtrape-capsule` product family. Commercial packaging is not a CE v0.1 implementation requirement.

---

## 1. Purpose

The purpose of this document is to define:

- how Opstage EE may be packaged commercially;
- what value EE should sell;
- what should remain available in CE;
- how licensing, support, deployment packages, and enterprise features may be organized;
- how EE differs from CE and Cloud commercially;
- how to avoid damaging CE trust with artificial restrictions;
- which commercial concepts CE should not implement.

The key rule is:

> EE should sell enterprise deployment, security, scale, integrations, compliance, and support — not artificial limitations of CE.

---

## 2. Commercial Goal

The goal of EE commercial packaging is:

> Create a sustainable private-deployment product for customers that need enterprise-grade Opstage capabilities inside their own environment.

EE should provide commercial value through:

- private enterprise deployment;
- production database support;
- enterprise identity and RBAC;
- stronger audit and compliance features;
- observability integrations;
- secret provider integrations;
- high availability and upgrade support;
- additional Agent modes and SDKs;
- deployment documentation and tooling;
- commercial support and accountability.

---

## 3. EE Commercial Packaging Is Not CE v0.1

CE v0.1 must not implement commercial packaging capabilities.

Out of scope for CE v0.1:

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

CE should remain a genuinely useful open-source product.

---

## 4. Product Relationship

Recommended edition relationship:

```text
Opstage CE      = open-source community edition
Opstage EE      = private enterprise commercial edition
Opstage Cloud   = hosted SaaS edition
```

Commercial distinction:

| Edition | Commercial Model | Deployment |
|---|---|---|
| CE | open-source | self-hosted, lightweight |
| EE | license / subscription / support contract | customer private environment |
| Cloud | SaaS subscription | provider-hosted |

EE and Cloud may share some commercial features, but they solve different deployment needs.

---

## 5. What EE Should Sell

EE should sell enterprise value.

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

EE should not sell basic governance by removing it from CE.

---

## 6. What CE Should Keep

CE should keep the core governance loop:

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

CE should include:

- SQLite default;
- local admin login;
- Node.js embedded Agent SDK;
- Agent registration;
- health visibility;
- config visibility;
- predefined actions;
- Commands and CommandResults;
- basic audit logs;
- Docker quick start;
- demo Capsule Service.

CE should not feel like a broken trial.

---

## 7. Commercial Boundary Principle

Good EE boundaries are based on enterprise needs:

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

Bad EE boundaries are based on crippling CE:

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

EE may be packaged in several ways.

### 8.1 Annual enterprise license

Customer pays an annual license for private deployment.

Useful for:

- enterprise procurement;
- predictable revenue;
- support contracts;
- offline deployment.

### 8.2 Subscription license

Customer pays recurring subscription for EE access and support.

Useful for:

- mid-size companies;
- renewal-based commercial model;
- feature entitlement updates.

### 8.3 Support contract

Customer may pay for support around EE deployment.

Useful for:

- customers who need help deploying and operating;
- private environment onboarding;
- upgrade assistance.

### 8.4 Professional services

Optional services may include:

- deployment setup;
- custom Agent integration;
- enterprise identity integration;
- observability integration;
- secret provider integration;
- migration support;
- security review support.

### 8.5 Private build or appliance

Long-term EE may provide:

- private container registry;
- offline package;
- air-gapped bundle;
- appliance-style deployment.

---

## 9. License Model

EE may use a license mechanism.

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

For early EE, avoid heavy license enforcement until real enterprise customers exist.

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
- break Agent communication silently.

---

## 10. Entitlement Model

EE may use feature entitlements.

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

EE packaging may include capacity dimensions.

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

EE private deployment should not feel like overly granular SaaS billing.

Avoid charging for every small event too early.

---

## 12. Candidate EE Packages

This is planning only and not final pricing.

### 12.1 EE Standard

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

### 12.2 EE Business

Purpose:

- larger private deployments and stronger operations.

Possible capabilities:

- higher Agent and service capacity;
- advanced audit retention;
- observability integrations;
- secret provider integration;
- sidecar Agent;
- backup and restore tooling;
- priority support.

### 12.3 EE Enterprise

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

Support is a major EE commercial value.

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

### 13.2 Priority support

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

## 14. Deployment Package

EE should provide a private deployment package.

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

Early EE may start with Docker Compose and external database support.

Kubernetes and air-gapped packages can come later.

---

## 15. Private Registry and Distribution

EE may be distributed through:

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

## 16. Documentation Package

EE should include enterprise documentation.

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

Documentation is part of the commercial product.

---

## 17. Professional Services Packaging

Professional services may be sold separately or bundled.

Possible services:

- installation assistance;
- enterprise identity setup;
- database setup review;
- observability integration;
- secret provider integration;
- Agent SDK integration;
- sidecar/external Agent design;
- migration from CE;
- training workshop;
- architecture review.

Professional services should not be required for normal installation, but can accelerate enterprise adoption.

---

## 18. CE to EE Upgrade Path

A clear CE-to-EE upgrade path is important.

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

Early EE may not support full automated migration, but the path should be designed.

---

## 19. EE to Cloud Relationship

Some customers may later move between EE and Cloud.

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

EE is suitable when customer needs include:

- private deployment;
- enterprise identity;
- more Agents or services than CE comfortably supports;
- production database;
- audit retention/export;
- secret provider integration;
- compliance review;
- vendor support;
- high availability;
- controlled upgrades.

Cloud is more suitable when the customer prefers managed SaaS and can send governance metadata to a hosted control plane.

CE is suitable for individuals, small teams, prototypes, and open-source self-hosted use.

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

### 23.1 CE trust damage

Risk:

- users feel CE is intentionally crippled.

Mitigation:

- keep CE genuinely useful;
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

- EE sales cycles are long.

Mitigation:

- use CE adoption and Cloud trials to generate demand;
- target focused early enterprise scenarios.

---

## 24. Commercial Anti-Patterns

Avoid these patterns.

### 24.1 CE as broken demo

CE should not be reduced to a marketing shell.

### 24.2 Charging for basic safety

Basic audit and safe predefined actions should exist in CE.

### 24.3 License failure deletes or hides data

License enforcement must not compromise customer data access or audit integrity.

### 24.4 Too many micro-entitlements

Enterprise packaging should be understandable.

### 24.5 Selling unsupported future features

Roadmap items should not be presented as delivered features.

### 24.6 Professional services required for basic deployment

Normal EE installation should be documented and repeatable.

---

## 25. EE Commercial MVP Candidate

A future EE commercial MVP may include:

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

Long-term EE commercial packaging may include:

- offline license file;
- private customer portal;
- signed release artifacts;
- air-gapped package;
- Helm chart;
- HA deployment package;
- SAML/LDAP/SCIM;
- SIEM integration;
- enterprise secret provider packs;
- premium Agent packs;
- custom SLA;
- professional services catalog.

---

## 27. CE Reservations

CE may reserve technical extension points such as:

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

CE must not implement commercial packaging concepts:

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

EE commercial packaging planning is acceptable when:

- EE commercial value is based on enterprise capabilities;
- CE remains genuinely useful;
- license and entitlement models are optional future work;
- deployment package and support package are clearly defined;
- CE-to-EE upgrade path is considered;
- support tiers and professional services are identified;
- commercial anti-patterns are explicit;
- CE v0.1 is not required to implement commercial restrictions.

---

## 29. Summary

Opstage EE commercial packaging should make private enterprise deployment sustainable without weakening the open-source CE foundation.

The most important commercial packaging rule is:

> Package EE around enterprise control, security, deployment, integrations, compliance, and support — while keeping CE a real open-source product.
