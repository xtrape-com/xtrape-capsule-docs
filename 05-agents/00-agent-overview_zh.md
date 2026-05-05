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
原始文件 / Original File: 00-agent-overview.md
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

# Agent（代理） 概述

- Status: 实施指南
- Edition: 共享
- Priority: 高
- Audience: agent SDK developers, Capsule Service（胶囊服务） developers, backend developers, architects, security reviewers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/openapi/opstage-ce-v0.1.yaml` disagree, the ADRs and OpenAPI contract win for CE（社区版） v0.1.

This document 定义 the overall Agent（代理） concept for the `xtrape-capsule` product family.

An Agent（代理） is the authorized governance bridge that allows a Capsule Service（胶囊服务） to join the Opstage（运维舞台） runtime governance system.

The current implementation focus is **CE（社区版）**. CE（社区版） v0.1 implements only the **Node.js Embedded Agent（代理）**.
Sidecar Agent（代理）, External Agent（代理）, Host Agent（代理）, Kubernetes Agent（代理）, and multi-language Agent（代理） SDKs are
future EE（企业版）/Cloud（云版） extension tracks and must not expand the CE（社区版） v0.1 implementation scope.

---

## 1. Purpose

The purpose of an Agent（代理） is to make Capsule Services governable by Opstage（运维舞台）.

An Agent（代理） allows Opstage（运维舞台） to:

- register a runtime participant;
- authenticate runtime communication;
- receive heartbeat signals;
- receive Capsule Service（胶囊服务） manifests;
- receive health reports;
- receive config metadata;
- receive predefined action metadata;
- deliver Commands;
- receive CommandResults;
- support auditability;
- calculate freshness and effective status.

The Agent（代理） is the runtime-side entry point into Opstage（运维舞台） governance.

---

## 2. Positioning

An Agent（代理） is:

> The authorized bridge between Opstage（运维舞台） Backend and one or more Capsule Services.

It is responsible for governance communication, not business ownership.

The Agent（代理） makes a Capsule Service（胶囊服务） visible and operable through Opstage（运维舞台）, but it should not take over the service's core business behavior.

---

## 3. What an Agent（代理） Is Not

An Agent（代理） is not:

- the Capsule Service（胶囊服务） itself;
- the business logic owner;
- a generic process supervisor in CE（社区版）;
- a remote shell;
- a secret vault;
- a full observability collector in CE（社区版）;
- a deployment orchestrator in CE（社区版）;
- a browser automation framework by itself;
- a Kubernetes operator in CE（社区版）;
- a workflow engine.

Future editions may introduce stronger Agent（代理） modes, but the Agent（代理） identity should remain governance bridge, not unrestricted runtime controller.

---

## 4. Relationship with Capsule Service（胶囊服务）

A Capsule Service（胶囊服务） is the lightweight service being governed.

An Agent（代理） is the bridge that reports the service and executes predefined governance operations.

Recommended relationship in CE（社区版）:

```text
Capsule Service process
├── business logic
└── Node.js Embedded Agent SDK
    ↓ outbound HTTP
Opstage Backend
```

The Capsule Service（胶囊服务） continues to own:

- business APIs;
- business data;
- internal workflows;
- local configuration;
- local secrets;
- domain behavior.

The Agent（代理） owns:

- governance registration;
- heartbeat;
- manifest reporting;
- health reporting;
- config metadata reporting;
- action metadata reporting;
- Command polling;
- predefined action handler dispatch;
- CommandResult reporting.

---

## 5. Relationship with Opstage（运维舞台）

Opstage（运维舞台） consists of:

```text
Opstage UI
Opstage Backend
Agent integration
```

Agent（代理） communicates only with Opstage（运维舞台） Backend through Agent（代理） APIs.

Recommended flow:

```text
Opstage UI
    ↓ Admin API
Opstage Backend
    ↑ Agent API
Agent
    ↔ Capsule Service providers and handlers
