<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 02-ee-roadmap.md
翻译状态 / Translation Status: 已翻译 / Translated
生成时间 / Generated: 2026-05-01 09:28:55
================================================================================
注意 / Notes:
- 技术术语如 Capsule Service、Agent、Opstage 等保留英文或采用中英对照
- 代码块中的内容不翻译
- 文件路径和 URL 不翻译
- 保持原有的 Markdown 格式结构
================================================================================
-->

# EE（企业版） Roadmap

- Status: Planning
- Edition: EE（企业版）
- Priority: Future
- Audience: founders, architects, product managers, enterprise buyers, backend developers, frontend developers, agent SDK developers, platform engineers, AI coding agents

This document 定义 the roadmap for **Opstage（运维舞台） EE（企业版） / Enterprise 版本**.

EE（企业版） is the future private commercial edition of the `xtrape-capsule` product family. It should provide enterprise-grade deployment, identity, security, audit, observability, Agent（代理） expansion, and commercial support for customers who need private deployment.

EE（企业版） is not a CE（社区版） v0.1 implementation requirement.

---

## 1. Purpose

The purpose of the EE（企业版） roadmap is to define:

- when EE（企业版） should start;
- what EE（企业版） should add beyond CE（社区版）;
- what EE（企业版） should not take away from CE（社区版）;
- which enterprise capabilities are likely needed;
- how EE（企业版） should be packaged commercially;
- how EE（企业版） should preserve CE（社区版） compatibility;
- how to avoid building enterprise complexity too early.

The key rule is:

> EE（企业版） should extend a proven CE（社区版） governance kernel with enterprise deployment, identity, security, audit, integrations, scale, and support.

---

## 2. EE（企业版） Product Positioning

EE（企业版） is:

> A private enterprise commercial edition of Opstage（运维舞台） for customers that need stronger governance inside their own environment.

EE（企业版） should be suitable for:

- private deployment;
- enterprise internal platforms;
- regulated or security-sensitive environments;
- larger Agent（代理） and Capsule Service（胶囊服务） fleets;
- stronger identity and permission controls;
- audit retention and export;
- enterprise observability integrations;
- enterprise secret provider integration;
- commercial support and upgrade guidance.

EE（企业版） should not be a replacement for CE（社区版）. It should be a stronger enterprise extension of the same model.

---

## 3. Relationship with CE（社区版）

CE（社区版） is the foundation.

EE（企业版） should extend CE（社区版）'s core governance kernel:

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

EE（企业版） should add enterprise capabilities around this kernel, not redefine the kernel.

CE（社区版） must remain genuinely useful as open source.

---

## 4. EE（企业版） Start Conditions

EE（企业版） should not start too early.

Recommended start conditions:

- CE（社区版） v0.1 proves the full governance loop;
- CE（社区版） has real users, demos, or internal adoption;
- Node Agent（代理） SDK is usable;
- Backend Agent（代理） API is reasonably stable;
- Command and Action model is validated;
- at least one real private-deployment need is identified;
- commercial support needs become visible;
- enterprise buyers request features not suitable for CE（社区版） v0.1.

Before these conditions, engineering should remain focused on CE（社区版）.

---

## 5. EE（企业版） Non-Goals During CE（社区版） v0.1

During CE（社区版） v0.1, do not implement:

```text
license enforcement
commercial entitlement engine
enterprise RBAC
SSO / OIDC / LDAP / SAML
HA deployment
Kubernetes / Helm requirement
PostgreSQL/MySQL requirement
advanced audit export
alert rule engine
SIEM integration
secret provider integration
Sidecar Agent
External Agent
Java/Python/Go SDKs
support bundle tool
private registry distribution
```

These are EE（企业版） roadmap items, not CE（社区版） v0.1 tasks.

---

## 6. EE（企业版） Capability Areas

EE（企业版） may add capabilities in these areas:

```text
Enterprise deployment
Production database
Identity and access control
Audit and compliance
Observability and alerting
Secret management
Agent expansion
Runtime expansion
Backup and restore
High availability
Commercial support
Packaging and distribution
```

Each capability should be added based on customer demand and implementation maturity.

---

## 7. EE（企业版） Phase 0 — CE（社区版） Stabilization Dependency

