# CE Data Model

- Status: Implementation Target
- Edition: CE
- Priority: Current

## Position

CE 是当前实现重点，目标是提供轻量、开源、可私有化部署的 Capsule Service 运行态治理平台。

## Current Constraints

- 默认 SQLite，后续预留 MySQL/PostgreSQL。
- 单镜像/单进程优先，前后端一体发布。
- Backend 使用 Node.js + TypeScript。
- UI 使用 Vue 或 React，发布为 Web 并兼容移动端查看。
- Agent 第一版只实现 Node.js Embedded Agent SDK。
- 通信优先使用 HTTP heartbeat + command polling。
- 不在 CE v0.1 实现 EE/Cloud 的复杂能力。

## Extension Principle

CE 要轻，但不能短视；EE/Cloud 要规划，但不能污染 CE 第一版实现。

# CE Data Model

- Status: Implementation Target
- Edition: CE
- Priority: Current
- Audience: architects, backend developers, database designers, agent SDK developers, AI coding agents

This document defines the data model for **Opstage CE v0.1**.

The CE data model should be simple enough for SQLite and the first MVP, while preserving a clean path toward MySQL/PostgreSQL, EE, and Cloud.

---

## 1. Data Model Goal

The goal of the CE v0.1 data model is to support the minimum complete Capsule governance loop:

```text
Admin login
    ↓
Agent registration
    ↓
Capsule Service report
    ↓
Heartbeat and health
    ↓
Config and action visibility
    ↓
Command creation
    ↓
Command polling and result reporting
    ↓
Audit log
```

The model should not over-normalize future EE/Cloud concepts before they are needed.

---

## 2. Design Principles

CE v0.1 data model should follow these principles:

1. Use SQLite by default.
2. Keep schema portable toward MySQL/PostgreSQL.
3. Store flexible metadata as JSON text where appropriate.
4. Store token hashes only, never raw tokens.
5. Avoid storing raw secrets.
6. Keep Workspace present but simple.
7. Distinguish reported status from effective status.
8. Keep Agent and Capsule Service state separate.
9. Model Commands and CommandResults explicitly.
10. Model AuditEvents explicitly.
11. Avoid first-class Tenant, Billing, Cluster, Metrics, and Log models in CE v0.1.

---

## 3. Required Data Objects

CE v0.1 should implement these objects:

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
SystemSetting
```

The following objects should not be first-class CE v0.1 models unless later required:

```text
Tenant
Organization
BillingAccount
ClusterNode
LogStream
MetricSeries
AlertRule
SecretStore
Role
Permission
```

---

## 4. Entity Relationship Overview

Recommended logical relationships:

```text
Workspace 1 --- n User
Workspace 1 --- n Agent
Workspace 1 --- n CapsuleService
Workspace 1 --- n Command
Workspace 1 --- n AuditEvent

Agent 1 --- n AgentToken
Agent 1 --- n CapsuleService
Agent 1 --- n Command

CapsuleService 1 --- n HealthReport
CapsuleService 1 --- n ConfigItem
CapsuleService 1 --- n ActionDefinition
CapsuleService 1 --- n Command

