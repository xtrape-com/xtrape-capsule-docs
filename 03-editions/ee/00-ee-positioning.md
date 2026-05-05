---
status: proposed
audience: founders
stability: evolving
last_reviewed: 2026-05-05
edition: ee
phase: future
---

# EE Positioning

- Status: Planning
- Edition: EE
- Priority: Future
- Audience: founders, product designers, architects, enterprise buyers, platform engineering teams, AI coding agents

This document defines the product positioning of **Opstage EE / Enterprise Edition**.

Opstage EE is the future private commercial edition of the `xtrape-capsule` product family. It should extend the CE
governance kernel for enterprise customers that require private deployment, stronger identity, larger scale,
compliance-oriented audit, observability integration, secret integration, and commercial support.

EE is not a CE v0.1 implementation requirement.

---

## 1. Positioning Statement

Opstage EE is:

> An enterprise-grade private deployment edition of Opstage for governing Capsule Services inside customer-controlled environments.

It helps organizations make lightweight services, AI automation services, integration services, and operational workers
visible, manageable, auditable, and secure without moving the control plane to a hosted SaaS provider.

---

## 2. Product Category

Opstage EE belongs to the category:

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

EE should not try to replace all enterprise DevOps systems.

Its core category should remain Capsule Service governance.

---

## 3. Core Product Promise

Opstage EE promises:

> Keep Capsule Services lightweight and independent, while giving enterprises private control, enterprise identity, auditability, operational visibility, and support.

The product should preserve the same core governance loop as CE:

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

EE should strengthen this loop for enterprise usage, not replace it with an incompatible model.

---

## 4. Target Customers

EE is designed for organizations that need private deployment or stronger governance.

Typical customers:

- enterprises that cannot send governance metadata to a hosted Cloud service;
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

Potential EE buyers:

- CTO;
- Head of Engineering;
- Head of Platform Engineering;
- Head of DevOps / SRE;
- Security lead;
- IT infrastructure lead;
- AI automation business owner.

### 5.2 Users

Potential EE users:

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

A service manages accounts, sessions, cookies, OAuth states, or browser contexts. EE provides visibility and safe
predefined operations while keeping raw secrets inside the customer environment.

### 6.4 Larger Agent fleets

A team operates many Agents and services and needs stronger database support, deployment patterns, observability, and diagnostics than CE.

### 6.5 Compliance-oriented operations

A company needs audit retention, audit export, permission changes, action history, and operational traceability.

### 6.6 Enterprise identity integration

An organization needs Opstage integrated with existing identity systems such as OIDC, LDAP, SAML, or enterprise SSO.

---

## 7. Core Value Proposition

EE should provide enterprise value through eight main areas.

### 7.1 Private control

Customers deploy Opstage inside their own environment.

This supports security, compliance, data residency, and internal operations policies.

### 7.2 Enterprise identity

EE can integrate with enterprise identity providers and permission models.

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

EE can support deployment models beyond CE single-container mode.

Potential deployment options:

```text
Docker Compose
Kubernetes / Helm
VM-based deployment
private cloud deployment
HA deployment
```

### 7.4 Enterprise database support

EE can support production databases such as:

```text
PostgreSQL
MySQL
```

and provide backup, restore, migration, and tuning guidance.

### 7.5 Operational scale

EE can support larger Agent and Capsule Service fleets with better diagnostics, retention, and performance.

### 7.6 Observability integration

EE can integrate with enterprise logging, metrics, tracing, and alerting systems.

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

EE can integrate with enterprise secret providers while preserving the `secretRef` boundary.

Examples:

```text
HashiCorp Vault
AWS Secrets Manager
Azure Key Vault
Google Secret Manager
Kubernetes Secrets
```

### 7.8 Commercial support

EE provides vendor-backed support, upgrade guidance, deployment documentation, and enterprise accountability.

---

## 8. Differentiation from CE

CE is the open-source, lightweight, self-hosted edition.

EE is the private enterprise edition.

Good EE differentiation:

- enterprise identity;
- RBAC and permissions;
- production database support;
- stronger deployment options;
- high availability;
- audit retention and export;
- observability integrations;
- secret provider integrations;
- Agent diversity;
- commercial support.

Bad EE differentiation:

- CE cannot register Agents;
- CE cannot execute predefined actions;
- CE cannot view audit logs;
- CE Agent SDK is intentionally incomplete.

The commercial boundary should be based on enterprise needs, not crippling the CE kernel.

---

## 9. Differentiation from Cloud

Cloud is hosted SaaS.

EE is private deployment.

| Area | EE | Cloud |
|---|---|---|
| Control plane | customer-controlled | provider-hosted |
| Data boundary | customer private environment | shared responsibility |
| Operations | customer/vendor supported | provider-operated |
| Identity | enterprise identity systems | SaaS organization/team identity |
| Billing | license or support contract | subscription |
| Upgrades | customer-controlled | provider-managed |
| Best for | private/security-sensitive customers | managed convenience |

