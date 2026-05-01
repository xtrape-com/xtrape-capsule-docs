<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 03-opstage-agent-integration.md
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

# Opstage（运维舞台） Agent（代理） Integration

- Status: 实施指南
- Edition: 共享
- Priority: 高
- Audience: agent SDK developers, backend developers, Capsule Service（胶囊服务） developers, architects, security reviewers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/openapi/opstage-ce-v0.1.yaml` disagree, the ADRs and OpenAPI contract win for CE（社区版） v0.1.

This document 定义 the Agent（代理） integration subsystem of **Opstage（运维舞台）**.

Agent（代理） integration is the bridge between Opstage（运维舞台） Backend and Capsule Services. It allows lightweight services to become visible, manageable, and auditable without becoming dependent on Opstage（运维舞台） for their core business runtime.

The current implementation focus is **Opstage（运维舞台） CE（社区版）**. EE（企业版） and Cloud（云版） Agent（代理） capabilities are future planning tracks and must not expand the CE（社区版） v0.1 implementation scope.

---

## 1. Purpose

The purpose of Agent（代理） integration is to make Capsule Services governable by Opstage（运维舞台）.

Agent（代理） integration should allow Opstage（运维舞台） to:

- register Agents;
- authenticate Agents;
- receive heartbeats;
- receive Capsule Service（胶囊服务） manifests;
- receive health reports;
- receive config metadata;
- receive predefined action metadata;
- deliver Commands;
- receive CommandResults;
- record audit-relevant operation results;
- calculate Agent（代理） and service freshness.

Agent（代理） integration should not take over the Capsule Service（胶囊服务）'s business runtime.

---

## 2. Positioning

An Agent（代理） is:

> A governance bridge between Opstage（运维舞台） Backend and one or more Capsule Services.

An Agent（代理） is not:

- the Capsule Service（胶囊服务） itself;
- the business logic owner;
- a remote shell;
- a generic process supervisor;
- a secret vault;
- a browser automation framework by itself;
- a full observability collector in CE（社区版）;
- a deployment orchestrator in CE（社区版）.

The Agent（代理） makes the service governable, but the service remains responsible for its own business behavior.

---

## 3. Relationship with Opstage（运维舞台） Components

Recommended CE（社区版） relationship:

```text
Opstage UI
    ↓ Admin API
Opstage Backend
    ↑ Agent API
Node.js Embedded Agent SDK
    ↔ Capsule Service providers and handlers
