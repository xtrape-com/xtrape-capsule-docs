---
status: proposed
audience: architects
stability: evolving
last_reviewed: 2026-05-05
---

# xtrape-capsule Overview

- Status: Conceptual Guidance
- Edition: Shared
- Priority: High
- Audience: architects, developers, AI coding agents

`xtrape-capsule` is the lightweight service architecture domain of Xtrape. It defines the concept, specifications,
runtime governance model, agent integration model, and edition strategy for Capsule Services.

`xtrape-capsule-opstage` is one core subsystem under this domain. It provides the runtime governance platform for Capsule Services, but it is not the whole `xtrape-capsule` domain.

The current implementation focus is **CE / Community Edition**. EE / Enterprise Edition and Cloud / SaaS Edition are
future planning targets. CE should reserve extension points for them, but it should not implement their full
capabilities in early versions.

---

## 1. Background

AI-era applications are producing more and more small service units:

- integration services for wrapping web or platform capabilities;
- account pool services for managing registered accounts;
- browser automation workers;
- OTP readers;
- proxy checkers;
- connector services;
- task workers;
- AI agent runtimes;
- session managers;
- lightweight internal tools.

These services are usually not complex by themselves. They may be a Node.js service, a Playwright worker, a Python
script, a small Java service, or an adapter that wraps a third-party platform capability.

The real problem is not how to implement these services. The real problem is:

> When the number of small services keeps growing, how can the team remember, observe, configure, audit, operate, and govern them over the long term without turning them into unmanaged islands?

Traditional microservice platforms, configuration centers, and monitoring systems do not fully match this problem:

- Microservice frameworks are often too heavy for these small capability units.
- Configuration centers usually focus on key-value configuration, not runtime governance.
- Monitoring systems can observe status, but they usually do not provide business-level control.
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

For AI automation and integration services, runtime state is often more important than static configuration:

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

A Java-only or Spring-Cloud-only framework is not flexible enough for this target.

### 2.5 Private Deployment and Cloud Evolution

The system should support lightweight self-hosted deployment first, but it should not block future enterprise and SaaS editions.

Therefore, CE must stay simple, while the architecture must preserve extension points for:

- stronger databases;
- cluster deployment;
- multi-workspace and multi-tenant models;
- RBAC and SSO;
- centralized logs and metrics;
- richer agent modes;
- hosted cloud control plane.

---

## 3. Vision

`xtrape-capsule` defines a lightweight service architecture for AI-era service ecosystems.

Its vision is:

> Make small capability services easy to register, observe, configure, audit, and operate without forcing them into a heavy microservice framework.

---

## 4. Core Concept

The core managed unit is the **Capsule Service**.

A Capsule Service is:

> A lightweight, self-contained, independently runnable, agent-governed service unit that exposes a clear capability, connector, worker, automation process, account resource, session resource, or runtime adapter.

A Capsule Service should be:

- independently runnable;
- language-neutral;
- observable;
- configurable;
- auditable;
- operable through a registered Agent;
- free from hard dependency on Opstage for startup.

---

## 5. Relationship with Opstage

`xtrape-capsule-opstage` is the runtime governance platform for Capsule Services.

It provides:

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

> `xtrape-capsule` defines Capsule Services. `xtrape-capsule-opstage` manages Capsule Services.

---

## 6. Relationship with Microservices

Capsule Services are not a replacement for all microservices.

They are intended for smaller, lighter, capability-oriented service units.

| Dimension | Microservice | Capsule Service |
|---|---|---|
| Primary split | Business domain | Capability / worker / connector / runtime unit |
| Typical size | Medium to large | Small to medium |
| Lifecycle | Long-running business service | Long-running, short-running, task-like, or worker-like |
| Technology stack | Often standardized | Multi-language and multi-runtime |
| Governance | Service registry, gateway, config, tracing | Agent registration, runtime status, actions, audit, config visibility |
| Typical examples | payment service, order service, user service | integration adapter, account pool, browser worker, OTP reader, proxy checker |

A traditional microservice may also be registered as a Capsule Service if it exposes or integrates with the Capsule governance contract.

---

## 7. High-Level Architecture

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

### 7.1 Capsule Service

The managed lightweight service. It may be implemented in Node.js, Java, Python, or another runtime.

### 7.2 Opstage Agent

The governance bridge between Capsule Service and Opstage Backend.

Agent modes:

- embedded agent;
- sidecar agent;
- external agent.

