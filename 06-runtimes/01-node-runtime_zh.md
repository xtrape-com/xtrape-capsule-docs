<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 01-node-runtime.md
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

# Node Runtime

- Status: 实现 Target
- Edition: CE（社区版）
- Priority: 高
- Audience: Capsule Service（胶囊服务） developers, Node.js developers, agent SDK developers, backend developers, test engineers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/` (OpenAPI / Prisma) disagree, the ADRs and contracts win for CE（社区版） v0.1.

This document 定义 the **Node.js Runtime** integration for Opstage（运维舞台） CE（社区版）.

Node.js is the first and reference runtime for `xtrape-capsule`. CE（社区版） v0.1 uses Node.js to prove the complete Capsule governance loop through a Node.js Capsule Service（胶囊服务） and the Node.js Embedded Agent（代理） SDK.

Java, Python, Go, Sidecar runtime integration, External Agent（代理） runtime integration, and Kubernetes runtime integration are future EE（企业版）/Cloud（云版） extension tracks and must not expand the CE（社区版） v0.1 implementation scope.

---

## 1. Purpose

The purpose of the Node.js Runtime is to define how a Node.js service becomes a Capsule Service（胶囊服务） governed by Opstage（运维舞台）.

The Node.js runtime should define:

- service identity conventions;
- SDK package usage;
- runtime configuration;
- Agent（代理） registration;
- Agent（代理） token storage;
- health provider integration;
- config metadata provider integration;
- predefined action registration;
- Command polling and execution;
- CommandResult reporting;
- sensitive data rules;
- demo service expectations;
- testing requirements.

The goal is to make Node.js services easy to govern without forcing a heavy microservice framework.

---

## 2. Runtime Scope

CE（社区版） v0.1 Node.js Runtime 包括:

```text
Node.js Capsule Service conventions
Node.js Embedded Agent SDK
TypeScript-first integration
file-based Agent token store
health provider
config provider
action registry
HTTP polling command delivery
CommandResult reporting
Docker-friendly demo service
```

CE（社区版） v0.1 Node.js Runtime does not include:

```text
Sidecar Agent
External Agent
multi-target Agent
Java/Python/Go SDKs
WebSocket/gRPC delivery
Agent Gateway
config publishing
secret provider integration
remote shell
arbitrary script execution
full observability collector
```

---

## 3. Runtime Requirements

Recommended runtime baseline:

```text
Node.js 20 LTS or later
TypeScript-first
ESM-first if repository standard allows it
```

The runtime should support:

- local development;
- Docker deployment;
- npm package usage;
- environment-variable configuration;
- HTTP communication with Opstage（运维舞台） Backend;
- safe operation when Opstage（运维舞台） Backend is temporarily unavailable.

The Node.js runtime should avoid heavy dependencies in CE（社区版） v0.1.

---

## 4. SDK Package

Node.js Runtime should use the CE（社区版） Node Agent（代理） SDK package:

```text
@xtrape/capsule-agent-node
```

This package 提供:

- `CapsuleAgent` class;
- registration client;
- file token store;
- heartbeat loop;
- manifest reporter;
- health provider API;
- config provider API;
- action registry;
- command polling loop;
- CommandResult reporter;
- basic retry/backoff;
- sanitized logging.

The SDK is the official CE（社区版） integration path for Node.js Capsule Services.

---

## 5. Node.js Capsule Service（胶囊服务） Definition

A Node.js Capsule Service（胶囊服务） is a Node.js application that:

- owns its business logic;
- integrates the Node Agent（代理） SDK;
- declares stable service identity;
- exposes health through a provider;
- exposes config metadata through a provider;
- exposes predefined actions through handlers;
- allows the Agent（代理） SDK to communicate with Opstage（运维舞台） Backend.

A Capsule Service（胶囊服务） is not required to expose its own admin UI.

Opstage（运维舞台） UI becomes the common governance surface.

---

## 6. Minimal Integration Example

Reference integration:

```ts
import { CapsuleAgent } from '@xtrape/capsule-agent-node';

const agent = new CapsuleAgent({
  backendUrl: process.env.OPSTAGE_BACKEND_URL ?? 'http://localhost:8080',
  registrationToken: process.env.OPSTAGE_REGISTRATION_TOKEN,
  tokenStore: {
    file: process.env.OPSTAGE_AGENT_TOKEN_FILE ?? './data/agent-token.json',
  },
  agent: {
    code: process.env.OPSTAGE_AGENT_CODE ?? 'local-node-agent',
    name: process.env.OPSTAGE_AGENT_NAME ?? 'Local Node Agent',
  },
  service: {
    code: 'demo-node-capsule-service',
    name: 'Demo Node Capsule Service',
    description: 'A demo Node.js Capsule Service for Opstage CE.',
    version: '0.1.0',
    runtime: 'nodejs',
  },
});

