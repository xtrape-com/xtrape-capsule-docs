---
status: draft
audience: founders
stability: unstable
last_reviewed: 2026-05-05
edition: ee
phase: future
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 02-ee-enterprise-security.md
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


# EE（企业版） Enterprise 安全

- Status: Planning
- Edition: EE（企业版）
- Priority: Future
- Audience: architects, security reviewers, enterprise engineers, backend developers, DevOps engineers, AI coding agents

This document 定义 the planned enterprise security model for **Opstage（运维舞台） EE（企业版） / Enterprise 版本**.

Opstage（运维舞台） EE（企业版） is the future private commercial edition of the `xtrape-capsule` product family. Enterprise
security capabilities are not CE（社区版） v0.1 implementation requirements.

---

## 1. Purpose

The purpose of this document is to define:

- the enterprise security goals of EE（企业版）;
- how EE（企业版） extends CE（社区版） security;
- identity and access management direction;
- RBAC and permission boundaries;
- SSO / OIDC / LDAP / SAML direction;
- Agent（代理） security and trust boundaries;
- secret integration principles;
- audit and compliance security capabilities;
- deployment and operational security expectations;
- which security concepts CE（社区版） should reserve without implementing EE（企业版） complexity.

The key rule is:

> EE（企业版） strengthens the CE（社区版） security model for enterprise private deployment, but CE（社区版） v0.1 must remain lightweight and simple.

---

## 2. 安全 Goal

The goal of EE（企业版） security is:

> Provide enterprise-grade access control, identity integration, Agent（代理） trust, secret boundary, auditability, and deployment security for private Opstage（运维舞台） installations.

EE（企业版） should protect:

- human user access;
- service account access;
- Agent（代理） registration and communication;
- Capsule Service（胶囊服务） operation;
- Command creation and execution;
- configuration visibility and change;
- audit data;
- secret references and secret provider integrations;
- enterprise deployment environments.

---

## 3. EE（企业版） 安全 Is Not CE（社区版） v0.1

CE（社区版） v0.1 must not implement full EE（企业版） security capabilities.

Out of scope for CE（社区版） v0.1:

- enterprise RBAC;
- SSO;
- OIDC;
- LDAP;
- SAML;
- SCIM;
- MFA enforcement;
- fine-grained action permissions;
- approval workflows;
- enterprise secret vault integration;
- immutable audit storage;
- SIEM integration;
- support access workflow;
- compliance reporting;
- enterprise license security;
- mTLS and device attestation.

CE（社区版） should only implement the security baseline needed for the MVP:

- local admin login;
- password hashing;
- registration token;
- Agent（代理） token;
- token hash storage;
- Agent（代理） API authentication;
- no arbitrary shell execution;
- sensitive value masking;
- basic AuditEvents.

---

## 4. Relationship with CE（社区版） 安全

CE（社区版） security baseline 提供 the kernel:

```text
Admin login
    ↓
Agent registration token
    ↓
Agent token
    ↓
Agent API authentication
    ↓
Predefined action Command
    ↓
CommandResult
    ↓
AuditEvent
```

EE（企业版） should extend this kernel with enterprise controls:

```text
Enterprise identity
RBAC
Permission scopes
Approval policies
Secret provider integration
Advanced audit
Deployment hardening
Supportability
```

EE（企业版） must not replace the CE（社区版） governance model with an incompatible security model.

---

## 5. Trust Boundaries

EE（企业版） runs in the customer's private environment, but trust boundaries still matter.

Recommended EE（企业版） trust zones:

```text
Browser / User Client
    ↓
Opstage UI / Backend
    ↓
Database / Audit Storage

Enterprise Identity Provider
    ↓
Opstage Auth Integration

Agent
    ↓
Capsule Service

Secret Provider
    ↓
Agent / Capsule Service / Backend integration depending on mode
```

Each boundary must be authenticated and authorized.

---

## 6. Identity and 认证

EE（企业版） should support enterprise identity integration.

### 6.1 Local authentication

EE（企业版） may keep local admin authentication for bootstrap and fallback.

Rules:

- password must be hashed;
- local admin should be clearly marked;
- fallback admin access should be auditable;
- production deployments should be able to disable or restrict local login if enterprise identity is configured.

### 6.2 OIDC

OIDC is likely the first enterprise identity integration candidate.

Possible capabilities:

- configure issuer URL;
- configure client ID and secret;
- map claims to user profile;
- map groups to roles;
- support redirect URI configuration;
- support logout behavior if practical.

### 6.3 LDAP

LDAP may be required by some enterprises.

Possible capabilities:

- LDAP server configuration;
- bind DN and bind password;
- user search base;
- group search base;
- attribute mapping;
- TLS/StartTLS support;
- group-to-role mapping.

### 6.4 SAML

SAML may be required by larger enterprises.

Possible capabilities:

- IdP metadata import;
- SP metadata export;
- assertion validation;
- group/attribute mapping;
- certificate rotation guidance.

### 6.5 SCIM

SCIM may be long-term enterprise work.

Possible capabilities:

- user provisioning;
- user deprovisioning;
- group synchronization;
- lifecycle audit.

SCIM should not be an early EE（企业版） MVP requirement unless demanded by target customers.

---

## 7. User Model

EE（企业版） user model should support both local and external identities.

Possible fields:

```text
id
username
email
displayName
identityProvider
externalSubject
status
lastLoginAt
createdAt
updatedAt
```

User status values:

```text
ACTIVE
DISABLED
LOCKED
PENDING
```

Rules:

- external identity should map to stable user records;
- disabled users cannot access Admin APIs;
- user login and failed login should be audited;
- identity provider changes should be audited.

---

## 8. RBAC Model

EE（企业版） should support role-based access control.

### 8.1 Scope levels

Possible permission scopes:

```text
System
Workspace
Agent
CapsuleService
Action
Audit
Settings
```

### 8.2 Built-in roles

Possible built-in roles:

```text
Owner
Admin
Operator
Viewer
Auditor
SecurityAdmin
```

### 8.3 Permission examples

```text
system.manage
workspace.view
workspace.manage
agent.view
agent.register
agent.disable
agent.revoke
service.view
service.action.execute
service.config.view
service.config.manage
command.view
command.cancel
audit.view
audit.export
settings.security.manage
```

### 8.4 设计 rule

RBAC should be enforced in Backend services and APIs.

UI-only permission hiding is not sufficient.

---

## 9. Permission Boundaries

EE（企业版） should define clear boundaries for sensitive operations.

### 9.1 Agent（代理） operations

Sensitive Agent（代理） operations:

- create registration token;
- register Agent（代理）;
- revoke Agent（代理）;
- disable Agent（代理）;
- rotate Agent（代理） token;
- change Agent（代理） ownership;
- view Agent（代理） diagnostics.

### 9.2 Service operations

Sensitive service operations:

- execute action;
- execute high-risk action;
- change config;
- reload config;
- disable service;
- view sensitive config metadata;
- view command result.

### 9.3 Audit operations

Sensitive audit operations:

- view audit logs;
- export audit logs;
- change retention;
- configure audit sink;
- view security audit details.

### 9.4 安全 settings

Sensitive security settings:

- configure SSO;
- configure LDAP/SAML/OIDC;
- configure role mappings;
- configure secret providers;
- configure support access;
- configure license/security policies.

---

## 10. Workspace 安全

Workspace is the main operational boundary.

EE（企业版） may support multiple Workspaces.

Workspace security may include:

- Workspace-level roles;
- Workspace-level Agent（代理） registration tokens;
- Workspace-level audit view;
- Workspace-level action policies;
- Workspace-level config policies;
- Workspace-level secret provider mapping;
- Workspace-level alert rules.

CE（社区版） v0.1 should only use one default Workspace.

---

## 11. Agent（代理） 安全

Agent（代理） security is central to Opstage（运维舞台）.

### 11.1 Agent（代理） authentication

Agents authenticate using Agent（代理） tokens.

Backend must validate:

- token hash;
- token status;
- expiration;
- Agent（代理） identity;
- disabled/revoked state;
- Agent（代理） ownership of target resources.

### 11.2 Agent（代理） authorization

An Agent（代理） may only:

- heartbeat for itself;
- report services assigned to itself;
- poll Commands assigned to itself;
- report CommandResults for Commands assigned to itself;
- report health/config/action metadata for its own services.

### 11.3 Agent（代理） token rotation

EE（企业版） may support:

- manual token rotation;
- scheduled token rotation;
- forced rotation after incident;
- token expiration policy;
- rotation audit events.

### 11.4 Agent（代理） revocation

EE（企业版） must support Agent（代理） revocation.

Revoked Agents should be rejected from Agent（代理） APIs.

Revocation should create AuditEvents.

### 11.5 Agent（代理） diagnostics

Agent（代理） diagnostics may include:

- last heartbeat;
- last service report;
- last command poll;
- last command result;
- Agent（代理） version;
- SDK version;
- runtime;
- protocol version;
- recent authentication failures.

---

## 12. Registration Token 安全

Registration tokens allow Agent（代理） enrollment and must be protected.

