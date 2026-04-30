# Cloud Multi-Tenant Model

- Status: Planning
- Edition: Cloud
- Priority: Future

## Position

Cloud 是未来 SaaS 云服务版规划，不是 CE v0.1 的实现要求。

## Planned Direction

- 官方托管 Opstage Backend 和 UI。
- 客户侧 Agent 主动 outbound 连接 Cloud。
- 多租户、组织、团队、订阅计费。
- 云端保存元数据、状态、审计、指标；敏感 secret 优先保留在客户侧或外部 Secret Store。

## CE Reservation

CE 的 Agent 注册、心跳、命令拉取模型应天然支持未来 Cloud：Backend 不主动扫描客户内网，Agent 主动连接控制面。

# Cloud Multi-Tenant Model

- Status: Planning
- Edition: Cloud
- Priority: Future
- Audience: founders, product designers, architects, cloud backend developers, security reviewers, AI coding agents

This document defines the planned multi-tenant model for **Opstage Cloud**.

Opstage Cloud is the future hosted SaaS edition of the `xtrape-capsule` product family. Multi-tenancy is a Cloud requirement, not a CE v0.1 implementation requirement.

---

## 1. Purpose

The purpose of this document is to define:

- why Cloud needs a multi-tenant model;
- the difference between Tenant, Organization, Workspace, Team, User, and Role;
- how Agents and Capsule Services are scoped in Cloud;
- how billing and subscription may relate to tenancy;
- how data isolation should be approached;
- which concepts CE should reserve without implementing;
- which concepts must not be pulled into CE v0.1.

The key rule is:

> CE may reserve `workspaceId`, but Cloud owns the full multi-tenant model.

---

## 2. Multi-Tenant Goal

The goal of the Cloud multi-tenant model is:

> Allow multiple customers, organizations, teams, and workspaces to safely use one hosted Opstage Cloud platform while preserving data isolation, access control, billing boundaries, and operational traceability.

Cloud must support multiple customer groups in one hosted platform.

CE v0.1 does not need this.

---

## 3. Core Hierarchy

Recommended Cloud hierarchy:

```text
Tenant
    ↓
Organization
    ↓
Workspace
    ↓
Agent
    ↓
Capsule Service
```

User membership and roles attach to Organization and/or Workspace:

```text
User
    ↓ membership
Organization / Workspace
    ↓ role assignment
Role
```

Billing usually attaches to Organization or Tenant, depending on final commercial design.

---

## 4. Concept Summary

| Concept | Meaning | CE v0.1 |
|---|---|---|
| Tenant | Platform-level isolation boundary | Not implemented |
| Organization | Customer/account/business owner boundary | Not implemented |
| Workspace | Operational grouping of Agents and Services | Reserved as default Workspace |
| Team | Optional collaboration grouping inside Organization | Not implemented |
| User | Human account | CE has local admin only |
| Membership | User belongs to Org/Workspace | Not implemented |
| Role | Permission bundle | CE may use owner only |
| Subscription | Commercial plan/billing state | Not implemented |
| Agent | Customer-side governance bridge | Implemented in CE |
| CapsuleService | Managed lightweight service | Implemented in CE |

---

## 5. Tenant

### 5.1 Definition

A Tenant is the highest Cloud isolation boundary.

It may represent:

- one customer account;
- one legal customer entity;
- one isolated SaaS partition;
- one billing and data boundary;
- one enterprise customer environment.

### 5.2 Planned responsibilities

Tenant may own:

- Organizations;
- global tenant settings;
- data isolation boundary;
- regional placement;
- compliance settings;
- customer-level retention policies;
- high-level usage limits.

### 5.3 Example fields

```text
id
code
name
status
region
planTier
createdAt
updatedAt
```

### 5.4 CE relationship

CE v0.1 must not implement Tenant.

CE should not require tenant IDs in APIs.

Cloud may introduce Tenant later without changing CE core concepts.

---

## 6. Organization

### 6.1 Definition