Capsule Service
```

The UI must not call Agent（代理） directly.

The Backend should not require inbound network access to Agent（代理） in CE（社区版）.

---

## 6. Core Agent（代理） Responsibilities

An Agent（代理） is responsible for:

- loading Agent（代理） configuration;
- registering with Opstage（运维舞台） using a registration token;
- storing the issued Agent（代理） token locally;
- authenticating Agent（代理） API calls;
- sending heartbeat;
- reporting one or more Capsule Services where supported;
- reporting service manifest;
- reporting health;
- reporting config metadata;
- reporting predefined actions;
- polling Commands;
- executing predefined action handlers;
- reporting CommandResults;
- retrying communication failures safely;
- avoiding raw secret leakage;
- keeping governance failure isolated from business runtime where practical.

---

## 7. Core Agent（代理） Non-Responsibilities

CE（社区版） Agent（代理） should not be responsible for:

- executing arbitrary shell commands;
- running arbitrary scripts;
- replacing the service's business logic;
- storing raw secrets in Opstage（运维舞台）;
- collecting all application logs;
- collecting all metrics and traces;
- supervising service processes;
- automatically discovering all services on a host;
- managing Kubernetes resources;
- implementing SaaS billing or tenant behavior;
- implementing enterprise SSO or RBAC.

These are either out of scope or future extension topics.

---

## 8. Agent（代理） Modes

Long-term Agent（代理） modes may include:

```text
embedded
sidecar
external
host
kubernetes
```

### 8.1 Embedded Agent（代理）

Agent（代理） runs inside the Capsule Service（胶囊服务） process.

CE（社区版） implements:

```text
Node.js Embedded Agent
```

### 8.2 Sidecar Agent（代理）

Agent（代理） runs beside one Capsule Service（胶囊服务） and communicates through local management endpoints, local IPC, or mounted files.

This is future EE（企业版） work.

### 8.3 External Agent（代理）

Agent（代理） runs outside one or more services and manages them through configured targets.

This is future EE（企业版） work.

### 8.4 Host Agent（代理）

Agent（代理） runs on a host and manages multiple configured local services.

This is long-term EE（企业版） work.

### 8.5 Kubernetes Agent（代理）

Agent（代理） runs inside Kubernetes and manages annotated or configured workloads.

This is long-term EE（企业版） work.

---

## 9. CE（社区版） Agent（代理） Scope

CE（社区版） v0.1 implements only:

```text
Node.js Embedded Agent SDK
```

Required CE（社区版） Agent（代理） capabilities:

- initialize from configuration;
- register with registration token;
- persist Agent（代理） token locally;
- send authenticated heartbeat;
- report service manifest;
- report health;
- report config metadata;
- report action definitions;
- poll Commands;
- execute predefined action handlers;
- report CommandResults;
- handle Backend downtime without crashing business service;
- avoid logging raw tokens;
- avoid reporting raw secrets.

---

## 10. CE（社区版） Agent（代理） Non-Goals

CE（社区版） v0.1 must not implement:

- sidecar Agent（代理）;
- external Agent（代理）;
- host Agent（代理）;
- Kubernetes Agent（代理）;
- Java Agent（代理） SDK;
- Python Agent（代理） SDK;
- Go Agent（代理） SDK;
- WebSocket command channel;
- gRPC streaming;
- Agent（代理） Gateway;
- automatic service discovery;
- Agent（代理） fleet upgrade manager;
- enterprise secret provider resolver;
- arbitrary shell execution;
- remote terminal.

These capabilities may be considered after the CE（社区版） governance loop is proven.

---

## 11. Node.js Embedded Agent（代理）

The Node.js Embedded Agent（代理） is the CE（社区版） reference Agent（代理） implementation.

It runs inside a Node.js Capsule Service（胶囊服务） process.

Example structure:

```text
Node.js Capsule Service
├── HTTP/API/business logic
├── local config and runtime state
└── Opstage Agent SDK
    ├── heartbeat loop
    ├── manifest reporter
    ├── health provider
    ├── config provider
    ├── action registry
    ├── command polling loop
    └── result reporter
```

The embedded Agent（代理） should be lightweight and should not require a separate process.

---

## 12. Developer Experience Target

A Capsule Service（胶囊服务） developer should be able to integrate the Agent（代理） with a small amount of code.

Example target API:

```ts
import { CapsuleAgent } from '@xtrape/capsule-agent-node';

const agent = new CapsuleAgent({
  backendUrl: process.env.OPSTAGE_BACKEND_URL ?? 'http://localhost:8080',
  registrationToken: process.env.OPSTAGE_REGISTRATION_TOKEN,
  tokenStore: {
    file: './data/agent-token.json',
  },
  service: {
    code: 'demo-capsule-service',
    name: 'Demo Capsule Service',
    version: '0.1.0',
    runtime: 'nodejs',
  },
});

agent.health(async () => ({
  status: 'UP',
  message: 'Demo service is healthy.',
}));

agent.configs(() => [
  {
    key: 'demo.message',
    label: 'Demo Message',
    type: 'string',
    defaultValue: 'hello capsule',
    editable: true,
    sensitive: false,
  },
]);

