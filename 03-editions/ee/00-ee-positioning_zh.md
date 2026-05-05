<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 00-ee-positioning.md
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

# EE（企业版） Positioning

- Status: Planning
- Edition: EE（企业版）
- Priority: Future
- Audience: founders, product designers, architects, enterprise buyers, platform engineering teams, AI coding agents

This document 定义 the product positioning of **Opstage（运维舞台） EE（企业版） / Enterprise 版本**.

Opstage（运维舞台） EE（企业版） is the future private commercial edition of the `xtrape-capsule` product family. It should extend the CE（社区版） governance kernel for enterprise customers that require private deployment, stronger identity, larger scale, compliance-oriented audit, observability integration, secret integration, and commercial support.

EE（企业版） is not a CE（社区版） v0.1 implementation requirement.

---

## 1. Positioning Statement

Opstage（运维舞台） EE（企业版） is:

> An enterprise-grade private deployment edition of Opstage（运维舞台） for governing Capsule Services inside customer-controlled environments.

It helps organizations make lightweight services, AI automation services, integration services, and operational workers visible, manageable, auditable, and secure without moving the control plane to a hosted SaaS provider.

---

## 2. Product Category

Opstage（运维舞台） EE（企业版） belongs to the category:

```text
Private runtime governance platform for lightweight services
```

It is related to, but different from:

- configuration centers;
- observability platforms;
- Kubernetes platforms;
- service meshes;
- enterprise admin panels;
- workflow engines;
- remote administration tools.

EE（企业版） should not try to replace all enterprise DevOps systems.

Its core category should remain Capsule Service（胶囊服务） governance.

---

## 3. Core Product Promise

Opstage（运维舞台） EE（企业版） promises:

> Keep Capsule Services lightweight and independent, while giving enterprises private control, enterprise identity, auditability, operational visibility, and support.

The product should preserve the same core governance loop as CE（社区版）:

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

EE（企业版） should strengthen this loop for enterprise usage, not replace it with an incompatible model.

---

## 4. Target Customers

EE（企业版） is designed for organizations that need private deployment or stronger governance.

Typical customers:

- enterprises that cannot send governance metadata to a hosted Cloud（云版） service;
- companies operating many internal lightweight services;
- AI automation teams with sensitive accounts and sessions;
- integration service operators managing private platform accounts;
- internal developer platform teams;
- platform engineering teams;
- security-conscious organizations;
- customers needing support, upgrade guidance, and commercial accountability.

---

## 5. Target Buyers and Users

### 5.1 Buyers

Potential EE（企业版） buyers:

- CTO;
- Head of Engineering;
- Head of Platform Engineering;
- Head of DevOps / SRE;
- 安全 lead;
- IT infrastructure lead;
- AI automation business owner.

### 5.2 Users

Potential EE（企业版） users:

- platform engineers;
- backend developers;
- AI automation engineers;
- Integration service developers;
- operators;
- SRE teams;
- security reviewers;
- compliance/audit users;
- support engineers.

---

## 6. Target Scenarios

### 6.1 Private Capsule governance

An enterprise runs many Capsule Services in private infrastructure and wants a unified control plane without using SaaS.

### 6.2 Enterprise Integration operations

A company builds integration services for platforms such as LLM providers, browsers, messaging systems, or internal tools and needs governed access, status, actions, and audit.

### 6.3 Sensitive account and session operations

A service manages accounts, sessions, cookies, OAuth states, or browser contexts. EE（企业版） 提供 visibility and safe predefined operations while keeping raw secrets inside the customer environment.

### 6.4 Larger Agent（代理） fleets

A team operates many Agents and services and needs stronger database support, deployment patterns, observability, and diagnostics than CE（社区版）.

### 6.5 Compliance-oriented operations

A company needs audit retention, audit export, permission changes, action history, and operational traceability.

### 6.6 Enterprise identity integration

An organization needs Opstage（运维舞台） integrated with existing identity systems such as OIDC, LDAP, SAML, or enterprise SSO.

---

## 7. Core Value Proposition

EE（企业版） should provide enterprise value through eight main areas.

### 7.1 Private control

Customers deploy Opstage（运维舞台） inside their own environment.

This 支持 security, compliance, data residency, and internal operations policies.

### 7.2 Enterprise identity

EE（企业版） can integrate with enterprise identity providers and permission models.

Potential capabilities:

```text
RBAC
SSO
OIDC
LDAP
SAML
SCIM
service accounts
API keys
```

