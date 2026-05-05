---
status: draft
audience: backend-developers
stability: unstable
last_reviewed: 2026-05-05
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

# 错误码

所有错误响应都使用 OpenAPI `ErrorEnvelope` 结构：

```json
{
  "success": false,
  "error": {
    "code": "ACTION_PREPARE_TIMEOUT",
    "message": "Action prepare timed out waiting for agent.",
    "details": {}
  }
}
```

## Envelope 规则

- code MUST be one of the codes in this document
- code values are stable, uppercase, snake-case strings
- message is English; UI MAY translate locally
- details is optional and structured; sensitive values MUST be redacted
- HTTP status codes are listed alongside each code; backend MUST use the listed status

## Generic Codes

| Code | HTTP | 含义 |
|---|---:|---|
| `VALIDATION_FAILED` | 422 | Request body or query parameters failed Zod validation. |
| `UNAUTHORIZED` | 401 | No valid session or token. |
| `FORBIDDEN` | 403 | Authenticated but not allowed (includes CSRF token mismatch). |
| `NOT_FOUND` | 404 | Requested resource does not exist or is not visible to the caller. |
| `CONFLICT` | 409 | State conflict (duplicate resource, idempotency violation). |
| `RATE_LIMITED` | 429 | Reserved for future EE/Cloud editions. |
| `INTERNAL_ERROR` | 500 | Unexpected server error. Use sparingly; prefer specific codes. |
| `SERVICE_UNAVAILABLE` | 503 | Backend cannot reach a critical dependency (e.g. database). |
| `REQUEST_ERROR` | 400 | Fallback for non-500 request errors when no more specific code is available. |
| `STATIC_NOT_FOUND` | 404 | Static UI asset was not found while serving the SPA/static bundle. |

## Authentication Codes

| Code | HTTP | 含义 |
|---|---:|---|
| `LOGIN_FAILED` | 401 | Username or password invalid (do not reveal which). |
| `SESSION_EXPIRED` | 401 | Session cookie present but expired. |
| `SESSION_INVALID` | 401 | Session cookie tampered with or session not found. |
| `CSRF_TOKEN_MISMATCH` | 403 | X-CSRF-Token header missing or does not match server-side session token. |
| `CSRF_INVALID` | 403 | X-CSRF-Token header missing or does not match server-side session token. Implementation alias for CSRF_TOKEN_MISMATCH. |

## Token Codes

| Code | HTTP | 含义 |
|---|---:|---|
| `REGISTRATION_TOKEN_INVALID` | 401 | Token does not exist or hash does not match. |
| `REGISTRATION_TOKEN_EXPIRED` | 401 | Token past expiresAt. |
| `REGISTRATION_TOKEN_USED` | 409 | Token already consumed. |
| `REGISTRATION_TOKEN_REVOKED` | 401 | Token revoked by admin. |
| `AGENT_TOKEN_INVALID` | 401 | Authorization: Bearer header missing or hash mismatch. |
| `AGENT_TOKEN_REVOKED` | 401 | Agent token has been revoked. |
| `AGENT_TOKEN_EXPIRED` | 401 | Agent token past expiresAt. |
| `REGISTRATION_TOKEN_NOT_FOUND` | 404 | Requested registration token does not exist or is not visible to the caller. |
| `REGISTRATION_TOKEN_NOT_DELETABLE` | 409 | Registration token can only be deleted after it is expired or revoked. |

## Agent Codes

| Code | HTTP | 含义 |
|---|---:|---|
| `AGENT_NOT_FOUND` | 404 | agentId does not exist. |
| `AGENT_DISABLED` | 403 | Agent is DISABLED. |
| `AGENT_REVOKED` | 403 | Agent is REVOKED. |
| `AGENT_CODE_TAKEN` | 409 | An Agent with this code already exists in the workspace. |
| `AGENT_ID_MISMATCH` | 403 | Path agentId does not match the Agent that owns the token. |
| `AGENT_NOT_AVAILABLE` | 409 | Agent exists but cannot currently accept commands for the requested service/action. |
| `AGENT_NOT_READY` | 409 | Agent has not sent a heartbeat or command poll yet. |
| `AGENT_HEARTBEAT_STALE` | 409 | Agent heartbeat/poll timestamp is older than the configured stale threshold. |

## Capsule Service Codes

| Code | HTTP | 含义 |
|---|---:|---|
| `CAPSULE_SERVICE_NOT_FOUND` | 404 | serviceId does not exist. |
| `CAPSULE_SERVICE_NOT_OWNED` | 403 | Service exists but does not belong to the calling Agent. |
| `CAPSULE_SERVICE_MANIFEST_INVALID` | 422 | Manifest validation failed (missing required fields, etc.). |
| `CAPSULE_SERVICE_CODE_TAKEN` | 409 | Service code conflict in workspace. |

## Action and Command Codes

| Code | HTTP | 含义 |
|---|---:|---|
| `ACTION_NOT_FOUND` | 404 | Action name not declared on the service manifest. |
| `ACTION_DISABLED` | 403 | ActionDefinition.enabled = false. |
| `ACTION_PAYLOAD_INVALID` | 422 | Payload failed inputSchema validation. |
| `ACTION_REQUIRES_CONFIRMATION` | 422 | Confirmation flag missing for an action with requiresConfirmation = true. |
| `COMMAND_NOT_FOUND` | 404 | commandId does not exist. |
| `COMMAND_NOT_OWNED` | 403 | Command exists but is not assigned to the calling Agent. |
| `COMMAND_ALREADY_TERMINAL` | 409 | Result reported for a Command already in a terminal state. |
| `COMMAND_EXPIRED` | 410 | Command past expiresAt and cannot be reported. |
| `COMMAND_INVALID_TRANSITION` | 409 | Attempted a CommandStatus transition that is not allowed. |
| `ACTION_PREPARE_TIMEOUT` | 408 | Action prepare command timed out while waiting for Agent response. |
| `ACTION_PREPARE_FAILED` | 424 | Agent returned a failed result for an ACTION_PREPARE command. |
| `COMMAND_ALREADY_COMPLETED` | 409 | Result was reported for a Command that already has a stored result or terminal status. |
| `COMMAND_NOT_RETRYABLE` | 409 | Requested Command cannot be retried from its current state. |
| `COMMAND_RESULT_TOO_LARGE` | 413 | Serialized CommandResult message/data/error exceeded OPSTAGE_COMMAND_RESULT_MAX_BYTES. |

## Config Codes (read-only in CE v0.1)

| Code | HTTP | 含义 |
|---|---:|---|
| `CONFIG_ITEM_NOT_FOUND` | 404 | Config key does not exist for the service. |
| `CONFIG_EDIT_NOT_SUPPORTED` | 405 | CE v0.1 does not support config editing — reserved for EE/Cloud. |

## User/Admin Codes

| Code | HTTP | 含义 |
|---|---:|---|
| `USER_ALREADY_EXISTS` | 409 | A user with the requested username already exists. |
| `USER_NOT_FOUND` | 404 | Requested user does not exist or is not visible to the caller. |
| `LAST_OWNER_REQUIRED` | 409 | Operation would remove or demote the last active owner. |

## System Codes

| Code | HTTP | 含义 |
|---|---:|---|
| `DATABASE_UNAVAILABLE` | 503 | Backend cannot reach SQLite database. |
| `BOOTSTRAP_FAILED` | 500 | Required environment variable missing — surfaced only via startup logs. |
