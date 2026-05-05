---
status: draft
audience: architects
stability: unstable
last_reviewed: 2026-05-05
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 04-design-principles.md
翻译状态 / Translation Status: 已翻译 / Translated
生成时间 / Generated: 2026-05-01 09:28:53
================================================================================
注意 / Notes:
- 技术术语如 Capsule Service、Agent、Opstage 等保留英文或采用中英对照
- 代码块中的内容不翻译
- 文件路径和 URL 不翻译
- 保持原有的 Markdown 格式结构
================================================================================
-->

# xtrape-capsule 设计 Principles

- Status: Conceptual Guidance
- Edition: 共享
- Priority: 高
- Audience: architects, developers, AI coding agents, reviewers

This document 定义 the design principles of the `xtrape-capsule` domain.

These principles should guide all CE（社区版）, EE（企业版）, and Cloud（云版） designs. CE（社区版） v0.1 should follow them strictly while keeping implementation lightweight.

---

## 1. Principle Summary

`xtrape-capsule` follows these core principles:

1. Capsule Services must remain independently runnable.
2. Opstage（运维舞台） is a governance plane, not a business runtime dependency.
3. Services enter governance through registered and authorized Agents.
4. Agent（代理） communication should be outbound-first.
5. CE（社区版） must stay lightweight and self-hosted first.
6. Specifications should be stable across languages and editions.
7. 实现 may be partial, but it must not violate long-term contracts.
8. Sensitive data should be referenced, not casually stored.
9. Actions must be explicit, predefined, and auditable.
10. 状态 freshness must be visible.
11. UI, backend, and agent responsibilities must stay separated.
12. CE（社区版） should reserve extension points for EE（企业版） and Cloud（云版） without implementing their full complexity.

---

## 2. Independent Capsule Runtime

A Capsule Service（胶囊服务） must be able to start and perform its core business work without Opstage（运维舞台） being online.

Correct model:

```text
Capsule Service starts
    ↓
Capsule Service performs core work
    ↓
Agent connects to Opstage if available
    ↓
Opstage provides governance features
```

Incorrect model:

```text
Opstage is unavailable
    ↓
Capsule Service cannot start
```

### Rationale

Opstage（运维舞台） 提供 governance, not mandatory runtime existence.

If every Capsule Service（胶囊服务） depends on Opstage（运维舞台） for startup, Opstage（运维舞台） becomes a single point of failure for all services.

### CE（社区版） v0.1 Requirement

The demo Capsule Service（胶囊服务） must be able to start even if Opstage（运维舞台） Backend is unavailable.

The embedded Agent（代理） should retry registration or heartbeat in the background without preventing the service from running.

---

## 3. Governance Plane, Not Business Runtime

Opstage（运维舞台） should observe, configure, command, audit, and govern Capsule Services.

Opstage（运维舞台） should not become the place where every Capsule Service（胶囊服务）'s business logic is implemented.

Opstage（运维舞台） responsibilities:

- service listing;
- Agent（代理） registration;
- status display;
- health visibility;
- command creation;
- action result tracking;
- configuration metadata visibility;
- audit logging;
- future observability and enterprise governance.

Capsule Service（胶囊服务） responsibilities:

- business logic;
- external platform integration;
- worker execution;
- account/session handling;
- local runtime behavior;
- execution of predefined actions;
- reporting status back through Agent（代理）.

### Anti-pattern

Do not implement service-specific business operations directly inside Opstage（运维舞台） Backend.

If an operation belongs to a Capsule Service（胶囊服务）, Opstage（运维舞台） should issue a command or action request and let the Capsule Service（胶囊服务） execute it through its Agent（代理）.

---

## 4. Agent（代理）-Based Registration

Opstage（运维舞台） must not directly assume access to arbitrary services.

A Capsule Service（胶囊服务） enters governance through a registered and authorized Agent（代理）.

The core model is:

```text
Capsule Service
    ↓
Agent
    ↓
Opstage Backend
    ↓
Opstage UI
```

### Registration Rules

1. An Agent（代理） uses a registration token for first registration.
2. Opstage（运维舞台） validates the registration token.
3. Opstage（运维舞台） issues an Agent（代理） token.
4. The Agent（代理） uses the Agent（代理） token for ongoing communication.
5. Opstage（运维舞台） stores only token hashes.
6. Tokens must be revocable.

### CE（社区版） v0.1 Requirement

CE（社区版） v0.1 must implement:

- registration token;
- Agent（代理） token;
- Agent（代理） heartbeat;
- Agent（代理） status;
- Capsule Service（胶囊服务） report;
- command polling;
- command result reporting.

---

## 5. Outbound-First Agent（代理） Communication

Agents should actively connect to Opstage（运维舞台） Backend.

Opstage（运维舞台） should not require direct inbound access to Agents or Capsule Services in CE（社区版） v0.1.

Preferred CE（社区版） flow:

```text
Agent -> Backend: register
Agent -> Backend: heartbeat
Agent -> Backend: report service status
Agent -> Backend: fetch pending commands
Agent -> Backend: report command result
```

### Rationale

Outbound-first communication works better for:

- local development;
- self-hosted deployments;
- NAT environments;
- customer-side servers;
- future Cloud（云版） SaaS model;
- fewer exposed inbound ports.

### Future Extension

Future versions may support:

- WebSocket channels;
- gRPC streaming;
- message queues;
- long-running log streams;
- interactive operation sessions.

CE（社区版） v0.1 should start with simple HTTP and polling.

---

## 6. Lightweight CE（社区版） First

CE（社区版） is the current implementation target.

CE（社区版） v0.1 should be lightweight, open-source, and self-hosted.

Preferred CE（社区版） v0.1 choices:

- SQLite by default;
- single-node deployment;
- single-image or simple Docker deployment;
- simple local admin authentication;
- Node.js embedded Agent（代理） SDK;
- HTTP heartbeat;
- command polling;
- basic audit log;
- basic health visibility;
- predefined actions.

Avoid in CE（社区版） v0.1:

- Kubernetes requirement;
- service mesh;
- distributed queue;
- enterprise RBAC;
- SSO;
- multi-tenant billing;
- full observability stack;
- arbitrary remote shell execution;
- mandatory MySQL/PostgreSQL;
- Java/Spring-only assumptions.

### Rationale

CE（社区版） should prove the core model with the lowest possible deployment and adoption cost.

---

## 7. Stable Cross-Language Specifications

`xtrape-capsule` must not be tied to one language or framework.

Specifications should work for:

- Node.js;
- Java;
- Python;
- Go;
- shell workers;
- browser automation workers;
- future runtimes.

共享 specifications include:

- Capsule Manifest Spec;
- Capsule Management Contract;
- Agent（代理） Registration Spec;
- Health Spec;
- Action Spec;
- Config Spec;
- Command Spec;
- Audit Event Spec;
- 状态 Model Spec.

### CE（社区版） v0.1 Rule

CE（社区版） v0.1 may implement only a subset of these specifications, but it should not introduce names, fields, or behaviors that contradict the long-term shared specs.

---

## 8. Partial 实现 Without Contract Violation

A specification can be larger than the CE（社区版） v0.1 implementation.

This is acceptable if CE（社区版） clearly states what subset it implements.

Example:

```text
Spec supports: embedded, sidecar, external Agent modes
CE v0.1 implements: embedded only
```

This is acceptable.

Bad example:

```text
Spec defines Agent mode as embedded / sidecar / external
CE stores mode as isNodeOnly = true
```

This blocks future evolution and violates the long-term model.

---

## 9. Secret Reference First

Sensitive data should be represented by references when possible.

Examples:

```text
agent-local://agent-id/secrets/chatgpt/account-001
vault://secret/path
opstage-secret://workspace/key
```

CE（社区版） v0.1 does not need a full secret store, but it should avoid spreading raw secrets into normal fields.

### Rules

- Do not store raw Agent（代理） tokens.
- Store only token hashes.
- Do not show sensitive config values in the UI.
- Prefer `secretRef` fields over raw secret values.
- 设计 future compatibility with external secret stores.

---

## 10. Explicit and Auditable Actions

Actions must be explicit and predefined.

Good examples:

```text
runHealthCheck
reloadConfig
refreshSession
clearExpiredSessions
rotateProxy
```

Bad examples:

```text
runShell
exec
bash
customCommand
```

### CE（社区版） v0.1 Rule

CE（社区版） v0.1 should not support arbitrary shell command execution from the UI.

Every action execution should create:

- a Command;
- a CommandResult;
- an AuditEvent.

---

## 11. 状态 Freshness Must Be Visible

Opstage（运维舞台） must distinguish between:

- last reported status;
- effective current status;
- last reported time;
- freshness of the report.

Example:

```json
{
  "reportedStatus": "ONLINE",
  "effectiveStatus": "STALE",
  "lastReportedAt": "2026-04-30T10:21:00Z",
  "reason": "agent offline"
}
```

### Rationale

If an Agent（代理） goes offline, Opstage（运维舞台） should not keep showing the Capsule Service（胶囊服务） as confidently online just because the last report was healthy.

### CE（社区版） v0.1 Requirement

CE（社区版） v0.1 should calculate offline or stale status based on heartbeat timeout.

---

## 12. Separate UI, Backend, and Agent（代理） Responsibilities

The system should be conceptually separated into:

```text
Opstage UI
Opstage Backend
Opstage Agent / Agent SDK
Capsule Service
```

Even if CE（社区版） v0.1 is packaged as a single deployable application, the code and responsibilities should stay separated.

### UI Responsibilities

- display dashboard;
- list Agents;
- list Capsule Services;
- show service details;
- show health and status;
- trigger predefined actions;
- show command results;
- show audit logs.

