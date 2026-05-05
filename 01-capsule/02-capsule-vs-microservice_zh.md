<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 02-capsule-vs-microservice.md
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

# Capsule Service（胶囊服务） vs Microservice

- Status: Conceptual Guidance
- Edition: 共享
- Priority: 高
- Audience: architects, developers, AI coding agents

This document compares **Capsule Service（胶囊服务）** with traditional **Microservice** architecture.

The purpose is not to claim that Capsule Services replace microservices. Instead, this document clarifies when a service should be modeled as a Capsule Service（胶囊服务）, when it should remain a traditional microservice, and how both models can coexist in the Xtrape ecosystem.

---

## 1. Summary

A **Microservice** is usually a business-domain-oriented service designed for independent deployment, independent ownership, and scalable business system decomposition.

A **Capsule Service（胶囊服务）** is a lightweight, capability-oriented service unit designed for easy runtime governance through Opstage（运维舞台） and Agents.

The shortest distinction is:

> Microservice decomposes business systems. Capsule Service（胶囊服务） governs lightweight capability units.

---

## 2. Why This Distinction Matters

`xtrape-capsule` is not intended to become another heavy microservice framework.

The first CE（社区版） version should stay lightweight. If Capsule Services are treated exactly like microservices, the implementation may become unnecessarily heavy:

- too much service discovery;
- too much gateway design;
- too much distributed transaction thinking;
- too much infrastructure dependency;
- too much framework coupling;
- too much Kubernetes-first assumption;
- too much enterprise governance too early.

Capsule Services exist because many AI-era services are smaller and more operational than traditional business-domain services.

Examples:

- integration adapters;
- browser automation workers;
- account pool managers;
- OTP readers;
- session refreshers;
- proxy checkers;
- connector workers;
- task-specific AI agent runners.

These services need visibility, health, configuration, action execution, and audit. They do not always need a full microservice platform.

---

## 3. Core Difference

||Dimension|Microservice|Capsule Service（胶囊服务）||
|---|---|---|
||Primary purpose|Business-domain decomposition|Lightweight capability governance||
||Main unit|Business service|Capability / worker / connector / runtime unit||
||Typical scope|Domain capability such as order, payment, user|Specific operational capability such as integration services, account pools, browser workers||
||Typical size|Medium to large|Small to medium||
||Lifecycle|Usually long-running and stable|Long-running, short-running, worker-like, or task-oriented||
||Technology stack|Often standardized by organization|Multi-language and multi-runtime by design||
||Data ownership|Often owns domain data|May own runtime data, operational state, or adapter-specific data||
||Governance mechanism|Registry, gateway, config center, tracing, service mesh|Agent（代理） registration, heartbeat, manifest, health, actions, audit||
||Coupling to platform|Often coupled to microservice framework|Should remain runnable without Opstage（运维舞台）||
||Typical deployment|Container / Kubernetes / service cluster|Local process, container, worker, script, embedded runtime, or service||
||Typical user|Backend platform team, business service team|AI automation team, tool team, connector team, ops team||

---

## 4. Microservice Model

A traditional microservice is usually designed around a business domain boundary.

Examples:

- `payment-service`;
- `order-service`;
- `user-service`;
- `inventory-service`;
- `notification-service`.

Microservices usually emphasize:

- domain boundary;
- independent deployment;
- API contracts;
- service discovery;
- centralized configuration;
- distributed tracing;
- independent scaling;
- team ownership;
- service-to-service communication;
- data ownership.

A microservice is usually part of the main business system.

---

## 5. Capsule Service（胶囊服务） Model

A Capsule Service（胶囊服务） is usually designed around a small operational capability.

Examples:

- `integration-worker`;
- `account-pool`;
- `browser-session-worker`;
- `otp-mail-reader`;
- `proxy-health-checker`;
- `telegram-connector`;
- `agent-runtime-worker`.

Capsule Services emphasize:

- lightweight implementation;
- independent runtime;
- stable identity;
- Agent（代理）-based registration;
- status visibility;
- health reporting;
- configuration visibility;
- predefined actions;
- command execution through Agent（代理）;
- auditability;
- cross-language support.

