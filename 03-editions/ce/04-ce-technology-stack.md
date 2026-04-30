# CE Technology Stack

- Status: Implementation Target
- Edition: CE
- Priority: Current

## Position

CE 是当前实现重点，目标是提供轻量、开源、可私有化部署的 Capsule Service 运行态治理平台。

## Current Constraints

- 默认 SQLite，后续预留 MySQL/PostgreSQL。
- 单镜像/单进程优先，前后端一体发布。
- Backend 使用 Node.js + TypeScript。
- UI 使用 Vue 或 React，发布为 Web 并兼容移动端查看。
- Agent 第一版只实现 Node.js Embedded Agent SDK。
- 通信优先使用 HTTP heartbeat + command polling。
- 不在 CE v0.1 实现 EE/Cloud 的复杂能力。

## Extension Principle

CE 要轻，但不能短视；EE/Cloud 要规划，但不能污染 CE 第一版实现。

# CE Technology Stack

- Status: Implementation Target
- Edition: CE
- Priority: Current
- Audience: architects, backend developers, frontend developers, agent SDK developers, DevOps engineers, AI coding agents

This document defines the recommended technology stack for **Opstage CE v0.1**.

The stack should support a lightweight open-source implementation, simple self-hosted deployment, Node.js embedded Agent integration, and future extension toward EE and Cloud.

---

## 1. Stack Decision Summary

Recommended CE v0.1 stack:

```text
Language:        TypeScript
Backend:         Node.js + NestJS
Database ORM:    Prisma
Database:        SQLite by default
UI:              React + TypeScript + Ant Design
Agent SDK:       Node.js + TypeScript
Package Manager: pnpm
Monorepo:        pnpm workspace
Build Tooling:   Vite for UI, tsup or tsdown for packages
Container:       Docker
Deployment:      single container first, Docker Compose optional
```

This stack prioritizes:

- TypeScript sharing across UI, Backend, and Agent SDK;
- clear modular Backend structure;
- lightweight SQLite deployment;
- future MySQL/PostgreSQL compatibility;
- fast UI development;
- open-source friendliness;
- simple local development.

---

## 2. Technology Principles

CE v0.1 technology choices should follow these principles:

1. Prefer one primary language across Backend, UI, and Agent SDK.
2. Keep local development simple.
3. Keep first deployment simple.
4. Avoid infrastructure that is unnecessary for CE v0.1.
5. Preserve future migration paths to EE and Cloud.
6. Avoid framework lock-in that blocks Agent or runtime diversity.
7. Prefer mature, widely used open-source libraries.
8. Avoid custom infrastructure unless it is part of the core product value.

---

## 3. Language

### 3.1 Recommended language

Use:

```text
TypeScript
```

for:

- Backend;
- UI;
- Node.js embedded Agent SDK;
- shared types;
- demo Capsule Service.

### 3.2 Rationale

TypeScript is recommended because:

- the first Agent SDK is Node.js-based;
- UI can share types with Backend and SDK;
- API contracts can be expressed as shared types;
- development speed is high;
- many AI coding tools handle TypeScript well;
- it avoids a Java/Spring-only constraint for Capsule Services.

### 3.3 Non-goal

CE v0.1 should not require Java or Spring Cloud.

Java runtime support may be planned later, but it is not part of the first CE implementation.

---

## 4. Backend Stack

### 4.1 Recommended backend stack

Use:

```text
Node.js + TypeScript + NestJS
```

### 4.2 Rationale

NestJS is recommended because:

- it provides a clear modular structure;
- it supports controllers, services, guards, interceptors, and dependency injection;
- it helps maintain clean boundaries as the product grows;
- it is familiar to many backend developers;
- it can support both REST APIs and future WebSocket/gRPC extensions;
- it fits well with Prisma and TypeScript.

### 4.3 Backend modules

Recommended Backend modules:

```text
auth
workspaces
agents
agent-tokens
capsule-services
health
configs
actions
commands
audit
system
```

### 4.4 Alternative backend stack

A lighter alternative is:

```text
Fastify + TypeScript + Prisma
```

Fastify is lighter and faster, but NestJS provides a stronger application architecture for productization.

### 4.5 Decision

For CE v0.1, choose:

```text
NestJS + TypeScript
```

unless implementation speed or packaging simplicity becomes a major problem.

---

## 5. Database and ORM

### 5.1 Recommended database

Use:

```text
SQLite
```

as the default CE v0.1 database.

### 5.2 Rationale

SQLite is recommended because:

- it is simple to deploy;
- it requires no external database service;
- it works well for single-node CE;
- it reduces installation friction;
- it is suitable for prototype and small self-hosted deployments.

### 5.3 Future database targets

Reserve extension points for:

```text
MySQL
PostgreSQL
```

EE should likely support MySQL/PostgreSQL officially.

Cloud should likely use PostgreSQL or another managed relational database.

### 5.4 Recommended ORM

Use:

```text
Prisma
```

### 5.5 Rationale

Prisma is recommended because:

- it supports SQLite, MySQL, and PostgreSQL;
- schema is explicit and readable;
- migrations are easy for early development;
- generated TypeScript client improves developer productivity;
- it works well in monorepos.