Command 1 --- 0..1 CommandResult
```

In CE v0.1, there is one default Workspace, but `workspaceId` should still be present on core tables where practical.

---

## 5. ID Strategy

### 5.1 Recommended ID format

CE v0.1 may use string IDs with stable prefixes.

Examples:

```text
usr_...
wks_...
agt_...
svc_...
tok_...
hlr_...
cfg_...
act_...
cmd_...
crs_...
aud_...
```

### 5.2 Rationale

String IDs are recommended for CE because:

- they are easy to debug;
- they work across SQLite, MySQL, and PostgreSQL;
- they avoid exposing sequential internal IDs;
- they are friendly to APIs and UI.

### 5.3 Alternative

Autoincrement integer IDs are acceptable for internal CE implementation, but public API IDs should preferably remain stable strings.

---

## 6. Workspace

A Workspace is the logical boundary for CE data.

CE v0.1 requires only one default Workspace.

### 6.1 Fields

```text
id              string primary key
code            string unique
name            string
status          string
createdAt       datetime
updatedAt       datetime
```

### 6.2 Default record

```text
code: default
name: Default Workspace
status: ACTIVE
```

### 6.3 Notes

- Workspace management UI is not required in CE v0.1.
- `workspaceId` should be included in core tables to preserve EE/Cloud upgrade paths.

---

## 7. User

A User represents a human Opstage operator.

CE v0.1 needs only simple local admin users.

### 7.1 Fields

```text
id              string primary key
workspaceId     string nullable or required
username        string unique
passwordHash    string
displayName     string nullable
role            string
status          string
lastLoginAt     datetime nullable
createdAt       datetime
updatedAt       datetime
```

### 7.2 Roles

CE v0.1 may support only:

```text
owner
```

Reserved roles:

```text
admin
viewer
```

### 7.3 Status values

```text
ACTIVE
DISABLED
```

### 7.4 Security rules

- Store only password hash.
- Do not store raw password.
- Use argon2 or bcrypt.
- Login and failed login should create AuditEvents.

---

## 8. Agent

An Agent is the governance bridge between Opstage Backend and Capsule Services.

### 8.1 Fields

```text
id                  string primary key
workspaceId         string
code                string
name                string
mode                string
runtime             string
version             string nullable
status              string
hostname            string nullable
os                  string nullable
arch                string nullable
lastHeartbeatAt     datetime nullable
registeredAt        datetime nullable
disabledAt          datetime nullable
revokedAt           datetime nullable
createdAt           datetime
updatedAt           datetime
```

### 8.2 Unique constraints

```text
workspaceId + code unique
```

### 8.3 Mode values

```text
embedded
sidecar
external
```

CE v0.1 implements only:

```text
embedded
```

### 8.4 Runtime values

```text
nodejs
java
python
go
other
```

CE v0.1 implements:

```text
nodejs
```

### 8.5 Status values

```text
PENDING
ONLINE
OFFLINE
DISABLED
REVOKED
```

### 8.6 Notes

Agent status should be calculated from heartbeat and administrative state.

Do not show an Agent as `ONLINE` if `lastHeartbeatAt` is beyond the offline threshold.

---

## 9. AgentToken

AgentToken stores registration tokens and Agent tokens.

Raw tokens must never be stored.

### 9.1 Fields

```text
id              string primary key
workspaceId     string
agentId         string nullable
tokenHash       string unique
type            string
status          string
name            string nullable
expiresAt       datetime nullable
createdAt       datetime
usedAt          datetime nullable
revokedAt       datetime nullable
```

### 9.2 Type values

```text
registration
agent
```

### 9.3 Status values

```text
ACTIVE
USED
REVOKED
EXPIRED
```

### 9.4 Rules

- Registration tokens may have `agentId = null` before use.
- Agent tokens must be associated with an Agent.
- One-time registration tokens should become `USED` after successful registration.
- Revoked Agent tokens must not be accepted.
- Raw token should be shown only once at creation time.

---

## 10. CapsuleService

CapsuleService is the main managed unit.

### 10.1 Fields

```text
id                  string primary key
workspaceId         string
agentId             string
code                string
name                string
description         string nullable
version             string nullable
runtime             string
agentMode           string
reportedStatus      string nullable
effectiveStatus     string
healthStatus        string nullable
manifestJson        text
lastReportedAt      datetime nullable
disabledAt          datetime nullable
createdAt           datetime
updatedAt           datetime
```

### 10.2 Unique constraints

```text
workspaceId + code unique
```

### 10.3 Status values

`effectiveStatus` uses CapsuleServiceStatus:

```text
UNKNOWN
ONLINE
UNHEALTHY
OFFLINE
STALE
DISABLED
```

`healthStatus` uses HealthStatus:

```text
UP
DOWN
DEGRADED
UNKNOWN
```

### 10.4 Rules

- `code` is stable and unique within Workspace.
- `manifestJson` stores full manifest.
- Key fields are extracted for list and query.
- `effectiveStatus` is calculated by Backend.
- Do not treat `reportedStatus` as current truth without freshness calculation.

---

## 11. HealthReport

HealthReport stores health information reported by Agents.

CE v0.1 may store latest report only or simple history.

### 11.1 Fields

```text
id                  string primary key
workspaceId         string
serviceId           string
agentId             string
status              string
message             string nullable
detailsJson         text nullable
dependenciesJson    text nullable
checkedAt           datetime nullable
receivedAt          datetime
createdAt           datetime
```

### 11.2 Status values

```text
UP
DOWN
DEGRADED
UNKNOWN
```

### 11.3 Retention

CE v0.1 may keep recent history or latest snapshot.

Recommended simple approach:

- store all reports initially;
- show latest report in UI;
- add cleanup later if needed.

### 11.4 Notes

Do not store raw secrets in health details.

---

## 12. ConfigItem

ConfigItem stores configuration metadata reported by a Capsule Service.

CE v0.1 focuses on config visibility, not editing.

### 12.1 Fields

```text
id                  string primary key
workspaceId         string
serviceId           string
configKey           string
label               string
description         string nullable
valueType           string
currentValueJson    text nullable
defaultValueJson    text nullable
editable            boolean
sensitive           boolean
required            boolean
sourceJson          text nullable
validationJson      text nullable
metadataJson        text nullable
createdAt           datetime
updatedAt           datetime
```

### 12.2 Unique constraints

```text
serviceId + configKey unique
```

### 12.3 Value types

```text
string
number
boolean
select
json
secretRef
```

### 12.4 Rules

- Sensitive raw values should not be stored.
- If `sensitive = true`, `currentValueJson` should be masked, null, or a `secretRef`.
- Config editing is not required in CE v0.1.

---

## 13. ActionDefinition

ActionDefinition stores predefined action metadata reported by a Capsule Service.

### 13.1 Fields

```text
id                  string primary key
workspaceId         string
serviceId           string
name                string
label               string
description         string nullable
dangerLevel         string
enabled             boolean
inputSchemaJson     text nullable
resultSchemaJson    text nullable
confirmRequired     boolean nullable
timeoutSeconds      integer nullable
metadataJson        text nullable
createdAt           datetime
updatedAt           datetime
```

### 13.2 Unique constraints

```text
serviceId + name unique
```

### 13.3 Danger levels

```text
LOW
MEDIUM
HIGH
CRITICAL
```

### 13.4 Rules

- Actions must be predefined.
- CE v0.1 must not support arbitrary shell execution.
- UI should require confirmation for `HIGH` and `CRITICAL` actions if present.

---

## 14. Command

Command stores an instruction created by Backend and executed by Agent.

CE v0.1 uses Command mainly for predefined action execution.

### 14.1 Fields

```text
id                  string primary key
workspaceId         string
agentId             string
serviceId           string
serviceCode         string
commandType         string
actionName          string nullable
payloadJson         text nullable
status              string
createdBy           string nullable
createdAt           datetime
expiresAt           datetime nullable
dispatchedAt        datetime nullable
startedAt           datetime nullable
finishedAt          datetime nullable
idempotencyKey      string nullable
metadataJson        text nullable
```

### 14.2 Command types

```text
ACTION
```

Reserved future types:

```text
CONFIG_UPDATE
CONFIG_RELOAD
SERVICE_REFRESH
AGENT_CONTROL
CUSTOM
```

### 14.3 Status values

```text
PENDING
DISPATCHED
SUCCESS
FAILED
EXPIRED
```

Reserved future values:

```text
RUNNING
CANCELLED
```

### 14.4 Rules

- Commands must target an Agent.
- Action commands must target a Capsule Service.
- Expired pending commands should not be dispatched.
- Commands should be audited.
- Command payloads should not contain raw secrets.

---

## 15. CommandResult

CommandResult stores the result reported by Agent after executing a Command.

### 15.1 Fields

```text
id                  string primary key
workspaceId         string
commandId           string unique
agentId             string
serviceId           string
status              string
outputText          string nullable
errorMessage        string nullable
resultJson          text nullable
startedAt           datetime nullable
finishedAt          datetime nullable
createdAt           datetime
```

### 15.2 Status values

```text
SUCCESS
FAILED
```

CE may also use `EXPIRED` if Backend creates result-like records for expired commands, but it is not required.

### 15.3 Rules

- One Command should have at most one final CommandResult.
- Failed result should include `errorMessage` where possible.
- Result JSON should be concise and not used as log storage.

---

## 16. AuditEvent

AuditEvent stores trace records for important operations.

### 16.1 Fields

```text
id                  string primary key
workspaceId         string
actorType           string
actorId             string nullable
actorName           string nullable
action              string
resourceType        string nullable
resourceId          string nullable
resourceCode        string nullable
description         string nullable
requestJson         text nullable
result              string
resultJson          text nullable
ip                  string nullable
userAgent           string nullable
metadataJson        text nullable
createdAt           datetime
```

### 16.2 Actor types

```text
user
agent
system
```

### 16.3 Result values

```text
SUCCESS
FAILED
DENIED
ERROR
PENDING
```

### 16.4 Required CE audit events

```text
user.login
user.login.failed
agent.registered
agent.service.reported
command.created
command.completed
command.failed
service.action.requested
service.action.completed
service.action.failed
```

### 16.5 Rules

- AuditEvents must not store raw secrets.
- Do not audit every heartbeat.
- Do not use AuditEvent as general application log storage.

---

## 17. SystemSetting

SystemSetting stores simple system-level configuration.

CE v0.1 may use environment variables only, but a SystemSetting table is useful for runtime display and future settings.

### 17.1 Fields

```text
id                  string primary key
key                 string unique
valueJson           text nullable
description         string nullable
sensitive           boolean
createdAt           datetime
updatedAt           datetime
```

### 17.2 Example settings

```text
agent.heartbeatIntervalSeconds
agent.offlineThresholdSeconds
command.pollIntervalSeconds
command.ttlSeconds
system.version
```

### 17.3 Rules

- Sensitive settings must not expose raw values.
- CE v0.1 may keep settings read-only in UI.

---

## 18. Recommended Prisma Model Shape

The actual Prisma schema may differ, but it should follow this shape.

Example excerpt:

```prisma
model Workspace {
  id        String   @id
  code      String   @unique
  name      String
  status    String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  agents    Agent[]
  services  CapsuleService[]
  users     User[]
}