### 7.3 Stronger deployment

EE（企业版） can support deployment models beyond CE（社区版） single-container mode.

Potential deployment options:

```text
Docker Compose
Kubernetes / Helm
VM-based deployment
private cloud deployment
HA deployment
```

### 7.4 Enterprise database support

EE（企业版） can support production databases such as:

```text
PostgreSQL
MySQL
```

and provide backup, restore, migration, and tuning guidance.

### 7.5 Operational scale

EE（企业版） can support larger Agent（代理） and Capsule Service（胶囊服务） fleets with better diagnostics, retention, and performance.

### 7.6 Observability integration

EE（企业版） can integrate with enterprise logging, metrics, tracing, and alerting systems.

Examples:

```text
Prometheus
Grafana
Loki
Elasticsearch
OpenTelemetry
SIEM systems
```

### 7.7 Secret integration

EE（企业版） can integrate with enterprise secret providers while preserving the `secretRef` boundary.

Examples:

```text
HashiCorp Vault
AWS Secrets Manager
Azure Key Vault
Google Secret Manager
Kubernetes Secrets
```

### 7.8 Commercial support

EE（企业版） 提供 vendor-backed support, upgrade guidance, deployment documentation, and enterprise accountability.

---

## 8. Differentiation from CE（社区版）

CE（社区版） is the open-source, lightweight, self-hosted edition.

EE（企业版） is the private enterprise edition.

Good EE（企业版） differentiation:

- enterprise identity;
- RBAC and permissions;
- production database support;
- stronger deployment options;
- high availability;
- audit retention and export;
- observability integrations;
- secret provider integrations;
- Agent（代理） diversity;
- commercial support.

Bad EE（企业版） differentiation:

- CE（社区版） cannot register Agents;
- CE（社区版） cannot execute predefined actions;
- CE（社区版） cannot view audit logs;
- CE（社区版） Agent（代理） SDK is intentionally incomplete.

The commercial boundary should be based on enterprise needs, not crippling the CE（社区版） kernel.

---

## 9. Differentiation from Cloud（云版）

Cloud（云版） is hosted SaaS.

EE（企业版） is private deployment.

||Area|EE（企业版）|Cloud（云版）||
|---|---|---|
||Control plane|customer-controlled|provider-hosted||
||Data boundary|customer private environment|shared responsibility||
||Operations|customer/vendor supported|provider-operated||
||Identity|enterprise identity systems|SaaS organization/team identity||
||Billing|license or support contract|subscription||
||Upgrades|customer-controlled|provider-managed||
||Best for|private/security-sensitive customers|managed convenience||

EE（企业版） should appeal to customers who want Opstage（运维舞台）'s capabilities but cannot or do not want to use a hosted Cloud（云版） service.

---

## 10. Market Timing

EE（企业版） should not be built before the CE（社区版） governance kernel is validated.

Recommended sequence:

```text
1. Build CE MVP.
2. Release CE publicly.
3. Collect real usage feedback.
4. Stabilize Agent, Command, Audit, and Status models.
5. Identify real enterprise requirements.
6. Build EE around validated enterprise demand.
```

EE（企业版） should be demand-driven, not assumption-driven.

---

## 11. Commercial Positioning

EE（企业版） should be positioned as a commercial private deployment product.

Possible commercial forms:

- annual license;
- subscription license;
- support contract;
- enterprise deployment package;
- private registry access;
- professional services;
- paid upgrade support;
- custom integration support.

The main value should be:

```text
enterprise control + enterprise security + operational scale + support
```

not artificial CE（社区版） limitations.

---

## 12. Messaging

### 12.1 Short description

```text
Private enterprise control plane for Capsule Services.
```

### 12.2 Longer description

```text
Opstage EE helps organizations privately deploy an enterprise-grade control plane for registering, observing, operating, and auditing Capsule Services across internal environments.
```

### 12.3 安全-facing message

```text
Keep the control plane and governance metadata inside your own environment while integrating with enterprise identity, audit, observability, and secret systems.
```

### 12.4 Platform-facing message

```text
Give platform teams a governed way to manage lightweight services, AI automation workers, integration services, and operational agents without forcing them into a heavy microservice platform.
```

---

## 13. What EE（企业版） Is Not

EE（企业版） should not be positioned as:

- a Kubernetes replacement;
- a full observability platform replacement;
- a full configuration center replacement;
- a generic remote shell platform;
- a browser automation platform by itself;
- a workflow engine as the primary identity;
- a completely separate product from CE（社区版）.

