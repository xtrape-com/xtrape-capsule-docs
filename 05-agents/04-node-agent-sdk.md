# Node Agent SDK

- Status: Implementation Target
- Edition: CE
- Priority: High
- Audience: agent SDK developers, Capsule Service developers, backend developers, test engineers, AI coding agents

This document defines the **Node.js Agent SDK** for Opstage CE.

The Node.js Agent SDK is the first and reference implementation of the Embedded Agent model. It allows a Node.js Capsule Service to register with Opstage Backend, report its runtime metadata, expose health/config/action metadata, poll Commands, execute predefined actions, and report CommandResults.

The current implementation focus is **CE v0.1**. Sidecar Agent, External Agent, Java SDK, Python SDK, Go SDK, Agent Gateway, WebSocket delivery, and enterprise secret integrations are future EE/Cloud capabilities and must not be implemented as part of this SDK v0.1.

---

## 1. Purpose

The purpose of the Node.js Agent SDK is to provide a lightweight integration library for Node.js Capsule Services.

The SDK should make it easy to:

- configure Opstage Backend connection;
- register with a registration token;
- store and reuse Agent token;
- send heartbeat;
- report service manifest;
- report health;
- report config metadata;
- report predefined actions;
- poll Commands;
- dispatch Commands to local action handlers;
- report CommandResults;
- handle Backend downtime safely;
- avoid token and secret leakage.

The SDK is the main developer-facing integration point for CE Capsule Services.

---

## 2. Scope

The SDK v0.1 should implement:

```text
Node.js Embedded Agent
HTTP Agent API client
file-based Agent token store
heartbeat loop
manifest report
health provider
config provider
action registry
command polling loop
CommandResult reporting
basic retry/backoff
safe logging
```

The SDK v0.1 should not implement:

```text
Sidecar Agent
External Agent
multi-target management
Java/Python/Go SDKs
WebSocket/gRPC command delivery
Agent Gateway protocol
config publishing
secret provider integration
remote shell
arbitrary script execution
Agent auto-upgrade
full observability collector
```

---

## 3. Package Name

Recommended npm package name:

```text
@xtrape/capsule-agent-node
```

Alternative names if needed:

```text
@xtrape/opstage-agent-node
@xtrape/capsule-node-agent
```

Current recommendation:

```text
@xtrape/capsule-agent-node
```

because the SDK belongs to the `xtrape-capsule` domain and implements the Node.js Agent capability.

---

## 4. Runtime Requirements

Recommended runtime:

```text
Node.js 20 LTS or later
TypeScript-first
ESM-first if repository standard allows it
```

The SDK should support:

- TypeScript projects;
- JavaScript projects;
- Common Node.js service runtimes;
- HTTP-based Backend connection;
- Dockerized Capsule Services.

The SDK should avoid heavy dependencies in v0.1.

---

## 5. Public API Overview

The SDK should expose a small public API.

Recommended exports:

```ts
export class CapsuleAgent {}
export type CapsuleAgentOptions = unknown;
export type HealthReportInput = unknown;
export type ConfigItemInput = unknown;
export type ActionDefinitionInput = unknown;
export type ActionHandler = unknown;
export type ActionResult = unknown;
export type TokenStore = unknown;
```

The final type names may be adjusted during implementation, but the public API should stay small and stable.

---

## 6. Minimal Usage Example

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
    description: 'A demo Capsule Service for Opstage CE.',
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
    currentValue: 'hello capsule',
    defaultValue: 'hello capsule',
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

This example should be used as the reference for the CE demo Capsule Service.

---

## 7. CapsuleAgentOptions

Recommended options:

```ts
type CapsuleAgentOptions = {
  backendUrl: string;
  registrationToken?: string;
  tokenStore?: TokenStoreOptions;
  agent?: {
    code?: string;
    name?: string;
    version?: string;
  };
  service: {
    code: string;
    name: string;
    description?: string;
    version?: string;
    runtime?: string;
    metadata?: Record<string, unknown>;
  };
  heartbeatIntervalSeconds?: number;
  commandPollIntervalSeconds?: number;
  startupReport?: boolean;
  strictMode?: boolean;
  logger?: AgentLogger;
};
```

Defaults:

```text
service.runtime = nodejs
agent.version = SDK package version
heartbeatIntervalSeconds = 30
commandPollIntervalSeconds = 5
startupReport = true
strictMode = false
```

---

## 8. Environment Variables

The SDK should support environment-variable-based configuration for common cases.

Recommended variables:

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

Environment variables should not override explicit code options unless documented clearly.

Recommended precedence:

```text
explicit code options > environment variables > SDK defaults
```

---

## 9. Token Store

The SDK v0.1 should implement a file-based token store.

Recommended option:

```ts
tokenStore: {
  file: './data/agent-token.json'
}
```

Token file may contain:

```json
{
  "agentId": "agt_001",
  "agentToken": "opstage_agent_xxx",
  "backendUrl": "http://localhost:8080",
  "createdAt": "2026-04-30T12:00:00Z"
}
```

Rules:

- create parent directory if needed;
- restrict file permissions where practical;
- never log raw Agent token;
- handle missing file safely;
- handle corrupted file safely;
- allow re-registration after token file deletion;
- do not commit token file to source control.

The demo service should include `.gitignore` rules for local token files.

---

## 10. Agent Registration

The SDK should register when no valid stored Agent token exists.

Registration flow:

```text
load token store
    ↓
if token exists, try authenticated call or proceed
    ↓
if no token, read registration token
    ↓
POST /api/agents/register
    ↓
receive agentId and Agent token
    ↓
store token locally
```

Registration request should include:

```json
{
  "agent": {
    "code": "local-dev-agent",
    "name": "Local Development Agent",
    "mode": "embedded",
    "runtime": "nodejs",
    "version": "0.1.0"
  },
  "service": {
    "code": "demo-capsule-service",
    "name": "Demo Capsule Service",
    "version": "0.1.0",
    "runtime": "nodejs"
  }
}
```

Exact API payload must match the Backend API spec when finalized.

---

## 11. Registration Token Handling

Registration token rules:

- use only for enrollment;
- do not store it after successful registration unless provided by application environment;
- do not log it;
- do not include it in health, manifest, config, action, or CommandResult payloads;
- stop noisy retries if Backend reports token invalid;
- allow retry if Backend is temporarily unavailable.

If no stored Agent token and no registration token exists, SDK should:

- log a clear sanitized error;
- not start heartbeat or command polling;
- keep service running by default unless `strictMode = true`.

---

## 12. Agent Token Handling

Agent token rules:

- use `Authorization: Bearer <agentToken>` for Agent API calls;
- never log raw token;
- never expose token through SDK health/config/action outputs;
- clear local token only on definitive invalid/revoked response;
- avoid repeated invalid-token request loops;
- support manual recovery by deleting token file and providing registration token.

Token rotation is future EE work and not required in SDK v0.1.

---

## 13. Lifecycle Methods

Recommended public methods:

```ts
class CapsuleAgent {
  constructor(options: CapsuleAgentOptions);

  health(provider: HealthProvider): void;
  configs(provider: ConfigProvider): void;
  action(definition: ActionRegistration): void;

  start(): Promise<void>;
  stop(): Promise<void>;

  reportManifest(): Promise<void>;
  runHealth(): Promise<HealthReportInput>;
}
```

Optional internal methods should not become public API unless necessary.

---

## 14. start()

`start()` should:

1. validate configuration;
2. load or register Agent token;
3. report manifest if `startupReport = true`;
4. start heartbeat loop;
5. start command polling loop;
6. return after startup tasks are initialized.

`start()` should not block forever.

If Backend is unavailable:

- with `strictMode = false`, log warning and retry in background;
- with `strictMode = true`, throw startup error.

---

## 15. stop()

`stop()` should:

- stop heartbeat timer;
- stop command polling timer;
- prevent new command execution;
- allow current command execution to finish if practical;
- flush pending CommandResult if practical;
- not block indefinitely.

CE v0.1 does not require Backend deregistration on stop.

Backend should infer offline state from heartbeat timeout.

---

## 16. Manifest Construction

SDK should construct a service manifest from:

- service options;
- registered health provider availability;
- config provider output;
- action registry;
- metadata;
- SDK version;
- runtime information.

Manifest should include:

```text
service identity
agentMode = embedded
runtime = nodejs
version
configs
actions
capabilities
metadata
```

