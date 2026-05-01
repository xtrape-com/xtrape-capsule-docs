<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 06-ee-secret-and-compliance.md
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

# EE（企业版） Secret and Compliance

- Status: Planning
- Edition: EE（企业版）
- Priority: Future
- Audience: architects, security reviewers, compliance stakeholders, backend developers, platform engineers, DevOps engineers, AI coding agents

This document 定义 the planned secret management and compliance direction for **Opstage（运维舞台） EE（企业版） / Enterprise 版本**.

Opstage（运维舞台） EE（企业版） is the future private commercial edition of the `xtrape-capsule` product family. Secret management and compliance capabilities are not CE（社区版） v0.1 implementation requirements.

---

## 1. Purpose

The purpose of this document is to define:

- how EE（企业版） should handle secrets safely;
- how `secretRef` should work as the default boundary;
- how enterprise secret providers may be integrated;
- how secret access should be audited;
- how compliance-oriented audit and retention may evolve;
- how data export, deletion, and retention should be planned;
- how support access and compliance reporting should be handled;
- which secret and compliance concepts CE（社区版） should reserve without implementing EE（企业版） complexity.

The key rule is:

> EE（企业版） should integrate with enterprise secret and compliance systems without making Opstage（运维舞台） the default raw secret store.

---

## 2. Scope

This document 涵盖 two related areas:

```text
Secret management
Compliance-oriented governance
```

These areas are related because both depend on:

- data boundary;
- access control;
- auditability;
- retention;
- export;
- supportability;
- customer trust.

This document does not define a full legal compliance program. It 定义 product and architecture direction.

---

## 3. EE（企业版） Secret and Compliance Is Not CE（社区版） v0.1

CE（社区版） v0.1 must not implement full EE（企业版） secret or compliance capabilities.

Out of scope for CE（社区版） v0.1:

- enterprise Secret Vault integration;
- managed secret store;
- secret rotation workflow;
- secret access audit;
- compliance report generator;
- immutable audit storage;
- SIEM integration;
- audit signing;
- audit export workflow;
- data retention policy engine;
- legal hold;
- support access approval workflow;
- data residency controls;
- DPA / compliance documentation automation.

CE（社区版） v0.1 should only implement:

- `secretRef` recognition;
- sensitive config masking;
- no raw token storage;
- basic AuditEvents;
- audit payload sanitization;
- no arbitrary shell execution.

---

## 4. Relationship with CE（社区版）

CE（社区版） 提供 the safety kernel:

```text
Sensitive flag
    ↓
secretRef
    ↓
Token hash storage
    ↓
Sanitized payloads
    ↓
Basic AuditEvents
```

EE（企业版） should extend this kernel with:

```text
Enterprise secret provider integrations
SecretRef validation
Secret access audit
Secret rotation workflows
Compliance audit retention
Audit export
Compliance-oriented reports
Support access audit
```

EE（企业版） must preserve CE（社区版）'s simple and safe data boundary.

---

## 5. Secret Boundary Principle

The default secret boundary should be:

```text
Opstage stores secretRef.
Agent or customer-controlled runtime resolves the raw secret.
```

This means Opstage（运维舞台） EE（企业版） should not become a raw secret database by default.

Recommended principle:

> Opstage（运维舞台） governs secret usage by reference and audit, while raw secrets remain in customer-controlled secret systems whenever possible.

---

## 6. Secret Data Classification

Secret-related data can be classified as:

```text
Raw secret
Secret reference
Secret metadata
Secret provider configuration
Secret access event
Secret rotation event
Secret policy
```

### 6.1 Raw secret

Examples:

```text
password
API key
OAuth access token
OAuth refresh token
cookie
private key
account credential
session credential
```

Raw secrets should not be stored in Opstage（运维舞台） by default.

### 6.2 Secret reference

A reference to a secret stored elsewhere.

Examples:

```text
agent-local://agent-001/secrets/chatgpt/account-001
vault://secret/data/capi/chatgpt/account-001
aws-secretsmanager://eu-west-1/account/secret-name
azure-keyvault://vault-name/secret-name
k8s-secret://namespace/name/key
```

### 6.3 Secret metadata

Metadata about a secret without its raw value.

Examples:

```text
name
label
type
provider
last rotated time
owner
usage scope
sensitive flag
```

### 6.4 Secret provider configuration

配置 that allows Opstage（运维舞台） or Agent（代理） to talk to a provider.

This configuration is sensitive and requires strong permission.

---

## 7. SecretRef Model

`secretRef` is the primary abstraction.