EE（企业版） may integrate with or extend some of these areas, but its main identity should remain Capsule governance.

---

## 14. Product Boundaries

### 14.1 EE（企业版） should include eventually

Potential EE（企业版） capabilities:

- production database support;
- enterprise deployment guides;
- RBAC;
- SSO/OIDC/LDAP/SAML;
- audit retention and export;
- alert rules;
- observability integrations;
- secret provider integrations;
- sidecar/external Agents;
- multi-language Agent（代理） SDKs;
- backup and restore guidance;
- commercial support.

### 14.2 EE（企业版） should not necessarily include first

Potential later items:

- full marketplace;
- full workflow engine;
- deep Kubernetes operator;
- complete SIEM product;
- full secret vault built from scratch;
- full configuration center clone;
- arbitrary remote shell terminal.

---

## 15. EE（企业版） MVP Positioning

A future EE（企业版） MVP should be positioned as:

> CE（社区版）-compatible private deployment with enterprise-ready database, identity, audit, and deployment support.

Possible EE（企业版） MVP features:

- CE（社区版） governance kernel;
- PostgreSQL or MySQL support;
- Docker Compose private deployment;
- basic RBAC;
- OIDC login;
- audit retention configuration;
- basic alert rules;
- deployment documentation;
- backup and restore guide;
- commercial license/support structure.

This is future planning only.

---

## 16. Relationship with Xtrape Capsule

`xtrape-capsule` is the domain and architecture concept.

Opstage（运维舞台） is the governance platform.

EE（企业版） is one commercial edition of Opstage（运维舞台）.

Recommended naming relationship:

```text
xtrape-capsule       = domain / architecture concept
Opstage              = governance platform
Opstage CE           = open-source community edition
Opstage EE           = enterprise private deployment edition
Opstage Cloud        = hosted SaaS edition
```

EE（企业版） should strengthen the Capsule model rather than redefine it.

---

## 17. Competitive Framing

EE（企业版） should be framed around the AI-era service sprawl problem.

Problem statement:

```text
AI-era teams will create more small services, agents, workers, connectors, integration adapters, account/session managers, and automation runtimes. These are easy to create but hard to govern over time.
```

EE（企业版） answer:

```text
Deploy a private enterprise control plane that makes these services visible, operable, auditable, and integrated with enterprise systems.
```

This framing is sharper than generic DevOps or admin-platform messaging.

---

## 18. Risks in Positioning

### 18.1 Too enterprise too early

If EE（企业版） is designed before CE（社区版） is validated, it may become heavy and speculative.

Mitigation:

- build CE（社区版） first;
- let real enterprise needs drive EE（企业版）.

### 18.2 Too broad

If EE（企业版） is marketed as observability + config + workflow + Kubernetes + remote shell, the message becomes unclear.

Mitigation:

- keep focus on Capsule governance.

### 18.3 CE（社区版） trust damage

If EE（企业版） is built by crippling CE（社区版）, open-source trust will suffer.

Mitigation:

- keep CE（社区版） genuinely useful;
- charge for enterprise capabilities.

### 18.4 Integration overload

EE（企业版） may try to integrate with too many enterprise systems too early.

Mitigation:

- prioritize identity, database, audit, and deployment first.

### 18.5 部署 support burden

Private deployment creates support complexity.

Mitigation:

- define supported deployment patterns clearly;
- avoid supporting every possible environment too early.

---

## 19. Success Criteria

EE（企业版） positioning is successful when customers understand that:

- EE（企业版） is private deployment, not hosted SaaS;
- EE（企业版） extends CE（社区版） instead of replacing it;
- CE（社区版） remains useful and open-source;
- EE（企业版） adds enterprise security, deployment, audit, database, observability, and support capabilities;
- Capsule Services remain lightweight and independent;
- Agents remain the core governance bridge;
- raw secrets should not be stored in Opstage（运维舞台） by default;
- EE（企业版） is suitable for security-sensitive and compliance-conscious organizations.

---

## 20. Summary

Opstage（运维舞台） EE（企业版） should be positioned as the enterprise private deployment edition of the Capsule governance model.

It should serve organizations that want the Opstage（运维舞台） control plane inside their own environment with enterprise-grade identity, audit, deployment, observability, secret integration, and support.

The most important EE（企业版） positioning rule is:

> EE（企业版） sells enterprise control, scale, security, integration, and support — not artificial limitations of CE（社区版）.