A Capsule Service（胶囊服务） may support a business system, but it is often closer to an operational capability, adapter, connector, worker, or automation unit.

---

## 6. Governance Difference

### 6.1 Microservice Governance

Microservice governance usually 包括:

- service registry;
- API gateway;
- configuration center;
- service mesh;
- tracing;
- metrics;
- centralized logs;
- CI/CD pipelines;
- deployment orchestration.

This is powerful, but often heavy.

### 6.2 Capsule Service（胶囊服务） Governance

Capsule Service（胶囊服务） governance starts from a smaller set of needs:

- service identity;
- Agent（代理） registration;
- heartbeat;
- health report;
- manifest report;
- configuration metadata;
- predefined actions;
- command result;
- audit log.

CE（社区版） v0.1 should implement only this minimum useful governance loop.

---

## 7. Runtime Dependency Difference

A microservice is often tightly integrated with its platform runtime.

For example, it may depend on:

- a service registry;
- a configuration center;
- a gateway;
- a service mesh;
- a distributed runtime environment.

A Capsule Service（胶囊服务） must remain independently runnable.

Correct model:

```text
Capsule Service starts and performs core work
    ↓
Agent connects to Opstage if available
    ↓
Opstage provides visibility and operation
```

Incorrect model:

```text
Opstage unavailable
    ↓
Capsule Service cannot start
```

This independence is a core design rule.

---

## 8. 部署 Difference

### 8.1 Microservice 部署

Typical microservice deployment:

```text
Kubernetes / service cluster
    ├── gateway
    ├── service registry
    ├── config center
    ├── service mesh
    └── business services
```

### 8.2 Capsule Service（胶囊服务） 部署

Typical Capsule CE（社区版） deployment:

```text
Single Opstage instance
    ├── Backend
    ├── UI
    └── SQLite

Node.js Capsule Service
    └── Embedded Agent SDK
```

Future deployments may include:

```text
Capsule Service + Sidecar Agent
External Agent + managed service target
Opstage EE cluster
Opstage Cloud backend
```

CE（社区版） v0.1 should not assume Kubernetes.

---

## 9. Data Difference

### 9.1 Microservice Data

A microservice usually owns business domain data.

Examples:

- orders;
- payments;
- users;
- inventory;
- invoices.

### 9.2 Capsule Service（胶囊服务） Data

A Capsule Service（胶囊服务） usually owns or reports operational capability data.

Examples:

- account status;
- session state;
- browser context state;
- quota state;
- proxy health;
- task state;
- connector status;
- worker health;
- action result.

Some Capsule Services may own important business-adjacent data, but their governance model remains runtime-oriented.

---

## 10. API Difference

### 10.1 Microservice APIs

Microservice APIs are usually business APIs.

Examples:

```text
POST /orders
GET /orders/{id}
POST /payments/authorize
GET /users/{id}
```

### 10.2 Capsule Governance APIs

Capsule governance APIs describe runtime state and management capabilities.

Examples:

```text
GET /_capsule/manifest
GET /_capsule/health
GET /_capsule/configs
GET /_capsule/actions
POST /_capsule/actions/{actionName}
```

In CE（社区版） v0.1, an embedded Agent（代理） SDK may report this information directly to Opstage（运维舞台） Backend instead of exposing all HTTP endpoints.

The long-term specification should allow both:

- service-exposed management contract;
- agent-reported management metadata.

---

## 11. When to Use Capsule Service（胶囊服务）

Use a Capsule Service（胶囊服务） when the target is:

- small or medium in scope;
- capability-oriented;
- operationally important;
- likely to be implemented in Node.js, Python, Java, or another runtime;
- not worth a full microservice framework;
- requiring health/status/config/action/audit visibility;
- useful to manage through an Agent（代理）;
- part of an AI automation, integration adapters, connector, or worker ecosystem.

Good candidates:

```text
integration-worker
integration-gemini
account-pool
browser-session-worker
otp-mail-reader
proxy-checker
gmail-connector
agent-runner
```

