<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 00-overview.md
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

# xtrape-capsule 概述

- Status: Conceptual Guidance
- Edition: 共享
- Priority: 高
- Audience: architects, developers, AI coding agents

`xtrape-capsule` is the lightweight service architecture domain of Xtrape. It 定义 the concept, specifications, runtime governance model, agent integration model, and edition strategy for Capsule Services.

`xtrape-capsule-opstage` is one core subsystem under this domain. It 提供 the runtime governance platform for Capsule Services, but it is not the whole `xtrape-capsule` domain.

The current implementation focus is **CE（社区版） / Community 版本**. EE（企业版） / Enterprise 版本 and Cloud（云版） / SaaS 版本 are future planning targets. CE（社区版） should reserve extension points for them, but it should not implement their full capabilities in early versions.

---

## 1. Background

AI-era applications are producing more and more small service units:

- CAPI services for wrapping web or platform capabilities;
- account pool services for managing registered accounts;
- browser automation workers;
- OTP readers;
- proxy checkers;
- connector services;
- task workers;
- AI agent runtimes;
- session managers;
- lightweight internal tools.

These services are usually not complex by themselves. They may be a Node.js service, a Playwright worker, a Python script, a small Java service, or an adapter that wraps a third-party platform capability.

The real problem is not how to implement these services. The real problem is:

> When the number of small services keeps growing, how can the team remember, observe, configure, audit, operate, and govern them over the long term without turning them into unmanaged islands?

Traditional microservice platforms, configuration centers, and monitoring systems do not fully match this problem:

- Microservice frameworks are often too heavy for these small capability units.
- 配置 centers usually focus on key-value configuration, not runtime governance.
- 监控 systems can observe status, but they usually do not provide business-level control.
- Internal admin panels become fragmented if each small service builds its own UI.

`xtrape-capsule` is proposed to solve this gap.

---

## 2. Problem Statement

Without a unified Capsule governance model, lightweight services tend to suffer from the following problems.

### 2.1 Service Forgetfulness

A team may create many small services over time, but after several months it becomes unclear:

- which services exist;
- where they are deployed;
- which ones are running;
- which ones are obsolete;
- which ones are unhealthy;
- which services are connected to which accounts, sessions, proxies, or capabilities.

### 2.2 Fragmented Management

If every service implements its own admin UI, the system becomes difficult to maintain:

- duplicated UI code;
- inconsistent permission model;
- inconsistent audit model;
- inconsistent configuration model;
- inconsistent health checks;
- no unified operation entry.

### 2.3 Runtime Blindness

For AI automation and CAPI services, runtime state is often more important than static configuration:

- whether an account is still valid;
- whether a browser session is alive;
- whether a provider is rate-limited;
- whether a service is degraded;
- whether a worker is stuck;
- whether a command succeeded;
- whether an action was performed by a user, an agent, or the system.

Traditional configuration centers do not capture this runtime model well.

### 2.4 Technology Stack Diversity

Capsule Services may be implemented in different languages and runtime environments:

- Node.js;
- Java;
- Python;
- Go;
- browser automation runtimes;
- shell scripts;
- local workers;
- containerized services.

A Java-only or Spring-Cloud（云版）-only framework is not flexible enough for this target.

### 2.5 Private 部署 and Cloud（云版） Evolution

The system should support lightweight self-hosted deployment first, but it should not block future enterprise and SaaS editions.

Therefore, CE（社区版） must stay simple, while the architecture must preserve extension points for:

- stronger databases;
- cluster deployment;
- multi-workspace and multi-tenant models;
- RBAC and SSO;
- centralized logs and metrics;
- richer agent modes;
- hosted cloud control plane.

---

## 3. Vision

`xtrape-capsule` 定义 a lightweight service architecture for AI-era service ecosystems.

Its vision is:

> Make small capability services easy to register, observe, configure, audit, and operate without forcing them into a heavy microservice framework.

---

## 4. Core 概念

The core managed unit is the **Capsule Service（胶囊服务）**.

A Capsule Service（胶囊服务） is:

> A lightweight, self-contained, independently runnable, agent-governed service unit that exposes a clear capability, connector, worker, automation process, account resource, session resource, or runtime adapter.

