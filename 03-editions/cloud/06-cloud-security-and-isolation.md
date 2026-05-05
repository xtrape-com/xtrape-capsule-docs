---
status: proposed
audience: founders
stability: evolving
last_reviewed: 2026-05-05
edition: cloud
phase: future
---

# Cloud Security and Isolation

- Status: Planning
- Edition: Cloud
- Priority: Future
- Audience: founders, architects, cloud engineers, backend developers, security reviewers, AI coding agents

This document defines the planned security and isolation model for **Opstage Cloud**.

Opstage Cloud is the future hosted SaaS edition of the `xtrape-capsule` product family. Cloud security and isolation are
future planning concerns and are not CE v0.1 implementation requirements.

---

## 1. Purpose

The purpose of this document is to define:

- the Cloud security goals;
- the Cloud trust boundaries;
- tenant and workspace isolation principles;
- identity and access control direction;
- Agent trust and authentication rules;
- data isolation and data boundary rules;
- secret handling principles;
- audit and compliance security direction;
- abuse prevention and rate limiting;
- operational security requirements;
- which concepts CE should reserve without implementing Cloud complexity.

The key rule is:

> Cloud must derive access from authenticated identity and scoped ownership, never from untrusted client-provided tenant or workspace fields.

---

## 2. Security Goal

The goal of Cloud security is:

> Allow multiple customers to safely use a shared hosted Opstage control plane while keeping tenant data isolated, Agent access scoped, secrets protected, and important operations auditable.

Cloud security must protect:

- user accounts;
- organizations;
- workspaces;
- Agents;
- Capsule Services;
- Commands;
- Audit Events;
- billing metadata;
- governance metadata;
- customer data boundaries;
- Cloud platform operations.

---

## 3. Cloud Is Not CE v0.1

CE v0.1 must not implement Cloud-only security capabilities such as:

- tenant isolation;
- organization-level RBAC;
- workspace memberships;
- SSO/OIDC/SAML;
- SCIM;
- billing security;
- Cloud Agent Gateway;
- multi-tenant rate limiting;
- Cloud support access workflow;
- compliance-grade audit retention;
- managed secret vault;
- Cloud data residency controls.

CE should reserve compatible concepts, but Cloud security must not become a dependency of CE v0.1.

---

## 4. Trust Boundaries

Cloud has stronger trust boundaries than CE.

Recommended Cloud trust zones:

```text
Browser / User Client
    ↓
Cloud UI / API Edge
    ↓
Cloud Backend Services
    ↓
Cloud Database / Storage

Customer Environment
    ↓
Agent
    ↓
Capsule Service
```

Agent connectivity boundary:

```text
Customer Agent
    ↓ outbound authenticated connection
Cloud Agent Gateway / Agent API
    ↓
Cloud Backend
```

Cloud must assume:

- browser clients are untrusted;
- Agent payloads are untrusted until authenticated and validated;
- tenant context in request body is untrusted;
- customer environments are outside Cloud control;
- support access must be controlled and audited;
- raw customer secrets should not be required by default.

---

## 5. Security Principles

Cloud security should follow these principles:

1. Authenticate every user and Agent.
2. Derive tenant and workspace context from authenticated identity.
3. Enforce authorization on the Backend, not only in UI.
4. Scope Agent access to its own Workspace and Commands.
5. Do not trust tenant/workspace IDs from arbitrary payloads.
6. Store hashes, not raw tokens.
7. Avoid raw customer secrets by default.
8. Use `secretRef` as the primary secret boundary.
9. Keep durable Command and Audit records.
10. Audit important operations.
11. Apply rate limits and abuse protections.
12. Keep support access restricted and auditable.
13. Preserve CE compatibility without importing Cloud complexity into CE.

---

## 6. Tenant Isolation

Tenant isolation is the foundation of Cloud security.

### 6.1 Tenant context

Tenant context should be derived from authenticated identity.

For user requests:

```text
User session -> Membership -> Organization / Workspace -> Tenant
```

For Agent requests:

```text
Agent token -> Agent -> Workspace -> Organization -> Tenant
```

For API clients:

```text
API key -> Service account -> Organization / Workspace -> Tenant
```

### 6.2 Untrusted tenant fields

Cloud must not trust `tenantId`, `organizationId`, or `workspaceId` from request payloads unless they are checked against authenticated identity.

