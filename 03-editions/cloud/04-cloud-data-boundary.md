---
status: proposed
audience: founders
stability: evolving
last_reviewed: 2026-05-05
edition: cloud
phase: future
---

# Cloud Data Boundary

- Status: Planning
- Edition: Cloud
- Priority: Future
- Audience: founders, product designers, architects, cloud engineers, backend developers, security reviewers, AI coding agents

This document defines the planned data boundary for **Opstage Cloud**.

Opstage Cloud is the future hosted SaaS edition of the `xtrape-capsule` product family. Cloud data boundary design is a
future capability and is not a CE v0.1 implementation requirement.

---

## 1. Purpose

The purpose of this document is to define:

- what data Opstage Cloud may store;
- what data should remain customer-controlled;
- how sensitive data should be represented;
- how `secretRef` should be used;
- how Agents should avoid leaking secrets;
- how audit, command, config, and health data should be bounded;
- what export, deletion, and retention capabilities Cloud may need;
- what CE should reserve without implementing Cloud complexity.

The key rule is:

> Cloud should store governance metadata and secret references by default, not raw customer operational secrets.

---

## 2. Boundary Statement

Opstage Cloud should provide hosted governance for Capsule Services while respecting customer data ownership.

Recommended boundary:

```text
Cloud stores:      governance metadata, status, health, commands, results, audit, usage metadata
Customer stores:   raw credentials, account secrets, cookies, private keys, local runtime data
Cloud may store:   optional managed secrets only if explicitly enabled in a future plan
```

This boundary should be clear in product messaging, security documentation, APIs, UI, and Agent SDK behavior.

---

## 3. Data Classification

Cloud data can be classified into several categories.

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

## 4. Data Cloud May Store by Default

Cloud may store the following data by default.

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

These are Cloud-only concepts and not CE v0.1 requirements.

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

Cloud should not store raw passwords. Passwords, if used, must be hashed.

### 4.3 Agent metadata

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

Agent metadata is governance metadata.

### 4.4 Capsule Service metadata

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

Cloud may store full manifests, but manifests must not include raw secrets.

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

Cloud should not store raw sensitive config values by default.

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

These are Cloud-only capabilities.

---

## 5. Data Cloud Should Not Store by Default

Cloud should not store the following by default:

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

If Cloud later supports optional managed secrets, that must be a separate explicit capability with clear security design.

---

## 6. SecretRef Boundary

`secretRef` is the primary data boundary mechanism.

A `secretRef` points to a secret without exposing its raw value to Cloud.

Examples:

```text
agent-local://agent-001/secrets/chatgpt/account-001
customer-vault://prod/integration-worker/account-001
aws-secretsmanager://region/account/secret-name
azure-keyvault://vault-name/secret-name
cloud-secret://org/workspace/secret-key
```

### 6.1 CE-compatible behavior

CE v0.1 should only need to:

- recognize `secretRef` as a value type;
- display it safely;
- preserve it in metadata;
- avoid resolving it.

### 6.2 Cloud behavior

Cloud should initially:

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

## 7. Agent-Local Secret Boundary

For many Capsule Services, the safest default is Agent-local secret handling.

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

Cloud does not see the actual credential.

---

## 8. Config Data Boundary

Config metadata is useful for governance, but config values can be sensitive.

### 8.1 Safe config data

Cloud may store:

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

If `sensitive = true`, Cloud should store:

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

Cloud may store:

```text
HealthStatus
message
dependency status
timing metadata
sanitized error code
```

Cloud should avoid storing:

```text
raw tokens
credentials
cookies
full request payloads
private customer records
full stack traces with secrets
```

Health provider errors should be sanitized before sending to Cloud.

---

## 11. Audit Data Boundary

Audit data is important and sensitive.

Cloud may store:

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

Cloud should not store raw secrets in audit events.

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

Cloud may provide retention tiers in future plans.

Examples:

```text
7 days
30 days
90 days
1 year
custom enterprise retention
```

