---
status: draft
audience: architects
stability: unstable
last_reviewed: 2026-05-05
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 03-domain-model.md
翻译状态 / Translation Status: 已翻译 / Translated
生成时间 / Generated: 2026-05-01 09:28:53
================================================================================
注意 / Notes:
- 技术术语如 Capsule Service、Agent、Opstage 等保留英文或采用中英对照
- 代码块中的内容不翻译
- 文件路径和 URL 不翻译
- 保持原有的 Markdown 格式结构
================================================================================
-->

# xtrape-capsule Domain Model

- Status: Conceptual Guidance
- Edition: 共享
- Priority: 高
- Audience: architects, backend developers, frontend developers, agent SDK developers, AI coding agents

This document 定义 the core domain objects of `xtrape-capsule`.

The domain model is shared by CE（社区版）, EE（企业版）, and Cloud（云版）, but CE（社区版） v0.1 should implement only the minimum subset
required to prove the Capsule Service（胶囊服务） governance loop.

---

## 1. Purpose

The purpose of this document is to define the major concepts and relationships in the `xtrape-capsule` domain.

It should guide:

- backend database model design;
- backend API design;
- UI information architecture;
- Node.js embedded Agent（代理） SDK design;
- future sidecar and external Agent（代理） design;
- CE（社区版） extension points for EE（企业版） and Cloud（云版）.

This document is not a physical database schema. The CE（社区版） database schema should be derived from this model but may simplify it.

---

## 2. Domain 概述

The core domain model can be summarized as:

```text
Workspace
    └── Agent
            └── CapsuleService
                    ├── Manifest
                    ├── HealthReport
                    ├── ConfigItem
                    ├── ActionDefinition
                    ├── Command
                    ├── CommandResult
                    ├── AuditEvent
                    └── RuntimeStatus
```

In CE（社区版） v0.1, there may be only one default Workspace, but the model should still leave room for multiple Workspaces in EE（企业版） and Cloud（云版）.

---

## 3. Core Objects

### 3.1 Workspace

A **Workspace** is a logical boundary for Agents, Capsule Services, users, commands, audit events, and configuration metadata.

In CE（社区版） v0.1:

- only one default Workspace is required;
- Workspace management UI is not required;
- the data model should still allow a `workspaceId` field where reasonable.

In EE（企业版） and Cloud（云版）, Workspace may become:

- an organization boundary;
- a tenant boundary;
- a project boundary;
- a customer environment boundary.

Recommended fields:

```text
id
code
name
status
createdAt
updatedAt
```

CE（社区版） v0.1 may create a built-in Workspace:

```text
code: default
name: Default Workspace
```

---

### 3.2 User

A **User** represents a human operator of Opstage（运维舞台）.

In CE（社区版） v0.1:

- a simple local admin user is enough;
- full RBAC is not required;
- SSO is not required;
- multi-user collaboration is optional and should not block the first milestone.

In EE（企业版） and Cloud（云版）, User may support:

- organization membership;
- roles;
- permissions;
- SSO / OIDC / LDAP;
- audit identity;
- approval workflows.

Recommended CE（社区版） fields:

```text
id
username
passwordHash
displayName
role
status
createdAt
updatedAt
```

Recommended initial roles:

```text
owner
admin
viewer
```

CE（社区版） v0.1 may implement only `owner`.

---

### 3.3 Agent（代理）

An **Agent（代理）** is the governance bridge between Opstage（运维舞台） Backend and one or more Capsule Services.

An Agent（代理） is responsible for:

- registration;
- authentication;
- heartbeat;
- service reporting;
- health reporting;
- command polling or command receiving;
- action execution;
- command result reporting;
- event reporting.

Agent（代理） modes:

```text
embedded
sidecar
external
```

CE（社区版） v0.1 implements only:

```text
embedded
```

Recommended fields:

```text
id
workspaceId
code
name
mode
runtime
version
status
hostname
os
arch
lastHeartbeatAt
registeredAt
disabledAt
createdAt
updatedAt
```

Recommended Agent（代理） statuses:

```text
PENDING
REGISTERED
ONLINE
OFFLINE
DISABLED
REVOKED
ERROR
```

