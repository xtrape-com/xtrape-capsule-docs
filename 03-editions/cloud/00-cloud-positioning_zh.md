<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 00-cloud-positioning.md
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

# Cloud（云版） Positioning

- Status: Planning
- Edition: Cloud（云版）
- Priority: Future
- Audience: founders, product designers, architects, cloud engineers, AI coding agents

This document 定义 the product positioning of **Opstage（运维舞台） Cloud（云版）**.

Opstage（运维舞台） Cloud（云版） is the future hosted SaaS edition of the `xtrape-capsule` product family. It should extend the same Agent（代理）-based Capsule governance model used by CE（社区版） and EE（企业版）, but provide it as a managed cloud service.

Cloud（云版） is not a CE（社区版） v0.1 implementation requirement.

---

## 1. Positioning Statement

Opstage（运维舞台） Cloud（云版） is:

> A hosted SaaS control plane for Capsule Services.

It helps teams register, observe, configure, operate, and audit Capsule Services without self-hosting Opstage（运维舞台） Backend and UI.

Cloud（云版） should preserve the core Capsule governance idea:

```text
Capsule Services stay in the customer's environment.
Agents connect outbound to Opstage Cloud.
Opstage Cloud provides visibility, operations, audit, and collaboration.
```

---

## 2. Product Category

Opstage（运维舞台） Cloud（云版） belongs to a new product category:

```text
Managed runtime governance for lightweight services
```

It is related to, but different from:

- configuration centers;
- observability platforms;
- service meshes;
- Kubernetes control planes;
- workflow platforms;
- remote administration tools.

Opstage（运维舞台） Cloud（云版） should not be positioned as a replacement for all of these tools.

Its core value is Capsule Service（胶囊服务） governance.

---

## 3. Cloud（云版） Product Goal

The product goal of Opstage（运维舞台） Cloud（云版） is:

> Provide a managed, team-oriented, multi-tenant control plane for lightweight services, AI automation services, integration services, and operational workers.

Cloud（云版） should reduce the cost of operating Opstage（运维舞台） itself while improving:

- team collaboration;
- centralized visibility;
- managed audit retention;
- managed alerting;
- easier onboarding;
- cross-environment governance;
- commercial support.

---

## 4. Core Value Proposition

Opstage（运维舞台） Cloud（云版） 提供 value through five product promises.

### 4.1 Managed control plane

Users do not need to install, upgrade, back up, or monitor Opstage（运维舞台） Backend.

The platform provider operates the control plane.

### 4.2 Outbound Agent（代理） connectivity

Customer-side Agents connect outbound to Cloud（云版）.

This avoids exposing customer service ports to the public internet.

### 4.3 Team-oriented governance

Cloud（云版） 支持 organizations, workspaces, teams, roles, and collaboration.

This makes Opstage（运维舞台） useful beyond single-developer self-hosting.

### 4.4 Managed audit and reporting

Cloud（云版） can provide longer audit retention, search, export, and reporting as managed capabilities.

### 4.5 Commercial reliability

Cloud（云版） can provide managed upgrades, backups, monitoring, support, and eventually SLA commitments.

---

## 5. Target Users

Opstage（运维舞台） Cloud（云版） is designed for:

- small teams that do not want to self-host;
- AI automation teams;
- integration service operators;
- agencies managing multiple customer environments;
- startups with many internal lightweight services;
- teams that need basic governance but lack dedicated platform engineers;
- organizations that prefer managed SaaS for operational tooling.

---

## 6. Target Use Cases

### 6.1 Managed integration governance

A team runs several integration services across different environments and wants a single hosted console for status, health, actions, commands, and audit.

### 6.2 AI automation operations

A team runs AI agents, browser automation workers, account/session services, or connector services and wants centralized operational visibility.

### 6.3 Agency operations

An agency manages automation services for several customers and needs workspace separation, auditability, and team access.

### 6.4 Distributed lightweight service fleet

A company runs many small services across VPS, home servers, private servers, and cloud instances. Cloud（云版） 提供 one control plane.

### 6.5 Managed audit and reporting

