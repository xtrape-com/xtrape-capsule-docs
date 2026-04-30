# Opstage Agent Integration

- Status: Implementation Guidance
- Edition: Shared
- Priority: High
- Audience: agent SDK developers, backend developers, Capsule Service developers, architects, security reviewers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/openapi/opstage-ce-v0.1.yaml` disagree, the ADRs and OpenAPI contract win for CE v0.1.

This document defines the Agent integration subsystem of **Opstage**.

Agent integration is the bridge between Opstage Backend and Capsule Services. It allows lightweight services to become visible, manageable, and auditable without becoming dependent on Opstage for their core business runtime.

The current implementation focus is **Opstage CE**. EE and Cloud Agent capabilities are future planning tracks and must not expand the CE v0.1 implementation scope.

---

## 1. Purpose

The purpose of Agent integration is to make Capsule Services governable by Opstage.

Agent integration should allow Opstage to:

- register Agents;
- authenticate Agents;
- receive heartbeats;
- receive Capsule Service manifests;
- receive health reports;
- receive config metadata;
- receive predefined action metadata;
- deliver Commands;
- receive CommandResults;
- record audit-relevant operation results;
- calculate Agent and service freshness.

Agent integration should not take over the Capsule Service's business runtime.

---

## 2. Positioning

An Agent is:

> A governance bridge between Opstage Backend and one or more Capsule Services.

An Agent is not:

- the Capsule Service itself;
- the business logic owner;
- a remote shell;
- a generic process supervisor;
- a secret vault;
- a browser automation framework by itself;
- a full observability collector in CE;
- a deployment orchestrator in CE.

The Agent makes the service governable, but the service remains responsible for its own business behavior.

---

## 3. Relationship with Opstage Components

Recommended CE relationship:

```text
Opstage UI
    ↓ Admin API
Opstage Backend
    ↑ Agent API
Node.js Embedded Agent SDK
    ↔ Capsule Service providers and handlers
