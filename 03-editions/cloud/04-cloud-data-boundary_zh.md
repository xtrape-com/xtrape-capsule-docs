<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 04-cloud-data-boundary.md
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

# Cloud（云版） Data Boundary

- Status: Planning
- Edition: Cloud（云版）
- Priority: Future
- Audience: founders, product designers, architects, cloud engineers, backend developers, security reviewers, AI coding agents

This document 定义 the planned data boundary for **Opstage（运维舞台） Cloud（云版）**.

Opstage（运维舞台） Cloud（云版） is the future hosted SaaS edition of the `xtrape-capsule` product family. Cloud（云版） data boundary design is a future capability and is not a CE（社区版） v0.1 implementation requirement.

---

## 1. Purpose

The purpose of this document is to define:

- what data Opstage（运维舞台） Cloud（云版） may store;
- what data should remain customer-controlled;
- how sensitive data should be represented;
- how `secretRef` should be used;
- how Agents should avoid leaking secrets;
- how audit, command, config, and health data should be bounded;
- what export, deletion, and retention capabilities Cloud（云版） may need;
- what CE（社区版） should reserve without implementing Cloud（云版） complexity.

The key rule is:

> Cloud（云版） should store governance metadata and secret references by default, not raw customer operational secrets.

---

## 2. Boundary Statement

Opstage（运维舞台） Cloud（云版） should provide hosted governance for Capsule Services while respecting customer data ownership.

Recommended boundary:

```text
Cloud stores:      governance metadata, status, health, commands, results, audit, usage metadata
Customer stores:   raw credentials, account secrets, cookies, private keys, local runtime data
Cloud may store:   optional managed secrets only if explicitly enabled in a future plan
```

This boundary should be clear in product messaging, security documentation, APIs, UI, and Agent（代理） SDK behavior.

---

## 3. Data Classification

Cloud（云版） data can be classified into several categories.

```text
Public product metadata
Customer governance metadata
Operational state
Action and command data
Audit data
Usage and billing data
Sensitive references
Raw secrets
Customer business data
```

Each category requires different handling.

---

## 4. Data Cloud（云版） May Store by Default

Cloud（云版） may store the following data by default.

### 4.1 Tenant and organization metadata

Examples:

```text
Tenant ID
Organization ID
Organization name
Workspace ID
Workspace name
Membership metadata
Role assignments
Subscription plan metadata
```

These are Cloud（云版）-only concepts and not CE（社区版） v0.1 requirements.

### 4.2 User and identity metadata

Examples:

```text
User ID
Email
Display name
Role assignments
Login timestamps
Identity provider metadata
```

Cloud（云版） should not store raw passwords. Passwords, if used, must be hashed.

### 4.3 Agent（代理） metadata

Examples:

```text
Agent ID
Agent code
Agent name
Agent mode
Runtime
Version
Hostname if reported
OS and architecture if reported
Last heartbeat time
Token status
Protocol version
```

Agent（代理） metadata is governance metadata.

### 4.4 Capsule Service（胶囊服务） metadata

Examples:

```text
Service ID
Service code
Service name
Version
Runtime
Agent mode
Description
Capabilities
Resources
Manifest metadata
```

Cloud（云版） may store full manifests, but manifests must not include raw secrets.

### 4.5 Health and status data

Examples:

```text
HealthStatus
CapsuleServiceStatus
AgentStatus
FreshnessStatus
Health message
Dependency health
Checked time
Received time
```

Health payloads must not include raw secrets or excessive customer business data.

### 4.6 Config metadata

Examples:

```text
Config key
Label
Description
Type
Default value if safe
Current value if non-sensitive
Editable flag
Sensitive flag
Validation metadata
Source metadata
secretRef
```

Cloud（云版） should not store raw sensitive config values by default.

### 4.7 Action metadata

Examples:

```text
Action name
Label
Description
Danger level
Input schema
Result schema
Enabled state
Confirmation requirement
```

Action metadata is safe if it does not contain secrets.

### 4.8 Command and CommandResult data

