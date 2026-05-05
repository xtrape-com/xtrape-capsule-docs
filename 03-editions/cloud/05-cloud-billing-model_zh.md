---
status: draft
audience: founders
stability: unstable
last_reviewed: 2026-05-05
edition: cloud
phase: future
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 05-cloud-billing-model.md
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

# Cloud（云版） Billing Model

- Status: Planning
- Edition: Cloud（云版）
- Priority: Future
- Audience: founders, product designers, architects, cloud backend developers, billing engineers, AI coding agents

This document 定义 the planned billing model for **Opstage（运维舞台） Cloud（云版）**.

Opstage（运维舞台） Cloud（云版） is the future hosted SaaS edition of the `xtrape-capsule` product family. Billing is a Cloud（云版） capability, not a CE（社区版） v0.1 implementation requirement.

---

## 1. Purpose

The purpose of this document is to define:

- how Opstage（运维舞台） Cloud（云版） may package commercial plans;
- which usage dimensions may be metered;
- which capabilities may become plan limits;
- how billing should relate to Tenant, Organization, and Workspace;
- how free, team, business, and enterprise tiers may differ;
- which billing concepts CE（社区版） should not implement;
- how to avoid damaging CE（社区版） trust with artificial limitations.

The key rule is:

> Cloud（云版） billing should monetize managed service value, scale, collaboration, retention, and support — not a crippled CE（社区版） core.

---

## 2. Billing Goal

The goal of Cloud（云版） billing is:

> Create a fair commercial model for hosted Capsule Service（胶囊服务） governance while keeping adoption simple and preserving trust in CE（社区版）.

Billing should reflect real platform costs and customer value, including:

- hosted control plane;
- managed database;
- Agent（代理） connectivity;
- command and audit processing;
- health history retention;
- alerting and notifications;
- team collaboration;
- support and reliability.

---

## 3. Billing Is Not CE（社区版） v0.1

CE（社区版） v0.1 must not implement:

- subscriptions;
- billing accounts;
- payment methods;
- invoices;
- usage metering;
- SaaS quotas;
- plan enforcement;
- entitlement checks;
- license enforcement.

CE（社区版） may reserve compatible concepts such as `workspaceId`, but billing must remain a Cloud（云版）/Commercial edition concern.

---

## 4. Commercial Positioning

Cloud（云版） should charge for managed value.

Good monetization areas:

- hosted Backend and UI;
- managed upgrades;
- managed backups;
- team collaboration;
- more Agents;
- more Capsule Services;
- longer audit retention;
- longer health history;
- alerting and notifications;
- advanced Agent（代理） connectivity;
- enterprise identity;
- SLA and support.

Bad monetization areas:

- blocking basic Agent（代理） registration;
- disabling basic health visibility;
- disabling predefined actions in CE（社区版）;
- disabling basic audit in CE（社区版）;
- making CE（社区版） intentionally unusable.

---

## 5. Billing Boundary

Recommended billing boundary:

```text
Organization owns Subscription and BillingAccount.
Workspace consumes plan quota.
Agents and Capsule Services generate usage.
```

Possible hierarchy:

```text
Tenant
    ↓
Organization
    ↓ billing account / subscription
Workspace
    ↓
Agents / Capsule Services / Commands / Audit Events
```

For early Cloud（云版） MVP, Tenant and Organization may be collapsed internally, but billing should still appear to users at the Organization/account level.

---

## 6. Core Billing Concepts

Future Cloud（云版） may introduce these billing concepts:

```text
Plan
Subscription
BillingAccount
PaymentMethod
Invoice
UsageRecord
Entitlement
Quota
Meter
Credit
AddOn
```

CE（社区版） v0.1 should not implement these objects.

---

## 7. Plan

### 7.1 Definition

A Plan 定义 a commercial package.

Example plans:

```text
Developer
Team
Business
Enterprise
```

### 7.2 Possible Plan fields

```text
id
code
name
description
billingInterval
basePrice
currency
includedLimits
features
status
createdAt
updatedAt
```

### 7.3 Billing intervals

Possible intervals:

```text
monthly
yearly
custom
```

Enterprise plans may use custom contracts.

---

## 8. Subscription

### 8.1 Definition

A Subscription is an Organization's active commercial relationship for a Plan.

### 8.2 Possible fields

```text
id
organizationId
planId
status
billingInterval
currentPeriodStart
currentPeriodEnd
trialEndsAt
cancelAt
createdAt
updatedAt
```

