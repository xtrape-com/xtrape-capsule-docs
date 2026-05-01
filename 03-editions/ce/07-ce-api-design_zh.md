<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 07-ce-api-design.md
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

# CE（社区版） API 设计

- Status: 实现 Target
- Edition: CE（社区版）
- Priority: Current
- Audience: architects, backend developers, frontend developers, agent SDK developers, AI coding agents

> **Precedence rule**: When this document and `09-contracts/openapi/opstage-ce-v0.1.yaml` disagree, the OpenAPI contract wins for CE（社区版） v0.1. Examples below are illustrative; the OpenAPI document is the normative wire format.

This document 定义 the API design for **Opstage（运维舞台） CE（社区版） v0.1**.

CE（社区版） APIs are divided into two surfaces:

```text
Admin APIs
Agent APIs
```

Admin APIs are used by Opstage（运维舞台） UI.

Agent（代理） APIs are used by registered Agents.

---

## 1. API 设计 Goal

The goal of the CE（社区版） API design is to support the minimum complete Capsule governance loop:

```text
Admin login
    ↓
Agent registration
    ↓
Agent heartbeat
    ↓
Capsule Service report
    ↓
UI service visibility
    ↓
Action request
    ↓
Command polling
    ↓
Command result reporting
    ↓
Audit log display
```

The API should be simple, JSON-based, easy to debug, and compatible with future EE（企业版） and Cloud（云版） extensions.

---

## 2. API Principles

CE（社区版） v0.1 APIs should follow these principles:

1. Use REST-style JSON APIs.
2. Keep Admin APIs and Agent（代理） APIs clearly separated.
3. Require UI authentication for Admin APIs.
4. Require Agent（代理） token authentication for Agent（代理） APIs after registration.
5. Do not let UI call Agents directly.
6. Do not expose arbitrary shell execution APIs.
7. Use stable resource names.
8. Use shared status values from the 状态 Model.
9. Return structured errors.
10. Keep paths stable enough for Agent（代理） SDK usage.
11. Allow additive future fields.
12. Avoid EE（企业版）/Cloud（云版）-only requirements in CE（社区版） v0.1.

---

## 3. API Surface 概述

### 3.1 Admin APIs

Admin APIs are called by Opstage（运维舞台） UI.

They provide:

- authentication;
- dashboard data;
- Agent（代理） list and detail;
- Capsule Service（胶囊服务） list and detail;
- action request;
- Command list and detail;
- Audit Event list and detail;
- system setup and settings.

Base path:

```text
/api/admin
```

### 3.2 Agent（代理） APIs

Agent（代理） APIs are called by Agents.

They provide:

- Agent（代理） registration;
- heartbeat;
- service report;
- command polling;
- command result reporting.

Base path:

```text
/api/agents
```

---

## 4. 认证

### 4.1 Admin API authentication

Admin APIs require a logged-in user.

Recommended CE（社区版） v0.1 options:

```text
HTTP-only session cookie
```

or:

```text
JWT bearer token
```

Preferred direction:

```text
HTTP-only session cookie
```

because the primary Admin API consumer is the browser UI.

JWT is acceptable if it simplifies implementation.

### 4.2 Agent（代理） API authentication

Agent（代理） APIs after registration require Agent（代理） token:

```http
Authorization: Bearer <agentToken>
```

Backend must validate:

- token hash;
- token status;
- Agent（代理） status;
- revoked/disabled state.

### 4.3 Registration endpoint authentication

Agent（代理） registration uses a registration token in request body.

```http
POST /api/agents/register
```

This endpoint does not use Agent（代理） token because the Agent（代理） is not registered yet.

---

## 5. Common Response Shape

CE（社区版） v0.1 may use a simple response shape.

### 5.1 Success response

```json
{
  "success": true,
  "data": {}
}
```

### 5.2 Error response

```json
{
  "success": false,
  "error": {
    "code": "AGENT_NOT_FOUND",
    "message": "Agent not found.",
    "details": {}
  }
}
```

### 5.3 List response

CE（社区版） v0.1 list endpoints return the array directly under `data`, with a sibling `pagination` object (matches OpenAPI):

```json
{
  "success": true,
  "data": [
    { "id": "agt_001", "code": "local-dev-agent" }
  ],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "total": 1
  }
}
```

### 5.4 Notes

This shape is fixed by `09-contracts/openapi/opstage-ce-v0.1.yaml`. Do not nest list items as `data.items`; that pattern is no longer valid in CE（社区版） v0.1.

---