---

## 12. When to Use Microservice

Use a traditional microservice when the target is:

- a core business domain;
- long-lived and stable;
- owned by a business team;
- requiring strong domain boundaries;
- requiring independent data ownership;
- part of a distributed business transaction landscape;
- already aligned with Java/Spring Cloud（云版） or other microservice infrastructure.

Good candidates:

```text
payment-service
order-service
customer-service
billing-service
inventory-service
```

A microservice may still be connected to Opstage（运维舞台） as a Capsule Service（胶囊服务） if it exposes a governance boundary. In that case, it is both a microservice and a governed Capsule target.

---

## 13. Coexistence Model

Capsule Services and microservices can coexist.

Example:

```text
Business System
├── payment-service              # Microservice
├── order-service                # Microservice
├── user-service                 # Microservice
│
├── integration-worker                 # Capsule Service
├── account-pool                 # Capsule Service
├── browser-session-worker       # Capsule Service
├── otp-mail-reader              # Capsule Service
└── proxy-health-checker         # Capsule Service
```

Opstage（运维舞台） does not replace the business service platform. It 提供 runtime governance for Capsule Services and optionally for microservices that choose to expose Capsule governance metadata.

---

## 14. Relationship with xtrape-framework

`xtrape-framework` may still be suitable for Java/Spring-based enterprise applications and traditional business services.

`xtrape-capsule` should not require every service to use `xtrape-framework`.

The recommended relationship is:

```text
xtrape-framework
    └── Java/Spring-oriented application framework

xtrape-capsule
    └── Cross-language lightweight service governance domain

xtrape-capsule-opstage
    └── Runtime governance platform for Capsule Services
```

A Java Spring service built with `xtrape-framework` may become a Capsule Service（胶囊服务） if it integrates with Agent（代理） or exposes the Capsule management contract.

---

## 15. CE（社区版） v0.1 设计 Implications

This comparison leads to the following CE（社区版） v0.1 design rules:

1. Do not implement a full microservice framework.
2. Do not require Kubernetes.
3. Do not require service mesh.
4. Do not require Nacos, Apollo, or a traditional configuration center.
5. Do not introduce distributed transaction concerns.
6. Do not force every service into Java or Spring Cloud（云版）.
7. Implement Node.js embedded Agent（代理） first.
8. Use SQLite by default.
9. Use HTTP heartbeat and command polling first.
10. Use predefined actions instead of arbitrary remote shell execution.
11. Keep Opstage（运维舞台） as a governance platform, not a business domain container.
12. Keep Capsule Services independently runnable.

---

## 16. Anti-Patterns

Avoid these anti-patterns when implementing CE（社区版）.

### 16.1 Turning Opstage（运维舞台） into a service mesh

Opstage（运维舞台） should not become a service mesh in CE（社区版） v0.1.

### 16.2 Forcing all Capsule Services into one runtime

Do not assume all future Capsule Services are Node.js, even though CE（社区版） v0.1 ships the Node.js Agent（代理） first.

### 16.3 Treating every business service as a Capsule Service（胶囊服务）

Not every microservice must be registered as a Capsule Service（胶囊服务）.

### 16.4 Treating every script as a Capsule Service（胶囊服务）

A script needs stable identity, ownership, status, and governance boundary before it should be treated as a Capsule Service（胶囊服务）.

### 16.5 Building EE（企业版） complexity into CE（社区版） v0.1

Do not add cluster deployment, full RBAC, SSO, centralized log stack, or multi-tenant billing to the first CE（社区版） prototype.

---

## 17. Summary

Microservices and Capsule Services solve different problems.

Microservices are mainly for business-domain decomposition.

Capsule Services are mainly for lightweight capability governance.

The first CE（社区版） implementation should stay focused on Capsule Service（胶囊服务） governance:

- Agent（代理） registration;
- service identity;
- health reporting;
- status visibility;
- predefined actions;
- command result reporting;
- basic audit;
- lightweight deployment.

This distinction protects `xtrape-capsule` from becoming too heavy too early.