CE（社区版） v0.1 may simplify this to:

```text
PENDING
ONLINE
OFFLINE
DISABLED
REVOKED
```

---

### 3.4 AgentToken

An **AgentToken** is used to authenticate Agent（代理） registration and later Agent（代理） communication.

There are two main token types:

```text
registration
agent
```

#### Registration Token

A registration token is used only for the first registration.

Properties:

- short-lived or one-time use;
- created by Opstage（运维舞台） admin or setup flow;
- exchanged for an Agent（代理） token;
- should be marked as used after successful registration.

#### Agent（代理） Token

An Agent（代理） token is used for ongoing communication after registration.

Properties:

- longer-lived than registration token;
- revocable;
- should be stored hashed in Opstage（运维舞台） database;
- can be rotated in future versions.

Recommended fields:

```text
id
agentId
workspaceId
tokenHash
type
status
expiresAt
createdAt
usedAt
revokedAt
```

Token statuses:

```text
ACTIVE
USED
REVOKED
EXPIRED
```

安全 rule:

> Raw tokens must not be stored in the database. Store only token hashes.

---

### 3.5 CapsuleService

A **CapsuleService** is the main managed service unit.

It represents a lightweight service, worker, connector, automation process, account manager, session manager, or runtime adapter that is governed through an Agent（代理）.

Recommended fields:

```text
id
workspaceId
agentId
code
name
description
version
runtime
agentMode
status
reportedStatus
effectiveStatus
manifestJson
lastReportedAt
createdAt
updatedAt
```

Rules:

- `code` should be stable and unique within a Workspace.
- A Capsule Service（胶囊服务） may be reported by one Agent（代理） in CE（社区版） v0.1.
- Future EE（企业版）/Cloud（云版） may support more advanced ownership, failover, or multiple deployment instances.

Recommended statuses:

```text
UNKNOWN
ONLINE
UNHEALTHY
OFFLINE
STALE
DISABLED
REMOVED
```

`reportedStatus` means the last status reported by the Agent（代理）.

`effectiveStatus` means the current status calculated by Opstage（运维舞台）.

Example:

```json
{
  "reportedStatus": "ONLINE",
  "effectiveStatus": "STALE",
  "reason": "agent offline"
}
```

---

### 3.6 CapsuleInstance

A **CapsuleInstance** represents a concrete running instance of a Capsule Service（胶囊服务）.

CE（社区版） v0.1 does not need to implement CapsuleInstance as a separate table if each Capsule Service（胶囊服务） maps to one running instance.

Future EE（企业版）/Cloud（云版） may need CapsuleInstance for:

- multiple instances of the same service;
- cluster deployment;
- per-instance health;
- per-instance logs;
- load balancing;
- failover;
- environment separation.

Recommended future fields:

```text
id
workspaceId
serviceId
agentId
instanceCode
hostname
runtime
version
status
lastReportedAt
createdAt
updatedAt
```

CE（社区版） v0.1 guidance:

> Do not over-engineer CapsuleInstance in CE（社区版） v0.1. Keep `CapsuleService` as the primary visible object.

---

### 3.7 CapsuleManifest

A **CapsuleManifest** 描述 the identity and management surface of a Capsule Service（胶囊服务）.

The manifest may include:

- service identity;
- runtime;
- agent mode;
- capabilities;
- resources;
- config metadata;
- action metadata;
- health dependencies;
- documentation links.

CE（社区版） v0.1 may store manifest as JSON:

```text
manifestJson
```

Minimum CE（社区版） v0.1 manifest:

```json
{
  "kind": "CapsuleService",
  "code": "demo-capsule-service",
  "name": "Demo Capsule Service",
  "version": "0.1.0",
  "runtime": "nodejs",
  "agentMode": "embedded",
  "capabilities": ["demo.echo"],
  "resources": [],
  "actions": ["echo", "runHealthCheck"]
}
```

Detailed rules belong to:

```text
02-specs/01-capsule-manifest-spec.md
```

---

### 3.8 HealthReport

A **HealthReport** 描述 the health of a Capsule Service（胶囊服务） at a specific time.

Recommended fields:

```text
id
workspaceId
serviceId
agentId
status
detailsJson
checkedAt
createdAt
```

Health statuses:

```text
UP
DOWN
DEGRADED
UNKNOWN
```

CE（社区版） v0.1 should store at least the latest health report for each Capsule Service（胶囊服务）.

It may also store recent history, but long-term health history retention is not required for v0.1.

Example:

```json
{
  "status": "UP",
  "details": {
    "database": "UP",
    "browser": "UP",
    "queue": "DEGRADED"
  },
  "checkedAt": "2026-04-30T10:21:00Z"
}
```

---

### 3.9 ConfigItem

A **ConfigItem** 描述 a manageable configuration item of a Capsule Service（胶囊服务）.

CE（社区版） v0.1 may implement configuration visibility only. Full configuration editing and publishing can be added later.

Recommended fields:

```text
id
workspaceId
serviceId
configKey
label
valueType
currentValue
defaultValue
editable
sensitive
metadataJson
createdAt
updatedAt
```

Recommended value types:

```text
string
number
boolean
select
json
secretRef
```

Rules:

- sensitive values should not be displayed in plain text;
- secret values should be represented by references when possible;
- config metadata should describe validation where possible;
- CE（社区版） v0.1 should avoid complex config publishing workflows.

---

### 3.10 ActionDefinition

An **ActionDefinition** 描述 a predefined operation that can be executed against a Capsule Service（胶囊服务）.

Examples:

```text
runHealthCheck
reloadConfig
refreshSession
clearExpiredSessions
disableAccount
rotateProxy
```

Recommended fields:

```text
id
workspaceId
serviceId
name
label
description
inputSchemaJson
dangerLevel
enabled
createdAt
updatedAt
```

Danger levels:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

CE（社区版） v0.1 should support only predefined actions.

安全 rule:

> CE（社区版） v0.1 should not support arbitrary shell command execution from the UI.

---

### 3.11 Command

A **Command** is an instruction issued by Opstage（运维舞台） Backend to an Agent（代理）.

A Command may ask the Agent（代理） to execute a predefined action on a Capsule Service（胶囊服务）.

Recommended fields:

```text
id
workspaceId
agentId
serviceId
commandType
actionName
payloadJson
status
createdBy
createdAt
expiresAt
dispatchedAt
startedAt
finishedAt
idempotencyKey
```

Command statuses:

```text
PENDING
DISPATCHED
RUNNING
SUCCESS
FAILED
EXPIRED
CANCELLED
```

CE（社区版） v0.1 should use command polling:

```text
Agent -> Backend: fetch pending commands
Agent -> Backend: report command result
```

Future versions may support WebSocket, gRPC streaming, or message queue delivery.

---

### 3.12 CommandResult

A **CommandResult** records the execution result of a Command.

Recommended fields:

```text
id
workspaceId
commandId
agentId
serviceId
status
outputText
errorMessage
resultJson
startedAt
finishedAt
createdAt
```

Rules:

- every completed Command should have a result;
- failed commands should include an error message;
- result payload should be JSON when structured data is available;
- command results should be auditable.

---

### 3.13 AuditEvent

An **AuditEvent** records an important user, system, or Agent（代理） operation.

Recommended fields:

```text
id
workspaceId
actorType
actorId
action
resourceType
resourceId
description
requestJson
resultJson
ip
userAgent
createdAt
```

Actor types:

```text
user
agent
system
```

Examples of auditable actions:

```text
agent.registered
agent.revoked
service.reported
service.action.requested
service.action.completed
command.created
command.completed
config.updated
user.login
```

CE（社区版） v0.1 should implement basic audit logs for:

- user login;
- Agent（代理） registration;
- command creation;
- command result;
- action execution.

---

### 3.14 Capability

A **Capability** represents a named ability provided by a Capsule Service（胶囊服务）.

Examples:

```text
demo.echo
chatgpt.chat
gmail.readOtp
browser.openPage
account.refreshSession
```

CE（社区版） v0.1 may store capabilities as part of `manifestJson` only.

Future EE（企业版）/Cloud（云版） may model Capability explicitly for:

- capability registry;
- capability routing;
- quota management;
- customer-level entitlement;
- billing;
- provider selection.

