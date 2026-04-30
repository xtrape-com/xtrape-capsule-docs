# Agent Overview

- Status: Draft
- Edition: Shared
- Priority: High

本文件属于 `xtrape-capsule` 文档集。`xtrape-capsule` 是面向轻服务 / Capsule Service 的领域体系；`xtrape-capsule-opstage` 是该体系下的统一运行态治理平台。

当前实现重点是 CE 开源社区版。EE 私有化商业版与 Cloud SaaS 版属于未来规划，CE 需要保留扩展点，但不应在早期版本实现其完整能力。

Agent 是 Capsule Service 加入 Opstage 治理体系的授权入口。CE 第一版实现 Node.js Embedded Agent，Sidecar 和 External Agent 属于后续扩展。

# Agent Overview

- Status: Implementation Guidance
- Edition: Shared
- Priority: High
- Audience: agent SDK developers, Capsule Service developers, backend developers, architects, security reviewers, AI coding agents

This document defines the overall Agent concept for the `xtrape-capsule` product family.

An Agent is the authorized governance bridge that allows a Capsule Service to join the Opstage runtime governance system.

The current implementation focus is **CE**. CE v0.1 implements only the **Node.js Embedded Agent**. Sidecar Agent, External Agent, Host Agent, Kubernetes Agent, and multi-language Agent SDKs are future EE/Cloud extension tracks and must not expand the CE v0.1 implementation scope.

---

## 1. Purpose

The purpose of an Agent is to make Capsule Services governable by Opstage.

An Agent allows Opstage to:

- register a runtime participant;
- authenticate runtime communication;
- receive heartbeat signals;
- receive Capsule Service manifests;
- receive health reports;
- receive config metadata;
- receive predefined action metadata;
- deliver Commands;
- receive CommandResults;
- support auditability;
- calculate freshness and effective status.

The Agent is the runtime-side entry point into Opstage governance.

---

## 2. Positioning

An Agent is:

> The authorized bridge between Opstage Backend and one or more Capsule Services.

It is responsible for governance communication, not business ownership.

The Agent makes a Capsule Service visible and operable through Opstage, but it should not take over the service's core business behavior.

---

## 3. What an Agent Is Not

An Agent is not:

- the Capsule Service itself;
- the business logic owner;
- a generic process supervisor in CE;
- a remote shell;
- a secret vault;
- a full observability collector in CE;
- a deployment orchestrator in CE;
- a browser automation framework by itself;
- a Kubernetes operator in CE;
- a workflow engine.

Future editions may introduce stronger Agent modes, but the Agent identity should remain governance bridge, not unrestricted runtime controller.

---

## 4. Relationship with Capsule Service

A Capsule Service is the lightweight service being governed.

An Agent is the bridge that reports the service and executes predefined governance operations.

Recommended relationship in CE:

```text
Capsule Service process
├── business logic
└── Node.js Embedded Agent SDK
    ↓ outbound HTTP
Opstage Backend
```

The Capsule Service continues to own:

- business APIs;
- business data;
- internal workflows;
- local configuration;
- local secrets;
- domain behavior.

The Agent owns:

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

## 5. Relationship with Opstage

Opstage consists of:

```text
Opstage UI
Opstage Backend
Agent integration
```

Agent communicates only with Opstage Backend through Agent APIs.

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

The UI must not call Agent directly.

The Backend should not require inbound network access to Agent in CE.

---

## 6. Core Agent Responsibilities

An Agent is responsible for:

- loading Agent configuration;
- registering with Opstage using a registration token;
- storing the issued Agent token locally;
- authenticating Agent API calls;
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

## 7. Core Agent Non-Responsibilities

CE Agent should not be responsible for:

- executing arbitrary shell commands;
- running arbitrary scripts;
- replacing the service's business logic;
- storing raw secrets in Opstage;
- collecting all application logs;
- collecting all metrics and traces;
- supervising service processes;
- automatically discovering all services on a host;
- managing Kubernetes resources;
- implementing SaaS billing or tenant behavior;
- implementing enterprise SSO or RBAC.

These are either out of scope or future extension topics.

---

## 8. Agent Modes

Long-term Agent modes may include:

```text
embedded
sidecar
external
host
kubernetes
```

### 8.1 Embedded Agent

Agent runs inside the Capsule Service process.

CE implements:

```text
Node.js Embedded Agent
```

### 8.2 Sidecar Agent

Agent runs beside one Capsule Service and communicates through local management endpoints, local IPC, or mounted files.

This is future EE work.

### 8.3 External Agent

Agent runs outside one or more services and manages them through configured targets.

This is future EE work.

### 8.4 Host Agent

Agent runs on a host and manages multiple configured local services.

This is long-term EE work.

### 8.5 Kubernetes Agent

Agent runs inside Kubernetes and manages annotated or configured workloads.

This is long-term EE work.

---

## 9. CE Agent Scope

CE v0.1 implements only:

```text
Node.js Embedded Agent SDK
```

Required CE Agent capabilities:

- initialize from configuration;
- register with registration token;
- persist Agent token locally;
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

## 10. CE Agent Non-Goals

CE v0.1 must not implement:

- sidecar Agent;
- external Agent;
- host Agent;
- Kubernetes Agent;
- Java Agent SDK;
- Python Agent SDK;
- Go Agent SDK;
- WebSocket command channel;
- gRPC streaming;
- Agent Gateway;
- automatic service discovery;
- Agent fleet upgrade manager;
- enterprise secret provider resolver;
- arbitrary shell execution;
- remote terminal.