agent.health(async () => ({
  status: 'UP',
  message: 'Node service is healthy.',
}));

agent.configs(() => [
  {
    key: 'demo.message',
    label: 'Demo Message',
    type: 'string',
    valuePreview: process.env.DEMO_MESSAGE ?? 'hello capsule',
    editable: true,
    sensitive: false,
    source: 'env',
  },
]);

agent.action({
  name: 'echo',
  label: 'Echo',
  description: 'Returns the submitted payload.',
  dangerLevel: 'LOW',
  handler: async (payload) => ({
    success: true,
    message: 'Echo completed.',
    data: payload,
  }),
});

agent.action({
  name: 'runHealthCheck',
  label: 'Run Health Check',
  description: 'Runs the registered health provider immediately.',
  dangerLevel: 'LOW',
  handler: async () => {
    const health = await agent.runHealth();
    return {
      success: true,
      message: 'Health check completed.',
      data: health,
    };
  },
});

await agent.start();
```

This example should be the baseline for the CE（社区版） demo service.

---

## 7. Service Identity

Node.js Capsule Service（胶囊服务） identity should be stable.

Recommended fields:

```text
code
name
description
version
runtime
metadata
```

Example:

```ts
service: {
  code: 'demo-node-capsule-service',
  name: 'Demo Node Capsule Service',
  description: 'A demo Node.js Capsule Service for Opstage CE.',
  version: '0.1.0',
  runtime: 'nodejs',
}
```

Rules:

- `code` must be stable across restarts;
- `code` should not contain secrets;
- `name` is human-readable;
- `runtime` should be `nodejs`;
- `version` should reflect the Capsule Service（胶囊服务） version;
- metadata should be optional and sanitized.

---

## 8. Runtime 配置

Node.js runtime should support configuration from code and environment variables.

Recommended environment variables:

```text
OPSTAGE_BACKEND_URL=http://localhost:8080
OPSTAGE_REGISTRATION_TOKEN=opstage_reg_xxx
OPSTAGE_AGENT_TOKEN_FILE=./data/agent-token.json
OPSTAGE_AGENT_CODE=local-node-agent
OPSTAGE_AGENT_NAME=Local Node Agent
OPSTAGE_HEARTBEAT_INTERVAL_SECONDS=30
OPSTAGE_COMMAND_POLL_INTERVAL_SECONDS=5
OPSTAGE_LOG_LEVEL=info
DEMO_MESSAGE=hello capsule
```

Recommended precedence:

```text
explicit code options > environment variables > SDK defaults
```

Registration token and Agent（代理） token must not be printed in logs.

---

## 9. Agent（代理） Token Store

Node.js runtime should use a file-based token store in CE（社区版） v0.1.

Recommended local path:

```text
./data/agent-token.json
```

Docker path may be:

```text
/app/data/agent-token.json
```

Rules:

- token file should be persisted across service restarts;
- token file should not be committed to source control;
- token directory should be mounted as Docker volume if needed;
- corrupted token file should be handled safely;
- deleting token file allows re-registration when registration token is available.

Recommended `.gitignore` entry:

```text
data/agent-token.json
*.agent-token.json
```

---

## 10. Health Provider

Node.js runtime should expose service health through SDK health provider.

Recommended API:

```ts
agent.health(async () => ({
  status: 'UP',
  message: 'Service is healthy.',
  dependencies: [
    {
      name: 'database',
      type: 'database',
      status: 'UP',
      message: 'Database is reachable.',
    },
  ],
}));
```

Recommended status values:

```text
UP
DOWN
DEGRADED
UNKNOWN
```

Rules:

- health provider should be lightweight;
- provider errors should not crash the service;
- provider errors should produce `UNKNOWN` or safe failure;
- health output must not contain raw secrets;
- dependency health is optional in CE（社区版）.

---

## 11. Config Provider

Node.js runtime should expose config metadata through SDK config provider.

Recommended API:

```ts
agent.configs(() => [
  {
    key: 'demo.message',
    label: 'Demo Message',
    type: 'string',
    currentValue: process.env.DEMO_MESSAGE ?? 'hello capsule',
    defaultValue: 'hello capsule',
    editable: true,
    sensitive: false,
    source: 'env',
  },
  {
    key: 'demo.accountSecret',
    label: 'Demo Account Secret',
    type: 'secretRef',
    currentValue: 'agent-local://local-node-agent/secrets/demo/account',
    editable: false,
    sensitive: true,
    source: 'local-secret-store',
  },
]);
```

Rules:

- config provider reports metadata, not a full config-center model;
- CE（社区版） 支持 visibility only;
- sensitive values must be masked or represented as `secretRef`;
- raw passwords, tokens, cookies, and API keys must not be reported;
- config editing and publishing are future EE（企业版） capabilities.

---

## 12. Action Registration

Node.js runtime should expose predefined actions through SDK action registry.

Recommended API:

```ts
agent.action({
  name: 'echo',
  label: 'Echo',
  description: 'Returns the submitted payload.',
  dangerLevel: 'LOW',
  inputSchema: {
    type: 'object',
    properties: {
      message: { type: 'string' },
    },
  },
  handler: async (payload) => ({
    success: true,
    message: 'Echo completed.',
    data: payload,
  }),
});
```

Rules:

- actions must be predefined in code;
- action names must be unique per service;
- unknown actions fail safely;
- action handlers must return serializable output;
- handler exceptions must be captured;
- no built-in arbitrary shell action;
- high-risk actions must declare appropriate danger level.

---

## 13. Demo Actions

The CE（社区版） Node.js demo service should include at least two safe actions.

### 13.1 echo

Purpose:

```text
Return the submitted payload.
```

Danger level:

```text
LOW
```

### 13.2 runHealthCheck

Purpose:

```text
Run the registered health provider immediately and return the result.
```

Danger level:

```text
LOW
```

These actions prove the full Command and CommandResult loop without introducing unsafe operations.

---

## 14. Command Execution

Node.js runtime uses SDK command polling.

Flow:

```text
SDK polls Backend for Commands
    ↓