### 7.1 Required properties

A secretRef should be:

- stable enough to store in config metadata;
- safe enough to display in masked or partial form;
- resolvable by an authorized runtime;
- provider-specific but parseable;
- auditable when used in sensitive operations.

### 7.2 Recommended examples

```text
agent-local://agent-001/secrets/chatgpt/account-001
vault://kv/capi/chatgpt/account-001
aws-secretsmanager://eu-west-1/123456789012/chatgpt-account-001
azure-keyvault://corp-vault/chatgpt-account-001
k8s-secret://prod/capi-chatgpt/account-001
```

### 7.3 UI display

UI should display secretRef safely.

Possible displays:

```text
secretRef: vault://kv/capi/chatgpt/account-001
```

or:

```text
secretRef: vault://.../account-001
```

UI should not show raw secret values.

---

## 8. Secret Provider Integration

EE（企业版） may integrate with enterprise secret providers.

Possible providers:

```text
HashiCorp Vault
AWS Secrets Manager
Azure Key Vault
Google Secret Manager
Kubernetes Secrets
CyberArk
1Password Business
enterprise internal secret service
```

Provider integration should be added based on real customer demand.

---

## 9. Provider Integration Modes

EE（企业版） may support different integration modes.

### 9.1 Agent（代理）-side resolution

Agent（代理） resolves secrets directly in the customer environment.

```text
Opstage Backend stores secretRef
    ↓
Command contains secretRef
    ↓
Agent resolves secretRef locally
    ↓
Capsule Service uses raw secret locally
```

This is the preferred default.

### 9.2 Backend-side validation only

Backend validates that a secretRef format or provider mapping exists, but does not read raw secret.

Useful for governance without raw secret access.

### 9.3 Backend-side resolution

Backend resolves raw secret from provider.

This should be optional and requires stronger security design.

Use only when there is a clear enterprise need.

### 9.4 Managed Opstage（运维舞台） secret store

Opstage（运维舞台） stores encrypted secrets.

This is the highest-risk mode and should not be early EE（企业版） default.

It requires separate design for encryption, key management, access control, audit, backup, and deletion.

---

## 10. Agent（代理）-Side Secret Resolution

Agent（代理）-side resolution is the recommended primary model.

Advantages:

- raw secrets stay in customer environment;
- Opstage（运维舞台） Backend does not need broad secret access;
- 支持 private networks;
- aligns with outbound Agent（代理） model;
- reduces compliance burden.

Requirements:

- Agent（代理） understands provider-specific secretRef;
- Agent（代理） has local permission to resolve secret;
- secret access is auditable if possible;
- Agent（代理） does not log raw secret;
- CommandResult does not return raw secret.

---

## 11. Secret Provider 配置 安全

Secret provider configuration is sensitive.

Examples:

```text
Vault address
Vault role ID
Vault token reference
AWS role ARN
Azure Key Vault tenant/client settings
Kubernetes service account binding
```

Rules:

- require strong permission to configure;
- audit configuration changes;
- avoid storing raw provider credentials where possible;
- use environment or deployment secret mechanisms;
- validate configuration without exposing secret values;
- document security assumptions.

---

## 12. Secret Access Audit

EE（企业版） may audit secret-related events.

Possible events:

```text
secretRef.created
secretRef.updated
secretRef.used
secretRef.validation.failed
secretProvider.configured
secretProvider.updated
secretProvider.deleted
secret.rotation.requested
secret.rotation.completed
secret.rotation.failed
```

Audit records should include:

- actor;
- action;
- resource;
- secretRef or masked secret identifier;
- provider type;
- result;
- timestamp;
- reason if provided.

Audit records must not include raw secrets.

---

## 13. Secret Rotation

EE（企业版） may support secret rotation workflows in the future.

Possible rotation model:

```text
Rotation request
    ↓
Approval if required
    ↓
Agent or provider rotates secret
    ↓
Capsule Service reloads or refreshes usage
    ↓
Health check verifies success
    ↓
AuditEvent records result
```

Potential rotation capabilities:

- manual rotation request;
- scheduled rotation reminder;
- provider-triggered rotation;
- post-rotation validation;
- rollback guidance;
- failure audit.

Secret rotation is not CE（社区版） v0.1.

---

## 14. Secrets in Configs

Configs may refer to secrets.

Rules:

- sensitive config values must be masked;
- secret config values should use `type = secretRef`;
- config UI should not display raw values;
- config export should not include raw secrets;
- config changes involving secretRef should be audited;
- config publishing should go through Commands and Agents if implemented.