## 6. HTTP 状态 Codes

Recommended usage:

||HTTP 状态|Meaning||
|---|---|
||200|Successful query or operation||
||201|Resource created||
||400|Invalid request payload||
||401|Not authenticated or invalid token||
||403|Authenticated but not allowed||
||404|Resource not found||
||409|Conflict, duplicate, invalid state transition||
||422|Validation failed||
||500|Internal server error||
|||

CE（社区版） may keep status usage simple, but it should not return `200` for clear authentication or validation failures.

---

## 7. Pagination, Sorting, and Filtering

All list endpoints share a single convention. Backend MUST validate every query param with the Zod schema exported from `@xtrape/capsule-contracts-node` (the published npm package; see [ADR 0008](../../08-decisions/0008-naming-and-repositories.md)) before reaching the data layer; unknown params return `422 VALIDATION_FAILED`.

### 7.1 Pagination

```text
page=1            # >= 1, default 1
pageSize=20       # 1..100, default 20
```

Response body (always wrapped in `SuccessEnvelope`):

```json
{
  "data": [ /* items of type T */ ],
  "pagination": { "page": 1, "pageSize": 20, "total": 137 }
}
```

`total` is the total count after filtering (NOT after pagination).

### 7.2 Sorting

```text
sort=-createdAt           # single field, descending
sort=name,-updatedAt      # multi-field, applied left-to-right
```

Allowed sort fields per endpoint (CE（社区版） v0.1):

||Endpoint|Allowed `sort` fields||
|----------------------------------------|------------------------------------------------------------------|
||`GET /api/admin/agents`|`createdAt`, `lastSeenAt`, `name`||
||`GET /api/admin/capsule-services`|`createdAt`, `lastReportedAt`, `code`, `name`||
||`GET /api/admin/commands`|`createdAt`, `finishedAt`||
||`GET /api/admin/audit-events`|`createdAt`||
||`GET /api/admin/registration-tokens`|`createdAt`, `expiresAt`||

Default sort if none supplied: `-createdAt` (newest first) for every list endpoint above.

### 7.3 Filtering

Filters are individual query params named after the field they filter:

||Endpoint|Supported filters||
|----------------------------------------|------------------------------------------------------------------|
||`GET /api/admin/agents`|`status` (`AgentStatus`)||
||`GET /api/admin/capsule-services`|`status` (`CapsuleServiceStatus`), `agentId`||
||`GET /api/admin/commands`|`status` (`CommandStatus`), `serviceId`, `agentId`||
||`GET /api/admin/audit-events`|`actorType`, `targetType`, `targetId`, `result`, `from`, `to` (`from`/`to` apply to `createdAt`)||
||`GET /api/admin/registration-tokens`|`status` (`TokenStatus`)||

Multiple values for the same key (e.g. `status=PENDING&status=RUNNING`) are OR'ed; multiple keys are AND'ed. `from`/`to` are ISO-8601 timestamps and apply to the endpoint's natural time field (`occurredAt` for audit, `createdAt` otherwise).

CE（社区版） v0.1 does NOT implement free-text search (`q=`); that is reserved for EE（企业版）.

### 7.4 Page size limits

```text
default pageSize = 20
max pageSize     = 100
```

Backend MUST clamp out-of-range values to `422 VALIDATION_FAILED` instead of silently coercing.

---

## 8. Time Format

Use ISO-8601 timestamps in API responses.

Example:

```text
2026-04-30T10:21:00Z
```

Backend may store timestamps in database format, but APIs should return ISO-compatible strings.

---

## 9. Admin APIs

### 9.1 Login

```http
POST /api/admin/auth/login
```

Request:

```json
{
  "username": "admin",
  "password": "<example-only>"
}
```

Response:

```json
{
  "success": true,
  "data": {
    "user": {
      "id": "usr_001",
      "username": "admin",
      "displayName": "Admin",
      "role": "owner"
    }
  }
}
```

Backend should create AuditEvent:

```text
user.login
```

Failed login should create:

```text
user.login.failed
```

### 9.2 Logout

```http
POST /api/admin/auth/logout
```

Response:

```json
{
  "success": true,
  "data": {}
}
```

### 9.3 Current user

```http
GET /api/admin/auth/me
```

Response:

```json
{
  "success": true,
  "data": {
    "id": "usr_001",
    "username": "admin",
    "displayName": "Admin",
    "role": "owner"
  }
}
```

---

## 10. Dashboard APIs

### 10.1 Dashboard summary

```http
GET /api/admin/dashboard/summary
```