A Capsule Service（胶囊服务） should be:

- independently runnable;
- language-neutral;
- observable;
- configurable;
- auditable;
- operable through a registered Agent（代理）;
- free from hard dependency on Opstage（运维舞台） for startup.

---

## 5. Relationship with Opstage（运维舞台）

`xtrape-capsule-opstage` is the runtime governance platform for Capsule Services.

It 提供:

- Web UI;
- backend control plane;
- agent registration;
- service registry;
- health visibility;
- command and action execution;
- configuration visibility;
- audit records;
- future observability, alerting, and enterprise governance.

The relationship is:

```text
xtrape-capsule
    ├── concept and domain model
    ├── shared specifications
    ├── agent model
    ├── runtime support
    ├── edition strategy
    └── xtrape-capsule-opstage
            ├── UI
            ├── Backend
            └── Agent integration
```

Or more simply:

> `xtrape-capsule` 定义 Capsule Services. `xtrape-capsule-opstage` manages Capsule Services.

---

## 6. Relationship with Microservices

Capsule Services are not a replacement for all microservices.

They are intended for smaller, lighter, capability-oriented service units.

||Dimension|Microservice|Capsule Service（胶囊服务）||
|---|---|---|
||Primary split|Business domain|Capability / worker / connector / runtime unit||
||Typical size|Medium to large|Small to medium||
||Lifecycle|Long-running business service|Long-running, short-running, task-like, or worker-like||
||Technology stack|Often standardized|Multi-language and multi-runtime||
||Governance|Service registry, gateway, config, tracing|Agent（代理） registration, runtime status, actions, audit, config visibility||
||Typical examples|payment service, order service, user service|CAPI wrapper, account pool, browser worker, OTP reader, proxy checker||

A traditional microservice may also be registered as a Capsule Service（胶囊服务） if it exposes or integrates with the Capsule governance contract.

---

## 7. 高-Level 架构

The long-term architecture has three primary roles:

```text
Capsule Service
    ↓
Opstage Agent
    ↓
Opstage Backend
    ↓
Opstage UI
```

### 7.1 Capsule Service（胶囊服务）

The managed lightweight service. It may be implemented in Node.js, Java, Python, or another runtime.

### 7.2 Opstage（运维舞台） Agent（代理）

The governance bridge between Capsule Service（胶囊服务） and Opstage（运维舞台） Backend.

Agent（代理） modes:

- embedded agent;
- sidecar agent;
- external agent.

CE（社区版） v0.1 focuses on Node.js embedded agent.

### 7.3 Opstage（运维舞台） Backend

The control plane backend. It stores agent state, service state, commands, audit logs, and configuration metadata.

### 7.4 Opstage（运维舞台） UI

The human-facing web console for viewing and operating Capsule Services.

---

## 8. Core 设计 Principles

### 8.1 Capsule Services must run independently

A Capsule Service（胶囊服务） should not require Opstage（运维舞台） to be online in order to start or perform its core business work.

Opstage（运维舞台） 提供 governance, not mandatory runtime existence.

### 8.2 Opstage（运维舞台） manages through Agents

Opstage（运维舞台） should not directly scan or take over arbitrary services.

A service enters governance through a registered and authorized Agent（代理）.

### 8.3 Agent（代理） connection should be outbound-first

Agents should actively connect to Opstage（运维舞台） Backend.

This 支持:

- private deployment;
- NAT environments;
- customer-side networks;
- Cloud（云版） SaaS future model;
- fewer exposed inbound ports.

### 8.4 CE（社区版） should remain lightweight

CE（社区版） v0.1 should avoid heavy dependencies and focus on the smallest useful governance loop.

### 8.5 Specifications should be stable

Cross-edition specifications should be designed carefully. Implementations may be partial, but they should not contradict the long-term model.

### 8.6 Business logic stays in Capsule Services

Opstage（运维舞台） should not become the place where every service's business logic is implemented.

Opstage（运维舞台） coordinates, observes, configures, audits, and commands. Capsule Services perform their own business functions.

---

## 9. 版本 Strategy

`xtrape-capsule` is planned in three editions:

