# Embedded Agent

- Status: Draft
- Edition: Shared
- Priority: High

本文件属于 `xtrape-capsule` 文档集。`xtrape-capsule` 是面向轻服务 / Capsule Service 的领域体系；`xtrape-capsule-opstage` 是该体系下的统一运行态治理平台。

当前实现重点是 CE 开源社区版。EE 私有化商业版与 Cloud SaaS 版属于未来规划，CE 需要保留扩展点，但不应在早期版本实现其完整能力。

Agent 是 Capsule Service 加入 Opstage 治理体系的授权入口。CE 第一版实现 Node.js Embedded Agent，Sidecar 和 External Agent 属于后续扩展。

# Embedded Agent

- Status: Implementation Guidance
- Edition: Shared
- Priority: High
- Audience: agent SDK developers, Capsule Service developers, backend developers, architects, security reviewers, AI coding agents

This document defines the **Embedded Agent** model for the `xtrape-capsule` product family.

An Embedded Agent runs inside the same process as a Capsule Service. It is the first Agent mode implemented by CE.

The current implementation focus is **CE**. CE v0.1 implements only the **Node.js Embedded Agent SDK**. Java, Python, Go, Sidecar Agent, External Agent, Host Agent, and Kubernetes Agent are future EE/Cloud extension tracks and must not expand the CE v0.1 implementation scope.

---

## 1. Purpose

The purpose of an Embedded Agent is to make a Capsule Service governable by Opstage without requiring a separate Agent process.

The Embedded Agent allows a Capsule Service to:

- register itself with Opstage through an Agent identity;
- authenticate to Opstage Backend;
- send heartbeat;
- report service manifest;
- report health;
- report config metadata;
- report predefined action definitions;
- poll Commands;
- execute local predefined action handlers;
- report CommandResults;
- keep governance communication separate from business logic where practical.

The Embedded Agent is the simplest Agent mode and the best fit for CE v0.1.

---

## 2. Positioning

An Embedded Agent is:

> An in-process governance bridge between a Capsule Service and Opstage Backend.

It is not:

- a separate sidecar process;
- a host-level supervisor;
- a Kubernetes controller;
- a remote shell;
- a secret vault;
- a full observability collector;
- a deployment orchestrator;
- the owner of the service's business logic.

The Capsule Service remains the business runtime. The Embedded Agent only exposes governance metadata and safe predefined operations.

---

## 3. CE Scope

CE v0.1 should implement one Embedded Agent SDK:

```text
Node.js Embedded Agent SDK
```

Required capabilities:

- initialize from code and environment variables;
- load stored Agent token;
- register with registration token when needed;
- store issued Agent token locally;
- send heartbeat;
- report service manifest;
- register health provider;
- register config provider;
- register action handlers;
- poll Commands from Backend;
- execute predefined action handlers;
- report CommandResults;
- handle Backend downtime gracefully;
- avoid logging tokens;
- avoid reporting raw secrets.

---

## 4. CE Non-Goals

CE v0.1 Embedded Agent should not implement:

- Java Embedded Agent SDK;
- Python Embedded Agent SDK;
- Go Embedded Agent SDK;
- sidecar Agent;
- external Agent;
- host Agent;
- Kubernetes Agent;
- WebSocket command channel;
- gRPC streaming;
- Agent Gateway protocol;
- automatic service discovery;
- config publishing workflow;
- enterprise secret provider integration;
- arbitrary shell execution;
- remote terminal;
- Agent auto-upgrade.

These may be future EE or Cloud capabilities.

---

## 5. Runtime Model

The Embedded Agent runs inside the Capsule Service process.

Recommended structure:

```text
Node.js Capsule Service Process
├── Business API / workers / handlers
├── Local configuration and runtime state
└── Opstage Embedded Agent SDK
    ├── Registration client
    ├── Agent token store
    ├── Heartbeat loop
    ├── Manifest reporter
    ├── Health provider wrapper
    ├── Config provider wrapper
    ├── Action registry
    ├── Command polling loop
    └── CommandResult reporter
```

The Embedded Agent should be lightweight and should not require a separate runtime service.

---

## 6. Process Isolation Principle

Because the Embedded Agent runs in-process, it must avoid destabilizing the Capsule Service.

Rules:

- Agent startup failure should not crash the business service by default;
- Backend outage should not crash the business service;
- provider exceptions should be captured;
- action handler exceptions should be reported as failed CommandResults;
- polling loop errors should be logged and retried;
- no unbounded retry loops without backoff;
- Agent should provide optional strict mode if a service wants governance to be mandatory.

