<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: README.md
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

# 共享 Specifications

- Status: 规范
- Edition: 共享
- Priority: 高
- Audience: architects, backend developers, frontend developers, agent SDK developers, AI coding agents

> **Precedence rule**: When this directory and `08-decisions/` ADRs or `09-contracts/` (OpenAPI / Prisma) disagree, the ADRs and contracts win for CE（社区版） v0.1. The contracts are normative; this directory captures shared concepts and rationale.

This directory 包含 the shared specifications for the `xtrape-capsule` domain.

These specifications define the long-term contracts shared by CE（社区版）, EE（企业版）, and Cloud（云版） editions. CE（社区版） v0.1 may implement only a subset of each specification, but it should not introduce incompatible names, status values, data structures, or protocol concepts.

---

## 1. Purpose

The purpose of `02-specs/` is to define stable cross-edition contracts for:

- Capsule Service（胶囊服务） metadata;
- Capsule management surface;
- Agent（代理） registration;
- health reporting;
- action execution;
- configuration metadata;
- command delivery;
- audit events;
- status values and mapping rules.

These documents should guide:

- Backend API design;
- Backend database model design;
- UI data model and display rules;
- Node.js embedded Agent（代理） SDK design;
- future sidecar and external Agent（代理） design;
- future EE（企业版） and Cloud（云版） compatibility.

---

## 2. Current 实现 Focus

The current implementation focus is **CE（社区版） v0.1**.

CE（社区版） v0.1 should implement the minimum useful subset of these specifications:

```text
Agent registration
Manifest reporting
Health reporting
Config visibility
Predefined actions
Command polling
Command result reporting
Basic audit events
Status freshness calculation
```

CE（社区版） v0.1 should not implement the full EE（企业版） or Cloud（云版） planning scope.

---

## 3. 规范 List

Recommended reading order:

```text
01-capsule-manifest-spec.md
02-capsule-management-contract.md
03-agent-registration-spec.md
04-health-spec.md
05-action-spec.md
06-config-spec.md
07-command-spec.md
08-audit-event-spec.md
09-status-model-spec.md
```

### `01-capsule-manifest-spec.md`

Defines the Capsule Manifest: the metadata contract that 描述 a Capsule Service（胶囊服务）'s identity, runtime, capabilities, resources, actions, configs, and governance metadata.

CE（社区版） v0.1 must support manifest reporting from the Node.js embedded Agent（代理） SDK.

### `02-capsule-management-contract.md`

Defines the logical management surface of a Capsule Service（胶囊服务）.

The long-term contract 包括:

```text
manifest
health
configs
actions
resources
events
metrics
```

CE（社区版） v0.1 should implement only:

```text
manifest
health
configs
actions
```

through the Node.js embedded Agent（代理） SDK.

### `03-agent-registration-spec.md`

Defines Agent（代理） enrollment, registration tokens, Agent（代理） tokens, heartbeat, service reporting, command polling, result reporting, Agent（代理） status, revocation, and authorization.

CE（社区版） v0.1 must implement the basic registration and heartbeat loop.

### `04-health-spec.md`

Defines HealthReport, DependencyHealth, HealthStatus, freshness, and how health interacts with Agent（代理） status and Capsule Service（胶囊服务） status.

CE（社区版） v0.1 must support health reporting and display, but not a full metrics or observability platform.

### `05-action-spec.md`

Defines predefined actions exposed by Capsule Services.

CE（社区版） v0.1 must support predefined action execution through Commands and must not support arbitrary shell execution.

> Note: if the file is currently named `action-spec.md`, it should be renamed to `05-action-spec.md` to match the numbered reading order.

### `06-config-spec.md`

Defines ConfigItem metadata, config visibility, sensitive value handling, `secretRef`, and future config editing extension points.

CE（社区版） v0.1 should implement config visibility only.

### `07-command-spec.md`

Defines Command and CommandResult, command lifecycle, command polling, expiration, idempotency, and safety rules.

CE（社区版） v0.1 should implement the `ACTION` command type only.

### `08-audit-event-spec.md`

Defines AuditEvent structure, action naming, audit triggers, request/result sanitization, storage, and UI requirements.

CE（社区版） v0.1 should implement lightweight audit logs, not a full compliance platform.

### `09-status-model-spec.md`

Defines AgentStatus, CapsuleServiceStatus, HealthStatus, CommandStatus, TokenStatus, AuditResult, FreshnessStatus, and effective status calculation.

CE（社区版） v0.1 must distinguish reported status from effective status.

---

## 4. CE（社区版） v0.1 规范 Subset

CE（社区版） v0.1 should implement the following minimum contract.

### 4.1 Manifest

Required fields:

```text
kind
code
name
version
runtime
agentMode
```

Optional fields:

```text
capabilities
actions
configs
resources
metadata
```

The Backend may store the full manifest as JSON and extract only key display fields.

### 4.2 Agent（代理） Registration

Required:

```text
registration token
Agent registration API
Agent token issuance
Agent token hash storage
heartbeat API
service report API
command polling API
command result API
```

### 4.3 Health

Required:

```text
HealthStatus: UP / DOWN / DEGRADED / UNKNOWN
HealthReport
latest health storage
stale calculation
UI display
```

### 4.4 Actions

Required:

```text
predefined ActionDefinition
action request from UI
Backend Command creation
Agent action handler
CommandResult reporting
AuditEvent
```

Forbidden in CE（社区版） v0.1:

```text
arbitrary shell execution
```

### 4.5 Config

Required:

```text
ConfigItem metadata
config visibility
sensitive value masking
secretRef type
```

Not required:

```text
config publishing
approval
rollback
versioning
```

### 4.6 Command

Required (must match OpenAPI `CommandStatus` and ADR 0003):

```text
ACTION command type
PENDING / RUNNING / SUCCEEDED / FAILED / EXPIRED
CANCELLED reserved (no UI)
polling delivery (transitions PENDING -> RUNNING)
result reporting (transitions RUNNING -> SUCCEEDED|FAILED)
basic expiration
```

### 4.7 Audit

Required:

```text
AuditEvent storage
user login audit
Agent registration audit
Command created audit
Command completed / failed audit
basic audit list UI
```

### 4.8 状态

Required:

```text
Agent effective status
Capsule Service effective status
HealthStatus
CommandStatus
TokenStatus
FreshnessStatus
reported vs effective status distinction
```

---

## 5. Compatibility Rules

### 5.1 Additive evolution

Specifications should evolve additively when possible.

New optional fields may be added.

Older clients should ignore unknown optional fields where practical.

### 5.2 Stable required fields

Required fields should not change meaning after they are used in implementation.

Examples of stable fields:

```text
code
name
version
runtime
agentMode
status
actionName
commandType
createdAt
```

### 5.3 Stable status values

状态 values must remain stable, uppercase, and non-localized.

UI may localize labels, but stored data and API values should use English uppercase identifiers.

### 5.4 CE（社区版） may implement subsets

A shared specification may define more than CE（社区版） v0.1 implements.

This is acceptable if CE（社区版） clearly documents its implemented subset.

Example:

```text
Spec supports: embedded, sidecar, external Agent modes
CE v0.1 implements: embedded only
```

### 5.5 Do not pollute CE（社区版） with EE（企业版） or Cloud（云版） complexity

EE（企业版） and Cloud（云版） may extend specifications, but they should not force CE（社区版） v0.1 to implement:

- multi-tenancy;
- billing;
- enterprise RBAC;
- SSO;
- cluster deployment;
- centralized log platform;
- metrics dashboard;
- approval workflow;
- secret vault integration.

CE（社区版） should reserve extension points without implementing heavy future capabilities.

---

## 6. 安全 Rules Across Specs

The following rules apply to all specifications.

### 6.1 No raw tokens in storage

Registration tokens and Agent（代理） tokens must be stored as hashes.

### 6.2 No raw secrets in manifests, configs, health, commands, or audit events

Sensitive data should be represented by `secretRef` or masked.

Sensitive examples:

```text
password
token
accessToken
refreshToken
cookie
apiKey
privateKey
credential
```

### 6.3 No arbitrary shell execution in CE（社区版） v0.1

CE（社区版） v0.1 must support only predefined actions.

### 6.4 Agent（代理） authorization required

Agent（代理） APIs must require a valid Agent（代理） token.

### 6.5 Audit important operations

Important governance operations should create AuditEvents.

---

## 7. 开发 Guidance

When implementing CE（社区版） v0.1:

1. Read this README first.
2. Read the manifest, registration, health, action, command, audit, and status specs.
3. Implement only the CE（社区版） v0.1 subset.
4. Keep fields compatible with future EE（企业版） and Cloud（云版）.
5. Do not introduce custom undocumented status values.
6. Do not store raw secrets.
7. Keep Agent（代理）-based registration as the only service onboarding path.
8. Prefer JSON fields for flexible metadata in CE（社区版） v0.1.
9. Avoid over-normalizing future resources too early.
10. Update the relevant spec before introducing a new shared concept.

---

## 8. Review Checklist

Before accepting a CE（社区版） implementation, check:

- Does the Agent（代理） register with a registration token?
- Does Backend issue and verify an Agent（代理） token?
- Are tokens stored as hashes?
- Does the Agent（代理） heartbeat update Agent（代理） status?
- Does Backend calculate stale service status?
- Does the manifest include stable service identity?
- Are actions predefined?
- Is arbitrary shell execution absent?
- Does action execution create a Command?
- Does Agent（代理） report a CommandResult?
- Are important operations audited?
- Are sensitive values masked or represented as `secretRef`?
- Are status values from the shared 状态 Model?
- Is CE（社区版） free from unnecessary EE（企业版）/Cloud（云版） features?

---

## 9. Anti-Patterns

Avoid these patterns:

### 9.1 Implementing CE（社区版） as a full enterprise platform

CE（社区版） v0.1 should stay lightweight.

### 9.2 Adding Cloud（云版）-only fields as CE（社区版） requirements

Do not require tenant, billing, subscription, or Cloud（云版） organization fields in CE（社区版） v0.1.

### 9.3 Using UI colors as backend status

Use stable status values, not colors.

### 9.4 Mixing business API and management contract

The Capsule Management Contract is for governance, not business endpoints.

### 9.5 Storing raw secrets

Never store raw credentials, cookies, or tokens in shared payloads.

### 9.6 Executing arbitrary remote commands

Use predefined actions and Command records.

---

## 10. Summary

The `02-specs/` directory 定义 the shared contracts that keep `xtrape-capsule` consistent across CE（社区版）, EE（企业版）, and Cloud（云版）.

CE（社区版） v0.1 should implement only the smallest useful subset, but it should follow the shared contracts carefully.

The key rule is:

> CE（社区版） may be small, but it should not be incompatible.
