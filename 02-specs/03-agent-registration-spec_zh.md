<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 03-agent-registration-spec.md
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

# Agent（代理） Registration 规范

- Status: 规范
- Edition: 共享
- Priority: 高
- Audience: backend developers, agent SDK developers, security reviewers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/openapi/opstage-ce-v0.1.yaml` disagree, the ADRs and OpenAPI contract win for CE（社区版） v0.1. The exact wire format is normative in OpenAPI; this document 解释 the rationale.

This document 定义 the **Agent（代理） Registration** specification for the `xtrape-capsule` domain.

Agent（代理） registration is the entry point for bringing Capsule Services under Opstage（运维舞台） governance.

Opstage（运维舞台） should only manage Capsule Services through registered and authorized Agents.

---

## 1. Purpose

The Agent（代理） Registration 规范 定义:

- how an Agent（代理） joins Opstage（运维舞台）;
- how a registration token is used;
- how an Agent（代理） token is issued;
- how Agent（代理） identity is established;
- how heartbeats are reported;
- how Agent（代理） online/offline status is calculated;
- how Capsule Services are reported by Agents;
- how commands are delivered to Agents;
- how Agent（代理） authorization and revocation should work;
- what CE（社区版） v0.1 must implement;
- what EE（企业版） and Cloud（云版） may extend in the future.

---

## 2. Core Rule

Opstage（运维舞台） must not directly manage arbitrary services.

A Capsule Service（胶囊服务） becomes governable only through a registered and authorized Agent（代理）.

The core model is:

```text
Capsule Service
    ↓
Agent
    ↓
Opstage Backend
    ↓
Opstage UI
```

CE（社区版） v0.1 implements:

```text
Node.js Capsule Service
    ↓ embedded Node.js Agent SDK
Opstage Backend
```

---

## 3. Agent（代理） Registration Model

Agent（代理） registration has two phases:

1. **Enrollment** using a Registration Token.
2. **Ongoing communication** using an Agent（代理） Token.

```text
Admin creates registration token
    ↓
Agent starts with registration token
    ↓
Agent calls Backend register API
    ↓
Backend validates token
    ↓
Backend creates or updates Agent identity
    ↓
Backend returns Agent token
    ↓
