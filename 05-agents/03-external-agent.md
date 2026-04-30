# External Agent

- Status: Draft
- Edition: Shared
- Priority: High

本文件属于 `xtrape-capsule` 文档集。`xtrape-capsule` 是面向轻服务 / Capsule Service 的领域体系；`xtrape-capsule-opstage` 是该体系下的统一运行态治理平台。

当前实现重点是 CE 开源社区版。EE 私有化商业版与 Cloud SaaS 版属于未来规划，CE 需要保留扩展点，但不应在早期版本实现其完整能力。

Agent 是 Capsule Service 加入 Opstage 治理体系的授权入口。CE 第一版实现 Node.js Embedded Agent，Sidecar 和 External Agent 属于后续扩展。

# External Agent

- Status: Planning
- Edition: EE
- Priority: Future
- Audience: agent developers, backend developers, Capsule Service developers, platform engineers, DevOps engineers, architects, security reviewers, AI coding agents

This document defines the planned **External Agent** model for the `xtrape-capsule` product family.

An External Agent is a separate governance process that manages one or more explicitly configured Capsule Service targets from outside their service processes.

External Agent is a future EE capability. It is not a CE v0.1 implementation requirement.

---

## 1. Purpose

The purpose of an External Agent is to make services governable when they cannot or should not embed an Agent SDK or run with a one-to-one sidecar.

An External Agent may be useful for:

- legacy services;
- non-Node.js services;
- services managed by directories or local files;
- account/session manager services;
- browser automation runtimes;
- small worker fleets;
- services that expose management endpoints;
- services that need centralized local governance from one Agent process.

External Agent should extend the Agent model without weakening Opstage's safety boundary.

---

## 2. Positioning

An External Agent is:

> A separate Agent process that governs explicitly configured external targets and reports them to Opstage as Capsule Services.

It is not:

- the Capsule Service itself;
- a generic remote shell;
- an unrestricted host controller;
- a full process supervisor by default;
- a Kubernetes operator by default;
- a full observability collector;
- a secret vault;
- a CE v0.1 feature.

The External Agent should be explicit, target-based, least-privilege, and auditable.

---

## 3. Relationship with Other Agent Modes

External Agent shares the same logical governance contract as Embedded and Sidecar Agent.

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

Differences:

```text
Embedded Agent runs inside one service process.
Sidecar Agent runs beside one service process.
External Agent runs outside one or more configured service targets.
```

Recommended relationship:

```text
External Agent Process
    ├── Target A: local HTTP endpoint
    ├── Target B: config directory
    ├── Target C: process supervisor adapter
    └── Target D: browser/account runtime adapter
        ↓ outbound Agent API
Opstage Backend
```

---

## 4. CE Boundary

CE v0.1 must not implement External Agent.

CE v0.1 implements only:

```text
Node.js Embedded Agent SDK
```

CE may reserve extension fields:

```text
agentMode
runtime
protocolVersion
capabilities
metadataJson
```

but CE must not implement External Agent runtime, target adapters, host management, or multi-target management.

---

## 5. Target-Based Model

External Agent should use explicit targets.

A target is a configured external service or runtime that the Agent manages.

Examples:

```text
local-http-service
config-directory-service
browser-profile-pool
account-session-manager
worker-group
legacy-service
```

Each target should declare:

```text
target code
target name
target type
management adapter
service identity
allowed actions
health source
config source
secretRef behavior
metadata
```

No automatic broad discovery should be enabled by default.

---

## 6. Target Configuration

A target may be configured in YAML, JSON, environment variables, or UI-generated bootstrap config.

Example YAML:

```yaml
agent:
  code: local-external-agent
  name: Local External Agent
  backendUrl: http://localhost:8080
  tokenStore: /var/lib/opstage-agent/token.json

targets:
  - code: capi-chatgpt-accounts
    name: CAPI ChatGPT Account Manager
    type: local-http
    service:
      code: capi-chatgpt-account-service
      name: CAPI ChatGPT Account Service
      runtime: nodejs
      version: 0.1.0
    localHttp:
      baseUrl: http://127.0.0.1:9100/_capsule
    actions:
      allow:
        - runHealthCheck
        - refreshAccountPool
        - validateSessions
```

Target configuration must not contain raw secrets unless explicitly designed and protected.

