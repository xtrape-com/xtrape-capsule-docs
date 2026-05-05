---
status: proposed
audience: architects
stability: evolving
last_reviewed: 2026-05-05
---

# Sidecar Agent

- Status: Planning
- Edition: EE
- Priority: Future
- Audience: agent SDK developers, Capsule Service developers, backend developers, platform engineers, DevOps engineers, architects, security reviewers, AI coding agents

This document defines the planned **Sidecar Agent** model for the `xtrape-capsule` product family.

A Sidecar Agent is a separate process that runs close to a Capsule Service and connects that service to Opstage governance through local management interfaces.

Sidecar Agent is a future EE capability. It is not a CE v0.1 implementation requirement.

---

## 1. Purpose

The purpose of a Sidecar Agent is to make a Capsule Service governable without embedding the Agent SDK directly into the service process.

A Sidecar Agent allows Opstage to govern services that:

- cannot embed the Node.js Agent SDK;
- are written in different languages;
- should keep governance code outside the business process;
- expose a local management endpoint;
- expose metadata through local files or IPC;
- run in container groups or pods;
- need stronger process isolation than Embedded Agent.

The Sidecar Agent extends the Agent model while preserving the same governance contract.

---

## 2. Positioning

A Sidecar Agent is:

> A separate local governance process that represents one nearby Capsule Service to Opstage.

It is not:

- the Capsule Service itself;
- a host-wide process supervisor;
- a generic remote shell;
- a Kubernetes operator by itself;
- a full observability collector;
- a secret vault;
- a replacement for the Embedded Agent in CE;
- a CE v0.1 requirement.

The Sidecar Agent should govern a clearly configured local service through explicit management contracts.

---

## 3. Relationship with Embedded Agent

Embedded Agent and Sidecar Agent share the same logical contract.

Shared contract:

```text
registration
Agent token authentication
heartbeat
service manifest report
health report
config metadata report
action definition report
Command polling or receiving
predefined action execution
CommandResult reporting
AuditEvent creation by Backend
```

Difference:

```text
Embedded Agent runs inside service process.
Sidecar Agent runs beside service process.
```

Recommended relationship:

```text
Capsule Service Process
    ↑ local management interface
Sidecar Agent Process
    ↓ outbound Agent API
Opstage Backend
```

---

## 4. CE Boundary

CE v0.1 must not implement Sidecar Agent.

CE v0.1 implements only:

```text
Node.js Embedded Agent SDK
```

CE may reserve these fields:

```text
agentMode
runtime
protocolVersion
capabilities
metadataJson
```

but CE must not implement sidecar runtime, sidecar packaging, or sidecar management contracts.

---

## 5. Target Use Cases

### 5.1 Non-Node.js service

A Java, Python, Go, or legacy service cannot use the Node.js embedded SDK but can expose a local management endpoint.

### 5.2 Process isolation

A team wants governance code isolated from business service code.

### 5.3 Container sidecar

A service runs with an Agent container in the same Docker Compose service group or Kubernetes Pod.

### 5.4 Legacy service wrapper

A legacy service exposes health/config/action metadata through files or a local endpoint, and the Sidecar Agent adapts it to Opstage.

### 5.5 Restricted service runtime

The service runtime cannot install additional SDK dependencies, but can expose a small local management interface.

---

## 6. Deployment Models

### 6.1 Local process pair

```text
Host
├── Capsule Service process
└── Sidecar Agent process
```

The Sidecar Agent communicates with the service through localhost, Unix socket, or local files.

### 6.2 Docker Compose sidecar

```text
Compose project
├── capsule-service container
└── sidecar-agent container
```

The two containers share:

- internal network;
- mounted configuration directory;
- optional shared volume;
- local management endpoint.

### 6.3 Kubernetes Pod sidecar

```text
Pod
├── app container
└── sidecar-agent container
```

The Sidecar Agent communicates with the app container through localhost inside the Pod.

Kubernetes Sidecar Agent support is future work and may need additional security design.

---

## 7. Local Management Interface