Backend returns Commands assigned to this Agent
    ↓
SDK validates command type and action name
    ↓
SDK executes local action handler
    ↓
SDK captures success or failure
    ↓
SDK reports CommandResult
```

CE（社区版） v0.1 支持 only:

```text
CommandType = ACTION
```

The runtime must not expose arbitrary command execution.

---

## 15. CommandResult Reporting

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

- successful action returns `SUCCESS`;
- failed action returns `FAILED`;
- handler exception returns `FAILED`;
- result should be concise;
- result must not include raw secrets;
- large logs should not be returned in CommandResult;
- errors should be sanitized where practical.

---

## 16. Sensitive Data Rules

Node.js runtime must avoid leaking sensitive data.

Sensitive examples:

```text
password
token
accessToken
refreshToken
cookie
apiKey
privateKey
credential
secret
authorization
registrationToken
agentToken
```

Rules:

- do not log registration token;
- do not log Agent（代理） token;
- do not report raw secrets in configs;
- do not return raw secrets in CommandResult;
- do not include raw secrets in health details;
- use `secretRef` for sensitive references;
- sanitize logs and errors where practical.

---

## 17. Backend Downtime Behavior

Node.js runtime should tolerate Opstage（运维舞台） Backend downtime.

If Backend is unavailable, SDK should:

- keep the business service running;
- retry heartbeat/reporting/polling with backoff;
- avoid log spam;
- re-report manifest after reconnect if needed;
- resume command polling after recovery.

Governance outage should not automatically become business outage.

---

## 18. Startup Behavior

Recommended startup behavior:

```text
Node service starts
    ↓
CapsuleAgent is created
    ↓
providers/actions are registered
    ↓
agent.start() is called
    ↓
SDK loads Agent token or registers
    ↓
SDK reports manifest
    ↓
SDK starts heartbeat loop
    ↓
