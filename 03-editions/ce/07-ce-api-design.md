# CE API Design

- Status: Implementation Target
- Edition: CE
- Priority: Current
- Audience: architects, backend developers, frontend developers, agent SDK developers, AI coding agents

This document defines the API design for **Opstage CE v0.1**.

CE APIs are divided into two surfaces:

```text
Admin APIs
Agent APIs
```

Admin APIs are used by Opstage UI.

Agent APIs are used by registered Agents.

---

## 1. API Design Goal

The goal of the CE API design is to support the minimum complete Capsule governance loop:

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

The API should be simple, JSON-based, easy to debug, and compatible with future EE and Cloud extensions.

---

## 2. API Principles

CE v0.1 APIs should follow these principles:

1. Use REST-style JSON APIs.
2. Keep Admin APIs and Agent APIs clearly separated.
3. Require UI authentication for Admin APIs.
4. Require Agent token authentication for Agent APIs after registration.
5. Do not let UI call Agents directly.
6. Do not expose arbitrary shell execution APIs.
7. Use stable resource names.
8. Use shared status values from the Status Model.
9. Return structured errors.
10. Keep paths stable enough for Agent SDK usage.
11. Allow additive future fields.
12. Avoid EE/Cloud-only requirements in CE v0.1.

---

## 3. API Surface Overview

### 3.1 Admin APIs

Admin APIs are called by Opstage UI.

They provide:

- authentication;
- dashboard data;
- Agent list and detail;
- Capsule Service list and detail;
- action request;
- Command list and detail;
- Audit Event list and detail;
- system setup and settings.

Base path:

```text
/api/admin
```

### 3.2 Agent APIs

Agent APIs are called by Agents.

They provide:

- Agent registration;
- heartbeat;
- service report;
- command polling;
- command result reporting.

Base path:

```text
/api/agents
```

---

## 4. Authentication

### 4.1 Admin API authentication

Admin APIs require a logged-in user.

Recommended CE v0.1 options:

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

### 4.2 Agent API authentication

Agent APIs after registration require Agent token:

```http
Authorization: Bearer <agentToken>
```

Backend must validate:

- token hash;
- token status;
- Agent status;
- revoked/disabled state.

### 4.3 Registration endpoint authentication

Agent registration uses a registration token in request body.

```http
POST /api/agents/register
```

This endpoint does not use Agent token because the Agent is not registered yet.

---

## 5. Common Response Shape

CE v0.1 may use a simple response shape.

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

```json
{
  "success": true,
  "data": {
    "items": [],
    "page": 1,
    "pageSize": 20,
    "total": 0
  }
}
```

### 5.4 Notes

The exact envelope may be adjusted during implementation, but APIs should remain consistent.

Do not mix raw arrays and enveloped responses randomly.

---

## 6. HTTP Status Codes

Recommended usage:

| HTTP Status | Meaning |
|---|---|
| 200 | Successful query or operation |
| 201 | Resource created |
| 400 | Invalid request payload |
| 401 | Not authenticated or invalid token |
| 403 | Authenticated but not allowed |
| 404 | Resource not found |
| 409 | Conflict, duplicate, invalid state transition |
| 422 | Validation failed |
| 500 | Internal server error |
|

CE may keep status usage simple, but it should not return `200` for clear authentication or validation failures.

---

## 7. Pagination and Filtering

List APIs should support simple pagination.

Recommended query parameters:

```text
page=1
pageSize=20
```

Optional filtering:

```text
status=ONLINE
q=demo
from=2026-04-30T00:00:00Z
to=2026-04-30T23:59:59Z
```

CE v0.1 may implement minimal filters.

Page size rules:

```text
default pageSize = 20
max pageSize = 100
```

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
  "password": "change-me"
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