The Sidecar Agent needs a local management interface to understand and operate the Capsule Service.

Possible interfaces:

```text
local HTTP endpoint
Unix domain socket
local TCP port
local IPC
shared manifest file
shared config metadata file
local action adapter
mounted directory
```

The first Sidecar Agent design should prefer a simple local HTTP management endpoint.

---

## 8. Recommended Local HTTP Contract

A future local HTTP management contract may use endpoints such as:

```http
GET  /_capsule/manifest
GET  /_capsule/health
GET  /_capsule/configs
GET  /_capsule/actions
POST /_capsule/actions/{actionName}
```

These endpoints are local service-side endpoints, not Opstage Backend endpoints.

They should normally be bound to localhost or private container network only.

---

## 9. Local Manifest Endpoint

Endpoint:

```http
GET /_capsule/manifest
```

Purpose:

```text
Return Capsule Service identity, runtime, version, configs, actions, and metadata.
```

Example response:

```json
{
  "code": "demo-java-service",
  "name": "Demo Java Service",
  "description": "A demo service managed by Sidecar Agent.",
  "version": "0.1.0",
  "runtime": "java",
  "agentMode": "sidecar",
  "configs": [],
  "actions": []
}
```

Manifest must not include raw secrets.

---

## 10. Local Health Endpoint

Endpoint:

```http
GET /_capsule/health
```

Purpose:

```text
Return current health status of the local Capsule Service.
```

Example response:

```json
{
  "status": "UP",
  "message": "Service is healthy.",
  "dependencies": [
    {
      "name": "database",
      "type": "database",
      "status": "UP",
      "message": "Database is reachable."
    }
  ]
}
```

Health must not include raw tokens, cookies, passwords, API keys, or private business data.

---

## 11. Local Configs Endpoint

Endpoint:

```http
GET /_capsule/configs
```

Purpose:

```text
Return configuration metadata for governance visibility.
```

Example response:

```json
[
  {
    "key": "service.mode",
    "label": "Service Mode",
    "type": "string",
    "currentValue": "production",
    "editable": false,
    "sensitive": false,
    "source": "env"
  },
  {
    "key": "account.secret",
    "label": "Account Secret",
    "type": "secretRef",
    "currentValue": "vault://kv/integration/account-001",
    "editable": false,
    "sensitive": true,
    "source": "vault"
  }
]
```

Sensitive values should be masked or represented as `secretRef`.

---

## 12. Local Actions Endpoint

Endpoint:

```http
GET /_capsule/actions
```

Purpose:

```text
Return predefined actions exposed by the Capsule Service.
```

Example response:

```json
[
  {
    "name": "runHealthCheck",
    "label": "Run Health Check",
    "description": "Runs an immediate health check.",
    "dangerLevel": "LOW",
    "enabled": true,
    "inputSchema": {
      "type": "object",
      "properties": {}
    }
  }
]
```

Only predefined actions should be exposed.

---

## 13. Local Action Execution Endpoint

Endpoint:

```http
POST /_capsule/actions/{actionName}
```

Purpose:

```text
Execute a predefined local action.
```

Example request:

```json
{
  "payload": {
    "message": "hello"
  },
  "context": {
    "commandId": "cmd_001"
  }
}
```

Example response:

```json
{
  "success": true,
  "message": "Action completed.",
  "data": {
    "message": "hello"
  }
}
```

The service must reject unknown actions.

The Sidecar Agent must not expose arbitrary shell execution as a generic action.

---

## 14. Sidecar Agent Lifecycle

Recommended lifecycle:

```text
Sidecar Agent starts
    ↓
loads configuration
    ↓
loads stored Agent token
    ↓
connects to local Capsule Service management interface
    ↓
registers with Opstage if needed
    ↓
fetches local manifest/configs/actions/health
    ↓
reports service manifest to Opstage Backend
    ↓
starts heartbeat loop
    ↓
starts command polling loop
    ↓
executes Commands through local action endpoint
    ↓
reports CommandResults
```

If the local service is unavailable, Sidecar Agent should report degraded or unknown health rather than crashing.