Capsule Service
```

The Agent（代理） communicates with Opstage（运维舞台） Backend through Agent（代理） APIs.

The UI never calls Agent（代理） directly.

The Backend does not require inbound network access to the Agent（代理） in CE（社区版）.

---

## 4. Core Agent（代理） Responsibilities

The Agent（代理） is responsible for:

- loading Agent（代理） configuration;
- registering with Opstage（运维舞台） using a registration token;
- storing Agent（代理） token locally;
- authenticating to Backend with Agent（代理） token;
- sending heartbeat;
- reporting service manifest;
- reporting health;
- reporting config metadata;
- reporting action definitions;
- polling Commands;
- executing predefined local action handlers;
- reporting CommandResults;
- retrying Backend communication failures safely;
- avoiding raw secret leakage.

---

## 5. Agent（代理） Non-Responsibilities

CE（社区版） Agent（代理） should not be responsible for:

- executing arbitrary shell commands;
- managing all application logs;
- collecting arbitrary metrics and traces;
- storing raw secrets in Opstage（运维舞台）;
- replacing service-specific business logic;
- starting or supervising the Capsule Service（胶囊服务） process;
- providing sidecar/external management mode;
- supporting Java/Python/Go runtimes;
- implementing Cloud（云版） Agent（代理） Gateway behavior;
- implementing enterprise secret provider integration.

Future editions may add some of these through explicit designs, but CE（社区版） Agent（代理） should stay small and safe.

---

## 6. CE（社区版） Agent（代理） Scope

Opstage（运维舞台） CE（社区版） v0.1 implements one Agent（代理） mode:

```text
Node.js embedded Agent SDK
```

The CE（社区版） Agent（代理） SDK should support:

- registration with registration token;
- Agent（代理） token storage;
- heartbeat;
- service manifest report;
- health provider;
- config provider;
- action registry;
- command polling;
- predefined action execution;
- CommandResult reporting;
- basic retry behavior;
- safe logging;
- sensitive value masking guidance.

---

## 7. CE（社区版） Agent（代理） Non-Goals

CE（社区版） v0.1 Agent（代理） integration should not implement:

- sidecar Agent（代理）;
- external Agent（代理）;
- host Agent（代理）;
- Kubernetes Agent（代理）;
- Java Agent（代理） SDK;
- Python Agent（代理） SDK;
- Go Agent（代理） SDK;
- Agent（代理） Gateway;
- WebSocket command channel;
- gRPC streaming;
- offline command queue;
- Agent（代理） auto-upgrade;
- Agent（代理） fleet management;
- service discovery;
- enterprise secret provider resolver;
- arbitrary shell execution.

These are future EE（企业版） or Cloud（云版） planning items.

---

## 8. Agent（代理） Modes

Long-term Agent（代理） modes may include:

||Mode|Description|CE（社区版） v0.1||
|---|---|---|
||embedded|Agent（代理） runs inside Capsule Service（胶囊服务） process|Node.js only||
||sidecar|Agent（代理） runs beside one service|Not implemented||
||external|Agent（代理） manages one or more services externally|Not implemented||
||host|Agent（代理） manages services on one host|Not implemented||
||kubernetes|Agent（代理） manages services in a Kubernetes cluster|Not implemented||

CE（社区版） should preserve the `agentMode` field but only implement `embedded`.

---

## 9. Node.js Embedded Agent（代理）

The Node.js Embedded Agent（代理） runs inside a Node.js Capsule Service（胶囊服务） process.

Example:

```text
Node.js process
├── Capsule Service business logic
└── Opstage Agent SDK
```

Strengths:

- easiest first implementation;
- direct access to service health and actions;
- no extra process required;
- easy for CAPI and automation services built with Node.js;
- good fit for CE（社区版） prototype.

Limitations:

- requires code integration;
- applies only to Node.js services in CE（社区版）;
- cannot manage legacy or non-Node services;
- Agent（代理） failures must not crash the business service by default.

---

## 10. Minimal SDK Usage

Target developer experience:

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

The exact API may evolve during implementation, but the CE（社区版） developer experience should stay close to this shape.

---

## 11. Agent（代理） 配置

Recommended Agent（代理） configuration options:

```text
backendUrl
registrationToken
agentCode
agentName
service code
service name
service version
token store path
heartbeat interval
command polling interval
log level
```

Recommended environment variables:

```text
OPSTAGE_BACKEND_URL=http://localhost:8080
OPSTAGE_REGISTRATION_TOKEN=opstage_reg_xxx
OPSTAGE_AGENT_TOKEN_FILE=./data/agent-token.json
OPSTAGE_AGENT_CODE=local-dev-agent
OPSTAGE_AGENT_NAME=Local Development Agent
OPSTAGE_HEARTBEAT_INTERVAL_SECONDS=30
OPSTAGE_COMMAND_POLL_INTERVAL_SECONDS=5
```

---

## 12. Registration Flow

Agent（代理） registration flow:

```text
Admin creates registration token in Opstage UI
    ↓
Capsule Service starts with embedded Agent SDK
    ↓
Agent loads stored Agent token if available
    ↓
If no token, Agent submits registration token to Backend
    ↓
Backend validates registration token
    ↓
Backend creates Agent and Agent token
    ↓
Agent stores Agent token locally
    ↓
Agent uses Agent token for future calls
```

Registration endpoint:

```http
POST /api/agents/register
```

Registration token should be:

- shown only once;
- stored as hash in Backend;
- scoped to default Workspace in CE（社区版）;
- revocable;
- optionally expiring;
- optionally one-time use.

---

## 13. Agent（代理） Token Handling

Agent（代理） token is used after registration.

Rules:

- Backend stores only token hash;
- Agent（代理） stores raw token locally through a token store;
- Agent（代理） sends token via 授权 header;
- Agent（代理） token must not be logged;
- Agent（代理） token should be cleared if Backend reports revoked or invalid token;
- token rotation is future EE（企业版） work.

授权 header:

```http
Authorization: Bearer <agentToken>
```

---

## 14. Startup Lifecycle

Recommended Agent（代理） startup lifecycle:

```text
Capsule Service starts
    ↓
Agent SDK is constructed
    ↓
Service registers health/config/action providers
    ↓
agent.start() is called
    ↓