Before EE（企业版） work starts, CE（社区版） should stabilize:

- core data model;
- Agent（代理） API;
- Admin API;
- Node Agent（代理） SDK;
- Command and Action model;
- AuditEvent model;
- status and freshness semantics;
- Docker quick start;
- security boundary;
- documentation.

EE（企业版） should not compensate for an unstable CE（社区版） kernel by adding more complexity.

---

## 8. EE（企业版） Phase 1 — Private 部署 Foundation

EE（企业版） Phase 1 should focus on production-ready private deployment.

Possible capabilities:

- PostgreSQL official support;
- MySQL official support if customer demand exists;
- external database configuration;
- backup and restore guide;
- migration guide from CE（社区版） SQLite;
- Docker Compose production template;
- deployment hardening guide;
- environment-based configuration;
- structured logs;
- support bundle basic tool;
- versioned release artifacts.

Goal:

> Make Opstage（运维舞台） deployable in a customer-controlled production-like environment.

---

## 9. EE（企业版） Phase 2 — Enterprise Identity and Permissions

EE（企业版） Phase 2 may add enterprise identity and permission controls.

Possible capabilities:

- RBAC;
- role management;
- permission model;
- OIDC login;
- LDAP integration;
- SAML integration if required;
- user groups;
- workspace-level permissions;
- action-level permissions;
- high-risk action confirmation;
- permission change audit.

Recommended first step:

```text
OIDC + simple RBAC
```

Avoid implementing every identity system at once.

---

## 10. EE（企业版） Phase 3 — Audit and Compliance

EE（企业版） Phase 3 may add stronger audit and compliance-oriented capabilities.

Possible capabilities:

- audit retention policy;
- audit export;
- CSV/JSON/NDJSON export;
- audit filtering and search;
- permission change audit;
- high-risk action audit reason;
- Agent（代理） token revocation audit;
- support access audit;
- compliance-oriented reports;
- data export workflow;
- data deletion support;
- immutable audit storage planning.

Goal:

> Make Opstage（运维舞台） suitable for enterprise traceability and security review.

---

## 11. EE（企业版） Phase 4 — Observability and Alerting

EE（企业版） Phase 4 may add operational observability at scale.

Possible capabilities:

- health history;
- Agent（代理） uptime history;
- command failure history;
- alert rule engine;
- notification channels;
- webhook alerts;
- email alerts;
- Slack/Teams/Telegram integration;
- Prometheus metrics endpoint;
- Grafana dashboard templates;
- OpenTelemetry integration;
- external log/metric/trace links.

Recommended first step:

```text
health history + alert rules for Agent offline and service DOWN
```

Do not build a full observability platform before core status and freshness are reliable.

---

## 12. EE（企业版） Phase 5 — Secret Provider Integration

EE（企业版） Phase 5 may add enterprise secret provider integration.

Recommended principle:

```text
Opstage stores secretRef.
Agent or customer runtime resolves raw secret.
```

Possible integrations:

- HashiCorp Vault;
- AWS Secrets Manager;
- Azure Key Vault;
- Google Secret Manager;
- Kubernetes Secret;
- enterprise internal secret service.

Possible capabilities:

- secretRef validation;
- secret provider configuration;
- Agent（代理）-side secret resolution;
- secret access audit;
- secret rotation workflow planning;
- sensitive config policy.

Raw secret storage in Opstage（运维舞台） should not be the default.

---

## 13. EE（企业版） Phase 6 — Agent（代理） Expansion

EE（企业版） may expand Agent（代理） modes after the Embedded Agent（代理） model is proven.

Recommended order:

```text
1. Sidecar Agent
2. External Agent
3. Java Embedded Agent SDK
4. Python Embedded Agent SDK
5. Go SDK or Go-based Agent runtime
6. Kubernetes Agent
```

Actual order should follow customer demand.

### 13.1 Sidecar Agent（代理）

Useful for:

- non-Node.js services;
- process isolation;
- local management endpoint integration;
- container sidecar deployment.

### 13.2 External Agent（代理）

Useful for:

- legacy services;
- account/session managers;
- browser automation runtimes;
- local service fleets;
- explicitly configured targets.