A team wants to know who executed which actions, on which services, with what result, without managing audit storage itself.

---

## 7. Cloud（云版） Differentiation

Cloud（云版） should differentiate through:

- Capsule Service（胶囊服务） model;
- Agent（代理）-based outbound governance;
- lightweight service focus;
- operational commands through predefined actions;
- safe `secretRef` boundary;
- hosted visibility and audit;
- future team and organization collaboration;
- managed experience without requiring Kubernetes.

Cloud（云版） should avoid competing directly as a full observability stack or Kubernetes platform in the first phase.

---

## 8. Relationship with CE（社区版）

CE（社区版） is the open-source self-hosted edition.

Cloud（云版） is the hosted managed edition.

### 8.1 CE（社区版） value

CE（社区版） 提供:

- trust;
- self-hosting;
- open-source adoption;
- local control;
- lightweight single-node deployment;
- proof of the Capsule governance model.

### 8.2 Cloud（云版） value

Cloud（云版） 提供:

- managed backend;
- managed UI;
- team collaboration;
- multi-tenant workspaces;
- managed audit retention;
- managed alerting;
- commercial support;
- lower operational burden.

### 8.3 共享 kernel

Both CE（社区版） and Cloud（云版） should share the same core concepts:

```text
Agent
CapsuleService
Manifest
HealthReport
ConfigItem
ActionDefinition
Command
CommandResult
AuditEvent
Status values
secretRef
```

Cloud（云版） should be a managed evolution of CE（社区版）, not a different incompatible product.

---

## 9. Relationship with EE（企业版）

EE（企业版） is the future enterprise private deployment edition.

Cloud（云版） and EE（企业版） should differ mainly by deployment and operating responsibility.

||Area|EE（企业版）|Cloud（云版）||
|---|---|---|
||部署|customer private environment|hosted SaaS||
||Operations|customer or vendor support|provider-operated||
||Database|customer-managed|provider-managed||
||Identity|enterprise identity|SaaS organization/team identity||
||Billing|commercial license|subscription billing||
||Data boundary|customer-controlled|shared responsibility||

Both should preserve the same Capsule governance model.

---

## 10. Data Boundary Positioning

Cloud（云版） must be very clear about what data it stores.

Cloud（云版） may store governance metadata:

- Agent（代理） metadata;
- Capsule Service（胶囊服务） metadata;
- health reports;
- config metadata;
- action metadata;
- command metadata;
- command results;
- audit events;
- usage records.

Cloud（云版） should avoid storing raw operational secrets by default.

Recommended positioning:

> Opstage（运维舞台） Cloud（云版） stores governance metadata and secret references, not raw customer secrets by default.

Sensitive data should stay in:

- customer environment;
- Agent（代理）-local secret store;
- customer-managed Vault;
- customer cloud secret manager.

---

## 11. Secret Boundary

Cloud（云版） should use `secretRef` as the main secret boundary.

Examples:

```text
agent-local://agent-001/secrets/chatgpt/account-001
customer-vault://prod/integration-worker/account-001
cloud-secret://org/workspace/secret-key
```

Cloud（云版） may later provide managed secrets as an optional paid capability, but this should be explicit.

The default product message should be conservative:

> Your secrets can remain in your environment. Cloud（云版） only needs references and operational metadata.

---

## 12. Agent（代理） Connectivity Positioning

Cloud（云版） should emphasize outbound Agent（代理） connectivity.

Recommended message:

> Agents connect outbound to Opstage（运维舞台） Cloud（云版） over HTTPS. You do not need to expose your Capsule Services to the public internet.

This is especially important for users running services behind NAT, firewalls, home networks, or private cloud environments.

---

## 13. Commercial Positioning

Cloud（云版） commercial value should come from managed service convenience and team features, not from disabling CE（社区版）.

Good commercial value areas:

- managed hosting;
- backups;
- upgrades;
- audit retention;
- alerting;
- team collaboration;
- organization management;
- usage dashboards;
- support;
- SLA;
- managed Agent（代理） gateway.

Bad commercial strategy:

- CE（社区版） cannot run actions;
- CE（社区版） cannot view audit logs;
- CE（社区版） Agent（代理） SDK is intentionally incomplete;
- CE（社区版） is only a marketing shell.

Cloud（云版） should monetize convenience, scale, collaboration, and reliability.

---

## 14. Cloud（云版） Messaging

### 14.1 Short description

```text
Hosted control plane for Capsule Services.
```

### 14.2 Longer description

```text
Opstage Cloud helps teams manage Capsule Services across environments with hosted visibility, predefined operations, command tracking, and audit logs through outbound Agents.
```

### 14.3 Developer-facing message

```text
Install an Agent SDK or Agent runtime, connect it to Opstage Cloud, and make your lightweight services visible and operable without hosting the control plane yourself.
```

### 14.4 安全-facing message

```text
Agents connect outbound, and operational secrets can remain in your environment through secret references.
```

---

## 15. What Cloud（云版） Is Not

Cloud（云版） should not be positioned as:

- a full Kubernetes platform;
- a full observability replacement;
- a full configuration center;
- a remote shell service;
- a browser automation platform by itself;
- a secret vault by default;
- a workflow engine as its first identity.

Cloud（云版） may integrate with some of these areas later, but its first identity should remain Capsule governance.

---

## 16. Cloud（云版） MVP Positioning

A future Cloud（云版） MVP should be positioned as:

> Hosted CE（社区版）-like governance with team and workspace support.

Possible Cloud（云版） MVP capabilities:

- hosted UI and Backend;
- user registration;
- organization/workspace creation;
- Agent（代理） registration token creation;
- remote Agent（代理） heartbeat;
- Capsule Service（胶囊服务） visibility;
- health visibility;
- predefined action execution;
- command results;
- audit logs;
- basic plan limits or private beta access.

Cloud（云版） MVP should not start as a full enterprise platform.

---

## 17. Competitive Framing

Cloud（云版） should be framed around the specific pain of many small services.

Problem statement:

```text
AI-era teams will create more lightweight services, agents, workers, connectors, and account/session services. These services are easy to create but hard to govern over time.
```

Opstage（运维舞台） Cloud（云版） answer:

```text
Use a hosted Agent-based control plane to make these services visible, operable, and auditable across environments.
```

This positioning is narrower and sharper than generic DevOps tooling.

---

## 18. Risks in Positioning

### 18.1 Too broad

If Cloud（云版） is positioned as observability + config + workflow + Kubernetes + agent platform, users will not understand its core value.

Mitigation:

- keep the message focused on Capsule governance.

### 18.2 Too close to CE（社区版）

If Cloud（云版） only looks like hosted CE（社区版） without team, retention, alerting, or managed value, users may not pay.

Mitigation:

- emphasize managed operations, collaboration, retention, and reliability.

### 18.3 Trust concerns

Users may worry about sending service metadata to Cloud（云版）.

Mitigation:

- document data boundary;
- keep secrets customer-controlled by default;
- provide CE（社区版） and EE（企业版） alternatives.

### 18.4 Premature enterprise complexity

Cloud（云版） may become too complex before product-market fit.

Mitigation:

- start with hosted CE（社区版）-like governance and iterate.

---

## 19. Success Criteria

Cloud（云版） positioning is successful when users understand that:

- Cloud（云版） is hosted Opstage（运维舞台）, not a separate product;
- Agents connect outbound from customer environments;
- Capsule Services can remain customer-side;
- Cloud（云版） 提供 managed visibility, actions, commands, and audit;
- Cloud（云版） is suitable for teams and multiple environments;
- CE（社区版） remains available for self-hosted users;
- EE（企业版） is available later for private enterprise deployment;
- raw secrets are not required by default.

---

## 20. Summary

Opstage（运维舞台） Cloud（云版） should be positioned as the hosted SaaS evolution of the Capsule governance model.

It should make lightweight services visible, operable, and auditable across environments without requiring users to self-host the control plane.

The most important Cloud（云版） positioning rule is:

> Cloud（云版） sells managed governance and collaboration, not control over customer secrets or a crippled replacement for CE（社区版）.