Agent loads stored Agent token
    ↓
Agent registers if needed
    ↓
Agent reports manifest
    ↓
Agent starts heartbeat loop
    ↓
Agent starts command polling loop
```

If Backend is unavailable at startup, Agent（代理） should:

- log a warning;
- retry in background;
- not crash the Capsule Service（胶囊服务） by default;
- keep the business service running.

---

## 15. Heartbeat Flow

Heartbeat flow:

```text
Agent timer fires
    ↓
Agent collects runtime metadata and optional latest health
    ↓
Agent sends heartbeat to Backend
    ↓
Backend validates Agent token
    ↓
Backend updates lastHeartbeatAt
    ↓
Backend recalculates Agent/service freshness
```

Endpoint:

```http
POST /api/agents/{agentId}/heartbeat
Authorization: Bearer <agentToken>
```

Heartbeat should include:

- timestamp;
- Agent（代理） version;
- runtime metadata;
- service status summary if available;
- latest health if lightweight.

Do not send raw secrets in heartbeat.

---

## 16. Service Manifest Report Flow

Manifest report flow:

```text
Agent builds manifest
    ↓
Agent sends manifest to Backend
    ↓
Backend validates Agent token
    ↓
Backend upserts Capsule Service
    ↓
Backend stores manifest, configs, and actions
    ↓
Backend updates lastReportedAt
```

Endpoint:

```http
POST /api/agents/{agentId}/services/report
Authorization: Bearer <agentToken>
```

Manifest should include:

```text
service identity
runtime
version
agentMode
capabilities
resources
configs
actions
metadata
```

Manifest must not include raw secrets.

---

## 17. Health Provider

Agent（代理） SDK should allow Capsule Service（胶囊服务） to register a health provider.

Example:

```ts
agent.health(async () => ({
  status: 'UP',
  message: 'Service is healthy.',
  dependencies: [],
}));
```

Recommended status values:

```text
UP
DOWN
DEGRADED
UNKNOWN
```

If the health provider throws, Agent（代理） should report safe `UNKNOWN` health or log the provider failure without crashing the service.

---

## 18. Config Provider

Agent（代理） SDK should allow Capsule Service（胶囊服务） to expose config metadata.

Example:

```ts
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
```

Rules:

- report metadata, not raw secrets;
- use `sensitive: true` for sensitive configs;
- use `secretRef` for secret references;
- CE（社区版） v0.1 支持 visibility only;
- config editing and publishing are future EE（企业版） work.

---

## 19. Action Registry

Agent（代理） SDK should allow Capsule Service（胶囊服务） to register predefined actions.

Example:

```ts
agent.action({
  name: 'runHealthCheck',
  label: 'Run Health Check',
  dangerLevel: 'LOW',
  handler: async () => {
    return {
      success: true,
      message: 'Health check completed.',
    };
  },
});
```

Action rules:

- action names must be unique per service;
- actions must be predefined;
- unknown actions fail safely;
- action results must be JSON-serializable;
- no built-in arbitrary shell action;
- high-risk actions should declare `dangerLevel`.

---

## 20. Command Polling Flow

CE（社区版） command delivery uses polling.

Flow:

```text
Agent polling timer fires
    ↓
Agent calls Backend for pending Commands
    ↓
Backend validates Agent token
    ↓
Backend returns Commands assigned to this Agent
    ↓
Agent executes each supported Command
    ↓
Agent reports CommandResult
```

Endpoint:

```http
GET /api/agents/{agentId}/commands
Authorization: Bearer <agentToken>
```

CE（社区版） v0.1 支持 only:

```text
ACTION
```

as Command type.

---

## 21. Command Execution Flow

For an `ACTION` Command:

```text
Agent receives Command
    ↓
Agent finds target service
    ↓
Agent finds action handler by actionName
    ↓
Agent executes handler with payload and context
    ↓
Agent captures result or error
    ↓