---

## 15. Sidecar Configuration

Recommended Sidecar Agent configuration fields:

```text
backendUrl
registrationToken
agentCode
agentName
tokenStore
localServiceUrl
localManagementAuth
heartbeatIntervalSeconds
commandPollIntervalSeconds
serviceCode override if needed
logLevel
strictMode
```

Recommended environment variables:

```text
OPSTAGE_BACKEND_URL=http://opstage:8080
OPSTAGE_REGISTRATION_TOKEN=opstage_reg_xxx
OPSTAGE_AGENT_TOKEN_FILE=/var/lib/opstage-agent/token.json
OPSTAGE_AGENT_CODE=demo-java-sidecar
OPSTAGE_AGENT_NAME=Demo Java Sidecar
CAPSULE_LOCAL_SERVICE_URL=http://localhost:9000
OPSTAGE_HEARTBEAT_INTERVAL_SECONDS=30
OPSTAGE_COMMAND_POLL_INTERVAL_SECONDS=5
```

---

## 16. Registration and Token Handling

Sidecar Agent uses the same registration and Agent token model as Embedded Agent.

Rules:

- registration token is used only for enrollment;
- Backend stores registration token hash;
- Backend issues Agent token after registration;
- Sidecar Agent stores Agent token locally;
- Backend stores only Agent token hash;
- Agent token is sent through Authorization header;
- raw tokens must not be logged.

Sidecar Agent should support token deletion and re-registration for operational recovery.

---

## 17. Heartbeat Behavior

Sidecar Agent sends heartbeat to Opstage Backend.

Heartbeat should include:

```text
Agent identity derived from token
agentMode = sidecar
runtime of Sidecar Agent
local service runtime if known
Agent version
local service connectivity summary
```

Heartbeat must not include raw secrets.

If local service is unreachable, heartbeat may still succeed while service health is reported as `UNKNOWN` or `DOWN`.

---

## 18. Service Report Behavior

Sidecar Agent reports the managed Capsule Service to Opstage Backend.

The report may be built from:

- local manifest endpoint;
- local config endpoint;
- local action endpoint;
- local health endpoint;
- static sidecar configuration;
- mounted manifest file.

The reported `agentMode` should be:

```text
sidecar
```

---

## 19. Command Execution Behavior

Sidecar Agent receives Commands from Opstage Backend and maps them to local action execution.

Flow:

```text
Sidecar Agent polls Command
    ↓
validates Command assignment
    ↓
checks local action definition
    ↓
POSTs to local action endpoint
    ↓
receives local action result
    ↓
sanitizes result
    ↓
reports CommandResult to Opstage Backend
```

If local service is unavailable, Sidecar Agent should report CommandResult as `FAILED` with a sanitized error.

---

## 20. Local Interface Security

The local management interface is security-sensitive.

Rules:

- bind to localhost or private container network;
- do not expose management endpoint publicly;
- use local authentication if needed;
- restrict allowed actions;
- validate payloads;
- sanitize errors;
- avoid raw secret output;
- log carefully;
- document deployment assumptions.

In container or Kubernetes deployments, network exposure must be reviewed carefully.

---

## 21. Secret Boundary

Sidecar Agent should preserve the `secretRef` boundary.

Recommended default:

```text
Opstage stores secretRef.
Sidecar Agent or local service resolves secret locally.
Raw secret remains outside Opstage Backend.
```

Possible secretRef examples:

```text
vault://kv/integration/account-001
agent-local://sidecar-agent/secrets/account-001
k8s-secret://namespace/name/key
```

Sidecar Agent must not report raw secrets in manifest, health, configs, logs, or CommandResults.

---

## 22. Failure Modes

### 22.1 Opstage Backend unavailable

Sidecar Agent should:

- keep running;
- retry with backoff;
- avoid log spam;
- keep local service unaffected.

### 22.2 Local service unavailable

Sidecar Agent should:

- keep heartbeat to Opstage if possible;
- report service health as `DOWN` or `UNKNOWN`;
- fail action Commands safely;
- retry local service connection.