Bad example:

```json
{
  "key": "account.password",
  "value": "plain-password",
  "sensitive": true
}
```

Good example:

```json
{
  "key": "account.secret",
  "value": "vault://kv/capi/chatgpt/account-001",
  "type": "secretRef",
  "sensitive": true
}
```

---

## 15. Secrets in Commands

Commands may need to reference secrets.

Rules:

- use secretRef instead of raw secret;
- validate user permission before creating command;
- validate Agent（代理）/service ownership;
- avoid logging command payload raw if it may include sensitive data;
- sanitize AuditEvent requestJson;
- sanitize CommandResult.

Bad example:

```json
{
  "password": "plain-password"
}
```

Good example:

```json
{
  "accountSecretRef": "vault://kv/capi/chatgpt/account-001"
}
```

---

## 16. Secrets in Health and Logs

Health reports and logs must not contain raw secrets.

Health should include:

```text
status
message
sanitized error code
dependency state
checkedAt
```

Health should not include:

```text
raw token
raw cookie
raw credential
OAuth code
private key
full secret-bearing request
```

Logs should also avoid raw secrets.

---

## 17. Compliance Direction

EE（企业版） compliance features should be based on governance traceability, not unsupported legal claims.

Potential compliance-oriented capabilities:

- audit retention;
- audit export;
- permission change history;
- action execution history;
- approval records;
- secret reference usage records;
- support access records;
- data export;
- data deletion support;
- configuration change history;
- incident response support.

EE（企业版） should avoid claiming certifications before the product and operational process support them.

---

## 18. Audit Retention

EE（企业版） may support configurable audit retention.

Possible retention policies:

```text
30 days
90 days
180 days
1 year
custom enterprise retention
```

Retention may be configured by:

- system;
- workspace;
- event category;
- compliance policy.

Retention changes should be audited.

---

## 19. Audit Export

EE（企业版） may support audit export.

Possible formats:

```text
CSV
JSON
NDJSON
ZIP bundle
```

Possible filters:

```text
time range
actor
action
resource type
resource ID
workspace
result
category
```

Rules:

- audit export requires permission;
- audit export itself must be audited;
- exported payloads must be sanitized;
- export files may require expiration;
- large exports should run as background jobs.

---

## 20. Immutable Audit Storage

Future EE（企业版） may support immutable audit storage.

Possible approaches:

- append-only audit table;
- external audit sink;
- object storage with retention lock;
- signed audit records;
- hash chain;
- SIEM export.

This is long-term work and should not be promised before implementation is mature.

---

## 21. Compliance Reports

EE（企业版） may provide compliance-oriented reports.

Possible reports:

- user access report;
- role and permission report;
- Agent（代理） registration and revocation report;
- high-risk action report;
- command execution report;
- secret reference usage report;
- configuration change report;
- audit export report;
- support access report.

Reports should be generated from AuditEvents and related durable records.

---

## 22. Support Access Compliance

If vendor support access is provided, it must be controlled.

Possible model:

```text
Customer requests support
    ↓
Support access approved
    ↓
Time-limited support session
    ↓
Support actions audited
    ↓
Support access expires
```

Rules:

- no raw secret access by default;
- support access should be visible to customer;
- support access should be time-limited;
- support actions should be audited;
- support bundle export should be sanitized.

---

## 23. Data Export

EE（企业版） may support data export for governance data.

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

Export should not include raw secrets.

SecretRefs may be included if safe and required.

---

## 24. Data Deletion

EE（企业版） may support deletion or cleanup workflows.

Possible deletion scopes:

- Agent（代理） removal;
- Capsule Service（胶囊服务） removal;
- old HealthReports;
- old Commands;
- old AuditEvents after retention;
- workspace cleanup;
- user deactivation.

Deletion must respect audit and compliance policies.

Some records may require retention even after logical deletion.

---

## 25. Data Residency

Some enterprise customers may require data residency.

For EE（企业版） private deployment, data residency is usually customer-controlled because Opstage（运维舞台） runs in the customer's environment.

EE（企业版） documentation should clarify:

- where data is stored;
- database location;
- object storage location;
- backup location;
- log storage location;
- secret provider location.

Cloud（云版） data residency is a separate Cloud（云版） concern.

---

## 26. SIEM and External Audit Integrations

EE（企业版） may integrate with SIEM or external audit systems.

Possible integrations:

```text
Splunk
Elastic / OpenSearch
QRadar
Microsoft Sentinel
generic webhook
syslog
Kafka
S3-compatible export
```

Integration should be added based on enterprise demand.