Default CE behavior should favor business runtime continuity.

---

## 7. Developer Experience Target

A Capsule Service developer should integrate the Embedded Agent with a small amount of code.

Target API shape:

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
  description: 'Returns the submitted payload.',
  dangerLevel: 'LOW',
  handler: async (payload) => ({
    success: true,
    message: 'Echo completed.',
    data: payload,
  }),
});

await agent.start();
```

The final API may evolve during implementation, but the SDK should preserve this level of simplicity.

---

## 8. Configuration

The Embedded Agent should support configuration from code and environment variables.

Recommended code options:

```text
backendUrl
registrationToken
agentCode
agentName
tokenStore
service
heartbeatIntervalSeconds
commandPollIntervalSeconds
logLevel
strictMode
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
OPSTAGE_LOG_LEVEL=info
```

Environment variables should be optional when equivalent code configuration is provided.

---

## 9. Service Identity

The Embedded Agent reports one Capsule Service identity in CE v0.1.

Recommended service identity fields:

```text
code
name
description
version
runtime
agentMode
metadata
```

Example:

```json
{
  "code": "demo-capsule-service",
  "name": "Demo Capsule Service",
  "description": "A demo service for Opstage CE.",
  "version": "0.1.0",
  "runtime": "nodejs",
  "agentMode": "embedded"
}
```

The `code` should be stable across restarts.

---

## 10. Agent Lifecycle

Recommended lifecycle:

```text
Capsule Service starts
    ↓
Embedded Agent is constructed
    ↓
Health/config/action providers are registered
    ↓
agent.start() is called
    ↓
Agent loads stored Agent token
    ↓
If no valid token exists, Agent registers with registration token
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

The lifecycle should be explicit and predictable.

---

## 11. Startup Behavior

During startup, the Embedded Agent should:

1. validate local configuration;
2. load stored Agent token if available;
3. register if no valid token exists;
4. report service manifest;
5. start periodic heartbeat;
6. start periodic command polling.

If Backend is unavailable:

- log a warning;
- retry later with backoff;
- do not crash the Capsule Service by default.

If registration token is missing and no stored Agent token exists:

- log a clear error;
- do not start governance loops;
- keep business service running by default.

---

## 12. Shutdown Behavior

On process shutdown, the Embedded Agent should:

- stop heartbeat loop;
- stop command polling loop;
- allow in-flight CommandResult reporting to finish if practical;
- not block shutdown indefinitely;
- log shutdown summary if useful.

CE v0.1 does not need a formal Agent deregistration call.

Backend should infer offline state from heartbeat timeout.

---

## 13. Registration Flow

Registration flow:

```text
Agent has no stored Agent token
    ↓
Agent reads registration token
    ↓
Agent calls POST /api/agents/register
    ↓
Backend validates registration token
    ↓
Backend creates or returns Agent identity
    ↓
Backend issues Agent token
    ↓
Agent stores Agent token locally
```

Registration request should include:

```text
agentCode
agentName
agentMode
runtime
version
service identity
metadata
```

Registration response should include:

```text
agentId
agentToken
workspaceId
configuration hints if any
```

Raw Agent token should only be returned once.

---

## 14. Token Store

The Embedded Agent needs a local token store.

CE v0.1 recommended token store:

```text
file-based token store
```

Example path:

```text
./data/agent-token.json
```

Token store rules:

- create parent directory if needed;
- restrict file permissions where practical;
- never log raw token;
- handle corrupted token file safely;
- allow token deletion for re-registration;
- support environment override for token file path.

Future EE may support OS keychain, Kubernetes Secret, Vault reference, or managed token stores.

---

## 15. Agent Token Usage

After registration, the Embedded Agent uses Agent token for Agent API calls.

Header:

```http
Authorization: Bearer <agentToken>
```

Agent token rules:

- never log the token;
- never include it in CommandResult;
- never include it in health or manifest;
- clear or invalidate local token if Backend returns a definitive revoked/invalid response;
- do not repeatedly spam Backend with invalid token requests.

---

## 16. Manifest Report

The Embedded Agent reports a manifest describing the Capsule Service.

Manifest should include:

```text
service identity
agentMode
runtime
version
capabilities
resources
health support
config metadata
action definitions
metadata
```

Recommended report time:

- after successful registration or token validation;
- after startup;
- after action/config metadata changes if dynamic update is supported;
- periodically only if needed.

CE v0.1 can report manifest at startup and after reconnect.