Prefer `secretRef`.

---

## 7. Target Types

Possible target types:

```text
local-http
filesystem
process-supervisor
container-runtime
browser-runtime
account-pool
custom-adapter
```

### 7.1 local-http

External Agent communicates with a local or private HTTP management endpoint.

### 7.2 filesystem

External Agent reads manifest, config, or status from files in a configured directory.

### 7.3 process-supervisor

External Agent interacts with a safe process supervisor API or adapter.

### 7.4 container-runtime

External Agent interacts with Docker or another container runtime through restricted adapters.

### 7.5 browser-runtime

External Agent manages browser/account/session runtimes through predefined safe adapters.

### 7.6 account-pool

External Agent observes and operates account pools through explicit account-management actions.

### 7.7 custom-adapter

External Agent uses a custom adapter plugin or script-like adapter.

Custom adapters require strong security rules and should not become arbitrary shell execution.

---

## 8. Adapter Model

External Agent should use adapters to manage targets.

Adapter responsibilities:

- read target manifest;
- read target health;
- read config metadata;
- read action definitions;
- execute predefined actions;
- sanitize results;
- map local errors to CommandResult errors;
- avoid raw secret leakage.

Adapter interface may look conceptually like:

```ts
interface ExternalTargetAdapter {
  getManifest(): Promise<CapsuleManifest>;
  getHealth(): Promise<HealthReport>;
  getConfigs(): Promise<ConfigItem[]>;
  getActions(): Promise<ActionDefinition[]>;
  executeAction(actionName: string, payload: unknown, context: ActionContext): Promise<ActionResult>;
}
```

This is planning only and not CE v0.1 API.

---

## 9. Local HTTP Target Contract

For local HTTP targets, External Agent may reuse the Sidecar local management contract:

```http
GET  /_capsule/manifest
GET  /_capsule/health
GET  /_capsule/configs
GET  /_capsule/actions
POST /_capsule/actions/{actionName}
```

This allows one local management protocol to support both Sidecar and External Agent models.

The endpoint should be private and protected.

---

## 10. Filesystem Target Contract

A filesystem target may expose governance metadata through files.

Example directory:

```text
/opt/capsule-targets/demo-service/
├── manifest.json
├── health.json
├── configs.json
├── actions.json
└── state/
```

Rules:

- configured directory must be explicit;
- Agent should not scan broad filesystem paths;
- file permissions must be documented;
- files must not contain raw secrets;
- action execution through filesystem should be carefully designed and is not recommended as the first option.

Filesystem target is useful mainly for read-only metadata visibility.

---

## 11. Process Supervisor Target

A process supervisor target may use a restricted adapter to observe or operate a service.

Possible supervisors:

```text
systemd
supervisord
pm2
Docker Compose
custom internal supervisor
```

Potential actions:

```text
getStatus
restartService
reloadService
```

Security rules:

- actions must be predefined;
- no free-form shell command;
- adapter permissions must be least privilege;
- high-risk actions must be marked HIGH or CRITICAL;
- results must be audited through Commands and CommandResults.

---

## 12. Browser or Account Runtime Target

External Agent may be useful for CAPI-style services that manage accounts, sessions, browser profiles, or automation contexts.

Possible targets:

```text
browser profile pool
LLM account pool
messaging account pool
OTP session helper
OAuth session keeper
```

Possible actions:

```text
validateSessions
refreshSession
markAccountUnavailable
rotateAccount
clearExpiredSessions
runLoginCheck
```

Rules:

- raw cookies must not be sent to Opstage;
- raw OAuth tokens must not be sent to Opstage;
- secret/session references should use `secretRef`;
- high-risk account actions should be marked HIGH or CRITICAL;
- action outputs must be sanitized.

---

## 13. External Agent Lifecycle

Recommended lifecycle:

```text
External Agent starts
    ↓
loads configuration
    ↓
loads stored Agent token
    ↓
loads explicit target configs
    ↓
initializes target adapters
    ↓
registers with Opstage if needed
    ↓
collects target manifests, health, configs, and actions
    ↓
reports Capsule Services to Opstage Backend
    ↓
starts heartbeat loop
    ↓
starts target refresh loop if configured
    ↓
starts command polling loop
    ↓
executes Commands through target adapters
    ↓
reports CommandResults
```

