
# EE Enterprise Security

- Status: Planning
- Edition: EE
- Priority: Future
- Audience: architects, security reviewers, enterprise engineers, backend developers, DevOps engineers, AI coding agents

This document defines the planned enterprise security model for **Opstage EE / Enterprise Edition**.

Opstage EE is the future private commercial edition of the `xtrape-capsule` product family. Enterprise security capabilities are not CE v0.1 implementation requirements.

---

## 1. Purpose

The purpose of this document is to define:

- the enterprise security goals of EE;
- how EE extends CE security;
- identity and access management direction;
- RBAC and permission boundaries;
- SSO / OIDC / LDAP / SAML direction;
- Agent security and trust boundaries;
- secret integration principles;
- audit and compliance security capabilities;
- deployment and operational security expectations;
- which security concepts CE should reserve without implementing EE complexity.

The key rule is:

> EE strengthens the CE security model for enterprise private deployment, but CE v0.1 must remain lightweight and simple.

---

## 2. Security Goal

The goal of EE security is:

> Provide enterprise-grade access control, identity integration, Agent trust, secret boundary, auditability, and deployment security for private Opstage installations.

EE should protect:

- human user access;
- service account access;
- Agent registration and communication;
- Capsule Service operation;
- Command creation and execution;
- configuration visibility and change;
- audit data;
- secret references and secret provider integrations;
- enterprise deployment environments.

---

## 3. EE Security Is Not CE v0.1

CE v0.1 must not implement full EE security capabilities.

Out of scope for CE v0.1:

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

CE should only implement the security baseline needed for the MVP:

- local admin login;
- password hashing;
- registration token;
- Agent token;
- token hash storage;
- Agent API authentication;
- no arbitrary shell execution;
- sensitive value masking;
- basic AuditEvents.

---

## 4. Relationship with CE Security

CE security baseline provides the kernel:

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

EE should extend this kernel with enterprise controls:

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

EE must not replace the CE governance model with an incompatible security model.

---

## 5. Trust Boundaries

EE runs in the customer's private environment, but trust boundaries still matter.

Recommended EE trust zones:

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

## 6. Identity and Authentication

EE should support enterprise identity integration.

### 6.1 Local authentication

EE may keep local admin authentication for bootstrap and fallback.

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

SCIM should not be an early EE MVP requirement unless demanded by target customers.

---

## 7. User Model

EE user model should support both local and external identities.

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

EE should support role-based access control.

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

### 8.4 Design rule

RBAC should be enforced in Backend services and APIs.

UI-only permission hiding is not sufficient.

---

## 9. Permission Boundaries

EE should define clear boundaries for sensitive operations.

### 9.1 Agent operations

Sensitive Agent operations:

- create registration token;
- register Agent;
- revoke Agent;
- disable Agent;
- rotate Agent token;
- change Agent ownership;
- view Agent diagnostics.

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

### 9.4 Security settings

Sensitive security settings:

- configure SSO;
- configure LDAP/SAML/OIDC;
- configure role mappings;
- configure secret providers;
- configure support access;
- configure license/security policies.

---

## 10. Workspace Security

Workspace is the main operational boundary.

EE may support multiple Workspaces.

Workspace security may include:

- Workspace-level roles;
- Workspace-level Agent registration tokens;
- Workspace-level audit view;
- Workspace-level action policies;
- Workspace-level config policies;
- Workspace-level secret provider mapping;
- Workspace-level alert rules.

CE v0.1 should only use one default Workspace.

---

## 11. Agent Security

Agent security is central to Opstage.

### 11.1 Agent authentication

Agents authenticate using Agent tokens.

Backend must validate:

- token hash;
- token status;
- expiration;
- Agent identity;
- disabled/revoked state;
- Agent ownership of target resources.

### 11.2 Agent authorization

An Agent may only:

- heartbeat for itself;
- report services assigned to itself;
- poll Commands assigned to itself;
- report CommandResults for Commands assigned to itself;
- report health/config/action metadata for its own services.

### 11.3 Agent token rotation

EE may support:

- manual token rotation;
- scheduled token rotation;
- forced rotation after incident;
- token expiration policy;
- rotation audit events.

### 11.4 Agent revocation

EE must support Agent revocation.

Revoked Agents should be rejected from Agent APIs.

Revocation should create AuditEvents.

### 11.5 Agent diagnostics

Agent diagnostics may include:

- last heartbeat;
- last service report;
- last command poll;
- last command result;
- Agent version;
- SDK version;
- runtime;
- protocol version;
- recent authentication failures.

---

## 12. Registration Token Security

Registration tokens allow Agent enrollment and must be protected.

Rules:

- scope registration tokens to Workspace;
- store only token hash;
- show raw token only once;
- support expiration;
- support revocation;
- support one-time use or limited-use tokens;
- audit token creation, use, and revocation;
- rate-limit failed registration attempts.

Possible EE enhancements:

- allowed runtime restriction;
- allowed Agent mode restriction;
- approval-required registration;
- IP allowlist;
- registration policy templates.

---

## 13. Command and Action Security

