<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 12-ce-extension-points.md
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


# CE（社区版） Extension Points for EE（企业版） and Cloud（云版）

- Status: 实现 Target
- Edition: CE（社区版）
- Priority: Current
- Audience: architects, backend developers, frontend developers, agent SDK developers, product designers, AI coding agents

This document 定义 the extension points that **Opstage（运维舞台） CE（社区版） v0.1** should preserve for future **EE（企业版）** and **Cloud（云版）** editions.

CE（社区版） should be lightweight and focused, but it must not be designed as a dead end. The first implementation should leave clean expansion paths for enterprise private deployment and hosted SaaS without forcing their complexity into CE（社区版） v0.1.

---

## 1. Purpose

The purpose of this document is to define:

- which future capabilities CE（社区版） should reserve space for;
- which abstractions should be designed carefully from the beginning;
- which fields should be present but lightweight;
- which future concepts should not be implemented in CE（社区版） v0.1;
- how to avoid polluting CE（社区版） with EE（企业版）/Cloud（云版） complexity;
- how to keep CE（社区版） compatible with future productization.

The main principle is:

> CE（社区版） should be small but not short-sighted.

---

## 2. Extension Philosophy

CE（社区版） v0.1 should implement the minimum complete governance loop:

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

Future editions may extend this loop, but CE（社区版） should not implement those future features prematurely.

Good extension strategy:

```text
Design stable concepts now.
Implement only CE-required behavior now.
Add EE/Cloud behavior later without breaking CE contracts.
```

Bad extension strategy:

```text
Implement tenants, billing, RBAC, cluster, logs, metrics, and SSO in CE v0.1 before the core loop is stable.
```

---

## 3. 版本 Relationship

### 3.1 CE（社区版）

CE（社区版） is the open-source, self-hosted, single-node-friendly edition.

CE（社区版） focuses on:

- SQLite default;
- local admin login;
- Node.js embedded Agent（代理） SDK;
- basic health visibility;
- config visibility;
- predefined actions;
- command polling;
- basic audit;
- simple Docker deployment.

### 3.2 EE（企业版）

EE（企业版） is the future enterprise private deployment edition.

EE（企业版） may focus on:

- MySQL/PostgreSQL official support;
- HA deployment;
- cluster mode;
- enterprise identity;
- RBAC;
- SSO/OIDC/LDAP;
- advanced audit retention;
- centralized logs;
- metrics dashboards;
- alert rules;
- secret vault integration;
- advanced Agent（代理） modes;
- enterprise support.

### 3.3 Cloud（云版）

Cloud（云版） is the future hosted SaaS edition.

Cloud（云版） may focus on:

- hosted Opstage（运维舞台） Backend;
- multi-tenant workspaces;
- organizations and teams;
- subscription billing;
- managed Agent（代理） gateway;
- managed alerting;
- managed audit retention;
- usage dashboards;
- collaboration;
- commercial SLA.

---

## 4. Core Extension Rules

### 4.1 Keep shared contracts stable