Agent uses Agent token for heartbeat, service report, command polling, and result reporting
```

---

## 4. Token Types

### 4.1 Registration Token

A **Registration Token** is used for first-time Agent（代理） enrollment.

Properties:

- short-lived or one-time use;
- created by an admin or setup flow;
- used only for `/agents/register`;
- exchanged for an Agent（代理） Token;
- should be marked as used after successful registration;
- should be revocable;
- should not be stored as plain text.

Recommended prefix for display or generated value:

```text
opstage_reg_
```

Example:

```text
opstage_reg_xxxxxxxxxxxxxxxxx
```

### 4.2 Agent（代理） Token

An **Agent（代理） Token** is used for ongoing authenticated Agent（代理） communication.

Properties:

- issued after successful registration;
- longer-lived than registration token;
- used for heartbeat, service reports, command polling, and command result reporting;
- revocable;
- rotatable in future versions;
- must be stored as a hash in Backend database.

Recommended prefix:

```text
opstage_agent_
```

Example:

```text
opstage_agent_xxxxxxxxxxxxxxxxx
```

### 4.3 Storage Rule

Raw tokens must not be stored in the database.

Backend should store:

```text
tokenHash
```

not:

```text
token
```

---

## 5. Registration Token Creation

CE（社区版） v0.1 should provide at least one way to create a registration token.

Possible approaches:

1. Admin UI creates a token.
2. Initial setup script creates a token.
3. Backend CLI creates a token.

CE（社区版） v0.1 may choose the simplest approach.

Recommended token metadata:

```text
id
workspaceId
tokenHash
type = registration
status
name
expiresAt
createdAt
usedAt
revokedAt
```

Recommended token statuses:

```text
ACTIVE
USED
REVOKED
EXPIRED
```

---

## 6. Agent（代理） Identity

An Agent（代理） must have a stable identity after registration.

CE（社区版） v0.1 Agent（代理） fields (must match Prisma `Agent` and OpenAPI `Agent`):

```text
id              agt_xxx
workspaceId     wks_xxx (default Workspace in CE v0.1)
code            stable kebab-case identifier
name            human-readable name (nullable)
mode            embedded | sidecar | external (CE v0.1: embedded only)
runtime         nodejs | java | python | go | other (CE v0.1: nodejs)
status          PENDING | ONLINE | OFFLINE | DISABLED | REVOKED
lastHeartbeatAt datetime nullable
disabledAt      datetime nullable
revokedAt       datetime nullable
createdAt       datetime
updatedAt       datetime
```

EE（企业版）/Cloud（云版） may extend Agent（代理） with `version`, `hostname`, `os`, `arch`, `registeredAt`, and `metadataJson` later. CE（社区版） v0.1 does NOT persist these; if an Agent（代理） reports them at registration, Backend may log them but should not require them.

### 6.1 `code`

Stable technical identifier of the Agent（代理）.

Rules:

- lowercase;
- kebab-case;
- unique within one Workspace;
- stable across restarts;
- should not include random runtime suffixes.

Examples:

```text
local-dev-agent
home-server-agent-01
capi-node-agent
```

### 6.2 `name`

Human-readable Agent（代理） name.

### 6.3 `mode`

Agent（代理） mode.

Allowed values:

```text
embedded
sidecar
external
```

CE（社区版） v0.1 implements only:

```text
embedded
```

### 6.4 `runtime`

Agent（代理） runtime.

Recommended values:

```text
nodejs
java
python
go
other
```

CE（社区版） v0.1 implements:

```text
nodejs
```

---

## 7. Register API

### 7.1 Endpoint

```http
POST /api/agents/register
```

This endpoint is called by the Agent（代理） using a Registration Token.

### 7.2 Request (matches OpenAPI `RegisterAgentRequest`)

```json
{
  "registrationToken": "opstage_reg_xxxxxxxxx",
  "agent": {
    "code": "local-dev-agent",
    "name": "Local Development Agent",
    "mode": "embedded",
    "runtime": "nodejs"
  },
  "service": {
    "code": "demo-capsule-service",
    "name": "Demo Capsule Service",
    "version": "0.1.0",
    "runtime": "nodejs",
    "manifest": {
      "kind": "CapsuleService",
      "code": "demo-capsule-service",
      "name": "Demo Capsule Service",
      "version": "0.1.0",
      "runtime": "nodejs",
      "agentMode": "embedded"
    }
  }
}
```

`service` is optional at registration time but recommended for CE（社区版） v0.1 embedded Agent（代理）. When provided, the `service` object must be a valid `ReportedService` (see §10.2).

The Agent（代理） MAY include additional informational fields such as `version`, `hostname`, `os`, `arch` in the request body; Backend ignores unknown fields in CE（社区版） v0.1 (forward-compat).

### 7.3 Response (envelope omitted; matches OpenAPI `RegisterAgentResponse`)

```json
{
  "agentId": "agt_V1StGXR8...",
  "agentToken": "opstage_agent_xxxxxxxxx",
  "heartbeatIntervalSeconds": 30,
  "commandPollIntervalSeconds": 5
}
```

The raw `agentToken` is shown only once. CE（社区版） v0.1 does NOT include `workspaceId` in the response (single default Workspace).

### 7.4 Backend Responsibilities

Backend must:

1. validate registration token;
2. verify token is active and not expired;
3. mark registration token as used if it is one-time;
4. create or update Agent（代理） record;
5. issue Agent（代理） token;
6. store only Agent（代理） token hash;
7. optionally upsert reported Capsule Service（胶囊服务） manifest;
8. write AuditEvent;
9. return Agent（代理） communication settings.

---

## 8. Re-registration

Agents may restart and need to re-register if they do not have a valid Agent（代理） Token.

CE（社区版） v0.1 rules:

- if Agent（代理） already has a valid Agent（代理） Token, it should use the token directly;
- if Agent（代理） token is missing, invalid, or revoked, Agent（代理） must use a new registration token;
- one-time registration tokens cannot be reused after successful registration;
- duplicate Agent（代理） `code` should update the existing Agent（代理） only if the registration token is valid and the backend policy allows it.

Future EE（企业版）/Cloud（云版） may define stricter enrollment policies.

---

## 9. Heartbeat API

### 9.1 Endpoint

```http
POST /api/agents/{agentId}/heartbeat
Authorization: Bearer <agentToken>
```

### 9.2 Request (matches OpenAPI `AgentHeartbeatRequest`)

```json
{
  "serviceId": "svc_001",
  "health": {
    "status": "UP",
    "message": "Demo service is healthy.",
    "details": {}
  }
}
```

Both `serviceId` and `health` are optional. A heartbeat with an empty body `{}` is valid and only updates `Agent.lastHeartbeatAt`.

CE（社区版） v0.1 也会把成功的 command polling（`GET /api/agents/{agentId}/commands`）视为轻量 heartbeat：它会更新 `Agent.lastHeartbeatAt` 并把 Agent（代理）置为 `ONLINE`。如果 Agent（代理）已经高频轮询 commands，除非需要通过 heartbeat endpoint 上报单个 service health，否则不需要单独 heartbeat loop。

A heartbeat reports health for at most one service per call. Multi-service Agents should send one heartbeat per service or rely on the dedicated `POST /api/agents/{agentId}/services/report` endpoint.

### 9.3 Response (envelope omitted; matches OpenAPI `AgentHeartbeatResponse`)

```json
{
  "heartbeatIntervalSeconds": 30,
  "commandPollIntervalSeconds": 5
}
```

Backend may use this to dynamically adjust the Agent（代理）'s polling cadence in future versions.

### 9.4 Backend Responsibilities

Backend must:

1. authenticate Agent（代理） token;
2. verify Agent（代理） is not revoked or disabled;
3. update `Agent.lastHeartbeatAt`;
4. transition `Agent.status` from `OFFLINE` or `PENDING` to `ONLINE` if needed;
5. if `health` is provided, create a `HealthReport` row and update `CapsuleService.lastHealthAt` + `healthStatus`;
6. recalculate `CapsuleService.status` (effective) for the affected service.

---

## 10. Service Report API

Agents should report Capsule Service（胶囊服务） metadata to Backend.

### 10.1 Endpoint

```http
POST /api/agents/{agentId}/services/report
Authorization: Bearer <agentToken>
```

### 10.2 Request (matches OpenAPI `ServiceReportRequest` / `ReportedService`)

```json
{
  "services": [
    {
      "code": "demo-capsule-service",
      "name": "Demo Capsule Service",
      "description": "Demo service for Opstage CE v0.1.",
      "version": "0.1.0",
      "runtime": "nodejs",
      "manifest": {
        "kind": "CapsuleService",
        "code": "demo-capsule-service",
        "name": "Demo Capsule Service",
        "version": "0.1.0",
        "runtime": "nodejs",
        "agentMode": "embedded",
        "capabilities": ["demo.echo"]
      },
      "health": {
        "status": "UP",
        "message": "Service is healthy."
      },
      "configs": [
        {
          "key": "demo.message",
          "label": "Demo Message",
          "type": "string",
          "editable": false,
          "sensitive": false,
          "valuePreview": "hello capsule",
          "source": "env"
        }
      ],
      "actions": [
        {
          "name": "runHealthCheck",
          "label": "Run Health Check",
          "dangerLevel": "LOW",
          "requiresConfirmation": false
        }
      ]
    }
  ]
}
```

`code` and `name` are sibling fields of `manifest` (not nested inside it). `health`, `configs`, and `actions` are optional but recommended.

对于 CE（社区版）规模部署，Agent（代理） SHOULD 避免反复上传未变化的 manifest/actions/configs。推荐模式是：启动时以及 manifest/actions/config 定义变化时发送完整 service report；稳定运行期间，通过 `POST /api/agents/{agentId}/heartbeat` 携带 `serviceId` 和 `health` 上报 service health。

### 10.3 Backend Responsibilities

Backend must:

1. authenticate Agent（代理） token;
2. validate manifest required fields (`kind`, `code`, `name`, `version`, `runtime`, `agentMode`);
3. upsert `CapsuleService` by `(workspaceId, code)` (matches Prisma `@@unique([workspaceId, code])`);
4. associate the service with the calling Agent（代理） (set `agentId`);
5. store the full manifest as `manifestJson`;
6. extract `description`, `version`, `runtime` for display columns;
7. update `lastReportedAt`;
8. if `health` is provided, create a `HealthReport` row and update `lastHealthAt` + `healthStatus`;
9. upsert `ConfigItem` rows by `(serviceId, configKey)`;
10. upsert `ActionDefinition` rows by `(serviceId, name)`;
11. recalculate `CapsuleService.status` (effective);
12. write an AuditEvent only when the service is newly registered or its manifest version changes (do NOT audit every identical re-report).

---

## 11. Command Polling API

CE（社区版） v0.1 should use polling for command delivery.

### 11.1 Endpoint

```http
GET /api/agents/{agentId}/commands
Authorization: Bearer <agentToken>
```

### 11.2 Response (matches OpenAPI: `SuccessEnvelope` with `data: Command[]`)

```json
{
  "success": true,
  "data": [
    {
      "id": "cmd_001",
      "agentId": "agt_001",
      "serviceId": "svc_001",
      "type": "ACTION",
      "actionName": "runHealthCheck",
      "payload": {},
      "status": "RUNNING",
      "createdAt": "2026-04-30T10:22:00Z",
      "startedAt": "2026-04-30T10:22:01Z",
      "expiresAt": "2026-04-30T10:27:00Z"
    }
  ]
}
```

### 11.3 Backend Responsibilities

Backend must:

1. authenticate Agent（代理） token;
2. reject if Agent（代理） is `DISABLED` or `REVOKED`;
3. return only `PENDING` Commands assigned to the calling Agent（代理）;
4. exclude commands where `now > expiresAt` (and mark them `EXPIRED` opportunistically);
5. transition each returned Command from `PENDING` to `RUNNING` and set `startedAt`;
6. order results by `createdAt ASC`.

---

## 12. Command Result API

### 12.1 Endpoint

```http
POST /api/agents/{agentId}/commands/{commandId}/result
Authorization: Bearer <agentToken>
```

### 12.2 Request (matches OpenAPI `ReportCommandResultRequest`)

Successful result:

```json
{
  "success": true,
  "message": "Health check completed.",
  "data": {
    "status": "UP",
    "details": {}
  }
}
```

Failed result:

```json
{
  "success": false,
  "message": "Action not found: refreshSession",
  "error": {
    "code": "ACTION_NOT_FOUND",
    "message": "Action not found: refreshSession"
  }
}
```

### 12.3 Backend Responsibilities

Backend must:

1. authenticate Agent（代理） token;
2. verify the command belongs to the calling Agent（代理）;
3. reject if the Command is already in a terminal state (`SUCCEEDED` / `FAILED` / `EXPIRED` / `CANCELLED`);
4. create a `CommandResult` row (1:1 with Command);
5. transition Command: `RUNNING -> SUCCEEDED` (when `success = true`) or `RUNNING -> FAILED`;
6. set `Command.completedAt` to server clock;
7. write AuditEvent (`command.completed` or `command.failed`);
8. expose the result to UI.

---

## 13. Agent（代理） 状态 Model

CE（社区版） v0.1 Agent（代理） statuses (must match OpenAPI `AgentStatus`):

```text
PENDING
ONLINE
OFFLINE
DISABLED
REVOKED
```

`REGISTERED` and `ERROR` are reserved for future EE（企业版）/Cloud（云版） editions.

### 13.1 `PENDING`

Agent（代理） record exists but Agent（代理） has not yet sent a successful heartbeat.

### 13.2 `ONLINE`

Agent（代理） has sent a valid heartbeat within the offline threshold.

### 13.3 `OFFLINE`

Agent（代理） has not sent a heartbeat within the offline threshold (default 90s).

### 13.4 `DISABLED`

Agent（代理） is disabled by an admin. May be re-enabled.

### 13.5 `REVOKED`

Agent（代理） token is revoked. Communication must be rejected.

---

## 14. Heartbeat Timeout and Offline Calculation

CE（社区版） v0.1 recommended defaults:

```text
heartbeatIntervalSeconds = 30
offlineThresholdSeconds = 90
```

Rule:

```text
if now - lastHeartbeatAt > offlineThresholdSeconds:
    Agent effective status = OFFLINE