### 5.6 Database design rules

CE v0.1 database design should:

- avoid SQLite-only assumptions where practical;
- use portable column types;
- use JSON/text fields for flexible metadata;
- store token hashes only;
- avoid storing raw secrets;
- keep schema simple;
- avoid over-normalizing future resource models too early.

---

## 6. UI Stack

### 6.1 Recommended UI stack

Use:

```text
React + TypeScript + Ant Design
```

### 6.2 Rationale

React + Ant Design is recommended because:

- it is strong for admin-console style products;
- Ant Design provides mature tables, forms, tabs, layouts, modals, tags, and status indicators;
- many developers and AI coding tools are familiar with React;
- it is suitable for fast MVP delivery;
- it can support responsive layouts for mobile viewing.

### 6.3 Alternative UI stack

Possible alternative:

```text
Vue 3 + TypeScript + Naive UI / Element Plus
```

Vue is also suitable, especially for teams that prefer Vue.

### 6.4 Decision

For CE v0.1, choose:

```text
React + TypeScript + Ant Design
```

unless the implementation team strongly prefers Vue.

### 6.5 UI build tool

Use:

```text
Vite
```

Rationale:

- fast dev server;
- simple build process;
- good TypeScript support;
- common for modern React/Vue apps.

---

## 7. Agent SDK Stack

### 7.1 Recommended SDK stack

Use:

```text
Node.js + TypeScript
```

### 7.2 SDK package output

The Node.js Agent SDK should support:

```text
ESM first
CommonJS compatibility if practical
TypeScript type declarations
```

### 7.3 SDK build tool

Recommended package build tool:

```text
tsup
```

or:

```text
tsdown
```

The final choice can be made during implementation.

### 7.4 SDK responsibilities

The SDK should provide:

- registration;
- heartbeat;
- manifest reporting;
- health provider;
- config provider;
- action registry;
- command polling;
- command result reporting;
- retry behavior;
- token persistence hook or guidance.

### 7.5 SDK non-goals

The SDK should not provide:

- browser automation logic itself;
- arbitrary shell command execution;
- secret vault implementation;
- UI components;
- sidecar mode in CE v0.1.

---

## 8. Shared Types and Contracts

### 8.1 Recommended package

Create a shared package:

```text
packages/shared-types
```

It should contain TypeScript types for:

- Capsule Manifest;
- HealthReport;
- ConfigItem;
- ActionDefinition;
- Command;
- CommandResult;
- AuditEvent;
- status values;
- Agent registration payloads.

### 8.2 Optional schema package

Optionally create:

```text
packages/capsule-spec
```

for:

- runtime validation schemas;
- constants;
- status enums;
- manifest validation helpers.

CE v0.1 may merge this into `shared-types` if separate packages are too heavy.

### 8.3 Runtime validation

For runtime validation, consider:

```text
Zod
```

Rationale:

- TypeScript-friendly;
- good for request validation;
- can derive types;
- lightweight enough for CE.

NestJS class-validator is also possible, but Zod is better aligned with shared schema packages.

---

## 9. Package Manager and Monorepo

### 9.1 Recommended package manager

Use:

```text
pnpm
```

### 9.2 Rationale

pnpm is recommended because:

- efficient disk usage;
- strong workspace support;
- widely used in TypeScript monorepos;
- good dependency isolation;
- fast install experience.

### 9.3 Recommended workspace structure

```text
xtrape-capsule-opstage/
├── apps/
│   ├── backend/
│   ├── ui/
│   └── demo-capsule-service/
├── packages/
│   ├── agent-sdk-node/
│   ├── shared-types/
│   └── capsule-spec/
├── deploy/
├── docs/
├── package.json
├── pnpm-workspace.yaml
└── README.md
```

---

## 10. API Style

### 10.1 Recommended API style

Use:

```text
REST JSON APIs
```

for CE v0.1.

### 10.2 Rationale

REST JSON is recommended because:

- simple to implement;
- easy to debug;
- works well with UI and Agent SDK;
- sufficient for heartbeat and command polling;
- avoids premature streaming complexity.

### 10.3 Future API extensions

Future EE/Cloud may add:

```text
WebSocket
gRPC streaming
message queue delivery
server-sent events
```

CE v0.1 should not implement these unless clearly required later.

---

## 11. Authentication and Security Stack

### 11.1 UI authentication

CE v0.1 should use simple local admin authentication.

Possible implementation:

```text
username + password
password hash with bcrypt or argon2
HTTP-only session cookie or JWT
```

Recommended:

```text
HTTP-only session cookie
```

for browser UI authentication, if implementation remains simple.

JWT is also acceptable for MVP speed.

### 11.2 Agent authentication

Agent APIs should use:

```text
Authorization: Bearer <agentToken>
```

Backend must store only token hashes.

### 11.3 Password hashing

Use one of:

```text
argon2
bcrypt
```

Recommended:

```text
argon2
```

if packaging is not problematic.

Use bcrypt if argon2 native dependency packaging causes friction.

### 11.4 Security non-goals

CE v0.1 should not implement:

- SSO;
- OIDC;
- LDAP;
- SAML;
- enterprise RBAC;
- mTLS;
- device attestation;
- secret vault.

---

## 12. Logging

### 12.1 CE logging

Use simple application logging.

Recommended options:

```text
pino
```

or NestJS built-in logger for the first version.

### 12.2 Logging scope

CE v0.1 logging should cover:

- backend startup;
- API errors;
- Agent registration;
- heartbeat failures;
- command processing errors;
- database migration errors.

### 12.3 Non-goal

CE v0.1 should not implement centralized log collection or log analysis.

---

## 13. Testing Stack

### 13.1 Backend tests

Recommended:

```text
Vitest or Jest
```

NestJS defaults often use Jest, but Vitest is faster and common in modern TypeScript projects.

Decision can follow NestJS project defaults unless there is a strong reason to switch.

### 13.2 UI tests

Recommended:

```text
Vitest + Testing Library
```

for component/unit tests.

### 13.3 End-to-end smoke tests

Recommended future direction:

```text
Playwright
```

CE v0.1 should at least support manual MVP acceptance testing.

Automated Playwright smoke tests are useful but optional for v0.1.

---

## 14. Build and Packaging

### 14.1 Backend build

NestJS build output should be packaged into a runtime container.

### 14.2 UI build

UI should build static assets with Vite.

Production-like CE packaging can serve UI static assets from Backend.

### 14.3 Package builds

Agent SDK and shared packages can use:

```text
tsup
```

or:

```text
tsdown
```

### 14.4 Docker packaging

CE v0.1 should provide:

- Dockerfile;
- Docker Compose example if useful;
- SQLite data volume;
- environment variable documentation.

Preferred first public deployment shape:

```text
single container
single exposed port
SQLite data volume
```

---

## 15. Environment Configuration

Recommended environment variables:

```text
OPSTAGE_PORT=8080
OPSTAGE_DATABASE_URL=file:./data/opstage.db
OPSTAGE_ADMIN_USERNAME=admin
OPSTAGE_ADMIN_PASSWORD=change-me
OPSTAGE_SESSION_SECRET=change-me
OPSTAGE_AGENT_HEARTBEAT_INTERVAL_SECONDS=30
OPSTAGE_AGENT_OFFLINE_THRESHOLD_SECONDS=90
OPSTAGE_COMMAND_POLL_INTERVAL_SECONDS=5
OPSTAGE_COMMAND_TTL_SECONDS=300
```

Agent SDK / demo service variables:

```text
OPSTAGE_BACKEND_URL=http://localhost:8080
OPSTAGE_REGISTRATION_TOKEN=opstage_reg_xxx
OPSTAGE_AGENT_TOKEN_FILE=./data/agent-token.json
```

---

## 16. Technologies Not Selected for CE v0.1

### 16.1 Java Spring Cloud

Not selected because CE must be lightweight and cross-runtime, and many target Capsule Services are Node.js-based.

### 16.2 Kubernetes

Not selected because CE v0.1 should run without cluster infrastructure.

### 16.3 Nacos / Apollo

Not selected because CE v0.1 is not a full configuration center.

### 16.4 Prometheus / Grafana / Loki / ELK

Not selected because CE v0.1 is not a full observability platform.

### 16.5 Redis / RabbitMQ / Kafka

Not selected because CE v0.1 command polling can work with the database only.

Queues may be introduced in EE/Cloud later.

### 16.6 WebSocket / gRPC

Not selected for v0.1 because HTTP polling is simpler and sufficient.

---

## 17. Future Upgrade Paths

CE v0.1 stack should keep the following upgrade paths open.

| Area | CE v0.1 | Future EE / Cloud |
|---|---|---|
| Database | SQLite | MySQL, PostgreSQL |
| Command channel | HTTP polling | WebSocket, gRPC, message queue |
| Auth | local admin | RBAC, SSO, OIDC, LDAP |
| Agent SDK | Node.js | Java, Python, Go |
| Agent mode | embedded | sidecar, external |
| Deployment | single container | cluster, HA, Helm |
| Observability | basic logs + health | metrics, logs, traces, alerts |
| Secrets | secretRef-ready | Vault, managed secret store |
| Config | visibility | publishing, versioning, rollback |

---

## 18. Technology Acceptance Criteria

The selected stack is acceptable when:

- a new developer can install dependencies with one command;
- Backend starts locally with SQLite;
- UI starts locally with Vite;
- Agent SDK can be developed and linked locally;
- demo Capsule Service can use the SDK;
- Docker packaging works;
- no external database is required for CE v0.1;
- no external SaaS is required;
- future MySQL/PostgreSQL support is not blocked;
- future sidecar/external Agent support is not blocked.

---

## 19. Summary

The CE technology stack should optimize for:

```text
simple development
simple deployment
shared TypeScript contracts
Node.js embedded Agent SDK
SQLite-first persistence
future extensibility
```

Recommended stack:

```text
TypeScript + NestJS + Prisma + SQLite + React + Ant Design + pnpm + Docker
```

The most important technology rule is:

> Use a stack that makes CE easy to build and run now, without closing the path to EE and Cloud later.