Response:

```json
{
  "success": true,
  "data": {
    "agents": {
      "total": 2,
      "online": 1,
      "offline": 1
    },
    "services": {
      "total": 3,
      "online": 1,
      "unhealthy": 1,
      "stale": 1
    },
    "commands": {
      "recentTotal": 12,
      "failedRecent": 1
    },
    "auditEvents": {
      "recentTotal": 30
    }
  }
}
```

---

## 11. Agent（代理） Admin APIs

### 11.1 List Agents

```http
GET /api/admin/agents
```

Query parameters:

```text
page
pageSize
status
q
```

Response:

```json
{
  "success": true,
  "data": [
    {
      "id": "agt_001",
      "code": "local-dev-agent",
      "name": "Local Development Agent",
      "mode": "embedded",
      "runtime": "nodejs",
      "status": "ONLINE",
      "lastHeartbeatAt": "2026-04-30T10:21:00Z",
      "createdAt": "2026-04-30T10:00:00Z",
      "updatedAt": "2026-04-30T10:21:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "total": 1
  }
}
```

### 11.2 Get Agent（代理） detail

```http
GET /api/admin/agents/{agentId}
```

Response (matches OpenAPI `AgentDetail`):

```json
{
  "success": true,
  "data": {
    "id": "agt_001",
    "code": "local-dev-agent",
    "name": "Local Development Agent",
    "mode": "embedded",
    "runtime": "nodejs",
    "status": "ONLINE",
    "lastHeartbeatAt": "2026-04-30T10:21:00Z",
    "createdAt": "2026-04-30T10:00:00Z",
    "updatedAt": "2026-04-30T10:21:00Z",
    "services": [
      {
        "id": "svc_001",
        "agentId": "agt_001",
        "code": "demo-capsule-service",
        "name": "Demo Capsule Service",
        "status": "HEALTHY",
        "healthStatus": "UP"
      }
    ]
  }
}
```

### 11.3 Disable Agent（代理）

Optional for CE（社区版） v0.1 UI, but useful in data model.

```http
POST /api/admin/agents/{agentId}/disable
```

### 11.4 Re-enable Agent（代理）

Optional for CE（社区版） v0.1 UI.

```http
POST /api/admin/agents/{agentId}/enable
```

### 11.5 Revoke Agent（代理）

Optional for CE（社区版） v0.1 UI, but important for security.

```http
POST /api/admin/agents/{agentId}/revoke
```

---

## 12. Registration Token Admin APIs

CE（社区版） v0.1 needs a way to create registration tokens.

### 12.1 Create registration token

```http
POST /api/admin/registration-tokens
```

Request:

```json
{
  "name": "Demo token",
  "expiresInSeconds": 86400
}
```

Response:

```json
{
  "success": true,
  "data": {
    "id": "tok_001",
    "token": "opstage_reg_xxxxxxxxx",
    "expiresAt": "2026-05-01T10:00:00Z"
  }
}
```

安全 rule:

> The raw token should be shown only once and stored only as a hash.

### 12.2 List registration tokens

Optional for CE（社区版） v0.1.

```http
GET /api/admin/registration-tokens
```

### 12.3 Revoke registration token

Optional for CE（社区版） v0.1.

```http
POST /api/admin/registration-tokens/{tokenId}/revoke
```

---

## 13. Capsule Service（胶囊服务） Admin APIs

### 13.1 List Capsule Services

```http
GET /api/admin/capsule-services
```

Query parameters:

```text
page
pageSize
status
runtime
agentId
q
```

Response:

```json
{
  "success": true,
  "data": [
    {
      "id": "svc_001",
      "agentId": "agt_001",
      "code": "demo-capsule-service",
      "name": "Demo Capsule Service",
      "version": "0.1.0",
      "runtime": "nodejs",
      "status": "HEALTHY",
      "healthStatus": "UP",
      "lastReportedAt": "2026-04-30T10:21:00Z",
      "lastHealthAt": "2026-04-30T10:21:00Z",
      "createdAt": "2026-04-30T10:00:00Z",
      "updatedAt": "2026-04-30T10:21:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "total": 1
  }
}
```

### 13.2 Get Capsule Service（胶囊服务） detail

```http
GET /api/admin/capsule-services/{serviceId}
```

Response (matches OpenAPI `CapsuleServiceDetail`):