These capabilities may be considered after the CE governance loop is proven.

---

## 11. Node.js Embedded Agent

The Node.js Embedded Agent is the CE reference Agent implementation.

It runs inside a Node.js Capsule Service process.

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

The embedded Agent should be lightweight and should not require a separate process.

---

## 12. Developer Experience Target

A Capsule Service developer should be able to integrate the Agent with a small amount of code.

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

## 13. Agent Lifecycle

Recommended CE Agent lifecycle:

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

If Opstage Backend is unavailable, the Agent should retry in the background and keep the Capsule Service running where practical.

---

## 14. Registration Model

Agent registration is the first trusted enrollment step.

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
- scoped to default Workspace in CE;
- optionally expiring;
- optionally one-time use;
- revocable if Backend supports it.

---

## 15. Agent Token Model

After registration, the Agent authenticates with an Agent token.

Rules:

- Backend stores only token hash;
- Agent stores raw token locally;
- Agent sends token through `Authorization: Bearer` header;
- token must not be logged;
- token should be cleared or marked invalid if Backend rejects it as revoked;
- token rotation is future EE work.

Example header:

```http
Authorization: Bearer <agentToken>
```

---

## 16. Heartbeat Model

Heartbeat tells Opstage that the Agent is still alive.

Heartbeat should include:

- Agent identity derived from token;
- timestamp;
- Agent version;
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

Agent reports a service manifest to describe the Capsule Service.

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

Agent exposes service health through a health provider.

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

Agent exposes configuration metadata, not full configuration-center behavior.

CE supports config visibility only.

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

Config editing and publishing are future EE capabilities.

---

## 20. Action Model

Agent exposes predefined actions.

An action is a safe, named operation implemented by the Capsule Service.

Examples:

```text
echo
runHealthCheck
reloadConfig
clearCache
refreshSession
```

CE action rules:

- actions must be predefined;
- unknown actions fail safely;
- action names must be stable;
- action handlers must return serializable results;
- no arbitrary shell action;
- high-risk actions should declare danger level.

---

## 21. Command Model

Commands are created by Backend and polled by Agent.

CE supports:

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

Agent should execute only Commands assigned to itself.

---

## 22. CommandResult Model

CommandResult is the Agent's report of execution outcome.

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

Agent must handle Opstage Backend downtime gracefully.

If Backend is unavailable, Agent should:

- keep Capsule Service running;
- retry registration/heartbeat/reporting later;
- avoid unbounded log spam;
- avoid losing local business function;
- re-report manifest when needed after recovery.

Governance failure should not automatically become business runtime failure.

---

## 24. Security Rules

Agent security rules:

1. Do not log registration token.
2. Do not log Agent token.
3. Do not report raw secrets.
4. Use `secretRef` for secret references.
5. Execute only predefined actions.
6. Do not include built-in shell execution.
7. Do not expose a remote terminal.
8. Validate handler existence before execution.
9. Report failures safely.
10. Keep Backend communication outbound-first in CE.
11. Keep business runtime isolated from governance errors where practical.

---

## 25. Data Boundary

Agent may send governance metadata:

- Agent metadata;
- service manifest;
- health status;
- config metadata;
- action metadata;
- CommandResult;
- sanitized errors.

Agent should not send by default:

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

## 26. Future EE Agent Direction

Future EE may add:

- Java Embedded Agent SDK;
- Python Embedded Agent SDK;
- Go Agent SDK;
- Sidecar Agent;
- External Agent;
- Host Agent;
- Kubernetes Agent;
- Agent diagnostics;
- Agent token rotation;
- Agent capability reporting;
- Agent compatibility matrix;
- enterprise secret provider integration;
- queue-backed or streaming command delivery.

These are not CE v0.1 requirements.

---

## 27. Future Cloud Agent Direction

Future Cloud may add:

- Cloud Agent Gateway;
- multi-tenant Agent routing;
- workspace-scoped registration tokens;
- Cloud connection diagnostics;
- WebSocket or streaming delivery;
- Agent traffic rate limiting;
- usage metering by Agent;
- managed alerting on Agent state;
- Cloud enrollment UX.

These are not CE v0.1 requirements.

---

## 28. CE Implementation Acceptance Criteria

CE Agent implementation is acceptable when:

- Node.js Embedded Agent SDK can be imported by a demo Capsule Service;
- Agent can register using registration token;
- Agent stores and reuses Agent token;
- Agent sends heartbeat;
- Agent reports service manifest;
- Agent reports health;
- Agent reports config metadata;
- Agent reports action definitions;
- Agent polls Commands;
- Agent executes predefined `echo` action;
- Agent executes predefined `runHealthCheck` action;
- Agent reports CommandResult;
- Backend downtime does not crash the Capsule Service;
- invalid or revoked token behavior is safe;
- raw tokens are not logged;
- raw secrets are not reported;
- arbitrary shell execution is not available.

---

## 29. Summary

Agent is the runtime-side governance bridge for Capsule Services.

CE should implement a small, safe, Node.js Embedded Agent first. EE and Cloud can later expand Agent modes, runtimes, protocols, diagnostics, and deployment patterns.

The most important Agent rule is:

> Agent makes Capsule Services governable through safe metadata, health, configs, predefined actions, Commands, Results, and AuditEvents — not through unrestricted runtime control.