Recommended future fields:

```text
id
workspaceId
serviceId
code
name
description
status
metadataJson
createdAt
updatedAt
```

---

### 3.15 ResourceDefinition

A **ResourceDefinition** 描述 a type of resource managed by a Capsule Service（胶囊服务）.

Examples:

```text
account
session
job
queue
proxy
connector
agentRun
```

CE（社区版） v0.1 may store resource definitions in manifest JSON only.

Future versions may use ResourceDefinition to generate admin pages dynamically.

Recommended future fields:

```text
id
workspaceId
serviceId
name
label
schemaJson
actionsJson
metadataJson
createdAt
updatedAt
```

---

### 3.16 SecretRef

A **SecretRef** is a reference to a sensitive value, not the sensitive value itself.

Examples:

```text
agent-local://agent-id/secrets/chatgpt/account-001
vault://secret/path
opstage-secret://workspace/key
```

CE（社区版） v0.1 does not need a full secret store.

However, data model and manifest design should avoid spreading raw secrets into normal fields.

Future secret modes:

```text
agent-local
opstage-managed
external-vault
cloud-provider-secret
```

---

### 3.17 Runtime

A **Runtime** 描述 the technology runtime used by a Capsule Service（胶囊服务） or Agent（代理）.

Recommended runtime values:

```text
nodejs
java
python
go
shell
other
```

CE（社区版） v0.1 支持 Node.js Agent（代理） SDK first, but the domain model must not assume Node.js forever.

---

### 3.18 版本

An **版本** 描述 the product line where a feature belongs.

版本 values:

```text
CE
EE
Cloud
```

Rules:

- CE（社区版） is the current implementation target;
- EE（企业版） and Cloud（云版） are planning targets;
- CE（社区版） should reserve extension points but not implement heavy EE（企业版）/Cloud（云版） features in v0.1.

---

## 4. Core Relationships

### 4.1 Workspace to Agent（代理）

```text
Workspace 1 --- n Agent
```

A Workspace may contain multiple Agents.

CE（社区版） v0.1 may have one default Workspace.

### 4.2 Agent（代理） to CapsuleService

```text
Agent 1 --- n CapsuleService
```

An Agent（代理） may report and manage multiple Capsule Services.

In CE（社区版） v0.1, an embedded Agent（代理） usually manages one local Capsule Service（胶囊服务）, but the model should not forbid multiple services.

### 4.3 CapsuleService to HealthReport

```text
CapsuleService 1 --- n HealthReport
```

CE（社区版） v0.1 may store only recent or latest reports.

### 4.4 CapsuleService to ConfigItem

```text
CapsuleService 1 --- n ConfigItem
```

CE（社区版） v0.1 may implement config visibility only.

### 4.5 CapsuleService to ActionDefinition

```text
CapsuleService 1 --- n ActionDefinition
```

Actions are predefined by the Capsule Service（胶囊服务） or Agent（代理） SDK.

### 4.6 CapsuleService to Command

```text
CapsuleService 1 --- n Command
Agent 1 --- n Command
```

A command is issued to an Agent（代理） and usually targets one Capsule Service（胶囊服务）.

### 4.7 Command to CommandResult

```text
Command 1 --- 0..1 CommandResult
```

A command may not have a result yet while it is pending or running.

### 4.8 Everything to AuditEvent

Important operations should generate AuditEvents.

```text
User / Agent / System -> AuditEvent -> Resource
```

---

## 5. CE（社区版） v0.1 Minimum Domain Model

CE（社区版） v0.1 should implement at least these objects:

```text
User
Workspace
Agent
AgentToken
CapsuleService
HealthReport
ConfigItem
ActionDefinition
Command
CommandResult
AuditEvent
```

CE（社区版） v0.1 may keep these as JSON inside other objects:

```text
Capability
ResourceDefinition
SecretRef
CapsuleManifest
```

CE（社区版） v0.1 should not implement as first-class objects unless needed:

```text
CapsuleInstance
Tenant
Organization
BillingAccount
ClusterNode
LogStream
MetricSeries
```

---

## 6. 状态 Model Summary

Detailed status rules should be defined in:

```text
02-specs/09-status-model-spec.md
```

Minimum CE（社区版） statuses:

### 6.1 AgentStatus

```text
PENDING
ONLINE
OFFLINE
DISABLED
REVOKED
```

### 6.2 CapsuleServiceStatus

```text
UNKNOWN
ONLINE
UNHEALTHY
OFFLINE
STALE
DISABLED
```

### 6.3 HealthStatus

```text
UP
DOWN
DEGRADED
UNKNOWN
```

### 6.4 CommandStatus

```text
PENDING
DISPATCHED
RUNNING
SUCCESS
FAILED
EXPIRED
CANCELLED
```

### 6.5 TokenStatus

```text
ACTIVE
USED
REVOKED
EXPIRED
```

---

## 7. 实施指南 for CE（社区版） v0.1

### 7.1 Keep physical schema simple

The physical database schema should be simple enough for SQLite.

Avoid advanced database features that make MySQL/PostgreSQL migration difficult.

### 7.2 Use JSON fields for early flexibility

For CE（社区版） v0.1, use JSON fields for flexible structures such as:

- manifest;
- health details;
- action input schema;
- config metadata;
- command payload;
- command result;
- audit request/result details.

### 7.3 Keep Workspace implicit but present

Create a default Workspace automatically.

Use `workspaceId` in core tables where reasonable, even if UI does not expose Workspace management.

### 7.4 Keep Capability and ResourceDefinition lightweight

Store them in the manifest first.

Do not build a full dynamic admin-resource system in CE（社区版） v0.1.

### 7.5 Store token hashes only

Never store raw Agent（代理） tokens in the database.

### 7.6 Preserve Agent（代理） mode field

Even though CE（社区版） v0.1 implements only embedded Agent（代理）, keep `agentMode` or `mode` fields to support future sidecar and external Agents.

### 7.7 Distinguish reported and effective status

Do not show a service as online only because its last report was online.

If the Agent（代理） is offline or the report is stale, calculate `effectiveStatus` accordingly.

---

## 8. Future Extension Objects

The following objects are not required for CE（社区版） v0.1 but should be considered in future planning.

### 8.1 Tenant

Required for Cloud（云版） multi-tenancy and possibly EE（企业版） customer isolation.

### 8.2 Organization

Required for enterprise user and workspace grouping.

### 8.3 Role and Permission

Required for full RBAC.

### 8.4 SecretStore

Required for managed secrets, external vault integration, and Cloud（云版） secret boundary.

### 8.5 LogStream

Required for centralized logs and log analysis.

### 8.6 MetricSeries

Required for metrics, monitoring dashboards, and alerting.

### 8.7 AlertRule

Required for advanced alerts.

### 8.8 BillingAccount

Required for Cloud（云版） subscription and usage billing.

### 8.9 License

Required for EE（企业版） commercial packaging.

---

## 9. Anti-Patterns

Avoid these domain model mistakes.

### 9.1 Modeling CE（社区版） as Cloud（云版） from day one

Do not introduce tenant billing, complex organization hierarchy, or Cloud（云版） isolation into CE（社区版） v0.1.

### 9.2 Modeling CapsuleService as a heavy microservice

Do not require gateway, service mesh, or distributed transaction concepts.

### 9.3 Storing raw secrets in normal fields

Use secret references where possible.

### 9.4 Ignoring Agent（代理） identity

Every service report must be associated with an Agent（代理）.

### 9.5 Ignoring status freshness

Always distinguish last reported status from current effective status.

### 9.6 Over-normalizing early manifest data

Do not prematurely normalize all manifest resources, capabilities, and schemas into separate tables in CE（社区版） v0.1.

---

## 10. Summary

The `xtrape-capsule` domain model is centered around:

- Workspace;
- Agent（代理）;
- CapsuleService;
- Manifest;
- HealthReport;
- ConfigItem;
- ActionDefinition;
- Command;
- CommandResult;
- AuditEvent.

CE（社区版） v0.1 should implement a simple but extensible subset of this model.

The key design balance is:

> Keep CE（社区版） lightweight enough for single-node open-source deployment, while keeping the model open enough for EE（企业版） and Cloud（云版） evolution.