## 11. Agent Admin APIs

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
  "data": {
    "items": [
      {
        "id": "agt_001",
        "code": "local-dev-agent",
        "name": "Local Development Agent",
        "mode": "embedded",
        "runtime": "nodejs",
        "version": "0.1.0",
        "status": "ONLINE",
        "lastHeartbeatAt": "2026-04-30T10:21:00Z",
        "registeredAt": "2026-04-30T10:00:00Z"
      }
    ],
    "page": 1,
    "pageSize": 20,
    "total": 1
  }
}
```

### 11.2 Get Agent detail

```http
GET /api/admin/agents/{agentId}
```

Response:

```json
{
  "success": true,
  "data": {
    "id": "agt_001",
    "code": "local-dev-agent",
    "name": "Local Development Agent",
    "mode": "embedded",
    "runtime": "nodejs",
    "version": "0.1.0",
    "status": "ONLINE",
    "hostname": "dev-machine",
    "os": "darwin",
    "arch": "arm64",
    "lastHeartbeatAt": "2026-04-30T10:21:00Z",
    "services": [
      {
        "id": "svc_001",
        "code": "demo-capsule-service",
        "name": "Demo Capsule Service",
        "effectiveStatus": "ONLINE"
      }
    ]
  }
}
```

### 11.3 Disable Agent

Optional for CE v0.1 UI, but useful in data model.

```http
POST /api/admin/agents/{agentId}/disable
```

### 11.4 Re-enable Agent

Optional for CE v0.1 UI.

```http
POST /api/admin/agents/{agentId}/enable
```

### 11.5 Revoke Agent

Optional for CE v0.1 UI, but important for security.

```http
POST /api/admin/agents/{agentId}/revoke
```

---

## 12. Registration Token Admin APIs

CE v0.1 needs a way to create registration tokens.

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

Security rule:

> The raw token should be shown only once and stored only as a hash.

### 12.2 List registration tokens

Optional for CE v0.1.

```http
GET /api/admin/registration-tokens
```

### 12.3 Revoke registration token

Optional for CE v0.1.

```http
POST /api/admin/registration-tokens/{tokenId}/revoke
```

---

## 13. Capsule Service Admin APIs

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
  "data": {
    "items": [
      {
        "id": "svc_001",
        "code": "demo-capsule-service",
        "name": "Demo Capsule Service",
        "version": "0.1.0",
        "runtime": "nodejs",
        "agentMode": "embedded",
        "effectiveStatus": "ONLINE",
        "reportedStatus": "ONLINE",
        "healthStatus": "UP",
        "lastReportedAt": "2026-04-30T10:21:00Z",
        "agent": {
          "id": "agt_001",
          "code": "local-dev-agent",
          "status": "ONLINE"
        }
      }
    ],
    "page": 1,
    "pageSize": 20,
    "total": 1
  }
}
```

### 13.2 Get Capsule Service detail

```http
GET /api/admin/capsule-services/{serviceId}
```

Response:

```json
{
  "success": true,
  "data": {
    "id": "svc_001",
    "code": "demo-capsule-service",
    "name": "Demo Capsule Service",
    "description": "A demo Capsule Service.",
    "version": "0.1.0",
    "runtime": "nodejs",
    "agentMode": "embedded",
    "reportedStatus": "ONLINE",
    "effectiveStatus": "ONLINE",
    "healthStatus": "UP",
    "freshness": "FRESH",
    "lastReportedAt": "2026-04-30T10:21:00Z",
    "agent": {
      "id": "agt_001",
      "code": "local-dev-agent",
      "status": "ONLINE",
      "lastHeartbeatAt": "2026-04-30T10:21:00Z"
    },
    "manifest": {},
    "health": {},
    "configs": [],
    "actions": []
  }
}
```

### 13.3 Get Capsule Service manifest

```http
GET /api/admin/capsule-services/{serviceId}/manifest
```

### 13.4 Get Capsule Service health

```http
GET /api/admin/capsule-services/{serviceId}/health
```

### 13.5 Get Capsule Service configs

```http
GET /api/admin/capsule-services/{serviceId}/configs
```

### 13.6 Get Capsule Service actions

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

Request:

```json
{
  "payload": {
    "message": "hello"
  },
  "confirmed": true
}
```

Response:

```json
{
  "success": true,
  "data": {
    "commandId": "cmd_001",
    "status": "PENDING"
  }
}
```

Backend responsibilities:

1. authenticate user;
2. validate service exists;
3. validate Agent is available or command can be queued;
4. validate action exists and is enabled;
5. validate payload if schema exists;
6. enforce confirmation for dangerous actions;
7. create Command;
8. write AuditEvent.

Security rule:

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

Response:

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "cmd_001",
        "serviceId": "svc_001",
        "serviceCode": "demo-capsule-service",
        "agentId": "agt_001",
        "commandType": "ACTION",
        "actionName": "echo",
        "status": "SUCCESS",
        "createdAt": "2026-04-30T10:22:00Z",
        "finishedAt": "2026-04-30T10:22:02Z"
      }
    ],
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

Response:

```json
{
  "success": true,
  "data": {
    "id": "cmd_001",
    "commandType": "ACTION",
    "actionName": "echo",
    "payload": {
      "message": "hello"
    },
    "status": "SUCCESS",
    "service": {
      "id": "svc_001",
      "code": "demo-capsule-service"
    },
    "agent": {
      "id": "agt_001",
      "code": "local-dev-agent"
    },
    "result": {
      "status": "SUCCESS",
      "outputText": "Action completed.",
      "resultJson": {
        "success": true,
        "data": {
          "message": "hello"
        }
      }
    },
    "createdAt": "2026-04-30T10:22:00Z",
    "dispatchedAt": "2026-04-30T10:22:01Z",
    "finishedAt": "2026-04-30T10:22:02Z"
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
actorType
actorId
resourceType
resourceId
result
from
to
```

Response:

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "aud_001",
        "actorType": "user",
        "actorName": "admin",
        "action": "command.created",
        "resourceType": "Command",
        "resourceId": "cmd_001",
        "description": "User created command echo for demo-capsule-service.",
        "result": "SUCCESS",
        "createdAt": "2026-04-30T10:22:00Z"
      }
    ],
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