Bad:

```json
{
  "tenantId": "ten_001",
  "workspaceId": "wks_001",
  "serviceCode": "demo-capsule-service"
}
```

if Backend accepts it without ownership validation.

Good:

```text
Authenticated identity determines accessible tenant and workspace.
Payload resource IDs are validated against that scope.
```

### 6.3 Query isolation

All Cloud database queries for customer data must be scoped by tenant, organization, or workspace context.

Required practice:

```text
No unscoped customer data query in Cloud services.
```

Potential enforcement mechanisms:

- repository-level scoped query helpers;
- tenant-aware service context;
- database row-level security if supported;
- integration tests for cross-tenant access;
- static review rules;
- audit of suspicious cross-scope attempts.

---

## 7. Workspace Isolation

Workspace is the primary operational boundary for Agents and Capsule Services.

Workspace owns:

- Agents;
- registration tokens;
- Capsule Services;
- Commands;
- CommandResults;
- HealthReports;
- ConfigItems;
- ActionDefinitions;
- AuditEvents;
- alert rules;
- operational settings.

Cloud access to these resources should require Workspace membership or a scoped service/Agent identity.

CE may reserve `workspaceId`, but Cloud owns full workspace security.

---

## 8. Organization Isolation

Organization is the customer-visible account boundary.

Organization may own:

- members;
- roles;
- workspaces;
- billing account;
- subscription;
- organization-level audit;
- organization settings;
- SSO configuration;
- data export and deletion requests.

Users may belong to multiple Organizations.

Cloud UI must make the active Organization and Workspace clear to avoid accidental cross-context operations.

---

## 9. Identity and Access Management

Cloud should support stronger identity than CE.

### 9.1 User authentication

Possible authentication methods:

- email/password;
- OAuth login;
- SSO/OIDC for higher plans;
- SAML for enterprise plans;
- MFA for higher-risk accounts;
- SCIM for enterprise lifecycle management.

### 9.2 User session security

Cloud user sessions should use secure practices:

- HTTP-only cookies;
- Secure flag over HTTPS;
- SameSite protection;
- CSRF protection where needed;
- session expiration;
- refresh flow if used;
- suspicious login detection in future.

### 9.3 Password security

If Cloud supports password login:

- store only password hashes;
- use strong password hashing such as argon2 or bcrypt;
- never log passwords;
- implement password reset securely;
- audit login and failed login events.

### 9.4 Service accounts and API keys

Future Cloud may support service accounts and API keys.

API keys must be:

- scoped;
- revocable;
- stored as hashes;
- shown only once;
- audited when used for sensitive operations.

---

## 10. Authorization Model

Cloud authorization should be scope-based and role-based.

Possible scopes:

```text
Organization
Workspace
Agent
CapsuleService
Action
Audit
Billing
```

Possible roles:

```text
Owner
Admin
Operator
Viewer
Auditor
BillingAdmin
```

Possible permissions:

```text
organization.manage
workspace.manage
agent.register
agent.revoke
service.view
service.action.execute
command.view
audit.view
billing.manage
```

Cloud authorization should be enforced in Backend services and APIs.

CE v0.1 should not implement this full model.

---

## 11. Agent Trust Model

Agents are customer-side actors that connect to Cloud.

### 11.1 Agent authentication

Agents authenticate with Agent tokens:

```http
Authorization: Bearer <agentToken>
```

Cloud must validate:

- token hash;
- token status;
- expiration;
- Agent identity;
- Workspace ownership;
- revoked/disabled state;
- protocol compatibility if required.

### 11.2 Agent scoping

An Agent may only:

- heartbeat for itself;
- report services under its Workspace;
- poll Commands assigned to itself;
- report CommandResults for Commands assigned to itself;
- report health/config/action metadata for its own services.

An Agent must not:

- call Admin APIs;
- access other Agents' Commands;
- report results for another Agent's Commands;
- select arbitrary tenant/workspace scope;
- create Commands directly unless future scoped capability allows it.

### 11.3 Agent revocation

Cloud must support Agent revocation.

Revoked Agents should be rejected from Agent APIs.

Revocation should create AuditEvents.

### 11.4 Agent token rotation

Future Cloud should support Agent token rotation.

CE v0.1 does not need full rotation workflow.

---