agent.action({
  name: 'echo',
  label: 'Echo',
  dangerLevel: 'LOW',
  handler: async (payload) => ({
    success: true,
    message: 'Echo completed.',
    data: payload,
  }),
});

await agent.start();
```

The final SDK API may evolve, but this represents the intended simplicity.

---

## 13. Agent（代理） Lifecycle

Recommended CE（社区版） Agent（代理） lifecycle:

```text
Capsule Service starts
    ↓
Agent SDK is initialized
    ↓
Health/config/action providers are registered
    ↓
Agent loads stored Agent token
    ↓
If no valid Agent token exists, Agent registers with registration token
    ↓
Agent reports service manifest
    ↓
Agent starts heartbeat loop
    ↓
Agent starts command polling loop
    ↓
Agent executes predefined actions when Commands arrive
    ↓
Agent reports CommandResults
```

If Opstage（运维舞台） Backend is unavailable, the Agent（代理） should retry in the background and keep the Capsule Service（胶囊服务） running where practical.

---

## 14. Registration Model

Agent（代理） registration is the first trusted enrollment step.

Flow:

```text
Admin creates registration token in Opstage UI
    ↓
Capsule Service starts with Agent SDK and registration token
    ↓
Agent calls registration endpoint
    ↓
Backend validates registration token
    ↓
Backend creates Agent record
    ↓
Backend issues Agent token
    ↓
Agent stores Agent token locally
```

Registration token rules:

- shown only once;
- stored as hash in Backend;
- scoped to default Workspace in CE（社区版）;
- optionally expiring;
- optionally one-time use;
- revocable if Backend 支持 it.

---

## 15. Agent（代理） Token Model

After registration, the Agent（代理） authenticates with an Agent（代理） token.

Rules:

- Backend stores only token hash;
- Agent（代理） stores raw token locally;
- Agent（代理） sends token through `Authorization: Bearer` header;
- token must not be logged;
- token should be cleared or marked invalid if Backend rejects it as revoked;
- token rotation is future EE（企业版） work.

Example header:

```http
Authorization: Bearer <agentToken>
```

---

## 16. Heartbeat Model

Heartbeat tells Opstage（运维舞台） that the Agent（代理） is still alive.

Heartbeat should include:

- Agent（代理） identity derived from token;
- timestamp;
- Agent（代理） version;
- runtime metadata;
- optional lightweight status summary.

Heartbeat must not include raw secrets.

Backend uses heartbeat to calculate:

```text
AgentStatus
CapsuleService freshness
Effective service status
```

---

## 17. Manifest Model

Agent（代理） reports a service manifest to describe the Capsule Service（胶囊服务）.

Manifest may include:

```text
service code
service name
version
runtime
agentMode
capabilities
resources
health support
config metadata
action definitions
metadata
```

Manifest must not include raw secrets.

Sensitive config values should use:

```text
secretRef
```

or be masked.

---

## 18. Health Model

Agent（代理） exposes service health through a health provider.

Recommended health statuses:

```text
UP
DOWN
DEGRADED
UNKNOWN
```

Health result may include:

```text
status
message
dependencies
details
checkedAt
```

Health must not include raw tokens, cookies, passwords, API keys, or private business data.

---

## 19. Config Metadata Model

Agent（代理） exposes configuration metadata, not full configuration-center behavior.

CE（社区版） 支持 config visibility only.

Config metadata may include:

```text
key
label
type
defaultValue
currentValue if safe
editable
sensitive
source
description
validation
metadata
```

If a value is sensitive, report:

```text
masked value
null
secretRef
```

not raw secret.

Config editing and publishing are future EE（企业版） capabilities.

---

## 20. Action Model

Agent（代理） exposes predefined actions.

An action is a safe, named operation implemented by the Capsule Service（胶囊服务）.

Examples:

```text
echo
runHealthCheck
reloadConfig
clearCache
refreshSession
```

CE（社区版） action rules:

- actions must be predefined;
- unknown actions fail safely;
- action names must be stable;
- action handlers must return serializable results;
- no arbitrary shell action;
- high-risk actions should declare danger level.

---

## 21. Command Model

Commands are created by Backend and polled by Agent（代理）.

CE（社区版） 支持:

```text
CommandType = ACTION
```

Command flow:

```text
UI requests action
    ↓
Backend creates Command
    ↓
Agent polls Command
    ↓
Agent executes local action handler
    ↓
