# Agent Registration Specification

- Status: Specification
- Edition: Shared
- Priority: High
- Audience: backend developers, agent SDK developers, security reviewers, AI coding agents

This document defines the **Agent Registration** specification for the `xtrape-capsule` domain.

Agent registration is the entry point for bringing Capsule Services under Opstage governance.

Opstage should only manage Capsule Services through registered and authorized Agents.

---

## 1. Purpose

The Agent Registration Specification defines:

- how an Agent joins Opstage;
- how a registration token is used;
- how an Agent token is issued;
- how Agent identity is established;
- how heartbeats are reported;
- how Agent online/offline status is calculated;
- how Capsule Services are reported by Agents;
- how commands are delivered to Agents;
- how Agent authorization and revocation should work;
- what CE v0.1 must implement;
- what EE and Cloud may extend in the future.

---

## 2. Core Rule

Opstage must not directly manage arbitrary services.

A Capsule Service becomes governable only through a registered and authorized Agent.

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

CE v0.1 implements:

```text
Node.js Capsule Service
    ↓ embedded Node.js Agent SDK
Opstage Backend
```

---

## 3. Agent Registration Model

Agent registration has two phases:

1. **Enrollment** using a Registration Token.
2. **Ongoing communication** using an Agent Token.

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

A **Registration Token** is used for first-time Agent enrollment.

Properties:

- short-lived or one-time use;
- created by an admin or setup flow;
- used only for `/agents/register`;
- exchanged for an Agent Token;
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

### 4.2 Agent Token

An **Agent Token** is used for ongoing authenticated Agent communication.

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

CE v0.1 should provide at least one way to create a registration token.

Possible approaches:

1. Admin UI creates a token.
2. Initial setup script creates a token.
3. Backend CLI creates a token.

CE v0.1 may choose the simplest approach.

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

## 6. Agent Identity

An Agent must have a stable identity after registration.

Recommended Agent fields:

```text
id
workspaceId
code
name
mode
runtime
version
status
hostname
os
arch
lastHeartbeatAt
registeredAt
disabledAt
createdAt
updatedAt
```

### 6.1 `code`

Stable technical identifier of the Agent.

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

Human-readable Agent name.

### 6.3 `mode`

Agent mode.

Allowed values:

```text
embedded
sidecar
external
```

CE v0.1 implements only:

```text
embedded
```

### 6.4 `runtime`

Agent runtime.

Recommended values:

```text
nodejs
java
python
go
other
```

CE v0.1 implements:

```text
nodejs
```

---

## 7. Register API

### 7.1 Endpoint

```http
POST /api/agents/register
```

This endpoint is called by the Agent using a Registration Token.

### 7.2 Request

```json
{
  "registrationToken": "opstage_reg_xxxxxxxxx",
  "agent": {
    "code": "local-dev-agent",
    "name": "Local Development Agent",
    "mode": "embedded",
    "runtime": "nodejs",
    "version": "0.1.0",
    "hostname": "dev-machine",
    "os": "darwin",
    "arch": "arm64"
  },
  "service": {
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

`service` is optional at registration time but recommended for CE v0.1 embedded Agent.

### 7.3 Response

```json
{
  "agentId": "agt_001",
  "agentToken": "opstage_agent_xxxxxxxxx",
  "workspaceId": "wks_default",
  "heartbeatIntervalSeconds": 30,
  "commandPollingIntervalSeconds": 5
}
```

### 7.4 Backend Responsibilities

Backend must:

1. validate registration token;
2. verify token is active and not expired;
3. mark registration token as used if it is one-time;
4. create or update Agent record;
5. issue Agent token;
6. store only Agent token hash;
7. optionally upsert reported Capsule Service manifest;
8. write AuditEvent;
9. return Agent communication settings.

---

## 8. Re-registration

Agents may restart and need to re-register if they do not have a valid Agent Token.

CE v0.1 rules:

- if Agent already has a valid Agent Token, it should use the token directly;
- if Agent token is missing, invalid, or revoked, Agent must use a new registration token;
- one-time registration tokens cannot be reused after successful registration;
- duplicate Agent `code` should update the existing Agent only if the registration token is valid and the backend policy allows it.

Future EE/Cloud may define stricter enrollment policies.

---

## 9. Heartbeat API

### 9.1 Endpoint

```http
POST /api/agents/{agentId}/heartbeat
Authorization: Bearer <agentToken>
```

### 9.2 Request

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
        "details": {}
      }
    }
  ]
}
```

### 9.3 Response

```json
{
  "accepted": true,
  "serverTime": "2026-04-30T10:21:01Z",
  "nextHeartbeatIntervalSeconds": 30
}
```

### 9.4 Backend Responsibilities

