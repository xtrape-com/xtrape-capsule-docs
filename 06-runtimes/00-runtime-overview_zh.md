<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 00-runtime-overview.md
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

# Runtime 概述

- Status: 实施指南
- Edition: 共享
- Priority: Medium
- Audience: architects, runtime SDK developers, Capsule Service（胶囊服务） developers, backend developers, agent SDK developers, AI coding agents

This document 定义 the runtime integration overview for the `xtrape-capsule` product family.

A runtime is a language or execution environment in which Capsule Services and Agents are implemented. Runtime documents explain how different ecosystems should connect to the Capsule governance model and Opstage（运维舞台） Agent（代理） capabilities.

The current implementation focus is **CE（社区版）**. CE（社区版） v0.1 prioritizes **Node.js**. Java, Python, Go, Sidecar runtime integration, External Agent（代理） runtime integration, and Kubernetes runtime integration are future EE（企业版）/Cloud（云版） extension tracks and must not expand the CE（社区版） v0.1 implementation scope.

---

## 1. Purpose

The purpose of runtime integration is to make the Capsule governance model practical across different implementation ecosystems.

Runtime documents should answer:

- how a service in this runtime becomes a Capsule Service（胶囊服务）;
- how the runtime integrates with an Agent（代理）;
- what SDK or helper package is needed;
- how service identity is declared;
- how health is reported;
- how config metadata is exposed;
- how predefined actions are registered;
- how Commands are executed;
- how CommandResults are reported;
- how secrets and sensitive values are handled;
- what belongs to CE（社区版） and what belongs to future EE（企业版）/Cloud（云版）.

---

## 2. Runtime Positioning

A runtime is:

> A concrete language or execution environment that can host Capsule Services and Agent（代理） integrations.

Examples:

```text
Node.js
Java
Python
Go
container sidecar runtime
external process runtime
Kubernetes runtime
```

The runtime layer should not redefine the Capsule model.

It should adapt the same core governance contract to each ecosystem.

---

## 3. 共享 Runtime Contract

All runtime integrations should preserve the same logical contract:

```text
Capsule Service identity
Agent integration
registration
heartbeat
manifest report
health report
config metadata report
action definition report
Command execution
CommandResult reporting
AuditEvent creation by Backend
secretRef boundary
```

Runtime-specific SDKs may differ in API style, but the governance semantics should remain consistent.

---

## 4. CE（社区版） Runtime Scope

CE（社区版） v0.1 should focus on one runtime:

```text
Node.js
```

Required CE（社区版） runtime work:

- Node.js Capsule Service（胶囊服务） conventions;
- Node.js Embedded Agent（代理） SDK;
- Node.js demo Capsule Service（胶囊服务）;
- TypeScript-first SDK API;
- health/config/action provider API;
- command polling and result reporting;
- Docker-friendly demo deployment.

CE（社区版） should prove the governance loop before adding more runtimes.

---

## 5. CE（社区版） Runtime Non-Goals

CE（社区版） v0.1 should not implement:

- Java runtime SDK;
- Python runtime SDK;
- Go runtime SDK;
- Sidecar runtime adapter;
- External Agent（代理） adapter framework;
- Kubernetes runtime integration;
- browser runtime adapter;
- account/session runtime adapter;
- runtime marketplace;
- runtime plugin system;
- multi-language compatibility matrix beyond planning.

These are future EE（企业版）/Cloud（云版） planning items.

---

## 6. Node.js Runtime

Node.js is the CE（社区版） reference runtime.

Node.js should provide:

```text
@xtrape/capsule-agent-node
```

as the first Agent（代理） SDK package.

Node.js runtime should support:

- embedded Agent（代理） mode;
- TypeScript-first usage;
- service identity declaration;
- health provider;
- config provider;
- action registry;
- command polling;
- CommandResult reporting;
- token store;
- safe logging;
- Docker deployment.

Node.js is the implementation target for CE（社区版） v0.1.

---

## 7. Java Runtime Direction

Java runtime is a future extension.

Potential use cases:

- Spring Boot services;
- Spring Cloud（云版） services;
- enterprise Java systems;
- future alignment with the broader xtrape Java ecosystem.

Possible package form:

```text
xtrape-capsule-agent-java
xtrape-capsule-agent-spring-boot-starter
```

Potential capabilities:

- Spring Boot starter;
- health indicator adapter;
- action annotation or registry;
- config metadata provider;
- Agent（代理） token store;
- HTTP polling client.

Java runtime is not a CE（社区版） v0.1 requirement.

---

## 8. Python Runtime Direction

Python runtime is a future extension.

Potential use cases:

- AI automation workers;
- data processing workers;
- FastAPI services;
- LangChain/LangGraph services;
- browser automation scripts;
- scraping and workflow workers.

Possible package form:

```text
xtrape-capsule-agent-python
```

Potential capabilities:

- async Agent（代理） client;
- FastAPI helper;
- health provider;
- config provider;
- action registry;
- file token store;
- command polling;
- CommandResult reporting.

Python runtime is not a CE（社区版） v0.1 requirement.

---

## 9. Go Runtime Direction

Go runtime is a future extension.

Potential use cases:

- lightweight infrastructure tools;
- single-binary Agents;
- Sidecar Agent（代理） implementation;
- External Agent（代理） implementation;
- host-level utilities.

Possible package form:

```text
xtrape-capsule-agent-go
```

Potential capabilities:

- low-resource Agent（代理） client;
- single-binary deployment;
- HTTP polling client;
- file token store;
- action registry;
- Sidecar/External Agent（代理） foundation.

Go runtime is not a CE（社区版） v0.1 requirement.

---

## 10. Sidecar Runtime Direction

Sidecar runtime integration is future EE（企业版） work.