Rules:

- scope registration tokens to Workspace;
- store only token hash;
- show raw token only once;
- support expiration;
- support revocation;
- support one-time use or limited-use tokens;
- audit token creation, use, and revocation;
- rate-limit failed registration attempts.

Possible EE（企业版） enhancements:

- allowed runtime restriction;
- allowed Agent（代理） mode restriction;
- approval-required registration;
- IP allowlist;
- registration policy templates.

---

## 13. Command and Action 安全

Commands and actions are high-value operational paths.

### 13.1 Predefined actions only

EE（企业版） should continue the CE（社区版） principle:

```text
Only predefined actions are allowed by default.
```

Do not introduce arbitrary shell execution as a normal operation model.

### 13.2 Action permission

Action execution should check:

- user permission;
- Workspace access;
- Capsule Service（胶囊服务） access;
- action existence;
- action enabled state;
- danger level;
- approval requirement;
- payload validation;
- operation policy.

### 13.3 高-risk actions

高-risk actions may require:

- confirmation;
- reason input;
- stronger role;
- approval workflow;
- MFA re-check;
- restricted operation window;
- audit reason.

### 13.4 Command ownership

Agent（代理） may only receive and report results for Commands assigned to itself.

Backend must reject cross-Agent（代理） CommandResult reports.

---

## 14. Approval Workflow

Approval workflow is an EE（企业版） candidate capability.

Possible approval use cases:

- execute high-risk action;
- change sensitive config;
- rotate credentials;
- disable Agent（代理）;
- revoke Agent（代理）;
- export audit data.

Possible approval model:

```text
Operation request
    ↓
Approval policy matched
    ↓
Approval task created
    ↓
Authorized approver approves or rejects
    ↓
Command is created or denied
    ↓
AuditEvent records decision
```

Approval workflow should not be required in CE（社区版） v0.1.

---

## 15. Secret Integration 安全

EE（企业版） should integrate with enterprise secret systems without requiring raw secrets to be stored in Opstage（运维舞台） by default.

### 15.1 SecretRef principle

Default model:

```text
Opstage stores secretRef.
Agent or approved runtime resolves secret locally or through enterprise provider.
```

Examples:

```text
vault://secret/path
aws-secretsmanager://region/account/secret-name
azure-keyvault://vault-name/secret-name
agent-local://agent-001/secrets/chatgpt/account-001
```

### 15.2 Secret provider configuration

Secret provider configuration is sensitive.

It should require strong permission and audit.

### 15.3 Secret access audit

Future EE（企业版） may audit:

- secret reference use;
- secret provider access attempt;
- failed secret resolution;
- secret rotation;
- secret provider configuration change.

### 15.4 Raw secret storage

Raw secret storage in Opstage（运维舞台） should not be default.

If EE（企业版） ever 支持 managed secrets, it requires a separate security design.

---

## 16. 配置 安全

EE（企业版） may support config management beyond CE（社区版） visibility.

安全 rules:

- sensitive config values must be masked;
- config changes require permission;
- high-risk config changes may require approval;
- config publishing should be audited;
- config rollback should be audited;
- secret config values should use `secretRef`;
- config apply/reload should go through Commands and Agents.

CE（社区版） v0.1 should not implement config publishing.

---

## 17. Audit 安全

EE（企业版） should provide stronger audit than CE（社区版）.

### 17.1 Required audit categories

Possible audit categories:

```text
identity
authorization
agent
service
command
action
config
secret
deployment
license
support
```

### 17.2 Audit event requirements

AuditEvents should capture:

- actor;
- action;
- resource;
- result;
- timestamp;
- request summary;
- result summary;
- reason if provided;
- approval reference if applicable;
- source IP / user agent where useful.

### 17.3 Audit sanitization

Audit payloads must not contain raw secrets.

Sensitive keys should be redacted:

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

### 17.4 Audit export

Audit export should require explicit permission and should be audited.

---

## 18. Compliance Direction

EE（企业版） may support compliance-oriented features.

Possible capabilities:

- audit retention policy;
- audit export;
- immutable audit sink;
- SIEM integration;
- approval records;
- permission change reports;
- access review reports;
- support access reports;
- configuration change reports.

EE（企业版） should avoid making compliance claims before implementation maturity.

---

## 19. 部署 安全

EE（企业版） private deployment should include security hardening guidance.

Topics:

- HTTPS / TLS setup;
- reverse proxy configuration;
- database credential management;
- secret provider configuration;
- admin bootstrap security;
- backup encryption;
- log redaction;
- network exposure;
- firewall rules;
- container security;
- Kubernetes security if supported;
- upgrade security.