---

## 17. Health Provider

The SDK should allow one health provider to be registered.

Example:

```ts
agent.health(async () => ({
  status: 'UP',
  message: 'Service is healthy.',
  dependencies: [
    {
      name: 'database',
      type: 'database',
      status: 'UP',
      message: 'SQLite is reachable.',
    },
  ],
}));
```

Health status values:

```text
UP
DOWN
DEGRADED
UNKNOWN
```

Rules:

- provider exceptions must be caught;
- health should not include raw secrets;
- health should be lightweight;
- health should not perform destructive operations;
- `UNKNOWN` is acceptable when provider fails.

---

## 18. Config Provider

The SDK should allow a config provider to expose config metadata.

Example:

```ts
agent.configs(() => [
  {
    key: 'demo.message',
    label: 'Demo Message',
    type: 'string',
    defaultValue: 'hello capsule',
    currentValue: 'hello capsule',
    editable: true,
    sensitive: false,
    source: 'env',
  },
  {
    key: 'demo.accountSecret',
    label: 'Demo Account Secret',
    type: 'secretRef',
    currentValue: 'agent-local://local-dev-agent/secrets/demo/account',
    editable: false,
    sensitive: true,
    source: 'local-secret-store',
  },
]);
```

Rules:

- report metadata, not raw secrets;
- mark sensitive items with `sensitive: true`;
- use `secretRef` for secret references;
- CE supports visibility only;
- config editing is future EE work.

---

## 19. Action Registry

The SDK should allow action handlers to be registered.

Example:

```ts
agent.action({
  name: 'runHealthCheck',
  label: 'Run Health Check',
  description: 'Runs the health provider immediately.',
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
```

Action rules:

- action name must be unique per service;
- action handler must be explicit;
- action handler must return serializable output;
- unknown action must fail safely;
- no built-in arbitrary shell action;
- high-risk actions should declare `HIGH` or `CRITICAL` danger level.

---

## 20. Command Polling

CE command delivery uses polling.

Recommended loop:

```text
wait commandPollIntervalSeconds
    ↓
GET /api/agents/{agentId}/commands
    ↓
for each Command:
    validate Command
    execute handler
    report CommandResult
```

Rules:

- poll only after Agent token is available;
- use backoff after Backend errors;
- avoid concurrent execution unless explicitly configured;
- skip or fail expired Commands;
- report unknown actions as failed;
- do not poll too aggressively by default.

Recommended CE default:

```text
5 seconds to 15 seconds
```

---

## 21. Command Execution

For each `ACTION` Command, the Embedded Agent should:

1. verify command type is `ACTION`;
2. verify target service matches this embedded service;
3. verify action handler exists;
4. verify action is enabled;
5. execute handler with payload and context;
6. catch errors;
7. produce CommandResult;
8. report CommandResult to Backend.

Execution context may include:

```text
commandId
actionName
payload
createdAt
metadata
```

CE v0.1 should execute one Command at a time unless concurrency is explicitly designed.

---

## 22. CommandResult Reporting

CommandResult should be reported after execution.

Endpoint:

```http
POST /api/agents/{agentId}/commands/{commandId}/result
```

Result should include:

```text
status
outputText
errorMessage
resultJson
startedAt
finishedAt
```

Rules:

- result should be concise;
- raw secrets must not be included;
- large logs should not be included;
- error messages should be sanitized where practical;
- reporting failure should be retried carefully;
- duplicate result reporting should be handled safely by Backend.

---

## 23. Retry and Backoff

The Embedded Agent should retry transient failures.

Recommended retry areas:

- registration;
- heartbeat;
- manifest report;
- command polling;
- CommandResult reporting.

Recommended backoff behavior:

```text
initial delay: 1-5 seconds
max delay: 60-300 seconds
jitter: recommended
```

CE implementation may use a simpler backoff but should avoid tight failure loops.

---

## 24. Offline Behavior

If Opstage Backend is offline, the Embedded Agent should:

- keep business service running;
- continue retrying in background;
- avoid log spam;
- re-report manifest after reconnect if needed;
- resume heartbeat and command polling;
- avoid duplicate execution of Commands where practical.

Governance unavailability should not automatically equal business service failure.

---

## 25. Error Handling

### 25.1 Registration error

If registration fails:

- log sanitized error;
- retry if failure is transient;
- stop retrying aggressively if registration token is invalid;
- keep service running by default.

### 25.2 Heartbeat error

If heartbeat fails:

- log warning;
- retry later;
- keep service running.

### 25.3 Manifest report error

If manifest report fails:

- log warning;
- retry after reconnect;
- keep service running.

### 25.4 Action handler error

If action handler throws:

- catch error;
- mark CommandResult as `FAILED`;
- sanitize error message;
- continue processing future Commands.

### 25.5 Token invalid or revoked

If Backend reports token invalid or revoked:

- stop using token;
- clear local token if safe;
- try re-registration only if registration token is available;
- avoid repeated noisy invalid token requests.

---

## 26. Logging Rules

Embedded Agent logs should include:

- registration started/succeeded/failed;
- heartbeat failed;
- manifest report failed;
- command polling failed;
- action execution failed;
- CommandResult report failed;
- token invalid/revoked state.

Embedded Agent logs must not include:

```text
registration token
Agent token
password
cookie
OAuth token
API key
private key
raw secret
```

---

## 27. Sensitive Data Rules

The Embedded Agent must not send raw secrets by default.

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
```

Use:

```text
secretRef
```

for sensitive references.

When returning CommandResult, sanitize error details and result JSON where practical.

---

## 28. Built-In Demo Actions

The CE demo service should include safe demo actions.

### 28.1 echo

Purpose:

```text
Return the submitted payload.
```

Danger level:

```text
LOW
```

### 28.2 runHealthCheck

Purpose:

```text
Run the registered health provider and return the health result.
```

Danger level:

```text
LOW
```

These actions prove the governance loop without introducing unsafe operations.

---

## 29. Built-In Action Restrictions

The Embedded Agent SDK must not include built-in unsafe actions such as:

```text
runShell
exec
bash
sh
runScript
customCommand
```

If a service developer registers a high-risk action manually, it must be explicit and visible through `dangerLevel`.

CE should not encourage remote shell-style usage.

---

## 30. Testing Requirements

Embedded Agent SDK should be tested for:

- configuration loading;
- token store read/write;
- registration success;
- registration failure;
- heartbeat success;
- heartbeat failure;
- manifest construction;
- health provider success/failure;
- config provider output;
- action registration;
- command polling;
- action execution success;
- action execution failure;
- CommandResult reporting;
- backend unavailable behavior;
- token invalid behavior;
- sensitive data masking where implemented.

---

## 31. Future Extension Points

The Embedded Agent should reserve clean extension points:

```text
agentVersion
protocolVersion
capabilities
agentMode
runtime
metadata
secretRef
commandType
```

These fields support future EE and Cloud evolution.

Do not implement future systems in CE just because fields exist.

---

## 32. Future EE Direction

Future EE may add:

- Java Embedded Agent SDK;
- Python Embedded Agent SDK;
- Go SDK;
- Agent token rotation;
- Agent diagnostics;
- capability reporting;
- secret provider integration;
- command progress events;
- long-running action support;
- action-level RBAC;
- sidecar/external Agent alternatives.

These are not CE v0.1 requirements.

---

## 33. Future Cloud Direction

Future Cloud may add:

- Cloud Agent Gateway;
- hosted enrollment UX;
- multi-tenant workspace-scoped registration;
- Agent traffic rate limiting;
- WebSocket or streaming delivery;
- connection diagnostics;
- usage metering by Agent;
- managed alerts on Agent state.

These are not CE v0.1 requirements.

---

## 34. Acceptance Criteria

The CE Embedded Agent is acceptable when:

- SDK can be installed in a Node.js demo Capsule Service;
- SDK can register with Backend using registration token;
- SDK stores issued Agent token locally;
- SDK reuses stored Agent token after restart;
- SDK sends heartbeat periodically;
- SDK reports service manifest;
- SDK reports health;
- SDK reports config metadata;
- SDK reports action definitions;
- SDK polls Commands;
- SDK executes `echo` action;
- SDK executes `runHealthCheck` action;
- SDK reports CommandResult;
- SDK handles Backend downtime without crashing the service;
- SDK handles invalid token safely;
- raw tokens are not logged;
- raw secrets are not reported;
- no arbitrary shell action is built in.

---

## 35. Summary

The Embedded Agent is the first and simplest Agent mode for Opstage CE.

It should provide a lightweight in-process SDK that makes a Node.js Capsule Service visible, healthy, configurable by metadata, operable through predefined actions, and auditable through Commands and CommandResults.

The most important Embedded Agent rule is:

> Keep the Embedded Agent small, safe, in-process, outbound-first, and limited to explicit governance capabilities rather than unrestricted runtime control.