### Backend Responsibilities

- authenticate users;
- manage Agent（代理） registration;
- store Agent（代理） state;
- store Capsule Service（胶囊服务） state;
- create commands;
- receive command results;
- store audit events;
- calculate effective status;
- serve UI API.

### Agent（代理） Responsibilities

- register;
- heartbeat;
- report manifest;
- report health;
- fetch commands;
- execute predefined actions;
- report command results.

### Capsule Service（胶囊服务） Responsibilities

- business function;
- action handlers;
- health provider;
- config metadata provider;
- manifest provider.

---

## 13. CE（社区版） Extension Points for EE（企业版） and Cloud（云版）

CE（社区版） should not implement heavy EE（企业版） or Cloud（云版） capabilities in v0.1, but it should preserve extension points.

Important extension points:

||Area|CE（社区版） v0.1|Future EE（企业版） / Cloud（云版）||
|---|---|---|
||Database|SQLite|MySQL, PostgreSQL, HA database||
||Workspace|default only|multi-workspace, organization, tenant||
||Auth|local admin|RBAC, SSO, OIDC, LDAP||
||Agent（代理）|Node.js embedded|sidecar, external, Java, Python, Docker, Kubernetes||
||Commands|polling|WebSocket, gRPC, queue-based delivery||
||Logs|basic or none|centralized logs, search, retention||
||Metrics|health only|time-series metrics, dashboards||
||Secrets|secretRef-ready|vault integration, managed secret store||
||部署|single-node|cluster, HA, cloud-hosted||
||Billing|none|Cloud（云版） subscription, usage billing||

---

## 14. 文档 as 开发 Contract

文档 is part of the development contract.

Before implementing a feature, check:

- concept documents in `01-capsule/`;
- shared specifications in `02-specs/`;
- CE（社区版） scope in `03-editions/ce/`;
- Opstage（运维舞台） documents in `04-opstage/`;
- Agent（代理） documents in `05-agents/`.

If a feature is not described clearly, update the documentation before or together with the implementation.

AI coding agents should treat CE（社区版） implementation documents as the current source of truth and EE（企业版）/Cloud（云版） documents as future planning references.

---

## 15. Review Checklist

Use this checklist when reviewing a design or implementation.

### 15.1 Independence

- Can the Capsule Service（胶囊服务） run without Opstage（运维舞台）?
- Does the Agent（代理） fail gracefully if Backend is unavailable?

### 15.2 Agent（代理） Governance

- Does the service enter governance through Agent（代理） registration?
- Are Agent（代理） tokens handled securely?
- Is every service report associated with an Agent（代理）?

### 15.3 Lightweight CE（社区版）

- Does the implementation avoid unnecessary enterprise features?
- Can it run with SQLite?
- Can it run in a simple local or Docker setup?

### 15.4 规范 Alignment

- Does it use shared names and statuses?
- Does it avoid blocking sidecar or external Agent（代理） support?
- Does it avoid Node.js-only assumptions in shared models?

### 15.5 安全

- Are raw tokens avoided in storage?
- Are sensitive values hidden or represented by references?
- Are actions predefined?
- Are operations auditable?

### 15.6 状态 Correctness

- Is stale status handled?
- Is heartbeat timeout handled?
- Is last reported status separated from effective status?

### 15.7 Separation of Responsibilities

- Is business logic kept inside Capsule Services?
- Is Opstage（运维舞台） kept as governance plane?
- Are UI, Backend, and Agent（代理） concerns separated?

---

## 16. Anti-Patterns

Avoid these anti-patterns.

### 16.1 Building a full microservice platform in CE（社区版） v0.1

CE（社区版） v0.1 should not become a Spring Cloud（云版）, Kubernetes, or service mesh platform.

### 16.2 Making Opstage（运维舞台） mandatory for service startup

Opstage（运维舞台） should not be required for Capsule Service（胶囊服务） startup.

### 16.3 Adding arbitrary command execution too early

Arbitrary shell execution creates serious security risk. Use predefined actions first.

### 16.4 Storing secrets directly

Do not store raw tokens, passwords, cookies, or credentials in ordinary fields.

### 16.5 Mixing EE（企业版）/Cloud（云版） requirements into CE（社区版） prototype

Do not implement multi-tenant billing, SSO, cluster deployment, or full observability stack in CE（社区版） v0.1.

### 16.6 Over-normalizing the manifest too early

Use JSON for flexible metadata in CE（社区版） v0.1. Normalize later when the model stabilizes.

---

## 17. Summary

The most important design idea of `xtrape-capsule` is:

> Keep services lightweight and independent, but make them governable through Agents and Opstage（运维舞台）.

CE（社区版） v0.1 should be simple enough to run easily and strong enough to prove the model.

Future EE（企业版） and Cloud（云版） editions should grow from the same principles without forcing CE（社区版） to become heavy too early.