Agent reports CommandResult to Backend
```

Unknown action behavior:

```text
status: FAILED
error code: ACTION_NOT_FOUND
```

Handler exception behavior:

```text
status: FAILED
error code: ACTION_FAILED
```

Agent（代理） should continue processing future Commands after one command fails.

---

## 22. CommandResult Reporting

Endpoint:

```http
POST /api/agents/{agentId}/commands/{commandId}/result
Authorization: Bearer <agentToken>
```

CommandResult should include:

```text
status
outputText
errorMessage
resultJson
startedAt
finishedAt
```

Rules:

- do not include raw secrets;
- sanitize errors where practical;
- report result only for assigned Commands;
- retry result reporting carefully if Backend is temporarily unavailable;
- avoid duplicate execution where practical.

---

## 23. Error Handling

Agent（代理） should handle these error categories:

### Backend unavailable

Behavior:

- log warning;
- retry later;
- keep Capsule Service（胶囊服务） running.

### Registration token invalid

Behavior:

- log clear error;
- stop repeated noisy registration attempts;
- keep business service running unless strict mode is configured.

### Agent（代理） token invalid or revoked

Behavior:

- clear stored token if safe;
- attempt re-registration only if registration token is available;
- otherwise stop governance communication and log error.

### Provider failure

Behavior:

- health provider failure reports `UNKNOWN`;
- config provider failure logs warning;
- action handler failure reports failed CommandResult.

---

## 24. 安全 Rules

Agent（代理） integration must follow these security rules:

1. Do not log registration token.
2. Do not log Agent（代理） token.
3. Do not report raw secrets.
4. Use `secretRef` for secret references.
5. Execute only predefined action handlers.
6. Do not include built-in shell action.
7. Validate command ownership through Backend.
8. Treat Backend errors carefully.
9. Keep business service running when governance Backend is unavailable.
10. Sanitize error details where practical.

---

## 25. Data Boundary

Agent（代理） may send governance metadata to Backend:

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
- OAuth access tokens;
- OAuth refresh tokens;
- private keys;
- raw account credentials;
- large application logs;
- customer business records.

Use `secretRef` for sensitive references.

---

## 26. 日志 Rules

Agent（代理） logs should include useful operational information:

- registration success;
- registration failure without token exposure;
- heartbeat failure;
- service report failure;
- command execution failure;
- command result report failure.

Agent（代理） logs must not include:

- registration token;
- Agent（代理） token;
- passwords;
- cookies;
- API keys;
- OAuth tokens;
- raw secrets.

---

## 27. Offline Behavior

If Opstage（运维舞台） Backend is offline, Agent（代理） should:

- keep Capsule Service（胶囊服务） running;
- retry heartbeat and polling;
- avoid unbounded log spam;
- avoid crashing the process;
- report latest state once Backend recovers;
- re-report manifest if needed.

Governance availability should not become business runtime availability.

---

## 28. Future EE（企业版） Agent（代理） Extensions

Future EE（企业版） may add:

- Java embedded Agent（代理） SDK;
- Python embedded Agent（代理） SDK;
- Go Agent（代理） SDK;
- sidecar Agent（代理）;
- external Agent（代理）;
- host Agent（代理）;
- Kubernetes Agent（代理）;
- Agent（代理） capability reporting;
- Agent（代理） diagnostics UI;
- Agent（代理） token rotation;
- Agent（代理） version compatibility matrix;
- secret provider integration;
- WebSocket or queue-backed command delivery.

These are not CE（社区版） v0.1 requirements.

---

## 29. Future Cloud（云版） Agent（代理） Extensions

Future Cloud（云版） may add:

- Agent（代理） Gateway;
- multi-tenant Agent（代理） routing;
- Cloud（云版） connection diagnostics;
- rate limiting;
- WebSocket or streaming connections;
- hosted Agent（代理） enrollment flow;
- workspace-scoped registration tokens;
- usage metering by Agent（代理）;
- managed alerting on Agent（代理） state.

These are not CE（社区版） v0.1 requirements.

---

## 30. Acceptance Criteria

Opstage（运维舞台） CE（社区版） Agent（代理） integration is acceptable when:

- Node.js embedded Agent（代理） SDK can be imported by demo service;
- Agent（代理） can register with Backend using registration token;
- Agent（代理） token is stored locally and reused;
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
- invalid token handling is safe;
- raw tokens are not logged;
- raw secrets are not reported;
- no arbitrary shell action exists.

---

## 31. Summary

Opstage（运维舞台） Agent（代理） integration is the bridge that makes Capsule Services governable.

It should be lightweight, safe, outbound-first, and based on predefined capabilities.

The most important Agent（代理） integration rule is:

> The Agent（代理） makes a Capsule Service（胶囊服务） visible and operable through Opstage（运维舞台）, but it must not take ownership of the service's business runtime or expose unsafe arbitrary execution.