```

If an Agent（代理） becomes offline, all services managed only by that Agent（代理） should become `STALE` or `UNKNOWN`, not confidently `HEALTHY`.

Recommended service status behavior (CE（社区版） v0.1, see `02-specs/09-status-model-spec.md`):

```text
Agent ONLINE  + health UP       -> CapsuleService.status = HEALTHY
Agent ONLINE  + health DEGRADED -> CapsuleService.status = UNHEALTHY
Agent ONLINE  + health DOWN     -> CapsuleService.status = OFFLINE
Agent ONLINE  + health UNKNOWN  -> CapsuleService.status = UNKNOWN
Agent OFFLINE | DISABLED | REVOKED -> CapsuleService.status = STALE
```

---

## 15. Capsule Service（胶囊服务） 状态 Interaction

Agent（代理） status and Capsule Service（胶囊服务） status must be separate.

Examples:

```text
Agent ONLINE, Service HEALTHY
Agent ONLINE, Service UNHEALTHY
Agent ONLINE, Service OFFLINE
Agent OFFLINE, Service STALE
Agent REVOKED, Service STALE
```

UI should make this distinction visible.

Bad UI behavior:

```text
Service shows green HEALTHY even though Agent has been offline for hours.
```

Correct UI behavior:

```text
Current: STALE
Last health: UP   (latest HealthReport)
Last reported at: 2026-04-30 10:21
Reason: Agent offline since 10:22
```

---

## 16. Agent（代理） 授权

CE（社区版） v0.1 may implement simple Agent（代理） authorization:

- valid Agent（代理） token required;
- Agent（代理） must not be disabled;
- Agent（代理） must not be revoked;
- Agent（代理） can only access its own commands;
- Agent（代理） can only report services associated with itself or allowed by Backend policy.

Future EE（企业版）/Cloud（云版） may add:

- workspace-scoped Agent（代理） permissions;
- environment restrictions;
- allowed service code patterns;
- allowed action types;
- approval policies;
- IP restrictions;
- device attestation.

---

## 17. Revocation

An Agent（代理） token may be revoked.

After revocation:

- heartbeat must be rejected;
- service report must be rejected;
- command polling must be rejected;
- command result reporting must be rejected unless policy allows late result submission;
- Agent（代理） status should become `REVOKED`;
- related services should become `STALE` or `DISABLED` depending on policy.

CE（社区版） v0.1 should support revoking Agent（代理） tokens from Backend data model, even if UI support is minimal.

---

## 18. Disablement

An Agent（代理） may be disabled by an admin.

Disabled Agent（代理） behavior:

- token may still exist but communication is rejected;
- no new commands should be delivered;
- UI should show Agent（代理） as `DISABLED`;
- services should show degraded governability.

Difference between disabled and revoked:

||State|Meaning||
|---|---|
||DISABLED|administrative switch; may be re-enabled||
||REVOKED|token trust removed; requires new enrollment or token rotation||

---

## 19. Audit Events

Agent（代理） registration and communication should create audit events.

Recommended events:

```text
agent.registrationToken.created
agent.registered
agent.heartbeat.received
agent.service.reported
agent.disabled
agent.enabled
agent.revoked
agent.command.polled
agent.command.resultReported
```

CE（社区版） v0.1 minimum audit events:

```text
agent.registered
agent.service.reported
command.created
command.completed
```

---

## 20. Error Model

Agent（代理） APIs should return structured errors.

Recommended shape:

```json
{
  "success": false,
  "error": {
    "code": "AGENT_TOKEN_INVALID",
    "message": "Agent token is invalid.",
    "details": {}
  }
}
```

Recommended error codes:

```text
REGISTRATION_TOKEN_INVALID
REGISTRATION_TOKEN_EXPIRED
REGISTRATION_TOKEN_USED
AGENT_TOKEN_INVALID
AGENT_TOKEN_REVOKED
AGENT_DISABLED
AGENT_NOT_FOUND
SERVICE_MANIFEST_INVALID
COMMAND_NOT_FOUND
COMMAND_NOT_ASSIGNED_TO_AGENT
COMMAND_EXPIRED
INTERNAL_ERROR
```

---

## 21. CE（社区版） v0.1 Required Subset

CE（社区版） v0.1 must implement:

- registration token model;
- Agent（代理） registration API;
- Agent（代理） token issuance;
- token hash storage;
- heartbeat API;
- service report API;
- command polling API;
- command result API;
- basic Agent（代理） status calculation;
- basic service stale calculation;
- basic audit events.

CE（社区版） v0.1 does not need to implement:

- WebSocket Agent（代理） channel;
- gRPC streaming;
- message queue command delivery;
- Agent（代理） token rotation UI;
- full Agent（代理） permission policy engine;
- device attestation;
- multi-tenant enrollment;
- sidecar or external Agent（代理） runtime.

---

## 22. 安全 Rules

### 22.1 Never store raw tokens

Store only token hashes.

### 22.2 Use HTTPS in production

For self-hosted local development, HTTP may be acceptable.

For production or Cloud（云版）, Agent（代理） communication must use HTTPS or equivalent secure transport.

### 22.3 Reject revoked or disabled Agents

Backend must reject requests from revoked or disabled Agents.

### 22.4 Do not expose Agent（代理） token to UI after creation

Agent（代理） token should be shown only once if generated by Backend.

### 22.5 Scope future permissions

Even if CE（社区版） v0.1 uses simple authorization, data model should allow future Agent（代理） permission scopes.

---

## 23. Compatibility Rules

- New optional fields may be added to Agent（代理） registration payloads.
- Older Backends may ignore unknown fields.
- Stable fields such as `agent.code`, `agent.mode`, `agent.runtime`, and `agent.version` should not change meaning.
- CE（社区版） may implement only embedded mode, but the model must preserve `mode` for future sidecar and external Agents.
- Cloud（云版） may add tenant and organization context later without changing the CE（社区版） registration core.

---

## 24. Anti-Patterns

Avoid these patterns.

### 24.1 Backend directly scanning services

Do not make Backend discover and manage random services directly.

### 24.2 Long-lived registration token reused forever

Registration token should not become a permanent Agent（代理） credential.

### 24.3 Raw token storage

Do not store raw registration tokens or Agent（代理） tokens.

### 24.4 Service status without Agent（代理） status

Do not show service status without considering Agent（代理） heartbeat freshness.

### 24.5 Command delivery to disabled Agent（代理）

Do not deliver new commands to disabled or revoked Agents.

### 24.6 Cloud（云版）-only enrollment in CE（社区版）

Do not require tenant, billing, or Cloud（云版） organization concepts for CE（社区版） v0.1 registration.

---

## 25. Summary

Agent（代理） registration is the trust entry point of `xtrape-capsule` governance.

CE（社区版） v0.1 should implement a simple but secure registration loop:

```text
Registration Token
    ↓
Agent Registration
    ↓
Agent Token
    ↓
Heartbeat
    ↓
Service Report
    ↓
Command Polling
    ↓
Command Result
```

This model keeps Opstage（运维舞台） separated from Capsule Services while allowing safe, auditable runtime governance.