Backend must:

1. authenticate Agent Token;
2. verify Agent is not revoked or disabled;
3. update `lastHeartbeatAt`;
4. update Agent status to `ONLINE`;
5. update reported service statuses if provided;
6. store latest health report if provided;
7. calculate effective service status if needed.

---

## 10. Service Report API

Agents should report Capsule Service metadata to Backend.

### 10.1 Endpoint

```http
POST /api/agents/{agentId}/services/report
Authorization: Bearer <agentToken>
```

### 10.2 Request

```json
{
  "services": [
    {
      "manifest": {
        "kind": "CapsuleService",
        "code": "demo-capsule-service",
        "name": "Demo Capsule Service",
        "version": "0.1.0",
        "runtime": "nodejs",
        "agentMode": "embedded",
        "capabilities": ["demo.echo"],
        "actions": [
          {
            "name": "runHealthCheck",
            "label": "Run Health Check",
            "dangerLevel": "LOW",
            "enabled": true
          }
        ],
        "configs": []
      },
      "reportedStatus": "ONLINE"
    }
  ]
}
```

### 10.3 Backend Responsibilities

Backend must:

1. authenticate Agent Token;
2. validate manifest required fields;
3. upsert CapsuleService by `workspaceId + code`;
4. associate CapsuleService with Agent;
5. store `manifestJson`;
6. extract display fields;
7. update `lastReportedAt`;
8. update `reportedStatus` and `effectiveStatus`;
9. write AuditEvent if service is newly registered or materially changed.

---

## 11. Command Polling API

CE v0.1 should use polling for command delivery.

### 11.1 Endpoint

```http
GET /api/agents/{agentId}/commands
Authorization: Bearer <agentToken>
```

### 11.2 Response

```json
{
  "commands": [
    {
      "commandId": "cmd_001",
      "serviceCode": "demo-capsule-service",
      "serviceId": "svc_001",
      "commandType": "ACTION",
      "actionName": "runHealthCheck",
      "payload": {},
      "issuedAt": "2026-04-30T10:22:00Z",
      "expiresAt": "2026-04-30T10:27:00Z"
    }
  ]
}
```

### 11.3 Backend Responsibilities

Backend must:

1. authenticate Agent Token;
2. return pending commands for that Agent;
3. exclude expired commands;
4. mark returned commands as `DISPATCHED` if appropriate;
5. avoid sending commands to revoked or disabled Agents.

---

## 12. Command Result API

### 12.1 Endpoint

```http
POST /api/agents/{agentId}/commands/{commandId}/result
Authorization: Bearer <agentToken>
```

### 12.2 Request

```json
{
  "status": "SUCCESS",
  "outputText": "Health check completed.",
  "resultJson": {
    "status": "UP",
    "details": {}
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
    "errorCode": "ACTION_NOT_FOUND"
  },
  "startedAt": "2026-04-30T10:22:01Z",
  "finishedAt": "2026-04-30T10:22:02Z"
}
```

### 12.3 Backend Responsibilities

Backend must:

1. authenticate Agent Token;
2. verify the command belongs to the Agent;
3. update Command status;
4. create or update CommandResult;
5. write AuditEvent;
6. expose the result to UI.

---

## 13. Agent Status Model

Recommended Agent statuses:

```text
PENDING
REGISTERED
ONLINE
OFFLINE
DISABLED
REVOKED
ERROR
```

CE v0.1 may implement:

```text
PENDING
ONLINE
OFFLINE
DISABLED
REVOKED
```

### 13.1 `PENDING`

Agent registration token was created, but Agent has not successfully registered.

### 13.2 `ONLINE`

Agent has sent a valid heartbeat recently.

### 13.3 `OFFLINE`

Agent has not sent heartbeat within the offline threshold.

### 13.4 `DISABLED`

Agent is disabled by an admin.

### 13.5 `REVOKED`

Agent token is revoked. Communication must be rejected.

### 13.6 `ERROR`

Agent reported an internal error or Backend detected inconsistent state.

---

## 14. Heartbeat Timeout and Offline Calculation

CE v0.1 recommended defaults:

```text
heartbeatIntervalSeconds = 30
offlineThresholdSeconds = 90
```

Rule:

```text
if now - lastHeartbeatAt > offlineThresholdSeconds:
    Agent effective status = OFFLINE
```

If an Agent becomes offline, all services managed only by that Agent should become `STALE` or `UNKNOWN`, not confidently `ONLINE`.

Recommended service status behavior:

```text
Agent ONLINE + service health UP       -> service ONLINE
Agent ONLINE + service health DOWN     -> service UNHEALTHY or OFFLINE
Agent OFFLINE + last service ONLINE    -> service STALE
Agent REVOKED/DISABLED                 -> service STALE or DISABLED depending on policy
```