Examples:

```text
Command ID
Command type
Action name
Target Agent
Target Service
Payload if safe
Status
Output text
Error message
Result JSON if safe
Timestamps
```

Command payloads and results must be sanitized and should not contain raw secrets.

### 4.9 Audit data

Examples:

```text
Actor
Action
Resource
Result
Timestamp
Sanitized request JSON
Sanitized result JSON
IP or region metadata
User agent metadata
```

Audit data may be sensitive and should be access-controlled and retention-managed.

### 4.10 Usage and billing metadata

Examples:

```text
Number of Agents
Number of Capsule Services
Command volume
Audit retention tier
Health history volume
Alert volume
Plan limits
Subscription status
```

These are Cloud（云版）-only capabilities.

---

## 5. Data Cloud（云版） Should Not Store by Default

Cloud（云版） should not store the following by default:

```text
raw passwords
raw registration tokens
raw Agent tokens
raw API keys
raw OAuth access tokens
raw OAuth refresh tokens
raw cookies
browser session cookies
private keys
account credentials
unencrypted secret values
customer business records
large application logs
full browser traces
private files from customer services
```

If Cloud（云版） later 支持 optional managed secrets, that must be a separate explicit capability with clear security design.

---

## 6. SecretRef Boundary

`secretRef` is the primary data boundary mechanism.

A `secretRef` points to a secret without exposing its raw value to Cloud（云版）.

Examples:

```text
agent-local://agent-001/secrets/chatgpt/account-001
customer-vault://prod/integration-worker/account-001
aws-secretsmanager://region/account/secret-name
azure-keyvault://vault-name/secret-name
cloud-secret://org/workspace/secret-key
```

### 6.1 CE（社区版）-compatible behavior

CE（社区版） v0.1 should only need to:

- recognize `secretRef` as a value type;
- display it safely;
- preserve it in metadata;
- avoid resolving it.

### 6.2 Cloud（云版） behavior

Cloud（云版） should initially:

- display secret references safely;
- not resolve customer-controlled secret references;
- not require raw secrets for basic governance;
- allow future optional managed secret providers.

### 6.3 UI display

Recommended UI display:

```text
secretRef: agent-local://agent-001/secrets/chatgpt/account-001
```

or masked form:

```text
secretRef: agent-local://.../account-001
```

---

## 7. Agent（代理）-Local Secret Boundary

For many Capsule Services, the safest default is Agent（代理）-local secret handling.

Recommended model:

```text
Raw secret stays in customer environment.
Agent or Capsule Service resolves it locally.
Cloud stores only secretRef.
```

Example:

```text
Cloud Command payload:
{
  "accountSecretRef": "agent-local://agent-001/secrets/chatgpt/account-001"
}

Agent resolves locally:
agent-local://agent-001/secrets/chatgpt/account-001 -> actual credential
```

Cloud（云版） does not see the actual credential.

---

## 8. Config Data Boundary

Config metadata is useful for governance, but config values can be sensitive.

### 8.1 Safe config data

Cloud（云版） may store:

```text
key
label
type
defaultValue if non-sensitive
currentValue if non-sensitive
editable
sensitive
validation
source
metadata
```

### 8.2 Sensitive config data

If `sensitive = true`, Cloud（云版） should store:

```text
null
masked value
secretRef
```

not raw value.

Bad:

```json
{
  "key": "chatgpt.password",
  "currentValue": "plain-text-password",
  "sensitive": true
}
```

Good:

```json
{
  "key": "chatgpt.accountSecret",
  "currentValue": "agent-local://agent-001/secrets/chatgpt/account-001",
  "type": "secretRef",
  "sensitive": true
}
```

---

## 9. Command Data Boundary

Commands may contain operational payloads.

### 9.1 Safe command payloads

Safe payload examples:

```json
{
  "sessionId": "ses_001"
}
```

```json
{
  "message": "hello"
}
```

### 9.2 Sensitive command payloads

If a Command needs a secret, it should use `secretRef`.

Bad:

```json
{
  "password": "plain-text-password"
}
```

Good:

```json
{
  "accountSecretRef": "agent-local://agent-001/secrets/chatgpt/account-001"
}
```

### 9.3 CommandResult boundary

CommandResult should be concise.

Do not use CommandResult as:

- log storage;
- browser trace storage;
- full customer data dump;
- raw credential output.

---

## 10. Health Data Boundary

Health data should describe operational health, not expose business data.

Cloud（云版） may store:

```text
HealthStatus
message
dependency status
timing metadata
sanitized error code
```

Cloud（云版） should avoid storing:

```text
raw tokens
credentials
cookies
full request payloads
private customer records
full stack traces with secrets
```

Health provider errors should be sanitized before sending to Cloud（云版）.

---

## 11. Audit Data Boundary

Audit data is important and sensitive.

Cloud（云版） may store:

```text
actor
action
resource
result
timestamp
sanitized request summary
sanitized result summary
metadata
```

Cloud（云版） should not store raw secrets in audit events.

### 11.1 Audit sanitization

Sensitive keys should be masked or removed:

```text
password
token
accessToken
refreshToken
cookie
apiKey
privateKey
credential
secret
authorization
```

Recommended mask:

```text
***REDACTED***
```

### 11.2 Audit retention

Cloud（云版） may provide retention tiers in future plans.

Examples:

```text
7 days
30 days
90 days
1 year
custom enterprise retention
```

CE（社区版） v0.1 does not need retention tiers.

---

## 12. Manifest Data Boundary

Manifest 描述 service metadata.

Cloud（云版） may store manifest fields such as:

```text
kind
schemaVersion
code
name
version
runtime
agentMode
capabilities
resources
actions
configs
metadata
```

Manifest must not include raw secrets.

If a service needs to declare secret usage, it should declare references or metadata only.

---

## 13. Logs, Metrics, and Traces Boundary

Cloud（云版） may later provide managed observability, but should not automatically collect arbitrary logs, metrics, or traces in early versions.

### 13.1 Logs

Large application logs should not be stored in CommandResult or AuditEvent.

If Cloud（云版） later 支持 logs, it should define:

- log collection scope;
- retention;
- filtering;
- sensitive data redaction;
- access control;
- pricing impact.

### 13.2 Metrics

Cloud（云版） may store governance metrics such as:

```text
heartbeat count
command count
failure count
Agent online duration
service stale duration
```

These are different from arbitrary application metrics.

### 13.3 Traces

Distributed tracing is not part of Cloud（云版） initial governance boundary.

---

## 14. Customer Business Data Boundary

Cloud（云版） should not become a default store for customer business data.

Examples of customer business data:

```text
end-user records
payment records
private documents
conversation history
browser page content
scraped raw content
business transaction payloads
```

Capsule Services should keep business data in customer-controlled systems unless explicitly designed otherwise.

Cloud（云版） may store summaries or references only when required for governance.

---

## 15. Optional Managed Secrets

Future Cloud（云版） may offer optional managed secrets.

This should be a separate feature with explicit security model.

Possible requirements:

- encryption at rest;
- key management;
- access policy;
- audit of secret access;
- secret rotation;
- customer opt-in;
- export/delete controls;
- enterprise plan boundary.

Managed secrets should not be required for basic Cloud（云版） governance.

---

## 16. Data Export

Cloud（云版） should eventually support customer data export.

Possible export scopes:

```text
Workspace metadata
Agent metadata
Capsule Service metadata
Command history
Audit events
Health history
Config metadata
```

Export formats may include:

```text
JSON
CSV
NDJSON
ZIP bundle
```

CE（社区版） v0.1 does not need Cloud（云版） export workflows.

---

## 17. Data Deletion

Cloud（云版） should eventually support data deletion controls.

Possible deletion scopes:

```text
Workspace deletion
Organization deletion
Agent deletion
Capsule Service removal
Audit retention expiration
User account deletion
```

Deletion must respect:

- compliance requirements;
- audit retention policy;
- billing records;
- legal hold if applicable;
- backup lifecycle.