Commands and actions are high-value operational paths.

### 13.1 Predefined actions only

EE should continue the CE principle:

```text
Only predefined actions are allowed by default.
```

Do not introduce arbitrary shell execution as a normal operation model.

### 13.2 Action permission

Action execution should check:

- user permission;
- Workspace access;
- Capsule Service access;
- action existence;
- action enabled state;
- danger level;
- approval requirement;
- payload validation;
- operation policy.

### 13.3 High-risk actions

High-risk actions may require:

- confirmation;
- reason input;
- stronger role;
- approval workflow;
- MFA re-check;
- restricted operation window;
- audit reason.

### 13.4 Command ownership

Agent may only receive and report results for Commands assigned to itself.

Backend must reject cross-Agent CommandResult reports.

---

## 14. Approval Workflow

Approval workflow is an EE candidate capability.

Possible approval use cases:

- execute high-risk action;
- change sensitive config;
- rotate credentials;
- disable Agent;
- revoke Agent;
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

Approval workflow should not be required in CE v0.1.

---

## 15. Secret Integration Security

EE should integrate with enterprise secret systems without requiring raw secrets to be stored in Opstage by default.

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

Future EE may audit:

- secret reference use;
- secret provider access attempt;
- failed secret resolution;
- secret rotation;
- secret provider configuration change.

### 15.4 Raw secret storage

Raw secret storage in Opstage should not be default.

If EE ever supports managed secrets, it requires a separate security design.

---

## 16. Configuration Security

EE may support config management beyond CE visibility.

Security rules:

- sensitive config values must be masked;
- config changes require permission;
- high-risk config changes may require approval;
- config publishing should be audited;
- config rollback should be audited;
- secret config values should use `secretRef`;
- config apply/reload should go through Commands and Agents.

CE v0.1 should not implement config publishing.

---

## 17. Audit Security

EE should provide stronger audit than CE.

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

EE may support compliance-oriented features.

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

EE should avoid making compliance claims before implementation maturity.

---

## 19. Deployment Security

EE private deployment should include security hardening guidance.

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

CE v0.1 should provide basic deployment security notes only.

---

## 20. Network Security

EE may support stronger network controls.

Possible capabilities:

- HTTPS required in production;
- internal-only deployment;
- IP allowlist;
- mTLS between components;
- reverse proxy guidance;
- private registry images;
- Agent proxy configuration;
- outbound-only Agent model;
- optional private network integration.

Inbound access to customer Agents should not be required by default.

---

## 21. Support Access Security

If EE includes vendor support workflows, support access must be controlled.

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

## 22. License and Entitlement Security

EE may include commercial license or entitlement mechanisms.

Possible capabilities:

- license key;
- offline license file;
- license expiration warning;
- feature entitlement check;
- support contract metadata;
- signed license payload;
- audit of license changes.

License checks should not compromise customer data security or core auditability.

CE should not implement license enforcement.

---

## 23. Logging Security

EE logs must avoid raw secrets.

Logs must not contain:

- passwords;
- registration tokens;
- Agent tokens;
- cookies;
- OAuth tokens;
- API keys;
- private keys;
- raw credentials.

Logs may contain:

- Agent ID;
- service code;
- command ID;
- audit event ID;
- sanitized error codes;
- status values.

---

## 24. Security Operations

EE deployments may need security operations guidance.

Possible topics:

- vulnerability patching;
- dependency scanning;
- backup and restore testing;
- access review;
- Agent token rotation;
- secret provider rotation;
- audit review;
- incident response;
- upgrade planning.

---

## 25. Incident Response

EE should support customer incident response.

Possible procedures:

- revoke Agent tokens;
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

## 26. CE Reservations

CE should reserve these EE-compatible security concepts:

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

CE should not implement:

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

### 27.2 Raw secrets in Opstage by default

Use `secretRef` and external secret providers.

### 27.3 Arbitrary shell as enterprise operation

Enterprise operations should still use predefined actions, permissions, approvals, and audit.

### 27.4 Audit logs with secrets

Audit payloads must be sanitized.

### 27.5 Agent can access other Agents' Commands

Agent ownership must be enforced by Backend.

### 27.6 SSO without local fallback plan

Enterprise identity failures need a secure bootstrap/fallback strategy.

### 27.7 Pulling EE security into CE v0.1

CE must remain lightweight and focused.

---

## 28. Security Acceptance Criteria

EE enterprise security planning is acceptable when:

- EE extends the CE security kernel;
- CE v0.1 remains lightweight;
- enterprise identity direction is clear;
- RBAC scope and permission concepts are clear;
- Agent token and registration token security are clear;
- Command and action security remain predefined and auditable;
- secretRef remains the default secret boundary;
- audit and compliance directions are documented;
- support access is recognized as security-sensitive;
- deployment security is addressed;
- anti-patterns are explicit.

---

## 29. Summary

Opstage EE security should provide enterprise-grade controls without breaking the Capsule governance model.

The most important enterprise security rule is:

> EE should strengthen identity, authorization, audit, secret boundaries, and deployment hardening while preserving the Agent-based governance kernel.
