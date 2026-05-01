<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 09-ce-agent-node-embedded.md
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

# CE（社区版） Node Embedded Agent（代理）

- Status: 实现 Target
- Edition: CE（社区版）
- Priority: Current
- Audience: agent SDK developers, Capsule Service（胶囊服务） developers, backend developers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/openapi/opstage-ce-v0.1.yaml` disagree, the ADRs and OpenAPI contract win for CE（社区版） v0.1.

This document 定义 the **Node.js Embedded Agent（代理）** design for **Opstage（运维舞台） CE（社区版） v0.1**.

The Node.js Embedded Agent（代理） is the first Agent（代理） implementation of `xtrape-capsule`. It runs inside a Node.js Capsule Service（胶囊服务） process and connects the service to Opstage（运维舞台） Backend.

---

## 1. Purpose

The purpose of the Node.js Embedded Agent（代理） is to make a Node.js Capsule Service（胶囊服务） governable by Opstage（运维舞台） without forcing the service to become dependent on Opstage（运维舞台） for its core startup and business logic.

The Agent（代理） SDK should provide:

- registration with Opstage（运维舞台） Backend;
- Agent（代理） token handling;
- heartbeat;
- service manifest reporting;
- health reporting;
- config metadata reporting;
- action definition reporting;
- command polling;
- predefined action execution;
- command result reporting;
- retry behavior when Backend is unavailable.

---

## 2. Positioning

The Node.js Embedded Agent（代理） is:

> A lightweight governance bridge embedded in a Node.js Capsule Service（胶囊服务）.

It is not:

- a service framework;
- a business logic framework;
- a process supervisor;
- a browser automation library;
- a secret vault;
- a remote shell execution tool;
- a full observability agent.

The Capsule Service（胶囊服务） owns its business logic. The Agent（代理） SDK owns the governance communication with Opstage（运维舞台）.

---

## 3. 架构 Role

The CE（社区版） v0.1 architecture is:

```text
Opstage UI
    ↓ Admin API
Opstage Backend
    ↑ Agent API
Node.js Embedded Agent SDK
    ↔ in-process providers and handlers
Capsule Service
```

The Agent（代理） SDK communicates only with Opstage（运维舞台） Backend.

The UI must never call the Agent（代理） SDK directly.

The Backend must never require inbound network access to the embedded Agent（代理）.

---

## 4. Core Responsibilities

The Node.js Embedded Agent（代理） SDK is responsible for:

1. reading SDK configuration;
2. loading stored Agent（代理） token if available;
3. registering with Backend using registration token if needed;
4. sending heartbeat periodically;
5. reporting Capsule Service（胶囊服务） manifest;
6. collecting health from health provider;
7. collecting config metadata from config provider;
8. reporting action definitions;
9. polling Commands from Backend;
10. dispatching `ACTION` Commands to local action handlers;
11. reporting CommandResults;
12. retrying communication failures without crashing the Capsule Service（胶囊服务）.

---

## 5. Non-Responsibilities

The SDK must not be responsible for:

- implementing Capsule Service（胶囊服务） business logic;
- implementing browser automation;
- managing account pools directly;
- storing raw business secrets in Opstage（运维舞台）;
- executing arbitrary shell commands;
- supervising external processes;
- providing sidecar or external Agent（代理） mode;
- implementing Java, Python, or Go Agent（代理） support;
- providing metrics, logs, or traces beyond CE（社区版） health and command reporting.

---

## 6. SDK Package

Recommended package name:

```text
@xtrape/capsule-agent-node
```

Alternative package names (not used in CE（社区版） v0.1):

```text
@xtrape/opstage-agent-node
```

CE（社区版） v0.1 location: the Node Agent（代理） SDK lives in its **own dedicated repository**, `xtrape-capsule-agent-node` (see [ADR 0008 — Naming and Repositories](../../08-decisions/0008-naming-and-repositories.md)). It is published to npm as `@xtrape/capsule-agent-node` and consumed by `xtrape-capsule-ce/apps/demo-capsule-service` (and external Capsule Service（胶囊服务） authors) via standard `pnpm add @xtrape/capsule-agent-node`. It is NOT a workspace package inside the CE（社区版） monorepo.

Recommended output:

```text
ESM first
TypeScript declarations
CommonJS compatibility if practical
```

---

## 7. Minimal Developer Experience

The SDK should make the common case simple.

Target usage:

```ts
import { CapsuleAgent } from '@xtrape/capsule-agent-node';