An Organization represents a customer-owned account or business group in Cloud.

For most SaaS users, Organization is the visible account boundary.

### 6.2 Planned responsibilities

Organization may own:

- users and memberships;
- workspaces;
- billing account;
- subscription;
- organization-level roles;
- organization audit logs;
- organization settings;
- data export requests.

### 6.3 Example fields

```text
id
tenantId
code
name
status
ownerUserId
createdAt
updatedAt
```

### 6.4 Relationship to Tenant

Possible model:

```text
Tenant 1 --- n Organization
```

For simpler Cloud MVP, Tenant and Organization may be collapsed internally.

However, they should remain conceptually distinct in planning.

### 6.5 CE relationship

CE v0.1 must not implement Organization.

CE local deployment may be viewed as a single implicit organization, but it should not require an Organization table.

---

## 7. Workspace

### 7.1 Definition

A Workspace is an operational boundary for Agents, Capsule Services, Commands, and Audit Events.

Workspace is the most important tenancy concept already partially reserved by CE.

### 7.2 Planned responsibilities

Workspace may own:

- Agents;
- Capsule Services;
- Commands;
- Audit Events;
- workspace settings;
- registration tokens;
- alert rules;
- service groups;
- workspace-level roles.

### 7.3 Example fields

```text
id
organizationId
code
name
status
defaultRegion
createdAt
updatedAt
```

### 7.4 CE relationship

CE v0.1 should have one default Workspace:

```text
wks_default
```

CE may include `workspaceId` on core records, but it should not implement:

- workspace switcher;
- workspace management UI;
- workspace invitations;
- workspace billing;
- workspace-level RBAC.

### 7.5 Design rule

Cloud should use Workspace as the primary operational filter.

Most user-facing Cloud pages should be scoped to a selected Workspace.

---

## 8. Team

### 8.1 Definition

A Team is an optional collaboration grouping inside an Organization.

Teams may help manage access to multiple Workspaces or service groups.

### 8.2 Planned responsibilities

Team may own:

- team members;
- team roles;
- workspace access rules;
- notification routing;
- responsibility assignment.

### 8.3 Example fields

```text
id
organizationId
name
description
status
createdAt
updatedAt
```

### 8.4 CE relationship

CE v0.1 must not implement Team.

Team is a future Cloud/EE collaboration concept.

---

## 9. User

### 9.1 Definition

A User is a human account in Opstage Cloud.

Cloud Users may belong to multiple Organizations and Workspaces.

### 9.2 Planned responsibilities

User may have:

- login identity;
- profile;
- memberships;
- roles;
- MFA settings;
- API keys;
- audit actor identity.

### 9.3 Example fields

```text
id
email
displayName
avatarUrl
status
lastLoginAt
createdAt
updatedAt
```

### 9.4 Identity providers

Cloud may support:

- email/password;
- OAuth login;
- SSO/OIDC;
- SAML for enterprise plans;
- SCIM for enterprise lifecycle management.

### 9.5 CE relationship

CE v0.1 should only implement local admin user.

CE does not need Cloud-style user membership.

---

## 10. Membership

### 10.1 Definition

Membership links a User to an Organization, Workspace, or Team.

### 10.2 Planned membership types

```text
OrganizationMembership
WorkspaceMembership
TeamMembership
```

### 10.3 Example fields

```text
id
userId
organizationId
workspaceId
teamId
roleId
status
invitedBy
joinedAt
createdAt
updatedAt
```

### 10.4 Status values

```text
INVITED
ACTIVE
SUSPENDED
REMOVED
```

### 10.5 CE relationship

CE v0.1 must not implement membership.

---

## 11. Role and Permission

### 11.1 Definition

A Role is a named permission bundle.

A Permission is an allowed operation on a resource type.

### 11.2 Planned role levels

Cloud may support roles at different scopes:

```text
Organization role
Workspace role
Service role
```

### 11.3 Possible built-in roles

```text
Owner
Admin
Operator
Viewer
BillingAdmin
Auditor
```