Agent reports CommandResult
```

Agent（代理） should execute only Commands assigned to itself.

---

## 22. CommandResult Model

CommandResult is the Agent（代理）'s report of execution outcome.

CommandResult may include:

```text
status
outputText
errorMessage
resultJson
startedAt
finishedAt
reportedAt
```

Rules:

- keep results concise;
- do not store large logs;
- do not include raw secrets;
- sanitize errors where practical;
- report failures explicitly.

---

## 23. Offline Behavior

Agent（代理） must handle Opstage（运维舞台） Backend downtime gracefully.

If Backend is unavailable, Agent（代理） should:

- keep Capsule Service（胶囊服务） running;
- retry registration/heartbeat/reporting later;
- avoid unbounded log spam;
- avoid losing local business function;
- re-report manifest when needed after recovery.

Governance failure should not automatically become business runtime failure.

---

## 24. 安全 Rules

Agent（代理） security rules:

1. Do not log registration token.
2. Do not log Agent（代理） token.
3. Do not report raw secrets.
4. Use `secretRef` for secret references.
5. Execute only predefined actions.
6. Do not include built-in shell execution.
7. Do not expose a remote terminal.
8. Validate handler existence before execution.
9. Report failures safely.
10. Keep Backend communication outbound-first in CE（社区版）.
11. Keep business runtime isolated from governance errors where practical.

---

## 25. Data Boundary

Agent（代理） may send governance metadata:

- Agent（代理） metadata;
- service manifest;
- health status;
- config metadata;
- action metadata;
- CommandResult;
- sanitized errors.

Agent（代理） should not send by default:

- raw passwords;
- raw cookies;
- OAuth tokens;
- API keys;
- private keys;
- account credentials;
- customer business records;
- large application logs;
- full browser traces.

Raw secrets should remain in customer-controlled runtime or secret providers.

---

## 26. Future EE（企业版） Agent（代理） Direction

Future EE（企业版） may add:

- Java Embedded Agent（代理） SDK;
- Python Embedded Agent（代理） SDK;
- Go Agent（代理） SDK;
- Sidecar Agent（代理）;
- External Agent（代理）;
- Host Agent（代理）;
- Kubernetes Agent（代理）;
- Agent（代理） diagnostics;
- Agent（代理） token rotation;
- Agent（代理） capability reporting;
- Agent（代理） compatibility matrix;
- enterprise secret provider integration;
- queue-backed or streaming command delivery.

These are not CE（社区版） v0.1 requirements.

---

## 27. Future Cloud（云版） Agent（代理） Direction

Future Cloud（云版） may add:

- Cloud（云版） Agent（代理） Gateway;
- multi-tenant Agent（代理） routing;
- workspace-scoped registration tokens;
- Cloud（云版） connection diagnostics;
- WebSocket or streaming delivery;
- Agent（代理） traffic rate limiting;
- usage metering by Agent（代理）;
- managed alerting on Agent（代理） state;
- Cloud（云版） enrollment UX.

These are not CE（社区版） v0.1 requirements.

---

## 28. CE（社区版） 实现 Acceptance Criteria

CE（社区版） Agent（代理） implementation is acceptable when:

- Node.js Embedded Agent（代理） SDK can be imported by a demo Capsule Service（胶囊服务）;
- Agent（代理） can register using registration token;
- Agent（代理） stores and reuses Agent（代理） token;
- Agent（代理） sends heartbeat;
- Agent（代理） reports service manifest;
- Agent（代理） reports health;
- Agent（代理） reports config metadata;
- Agent（代理） reports action definitions;
- Agent（代理） polls Commands;
- Agent（代理） executes predefined `echo` action;
- Agent（代理） executes predefined `runHealthCheck` action;
- Agent（代理） reports CommandResult;
- Backend downtime does not crash the Capsule Service（胶囊服务）;
- invalid or revoked token behavior is safe;
- raw tokens are not logged;
- raw secrets are not reported;
- arbitrary shell execution is not available.

---

## 29. Summary

Agent（代理） is the runtime-side governance bridge for Capsule Services.

CE（社区版） should implement a small, safe, Node.js Embedded Agent（代理） first. EE（企业版） and Cloud（云版） can later expand
Agent（代理） modes, runtimes, protocols, diagnostics, and deployment patterns.

The most important Agent（代理） rule is:

> Agent（代理） makes Capsule Services governable through safe metadata, health, configs, predefined actions, Commands, Results, and AuditEvents — not through unrestricted runtime control.