||版本|Name|状态|Purpose||
|---|---|---|---|
||CE（社区版）|Community 版本|Current implementation target|Lightweight, open-source, self-hosted edition||
||EE（企业版）|Enterprise 版本|Future planning|Private-deployment commercial edition||
||Cloud（云版）|SaaS Cloud（云版） 版本|Future planning|Hosted SaaS edition||

### 9.1 CE（社区版）

CE（社区版） should prove the core model with minimal operational cost.

CE（社区版） focuses on:

- SQLite-first storage;
- single-node deployment;
- simple local admin;
- Node.js embedded agent SDK;
- agent registration;
- heartbeat;
- service status display;
- basic health;
- basic actions and commands;
- basic audit log.

### 9.2 EE（企业版）

EE（企业版） will target enterprise private deployment.

Future EE（企业版） capabilities may include:

- MySQL / PostgreSQL official support;
- cluster deployment;
- HA;
- RBAC;
- SSO / OIDC / LDAP;
- centralized logs and metrics;
- monitoring dashboards;
- secret vault integration;
- richer agent modes;
- enterprise installation and support.

### 9.3 Cloud（云版）

Cloud（云版） will target hosted SaaS usage.

Future Cloud（云版） capabilities may include:

- multi-tenant workspace model;
- subscription billing;
- hosted backend;
- agent outbound connectivity;
- cloud-side metadata and status;
- customer-side secret boundary;
- cloud alerting and reporting.

---

## 10. CE（社区版） v0.1 实现 Boundary

CE（社区版） v0.1 is the current implementation target.

It should implement:

- Opstage（运维舞台） Backend;
- Opstage（运维舞台） UI;
- SQLite persistence;
- Node.js embedded Agent（代理） SDK;
- demo Capsule Service（胶囊服务）;
- agent registration with registration token;
- agent token for later communication;
- heartbeat;
- service report;
- health report;
- command polling;
- command result report;
- basic action execution;
- basic audit log;
- simple Docker deployment.

It should not implement:

- multi-tenant Cloud（云版） model;
- enterprise RBAC;
- SSO;
- Kubernetes deployment;
- distributed queue;
- full centralized log platform;
- full metrics and dashboard system;
- billing;
- advanced secret vault integration;
- Java or Python SDK unless explicitly added later.

---

## 11. 共享 Specifications

The following specifications should guide implementation:

- Capsule Manifest Spec;
- Capsule Management Contract;
- Agent（代理） Registration Spec;
- Health Spec;
- Action Spec;
- Config Spec;
- Command Spec;
- Audit Event Spec;
- 状态 Model Spec.

These specifications live under:

```text
02-specs/
```

CE（社区版） v0.1 may implement only a subset, but the implementation should keep data model and API names compatible with the long-term specification direction.

---

## 12. Non-Goals

The following are not goals of `xtrape-capsule` CE（社区版） v0.1:

- replacing Kubernetes;
- replacing full observability platforms;
- replacing all configuration centers;
- forcing all services to use one language or framework;
- forcing all services to depend on Opstage（运维舞台） at runtime;
- building a complete enterprise platform in the first version;
- building a SaaS control plane in the first version.

---

## 13. 开发 Guidance

When implementing CE（社区版） v0.1, developers and AI coding agents should follow these rules:

1. Start from CE（社区版） documents, not EE（企业版） or Cloud（云版） planning documents.
2. Use shared specs for naming and compatibility.
3. Keep implementation simple and self-hosted.
4. Use SQLite by default, but avoid database design that blocks MySQL/PostgreSQL.
5. Use Agent（代理）-based registration as the only supported service onboarding path.
6. Implement Node.js embedded Agent（代理） first.
7. Do not add heavy enterprise features unless they are explicitly marked as CE（社区版） requirements.
8. Keep code modular enough for future UI/backend/agent separation.
9. Keep Capsule Service（胶囊服务） business logic outside Opstage（运维舞台）.
10. Treat documentation as part of the development contract.

---

## 14. Summary

`xtrape-capsule` 提供 a lightweight service architecture for managing AI-era small capability services.

Its key idea is:

> Many small services should remain lightweight and independent, but they should not remain invisible or unmanaged.

`xtrape-capsule-opstage` 提供 the governance platform, while Agents provide the connection between the platform and the services.

CE（社区版） v0.1 should prove this model in the simplest practical way.