### 11.4 Possible permissions

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

### 11.5 CE relationship

CE v0.1 may use only:

```text
owner
```

CE must not implement a full RBAC policy engine.

---

## 12. Subscription and Billing Boundary

### 12.1 Definition

Subscription represents the commercial plan and entitlement state.

Billing boundary may attach to:

```text
Organization
```

or:

```text
Tenant
```

depending on final Cloud architecture.

### 12.2 Planned billing objects

```text
Plan
Subscription
BillingAccount
UsageRecord
Invoice
PaymentMethod
Entitlement
Quota
```

### 12.3 Possible plan dimensions

- number of users;
- number of Workspaces;
- number of Agents;
- number of Capsule Services;
- command volume;
- audit retention;
- health history retention;
- alert volume;
- support tier.

### 12.4 CE relationship

CE v0.1 must not implement billing or subscription.

---

## 13. Agent Scoping

### 13.1 Cloud Agent ownership

In Cloud, an Agent should belong to exactly one Workspace at a time.

Recommended relationship:

```text
Workspace 1 --- n Agent
Agent 1 --- n CapsuleService
```

### 13.2 Agent registration token scope

Registration tokens should be scoped to:

```text
Workspace
```

possibly also:

```text
Organization
Tenant
```

internally.

### 13.3 Agent token scope

Agent token should be scoped to:

- Agent;
- Workspace;
- Organization/Tenant internally;
- allowed capabilities if future scoped tokens are implemented.

### 13.4 CE relationship

CE v0.1 uses one default Workspace.

Agent registration token can be implicitly scoped to `wks_default`.

---

## 14. Capsule Service Scoping

### 14.1 Cloud service ownership

A Capsule Service belongs to a Workspace and is reported by an Agent.

Recommended relationship:

```text
Workspace 1 --- n CapsuleService
Agent 1 --- n CapsuleService
```

### 14.2 Service code uniqueness

Recommended uniqueness:

```text
workspaceId + serviceCode unique
```

This is compatible with CE.

### 14.3 Service visibility

User visibility should be determined by Workspace membership and role.

### 14.4 CE relationship

CE should already use `workspaceId + code` uniqueness if practical.

---

## 15. Command Scoping

### 15.1 Command ownership

A Command should belong to:

- Workspace;
- Agent;
- Capsule Service;
- creating User or system actor.

### 15.2 Access rules

Cloud UI users may view or create Commands only if they have permission in the Workspace.

Agents may poll only Commands assigned to themselves.

### 15.3 CE relationship

CE should already store:

```text
workspaceId
agentId
serviceId
createdBy
```

where practical.

---

## 16. Audit Scoping

### 16.1 Audit ownership

AuditEvents should belong to:

```text
Workspace
```

and internally to:

```text
Organization / Tenant
```

in Cloud.

### 16.2 Audit access

Users may access AuditEvents based on:

- organization role;
- workspace role;
- audit-specific permission;
- plan entitlement;
- retention policy.

### 16.3 CE relationship

CE should store `workspaceId` on AuditEvent if practical.

CE does not need organization-level audit.

---

## 17. Data Isolation Model

Cloud must isolate customer data.

Possible isolation strategies:

### 17.1 Shared database, tenant-scoped rows

```text
Single database
Tenant/Organization/Workspace IDs on all rows
Strict query filters
```

Pros:

- simpler to operate;
- lower cost;
- easier early Cloud MVP.

Cons:

- requires strict application-level isolation;
- higher blast radius if bugs exist.

### 17.2 Separate schema per tenant

```text
One database cluster
Separate schema per tenant
```

Pros:

- stronger separation;
- easier tenant export.

Cons:

- more operational complexity.

### 17.3 Separate database per tenant

```text
Dedicated database per tenant
```

Pros:

- strongest isolation;
- enterprise-friendly.

Cons:

- expensive and operationally heavy.

### 17.4 Planning recommendation

For early Cloud, a shared database with strict tenant-scoped rows may be sufficient.

