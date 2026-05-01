<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 03-external-agent.md
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

# External Agent（代理）

- Status: Planning
- Edition: EE（企业版）
- Priority: Future
- Audience: agent developers, backend developers, Capsule Service（胶囊服务） developers, platform engineers, DevOps engineers, architects, security reviewers, AI coding agents

This document 定义 the planned **External Agent（代理）** model for the `xtrape-capsule` product family.

An External Agent（代理） is a separate governance process that manages one or more explicitly configured Capsule Service（胶囊服务） targets from outside their service processes.

External Agent（代理） is a future EE（企业版） capability. It is not a CE（社区版） v0.1 implementation requirement.

---

## 1. Purpose

The purpose of an External Agent（代理） is to make services governable when they cannot or should not embed an Agent（代理） SDK or run with a one-to-one sidecar.

An External Agent（代理） may be useful for:

- legacy services;
- non-Node.js services;
- services managed by directories or local files;
- account/session manager services;
- browser automation runtimes;
- small worker fleets;
- services that expose management endpoints;
- services that need centralized local governance from one Agent（代理） process.

External Agent（代理） should extend the Agent（代理） model without weakening Opstage（运维舞台）'s safety boundary.

---

## 2. Positioning

An External Agent（代理） is:

> A separate Agent（代理） process that governs explicitly configured external targets and reports them to Opstage（运维舞台） as Capsule Services.

It is not:

- the Capsule Service（胶囊服务） itself;
- a generic remote shell;
- an unrestricted host controller;
- a full process supervisor by default;
- a Kubernetes operator by default;
- a full observability collector;
- a secret vault;
- a CE（社区版） v0.1 feature.

The External Agent（代理） should be explicit, target-based, least-privilege, and auditable.

---

## 3. Relationship with Other Agent（代理） Modes

External Agent（代理） shares the same logical governance contract as Embedded and Sidecar Agent（代理）.

共享 contract:

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

## 4. CE（社区版） Boundary

CE（社区版） v0.1 must not implement External Agent（代理）.

CE（社区版） v0.1 implements only:

```text
Node.js Embedded Agent SDK
```

CE（社区版） may reserve extension fields:

```text
agentMode
runtime
protocolVersion
capabilities
metadataJson
```

but CE（社区版） must not implement External Agent（代理） runtime, target adapters, host management, or multi-target management.

---

## 5. Target-Based Model

External Agent（代理） should use explicit targets.

A target is a configured external service or runtime that the Agent（代理） manages.

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

## 6. Target 配置

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

External Agent（代理） communicates with a local or private HTTP management endpoint.

### 7.2 filesystem

External Agent（代理） reads manifest, config, or status from files in a configured directory.

### 7.3 process-supervisor

External Agent（代理） interacts with a safe process supervisor API or adapter.

### 7.4 container-runtime

External Agent（代理） interacts with Docker or another container runtime through restricted adapters.

### 7.5 browser-runtime

External Agent（代理） manages browser/account/session runtimes through predefined safe adapters.

### 7.6 account-pool

External Agent（代理） observes and operates account pools through explicit account-management actions.

### 7.7 custom-adapter

External Agent（代理） uses a custom adapter plugin or script-like adapter.

Custom adapters require strong security rules and should not become arbitrary shell execution.

---

## 8. Adapter Model

External Agent（代理） should use adapters to manage targets.

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

This is planning only and not CE（社区版） v0.1 API.

---

## 9. Local HTTP Target Contract

For local HTTP targets, External Agent（代理） may reuse the Sidecar local management contract:

```http
GET  /_capsule/manifest
GET  /_capsule/health
GET  /_capsule/configs
GET  /_capsule/actions
POST /_capsule/actions/{actionName}
```

This allows one local management protocol to support both Sidecar and External Agent（代理） models.

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
- Agent（代理） should not scan broad filesystem paths;
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

安全 rules:

- actions must be predefined;
- no free-form shell command;
- adapter permissions must be least privilege;
- high-risk actions must be marked HIGH or CRITICAL;
- results must be audited through Commands and CommandResults.