### 22.3 Local action fails

Sidecar Agent should:

- capture sanitized error;
- report failed CommandResult;
- continue processing future Commands.

### 22.4 Agent token invalid

Sidecar Agent should:

- stop using invalid token;
- clear local token if safe;
- re-register only if registration token is available;
- avoid noisy invalid-token loops.

---

## 23. Logging Rules

Sidecar Agent logs should include:

- startup status;
- local service connection status;
- registration success/failure;
- heartbeat failure;
- service report failure;
- command polling failure;
- local action execution failure;
- CommandResult report failure.

Sidecar Agent logs must not include:

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

## 24. Comparison with Embedded Agent

| Area | Embedded Agent | Sidecar Agent |
|---|---|---|
| Process | inside service process | separate nearby process |
| CE v0.1 | implemented for Node.js | not implemented |
| Service code change | required | local management interface required |
| Runtime support | SDK language dependent | can support more runtimes |
| Isolation | lower | stronger |
| Deployment complexity | lower | higher |
| Local interface | direct in-process calls | HTTP/IPC/files |
| Best for | new Node.js services | non-Node, legacy, isolated services |

---

## 25. Risks

### 25.1 Local management endpoint exposure

If exposed publicly, it may become a security vulnerability.

Mitigation:

- bind to localhost or private network;
- document deployment security;
- use local auth where needed.

### 25.2 Contract drift

Local management contract may diverge across runtimes.

Mitigation:

- define a stable management contract;
- version the contract;
- add compatibility tests.

### 25.3 Over-powerful sidecar

Sidecar Agent may drift into arbitrary host control.

Mitigation:

- keep actions predefined;
- avoid shell execution;
- require explicit adapters.

### 25.4 Operational complexity

Sidecar adds another process or container.

Mitigation:

- provide clear deployment templates;
- make diagnostics visible.

---

## 26. Future EE Direction

Future EE Sidecar Agent may add:

- official sidecar binary;
- Docker image;
- Docker Compose template;
- Kubernetes Pod template;
- local management contract SDKs;
- service-side helper libraries;
- sidecar diagnostics;
- token rotation;
- local management authentication;
- secret provider integration;
- command progress reporting.

---

## 27. Future Cloud Direction

Future Cloud may use Sidecar Agent with:

- Cloud Agent Gateway;
- workspace-scoped registration tokens;
- Cloud connection diagnostics;
- rate limiting;
- usage metering;
- managed alerts on sidecar connectivity;
- Cloud enrollment instructions.

These are future planning items.

---

## 28. CE Reservations

CE should reserve these Sidecar-compatible concepts:

```text
agentMode
runtime
Agent token model
registration token model
service manifest
health report
config metadata
action definition
Command
CommandResult
secretRef
protocolVersion if practical
capabilities if practical
```

CE should not implement Sidecar Agent runtime in v0.1.

---

## 29. Acceptance Criteria for Future Sidecar Agent

A future Sidecar Agent implementation is acceptable when:

- Sidecar Agent can run as a separate process;
- Sidecar Agent can register with Opstage Backend;
- Sidecar Agent can store and reuse Agent token;
- Sidecar Agent can connect to local Capsule Service management interface;
- Sidecar Agent can report service manifest;
- Sidecar Agent can report health;
- Sidecar Agent can report config metadata;
- Sidecar Agent can report action definitions;
- Sidecar Agent can poll Commands;
- Sidecar Agent can execute local predefined actions;
- Sidecar Agent can report CommandResults;
- local service outage is handled safely;
- Opstage Backend outage is handled safely;
- raw tokens are not logged;
- raw secrets are not reported;
- no arbitrary shell execution is provided by default.

---

## 30. Summary

Sidecar Agent is a future Agent mode for governing services that should not or cannot embed an Agent SDK directly.

It should preserve the same Opstage governance contract while adding process isolation and runtime flexibility.

The most important Sidecar Agent rule is:

> Keep the Sidecar Agent close to the service, explicit in its local management contract, outbound-first toward Opstage, and limited to predefined governance operations.