Response includes sanitized `requestJson` and `resultJson`.

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

Optional for CE v0.1.

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

## 18. Agent APIs

Agent APIs are used by Agent SDK.

### 18.1 Register Agent

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

Request:

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
        "checkedAt": "2026-04-30T10:21:00Z",
        "message": "Service is healthy.",
        "details": {}
      }
    }
  ]
}
```

Response:

```json
{
  "success": true,
  "data": {
    "accepted": true,
    "serverTime": "2026-04-30T10:21:01Z",
    "nextHeartbeatIntervalSeconds": 30
  }
}
```

### 18.3 Service report

```http
POST /api/agents/{agentId}/services/report
Authorization: Bearer <agentToken>
```

Request:

```json
{
  "services": [
    {
      "manifest": {
        "kind": "CapsuleService",
        "schemaVersion": "1.0",
        "code": "demo-capsule-service",
        "name": "Demo Capsule Service",
        "version": "0.1.0",
        "runtime": "nodejs",
        "agentMode": "embedded",
        "capabilities": ["demo.echo"],
        "actions": [
          {
            "name": "echo",
            "label": "Echo",
            "dangerLevel": "LOW",
            "enabled": true
          }
        ],
        "configs": [
          {
            "key": "demo.message",
            "label": "Demo Message",
            "type": "string",
            "defaultValue": "hello capsule",
            "editable": true,
            "sensitive": false
          }
        ]
      },
      "reportedStatus": "ONLINE"
    }
  ]
}
```

Response:

```json
{
  "success": true,
  "data": {
    "accepted": true,
    "services": [
      {
        "code": "demo-capsule-service",
        "serviceId": "svc_001",
        "status": "ACCEPTED"
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
  "data": {
    "commands": [
      {
        "commandId": "cmd_001",
        "serviceId": "svc_001",
        "serviceCode": "demo-capsule-service",
        "commandType": "ACTION",
        "actionName": "echo",
        "payload": {
          "message": "hello"
        },
        "issuedAt": "2026-04-30T10:22:00Z",
        "expiresAt": "2026-04-30T10:27:00Z"
      }
    ]
  }
}
```

### 18.5 Report Command Result

```http
POST /api/agents/{agentId}/commands/{commandId}/result
Authorization: Bearer <agentToken>
```

Request:

```json
{
  "status": "SUCCESS",
  "outputText": "Action completed.",
  "resultJson": {
    "success": true,
    "data": {
      "message": "hello"
    }
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
    "success": false,
    "error": {
      "code": "ACTION_NOT_FOUND",
      "message": "Action not found: refreshSession"
    }
  },
  "startedAt": "2026-04-30T10:22:01Z",
  "finishedAt": "2026-04-30T10:22:02Z"
}
```

Response:

```json
{
  "success": true,
  "data": {
    "accepted": true,
    "commandId": "cmd_001",
    "status": "SUCCESS"
  }
}
```

---

## 19. Error Codes

Recommended common error codes:

```text
VALIDATION_FAILED
UNAUTHORIZED
FORBIDDEN
NOT_FOUND
CONFLICT
INTERNAL_ERROR
```

Agent-related error codes:

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

## 20. Security Rules

### 20.1 No arbitrary shell API

CE v0.1 must not provide endpoints such as:

```http
POST /api/agents/{agentId}/shell
POST /api/admin/capsule-services/{serviceId}/exec
POST /api/admin/commands/shell
```

### 20.2 Token safety

- Raw Agent tokens must not be stored.
- Registration tokens must be shown only once.
- Agent tokens must be stored as hashes.
- Agent APIs must reject revoked or disabled Agents.

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
- Agent registration;
- service report;
- action request;
- Command creation;
- Command success/failure.

---

## 21. CE v0.1 Required Endpoints

CE v0.1 must implement at least:

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

### Agent APIs

```text
POST /api/agents/register
POST /api/agents/{agentId}/heartbeat
POST /api/agents/{agentId}/services/report
GET  /api/agents/{agentId}/commands
POST /api/agents/{agentId}/commands/{commandId}/result
```

Optional CE v0.1 endpoints:

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

Future EE/Cloud may add:

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
- Agent gateway APIs;
- billing APIs for Cloud.

CE v0.1 should not require these.

---

## 23. API Acceptance Criteria

The CE API design is acceptable when:

- UI can authenticate and load dashboard;
- UI can list Agents and Capsule Services;
- Agent can register using a registration token;
- Agent can heartbeat using Agent token;
- Agent can report service manifest;
- UI can request a predefined action;
- Backend creates a Command;
- Agent can poll Commands;
- Agent can report CommandResult;
- UI can display Commands and Audit Events;
- stale status can be represented;
- no arbitrary shell execution API exists;
- error responses are structured.

---

## 24. Summary

CE APIs should be small, explicit, and safe.

The most important API rule is:

> UI talks to Backend, Agent talks to Backend, and all operations go through predefined actions and Commands.