```json
{
  "success": true,
  "data": {
    "id": "svc_001",
    "agentId": "agt_001",
    "code": "demo-capsule-service",
    "name": "Demo Capsule Service",
    "description": "A demo Capsule Service.",
    "version": "0.1.0",
    "runtime": "nodejs",
    "status": "HEALTHY",
    "healthStatus": "UP",
    "lastReportedAt": "2026-04-30T10:21:00Z",
    "lastHealthAt": "2026-04-30T10:21:00Z",
    "createdAt": "2026-04-30T10:00:00Z",
    "updatedAt": "2026-04-30T10:21:00Z",
    "manifest": {},
    "health": {},
    "configs": [],
    "actions": []
  }
}
```

### 13.3 Get Capsule Service（胶囊服务） manifest

```http
GET /api/admin/capsule-services/{serviceId}/manifest
```

### 13.4 Get Capsule Service（胶囊服务） health

```http
GET /api/admin/capsule-services/{serviceId}/health
```

### 13.5 Get Capsule Service（胶囊服务） configs

```http
GET /api/admin/capsule-services/{serviceId}/configs
```

### 13.6 Get Capsule Service（胶囊服务） actions

```http
GET /api/admin/capsule-services/{serviceId}/actions
```

These detail endpoints may be implemented separately or included in the main detail response.

---

## 14. Action Admin APIs

### 14.1 Request action execution

```http
POST /api/admin/capsule-services/{serviceId}/actions/{actionName}
```

Request (matches OpenAPI `CreateActionCommandRequest`):

```json
{
  "payload": {
    "message": "hello"
  }
}
```

Response (matches OpenAPI `Command`):

```json
{
  "success": true,
  "data": {
    "id": "cmd_001",
    "agentId": "agt_001",
    "serviceId": "svc_001",
    "type": "ACTION",
    "actionName": "echo",
    "payload": { "message": "hello" },
    "status": "PENDING",
    "createdByUserId": "usr_001",
    "createdAt": "2026-04-30T10:22:00Z",
    "expiresAt": "2026-04-30T10:27:00Z"
  }
}
```

Backend responsibilities:

1. authenticate user;
2. validate service exists;
3. validate Agent（代理） is available or command can be queued;
4. validate action exists and is enabled;
5. validate payload if schema exists;
6. enforce confirmation for dangerous actions;
7. create Command;
8. write AuditEvent.

安全 rule:

> This endpoint must execute only predefined actions. It must not accept arbitrary shell commands.

---

## 15. Command Admin APIs

### 15.1 List Commands

```http
GET /api/admin/commands
```

Query parameters:

```text
page
pageSize
status
serviceId
agentId
from
to
```

Response (matches OpenAPI `Command[]` + `Pagination`):

```json
{
  "success": true,
  "data": [
    {
      "id": "cmd_001",
      "agentId": "agt_001",
      "serviceId": "svc_001",
      "type": "ACTION",
      "actionName": "echo",
      "status": "SUCCEEDED",
      "createdAt": "2026-04-30T10:22:00Z",
      "startedAt": "2026-04-30T10:22:01Z",
      "completedAt": "2026-04-30T10:22:02Z"
    }
  ],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "total": 1
  }
}
```

### 15.2 Get Command detail

```http
GET /api/admin/commands/{commandId}
```

Response (matches OpenAPI `CommandDetail`):

```json
{
  "success": true,
  "data": {
    "id": "cmd_001",
    "agentId": "agt_001",
    "serviceId": "svc_001",
    "type": "ACTION",
    "actionName": "echo",
    "payload": { "message": "hello" },
    "status": "SUCCEEDED",
    "createdByUserId": "usr_001",
    "createdAt": "2026-04-30T10:22:00Z",
    "startedAt": "2026-04-30T10:22:01Z",
    "completedAt": "2026-04-30T10:22:02Z",
    "expiresAt": "2026-04-30T10:27:00Z",
    "result": {
      "id": "crs_001",
      "commandId": "cmd_001",
      "success": true,
      "message": "Action completed.",
      "data": { "message": "hello" },
      "reportedAt": "2026-04-30T10:22:02Z"
    }
  }
}
```

---

## 16. Audit Admin APIs

### 16.1 List Audit Events

```http
GET /api/admin/audit-events
```

Query parameters:

```text
page
pageSize
action
actorType       USER | AGENT | SYSTEM
actorId
targetType
targetId
result          SUCCESS | FAILURE
from
to
```

Response (matches OpenAPI `AuditEvent[]` + `Pagination`):