SDK starts command polling loop
```

If no Agent（代理） token and no registration token are available:

- SDK logs sanitized error;
- SDK does not start governance loops;
- business service continues by default unless strict mode is enabled.

---

## 19. Shutdown Behavior

Node.js runtime should stop Agent（代理） loops cleanly.

Recommended behavior:

- call `await agent.stop()` if application has shutdown hooks;
- stop heartbeat loop;
- stop command polling loop;
- avoid starting new command execution;
- allow in-flight command to finish if practical;
- do not block shutdown indefinitely.

CE（社区版） does not require deregistration on shutdown.

Backend infers offline state from heartbeat timeout.

---

## 20. Docker Runtime

Node.js Capsule Service（胶囊服务） should be easy to run in Docker.

Recommended Docker environment:

```text
OPSTAGE_BACKEND_URL=http://opstage:8080
OPSTAGE_REGISTRATION_TOKEN=opstage_reg_xxx
OPSTAGE_AGENT_TOKEN_FILE=/app/data/agent-token.json
DEMO_MESSAGE=hello capsule
```

Recommended volume:

```text
/app/data
```

so the Agent（代理） token survives container restart.

The demo Dockerfile should not bake registration token into the image.

Registration token should be passed at runtime.

---

## 21. Docker Compose Demo

A CE（社区版） Docker Compose demo may include:

```text
opstage
node-demo-capsule-service
```

Optional services may include:

```text
sqlite volume
network
```

The demo should show:

1. start Opstage（运维舞台）;
2. create registration token;
3. start Node demo service with token;
4. Agent（代理） appears in UI;
5. Capsule Service（胶囊服务） appears in UI;
6. health is visible;
7. configs are visible;
8. actions are visible;
9. `echo` action can run;
10. CommandResult appears;
11. AuditEvent appears.

---

## 22. Local 开发 Workflow

Recommended local workflow:

```text
1. Start Opstage Backend/UI locally.
2. Create registration token from UI.
3. Export OPSTAGE_BACKEND_URL.
4. Export OPSTAGE_REGISTRATION_TOKEN.
5. Start Node demo Capsule Service.
6. Verify Agent and service in UI.
7. Run echo action.
8. Inspect CommandResult and AuditEvent.
```

The developer should not need to manually edit database records.

---

## 23. 测试 Requirements

Node.js runtime tests should verify:

- demo service starts;
- SDK options load correctly;
- environment variables work;
- token store persists token;
- health provider returns status;
- config provider returns metadata;
- action registry exposes actions;
- command execution invokes correct handler;
- action failure returns failed result;
- Backend downtime does not crash service;
- sensitive data is not logged or reported;
- Docker demo can start with runtime env variables.

Runtime tests may reuse Node Agent（代理） SDK tests where appropriate.

---

## 24. 文档 Requirements

Node.js runtime documentation should include:

- installation command;
- minimal integration example;
- environment variable reference;
- token store explanation;
- health provider example;
- config provider example;
- action registration example;
- Docker example;
- troubleshooting section;
- security notes.

This document can serve as the source for implementation and user-facing quick start docs.

---

## 25. Troubleshooting Notes

Common issues:

### 25.1 Agent（代理） does not register

Check:

- `OPSTAGE_BACKEND_URL`;
- `OPSTAGE_REGISTRATION_TOKEN`;
- token expiration;
- network connectivity;
- Backend logs.

### 25.2 Agent（代理） token invalid

Possible fixes:

- delete local token file;
- create a new registration token;
- restart service;
- check if Agent（代理） was revoked.

### 25.3 Service does not appear

Check:

- Agent（代理） registration status;
- manifest report errors;
- service code configuration;
- Backend Agent（代理） API logs.

### 25.4 Action does not run

Check:

- action name;
- action enabled state;
- Command status;
- Agent（代理） polling logs;
- handler error logs;
- CommandResult detail.

---

## 26. Future EE（企业版） Direction

Future EE（企业版） may extend Node.js runtime with:

- Agent（代理） token rotation;
- stronger diagnostics;
- capability reporting;
- secret provider resolver hooks;
- command progress events;
- long-running action support;
- config apply/reload helpers;
- action-level permission metadata;
- sidecar/external Agent（代理） interoperability.

These are not CE（社区版） v0.1 requirements.

---

## 27. Future Cloud（云版） Direction

Future Cloud（云版） may extend Node.js runtime with:

- Cloud（云版） Agent（代理） Gateway URL;
- workspace-scoped enrollment;
- rate-limit handling;
- Cloud（云版） connection diagnostics;
- WebSocket or streaming delivery;
- managed alert hints;
- usage metering metadata.

These are not CE（社区版） v0.1 requirements.

---

## 28. Anti-Patterns

Avoid these patterns.

### 28.1 Service depends on Opstage（运维舞台） to start business logic

By default, business runtime should continue even if governance is unavailable.

### 28.2 Raw tokens in logs

Registration token and Agent（代理） token must never be logged.

### 28.3 Config provider reports secrets

Use `secretRef` or masked values.

### 28.4 Action registry exposes shell execution

Remote shell is not the CE（社区版） operation model.

### 28.5 Demo service is too complex

The demo should prove the governance loop, not become a business application.

### 28.6 Node runtime tries to solve every future runtime problem

Keep Node runtime focused and let future runtimes extend the shared model.

---

## 29. Acceptance Criteria

Node.js Runtime implementation is acceptable when:

- Node.js demo Capsule Service（胶囊服务） can import `@xtrape/capsule-agent-node`;
- service identity is declared;
- Agent（代理） can register with registration token;
- Agent（代理） token is stored and reused;
- heartbeat works;
- manifest report works;
- health provider works;
- config provider works;
- actions are reported;
- `echo` action works;
- `runHealthCheck` action works;
- CommandResult is reported;
- Opstage（运维舞台） UI shows Agent（代理）, service, health, configs, actions, Commands, and AuditEvents;
- Backend downtime does not crash demo service by default;
- raw tokens are not logged;
- raw secrets are not reported;
- Docker demo can run with runtime environment variables.

---

## 30. Summary

Node.js Runtime is the CE（社区版） reference runtime for Capsule Services.

It should prove that a lightweight Node.js service can become visible, healthy, configurable by metadata, operable through predefined actions, and auditable through Opstage（运维舞台）.

The most important Node Runtime rule is:

> Keep Node.js runtime integration simple, explicit, safe, and sufficient to prove the complete Capsule governance loop before adding more runtimes.