This is future Cloud（云版） work.

---

## 18. Data Retention

Cloud（云版） should define retention policies for each data category.

Possible default retention examples:

||Data Category|Possible Retention||
|---|---|
||Agent（代理） metadata|while Agent（代理） exists||
||Service metadata|while Service exists||
||Health history|plan-dependent||
||Command history|plan-dependent||
||Audit events|plan-dependent or compliance-dependent||
||Usage records|billing-dependent||
||Deleted objects|soft-delete window||

Final retention policies are future product decisions.

---

## 19. Data Residency

Cloud（云版） may later need data residency options.

Possible requirements:

- region selection;
- EU data residency;
- customer-specific region;
- enterprise dedicated storage;
- regional Agent（代理） Gateway.

This is not a CE（社区版） concern.

---

## 20. Access Control for Cloud（云版） Data

Cloud（云版） data access should be governed by:

- organization membership;
- workspace membership;
- role permissions;
- Agent（代理） token scope;
- service account permissions;
- support access policies.

CE（社区版） v0.1 may use only local admin access.

Cloud（云版） must avoid cross-tenant data exposure.

---

## 21. Support Access Boundary

Cloud（云版） provider support staff may need limited access for troubleshooting.

Future design should define:

- support access approval;
- support access audit;
- time-limited access;
- customer-visible support activity;
- restricted data views;
- no raw secret access by default.

This is a Cloud（云版） operational requirement, not CE（社区版） v0.1.

---

## 22. Data Flow 概述

Recommended data flow:

```text
Customer Capsule Service
    ↓ local providers and handlers
Customer Agent
    ↓ sanitized metadata, status, command results
Opstage Cloud
    ↓ governance storage and UI
Customer Users
```

Secret flow should be different:

```text
Customer Secret Store
    ↓ resolved locally by Agent / Capsule Service
Customer Agent / Service runtime

Cloud stores only secretRef.
```

---

## 23. CE（社区版） Reservations

CE（社区版） should reserve these data-boundary-compatible concepts:

```text
secretRef
sensitive flag
metadataJson
requestJson
resultJson
workspaceId
Agent token hash
registration token hash
sanitized AuditEvent
ConfigItem.sensitive
ConfigItem.type = secretRef
```

CE（社区版） should not implement:

```text
Cloud data export workflow
Cloud data deletion workflow
Cloud retention tiers
Cloud managed secret store
Cloud support access controls
Cloud data residency
Cloud tenant isolation
```

---

## 24. Anti-Patterns

Avoid these patterns.

### 24.1 Cloud（云版） stores raw secrets by default

This damages trust and increases security risk.

### 24.2 CommandResult as data dump

CommandResult should not become a place for large logs or customer business data.

### 24.3 AuditEvent as log platform

AuditEvent should not store full application logs.

### 24.4 Manifest with secrets

Manifest should describe service structure, not carry credentials.

### 24.5 Trusting Agent（代理）-provided tenant fields

Cloud（云版） ownership context must come from authenticated Agent（代理） identity.

### 24.6 Hiding data boundary in documentation

Cloud（云版） must communicate clearly what it stores and what it does not store.

---

## 25. Acceptance Criteria

Cloud（云版） data boundary planning is acceptable when:

- default Cloud（云版） storage is governance metadata, not raw secrets;
- `secretRef` is the primary secret boundary;
- Agent（代理）-local secret resolution is supported conceptually;
- config, command, health, audit, and manifest boundaries are clear;
- customer business data is not stored by default;
- export, deletion, retention, and residency are identified as future Cloud（云版） capabilities;
- CE（社区版） reservations are clear;
- CE（社区版） v0.1 is not required to implement Cloud（云版） data governance workflows.

---

## 26. Summary

Opstage（运维舞台） Cloud（云版） should provide managed governance while keeping customer secrets and business data under customer control by default.

The most important data boundary rule is:

> Cloud（云版） stores what it needs to govern Capsule Services, not everything the Capsule Services know.