CE（社区版） v0.1 should provide basic deployment security notes only.

---

## 20. Network 安全

EE（企业版） may support stronger network controls.

Possible capabilities:

- HTTPS required in production;
- internal-only deployment;
- IP allowlist;
- mTLS between components;
- reverse proxy guidance;
- private registry images;
- Agent（代理） proxy configuration;
- outbound-only Agent（代理） model;
- optional private network integration.

Inbound access to customer Agents should not be required by default.

---

## 21. Support Access 安全

If EE（企业版） 包括 vendor support workflows, support access must be controlled.

Possible model:

- customer-approved support session;
- time-limited access;
- restricted permission scope;
- support access audit;
- support bundle export;
- no raw secret access by default;
- customer-visible support activity.

Support access should not bypass security boundaries.

---

## 22. License and Entitlement 安全

EE（企业版） may include commercial license or entitlement mechanisms.

Possible capabilities:

- license key;
- offline license file;
- license expiration warning;
- feature entitlement check;
- support contract metadata;
- signed license payload;
- audit of license changes.

License checks should not compromise customer data security or core auditability.

CE（社区版） should not implement license enforcement.

---

## 23. 日志 安全

EE（企业版） logs must avoid raw secrets.

Logs must not contain:

- passwords;
- registration tokens;
- Agent（代理） tokens;
- cookies;
- OAuth tokens;
- API keys;
- private keys;
- raw credentials.

Logs may contain:

- Agent（代理） ID;
- service code;
- command ID;
- audit event ID;
- sanitized error codes;
- status values.

---

## 24. 安全 Operations

EE（企业版） deployments may need security operations guidance.

Possible topics:

- vulnerability patching;
- dependency scanning;
- backup and restore testing;
- access review;
- Agent（代理） token rotation;
- secret provider rotation;
- audit review;
- incident response;
- upgrade planning.

---

## 25. Incident Response

EE（企业版） should support customer incident response.

Possible procedures:

- revoke Agent（代理） tokens;
- rotate registration tokens;
- disable users;
- export audit logs;
- identify affected services;
- identify executed Commands;
- rotate secret references;
- preserve audit records;
- generate support bundle.

This can be documentation first and tooling later.

---

## 26. CE（社区版） Reservations

CE（社区版） should reserve these EE（企业版）-compatible security concepts:

```text
workspaceId
Agent token hash
registration token hash
Agent disabled/revoked state
secretRef
sensitive flag
AuditEvent actor/resource fields
Command ownership by Agent
CapsuleService ownership by Agent
createdBy
actorType
actorId
resourceType
resourceId
status and freshness calculation
```

CE（社区版） should not implement:

```text
RBAC
SSO
OIDC
LDAP
SAML
SCIM
Approval workflow
Enterprise secret provider integration
Compliance audit suite
Support access workflow
Commercial license security
mTLS
Device attestation
```

---

## 27. Anti-Patterns

Avoid these patterns.

### 27.1 UI-only authorization

Backend must enforce permissions.

### 27.2 Raw secrets in Opstage（运维舞台） by default

Use `secretRef` and external secret providers.

### 27.3 Arbitrary shell as enterprise operation

Enterprise operations should still use predefined actions, permissions, approvals, and audit.

### 27.4 Audit logs with secrets

Audit payloads must be sanitized.

### 27.5 Agent（代理） can access other Agents' Commands

Agent（代理） ownership must be enforced by Backend.

### 27.6 SSO without local fallback plan

Enterprise identity failures need a secure bootstrap/fallback strategy.

### 27.7 Pulling EE（企业版） security into CE（社区版） v0.1

CE（社区版） must remain lightweight and focused.

---

## 28. 安全 Acceptance Criteria

EE（企业版） enterprise security planning is acceptable when:

- EE（企业版） extends the CE（社区版） security kernel;
- CE（社区版） v0.1 remains lightweight;
- enterprise identity direction is clear;
- RBAC scope and permission concepts are clear;
- Agent（代理） token and registration token security are clear;
- Command and action security remain predefined and auditable;
- secretRef remains the default secret boundary;
- audit and compliance directions are documented;
- support access is recognized as security-sensitive;
- deployment security is addressed;
- anti-patterns are explicit.

---

## 29. Summary

Opstage（运维舞台） EE（企业版） security should provide enterprise-grade controls without breaking the Capsule governance model.

The most important enterprise security rule is:

> EE（企业版） should strengthen identity, authorization, audit, secret boundaries, and deployment hardening while preserving the Agent（代理）-based governance kernel.