### 13.3 Multi-language SDKs

Useful for:

- Java enterprise services;
- Python AI automation services;
- Go infrastructure services.

---

## 14. EE（企业版） Phase 7 — 高 Availability and Scale

EE（企业版） may add high availability and scale capabilities.

Possible capabilities:

- stateless Backend deployment model;
- external PostgreSQL/MySQL database;
- Redis or queue if needed;
- worker process split;
- scheduler process split;
- horizontal scaling guidance;
- HA deployment guide;
- Kubernetes Helm chart;
- readiness/liveness probes;
- rolling upgrade guide;
- performance testing;
- capacity planning.

Do not add HA before production deployment basics are validated.

---

## 15. EE（企业版） Phase 8 — Commercial Packaging

EE（企业版） commercial packaging may include:

- private distribution channel;
- private Docker images;
- versioned release bundles;
- signed artifacts;
- license contract;
- support entitlement;
- optional offline license file;
- support bundle tool;
- installation guide;
- upgrade guide;
- backup/restore guide;
- security hardening guide;
- commercial support process.

Recommended early approach:

```text
commercial contract + private distribution + support entitlement
```

Avoid heavy runtime license enforcement before real commercial demand exists.

---

## 16. EE（企业版） Packaging Tiers

Future EE（企业版） may use simple tiers.

Candidate tiers:

```text
EE Standard
EE Business
EE Enterprise
```

### 16.1 EE（企业版） Standard

Possible focus:

- private deployment;
- PostgreSQL/MySQL support;
- OIDC;
- basic RBAC;
- audit export;
- standard support.

### 16.2 EE（企业版） Business

Possible focus:

- larger Agent（代理）/service capacity;
- alert rules;
- observability integrations;
- secret provider integration;
- Sidecar Agent（代理）;
- priority support.

### 16.3 EE（企业版） Enterprise

Possible focus:

- HA deployment;
- SAML/LDAP/SCIM if needed;
- SIEM integration;
- air-gapped package;
- custom SLA;
- professional services.

Tiers should remain simple and understandable.

---

## 17. EE（企业版） Commercial Boundary

EE（企业版） should sell enterprise value.

Good EE（企业版） boundaries:

```text
production database
enterprise identity
RBAC
advanced audit
audit export
alerting
observability integrations
secret provider integrations
Agent expansion
HA deployment
support and SLA
```

Bad EE（企业版） boundaries:

```text
CE cannot register Agents
CE cannot run predefined actions
CE cannot view basic audit logs
CE cannot persist data
CE SDK is intentionally incomplete
```

CE（社区版） trust matters for future EE（企业版） adoption.

---

## 18. CE（社区版） to EE（企业版） Upgrade Path

EE（企业版） should provide a CE（社区版）-to-EE（企业版） upgrade path.

Possible steps:

```text
1. Backup CE SQLite data.
2. Export or migrate CE data.
3. Provision PostgreSQL/MySQL.
4. Deploy EE Backend and UI.
5. Run migration tool.
6. Configure identity and permissions.
7. Reuse or rotate Agent tokens.
8. Validate Agents and Capsule Services.
9. Validate Commands and AuditEvents.
10. Enable EE features gradually.
```

Early EE（企业版） may support a documented manual migration before automated tooling.

---

## 19. EE（企业版） 部署 Models

Possible EE（企业版） deployment models:

```text
Docker Compose private deployment
Kubernetes deployment
Helm chart
VM-based deployment
air-gapped deployment
private appliance-like bundle
```

Recommended first EE（企业版） deployment model:

```text
Docker Compose + external database
```

Kubernetes and air-gapped deployment should come later.

---

## 20. EE（企业版） 文档 Requirements

EE（企业版） documentation should include:

- installation guide;
- production deployment guide;
- configuration reference;
- database setup guide;
- upgrade guide;
- backup and restore guide;
- security hardening guide;
- RBAC guide;
- SSO guide;
- audit and compliance guide;
- observability integration guide;
- secret provider integration guide;
- Agent（代理） deployment guide;
- troubleshooting guide;
- support bundle guide.

文档 is part of the EE（企业版） product value.

---

## 21. EE（企业版） Support Model

EE（企业版） support may include:

- standard support;
- priority support;
- enterprise support;
- named support contact;
- private support channel;
- upgrade assistance;
- security review assistance;
- incident support;
- professional services.

Support should be tied to clearly supported deployment patterns.

Unsupported custom deployments should be documented carefully.

---

## 22. EE（企业版） Risks

### 22.1 Starting EE（企业版） too early

Risk:

- CE（社区版） remains unfinished.

Mitigation:

- require CE（社区版） kernel validation before EE（企业版） implementation.

### 22.2 Overbuilding enterprise features

Risk:

- engineering effort goes into unused features.

Mitigation:

- add EE（企业版） features based on real customer demand.

### 22.3 Damaging CE（社区版） trust

Risk:

- CE（社区版） users feel the project is artificially restricted.

Mitigation:

- keep CE（社区版） useful and honest.

### 22.4 Support burden

Risk:

- private deployment support becomes expensive.

Mitigation:

- define supported deployment patterns and provide strong docs.

### 22.5 安全 promises ahead of implementation

Risk:

- enterprise claims exceed actual controls.

Mitigation:

- document implemented features accurately.

---

## 23. EE（企业版） Roadmap Guardrails

Guardrails:

1. Do not start EE（企业版） before CE（社区版） kernel works.
2. Do not redefine CE（社区版） concepts in EE（企业版）.
3. Do not make CE（社区版） a broken demo.
4. Do not implement all enterprise features at once.
5. Do not add heavy license enforcement before demand.
6. Do not store raw secrets by default.
7. Do not add arbitrary shell execution as an enterprise shortcut.
8. Do not claim compliance before controls exist.
9. Do not support unlimited deployment patterns without capacity.
10. Do not let EE（企业版） planning expand CE（社区版） v0.1 scope.

---

## 24. Decision Checkpoints

Before starting EE（企业版）, ask:

- Is CE（社区版） v0.1 working end to end?
- Is the Node Agent（代理） SDK usable?
- Is the Agent（代理） API stable enough?
- Are there real private deployment users?
- Which enterprise feature has the strongest demand?
- Which deployment model is needed first?
- What support scope can be handled?
- Which database should be officially supported first?
- Is CE（社区版）-to-EE（企业版） migration necessary for early customers?

Before adding each EE（企业版） feature, ask:

- Is this requested by real customers?
- Does it preserve the CE（社区版） kernel?
- Does it require new security documentation?
- Does it increase support burden?
- Can it be delivered incrementally?

---

## 25. EE（企业版） Roadmap Summary

Recommended EE（企业版） roadmap summary:

```text
EE Phase 0
  Wait for CE kernel stabilization.

EE Phase 1
  Private deployment foundation with production database support.

EE Phase 2
  Enterprise identity and RBAC.

EE Phase 3
  Audit retention, export, and compliance-oriented features.

EE Phase 4
  Observability and alerting integrations.

EE Phase 5
  Secret provider integration.

EE Phase 6
  Agent and runtime expansion.

EE Phase 7
  High availability and scale.

EE Phase 8
  Commercial packaging and support maturity.
```

The exact order should follow customer demand, but CE（社区版） kernel stability comes first.

---

## 26. Acceptance Criteria

This EE（企业版） roadmap is acceptable when:

- EE（企业版） is clearly future, not CE（社区版） v0.1;
- EE（企业版） extends the CE（社区版） governance kernel;
- EE（企业版） capability areas are clear;
- EE（企业版） start conditions are clear;
- private deployment foundation is prioritized;
- identity, audit, observability, secrets, Agent（代理） expansion, and HA are sequenced;
- commercial packaging is described without overengineering early license systems;
- CE（社区版） remains genuinely useful;
- EE（企业版） guardrails prevent scope creep and trust damage.

---

## 27. Summary

EE（企业版） should become the private enterprise commercial edition after the CE（社区版） kernel is proven.

It should focus on enterprise deployment, identity, audit, observability, secrets, Agent（代理） expansion, scale, and support while preserving the same Capsule governance model.

The most important EE（企业版） roadmap rule is:

> Start EE（企业版） only after CE（社区版） proves the kernel, then sell enterprise strength without weakening the open-source foundation.