const agent = new CapsuleAgent({
  backendUrl: process.env.OPSTAGE_BACKEND_URL ?? 'http://localhost:8080',
  registrationToken: process.env.OPSTAGE_REGISTRATION_TOKEN,
  tokenStore: {
    file: process.env.OPSTAGE_AGENT_TOKEN_FILE ?? './data/agent-token.json',
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

This exact API may evolve during implementation, but CE（社区版） v0.1 should support this conceptual shape.

---

## 8. 配置

### 8.1 Required configuration

```ts
export interface CapsuleAgentOptions {
  backendUrl: string;
  registrationToken?: string;
  agent?: AgentIdentityOptions;
  service: CapsuleServiceOptions;
  tokenStore?: AgentTokenStoreOptions;
  heartbeatIntervalSeconds?: number;
  commandPollingIntervalSeconds?: number;
  commandTtlSeconds?: number;
  logger?: CapsuleAgentLogger;
}
```

### 8.2 Agent（代理） identity options

```ts
export interface AgentIdentityOptions {
  code?: string;
  name?: string;
  mode?: 'embedded';
  runtime?: 'nodejs';
  version?: string;
}
```

If `agent.code` is not provided, the SDK may derive a stable default from service code and hostname, but explicit code is preferred.

### 8.3 Service options

```ts
export interface CapsuleServiceOptions {
  code: string;
  name: string;
  description?: string;
  version: string;
  runtime?: 'nodejs';
  agentMode?: 'embedded';
  capabilities?: Array<string | CapsuleCapability>;
  resources?: CapsuleResourceDefinition[];
  metadata?: Record<string, unknown>;
}
```

### 8.4 Environment variables

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

## 9. Token Handling

### 9.1 Token types

The SDK handles two token types:

```text
registration token
agent token
```

A registration token is used only for first registration.

An Agent（代理） token is used for ongoing communication.

### 9.2 Token persistence

The SDK should support a token store abstraction.

Recommended interface:

```ts
export interface AgentTokenStore {
  load(): Promise<StoredAgentToken | null>;
  save(token: StoredAgentToken): Promise<void>;
  clear(): Promise<void>;
}

export interface StoredAgentToken {
  agentId: string;
  agentToken: string;
  workspaceId?: string;
  savedAt: string;
}
```

CE（社区版） v0.1 should provide a simple file token store.

### 9.3 File token store

Recommended behavior:

- store token in a local file controlled by the Capsule Service（胶囊服务） owner;
- create parent directory if missing;
- set restrictive file permissions where possible;
- do not print Agent（代理） token in logs;
- clear token if Backend says token is revoked or invalid.

### 9.4 Registration token rule

Registration token should not be used repeatedly after successful registration.

Preferred flow:

```text
Load stored Agent token
    ↓ if found
Use Agent token
    ↓ if missing or invalid
Use registration token to register
    ↓
Save Agent token
```

---

## 10. Startup Lifecycle

Recommended startup flow:

```text
Capsule Service starts
    ↓
Agent SDK is constructed
    ↓
Service registers health/config/action providers
    ↓
agent.start() is called
    ↓
SDK loads stored Agent token
    ↓
If no valid token, SDK registers with Backend
    ↓
SDK reports service manifest
    ↓
SDK starts heartbeat loop
    ↓
SDK starts command polling loop
```

### 10.1 Backend unavailable at startup

If Backend is unavailable, the SDK should:

- log a warning;
- keep retrying in background;
- not throw fatal error by default;
- not prevent Capsule Service（胶囊服务） startup.

The user may optionally configure strict startup mode later, but CE（社区版） v0.1 default should be non-blocking.

---

## 11. Registration Flow

### 11.1 Register request

The SDK calls:

```http
POST /api/agents/register
```

Request 包括:

- registration token;
- Agent（代理） identity;
- optional initial service manifest.

### 11.2 Register response

Backend returns:

```json
{
  "agentId": "agt_001",
  "agentToken": "opstage_agent_xxx",
  "workspaceId": "wks_default",
  "heartbeatIntervalSeconds": 30,
  "commandPollingIntervalSeconds": 5
}
```

### 11.3 SDK behavior

After successful registration, SDK should:

1. save Agent（代理） token;
2. update runtime Agent（代理） ID;
3. apply server-provided intervals if present;
4. report service manifest if not already accepted;
5. start heartbeat and command polling.

---

## 12. Manifest Reporting

The SDK should build a Capsule Manifest from:

- service options;
- registered capabilities;
- registered config providers or static configs;
- registered action definitions;
- resources;
- metadata.

Minimum manifest:

```json
{
  "kind": "CapsuleService",
  "schemaVersion": "1.0",
  "code": "demo-capsule-service",
  "name": "Demo Capsule Service",
  "version": "0.1.0",
  "runtime": "nodejs",
  "agentMode": "embedded",
  "capabilities": ["demo.echo"],
  "resources": [],
  "actions": [],
  "configs": []
}
```

The SDK should report manifest through:

```http
POST /api/agents/{agentId}/services/report
```

Manifest should be reported:

- after registration;
- after startup if Agent（代理） token already exists;
- periodically only if needed;
- when action/config metadata changes if dynamic update is supported later.

CE（社区版） v0.1 may report once at startup and again on reconnect.

---

## 13. Heartbeat Loop

The SDK should send heartbeat periodically.

Endpoint:

```http
POST /api/agents/{agentId}/heartbeat
Authorization: Bearer <agentToken>
```

Heartbeat payload should include:

- timestamp;
- Agent（代理） runtime metadata;
- service reported status;
- latest health if available.

Example:

```json
{
  "timestamp": "2026-04-30T10:21:00Z",
  "agent": {
    "version": "0.1.0",
    "hostname": "dev-machine",
    "os": "darwin",
    "arch": "arm64"
  },
  "services": [
    {
      "code": "demo-capsule-service",
      "reportedStatus": "ONLINE",
      "health": {
        "status": "UP",
        "checkedAt": "2026-04-30T10:21:00Z",
        "message": "Service is healthy."
      }
    }
  ]
}
```

### 13.1 Heartbeat failure behavior

If heartbeat fails, the SDK should:

- log a warning;
- retry on next interval;
- not crash the Capsule Service（胶囊服务）;
- detect invalid/revoked token and trigger re-registration or stop governance communication depending on error.

---

## 14. Health Provider

The SDK should support one health provider for CE（社区版） v0.1.

Recommended API:

```ts
agent.health(async () => ({
  status: 'UP',
  message: 'Service is healthy.',
  details: {},
  dependencies: [],
}));
```

Type shape:

```ts
export type HealthProvider = () => Promise<CapsuleHealthReport> | CapsuleHealthReport;

export interface CapsuleHealthReport {
  status: 'UP' | 'DOWN' | 'DEGRADED' | 'UNKNOWN';
  checkedAt?: string;
  message?: string;
  details?: Record<string, unknown>;
  dependencies?: DependencyHealth[];
}
```

If health provider throws, SDK should report:

```json
{
  "status": "UNKNOWN",
  "message": "Health provider failed."
}
```

and include sanitized error details if safe.

---

## 15. Config Provider

The SDK should support static configs and provider function.

Recommended API:

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

Type shape:

```ts
export type ConfigProvider = () => Promise<CapsuleConfigItem[]> | CapsuleConfigItem[];
```

Rules:

- do not report raw secrets;
- use `secretRef` for sensitive references;
- mark sensitive values with `sensitive: true`;
- config reporting failure should not crash the service.

CE（社区版） v0.1 支持 config visibility only. The SDK does not need to apply remote config changes.

---

## 16. Action Registry

The SDK should provide an action registry.

Recommended API:

```ts
agent.action({
  name: 'runHealthCheck',
  label: 'Run Health Check',
  description: 'Run a manual health check.',
  dangerLevel: 'LOW',
  handler: async () => {
    const health = await checkHealth();
    return {
      success: true,
      message: 'Health check completed.',
      data: health,
    };
  },
});
```

Type shape:

```ts
export interface CapsuleActionDefinition {
  name: string;
  label: string;
  description?: string;
  dangerLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  enabled?: boolean;
  inputSchema?: Record<string, unknown>;
  resultSchema?: Record<string, unknown>;
  confirmRequired?: boolean;
  timeoutSeconds?: number;
  metadata?: Record<string, unknown>;
}

export type CapsuleActionHandler = (
  payload: unknown,
  context: CapsuleActionContext
) => Promise<CapsuleActionResult> | CapsuleActionResult;

export interface CapsuleActionContext {
  commandId: string;
  actionName: string;
  serviceCode: string;
  agentId: string;
  requestedAt: string;
}

export interface CapsuleActionResult {
  success: boolean;
  message?: string;
  data?: unknown;
  error?: {
    code?: string;
    message: string;
    details?: unknown;
  };
}
```

Rules:

- action names must be unique within one Capsule Service（胶囊服务）;
- unknown actions must fail safely;
- no default shell action;
- action result must be JSON-serializable.

---

## 17. Command Polling

CE（社区版） v0.1 uses command polling.

Endpoint:

```http
GET /api/agents/{agentId}/commands
Authorization: Bearer <agentToken>
```

Polling interval default:

```text
5 seconds
```

SDK should:

1. poll Backend periodically;
2. ignore empty command lists;
3. process returned commands in order;
4. dispatch only supported command types;
5. report results;
6. avoid executing the same Command ID twice where practical.

CE（社区版） v0.1 支持 only:

```text
ACTION
```

---

## 18. Command Execution

For an `ACTION` Command, SDK should:

```text
Find service by serviceCode
    ↓
Find action handler by actionName
    ↓
Execute handler with payload and context
    ↓
Convert handler result to CommandResult
    ↓
Report CommandResult to Backend
```

Unknown action behavior:

```json
{
  "status": "FAILED",
  "outputText": "Action not found.",
  "errorMessage": "Action not found: refreshSession",
  "resultJson": {
    "success": false,
    "error": {
      "code": "ACTION_NOT_FOUND",
      "message": "Action not found: refreshSession"
    }
  }
}
```

Handler exception behavior:

```json
{
  "status": "FAILED",
  "outputText": "Action failed.",
  "errorMessage": "Action handler failed.",
  "resultJson": {
    "success": false,
    "error": {
      "code": "ACTION_FAILED",
      "message": "Action handler failed."
    }
  }
}
```

---

## 19. Command Result Reporting

Endpoint:

```http
POST /api/agents/{agentId}/commands/{commandId}/result
Authorization: Bearer <agentToken>
```

Successful result:

```json
{
  "status": "SUCCESS",
  "outputText": "Action completed.",
  "resultJson": {
    "success": true,
    "message": "Echo completed.",
    "data": {
      "message": "hello"
    }
  },
  "startedAt": "2026-04-30T10:22:01Z",
  "finishedAt": "2026-04-30T10:22:02Z"
}
```

Failed result:

```json
{
  "status": "FAILED",
  "outputText": "Action failed.",
  "errorMessage": "Action not found: refreshSession",
  "resultJson": {
    "success": false,
    "error": {
      "code": "ACTION_NOT_FOUND",
      "message": "Action not found: refreshSession"
    }
  },
  "startedAt": "2026-04-30T10:22:01Z",
  "finishedAt": "2026-04-30T10:22:02Z"
}
```

If result reporting fails, SDK should retry carefully.

CE（社区版） v0.1 may keep retry simple and log failures.

---

## 20. Error Handling

The SDK should handle these error categories:

### 20.1 Backend unavailable

Behavior:

- log warning;
- retry later;
- continue service runtime.

### 20.2 Registration token invalid

Behavior:

- log clear error;
- stop registration attempts until configuration changes;
- do not crash service unless strict mode is enabled.

### 20.3 Agent（代理） token invalid or revoked

Behavior:

- clear stored token;
- attempt re-registration if registration token is available;
- otherwise stop governance communication and log error.

### 20.4 Command execution error

Behavior:

- capture error;
- sanitize error details;
- report failed CommandResult;
- continue polling future commands.

### 20.5 Provider error

Behavior:

- health provider error should report `UNKNOWN`;
- config provider error should log warning and report no configs or last known configs;
- action handler error should report command failure.

---

## 21. 日志

The SDK should provide simple logging.

Recommended log levels:

```text
debug
info
warn
error
```

SDK must not log:

- raw Agent（代理） token;
- registration token;
- passwords;
- cookies;
- credentials;
- raw secrets.

Recommended default:

- log registration success;
- log heartbeat failures at warn level;
- log command execution failures;
- avoid noisy heartbeat success logs unless debug is enabled.

---

## 22. 安全 Rules

### 22.1 No arbitrary shell execution

The SDK must not include a built-in shell execution action.

Bad default action:

```text
runShell
exec
bash
```

### 22.2 Do not leak tokens

The SDK must not log Agent（代理） token or registration token.

### 22.3 Do not report raw secrets

Manifest, configs, health, command results, and action outputs should not contain raw secrets.

### 22.4 Use predefined handlers only

Commands must map to registered action handlers.

Unknown actions must fail safely.

### 22.5 Agent（代理） token protection

The SDK should store Agent（代理） token in a local file only if configured and should recommend restrictive permissions.

---

## 23. Demo Capsule Service（胶囊服务） Requirements

The demo service must use the Node.js Embedded Agent（代理） SDK.

Required service identity:

```text
code: demo-capsule-service
name: Demo Capsule Service
version: 0.1.0
runtime: nodejs
agentMode: embedded
```

Required health:

```json
{
  "status": "UP",
  "message": "Demo service is healthy."
}
```

Required config:

```json
{
  "key": "demo.message",
  "label": "Demo Message",
  "type": "string",
  "defaultValue": "hello capsule",
  "editable": true,
  "sensitive": false
}
```

Required actions:

```text
runHealthCheck
echo
```

---

## 24. Internal SDK Components

Recommended internal components:

```text
CapsuleAgent
AgentHttpClient
RegistrationManager
TokenStore
HeartbeatLoop
ServiceReporter
HealthCollector
ConfigCollector
ActionRegistry
CommandPoller
CommandExecutor
ResultReporter
AgentLogger
```

### 24.1 `CapsuleAgent`

Main public class.

### 24.2 `AgentHttpClient`

Handles HTTP requests to Backend.

### 24.3 `RegistrationManager`

Handles registration and token acquisition.

### 24.4 `TokenStore`

Loads, saves, and clears Agent（代理） token.

### 24.5 `HeartbeatLoop`

Sends heartbeat periodically.

### 24.6 `ServiceReporter`

Builds and reports manifest.

### 24.7 `ActionRegistry`

Stores action definitions and handlers.

### 24.8 `CommandPoller`

Polls commands.

### 24.9 `CommandExecutor`

Executes supported commands.

### 24.10 `ResultReporter`

Reports CommandResult.

---

## 25. CE（社区版） v0.1 Required SDK Features

CE（社区版） v0.1 SDK must implement:

- `CapsuleAgent` public class;
- registration with registration token;
- Agent（代理） token storage abstraction;
- file token store;
- heartbeat loop;
- service manifest reporting;
- health provider;
- config provider;
- action registry;
- command polling;
- `ACTION` command execution;
- CommandResult reporting;
- safe error handling;
- safe logging;
- no arbitrary shell action.

---

## 26. Out of Scope for CE（社区版） v0.1 SDK

The SDK does not need:

- sidecar mode;
- external Agent（代理） mode;
- Java/Python/Go support;
- WebSocket command channel;
- gRPC streaming;
- message queue integration;
- automatic config update application;
- secret vault integration;
- metrics exporter;
- log streaming;
- process supervision;
- arbitrary shell command execution.

---

## 27. SDK Acceptance Criteria

The SDK is acceptable when:

- demo service can instantiate `CapsuleAgent`;
- Agent（代理） can register with Backend;
- Agent（代理） token is saved and reused;
- Agent（代理） sends heartbeat;
- Agent（代理） reports manifest;
- Agent（代理） reports health;
- Agent（代理） reports configs and actions;
- Agent（代理） polls Commands;
- Agent（代理） executes `echo` and `runHealthCheck`;
- Agent（代理） reports CommandResult;
- Backend downtime does not crash the service;
- invalid token handling is safe;
- raw tokens are not logged;
- no shell execution action exists.

---

## 28. Summary

The Node.js Embedded Agent（代理） is the first integration path for Opstage（运维舞台） CE（社区版）.

It should be small, safe, and easy to embed.

The most important SDK rule is:

> The Agent（代理） makes a Capsule Service（胶囊服务） governable, but it must not take over the service's business runtime.