## 12. Registration Token Security

Registration tokens are sensitive because they allow Agent enrollment.

Rules:

- scope registration token to Workspace;
- store only token hash;
- show raw token only once;
- support expiration;
- support revocation;
- support one-time use where practical;
- rate-limit registration attempts;
- audit creation, use, and revocation.

Cloud may add enrollment policies later:

- allowed runtime;
- allowed Agent mode;
- expiration window;
- max uses;
- IP or region constraints;
- approval requirement.

---

## 13. Agent Gateway Security

Future Cloud may introduce Agent Gateway.

Security responsibilities may include:

- TLS termination;
- Agent token validation;
- tenant/workspace context derivation;
- request rate limiting;
- abuse detection;
- protocol version negotiation;
- connection lifecycle tracking;
- routing only to authorized internal services;
- rejection of revoked Agents;
- protection against malformed payloads.

Agent Gateway must not become a bypass around Backend authorization.

CE v0.1 does not need Agent Gateway.

---

## 14. Data Isolation

Cloud may use one of several data isolation strategies.

### 14.1 Shared database with scoped rows

```text
Shared database
Tenant/Organization/Workspace IDs on rows
Strict scoped queries
```

This is likely simplest for early Cloud.

### 14.2 Separate schema per tenant

Provides stronger isolation with higher operational complexity.

### 14.3 Separate database per tenant

Strongest isolation, but expensive and complex.

### 14.4 Security rule

Regardless of storage strategy:

```text
Application code must enforce scope checks before returning customer data.
```

---

## 15. Data Boundary Security

Cloud should store governance metadata by default, not raw customer operational secrets.

Cloud may store:

- Agent metadata;
- Capsule Service metadata;
- health reports;
- config metadata;
- action metadata;
- command metadata;
- sanitized command results;
- sanitized audit events;
- usage metadata.

Cloud should not store by default:

- raw passwords;
- raw registration tokens;
- raw Agent tokens;
- raw cookies;
- raw OAuth tokens;
- private keys;
- account credentials;
- customer business records;
- large application logs;
- browser traces.

---

## 16. Secret Handling

### 16.1 Default secret boundary

Default model:

```text
Customer secrets remain in customer environment.
Cloud stores only secretRef.
```

### 16.2 SecretRef

Examples:

```text
agent-local://agent-001/secrets/chatgpt/account-001
customer-vault://prod/integration-worker/account-001
aws-secretsmanager://region/account/secret-name
cloud-secret://org/workspace/secret-key
```

### 16.3 Optional managed secrets

Future Cloud may support optional managed secrets.

Managed secrets require a separate design covering:

- encryption;
- key management;
- access policies;
- audit;
- rotation;
- export and deletion;
- customer opt-in;
- plan boundaries.

Managed secrets must not be required for basic Cloud governance.

---

## 17. Command Security

Commands are operationally sensitive.

Cloud must enforce:

- user permission to request action;
- service belongs to selected Workspace;
- action exists and is enabled;
- action payload validation;
- confirmation for high-risk actions;
- Agent assignment;
- command expiration;
- Agent ownership on result report;
- audit event creation.

Cloud must not provide arbitrary shell execution by default.

Even in future editions, unsafe operations should use predefined actions, approvals, permissions, and audit.

---

## 18. Action Security

Actions must be predefined by Capsule Services.

Before creating an Action Command, Cloud should validate:

- authenticated user;
- workspace access;
- service visibility;
- action definition;
- action enabled state;
- danger level;
- confirmation requirement;
- payload schema if available;
- quota or plan entitlement if applicable.

Dangerous actions may require:

- confirmation;
- stronger role;
- approval workflow;
- audit reason;
- MFA in future plans.

---

## 19. Audit Security

Cloud audit is a security feature.

AuditEvents should record important operations:

- login;
- failed login;
- user invitation;
- role change;
- registration token creation;
- Agent registration;
- Agent revocation;
- service report;
- action request;
- Command creation;
- Command success/failure;
- billing changes;
- security settings changes.

Audit payloads must be sanitized.

Audit access should require proper permission.

Future Cloud may add immutable audit storage or export.

---

## 20. Support Access Security

Cloud provider support access must be controlled.

Future support access model should include:

- explicit support role;
- time-limited access;
- customer approval where appropriate;
- support access audit;
- restricted views;
- no raw secret access by default;
- support impersonation controls if implemented;
- customer-visible support activity logs.

Support access is not a CE concern.

---

## 21. Rate Limiting and Abuse Prevention

Cloud must protect itself from abuse.

Possible rate limits:

- login attempts;
- registration token attempts;
- Agent heartbeat rate;
- command polling rate;
- service report frequency;
- command result submissions;
- API key requests;
- invitation sends;
- notification sends.

Abuse prevention may include:

- IP-based throttling;
- tenant-based quotas;
- Agent-based rate limits;
- suspicious behavior detection;
- temporary blocks;
- security alerts.

CE v0.1 may implement minimal defensive checks but should not require Cloud-scale rate limiting.

---

## 22. Network Security

Cloud should use HTTPS for all external communication.

Agent connectivity should use:

```text
Agent -> Cloud over HTTPS / secure WebSocket
```

Future Cloud may support:

- mTLS for enterprise plans;
- IP allowlists;
- private network connectivity;
- regional Agent Gateway;
- proxy-aware Agent SDK.

Cloud should not require inbound connections into customer environments.

---

## 23. Storage Security

Cloud storage should follow secure practices:

- encryption at rest;
- encrypted backups;
- access-controlled database credentials;
- secret-managed application configuration;
- least-privilege service accounts;
- backup retention policy;
- restore testing;
- audit of administrative access.

Exact implementation depends on future Cloud infrastructure choice.

---

## 24. Operational Security

Cloud operations should include:

- production monitoring;
- alerting;
- incident response;
- vulnerability patching;
- dependency scanning;
- secret rotation;
- access reviews;
- backup and restore testing;
- deployment audit;
- change management.

These are Cloud platform operations, not CE v0.1 requirements.

---

## 25. Compliance Direction

Future Cloud may need compliance-related capabilities depending on target customers.

Possible areas:

- GDPR support;
- data export;
- data deletion;
- audit retention;
- DPA process;
- subprocessors list;
- data residency;
- SOC 2 readiness;
- enterprise security questionnaire support.

These should be planned only when Cloud becomes a real commercial target.

---

## 26. Incident Response

Cloud should eventually define incident response procedures.

Potential procedures:

- incident classification;
- customer notification;
- credential revocation;
- audit preservation;
- forensic logging;
- remediation tracking;
- post-incident review.

CE v0.1 does not need formal incident response beyond normal security documentation.

---

## 27. CE Reservations

CE should reserve these Cloud-compatible security concepts:

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
status and freshness calculation
```

CE should not implement:

```text
Tenant isolation
Organization membership
Cloud RBAC
Cloud SSO
Cloud Agent Gateway
Cloud support access workflow
Cloud compliance audit suite
Cloud rate limiting system
Cloud managed secret vault
```

---

## 28. Anti-Patterns

Avoid these patterns.

### 28.1 Trusting tenant IDs from request payloads

Tenant context must come from authenticated identity.

### 28.2 UI-only authorization

Backend must enforce authorization.

### 28.3 Agent can choose arbitrary Workspace

Agent ownership must come from Agent token.

### 28.4 Raw secrets in Cloud by default

Use `secretRef` and customer-controlled secrets.

### 28.5 Audit logs with secrets

Audit payloads must be sanitized.

### 28.6 Support access without audit

Support access must be controlled and logged.

### 28.7 Pulling Cloud isolation into CE v0.1

CE should stay lightweight and single-node-friendly.

---

## 29. Security Acceptance Criteria

Cloud security and isolation planning is acceptable when:

- tenant context derivation is clearly defined;
- user and Agent trust boundaries are clear;
- Agent token scope is clear;
- Workspace is the primary operational boundary;
- data isolation strategy options are identified;
- Cloud does not store raw secrets by default;
- `secretRef` is the default secret boundary;
- support access is recognized as a security-sensitive workflow;
- audit and rate limiting are included in planning;
- CE reservations are clear;
- CE v0.1 is not burdened with Cloud security infrastructure.

---

## 30. Summary

Opstage Cloud security must protect a shared SaaS control plane while keeping customer environments and secrets safe by default.

The most important security and isolation rule is:

> In Cloud, every resource access must be scoped by authenticated identity, tenant/workspace ownership, and explicit authorization — never by untrusted client claims alone.