Capsule Service
```

The Agent communicates with Opstage Backend through Agent APIs.

The UI never calls Agent directly.

The Backend does not require inbound network access to the Agent in CE.

---

## 4. Core Agent Responsibilities

The Agent is responsible for:

- loading Agent configuration;
- registering with Opstage using a registration token;
- storing Agent token locally;
- authenticating to Backend with Agent token;
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

## 5. Agent Non-Responsibilities

CE Agent should not be responsible for:

- executing arbitrary shell commands;
- managing all application logs;
- collecting arbitrary metrics and traces;
- storing raw secrets in Opstage;
- replacing service-specific business logic;
- starting or supervising the Capsule Service process;
- providing sidecar/external management mode;
- supporting Java/Python/Go runtimes;
- implementing Cloud Agent Gateway behavior;
- implementing enterprise secret provider integration.

Future editions may add some of these through explicit designs, but CE Agent should stay small and safe.

---

## 6. CE Agent Scope

Opstage CE v0.1 implements one Agent mode:

```text
Node.js embedded Agent SDK
```

The CE Agent SDK should support:

- registration with registration token;
- Agent token storage;
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

## 7. CE Agent Non-Goals

CE v0.1 Agent integration should not implement:

- sidecar Agent;
- external Agent;
- host Agent;
- Kubernetes Agent;
- Java Agent SDK;
- Python Agent SDK;
- Go Agent SDK;
- Agent Gateway;
- WebSocket command channel;
- gRPC streaming;
- offline command queue;
- Agent auto-upgrade;
- Agent fleet management;
- service discovery;
- enterprise secret provider resolver;
- arbitrary shell execution.

These are future EE or Cloud planning items.

---

## 8. Agent Modes

Long-term Agent modes may include:

| Mode | Description | CE v0.1 |
|---|---|---|
| embedded | Agent runs inside Capsule Service process | Node.js only |
| sidecar | Agent runs beside one service | Not implemented |
| external | Agent manages one or more services externally | Not implemented |
| host | Agent manages services on one host | Not implemented |
| kubernetes | Agent manages services in a Kubernetes cluster | Not implemented |

CE should preserve the `agentMode` field but only implement `embedded`.

---

## 9. Node.js Embedded Agent

The Node.js Embedded Agent runs inside a Node.js Capsule Service process.

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
- good fit for CE prototype.

Limitations:

- requires code integration;
- applies only to Node.js services in CE;
- cannot manage legacy or non-Node services;
- Agent failures must not crash the business service by default.

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

The exact API may evolve during implementation, but the CE developer experience should stay close to this shape.

---

## 11. Agent Configuration

Recommended Agent configuration options:

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

Agent registration flow:

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
- scoped to default Workspace in CE;
- revocable;
- optionally expiring;
- optionally one-time use.

---

## 13. Agent Token Handling

Agent token is used after registration.

Rules:

- Backend stores only token hash;
- Agent stores raw token locally through a token store;
- Agent sends token via Authorization header;
- Agent token must not be logged;
- Agent token should be cleared if Backend reports revoked or invalid token;
- token rotation is future EE work.

Authorization header:

```http
Authorization: Bearer <agentToken>
```

---

## 14. Startup Lifecycle

Recommended Agent startup lifecycle:

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

If Backend is unavailable at startup, Agent should:

- log a warning;
- retry in background;
- not crash the Capsule Service by default;
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
- Agent version;
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

Agent SDK should allow Capsule Service to register a health provider.

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

If the health provider throws, Agent should report safe `UNKNOWN` health or log the provider failure without crashing the service.

---

## 18. Config Provider

Agent SDK should allow Capsule Service to expose config metadata.

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
- CE v0.1 supports visibility only;
- config editing and publishing are future EE work.

---

## 19. Action Registry

Agent SDK should allow Capsule Service to register predefined actions.

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

CE command delivery uses polling.

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

CE v0.1 supports only:

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

Agent should continue processing future Commands after one command fails.

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

Agent should handle these error categories:

### Backend unavailable

Behavior:

- log warning;
- retry later;
- keep Capsule Service running.

### Registration token invalid

Behavior:

- log clear error;
- stop repeated noisy registration attempts;
- keep business service running unless strict mode is configured.

### Agent token invalid or revoked

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

## 24. Security Rules

Agent integration must follow these security rules:

1. Do not log registration token.
2. Do not log Agent token.
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

Agent may send governance metadata to Backend:

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
- OAuth access tokens;
- OAuth refresh tokens;
- private keys;
- raw account credentials;
- large application logs;
- customer business records.

Use `secretRef` for sensitive references.

---

## 26. Logging Rules

Agent logs should include useful operational information:

- registration success;
- registration failure without token exposure;
- heartbeat failure;
- service report failure;
- command execution failure;
- command result report failure.

Agent logs must not include:

- registration token;
- Agent token;
- passwords;
- cookies;
- API keys;
- OAuth tokens;
- raw secrets.

---

## 27. Offline Behavior

If Opstage Backend is offline, Agent should:

- keep Capsule Service running;
- retry heartbeat and polling;
- avoid unbounded log spam;
- avoid crashing the process;
- report latest state once Backend recovers;
- re-report manifest if needed.

Governance availability should not become business runtime availability.

---

## 28. Future EE Agent Extensions

Future EE may add:

- Java embedded Agent SDK;
- Python embedded Agent SDK;
- Go Agent SDK;
- sidecar Agent;
- external Agent;
- host Agent;
- Kubernetes Agent;
- Agent capability reporting;
- Agent diagnostics UI;
- Agent token rotation;
- Agent version compatibility matrix;
- secret provider integration;
- WebSocket or queue-backed command delivery.

These are not CE v0.1 requirements.

---

## 29. Future Cloud Agent Extensions

Future Cloud may add:

- Agent Gateway;
- multi-tenant Agent routing;
- Cloud connection diagnostics;
- rate limiting;
- WebSocket or streaming connections;
- hosted Agent enrollment flow;
- workspace-scoped registration tokens;
- usage metering by Agent;
- managed alerting on Agent state.

These are not CE v0.1 requirements.

---

## 30. Acceptance Criteria

Opstage CE Agent integration is acceptable when:

- Node.js embedded Agent SDK can be imported by demo service;
- Agent can register with Backend using registration token;
- Agent token is stored locally and reused;
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
- invalid token handling is safe;
- raw tokens are not logged;
- raw secrets are not reported;
- no arbitrary shell action exists.

---

## 31. Summary

Opstage Agent integration is the bridge that makes Capsule Services governable.

It should be lightweight, safe, outbound-first, and based on predefined capabilities.

The most important Agent integration rule is:

> The Agent makes a Capsule Service visible and operable through Opstage, but it must not take ownership of the service's business runtime or expose unsafe arbitrary execution.
