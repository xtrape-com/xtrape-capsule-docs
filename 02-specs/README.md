---
status: accepted
audience: architects
stability: evolving
last_reviewed: 2026-05-05
---

# Shared Specifications

- Status: Specification
- Edition: Shared
- Priority: High
- Audience: architects, backend developers, frontend developers, agent SDK developers, AI coding agents

> **Precedence rule**: When this directory and `08-decisions/` ADRs or `09-contracts/` (OpenAPI / Prisma) disagree, the ADRs and contracts win for CE v0.1. The contracts are normative; this directory captures shared concepts and rationale.

This directory contains the shared specifications for the `xtrape-capsule` domain.

These specifications define the long-term contracts shared by CE, EE, and Cloud editions. CE v0.1 may implement only a
subset of each specification, but it should not introduce incompatible names, status values, data structures, or
protocol concepts.

---

## 1. Purpose

The purpose of `02-specs/` is to define stable cross-edition contracts for:

- Capsule Service metadata;
- Capsule management surface;
- Agent registration;
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
- Node.js embedded Agent SDK design;
- future sidecar and external Agent design;
- future EE and Cloud compatibility.

---

## 2. Current Implementation Focus

The current implementation focus is **CE v0.1**.

CE v0.1 should implement the minimum useful subset of these specifications:

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

CE v0.1 should not implement the full EE or Cloud planning scope.

---

## 3. Specification List

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

Defines the Capsule Manifest: the metadata contract that describes a Capsule Service's identity, runtime, capabilities, resources, actions, configs, and governance metadata.

CE v0.1 must support manifest reporting from the Node.js embedded Agent SDK.

### `02-capsule-management-contract.md`

Defines the logical management surface of a Capsule Service.

The long-term contract includes:

```text
manifest
health
configs
actions
resources
events
metrics
```

CE v0.1 should implement only:

```text
manifest
health
configs
actions
```

through the Node.js embedded Agent SDK.

### `03-agent-registration-spec.md`

Defines Agent enrollment, registration tokens, Agent tokens, heartbeat, service reporting, command polling, result reporting, Agent status, revocation, and authorization.

CE v0.1 must implement the basic registration and heartbeat loop.

### `04-health-spec.md`

Defines HealthReport, DependencyHealth, HealthStatus, freshness, and how health interacts with Agent status and Capsule Service status.

CE v0.1 must support health reporting and display, but not a full metrics or observability platform.

### `05-action-spec.md`

Defines predefined actions exposed by Capsule Services.

CE v0.1 must support predefined action execution through Commands and must not support arbitrary shell execution.

> Note: if the file is currently named `action-spec.md`, it should be renamed to `05-action-spec.md` to match the numbered reading order.

### `06-config-spec.md`

Defines ConfigItem metadata, config visibility, sensitive value handling, `secretRef`, and future config editing extension points.

CE v0.1 should implement config visibility only.

### `07-command-spec.md`

Defines Command and CommandResult, command lifecycle, command polling, expiration, idempotency, and safety rules.

CE v0.1 should implement the `ACTION` command type only.

### `08-audit-event-spec.md`

Defines AuditEvent structure, action naming, audit triggers, request/result sanitization, storage, and UI requirements.

CE v0.1 should implement lightweight audit logs, not a full compliance platform.

### `09-status-model-spec.md`

Defines AgentStatus, CapsuleServiceStatus, HealthStatus, CommandStatus, TokenStatus, AuditResult, FreshnessStatus, and effective status calculation.

CE v0.1 must distinguish reported status from effective status.

---

## 4. CE v0.1 Specification Subset

CE v0.1 should implement the following minimum contract.

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

### 4.2 Agent Registration

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

Forbidden in CE v0.1:

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

### 4.8 Status

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

Status values must remain stable, uppercase, and non-localized.

UI may localize labels, but stored data and API values should use English uppercase identifiers.

### 5.4 CE may implement subsets

A shared specification may define more than CE v0.1 implements.

This is acceptable if CE clearly documents its implemented subset.

Example:

```text
Spec supports: embedded, sidecar, external Agent modes
CE v0.1 implements: embedded only
```

### 5.5 Do not pollute CE with EE or Cloud complexity

EE and Cloud may extend specifications, but they should not force CE v0.1 to implement:

- multi-tenancy;
- billing;
- enterprise RBAC;
- SSO;
- cluster deployment;
- centralized log platform;
- metrics dashboard;
- approval workflow;
- secret vault integration.

CE should reserve extension points without implementing heavy future capabilities.

---

## 6. Security Rules Across Specs

The following rules apply to all specifications.

### 6.1 No raw tokens in storage

Registration tokens and Agent tokens must be stored as hashes.

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

### 6.3 No arbitrary shell execution in CE v0.1

CE v0.1 must support only predefined actions.

### 6.4 Agent authorization required

Agent APIs must require a valid Agent token.

### 6.5 Audit important operations

Important governance operations should create AuditEvents.

---

## 7. Development Guidance

When implementing CE v0.1:

1. Read this README first.
2. Read the manifest, registration, health, action, command, audit, and status specs.
3. Implement only the CE v0.1 subset.
4. Keep fields compatible with future EE and Cloud.
5. Do not introduce custom undocumented status values.
6. Do not store raw secrets.
7. Keep Agent-based registration as the only service onboarding path.
8. Prefer JSON fields for flexible metadata in CE v0.1.
9. Avoid over-normalizing future resources too early.
10. Update the relevant spec before introducing a new shared concept.

---

## 8. Review Checklist

Before accepting a CE implementation, check:

- Does the Agent register with a registration token?
- Does Backend issue and verify an Agent token?
- Are tokens stored as hashes?
- Does the Agent heartbeat update Agent status?
- Does Backend calculate stale service status?
- Does the manifest include stable service identity?
- Are actions predefined?
- Is arbitrary shell execution absent?
- Does action execution create a Command?
- Does Agent report a CommandResult?
- Are important operations audited?
- Are sensitive values masked or represented as `secretRef`?
- Are status values from the shared Status Model?
- Is CE free from unnecessary EE/Cloud features?

---

## 9. Anti-Patterns

Avoid these patterns:

### 9.1 Implementing CE as a full enterprise platform

CE v0.1 should stay lightweight.

### 9.2 Adding Cloud-only fields as CE requirements

Do not require tenant, billing, subscription, or Cloud organization fields in CE v0.1.

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

The `02-specs/` directory defines the shared contracts that keep `xtrape-capsule` consistent across CE, EE, and Cloud.

CE v0.1 should implement only the smallest useful subset, but it should follow the shared contracts carefully.

The key rule is:

> CE may be small, but it should not be incompatible.

## Spec Status Policy

This repository currently keeps specs in place to avoid breaking references. Use the frontmatter `status` field to distinguish accepted specs from draft specs.

- `status: accepted` means the document is a current implementation target or stable design baseline.
- `status: draft` or `status: proposed` means the document is exploratory or future-looking.
- Implementation docs should reference accepted specs first.

A future cleanup may move files into `accepted/` and `draft/` folders once references are updated safely.