model Agent {
  id              String   @id
  workspaceId     String
  code            String
  name            String
  mode            String
  runtime         String
  version         String?
  status          String
  hostname        String?
  os              String?
  arch            String?
  lastHeartbeatAt DateTime?
  registeredAt    DateTime?
  disabledAt      DateTime?
  revokedAt       DateTime?
  createdAt       DateTime @default(now())
  updatedAt       DateTime @updatedAt

  workspace Workspace @relation(fields: [workspaceId], references: [id])
  services  CapsuleService[]
  tokens    AgentToken[]

  @@unique([workspaceId, code])
}

model CapsuleService {
  id              String   @id
  workspaceId     String
  agentId         String
  code            String
  name            String
  description     String?
  version         String?
  runtime         String
  agentMode       String
  reportedStatus  String?
  effectiveStatus String
  healthStatus    String?
  manifestJson    String
  lastReportedAt  DateTime?
  disabledAt      DateTime?
  createdAt       DateTime @default(now())
  updatedAt       DateTime @updatedAt

  workspace Workspace @relation(fields: [workspaceId], references: [id])
  agent     Agent     @relation(fields: [agentId], references: [id])

  @@unique([workspaceId, code])
}
```

Full schema should be implemented in the actual repository.

---

## 19. Indexing Recommendations

CE v0.1 should keep indexes simple.

Recommended indexes:

```text
User.username unique
Workspace.code unique
Agent.workspaceId + Agent.code unique
Agent.lastHeartbeatAt
CapsuleService.workspaceId + CapsuleService.code unique
CapsuleService.agentId
CapsuleService.effectiveStatus
Command.agentId + Command.status
Command.serviceId + Command.createdAt
Command.createdAt
AuditEvent.workspaceId + AuditEvent.createdAt
AuditEvent.resourceType + AuditEvent.resourceId
AuditEvent.actorType + AuditEvent.actorId
```

SQLite should handle this scale for CE.

---

## 20. JSON Field Guidelines

Use JSON text fields for flexible metadata in CE v0.1.

Recommended JSON fields:

```text
manifestJson
HealthReport.detailsJson
HealthReport.dependenciesJson
ConfigItem.currentValueJson
ConfigItem.defaultValueJson
ConfigItem.sourceJson
ConfigItem.validationJson
ConfigItem.metadataJson
ActionDefinition.inputSchemaJson
ActionDefinition.resultSchemaJson
ActionDefinition.metadataJson
Command.payloadJson
Command.metadataJson
CommandResult.resultJson
AuditEvent.requestJson
AuditEvent.resultJson
AuditEvent.metadataJson
SystemSetting.valueJson
```

Rules:

- JSON should be valid JSON when stored.
- Do not store raw secrets in JSON.
- Keep large logs out of JSON fields.
- Normalize later only when access patterns require it.

---

## 21. Status Storage Rules

### 21.1 Agent status

Agent status should be stored but also recalculated from heartbeat when queried or by scheduled check.

### 21.2 Capsule Service status

Store both:

```text
reportedStatus
effectiveStatus
```

Do not show `reportedStatus` as current truth without freshness calculation.

### 21.3 Health status

Store latest HealthStatus on CapsuleService for list performance.

Store detailed health in HealthReport.

---

## 22. Token and Secret Rules

### 22.1 Token storage

Store only:

```text
tokenHash
```

Never store raw:

```text
registrationToken
agentToken
```

### 22.2 Secret handling

Do not store raw secrets in:

- manifestJson;
- config values;
- health details;
- command payload;
- command result;
- audit events.

Use `secretRef` where needed.

---

## 23. Data Retention

CE v0.1 may keep data indefinitely by default.

Future cleanup may be added for:

- old HealthReports;
- old Commands;
- old CommandResults;
- old AuditEvents.

Do not implement complex retention policies in CE v0.1 unless needed.

---

## 24. Migration Considerations

The schema should preserve future migration paths.

### 24.1 SQLite to MySQL/PostgreSQL

Avoid:

- SQLite-specific SQL where possible;
- relying on loose typing behavior;
- storing non-portable datetime formats.

Prefer:

- ISO-compatible datetime handling;
- Prisma migrations;
- portable indexes;
- explicit string status values.

### 24.2 CE to EE/Cloud

Keep room for:

- multiple Workspaces;
- RBAC;
- organizations;
- tenants;
- external databases;
- richer Agent modes;
- managed secrets;
- observability tables.

Do not implement these first-class in CE v0.1.

---

## 25. Data Model Non-Goals

CE v0.1 data model should not include:

- Tenant;
- Organization;
- BillingAccount;
- Subscription;
- Invoice;
- ClusterNode;
- MetricSeries;
- LogStream;
- TraceSpan;
- AlertRule;
- SecretStore;
- ApprovalWorkflow;
- ConfigVersion;
- ConfigRelease;
- Role/Permission policy engine.

These may be added in EE/Cloud or later CE versions.

---

## 26. Data Model Acceptance Criteria

The CE v0.1 data model is acceptable when:

- it supports admin login;
- it supports default Workspace;
- it supports Agent registration and token validation;
- it stores only token hashes;
- it supports Agent heartbeat and offline calculation;
- it supports Capsule Service manifest storage;
- it supports latest health display;
- it supports config visibility;
- it supports predefined actions;
- it supports Command and CommandResult;
- it supports AuditEvent;
- it avoids raw secret storage;
- it runs on SQLite;
- it does not block MySQL/PostgreSQL migration.

---

## 27. Summary

The CE data model should be small, explicit, and extensible.

It should implement the core governance records:

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

The most important data model rule is:

> Store enough structure to operate safely, and use JSON for flexible metadata until the model proves itself.