Manifest must not include raw tokens or secrets.

---

## 17. Health Provider API

Recommended type shape:

```ts
type HealthProvider = () => Promise<HealthReportInput> | HealthReportInput;

type HealthReportInput = {
  status: 'UP' | 'DOWN' | 'DEGRADED' | 'UNKNOWN';
  message?: string;
  dependencies?: Array<{
    name: string;
    type?: string;
    status: 'UP' | 'DOWN' | 'DEGRADED' | 'UNKNOWN';
    message?: string;
  }>;
  details?: Record<string, unknown>;
};
```

Rules:

- catch provider exceptions;
- convert provider exception to `UNKNOWN` or failed health report;
- sanitize health details where practical;
- do not include raw secrets;
- keep health provider lightweight.

---

## 18. Config Provider API

Recommended type shape:

```ts
type ConfigProvider = () => Promise<ConfigItemInput[]> | ConfigItemInput[];

type ConfigItemInput = {
  key: string;
  label?: string;
  type: 'string' | 'number' | 'boolean' | 'json' | 'secretRef';
  currentValue?: unknown;
  defaultValue?: unknown;
  editable?: boolean;
  sensitive?: boolean;
  source?: string;
  description?: string;
  validation?: Record<string, unknown>;
  metadata?: Record<string, unknown>;
};
```

Rules:

- config keys should be stable;
- sensitive values should be masked or represented as `secretRef`;
- raw secrets must not be reported;
- CE supports visibility only;
- config editing is not implemented in SDK v0.1.

---

## 19. Action Registration API

Recommended type shape:

```ts
type ActionRegistration = {
  name: string;
  label?: string;
  description?: string;
  dangerLevel?: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  enabled?: boolean;
  inputSchema?: Record<string, unknown>;
  resultSchema?: Record<string, unknown>;
  metadata?: Record<string, unknown>;
  handler: ActionHandler;
};

type ActionHandler = (
  payload: unknown,
  context: ActionContext
) => Promise<ActionResult> | ActionResult;

type ActionContext = {
  commandId: string;
  actionName: string;
  serviceCode: string;
  createdAt?: string;
  metadata?: Record<string, unknown>;
};

type ActionResult = {
  success: boolean;
  message?: string;
  data?: unknown;
};
```

Rules:

- action name must be unique;
- unknown action must fail safely;
- handler exceptions must be captured;
- result must be serializable;
- no built-in arbitrary shell action;
- high-risk actions should declare danger level.

---

## 20. Built-In Helper: runHealthCheck

SDK may provide helper behavior for a demo action, but it should not auto-register actions without developer awareness.

Recommended demo code should explicitly register:

```ts
agent.action({
  name: 'runHealthCheck',
  label: 'Run Health Check',
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

This keeps action exposure explicit.

---

## 21. Forbidden Built-In Actions

The SDK must not provide built-in actions such as:

```text
runShell
exec
bash
sh
runScript
customCommand
```

If a developer manually registers a dangerous action, it must be explicit and should declare `dangerLevel = HIGH` or `CRITICAL`.

The SDK should not encourage remote shell usage.

---

## 22. Heartbeat Loop

Heartbeat loop should:

- run after Agent token is available;
- send heartbeat periodically;
- include Agent runtime metadata;
- optionally include lightweight service status summary;
- handle Backend failure with backoff;
- avoid overlapping heartbeat requests;
- avoid raw secrets.

Recommended default:

```text
heartbeatIntervalSeconds = 30
```

Heartbeat endpoint should match Backend Agent API spec.

---

## 23. Manifest Report Loop

SDK v0.1 may report manifest:

- once after startup;
- after successful re-registration;
- after Backend reconnect if previous report failed.

Continuous frequent manifest reporting is not required.

If provider output changes dynamically, future SDK versions may support explicit `reportManifest()` calls or automatic dirty-state detection.

---

## 24. Command Polling Loop

Command polling loop should:

- run after Agent token is available;
- call Backend periodically;
- avoid overlapping polls;
- handle Backend errors with backoff;
- process Commands assigned to this Agent;
- dispatch only supported command types;
- execute one Command at a time by default;
- report CommandResult after execution.

Recommended default:

```text
commandPollIntervalSeconds = 5
```

SDK v0.1 supports only:

```text
CommandType = ACTION
```

---

## 25. Command Handling

For each Command:

1. verify `commandType = ACTION`;
2. verify `actionName` is present;
3. find registered action handler;
4. check action enabled state;
5. execute handler with payload and context;
6. capture success or failure;
7. report CommandResult.

If action is unknown:

```text
status = FAILED
errorCode = ACTION_NOT_FOUND
```

If handler throws:

```text
status = FAILED
errorCode = ACTION_FAILED
```

---

## 26. CommandResult Reporting

CommandResult should include:

```text
status
outputText
errorMessage
resultJson
startedAt
finishedAt
```

Mapping from ActionResult:

```text
success = true  -> status SUCCESS
success = false -> status FAILED
message         -> outputText or errorMessage
data            -> resultJson
```

Rules:

- sanitize result before reporting;
- do not report raw secrets;
- keep result concise;
- retry transient report failures carefully;
- avoid duplicate execution where practical.

---

## 27. Retry and Backoff

SDK should implement simple retry/backoff for:

- registration;
- heartbeat;
- manifest report;
- command polling;
- CommandResult reporting.

Recommended behavior:

```text
initial delay: 1-5 seconds
max delay: 60-300 seconds
jitter: recommended
```

CE implementation can start simple, but must avoid tight retry loops.

---

## 28. Error Handling

### 28.1 Backend unavailable

Behavior:

- log warning;
- retry later;
- keep Capsule Service running.

### 28.2 Registration token invalid

Behavior:

- log sanitized error;
- stop aggressive registration retry;
- keep service running unless strict mode is enabled.

### 28.3 Agent token invalid or revoked

Behavior:

- stop using token;
- clear token if safe;
- re-register only if registration token exists;
- avoid noisy invalid-token loop.

### 28.4 Provider error

Behavior:

- health provider error returns `UNKNOWN`;
- config provider error logs warning and reports empty or last known safe configs if implemented;
- action handler error reports failed CommandResult.

---

## 29. Logging API

The SDK should support a simple logger interface.

Recommended shape:

```ts
type AgentLogger = {
  debug?(message: string, meta?: Record<string, unknown>): void;
  info?(message: string, meta?: Record<string, unknown>): void;
  warn?(message: string, meta?: Record<string, unknown>): void;
  error?(message: string, meta?: Record<string, unknown>): void;
};
```

Default logger may use `console`.

All logs must sanitize tokens and secrets.

---

## 30. Sensitive Data Sanitization

The SDK should avoid reporting or logging sensitive data.

Sensitive keys:

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

Recommended replacement:

```text
***REDACTED***
```

Sanitization should be applied to:

- logs;
- CommandResult error details;
- config metadata where practical;
- health details where practical.

---

## 31. HTTP Client Requirements

SDK HTTP client should:

- support JSON request/response;
- set `Authorization` header for Agent API calls;
- set reasonable timeouts;
- handle non-2xx responses;
- classify retryable vs non-retryable errors;
- avoid logging raw request headers;
- avoid logging token-bearing URLs or headers;
- expose useful sanitized error messages.

The SDK may use built-in `fetch` in Node.js 20+.

---

## 32. Internal Module Structure

Recommended SDK source structure:

```text
src/
├── index.ts
├── CapsuleAgent.ts
├── options.ts
├── types.ts
├── api/
│   ├── AgentApiClient.ts
│   └── dto.ts
├── token/
│   ├── TokenStore.ts
│   └── FileTokenStore.ts
├── runtime/
│   ├── heartbeatLoop.ts
│   ├── commandPollingLoop.ts
│   └── backoff.ts
├── manifest/
│   └── buildManifest.ts
├── actions/
│   └── ActionRegistry.ts
├── security/
│   └── sanitize.ts
└── logging/
    └── logger.ts