External Agent should continue running even if one target fails.

---

## 14. Multi-Target Management

External Agent may manage multiple targets.

Rules:

- each target maps to a Capsule Service record;
- each target has stable service code;
- target failures should be isolated;
- a failed target should not crash the whole Agent;
- Command execution must route to the correct target;
- target configuration changes should be explicit;
- target additions/removals should be auditable where supported.

Multi-target support should not become uncontrolled service discovery.

---

## 15. Service Identity Mapping

Each target should map to a Capsule Service identity.

Recommended target-to-service mapping:

```text
target.code -> CapsuleService.code or service.code
agent.id + target.code -> management identity
```

Possible uniqueness:

```text
workspaceId + service.code
```

or:

```text
workspaceId + agentId + target.code
```

The final uniqueness rule should align with Backend service identity design.

---

## 16. Registration and Token Handling

External Agent uses the same registration and Agent token model as other Agents.

Rules:

- registration token is used for Agent enrollment;
- Backend stores only registration token hash;
- Backend issues Agent token;
- External Agent stores Agent token locally;
- Backend stores only Agent token hash;
- Agent token is sent through Authorization header;
- raw tokens must not be logged.

Target credentials should not be mixed with Opstage Agent token.

---

## 17. Heartbeat Behavior

External Agent sends Agent-level heartbeat.

Heartbeat may include:

```text
agentMode = external
Agent version
runtime
hostname
OS
architecture
target count
target summary
```

Target-specific health should be reported as Capsule Service health, not only Agent heartbeat.

If one target is down but Agent is alive, Agent status may remain online while that service is DOWN or STALE.

---

## 18. Service Report Behavior

External Agent reports one Capsule Service per target.

For each target, it may report:

```text
service identity
runtime
version
agentMode = external
targetType
manifestJson
health
configs
actions
metadata
```

Report failures should be isolated per target.

---

## 19. Command Execution Behavior

External Agent routes Commands to target adapters.

Flow:

```text
External Agent polls Command
    ↓
validates Command assignment
    ↓
finds target by serviceId or serviceCode
    ↓
finds target adapter
    ↓
validates action exists and is allowed
    ↓
executes target adapter action
    ↓
sanitizes result
    ↓
reports CommandResult
```

If target is missing or unavailable, report failed CommandResult.

---

## 20. Action Allowlist

External Agent should support target action allowlists.

Example:

```yaml
actions:
  allow:
    - runHealthCheck
    - validateSessions
    - refreshAccountPool
```

Rules:

- unknown actions are rejected;
- actions not in allowlist are rejected;
- high-risk actions must be explicitly allowed;
- no wildcard allow by default;
- arbitrary shell actions are not allowed by default.

---

## 21. Security Boundary

External Agent has broader risk than Embedded or Sidecar Agent because it may manage multiple targets.

Security rules:

1. Require explicit target configuration.
2. Use least privilege for target adapters.
3. Do not scan broad host resources by default.
4. Do not expose arbitrary shell execution.
5. Do not log raw tokens or secrets.
6. Do not send raw credentials to Opstage.
7. Use `secretRef` for secret references.
8. Isolate target failures.
9. Audit operations through CommandResult and Backend AuditEvents.
10. Mark high-risk actions clearly.

---

## 22. Secret Boundary

External Agent may interact with sensitive local targets, especially account/session services.

Default rule:

```text
Opstage stores secretRef.
External Agent or target runtime resolves raw secret locally.
Raw secret is not sent to Opstage Backend.
```

Examples:

```text
agent-local://external-agent/secrets/account-001
vault://kv/capi/chatgpt/account-001
browser-profile://local/profile-001
```

Command payloads and results should use references and summaries instead of raw credentials.

---

## 23. Failure Modes

### 23.1 Opstage Backend unavailable

External Agent should:

- keep running;
- retry with backoff;
- avoid log spam;
- keep targets unaffected.

### 23.2 One target unavailable

External Agent should:

- mark that target service as DOWN or UNKNOWN;
- continue managing other targets;
- fail Commands for that target safely.

### 23.3 Adapter failure

External Agent should:

- isolate adapter error;
- report sanitized CommandResult failure;
- keep Agent process alive.

### 23.4 Configuration error

External Agent should:

- reject invalid target config;
- log sanitized error;
- continue with valid targets if possible.