EE should appeal to customers who want Opstage's capabilities but cannot or do not want to use a hosted Cloud service.

---

## 10. Market Timing

EE should not be built before the CE governance kernel is validated.

Recommended sequence:

```text
1. Build CE MVP.
2. Release CE publicly.
3. Collect real usage feedback.
4. Stabilize Agent, Command, Audit, and Status models.
5. Identify real enterprise requirements.
6. Build EE around validated enterprise demand.
```

EE should be demand-driven, not assumption-driven.

---

## 11. Commercial Positioning

EE should be positioned as a commercial private deployment product.

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

not artificial CE limitations.

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

### 12.3 Security-facing message

```text
Keep the control plane and governance metadata inside your own environment while integrating with enterprise identity, audit, observability, and secret systems.
```

### 12.4 Platform-facing message

```text
Give platform teams a governed way to manage lightweight services, AI automation workers, integration services, and operational agents without forcing them into a heavy microservice platform.
```

---

## 13. What EE Is Not

EE should not be positioned as:

- a Kubernetes replacement;
- a full observability platform replacement;
- a full configuration center replacement;
- a generic remote shell platform;
- a browser automation platform by itself;
- a workflow engine as the primary identity;
- a completely separate product from CE.

EE may integrate with or extend some of these areas, but its main identity should remain Capsule governance.

---

## 14. Product Boundaries

### 14.1 EE should include eventually

Potential EE capabilities:

- production database support;
- enterprise deployment guides;
- RBAC;
- SSO/OIDC/LDAP/SAML;
- audit retention and export;
- alert rules;
- observability integrations;
- secret provider integrations;
- sidecar/external Agents;
- multi-language Agent SDKs;
- backup and restore guidance;
- commercial support.

### 14.2 EE should not necessarily include first

Potential later items:

- full marketplace;
- full workflow engine;
- deep Kubernetes operator;
- complete SIEM product;
- full secret vault built from scratch;
- full configuration center clone;
- arbitrary remote shell terminal.

---

## 15. EE MVP Positioning

A future EE MVP should be positioned as:

> CE-compatible private deployment with enterprise-ready database, identity, audit, and deployment support.

Possible EE MVP features:

- CE governance kernel;
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

Opstage is the governance platform.

EE is one commercial edition of Opstage.

Recommended naming relationship:

```text
xtrape-capsule       = domain / architecture concept
Opstage              = governance platform
Opstage CE           = open-source community edition
Opstage EE           = enterprise private deployment edition
Opstage Cloud        = hosted SaaS edition
```

EE should strengthen the Capsule model rather than redefine it.

---

## 17. Competitive Framing

EE should be framed around the AI-era service sprawl problem.

Problem statement:

```text
AI-era teams will create more small services, agents, workers, connectors, integration adapters, account/session managers, and automation runtimes. These are easy to create but hard to govern over time.
```

EE answer:

```text
Deploy a private enterprise control plane that makes these services visible, operable, auditable, and integrated with enterprise systems.
```

This framing is sharper than generic DevOps or admin-platform messaging.

---

## 18. Risks in Positioning

### 18.1 Too enterprise too early

If EE is designed before CE is validated, it may become heavy and speculative.

Mitigation:

- build CE first;
- let real enterprise needs drive EE.

### 18.2 Too broad

If EE is marketed as observability + config + workflow + Kubernetes + remote shell, the message becomes unclear.

Mitigation:

- keep focus on Capsule governance.

### 18.3 CE trust damage

If EE is built by crippling CE, open-source trust will suffer.

Mitigation:

- keep CE genuinely useful;
- charge for enterprise capabilities.

### 18.4 Integration overload

EE may try to integrate with too many enterprise systems too early.

Mitigation:

- prioritize identity, database, audit, and deployment first.

### 18.5 Deployment support burden

Private deployment creates support complexity.

Mitigation:

- define supported deployment patterns clearly;
- avoid supporting every possible environment too early.

---

## 19. Success Criteria

EE positioning is successful when customers understand that:

- EE is private deployment, not hosted SaaS;
- EE extends CE instead of replacing it;
- CE remains useful and open-source;
- EE adds enterprise security, deployment, audit, database, observability, and support capabilities;
- Capsule Services remain lightweight and independent;
- Agents remain the core governance bridge;
- raw secrets should not be stored in Opstage by default;
- EE is suitable for security-sensitive and compliance-conscious organizations.

---

## 20. Summary

Opstage EE should be positioned as the enterprise private deployment edition of the Capsule governance model.

It should serve organizations that want the Opstage control plane inside their own environment with enterprise-grade
identity, audit, deployment, observability, secret integration, and support.

The most important EE positioning rule is:

> EE sells enterprise control, scale, security, integration, and support — not artificial limitations of CE.