Initial EE（企业版） may start with audit export before real-time SIEM streaming.

---

## 27. 安全 and Compliance 文档

EE（企业版） should provide documentation for security reviewers.

Possible docs:

- security architecture overview;
- data boundary document;
- secret handling guide;
- audit model guide;
- deployment hardening guide;
- backup and restore guide;
- support access guide;
- incident response guide;
- compliance feature matrix.

These documents can reduce sales and onboarding friction.

---

## 28. Incident Response Support

EE（企业版） may support incident response workflows.

Possible procedures:

- revoke Agent（代理） tokens;
- rotate registration tokens;
- disable users;
- export audit logs;
- identify affected services;
- identify executed Commands;
- review high-risk actions;
- rotate secret references;
- generate support bundle;
- preserve audit records.

Incident response can start as documentation and later become UI tooling.

---

## 29. License and Compliance Boundary

Commercial license enforcement should not interfere with compliance record integrity.

Rules:

- license expiration should not delete audit records;
- license expiration should not hide existing audit data completely;
- license state changes should be audited;
- support entitlement checks should not expose secrets;
- compliance export behavior under expired license must be defined carefully.

CE（社区版） should not include license enforcement.

---

## 30. EE（企业版） Secret and Compliance MVP Candidate

A future EE（企业版） MVP may include:

- secretRef validation;
- Vault-style secretRef documentation;
- sensitive config masking;
- audit retention configuration;
- audit export;
- permission change audit;
- Agent（代理） token revocation audit;
- high-risk action audit reason;
- support bundle export;
- security hardening guide;
- compliance feature matrix.

This is a candidate only and should be validated by real enterprise demand.

---

## 31. Long-Term Capabilities

Long-term EE（企业版） may include:

- HashiCorp Vault integration;
- AWS/Azure/GCP secret manager integrations;
- secret rotation workflows;
- secret access audit;
- immutable audit storage;
- signed audit records;
- SIEM streaming;
- compliance reports;
- support access workflow;
- data retention policy engine;
- legal hold;
- advanced incident response tooling;
- managed encrypted Opstage（运维舞台） secret store if explicitly needed.

These should not be implemented before the secretRef and audit model are stable.

---

## 32. CE（社区版） Reservations

CE（社区版） should reserve these secret and compliance compatible concepts:

```text
secretRef
sensitive flag
ConfigItem.sensitive
ConfigItem.valueType = secretRef
Agent token hash
registration token hash
AuditEvent
AuditEvent.actorType
AuditEvent.actorId
AuditEvent.resourceType
AuditEvent.resourceId
AuditEvent.requestJson
AuditEvent.resultJson
Command
CommandResult
metadataJson
```

CE（社区版） should not implement:

```text
Secret Vault integration
managed secret store
secret rotation workflow
secret access audit
immutable audit storage
SIEM integration
compliance report generator
audit export workflow
retention policy engine
support access workflow
legal hold
```

---

## 33. Anti-Patterns

Avoid these patterns.

### 33.1 Opstage（运维舞台） as raw secret store by default

This increases risk and compliance burden.

### 33.2 Raw secrets in audit logs

Audit payloads must be sanitized.

### 33.3 Raw secrets in CommandResult

CommandResult must not leak credentials.

### 33.4 Compliance claims before implementation

Do not claim compliance features before real controls exist.

### 33.5 Secret provider configuration without audit

Provider settings are sensitive and must be auditable.

### 33.6 Support access without customer visibility

Support access must be controlled and auditable.

### 33.7 Pulling EE（企业版） compliance into CE（社区版） v0.1

CE（社区版） should remain lightweight.

---

## 34. Acceptance Criteria

EE（企业版） secret and compliance planning is acceptable when:

- secretRef is the default secret boundary;
- raw secret storage is not the default;
- Agent（代理）-side resolution is the preferred model;
- enterprise secret provider integration paths are clear;
- secret access and provider configuration audit are planned;
- audit retention and export are defined as EE（企业版） capabilities;
- compliance reporting is framed carefully;
- support access compliance is recognized;
- CE（社区版） reservations are clear;
- CE（社区版） v0.1 remains lightweight.

---

## 35. Summary

Opstage（运维舞台） EE（企业版） should provide enterprise secret and compliance capabilities by governing references, access, audit, retention, and export rather than becoming a raw secret vault by default.

The most important secret and compliance rule is:

> Keep raw secrets in customer-controlled systems by default, and make Opstage（运维舞台） responsible for safe references, auditable operations, and compliance-oriented governance records.