共享 concepts should be stable across CE（社区版）, EE（企业版）, and Cloud（云版）:

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
```

### 4.2 Add optional fields instead of changing meanings

Future editions should add optional fields rather than changing existing field semantics.

Good:

```json
{
  "code": "demo-capsule-service",
  "tenantId": "ten_001"
}
```

Bad:

```json
{
  "code": "tenant/service/code"
}
```

if it changes the meaning of `code`.

### 4.3 Use lightweight placeholders carefully

CE（社区版） may include fields such as:

```text
workspaceId
metadataJson
agentMode
runtime
edition
```

But CE（社区版） should not implement full tenant, billing, or cluster systems.

### 4.4 Prefer interfaces over hardcoded future assumptions

设计 APIs and database models so future implementations can be swapped.

Examples:

- database provider;
- command delivery channel;
- token store;
- Agent（代理） mode;
- authentication provider;
- secret reference resolver.

### 4.5 Do not expose unfinished future features in CE（社区版） UI

CE（社区版） UI should not show disabled EE（企业版）/Cloud（云版） features as clutter.

Good:

```text
Keep CE UI focused.
Document future roadmap separately.
```

Bad:

```text
Show SSO, RBAC, Billing, Metrics, Logs, Cluster tabs as disabled UI items.
```

---

## 5. Workspace Extension Point

### 5.1 CE（社区版） behavior

CE（社区版） v0.1 should create one default Workspace.

Required:

```text
Workspace table
workspaceId on core records where practical
Default Workspace bootstrap
No Workspace management UI
```

### 5.2 Future EE（企业版）/Cloud（云版） behavior

Future editions may add:

- multiple Workspaces;
- Workspace switcher;
- Workspace-level permissions;
- Workspace settings;
- Workspace quotas;
- Workspace audit boundaries.

### 5.3 设计 rule

Do not hardcode global-only assumptions.

Core records should be able to belong to a Workspace:

```text
Agent
CapsuleService
Command
AuditEvent
ConfigItem
ActionDefinition
HealthReport
```

CE（社区版） may always use `wks_default`.

---

## 6. Database Extension Point

### 6.1 CE（社区版） behavior

CE（社区版） v0.1 uses:

```text
SQLite
```

### 6.2 Future EE（企业版）/Cloud（云版） behavior

Future editions may use:

```text
MySQL
PostgreSQL
Managed PostgreSQL
```

### 6.3 设计 rule

Use Prisma or an equivalent abstraction so the schema can evolve.

Avoid:

- SQLite-only SQL assumptions;
- loose typing assumptions;
- non-portable datetime formats;
- raw SQL unless necessary.

Prefer:

- portable schema;
- string IDs;
- explicit status values;
- JSON stored as text where needed;
- migrations.

---

## 7. Agent（代理） Mode Extension Point

### 7.1 CE（社区版） behavior

CE（社区版） v0.1 implements only:

```text
embedded Node.js Agent SDK
```

### 7.2 Future behavior

Future editions may support:

```text
embedded Agent
sidecar Agent
external Agent
host Agent
Kubernetes Agent
```

### 7.3 设计 rule

Keep `agentMode` in Manifest and Agent（代理） records.

Allowed values:

```text
embedded
sidecar
external
```

CE（社区版） should implement only `embedded`, but it should not hardcode the entire model as embedded-only.

### 7.4 Future sidecar model

A sidecar Agent（代理） may run as a separate process near a Capsule Service（胶囊服务） and communicate through:

```text
/_capsule management endpoint
local IPC
filesystem configuration
```

CE（社区版） should not implement this in v0.1, but the management contract should remain compatible.

### 7.5 Future external Agent（代理） model

An external Agent（代理） may manage services through configured targets:

```text
process directory
config files
HTTP management endpoint
logs directory
runtime scripts
```

This is future work.

---

## 8. Runtime Extension Point

### 8.1 CE（社区版） behavior

CE（社区版） v0.1 支持:

```text
nodejs
```

### 8.2 Future behavior

Future runtimes may include:

```text
java
python
go
shell
other
```

### 8.3 设计 rule

Keep `runtime` as a field on:

```text
Agent
CapsuleService
Manifest
```

Do not design core contracts as Node.js-only.

Node.js is the first implementation, not the permanent model boundary.

---

## 9. Command Delivery Extension Point

### 9.1 CE（社区版） behavior

CE（社区版） v0.1 uses:

```text
HTTP polling
```

### 9.2 Future behavior

Future editions may support:

```text
WebSocket
Server-Sent Events
gRPC streaming
message queue
long polling
Agent gateway
```

### 9.3 设计 rule

Command model should be independent from delivery mechanism.

The following should remain stable:

```text
Command
CommandResult
CommandStatus
agentId
serviceId
commandType
actionName
payload
result
```

Polling is only a transport strategy.

Do not embed polling-specific assumptions into Command semantics.

---

## 10. 认证 Extension Point

### 10.1 CE（社区版） behavior

CE（社区版） v0.1 uses:

```text
local admin login
```

### 10.2 Future EE（企业版） behavior

EE（企业版） may support:

```text
RBAC
SSO
OIDC
LDAP
SAML
MFA
service accounts
API clients
```

### 10.3 Future Cloud（云版） behavior

Cloud（云版） may support:

```text
organizations
teams
invites
billing users
workspace roles
OAuth login
```

### 10.4 设计 rule

CE（社区版） should keep User model simple but avoid blocking future identity expansion.

Recommended CE（社区版） fields:

```text
id
workspaceId
username
passwordHash
displayName
role
status
```

Reserved concepts should be documented but not implemented as full systems.

---

## 11. 授权 Extension Point

### 11.1 CE（社区版） behavior

CE（社区版） v0.1 may support only:

```text
owner
```

or a simple local admin role.

### 11.2 Future behavior

Future editions may support:

- RBAC;
- action-level permissions;
- service-level permissions;
- Agent（代理） permission scopes;
- approval policies;
- environment-level controls;
- workspace-level roles.

### 11.3 设计 rule

Do not implement a policy engine in CE（社区版） v0.1.

However, keep enough fields for future expansion:

```text
createdBy
actorType
actorId
workspaceId
resourceType
resourceId
```

AuditEvent should already capture actors and resources.

---

## 12. Config Management Extension Point

### 12.1 CE（社区版） behavior

CE（社区版） v0.1 支持:

```text
config visibility only
```

### 12.2 Future behavior

Future editions may support:

- config editing;
- config publishing;
- approval;
- versioning;
- rollback;
- environment promotion;
- config drift detection;
- config reload orchestration.

### 12.3 设计 rule

ConfigItem should include fields that allow future management:

```text
editable
sensitive
source
validation
metadata
```

But CE（社区版） should not implement config publishing workflow.

Future config changes should be modeled as Commands or workflows, not direct uncontrolled writes.

---

## 13. Secret Management Extension Point

### 13.1 CE（社区版） behavior

CE（社区版） v0.1 recognizes:

```text
secretRef
```

but does not resolve or manage secrets.

### 13.2 Future behavior

Future editions may support:

- Opstage（运维舞台）-managed secret store;
- Agent（代理）-local secret store;
- Vault integration;
- cloud secret managers;
- secret rotation;
- secret access audit.

### 13.3 设计 rule

Never require CE（社区版） to store raw secrets.

Use references:

```text
agent-local://agent-001/secrets/chatgpt/account-001
vault://secret/path
opstage-secret://workspace/key
```

CE（社区版） should display references safely and preserve them in metadata.

---

## 14. Observability Extension Point

### 14.1 CE（社区版） behavior

CE（社区版） v0.1 支持:

```text
health visibility
basic application logs
basic command result visibility
```

### 14.2 Future behavior

Future editions may support:

- centralized logs;
- metrics collection;
- dashboards;
- alert rules;
- traces;
- event streams;
- integrations with Prometheus, Grafana, Loki, Elasticsearch, OpenTelemetry.

### 14.3 设计 rule

Do not turn CE（社区版） v0.1 into an observability platform.

Keep HealthReport small and clear.

Do not store large logs in:

```text
HealthReport.detailsJson
CommandResult.resultJson
AuditEvent.resultJson
```

---

## 15. Audit Extension Point

### 15.1 CE（社区版） behavior

CE（社区版） v0.1 支持 basic AuditEvents.

### 15.2 Future behavior

Future editions may support:

- retention policies;
- immutable audit storage;
- audit export;
- compliance reports;
- SIEM integration;
- audit signing;
- advanced search;
- audit read tracking.

### 15.3 设计 rule

AuditEvent shape should already include:

```text
workspaceId
actorType
actorId
action
resourceType
resourceId
result
requestJson
resultJson
createdAt
```

This gives future editions enough structure without implementing compliance systems in CE（社区版）.

---

## 16. 部署 Extension Point

### 16.1 CE（社区版） behavior

CE（社区版） v0.1 deployment:

```text
single container
single process
SQLite volume
single exposed port
```

### 16.2 Future EE（企业版） behavior

EE（企业版） may support:

- separate Backend and UI deployment;
- external database;
- worker process;
- scheduler process;
- HA mode;
- Docker Compose;
- Helm chart;
- private registry packages.

### 16.3 Future Cloud（云版） behavior

Cloud（云版） may support:

- hosted multi-tenant backend;
- Agent（代理） gateway;
- managed database;
- managed logs;
- managed metrics;
- managed backups;
- scalable workers.

### 16.4 设计 rule

Do not make CE（社区版） require cluster infrastructure.

But structure code so Backend, UI, and Agent（代理） SDK can be split later.

---

## 17. API Extension Point

### 17.1 CE（社区版） behavior

CE（社区版） v0.1 exposes REST JSON APIs.

### 17.2 Future behavior

Future editions may add:

- WebSocket APIs;
- streaming APIs;
- OpenAPI specification;
- SDK clients;
- public Cloud（云版） APIs;
- webhook APIs;
- marketplace APIs.

### 17.3 设计 rule

Keep CE（社区版） REST API stable and explicit.

Do not overload endpoints with future optional behaviors that make CE（社区版） confusing.

Use additive endpoints later.

---

## 18. UI Extension Point

### 18.1 CE（社区版） behavior

CE（社区版） UI 包括:

- Dashboard;
- Agents;
- Capsule Services;
- Commands;
- Audit Logs;
- System Settings.

### 18.2 Future behavior

Future UI may add:

- RBAC management;
- SSO settings;
- Workspace switcher;
- metrics dashboards;
- log search;
- alert rules;
- secret management;
- config publishing workflow;
- team collaboration;
- billing for Cloud（云版）.

### 18.3 设计 rule

Do not show disabled future tabs in CE（社区版） v0.1.

Keep CE（社区版） UI focused on implemented functionality.

Future UI should expand navigation without changing the core CE（社区版） pages drastically.

---

## 19. Plugin and Marketplace Extension Point

### 19.1 CE（社区版） behavior

CE（社区版） v0.1 does not need a plugin system.

### 19.2 Future behavior

Future editions may support:

- Capsule Service（胶囊服务） templates;
- Agent（代理） extensions;
- action packs;
- connector packs;
- marketplace listings;
- verified integrations.

### 19.3 设计 rule

Do not implement plugin infrastructure before the core product is stable.

However, keep specs and Agent（代理） SDK clean enough that third-party Capsule Services can be created manually.

---

## 20. Commercial Extension Point

### 20.1 CE（社区版） behavior

CE（社区版） should not include billing or license enforcement.

### 20.2 Future behavior

EE（企业版）/Cloud（云版） may include:

- license management;
- subscription billing;
- usage metering;
- commercial support metadata;
- edition flags.

### 20.3 设计 rule

Do not make CE（社区版） feel like a disabled commercial trial.

Commercial boundaries should be based on:

- scale;
- enterprise governance;
- managed service value;
- support;
- compliance;
- advanced integrations.

not on disabling the core CE（社区版） governance loop.

---

## 21. Data Model Extension Summary

CE（社区版） should include these future-friendly fields where practical:

```text
workspaceId
metadataJson
manifestJson
runtime
agentMode
createdBy
actorType
actorId
resourceType
resourceId
status
```

CE（社区版） should not implement these as first-class models in v0.1:

```text
Tenant
Organization
BillingAccount
Subscription
ClusterNode
MetricSeries
LogStream
TraceSpan
AlertRule
SecretStore
ApprovalWorkflow
ConfigVersion
RolePermissionPolicy
```

---

## 22. Anti-Patterns

Avoid these patterns.

### 22.1 Implementing future complexity too early

Do not build EE（企业版）/Cloud（云版） infrastructure before CE（社区版） MVP works.

### 22.2 Hardcoding CE（社区版） as permanently single-user

CE（社区版） may have one default Workspace and simple admin, but the model should not make future multi-workspace impossible.

### 22.3 Hiding commercial features in CE（社区版） UI

Do not clutter CE（社区版） UI with disabled commercial tabs.

### 22.4 Changing shared field meanings later

Do not redefine `code`, `status`, `agentMode`, `runtime`, or `workspaceId` later.

### 22.5 Building arbitrary shell execution as an extension point

Shell execution is not a safe extension point for CE（社区版） v0.1.

Future operation models should still use predefined actions, approvals, and audit.

---

## 23. Extension Acceptance Criteria

CE（社区版） extension design is acceptable when:

- CE（社区版） v0.1 remains lightweight;
- CE（社区版） MVP is not blocked by future features;
- shared specs remain useful for EE（企业版） and Cloud（云版）;
- Workspace exists but multi-workspace is not implemented;
- SQLite works but MySQL/PostgreSQL path remains open;
- embedded Agent（代理） works but sidecar/external path remains open;
- polling works but streaming path remains open;
- config visibility works but config publishing path remains open;
- secretRef works but secret vault is not required;
- audit works but compliance suite is not required;
- UI is focused on CE（社区版） features;
- no arbitrary shell extension is introduced.

---

## 24. Summary

CE（社区版） should be the stable open-source kernel of Opstage（运维舞台）.

It should implement the smallest complete governance loop while preserving clean paths for EE（企业版） and Cloud（云版）.

The most important extension rule is:

> Reserve space for the future, but do not make the future a dependency of CE（社区版） v0.1.