---

## 12. Browser or Account Runtime Target

External Agent（代理） may be useful for CAPI-style services that manage accounts, sessions, browser profiles, or automation contexts.

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

- raw cookies must not be sent to Opstage（运维舞台）;
- raw OAuth tokens must not be sent to Opstage（运维舞台）;
- secret/session references should use `secretRef`;
- high-risk account actions should be marked HIGH or CRITICAL;
- action outputs must be sanitized.

---

## 13. External Agent（代理） Lifecycle

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

External Agent（代理） should continue running even if one target fails.

---

## 14. Multi-Target Management

External Agent（代理） may manage multiple targets.

Rules:

- each target maps to a Capsule Service（胶囊服务） record;
- each target has stable service code;
- target failures should be isolated;
- a failed target should not crash the whole Agent（代理）;
- Command execution must route to the correct target;
- target configuration changes should be explicit;
- target additions/removals should be auditable where supported.

Multi-target support should not become uncontrolled service discovery.

---

## 15. Service Identity Mapping

Each target should map to a Capsule Service（胶囊服务） identity.

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

External Agent（代理） uses the same registration and Agent（代理） token model as other Agents.

Rules:

- registration token is used for Agent（代理） enrollment;
- Backend stores only registration token hash;
- Backend issues Agent（代理） token;
- External Agent（代理） stores Agent（代理） token locally;
- Backend stores only Agent（代理） token hash;
- Agent（代理） token is sent through 授权 header;
- raw tokens must not be logged.

Target credentials should not be mixed with Opstage（运维舞台） Agent（代理） token.

---

## 17. Heartbeat Behavior

External Agent（代理） sends Agent（代理）-level heartbeat.

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

Target-specific health should be reported as Capsule Service（胶囊服务） health, not only Agent（代理） heartbeat.

If one target is down but Agent（代理） is alive, Agent（代理） status may remain online while that service is DOWN or STALE.

---

## 18. Service Report Behavior

External Agent（代理） reports one Capsule Service（胶囊服务） per target.

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

External Agent（代理） routes Commands to target adapters.

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

External Agent（代理） should support target action allowlists.

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

## 21. 安全 Boundary

External Agent（代理） has broader risk than Embedded or Sidecar Agent（代理） because it may manage multiple targets.

安全 rules:

1. Require explicit target configuration.
2. Use least privilege for target adapters.
3. Do not scan broad host resources by default.
4. Do not expose arbitrary shell execution.
5. Do not log raw tokens or secrets.
6. Do not send raw credentials to Opstage（运维舞台）.
7. Use `secretRef` for secret references.
8. Isolate target failures.
9. Audit operations through CommandResult and Backend AuditEvents.
10. Mark high-risk actions clearly.

---

## 22. Secret Boundary

External Agent（代理） may interact with sensitive local targets, especially account/session services.

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

### 23.1 Opstage（运维舞台） Backend unavailable

External Agent（代理） should:

- keep running;
- retry with backoff;
- avoid log spam;
- keep targets unaffected.

### 23.2 One target unavailable

External Agent（代理） should:

- mark that target service as DOWN or UNKNOWN;
- continue managing other targets;
- fail Commands for that target safely.

### 23.3 Adapter failure

External Agent（代理） should:

- isolate adapter error;
- report sanitized CommandResult failure;
- keep Agent（代理） process alive.

### 23.4 配置 error

External Agent（代理） should:

- reject invalid target config;
- log sanitized error;
- continue with valid targets if possible.

### 23.5 Token invalid

External Agent（代理） should:

- stop using invalid Agent（代理） token;
- clear token if safe;
- re-register only if registration token exists;
- avoid noisy invalid-token loops.

---

## 24. 日志 Rules

External Agent（代理） logs should include:

- startup summary;
- target config load result;
- target adapter initialization result;
- registration success/failure;
- heartbeat failure;
- service report failure;
- command polling failure;
- target action execution failure;
- CommandResult report failure.