It may define how non-embedded services expose local management interfaces to a Sidecar Agent（代理）.

Potential local contract:

```http
GET  /_capsule/manifest
GET  /_capsule/health
GET  /_capsule/configs
GET  /_capsule/actions
POST /_capsule/actions/{actionName}
```

Sidecar runtime integration is not a CE（社区版） v0.1 requirement.

---

## 11. External Runtime Direction

External runtime integration is future EE（企业版） work.

It may define how External Agents manage explicitly configured targets through adapters.

Potential target types:

```text
local-http
filesystem
process-supervisor
container-runtime
browser-runtime
account-pool
custom-adapter
```

External runtime integration is not a CE（社区版） v0.1 requirement.

---

## 12. Kubernetes Runtime Direction

Kubernetes runtime integration is long-term EE（企业版）/Cloud（云版） work.

Potential capabilities:

- workload discovery through annotations;
- Kubernetes Agent（代理）;
- namespace-scoped governance;
- Kubernetes RBAC integration;
- ConfigMap/Secret references;
- Pod health mapping;
- Helm-based deployment.

Kubernetes runtime integration is not a CE（社区版） v0.1 requirement.

---

## 13. Runtime SDK 设计 Principles

Runtime SDKs should follow these principles:

1. Preserve the shared Capsule governance contract.
2. Use idiomatic APIs for each language.
3. Keep service integration small.
4. Keep Agent（代理） communication outbound-first.
5. Execute only predefined actions.
6. Avoid arbitrary shell execution.
7. Use `secretRef` for sensitive references.
8. Avoid raw secret reporting.
9. Keep token storage safe.
10. Handle Backend downtime without crashing business runtime by default.
11. Keep CE（社区版） runtime work focused on Node.js first.

---

## 14. Runtime Data Boundary

Runtime integrations may report governance metadata:

- service identity;
- runtime metadata;
- health status;
- config metadata;
- action metadata;
- CommandResult;
- sanitized errors.

Runtime integrations should not report raw sensitive data by default:

- passwords;
- cookies;
- OAuth tokens;
- API keys;
- private keys;
- account credentials;
- raw browser sessions;
- large application logs;
- private business records.

Use `secretRef`, masked values, or summaries.

---

## 15. Runtime Compatibility Fields

共享 runtime-related fields may include:

```text
runtime
runtimeVersion
agentMode
agentVersion
sdkVersion
protocolVersion
capabilities
metadataJson
```

CE（社区版） may reserve these fields but should not implement a full compatibility matrix in v0.1.

Future EE（企业版） may use these fields for Agent（代理） diagnostics and compatibility warnings.

---

## 16. Runtime 文档 Requirements

Each runtime document should define:

- runtime scope;
- package name;
- installation method;
- minimal usage example;
- configuration model;
- service identity model;
- health provider model;
- config provider model;
- action registration model;
- command execution model;
- token storage model;
- sensitive data rules;
- testing requirements;
- CE（社区版）/EE（企业版）/Cloud（云版） boundary.

Node.js should be documented first because it is the CE（社区版） implementation target.

---

## 17. 实现 优先级

Recommended runtime implementation priority:

```text
1. Node.js runtime conventions
2. Node.js Agent SDK
3. Node.js demo Capsule Service
4. Node.js SDK tests
5. Java runtime planning
6. Python runtime planning
7. Go runtime planning
8. Sidecar/External runtime planning
```

Only items 1-4 are CE（社区版） v0.1 implementation targets.

---

## 18. Future EE（企业版） Direction

Future EE（企业版） may add:

- Java Agent（代理） SDK;
- Spring Boot starter;
- Python Agent（代理） SDK;
- FastAPI helper;
- Go Agent（代理） SDK;
- Sidecar Agent（代理） runtime;
- External Agent（代理） adapter framework;
- runtime compatibility matrix;
- Agent（代理） diagnostics by runtime;
- runtime-specific deployment templates;
- enterprise support for selected runtimes.

These are not CE（社区版） v0.1 requirements.

---

## 19. Future Cloud（云版） Direction

Future Cloud（云版） may add:

- Cloud（云版） enrollment snippets per runtime;
- workspace-scoped registration token examples;
- Agent（代理） Gateway configuration per runtime;
- runtime connection diagnostics;
- runtime-specific usage metering;
- managed alerts by runtime;
- hosted documentation and quick-start generator.

These are not CE（社区版） v0.1 requirements.

---

## 20. Anti-Patterns

Avoid these patterns.

### 20.1 Adding too many runtimes before Node.js is stable

The first goal is to prove the governance loop, not maximize language coverage.

### 20.2 Runtime SDKs with incompatible semantics

Different runtimes may use different APIs, but they must preserve the same governance model.

### 20.3 Runtime SDK 包括 shell execution

Remote shell is not the Capsule operation model.

### 20.4 Runtime reports raw secrets

Use `secretRef` or masking.

### 20.5 Runtime integration crashes business service on Opstage（运维舞台） outage by default

Governance outage should not automatically become business outage.

---

## 21. Acceptance Criteria

Runtime overview is acceptable when:

- runtime concept is clearly defined;
- Node.js is clearly the CE（社区版） v0.1 runtime target;
- Java/Python/Go are clearly future planning items;
- Sidecar/External/Kubernetes runtime directions are future-only;
- shared runtime contract is explicit;
- runtime SDK principles are clear;
- data boundary and secretRef rules are explicit;
- runtime documentation requirements are clear;
- CE（社区版） implementation scope is protected from future runtime expansion.

---

## 22. Summary

Runtime integration adapts the Capsule governance model to concrete language and execution environments.

The most important runtime rule is:

> Prove the Capsule governance contract with Node.js first, then add more runtimes only as compatible extensions of the same model.