For enterprise Cloud or regulated customers, stronger isolation may be required.

This decision should be revisited during Cloud architecture design.

---

## 18. Tenant Context Resolution

Cloud requests must resolve tenant context consistently.

Possible resolution sources:

- authenticated user membership;
- selected organization/workspace in UI;
- Agent token scope;
- API key scope;
- subdomain;
- request path.

Examples:

```text
https://cloud.opstage.example/org/acme/workspaces/prod
https://acme.opstage.example/workspaces/prod
```

The final URL and tenant routing model is future work.

---

## 19. Agent Tenant Context

For Agent requests, tenant context should be derived from Agent token, not from user-provided request fields.

Bad:

```json
{
  "tenantId": "ten_001",
  "workspaceId": "wks_001"
}
```

if Backend trusts these fields blindly.

Good:

```text
Agent token -> Agent -> Workspace -> Organization -> Tenant
```

Agent may include service code and metadata, but Backend should derive ownership from authenticated Agent identity.

---

## 20. Data Model Planning Summary

Future Cloud data model may include:

```text
Tenant
Organization
Workspace
User
Membership
Role
Permission
Team
Invitation
Subscription
Plan
UsageRecord
BillingAccount
Agent
AgentToken
CapsuleService
Command
CommandResult
AuditEvent
```

CE v0.1 should include only:

```text
Workspace default
User local admin
Agent
AgentToken
CapsuleService
Command
CommandResult
AuditEvent
```

---

## 21. CE Reservations for Multi-Tenancy

CE should reserve:

```text
workspaceId
createdBy
actorType
actorId
resourceType
resourceId
metadataJson
```

CE should not implement:

```text
tenantId
organizationId
subscriptionId
billingAccountId
membership tables
role permission policy engine
team management
invitation workflow
```

unless later CE scope explicitly changes.

---

## 22. Multi-Tenant Security Considerations

Cloud multi-tenancy requires strong security design.

Future Cloud must consider:

- tenant data isolation;
- strict query scoping;
- authorization checks;
- Agent token scoping;
- workspace-level permissions;
- audit of cross-boundary access attempts;
- data export and deletion;
- retention policies;
- abuse prevention;
- rate limiting.

These are Cloud requirements, not CE v0.1 requirements.

---

## 23. Multi-Tenant UI Considerations

Future Cloud UI may need:

- organization switcher;
- workspace switcher;
- member management;
- invitations;
- role management;
- billing settings;
- usage dashboard;
- audit by organization/workspace;
- Agent registration token scoped to selected Workspace.

CE UI should not show these Cloud-only controls.

---

## 24. Anti-Patterns

Avoid these patterns.

### 24.1 Pulling Cloud tenancy into CE v0.1

Do not require CE users to create tenants or organizations.

### 24.2 Trusting tenant IDs from Agent payloads

Agent ownership must come from authenticated Agent token.

### 24.3 Mixing billing with Workspace core model

Workspace should remain an operational boundary. Billing should be separate.

### 24.4 Changing service code uniqueness later

Keep `workspaceId + serviceCode` as the expected uniqueness boundary.

### 24.5 Showing disabled Cloud tenant UI in CE

Do not clutter CE UI with Cloud-only features.

---

## 25. Acceptance Criteria

The Cloud multi-tenant model planning is acceptable when:

- Tenant, Organization, Workspace, User, Membership, Role, and Subscription are clearly separated;
- Workspace is identified as the primary operational boundary;
- Agent token is the source of Agent tenant context;
- Capsule Service uniqueness is scoped by Workspace;
- CE reservations are clear;
- CE v0.1 is not required to implement Cloud tenancy;
- future Cloud security concerns are documented;
- data isolation strategy options are identified.

---

## 26. Summary

Cloud multi-tenancy should support hosted SaaS usage without breaking the CE governance kernel.

The most important multi-tenant rule is:

> In Cloud, tenant context must be derived from authenticated identity and scoped ownership, not trusted from arbitrary client payloads.