External Agent（代理） logs must not include:

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

## 25. Comparison with Embedded and Sidecar Agent（代理）

||Area|Embedded Agent（代理）|Sidecar Agent（代理）|External Agent（代理）||
|---|---|---|---|
||Process location|inside service|beside service|outside one or more targets||
||CE（社区版） v0.1|implemented for Node.js|not implemented|not implemented||
||Target count|usually one|usually one|one or many||
||Service code change|SDK integration|local management interface|target adapter/config||
||Isolation|lowest|medium|medium/high||
||Runtime flexibility|SDK-dependent|high|high||
||Operational risk|lower|medium|higher||
||Best for|new Node.js services|one isolated service|legacy, fleets, account/session managers||

---

## 26. Risks

### 26.1 Over-broad host access

External Agent（代理） may be given too much filesystem or process access.

Mitigation:

- explicit target config;
- least privilege;
- no broad scanning by default.

### 26.2 Arbitrary execution drift

External Agent（代理） may drift into a remote shell tool.

Mitigation:

- predefined adapters and actions only;
- no built-in shell execution;
- action allowlists.

### 26.3 Secret leakage

External Agent（代理） may touch sensitive account/session data.

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
- Backend Agent（代理） ownership validation;
- per-target adapter registry.

### 26.5 Operational complexity

External Agent（代理） adds configuration and adapter complexity.

Mitigation:

- start with one or two adapter types;
- provide strong examples;
- add diagnostics.

---

## 27. Future EE（企业版） Direction

Future EE（企业版） External Agent（代理） may add:

- official external Agent（代理） binary;
- Docker image;
- systemd deployment template;
- local HTTP target adapter;
- filesystem target adapter;
- process supervisor adapter;
- account/session manager adapter;
- target diagnostics;
- target action allowlists;
- secret provider resolvers;
- Agent（代理） token rotation;
- capability reporting;
- compatibility matrix.

---

## 28. Future Cloud（云版） Direction

Future Cloud（云版） may use External Agent（代理） with:

- Cloud（云版） Agent（代理） Gateway;
- workspace-scoped registration tokens;
- Cloud（云版） connection diagnostics;
- Agent（代理） traffic rate limiting;
- usage metering by Agent（代理） and service count;
- managed alerts on target health;
- Cloud（云版） enrollment instructions;
- target count plan limits.

These are future planning items.

---

## 29. CE（社区版） Reservations

CE（社区版） should reserve these External Agent（代理）-compatible concepts:

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

CE（社区版） should not implement External Agent（代理） runtime in v0.1.

---

## 30. Acceptance Criteria for Future External Agent（代理）

A future External Agent（代理） implementation is acceptable when:

- External Agent（代理） runs as a separate process;
- External Agent（代理） can register with Opstage（运维舞台） Backend;
- External Agent（代理） stores and reuses Agent（代理） token;
- External Agent（代理） loads explicit target configs;
- External Agent（代理） initializes target adapters;
- External Agent（代理） reports one Capsule Service（胶囊服务） per target;
- External Agent（代理） reports health per target;
- External Agent（代理） reports config metadata per target;
- External Agent（代理） reports action definitions per target;
- External Agent（代理） polls Commands;
- External Agent（代理） routes Commands to the correct target adapter;
- External Agent（代理） enforces action allowlists;
- External Agent（代理） reports CommandResults;
- one target failure does not crash all targets;
- Opstage（运维舞台） Backend outage is handled safely;
- raw tokens are not logged;
- raw secrets are not reported;
- no arbitrary shell execution is provided by default.

---

## 31. Summary

External Agent（代理） is a future Agent（代理） mode for governing explicitly configured services or runtimes from outside their processes.

It is valuable for legacy services, account/session managers, browser automation runtimes, and small local service fleets, but it carries broader security and operational risks than Embedded Agent（代理）.

The most important External Agent（代理） rule is:

> Govern only explicit targets through least-privilege adapters and predefined actions; never let External Agent（代理） become an unrestricted host controller or remote shell.