### 8.3 状态 values

Possible values:

```text
TRIALING
ACTIVE
PAST_DUE
CANCELLED
EXPIRED
SUSPENDED
```

### 8.4 CE（社区版） relationship

CE（社区版） must not require Subscription.

---

## 9. BillingAccount

### 9.1 Definition

BillingAccount stores billing ownership and payment metadata for an Organization.

### 9.2 Possible fields

```text
id
organizationId
billingEmail
companyName
taxId
country
paymentProviderCustomerId
status
createdAt
updatedAt
```

### 9.3 Payment provider

Cloud（云版） may later integrate with a payment provider such as Stripe, Paddle, Lemon Squeezy, or another provider depending on company jurisdiction and product strategy.

Payment provider choice is not decided in this document.

---

## 10. UsageRecord

### 10.1 Definition

UsageRecord stores billable or quota-relevant usage.

### 10.2 Possible fields

```text
id
organizationId
workspaceId
meterCode
quantity
unit
periodStart
periodEnd
source
metadataJson
createdAt
```

### 10.3 Meter examples

```text
agent.count
capsuleService.count
command.count
auditEvent.count
healthReport.count
alertNotification.count
userSeat.count
storage.audit.gbMonth
storage.health.gbMonth
```

Usage records should be append-only or auditable enough for billing disputes.

---

## 11. Entitlement

### 11.1 Definition

An Entitlement represents what an Organization is allowed to use under its plan.

Examples:

```text
maxAgents = 5
maxCapsuleServices = 20
auditRetentionDays = 30
healthRetentionDays = 7
alertChannels = [email, webhook]
```

### 11.2 Possible fields

```text
id
organizationId
planId
key
valueJson
source
createdAt
updatedAt
```

### 11.3 Runtime behavior

Entitlements may be checked when:

- creating a Workspace;
- creating registration tokens;
- registering Agents;
- reporting new Capsule Services;
- enabling alert rules;
- retaining audit or health history;
- inviting users.

---

## 12. Quota

### 12.1 Definition

Quota is an enforced limit derived from a Plan or Entitlement.

### 12.2 Possible quota types

```text
hard quota
soft quota
warning threshold
overage allowed
manual approval required
```

### 12.3 Recommended approach

Early Cloud（云版） should prefer soft limits and clear warnings before hard blocking critical governance flows.

Example:

```text
Agent count exceeded plan limit. Existing Agents continue working, but new Agent registration requires upgrade.
```

Avoid abruptly breaking existing Agent（代理） communication unless required for abuse prevention or severe payment failure.

---

## 13. Candidate Pricing Dimensions

Cloud（云版） may use these dimensions for pricing or plan limits.

### 13.1 Agents

Agents are a natural pricing dimension.

Reason:

- each Agent（代理） creates heartbeat traffic;
- each Agent（代理） represents a managed runtime connection;
- Agent（代理） count maps well to customer scale.

Possible limit:

```text
maxAgents
```

### 13.2 Capsule Services

Capsule Services are another natural dimension.

Reason:

- each service creates metadata, health, config, action, command, and audit records;
- service count maps directly to governance scope.

Possible limit:

```text
maxCapsuleServices
```

### 13.3 Users or seats

Team plans may charge by seats.

Possible limit:

```text
maxUsers
```

### 13.4 Workspaces

Workspaces may be limited by plan.

Possible limit:

```text
maxWorkspaces
```

### 13.5 Command volume

Command volume may become a usage dimension.

Possible meter:

```text
command.count
```

Do not overcharge early users for low command volume.

### 13.6 Audit retention

Audit retention is a strong plan differentiator.

Possible limits:

```text
auditRetentionDays = 7 / 30 / 90 / 365 / custom
```

### 13.7 Health history retention

Health history can be plan-based.

Possible limits:

```text
healthRetentionDays = 1 / 7 / 30 / 90
```

### 13.8 Alerts and notifications

Alerting can be plan-based.

Possible dimensions:

```text
maxAlertRules
alertNotification.count
enabled notification channels
```

### 13.9 Storage

Long-term storage may be billed or limited.

Possible meters:

```text
storage.audit.gbMonth
storage.health.gbMonth
storage.logs.gbMonth
```

Logs should not be part of early Cloud（云版） unless explicitly implemented.

---

## 14. Candidate Plan Structure

This is planning only and should not be treated as final pricing.

### 14.1 Developer / Free

Purpose:

- individual testing;
- early adoption;
- demo usage;
- low-cost onboarding.

Possible limits:

```text
1 organization
1 workspace
1-3 Agents
3-10 Capsule Services
basic health visibility
basic commands
short audit retention
community support
```

### 14.2 Team

Purpose:

- small team collaboration;
- managed governance for small service fleets.

Possible limits:

```text
multiple users
several workspaces
more Agents
more Capsule Services
30-day audit retention
basic alerting
email/webhook notifications
standard support
```

### 14.3 Business

Purpose:

- serious operational usage;
- agencies;
- growing service fleets.

Possible capabilities:

```text
higher Agent limits
higher service limits
longer audit retention
longer health history
advanced alerting
role-based access
priority support
more integrations
```

### 14.4 Enterprise

Purpose:

- larger customers;
- compliance needs;
- custom support and security.

Possible capabilities:

```text
custom limits
SSO/OIDC/SAML
SCIM
custom audit retention
SLA
premium support
private networking options
custom data residency
enterprise contract
```

---

## 15. Free Tier Strategy

Cloud（云版） may need a free or developer tier to encourage adoption.

A good free tier should:

- let users experience the full core loop;
- allow real experimentation;
- limit scale, retention, and team features;
- avoid blocking basic actions and audit entirely;
- guide users toward paid plans when scale grows.

Bad free tier:

```text
Agent registration works, but commands do not.
Audit logs are completely disabled.
Health visibility is blocked.
```

Good free tier:

```text
Small number of Agents and Services.
Short retention.
Basic features available.
Upgrade for scale, teams, retention, and alerts.
```

---

## 16. Trial Strategy

Cloud（云版） may provide trials for paid plans.

Possible trial model:

```text
14-day Team trial
30-day Business trial
private beta access for early users
```

Trial should be simple and should not require complex billing implementation at the earliest prototype stage.

---

## 17. Overage Strategy

Cloud（云版） should define how usage beyond plan limits is handled.

Possible approaches:

### 17.1 Hard block

Block new usage immediately.

Example:

```text
Cannot register new Agent because plan limit is reached.
```

### 17.2 Soft warning

Allow usage temporarily and show warning.

Example:

```text
You have exceeded your Agent limit. Upgrade to continue adding Agents.
```

### 17.3 Overage billing

Charge for extra usage.

Example:

```text
Additional Agent per month.
Additional audit storage per GB-month.
```

### 17.4 Recommended early approach

For early Cloud（云版）, use simple limits and soft warnings where possible.

Do not build complex overage billing before Cloud（云版） usage patterns are understood.

---

## 18. Metering Strategy

### 18.1 Snapshot meters

Some dimensions are measured as current counts:

```text
active Agents
active Capsule Services
active Users
active Workspaces
```

### 18.2 Event meters

Some dimensions are measured over time:

```text
commands executed
alert notifications sent
audit events written
health reports received
```

### 18.3 Storage meters

Some dimensions are measured by stored data volume:

```text
audit storage
health history storage
log storage if implemented
```

### 18.4 MVP recommendation

Early Cloud（云版） MVP may not need full billing-grade metering.

It may start with:

- manual plan assignment;
- simple count limits;
- basic usage dashboard;
- no automated charging until product value is validated.

---

## 19. Plan Enforcement Points

Plan enforcement may happen at these points:

```text
Organization creation
Workspace creation
User invitation
Registration token creation
Agent registration
Capsule Service report
Alert rule creation
Retention processing
Notification sending
```

Recommended enforcement behavior:

- never trust client-side enforcement only;
- enforce on Backend;
- provide clear error messages;
- avoid disrupting existing critical Agent（代理） heartbeat unless necessary.

---

## 20. Billing and Agent（代理） Behavior

Billing state should not make Agent（代理） behavior unpredictable.

Recommended rules:

- existing Agents should still be able to heartbeat during grace period;
- new Agent（代理） registration may be blocked if quota is exceeded;
- command execution may be limited for suspended accounts depending on policy;
- audit should continue for denied or blocked operations;
- status visibility should remain available enough for users to understand the issue.

Avoid silent failures.

---

## 21. Billing and Data Retention

Plan may control retention.

Examples:

```text
Developer: 7-day audit retention
Team: 30-day audit retention
Business: 90-day audit retention
Enterprise: custom retention
```

Retention changes should be clear to users.

When downgrading, Cloud（云版） should define whether old data is:

- retained until natural expiration;
- truncated after grace period;
- archived;
- exportable before deletion.

---

## 22. Billing and Alerts

Alerting is a strong commercial feature.

Possible limits:

```text
maxAlertRules
allowedChannels
monthlyNotificationLimit
```

Example channel tiers:

```text
Developer: email only
Team: email + webhook
Business: email + webhook + Slack/Telegram
Enterprise: custom integrations
```

This is future planning only.

---

## 23. Billing and Support

Support level may be plan-based.

Possible support tiers:

```text
Community
Standard
Priority
Enterprise
```

Support value may include:

- response time;
- private support channel;
- deployment review;
- Agent（代理） diagnostics assistance;
- custom integration guidance.

---

## 24. Payment Provider Strategy

Cloud（云版） may eventually integrate with a payment provider.

Possible providers:

```text
Stripe
Paddle
Lemon Squeezy
FastSpring
manual invoice for enterprise
```

Provider selection depends on:

- company jurisdiction;
- tax handling;
- SaaS subscription support;
- payout countries;
- invoice requirements;
- B2B sales model.

This document does not choose a payment provider.

---

## 25. Cloud（云版） MVP Billing Candidate

A future Cloud（云版） MVP may use a lightweight billing model:

```text
private beta access
manual plan assignment
basic limits
no automatic payment at first
simple usage dashboard
```

This lets the product validate Cloud（云版） value before implementing complex billing.

Possible MVP limits:

```text
maxOrganizations
maxWorkspaces
maxAgents
maxCapsuleServices
auditRetentionDays
healthRetentionDays
```

---

## 26. CE（社区版） Reservations

CE（社区版） may reserve:

```text
workspaceId
createdBy
actorType
actorId
resourceType
resourceId
metadataJson
```

CE（社区版） must not implement:

```text
Plan
Subscription
BillingAccount
PaymentMethod
Invoice
UsageRecord
Entitlement
Quota
Cloud plan enforcement
Cloud payment provider integration
```

CE（社区版） should remain a genuinely useful open-source product.

---

## 27. Anti-Patterns

Avoid these patterns.

### 27.1 Crippling CE（社区版） to force Cloud（云版） upgrades

CE（社区版） should remain useful for self-hosted users.

### 27.2 Charging too early before value is clear

Cloud（云版） should validate usage and customer value before complex billing automation.

### 27.3 Billing on confusing dimensions

Avoid pricing dimensions users cannot understand.

### 27.4 Hard-blocking operational visibility

Users should still understand what is happening even when quota or billing issues occur.

### 27.5 Making billing part of Agent（代理） protocol

Agent（代理） protocol should not depend on pricing logic.

Billing decisions belong to Cloud（云版） Backend.

### 27.6 Storing raw payment data

Do not store raw card data. Use payment provider tokens and hosted billing systems.

---

## 28. Risks

### 28.1 Pricing complexity risk

Too many meters may confuse users.

Mitigation:

- start with simple plan limits.

### 28.2 Cost mismatch risk

Flat plans may not cover heavy usage.

Mitigation:

- monitor usage patterns;
- add overage or higher tiers later.

### 28.3 Trust risk

Users may feel CE（社区版） is intentionally weakened.

Mitigation:

- keep CE（社区版） useful;
- charge for Cloud（云版） managed value.

### 28.4 Payment provider risk

Provider restrictions may affect global sales.

Mitigation:

- choose provider carefully;
- support manual enterprise invoicing.

### 28.5 Quota disruption risk

Hard quota blocks may disrupt operations.

Mitigation:

- use grace periods and clear warnings.

---

## 29. Billing Acceptance Criteria

Cloud（云版） billing model planning is acceptable when:

- billing is clearly Cloud（云版）-only;
- CE（社区版） remains free of billing infrastructure;
- monetization is based on managed service value and scale;
- plan dimensions are understandable;
- Agent（代理） and Capsule Service（胶囊服务） counts are considered primary dimensions;
- retention and alerting are recognized as paid-value areas;
- MVP billing can start simple;
- hard quota behavior does not silently break governance;
- payment provider choice is deferred until business needs are clearer.

---

## 30. Summary

Opstage（运维舞台） Cloud（云版） billing should support a sustainable hosted SaaS business without undermining the open-source CE（社区版） foundation.

The most important billing rule is:

> Charge for Cloud（云版） convenience, scale, retention, collaboration, and support — not for artificially breaking the core Capsule governance loop.