```json
{
  "success": true,
  "data": [
    {
      "id": "aud_001",
      "actorType": "USER",
      "actorId": "usr_001",
      "action": "command.created",
      "targetType": "Command",
      "targetId": "cmd_001",
      "result": "SUCCESS",
      "message": "User created command echo for demo-capsule-service.",
      "metadata": {
        "actionName": "echo"
      },
      "createdAt": "2026-04-30T10:22:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "total": 1
  }
}
```

### 16.2 Get Audit Event detail

```http
GET /api/admin/audit-events/{auditEventId}
```

Response 包括 sanitized `metadata`. Sensitive fields must be redacted before storage.

---

## 17. System APIs

### 17.1 System health

```http
GET /api/system/health
```

Response:

```json
{
  "success": true,
  "data": {
    "status": "UP",
    "version": "0.1.0",
    "database": "UP"
  }
}
```

### 17.2 System settings

Optional for CE（社区版） v0.1.

```http
GET /api/system/settings
```

Response:

```json
{
  "success": true,
  "data": {
    "agentHeartbeatIntervalSeconds": 30,
    "agentOfflineThresholdSeconds": 90,
    "commandPollIntervalSeconds": 5,
    "commandTtlSeconds": 300
  }
}
```

---

## 18. Agent（代理） APIs

Agent（代理） APIs are used by Agent（代理） SDK.

### 18.1 Register Agent（代理）

```http
POST /api/agents/register
```

Request:

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

Response:

```json
{
  "success": true,
  "data": {
    "agentId": "agt_001",
    "agentToken": "opstage_agent_xxxxxxxxx",
    "workspaceId": "wks_default",
    "heartbeatIntervalSeconds": 30,
    "commandPollingIntervalSeconds": 5
  }
}
```

### 18.2 Heartbeat

```http
POST /api/agents/{agentId}/heartbeat
Authorization: Bearer <agentToken>
```

Request (matches OpenAPI `AgentHeartbeatRequest`):

```json
{
  "serviceId": "svc_001",
  "health": {
    "status": "UP",
    "message": "Service is healthy.",
    "details": {}
  }
}
```

Response (matches OpenAPI `AgentHeartbeatResponse`):

```json
{
  "success": true,
  "data": {
    "heartbeatIntervalSeconds": 30,
    "commandPollIntervalSeconds": 5
  }
}
```

### 18.3 Service report

```http
POST /api/agents/{agentId}/services/report
Authorization: Bearer <agentToken>
```

Request (matches OpenAPI `ServiceReportRequest`):

```json
{
  "services": [
    {
      "code": "demo-capsule-service",
      "name": "Demo Capsule Service",
      "version": "0.1.0",
      "runtime": "nodejs",
      "manifest": {
        "kind": "CapsuleService",
        "schemaVersion": "1.0",
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
          "name": "echo",
          "label": "Echo",
          "dangerLevel": "LOW",
          "requiresConfirmation": false
        }
      ]
    }
  ]
}
```

Response (matches OpenAPI `ServiceReportResponse`):

```json
{
  "success": true,
  "data": {
    "services": [
      {
        "code": "demo-capsule-service",
        "serviceId": "svc_001",
        "accepted": true
      }
    ]
  }
}
```

### 18.4 Poll Commands

```http
GET /api/agents/{agentId}/commands
Authorization: Bearer <agentToken>
```

Response:

```json
{
  "success": true,
  "data": [
    {
      "id": "cmd_001",
      "agentId": "agt_001",
      "serviceId": "svc_001",
      "type": "ACTION",
      "actionName": "echo",
      "payload": { "message": "hello" },
      "status": "RUNNING",
      "createdAt": "2026-04-30T10:22:00Z",
      "startedAt": "2026-04-30T10:22:01Z",
      "expiresAt": "2026-04-30T10:27:00Z"
    }
  ]
}
```

### 18.5 Report Command Result

```http
POST /api/agents/{agentId}/commands/{commandId}/result
Authorization: Bearer <agentToken>
```

Request (matches OpenAPI `ReportCommandResultRequest`):