---

## 15. Capsule Service Status Interaction

Agent status and Capsule Service status must be separate.

Examples:

```text
Agent ONLINE, Service ONLINE
Agent ONLINE, Service UNHEALTHY
Agent ONLINE, Service OFFLINE
Agent OFFLINE, Service STALE
Agent REVOKED, Service STALE
```

UI should make this distinction visible.

Bad UI behavior:

```text
Service shows green ONLINE even though Agent has been offline for hours.
```

Correct UI behavior:

```text
Last reported: ONLINE
Current: STALE
Reason: Agent offline since 10:21
```

---

## 16. Agent Authorization

CE v0.1 may implement simple Agent authorization:

- valid Agent token required;
- Agent must not be disabled;
- Agent must not be revoked;
- Agent can only access its own commands;
- Agent can only report services associated with itself or allowed by Backend policy.

Future EE/Cloud may add:

- workspace-scoped Agent permissions;
- environment restrictions;
- allowed service code patterns;
- allowed action types;
- approval policies;
- IP restrictions;
- device attestation.

---

## 17. Revocation

An Agent token may be revoked.

After revocation:

- heartbeat must be rejected;
- service report must be rejected;
- command polling must be rejected;
- command result reporting must be rejected unless policy allows late result submission;
- Agent status should become `REVOKED`;
- related services should become `STALE` or `DISABLED` depending on policy.

CE v0.1 should support revoking Agent tokens from Backend data model, even if UI support is minimal.

---

## 18. Disablement

An Agent may be disabled by an admin.

Disabled Agent behavior:

- token may still exist but communication is rejected;
- no new commands should be delivered;
- UI should show Agent as `DISABLED`;
- services should show degraded governability.

Difference between disabled and revoked:

| State | Meaning |
|---|---|
| DISABLED | administrative switch; may be re-enabled |
| REVOKED | token trust removed; requires new enrollment or token rotation |

---

## 19. Audit Events

Agent registration and communication should create audit events.

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

CE v0.1 minimum audit events:

```text
agent.registered
agent.service.reported
command.created
command.completed
```

---

## 20. Error Model

Agent APIs should return structured errors.

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

## 21. CE v0.1 Required Subset

CE v0.1 must implement:

- registration token model;
- Agent registration API;
- Agent token issuance;
- token hash storage;
- heartbeat API;
- service report API;
- command polling API;
- command result API;
- basic Agent status calculation;
- basic service stale calculation;
- basic audit events.

CE v0.1 does not need to implement:

- WebSocket Agent channel;
- gRPC streaming;
- message queue command delivery;
- Agent token rotation UI;
- full Agent permission policy engine;
- device attestation;
- multi-tenant enrollment;
- sidecar or external Agent runtime.

---

## 22. Security Rules

### 22.1 Never store raw tokens

Store only token hashes.

### 22.2 Use HTTPS in production

For self-hosted local development, HTTP may be acceptable.

For production or Cloud, Agent communication must use HTTPS or equivalent secure transport.

### 22.3 Reject revoked or disabled Agents

Backend must reject requests from revoked or disabled Agents.

### 22.4 Do not expose Agent token to UI after creation

Agent token should be shown only once if generated by Backend.

### 22.5 Scope future permissions

Even if CE v0.1 uses simple authorization, data model should allow future Agent permission scopes.

---

## 23. Compatibility Rules

- New optional fields may be added to Agent registration payloads.
- Older Backends may ignore unknown fields.
- Stable fields such as `agent.code`, `agent.mode`, `agent.runtime`, and `agent.version` should not change meaning.
- CE may implement only embedded mode, but the model must preserve `mode` for future sidecar and external Agents.
- Cloud may add tenant and organization context later without changing the CE registration core.

---

## 24. Anti-Patterns

Avoid these patterns.

### 24.1 Backend directly scanning services

Do not make Backend discover and manage random services directly.

### 24.2 Long-lived registration token reused forever

Registration token should not become a permanent Agent credential.

### 24.3 Raw token storage

Do not store raw registration tokens or Agent tokens.

### 24.4 Service status without Agent status

Do not show service status without considering Agent heartbeat freshness.

### 24.5 Command delivery to disabled Agent

Do not deliver new commands to disabled or revoked Agents.

### 24.6 Cloud-only enrollment in CE

Do not require tenant, billing, or Cloud organization concepts for CE v0.1 registration.

---

## 25. Summary

Agent registration is the trust entry point of `xtrape-capsule` governance.

CE v0.1 should implement a simple but secure registration loop:

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

This model keeps Opstage separated from Capsule Services while allowing safe, auditable runtime governance.
