# EE Planned Capabilities

- Status: Planning
- Edition: EE
- Priority: Future
- Audience: founders, product designers, architects, enterprise engineers, backend developers, DevOps engineers, security reviewers, AI coding agents

This document defines the planned capabilities for **Opstage EE / Enterprise Edition**.

Opstage EE is the future private commercial edition of the `xtrape-capsule` product family. It is not a CE v0.1 implementation requirement.

---

## 1. Purpose

The purpose of this document is to define:

- which capabilities Opstage EE may provide;
- how EE capabilities extend the CE governance kernel;
- which capabilities may become EE MVP candidates;
- which capabilities should remain long-term planning items;
- which EE capabilities must not be pulled into CE v0.1;
- how EE should preserve compatibility with CE and Cloud.

The core rule is:

> EE extends the CE governance kernel for private enterprise deployment, but CE v0.1 must remain lightweight and self-hosted.

---

## 2. Capability Layers

Opstage EE capabilities can be grouped into layers:

```text
Core Governance Layer
Enterprise Identity and Access Layer
Enterprise Deployment Layer
Enterprise Database Layer
Agent Expansion Layer
Command and Operation Layer
Configuration Management Layer
Observability and Alerting Layer
Audit and Compliance Layer
Secret Integration Layer
Commercial and Support Layer
```

EE does not need to implement all layers in its first release.

---

## 3. Core Governance Layer

The Core Governance Layer is inherited from CE.

It includes:

- Agent registration;
- Agent token authentication;
- Capsule Service report;
- manifest storage;
- heartbeat;
- health visibility;
- config visibility;
- predefined actions;
- Commands;
- CommandResults;
- AuditEvents;
- status and freshness calculation.

These capabilities should remain compatible with CE contracts.

Shared concepts should remain stable:

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

EE may strengthen implementation, but should not replace the CE kernel with an incompatible model.

---

## 4. Enterprise Identity and Access Layer

EE should support stronger identity and authorization than CE.

### 4.1 RBAC

Possible capabilities:

- role-based access control;
- workspace-level roles;
- service-level permissions;
- action-level permissions;
- audit-level permissions;
- billing/license admin role if needed;
- permission change audit.

Possible roles:

```text
Owner
Admin
Operator
Viewer
Auditor
SecurityAdmin
```

Possible permissions:

```text
workspace.manage
agent.register
agent.revoke
service.view
service.action.execute
command.view
audit.view
settings.manage
```

### 4.2 Enterprise login

Possible integrations:

```text
OIDC
OAuth2
LDAP
SAML
```

### 4.3 Service accounts and API keys

Possible capabilities:

- service accounts;
- scoped API keys;
- token hashing;
- key expiration;
- key revocation;
- API access audit.

### 4.4 Approval workflows

Future EE may support approval workflows for high-risk actions.

Possible examples:

- two-person approval;
- reason required;
- approval timeout;
- approval audit trail;
- action-level approval policy.

### 4.5 CE relationship

CE v0.1 may use only local admin authentication.

CE should not implement enterprise RBAC or SSO.

---

## 5. Enterprise Deployment Layer

EE should support stronger private deployment models.

### 5.1 Deployment models

Possible deployment modes:

```text
Docker Compose
Kubernetes / Helm
VM-based deployment
Private cloud deployment
Air-gapped or restricted network deployment
```

### 5.2 Deployment components

Possible EE components:

```text
Opstage UI
Opstage Backend API
Worker
Scheduler
Database
Cache
Queue
Object storage
Log integration
Metric integration
Secret provider integration
```

### 5.3 Operational tooling

Possible capabilities:

- installer scripts;
- Helm charts;
- environment validation;
- health checks;
- backup and restore tooling;
- upgrade scripts;
- migration tooling;
- deployment diagnostics.

### 5.4 CE relationship

CE v0.1 should remain single-container and SQLite-first.

CE should not require Kubernetes, Redis, queues, or external databases.

---

## 6. Enterprise Database Layer

CE v0.1 uses SQLite by default.

EE should support production databases.

### 6.1 Candidate databases

Primary candidates:

```text
PostgreSQL
MySQL
```

Possible future candidates:

```text
Oracle
SQL Server
```

only if enterprise demand justifies them.

### 6.2 Database capabilities

EE may provide:

- official PostgreSQL support;
- official MySQL support;
- migration support;
- connection pooling;
- backup and restore guidance;
- performance tuning guidance;
- retention and cleanup jobs;
- database health checks;
- HA database deployment guidance.

### 6.3 CE relationship

CE should keep schema portable and avoid SQLite-only assumptions where practical.

CE should not implement full enterprise database operations.

---

## 7. Agent Expansion Layer

CE v0.1 implements Node.js embedded Agent SDK.

EE may expand Agent capabilities.

### 7.1 Agent modes

Possible Agent modes:

```text
embedded
sidecar
external
host
kubernetes
```

### 7.2 Runtime SDKs

Possible Agent SDKs:

```text
Node.js
Java
Python
Go
```

### 7.3 Sidecar Agent

A sidecar Agent may manage a Capsule Service through:

- local HTTP management endpoint;
- local IPC;
- configuration files;
- process metadata;
- mounted directories.

### 7.4 External Agent

An external Agent may manage services through configured targets:

- process directory;
- config files;
- HTTP management endpoint;
- logs directory;
- runtime scripts;
- service supervisor integration.

### 7.5 Agent diagnostics

EE may provide:

- Agent version compatibility;
- Agent connection diagnostics;
- Agent upgrade guidance;
- Agent capability reporting;
- protocol version warnings;
- Agent runtime health.

### 7.6 CE relationship

CE v0.1 should only implement Node.js embedded Agent SDK.

CE should reserve `agentMode` and `runtime` fields.

---

## 8. Command and Operation Layer

CE v0.1 supports predefined actions through Command polling.

EE may add stronger operation controls.

### 8.1 Command delivery

Possible delivery modes:

```text
HTTP polling
long polling
WebSocket
gRPC streaming
queue-backed delivery
```

### 8.2 Command lifecycle

Possible capabilities:

- command cancellation;
- command retry policy;
- command scheduling;
- long-running command progress;
- command timeout policy;
- command priority;
- command concurrency limits;
- resource locks;
- batch commands.

### 8.3 Operation safety

Possible capabilities:

- approval workflow;
- action-level permission;
- high-risk action confirmation;
- reason required;
- action cooldown;
- operation window policy;
- audit reason and result enforcement.

### 8.4 CE relationship

CE v0.1 should keep only simple `ACTION` Commands, polling, and CommandResult reporting.

CE must not provide arbitrary shell execution.

---

## 9. Configuration Management Layer

CE v0.1 supports config visibility only.

EE may add configuration management capabilities.

### 9.1 Planned capabilities

Possible capabilities:

- config editing;
- config publishing;
- config approval;
- config versioning;
- config rollback;
- environment promotion;
- config diff;
- config drift detection;
- config reload action;
- config source integration;
- read-only view of external config sources.

### 9.2 Design principle

EE should not become merely another Nacos/Apollo clone.

Configuration management should be tied to Capsule governance:

```text
Config metadata
    ↓
Approved change
    ↓
Command or workflow
    ↓
Agent applies or reloads
    ↓
Audit records result
```

### 9.3 CE relationship

CE should preserve ConfigItem fields such as:

```text
editable
sensitive
source
validation
metadata
```

but CE v0.1 should not implement config publishing workflow.

---

## 10. Observability and Alerting Layer

EE may integrate with enterprise observability systems.

### 10.1 Health history

Possible capabilities:

- health timeline;
- uptime history;
- service stale duration;
- Agent online/offline history;
- dependency health history.

### 10.2 Metrics

Possible capabilities:

- command success rate;
- command failure rate;
- action execution duration;
- Agent heartbeat statistics;
- service count trend;
- Agent count trend.

### 10.3 Logs

Possible integrations:

```text
Loki
Elasticsearch
OpenSearch
enterprise log platform
```

### 10.4 Metrics and dashboards

Possible integrations:

```text
Prometheus
Grafana
OpenTelemetry
```

### 10.5 Alerts

Possible alert rules:

- Agent offline;
- service stale;
- service unhealthy;
- command failed;
- command timeout;
- registration token used;
- abnormal command failure rate.

Possible notification channels:

```text
email
webhook
Slack
Telegram
enterprise incident system
```

### 10.6 CE relationship

CE v0.1 should only provide basic health visibility and simple application logs.

CE should not become a full observability platform.

---

## 11. Audit and Compliance Layer

EE may support stronger audit and compliance capabilities.

### 11.1 Audit retention

Possible capabilities:

- configurable retention;
- retention by workspace;
- retention by event type;
- retention by compliance policy;
- cleanup jobs;
- archive jobs.

### 11.2 Audit search and export

Possible capabilities:

- audit search;
- actor filter;
- resource filter;
- action filter;
- result filter;
- time range filter;
- CSV export;
- JSON/NDJSON export;
- compliance report export.

### 11.3 Immutable audit

Future EE may support:

- append-only audit storage;
- signed audit records;
- external audit sink;
- SIEM integration.

### 11.4 Compliance records

Possible audit events:

- permission changes;
- SSO configuration changes;
- Agent revocation;
- high-risk action approval;
- license changes;
- support access.

### 11.5 CE relationship

CE v0.1 only needs basic AuditEvents.

CE should preserve actor/resource fields.

---

## 12. Secret Integration Layer

EE may integrate with enterprise secret providers.

### 12.1 Secret providers

Possible providers:

```text
HashiCorp Vault
AWS Secrets Manager
Azure Key Vault
Google Secret Manager
Kubernetes Secrets
enterprise internal secret service
```

### 12.2 SecretRef model

EE should preserve the `secretRef` boundary.

Examples:

```text
vault://secret/path
aws-secretsmanager://region/account/secret-name
azure-keyvault://vault-name/secret-name
agent-local://agent-001/secrets/chatgpt/account-001
```

### 12.3 Planned capabilities

Possible capabilities:

- secretRef validation;
- secret provider configuration;
- secret access audit;
- secret rotation workflow;
- secret availability check;
- permission-based secret reference usage;
- Agent-side secret resolution guidance.

### 12.4 CE relationship

CE v0.1 should recognize and display `secretRef` safely.

CE should not implement a full secret vault.

---

## 13. Commercial and Support Layer

EE is a commercial private deployment edition.

### 13.1 License and entitlement

Possible capabilities:

- license key;
- offline license file;
- subscription contract;
- feature entitlements;
- license expiration warning;
- support contract metadata.

### 13.2 Enterprise support

Possible support capabilities:

- support bundle export;
- environment diagnostics;
- upgrade report;
- deployment health report;
- private support channel;
- SLA-backed support;
- support access audit if remote support is provided.

### 13.3 Documentation

EE should provide:

- installation guide;
- upgrade guide;
- backup and restore guide;
- SSO setup guide;
- database setup guide;
- security hardening guide;
- Agent deployment guide;
- troubleshooting guide.

### 13.4 CE relationship

CE should not include license enforcement.

CE documentation should remain open-source friendly.

---

## 14. EE MVP Candidate Capabilities

A future EE MVP may include:

- CE-compatible core governance;
- PostgreSQL or MySQL official support;
- Docker Compose private deployment;
- production configuration documentation;
- local RBAC;
- OIDC login;
- audit retention configuration;
- audit export;
- basic alert rules;
- sidecar Agent prototype;
- backup and restore guide;
- upgrade guide;
- commercial license or support entitlement mechanism.

This is a candidate only and should be validated by real enterprise demand.

---

## 15. Long-Term EE Capabilities

Long-term EE may include:

- HA deployment;
- Kubernetes Helm chart;
- full RBAC matrix;
- SAML and SCIM;
- approval workflows;
- Java/Python/Go Agent SDKs;
- external Agent mode;
- Kubernetes Agent;
- advanced audit compliance;
- SIEM integration;
- advanced alert routing;
- full secret provider integrations;
- config publishing workflow;
- enterprise marketplace or integration packs;
- air-gapped deployment support;
- dedicated enterprise appliance.

These should not be implemented before CE and early EE value are validated.

---

## 16. Capabilities Explicitly Not for CE v0.1

The following EE capabilities must not be required by CE v0.1:

```text
RBAC
SSO
OIDC
LDAP
SAML
SCIM
PostgreSQL/MySQL requirement
High availability
Kubernetes
Redis/Queue requirement
Sidecar Agent
External Agent
Java/Python/Go Agent SDKs
Centralized logs
Metrics dashboards
Alert rules
Secret Vault integration
Compliance audit suite
Commercial license enforcement
Enterprise installer
```

CE may reserve compatible extension points, but must not implement these systems in v0.1.

---

## 17. Capability Dependency Rules

EE capabilities should be layered carefully.

### 17.1 Core first

EE must preserve and strengthen the CE core governance loop.

### 17.2 Database before scale

Production database support should come before high availability claims.

### 17.3 Identity before fine-grained authorization

SSO and user model should be stable before deep permission matrix.

### 17.4 Audit before compliance claims

Reliable audit events and retention should come before compliance marketing.

### 17.5 SecretRef before managed secret workflows

Secret reference boundary should be proven before implementing deep secret provider integrations.

### 17.6 Agent contract before new Agent modes

The shared Agent contract should be stable before sidecar/external/multi-language Agents expand.

---

## 18. Risks

### 18.1 Enterprise scope explosion

Risk:

- EE becomes a heavy enterprise platform before the core product is validated.

Mitigation:

- build CE first;
- validate enterprise requirements;
- prioritize identity, database, deployment, audit, and support.

### 18.2 Integration overload

Risk:

- too many integrations are attempted early.

Mitigation:

- start with one or two high-value integrations.

### 18.3 CE trust damage

Risk:

- CE is weakened to force EE upgrades.

Mitigation:

- keep CE useful;
- sell enterprise capabilities, not disabled basics.

### 18.4 Deployment support complexity

Risk:

- private deployment generates many support variants.

Mitigation:

- define supported deployment patterns;
- document unsupported modes clearly.

### 18.5 Compatibility drift

Risk:

- EE diverges from CE and Cloud contracts.

Mitigation:

- keep shared specs stable;
- version breaking changes carefully.

---

## 19. Capability Acceptance Criteria

EE capability planning is acceptable when:

- EE capabilities clearly extend CE instead of replacing it;
- CE v0.1 remains lightweight;
- enterprise identity, database, deployment, audit, and support are prioritized;
- Agent expansion is planned without breaking the CE Agent model;
- command and audit models remain stable;
- secretRef remains the default secret boundary;
- observability is framed as integration, not full replacement;
- commercial value is based on enterprise capability and support, not crippling CE.

---

## 20. Summary

Opstage EE may eventually provide many enterprise capabilities, but its first value should remain clear:

```text
Private enterprise deployment of the Capsule governance kernel.
```

The most important EE capability rule is:

> Build EE as an enterprise-strength extension of CE, not as a heavy platform that loses the Capsule focus.