CE v0.1 focuses on Node.js embedded agent.

### 7.3 Opstage Backend

The control plane backend. It stores agent state, service state, commands, audit logs, and configuration metadata.

### 7.4 Opstage UI

The human-facing web console for viewing and operating Capsule Services.

---

## 8. Core Design Principles

### 8.1 Capsule Services must run independently

A Capsule Service should not require Opstage to be online in order to start or perform its core business work.

Opstage provides governance, not mandatory runtime existence.

### 8.2 Opstage manages through Agents

Opstage should not directly scan or take over arbitrary services.

A service enters governance through a registered and authorized Agent.

### 8.3 Agent connection should be outbound-first

Agents should actively connect to Opstage Backend.

This supports:

- private deployment;
- NAT environments;
- customer-side networks;
- Cloud SaaS future model;
- fewer exposed inbound ports.

### 8.4 CE should remain lightweight

CE v0.1 should avoid heavy dependencies and focus on the smallest useful governance loop.

### 8.5 Specifications should be stable

Cross-edition specifications should be designed carefully. Implementations may be partial, but they should not contradict the long-term model.

### 8.6 Business logic stays in Capsule Services

Opstage should not become the place where every service's business logic is implemented.

Opstage coordinates, observes, configures, audits, and commands. Capsule Services perform their own business functions.

---

## 9. Edition Strategy

`xtrape-capsule` is planned in three editions:

| Edition | Name | Status | Purpose |
|---|---|---|---|
| CE | Community Edition | Current implementation target | Lightweight, open-source, self-hosted edition |
| EE | Enterprise Edition | Future planning | Private-deployment commercial edition |
| Cloud | SaaS Cloud Edition | Future planning | Hosted SaaS edition |

### 9.1 CE

CE should prove the core model with minimal operational cost.

CE focuses on:

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

### 9.2 EE

EE will target enterprise private deployment.

Future EE capabilities may include:

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

### 9.3 Cloud

Cloud will target hosted SaaS usage.

Future Cloud capabilities may include:

- multi-tenant workspace model;
- subscription billing;
- hosted backend;
- agent outbound connectivity;
- cloud-side metadata and status;
- customer-side secret boundary;
- cloud alerting and reporting.

---

## 10. CE v0.1 Implementation Boundary

CE v0.1 is the current implementation target.

It should implement:

- Opstage Backend;
- Opstage UI;
- SQLite persistence;
- Node.js embedded Agent SDK;
- demo Capsule Service;
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

- multi-tenant Cloud model;
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

## 11. Shared Specifications

The following specifications should guide implementation:

- Capsule Manifest Spec;
- Capsule Management Contract;
- Agent Registration Spec;
- Health Spec;
- Action Spec;
- Config Spec;
- Command Spec;
- Audit Event Spec;
- Status Model Spec.

These specifications live under:

```text
02-specs/
```

CE v0.1 may implement only a subset, but the implementation should keep data model and API names compatible with the long-term specification direction.

---

## 12. Non-Goals

The following are not goals of `xtrape-capsule` CE v0.1:

- replacing Kubernetes;
- replacing full observability platforms;
- replacing all configuration centers;
- forcing all services to use one language or framework;
- forcing all services to depend on Opstage at runtime;
- building a complete enterprise platform in the first version;
- building a SaaS control plane in the first version.

---

## 13. Development Guidance

When implementing CE v0.1, developers and AI coding agents should follow these rules:

1. Start from CE documents, not EE or Cloud planning documents.
2. Use shared specs for naming and compatibility.
3. Keep implementation simple and self-hosted.
4. Use SQLite by default, but avoid database design that blocks MySQL/PostgreSQL.
5. Use Agent-based registration as the only supported service onboarding path.
6. Implement Node.js embedded Agent first.
7. Do not add heavy enterprise features unless they are explicitly marked as CE requirements.
8. Keep code modular enough for future UI/backend/agent separation.
9. Keep Capsule Service business logic outside Opstage.
10. Treat documentation as part of the development contract.

---

## 14. Summary

`xtrape-capsule` provides a lightweight service architecture for managing AI-era small capability services.

Its key idea is:

> Many small services should remain lightweight and independent, but they should not remain invisible or unmanaged.

`xtrape-capsule-opstage` provides the governance platform, while Agents provide the connection between the platform and the services.

CE v0.1 should prove this model in the simplest practical way.