```

The final structure may be adjusted, but responsibilities should remain separated.

---

## 33. Build and Distribution

SDK should be distributed as an npm package.

Recommended outputs:

```text
TypeScript declarations
ESM build
optional CommonJS build if needed
source maps optional
```

Recommended package scripts:

```text
build
test
lint
typecheck
format
```

The SDK should be usable from the CE demo Capsule Service without local hacks.

---

## 34. Demo Capsule Service Requirements

The repository should include or reference a demo Capsule Service using the SDK.

Demo should prove:

- registration;
- token persistence;
- heartbeat;
- manifest report;
- health report;
- config metadata;
- action definitions;
- `echo` action;
- `runHealthCheck` action;
- CommandResult reporting;
- safe logs.

Demo should not include real secrets.

---

## 35. Testing Requirements

SDK tests should cover:

- option resolution;
- environment variable loading;
- token store read/write;
- corrupted token file handling;
- registration success;
- registration token invalid;
- Agent token invalid;
- heartbeat success/failure;
- manifest construction;
- health provider success/error;
- config provider success/error;
- action registration duplicate name;
- command polling success;
- unknown command type;
- unknown action;
- action success;
- action failure;
- CommandResult reporting;
- Backend unavailable behavior;
- log sanitization;
- result sanitization.

Tests should avoid real network dependency by using mocked HTTP clients or local test servers.

---

## 36. Versioning

SDK should expose its version in Agent metadata.

Recommended fields:

```text
agentVersion
sdkVersion
protocolVersion
runtime
```

CE v0.1 may use:

```text
protocolVersion = 0.1
```

or omit protocolVersion until Backend protocol stabilizes.

However, the model should reserve space for protocol compatibility checks.

---

## 37. Future Extension Points

Reserve but do not implement full future systems:

```text
protocolVersion
capabilities
commandType expansion
command progress
secretRef resolver hook
custom token store
custom HTTP client
custom logger
manual reportManifest
Agent diagnostics metadata
```

Do not implement EE/Cloud capabilities unless needed by CE v0.1.

---

## 38. Future EE Direction

Future EE may extend the Node SDK with:

- Agent token rotation;
- capability reporting;
- diagnostics reporting;
- custom token stores;
- secret provider resolver hooks;
- command progress events;
- long-running action support;
- action-level permissions metadata;
- config apply/reload helpers;
- sidecar/external Agent interoperability helpers.

These are not SDK v0.1 requirements.

---

## 39. Future Cloud Direction

Future Cloud may extend SDK usage with:

- Cloud Agent Gateway URL;
- workspace-scoped registration token;
- connection diagnostics;
- rate-limit handling;
- WebSocket or streaming delivery;
- managed alert hints;
- usage metering metadata.

These are not SDK v0.1 requirements.

---

## 40. Anti-Patterns

Avoid these patterns.

### 40.1 SDK crashes business service on Backend outage by default

Governance outage should not automatically become business outage.

### 40.2 SDK logs tokens

Registration token and Agent token must never be logged.

### 40.3 SDK reports raw secrets

Use `secretRef` or masked values.

### 40.4 SDK includes shell action

Remote shell is not the CE operation model.

### 40.5 SDK hides too much behavior

Action registration should be explicit.

### 40.6 SDK starts future protocol complexity too early

Keep v0.1 focused on HTTP polling and the core governance loop.

---

## 41. Acceptance Criteria

Node Agent SDK v0.1 is acceptable when:

- package can be imported by a Node.js demo service;
- SDK can resolve options from code and environment variables;
- SDK can register with registration token;
- SDK stores Agent token locally;
- SDK reuses Agent token after restart;
- SDK sends authenticated heartbeat;
- SDK reports service manifest;
- SDK reports health;
- SDK reports config metadata;
- SDK reports action definitions;
- SDK polls Commands;
- SDK executes `echo` action;
- SDK executes `runHealthCheck` action;
- SDK reports CommandResult;
- SDK handles Backend downtime safely;
- SDK handles invalid registration token safely;
- SDK handles invalid Agent token safely;
- SDK logs useful sanitized errors;
- SDK does not log raw tokens;
- SDK does not report raw secrets;
- SDK does not provide arbitrary shell execution.

---

## 42. Summary

The Node.js Agent SDK is the CE reference Agent implementation.

It should be small, safe, easy to integrate, and sufficient to prove the full Opstage governance loop with a real Node.js Capsule Service.

The most important Node Agent SDK rule is:

> Make Node.js services governable through explicit SDK registration, health/config/action providers, Command polling, and safe CommandResult reporting — without introducing remote shell behavior or leaking secrets.