### 23.5 Token invalid

External Agent should:

- stop using invalid Agent token;
- clear token if safe;
- re-register only if registration token exists;
- avoid noisy invalid-token loops.

---

## 24. Logging Rules

External Agent logs should include:

- startup summary;
- target config load result;
- target adapter initialization result;
- registration success/failure;
- heartbeat failure;
- service report failure;
- command polling failure;
- target action execution failure;
- CommandResult report failure.

External Agent logs must not include:

```text
registration token
Agent token
password
cookie
OAuth token
API key
private key
raw secret
raw browser session
```

---

## 25. Comparison with Embedded and Sidecar Agent

| Area | Embedded Agent | Sidecar Agent | External Agent |
|---|---|---|---|
| Process location | inside service | beside service | outside one or more targets |
| CE v0.1 | implemented for Node.js | not implemented | not implemented |
| Target count | usually one | usually one | one or many |
| Service code change | SDK integration | local management interface | target adapter/config |
| Isolation | lowest | medium | medium/high |
| Runtime flexibility | SDK-dependent | high | high |
| Operational risk | lower | medium | higher |
| Best for | new Node.js services | one isolated service | legacy, fleets, account/session managers |

---

## 26. Risks

### 26.1 Over-broad host access

External Agent may be given too much filesystem or process access.

Mitigation:

- explicit target config;
- least privilege;
- no broad scanning by default.

### 26.2 Arbitrary execution drift

External Agent may drift into a remote shell tool.

Mitigation:

- predefined adapters and actions only;
- no built-in shell execution;
- action allowlists.

### 26.3 Secret leakage

External Agent may touch sensitive account/session data.

Mitigation:

- use `secretRef`;
- sanitize outputs;
- do not log secrets;
- keep raw credentials local.

### 26.4 Target identity confusion

Multiple targets may cause command routing mistakes.

Mitigation:

- stable target identity;
- explicit service mapping;
- Backend Agent ownership validation;
- per-target adapter registry.

### 26.5 Operational complexity

External Agent adds configuration and adapter complexity.

Mitigation:

- start with one or two adapter types;
- provide strong examples;
- add diagnostics.

---

## 27. Future EE Direction

Future EE External Agent may add:

- official external Agent binary;
- Docker image;
- systemd deployment template;
- local HTTP target adapter;
- filesystem target adapter;
- process supervisor adapter;
- account/session manager adapter;
- target diagnostics;
- target action allowlists;
- secret provider resolvers;
- Agent token rotation;
- capability reporting;
- compatibility matrix.

---

## 28. Future Cloud Direction

Future Cloud may use External Agent with:

- Cloud Agent Gateway;
- workspace-scoped registration tokens;
- Cloud connection diagnostics;
- Agent traffic rate limiting;
- usage metering by Agent and service count;
- managed alerts on target health;
- Cloud enrollment instructions;
- target count plan limits.

These are future planning items.

---

## 29. CE Reservations

CE should reserve these External Agent-compatible concepts:

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
metadataJson
protocolVersion if practical
capabilities if practical
```

CE should not implement External Agent runtime in v0.1.

---

## 30. Acceptance Criteria for Future External Agent

A future External Agent implementation is acceptable when:

- External Agent runs as a separate process;
- External Agent can register with Opstage Backend;
- External Agent stores and reuses Agent token;
- External Agent loads explicit target configs;
- External Agent initializes target adapters;
- External Agent reports one Capsule Service per target;
- External Agent reports health per target;
- External Agent reports config metadata per target;
- External Agent reports action definitions per target;
- External Agent polls Commands;
- External Agent routes Commands to the correct target adapter;
- External Agent enforces action allowlists;
- External Agent reports CommandResults;
- one target failure does not crash all targets;
- Opstage Backend outage is handled safely;
- raw tokens are not logged;
- raw secrets are not reported;
- no arbitrary shell execution is provided by default.

---

## 31. Summary

External Agent is a future Agent mode for governing explicitly configured services or runtimes from outside their processes.

It is valuable for legacy services, account/session managers, browser automation runtimes, and small local service fleets, but it carries broader security and operational risks than Embedded Agent.

The most important External Agent rule is:

> Govern only explicit targets through least-privilege adapters and predefined actions; never let External Agent become an unrestricted host controller or remote shell.