CE v0.1 does not need retention tiers.

---

## 12. Manifest Data Boundary

Manifest describes service metadata.

Cloud may store manifest fields such as:

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

Cloud may later provide managed observability, but should not automatically collect arbitrary logs, metrics, or traces in early versions.

### 13.1 Logs

Large application logs should not be stored in CommandResult or AuditEvent.

If Cloud later supports logs, it should define:

- log collection scope;
- retention;
- filtering;
- sensitive data redaction;
- access control;
- pricing impact.

### 13.2 Metrics

Cloud may store governance metrics such as:

```text
heartbeat count
command count
failure count
Agent online duration
service stale duration
```

These are different from arbitrary application metrics.

### 13.3 Traces

Distributed tracing is not part of Cloud initial governance boundary.

---

## 14. Customer Business Data Boundary

Cloud should not become a default store for customer business data.

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

Cloud may store summaries or references only when required for governance.

---

## 15. Optional Managed Secrets

Future Cloud may offer optional managed secrets.

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

Managed secrets should not be required for basic Cloud governance.

---

## 16. Data Export

Cloud should eventually support customer data export.

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

CE v0.1 does not need Cloud export workflows.

---

## 17. Data Deletion

Cloud should eventually support data deletion controls.

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

This is future Cloud work.

---

## 18. Data Retention

Cloud should define retention policies for each data category.

Possible default retention examples:

| Data Category | Possible Retention |
|---|---|
| Agent metadata | while Agent exists |
| Service metadata | while Service exists |
| Health history | plan-dependent |
| Command history | plan-dependent |
| Audit events | plan-dependent or compliance-dependent |
| Usage records | billing-dependent |
| Deleted objects | soft-delete window |

Final retention policies are future product decisions.

---

## 19. Data Residency

Cloud may later need data residency options.

Possible requirements:

- region selection;
- EU data residency;
- customer-specific region;
- enterprise dedicated storage;
- regional Agent Gateway.

This is not a CE concern.

---

## 20. Access Control for Cloud Data

Cloud data access should be governed by:

- organization membership;
- workspace membership;
- role permissions;
- Agent token scope;
- service account permissions;
- support access policies.

CE v0.1 may use only local admin access.

Cloud must avoid cross-tenant data exposure.

---

## 21. Support Access Boundary

Cloud provider support staff may need limited access for troubleshooting.

Future design should define:

- support access approval;
- support access audit;
- time-limited access;
- customer-visible support activity;
- restricted data views;
- no raw secret access by default.

This is a Cloud operational requirement, not CE v0.1.

---

## 22. Data Flow Overview

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

## 23. CE Reservations

CE should reserve these data-boundary-compatible concepts:

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

CE should not implement:

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

### 24.1 Cloud stores raw secrets by default

This damages trust and increases security risk.

### 24.2 CommandResult as data dump

CommandResult should not become a place for large logs or customer business data.

### 24.3 AuditEvent as log platform

AuditEvent should not store full application logs.

### 24.4 Manifest with secrets

Manifest should describe service structure, not carry credentials.

### 24.5 Trusting Agent-provided tenant fields

Cloud ownership context must come from authenticated Agent identity.

### 24.6 Hiding data boundary in documentation

Cloud must communicate clearly what it stores and what it does not store.

---

## 25. Acceptance Criteria

Cloud data boundary planning is acceptable when:

- default Cloud storage is governance metadata, not raw secrets;
- `secretRef` is the primary secret boundary;
- Agent-local secret resolution is supported conceptually;
- config, command, health, audit, and manifest boundaries are clear;
- customer business data is not stored by default;
- export, deletion, retention, and residency are identified as future Cloud capabilities;
- CE reservations are clear;
- CE v0.1 is not required to implement Cloud data governance workflows.

---

## 26. Summary

Opstage Cloud should provide managed governance while keeping customer secrets and business data under customer control by default.

The most important data boundary rule is:

> Cloud stores what it needs to govern Capsule Services, not everything the Capsule Services know.