```json
{
  "success": true,
  "message": "Action completed.",
  "data": {
    "message": "hello"
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

Response (matches OpenAPI `Command` after transition):

```json
{
  "success": true,
  "data": {
    "id": "cmd_001",
    "status": "SUCCEEDED",
    "completedAt": "2026-04-30T10:22:02Z"
  }
}
```

---

## 19. Error Codes

The canonical, exhaustive CE（社区版） v0.1 error code list lives in `09-contracts/errors.md`. The codes below are illustrative.

Recommended common error codes:

```text
VALIDATION_FAILED
UNAUTHORIZED
FORBIDDEN
NOT_FOUND
CONFLICT
INTERNAL_ERROR
```

Agent（代理）-related error codes:

```text
REGISTRATION_TOKEN_INVALID
REGISTRATION_TOKEN_EXPIRED
REGISTRATION_TOKEN_USED
AGENT_TOKEN_INVALID
AGENT_TOKEN_REVOKED
AGENT_DISABLED
AGENT_NOT_FOUND
```

Service-related error codes:

```text
SERVICE_NOT_FOUND
SERVICE_MANIFEST_INVALID
SERVICE_NOT_MANAGEABLE
ACTION_NOT_FOUND
ACTION_DISABLED
PAYLOAD_INVALID
```

Command-related error codes:

```text
COMMAND_NOT_FOUND
COMMAND_EXPIRED
COMMAND_NOT_ASSIGNED_TO_AGENT
COMMAND_ALREADY_COMPLETED
COMMAND_INVALID_STATE
```

---

## 20. 安全 Rules

### 20.1 No arbitrary shell API

CE（社区版） v0.1 must not provide endpoints such as:

```http
POST /api/agents/{agentId}/shell
POST /api/admin/capsule-services/{serviceId}/exec
POST /api/admin/commands/shell
```

### 20.2 Token safety

- Raw Agent（代理） tokens must not be stored.
- Registration tokens must be shown only once.
- Agent（代理） tokens must be stored as hashes.
- Agent（代理） APIs must reject revoked or disabled Agents.

### 20.3 Sensitive payloads

APIs should avoid returning raw secrets in:

- manifest;
- config values;
- health details;
- command payloads;
- command results;
- audit events.

Use `secretRef` or masking.

### 20.4 Audit important operations

Backend should audit:

- login;
- failed login;
- Agent（代理） registration;
- service report;
- action request;
- Command creation;
- Command success/failure.

---

## 21. CE（社区版） v0.1 Required Endpoints

CE（社区版） v0.1 must implement at least:

### Admin APIs

```text
POST /api/admin/auth/login
POST /api/admin/auth/logout
GET  /api/admin/auth/me
GET  /api/admin/dashboard/summary
GET  /api/admin/agents
GET  /api/admin/agents/{agentId}
POST /api/admin/registration-tokens
GET  /api/admin/capsule-services
GET  /api/admin/capsule-services/{serviceId}
POST /api/admin/capsule-services/{serviceId}/actions/{actionName}
GET  /api/admin/commands
GET  /api/admin/commands/{commandId}
GET  /api/admin/audit-events
```

### Agent（代理） APIs

```text
POST /api/agents/register
POST /api/agents/{agentId}/heartbeat
POST /api/agents/{agentId}/services/report
GET  /api/agents/{agentId}/commands
POST /api/agents/{agentId}/commands/{commandId}/result
```

Optional CE（社区版） v0.1 endpoints:

```text
GET  /api/admin/capsule-services/{serviceId}/manifest
GET  /api/admin/capsule-services/{serviceId}/health
GET  /api/admin/capsule-services/{serviceId}/configs
GET  /api/admin/capsule-services/{serviceId}/actions
GET  /api/admin/audit-events/{auditEventId}
```

### System APIs

```text
GET  /api/system/health
GET  /api/system/version
```

---

## 22. Future API Extensions

Future EE（企业版）/Cloud（云版） may add:

- RBAC APIs;
- Workspace management APIs;
- Organization and tenant APIs;
- SSO configuration APIs;
- config publishing APIs;
- secret management APIs;
- metrics APIs;
- log APIs;
- alert APIs;
- WebSocket command channel;
- Agent（代理） gateway APIs;
- billing APIs for Cloud（云版）.

CE（社区版） v0.1 should not require these.

---

## 23. API Acceptance Criteria

The CE（社区版） API design is acceptable when:

- UI can authenticate and load dashboard;
- UI can list Agents and Capsule Services;
- Agent（代理） can register using a registration token;
- Agent（代理） can heartbeat using Agent（代理） token;
- Agent（代理） can report service manifest;
- UI can request a predefined action;
- Backend creates a Command;
- Agent（代理） can poll Commands;
- Agent（代理） can report CommandResult;
- UI can display Commands and Audit Events;
- stale status can be represented;
- no arbitrary shell execution API exists;
- error responses are structured.

---

## 24. Summary

CE（社区版） APIs should be small, explicit, and safe.

The most important API rule is:

> UI talks to Backend, Agent（代理） talks to Backend, and all operations go through predefined actions and Commands.
