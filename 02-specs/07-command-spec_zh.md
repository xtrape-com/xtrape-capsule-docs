<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 07-command-spec.md
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

# Command 规范

- Status: 规范
- Edition: 共享
- Priority: 高
- Audience: backend developers, frontend developers, agent SDK developers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/` (OpenAPI / Prisma) disagree, the ADRs and contracts win for CE（社区版） v0.1. This document captures the long-term shared concept; the contracts capture the CE（社区版） v0.1 wire format.

This document 定义 the **Command** specification for the `xtrape-capsule` domain.

A Command is an instruction created by Opstage（运维舞台） Backend and executed by an authorized Agent（代理）. Commands are the delivery mechanism for operational requests such as predefined Capsule Service（胶囊服务） actions.

In CE（社区版） v0.1, Commands are primarily used to execute predefined actions through the Node.js embedded Agent（代理） SDK.

---

## 1. Purpose

The Command 规范 定义:

- what a Command is;
- how Backend creates Commands;
- how Agents fetch Commands;
- how Agents execute Commands;
- how CommandResult is reported;
- Command status lifecycle;
- timeout and expiration behavior;
- idempotency requirements;
- audit requirements;
- CE（社区版） v0.1 required subset;
- future EE（企业版） and Cloud（云版） extension points.

Commands provide a safe and auditable way for Opstage（运维舞台） to operate Capsule Services without giving the UI arbitrary remote execution power.

---

## 2. Core Rule

Opstage（运维舞台） UI must not directly call Agents or Capsule Services.

Operational requests should flow through Backend-created Commands.

Correct CE（社区版） v0.1 flow:

```text
User requests predefined action in UI
    ↓
Backend validates request
    ↓
Backend creates Command
    ↓
Agent polls Command
    ↓
Agent executes predefined handler
    ↓
Agent reports CommandResult
    ↓
Backend updates Command status
    ↓
Backend writes AuditEvent
    ↓
UI shows result
```

Incorrect flow:

```text
UI directly calls Agent
    ↓
Agent executes untracked operation
```

Another incorrect flow:

```text
UI sends arbitrary shell command
    ↓
Agent executes shell
```

CE（社区版） v0.1 must not support arbitrary shell command execution.

---

## 3. Command Scope

In CE（社区版） v0.1, a Command should represent one operational instruction targeting one Agent（代理） and usually one Capsule Service（胶囊服务）.

Typical CE（社区版） command:

```text
Execute action runHealthCheck on demo-capsule-service through agent agt_001.
```

Future Commands may support:

- config changes;
- service reload;
- resource-level actions;
- approval workflow;
- scheduled execution;
- batch execution;
- long-running operations;
- streaming logs;
- interactive sessions.

CE（社区版） v0.1 should implement only the action-execution command path.

---

## 4. Command Types

Recommended command types:

```text
ACTION
CONFIG_UPDATE
CONFIG_RELOAD
SERVICE_REFRESH
AGENT_CONTROL
CUSTOM
```

CE（社区版） v0.1 must implement:

```text
ACTION
```

Other command types are reserved for future versions.

### 4.1 `ACTION`

Execute a predefined Capsule Service（胶囊服务） action.

Example:

```json
{
  "type": "ACTION",
  "actionName": "runHealthCheck"
}
```

### 4.2 `CONFIG_UPDATE`

Reserved for future configuration changes.

### 4.3 `CONFIG_RELOAD`

Reserved for future config reload orchestration.

### 4.4 `SERVICE_REFRESH`

Reserved for future service metadata refresh.

### 4.5 `AGENT_CONTROL`

Reserved for future Agent（代理） control operations.

### 4.6 `CUSTOM`

Reserved for future controlled extension.

`CUSTOM` must not become arbitrary shell execution.

---

## 5. Command Object

### 5.1 CE（社区版） v0.1 Command (must match OpenAPI `Command`)

```json
{
  "id": "cmd_001",
  "agentId": "agt_001",
  "serviceId": "svc_001",
  "type": "ACTION",
  "actionName": "runHealthCheck",
  "payload": {},
  "status": "PENDING",
  "createdByUserId": "usr_001",
  "createdAt": "2026-04-30T10:22:00Z",
  "startedAt": null,
  "completedAt": null,
  "expiresAt": "2026-04-30T10:27:00Z"
}
```

### 5.2 Future Command Fields

The following fields may be added in EE（企业版）/Cloud（云版）:

```text
idempotencyKey
metadata
priority
concurrencyKey
resourceLockKey
```

CE（社区版） v0.1 does not require these.

---

## 6. Command Fields

CE（社区版） v0.1 fields match OpenAPI `Command` schema. Field names are normative.

### 6.1 `id`

Unique Command identifier. Required. Prefix: `cmd_`.

### 6.2 `agentId`

Target Agent（代理） that must execute the Command. Required. Prefix: `agt_`.

### 6.3 `serviceId`

Target Capsule Service（胶囊服务）. Required. Prefix: `svc_`.

### 6.4 `type`

Type of Command. Required. CE（社区版） v0.1 支持 only `ACTION`. Other types (`CONFIG_UPDATE`, `CONFIG_RELOAD`, `SERVICE_REFRESH`, `AGENT_CONTROL`, `CUSTOM`) are reserved for future EE（企业版）/Cloud（云版）.

### 6.5 `actionName`

Name of the action to execute. Required when `type = ACTION`.

### 6.6 `payload`

Command input payload. Optional. Must be JSON-serializable. Passed to the action handler as-is.

### 6.7 `status`

Current Command status. Required. Values defined in §7.

### 6.8 `createdByUserId`

User who created the Command. Optional (may be null for system-initiated commands). Prefix: `usr_`.

### 6.9 `createdAt`

Command creation timestamp. Required.

### 6.10 `startedAt`

Timestamp when Backend transitioned the Command to RUNNING (set during Agent（代理） polling). Nullable.

### 6.11 `completedAt`

Timestamp when Command reached a terminal state (SUCCEEDED / FAILED / EXPIRED / CANCELLED). Nullable.

### 6.12 `expiresAt`

Expiration timestamp. Recommended. Expired Commands must not be delivered to Agents.

### 6.13 Workspace boundary

`workspaceId` is stored on the database row but is not exposed in the CE（社区版） v0.1 API surface (single default Workspace).

---

## 7. Command 状态 Lifecycle

Allowed Command statuses (CE（社区版） v0.1 baseline, must match `09-contracts/openapi` `CommandStatus`):

```text
PENDING
RUNNING
SUCCEEDED
FAILED
EXPIRED
CANCELLED
```

### 7.1 `PENDING`

Command has been created and is waiting for Agent（代理） delivery.

### 7.2 `RUNNING`

Agent（代理） has polled the Command and is executing it.

Backend transitions `PENDING -> RUNNING` when the Agent（代理） fetches the Command via `GET /api/agents/{agentId}/commands`.

### 7.3 `SUCCEEDED`

Command completed successfully (Agent（代理） reported `success = true`).

### 7.4 `FAILED`

Command execution failed (Agent（代理） reported `success = false`).

Failure should include an error message or structured error in CommandResult.

### 7.5 `EXPIRED`

Command expired before completion.

### 7.6 `CANCELLED`

Command was cancelled before completion.

CE（社区版） v0.1 does not need to implement cancellation UI, but the state must be reserved for future use.

---

## 8. 状态 Transitions

Allowed transitions (CE（社区版） v0.1 baseline):

```text
PENDING   -> RUNNING       (Agent polled the Command)
PENDING   -> EXPIRED       (timeout reached before delivery)
PENDING   -> CANCELLED     (admin cancelled, future)

RUNNING   -> SUCCEEDED     (Agent reported success)
RUNNING   -> FAILED        (Agent reported failure)
RUNNING   -> EXPIRED       (timeout reached during execution)
RUNNING   -> CANCELLED     (future)
```

Invalid transitions must be rejected.

Examples of invalid transitions:

```text
SUCCEEDED -> RUNNING
FAILED    -> SUCCEEDED
EXPIRED   -> SUCCEEDED
CANCELLED -> SUCCEEDED
```

CE（社区版） v0.1 minimum lifecycle:

```text
PENDING -> RUNNING -> SUCCEEDED
PENDING -> RUNNING -> FAILED
PENDING -> EXPIRED
```

---

## 9. Command Creation

Backend creates Commands in response to an authenticated and authorized operation request.

For CE（社区版） v0.1, the main creation path is:

```http
POST /api/admin/capsule-services/{serviceId}/actions/{actionName}
```

Backend responsibilities:

1. authenticate user;
2. validate target service;
3. validate associated Agent（代理）;
4. verify Agent（代理） is not disabled or revoked;
5. verify action exists and is enabled;
6. validate payload if schema is available;
7. check danger level and confirmation policy;
8. create Command;
9. write AuditEvent;
10. return Command summary to UI.

---

## 10. Command Polling

CE（社区版） v0.1 should use polling for command delivery.

Agent（代理） polls Backend:

```http
GET /api/agents/{agentId}/commands
Authorization: Bearer <agentToken>
```

Response (matches OpenAPI `SuccessEnvelope` with `data: Command[]`):

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

Backend responsibilities:

1. authenticate Agent（代理） token;
2. verify Agent（代理） is not disabled or revoked;
3. fetch `PENDING` Commands assigned to Agent（代理）;
4. exclude expired Commands;
5. transition returned Commands from `PENDING` to `RUNNING` and set `startedAt`;
6. return Commands in stable order, usually by `createdAt`.

---

## 11. Command Execution

Agent（代理） receives a Command and executes it locally.

For `ACTION` commands:

1. find Capsule Service（胶囊服务） by `serviceCode`;
2. find registered action handler by `actionName`;
3. pass `payload` to handler;
4. catch errors;
5. build CommandResult;
6. report result to Backend.

Agent（代理） must reject unknown actions.

Unknown action result example (CommandResult report body, see §13):

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

---

## 12. CommandResult Object

CE（社区版） v0.1 CommandResult uses the OpenAPI shape. The Agent（代理） reports `success` (boolean) plus optional `message`, `data`, and `error`. Backend persists these along with timing metadata.

### 12.1 CommandResult report body (Agent（代理） → Backend)

Matches OpenAPI `ReportCommandResultRequest`:

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

### 12.2 Persisted CommandResult fields (matches Prisma `CommandResult`)

```text
id            crs_xxx
commandId     cmd_xxx (unique 1:1)
agentId       agt_xxx
success       boolean
message       string nullable
dataJson      JSON text nullable        (serialized from `data`)
errorJson     JSON text nullable        (serialized from `error`)
reportedAt    datetime
createdAt     datetime
```

The Command row separately tracks `startedAt` (set during polling) and `completedAt` (set when the result is received).

### 12.3 Success Result

```json
{
  "success": true,
  "message": "Action completed.",
  "data": {
    "status": "UP"
  }
}
```

### 12.4 Failed Result

```json
{
  "success": false,
  "message": "Action handler threw an error.",
  "error": {
    "code": "ACTION_FAILED",
    "message": "Action handler threw an error."
  }
}
```

### 12.5 Optional timing fields

The Agent（代理） MAY include `startedAt` and `finishedAt` (ISO-8601). Backend uses them only to refine `Command.startedAt` / `Command.completedAt` if the Agent（代理）'s clock is trustworthy; Backend's own clock is authoritative.

---

## 13. Command Result Reporting

Agent（代理） reports CommandResult to Backend:

```http
POST /api/agents/{agentId}/commands/{commandId}/result
Authorization: Bearer <agentToken>
```

Request body (matches OpenAPI `ReportCommandResultRequest`):

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

Backend responsibilities:

1. authenticate Agent（代理） token;
2. verify Command belongs to authenticated Agent（代理）;
3. reject reports for Commands already in a terminal state (`SUCCEEDED` / `FAILED` / `EXPIRED` / `CANCELLED`);
4. create `CommandResult` row;
5. transition Command status: `RUNNING -> SUCCEEDED` if `success = true`, otherwise `RUNNING -> FAILED`;
6. set `Command.completedAt` to the server clock;
7. write AuditEvent;
8. expose result to UI.

---

## 14. Timeout and Expiration

Commands should have an expiration time.

Recommended CE（社区版） v0.1 defaults:

```text
defaultCommandTtlSeconds = 300
```

Rules:

- expired Commands should not be delivered to Agents;
- Backend may mark expired Commands as `EXPIRED` during polling or periodic cleanup;
- if Agent（代理） reports result after expiration, Backend may reject it or accept it with a warning depending on policy;
- CE（社区版） v0.1 may accept late results if the Command was previously dispatched, but should record actual finish time.

Recommended simple CE（社区版） rule:

```text
If command is PENDING and now > expiresAt:
    mark EXPIRED and do not deliver to Agent

If command is RUNNING and result arrives after expiresAt:
    accept result, but record actual finishedAt and keep audit metadata
```

---

## 15. Idempotency

Idempotency prevents duplicate operations.

CE（社区版） v0.1 may keep idempotency simple.

Recommended behavior:

- store optional `idempotencyKey`;
- avoid creating duplicate active Commands with the same `idempotencyKey` for the same service;
- Agent（代理） should avoid executing the same Command ID twice if it already reported a final result.

Agent（代理）-side rule:

```text
If commandId was already completed locally:
    do not execute again
    report previous result if available
```

Future EE（企业版）/Cloud（云版） may implement stronger idempotency, deduplication, and exactly-once-like semantics.

---

## 16. Ordering

CE（社区版） v0.1 should deliver Commands to an Agent（代理） in creation order.

Recommended ordering:

```text
createdAt ASC
```

CE（社区版） v0.1 does not need complex priority queues.

Future versions may add:

- priority;
- scheduling;
- concurrency limits;
- per-service command ordering;
- resource-level locks.

---

## 17. Concurrency

CE（社区版） v0.1 may keep command execution simple.

Recommended defaults:

```text
Agent may process one command at a time per Capsule Service.
```

Future fields:

```text
priority
concurrencyKey
resourceLockKey
maxRetries
retryPolicy
```

CE（社区版） v0.1 does not need to implement these.

---

## 18. Retry

CE（社区版） v0.1 does not need automatic retry.

If an action fails, the user may manually trigger it again.

Future retry policy may include:

```json
{
  "maxRetries": 3,
  "retryDelaySeconds": 10,
  "retryOn": ["TIMEOUT", "TEMPORARY_FAILURE"]
}
```

Do not implement retry in CE（社区版） v0.1 unless explicitly required.

---

## 19. Audit Events

Commands must be auditable.

Recommended audit events:

```text
command.created
command.dispatched
command.started
command.completed
command.failed
command.expired
command.cancelled
```

CE（社区版） v0.1 minimum audit events:

```text
command.created
command.completed
command.failed
```

Action-related audit events may also be created:

```text
service.action.requested
service.action.completed
service.action.failed
```

---

## 20. UI Requirements

CE（社区版） v0.1 UI should show:

- command status;
- target service;
- action name;
- created time;
- finish time;
- output text;
- error message;
- result JSON if available.

Service detail page should show recent Commands for that service.

Command list page may show all recent Commands.

UI should not expose arbitrary command input beyond predefined action payloads.

---

## 21. Backend Requirements

CE（社区版） v0.1 Backend should implement:

- Command table or equivalent storage;
- CommandResult table or equivalent storage;
- command creation from action request;
- command polling API;
- command result API;
- expiration handling;
- basic status transitions;
- audit events;
- UI query APIs for command list and detail.

---

## 22. Agent（代理） SDK Requirements

CE（社区版） v0.1 Node.js embedded Agent（代理） SDK should implement:

- polling loop;
- command dispatch to local handler;
- unknown action rejection;
- error capture;
- result reporting;
- basic duplicate command protection;
- non-blocking failure behavior.

The Agent（代理） SDK must not include a default arbitrary shell execution handler.

---

## 23. Error Model

Recommended Command-related error codes:

```text
COMMAND_NOT_FOUND
COMMAND_EXPIRED
COMMAND_CANCELLED
COMMAND_NOT_ASSIGNED_TO_AGENT
COMMAND_ALREADY_COMPLETED
ACTION_NOT_FOUND
ACTION_DISABLED
ACTION_FAILED
PAYLOAD_INVALID
AGENT_DISABLED
AGENT_REVOKED
INTERNAL_ERROR
```

Error result shape (CommandResult report body):

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

---

## 24. 安全 Rules

### 24.1 No arbitrary shell execution

CE（社区版） v0.1 must not provide generic shell command execution.

### 24.2 Agent（代理） token required

Agent（代理） command polling and result reporting require a valid Agent（代理） token.

### 24.3 Agent（代理） ownership check

Agent（代理） can only fetch and report Commands assigned to itself.

### 24.4 Validate action existence

Backend should create only action Commands for actions declared by the latest known manifest or action report.

### 24.5 Audit every operation

Command creation and final result should be audited.

### 24.6 Avoid sensitive payload leakage

Command payloads and results should avoid raw secrets.

If a payload must refer to a secret, use `secretRef`.

---

## 25. CE（社区版） v0.1 Required Subset

CE（社区版） v0.1 must implement:

- `ACTION` command type;
- Command creation from UI action request;
- Command polling by Agent（代理） (transitions `PENDING -> RUNNING`);
- CommandResult reporting (transitions `RUNNING -> SUCCEEDED|FAILED`);
- statuses: `PENDING`, `RUNNING`, `SUCCEEDED`, `FAILED`, `EXPIRED`;
- `CANCELLED` reserved (no UI required);
- basic expiration;
- basic audit;
- command list/detail UI;
- no arbitrary shell execution.

CE（社区版） v0.1 does not need to implement:

- WebSocket command delivery;
- gRPC streaming;
- message queue delivery;
- cancellation UI;
- automatic retry;
- scheduling;
- priority queue;
- batch commands;
- command approval workflow;
- resource locking;
- interactive sessions.

---

## 26. Future Extensions

Future EE（企业版）/Cloud（云版） may add:

- WebSocket command channel;
- gRPC streaming;
- reliable queue-based delivery;
- command priority;
- command scheduling;
- command approval;
- retries;
- cancellation;
- command templates;
- resource locks;
- concurrency policies;
- long-running progress updates;
- log streaming;
- interactive operation sessions.

These extensions should build on the same Command and CommandResult model.

---

## 27. Anti-Patterns

Avoid these patterns.

### 27.1 UI directly calling Agent（代理）

All operations should go through Backend-created Commands.

### 27.2 Shell command as default Command type

Do not create generic shell command execution in CE（社区版） v0.1.

### 27.3 Command without audit

Do not create or complete Commands without audit records.

### 27.4 Command without Agent（代理） ownership validation

Do not allow Agents to fetch or update Commands assigned to other Agents.

### 27.5 Infinite pending Commands

Commands should expire.

### 27.6 Treating command result as logs

CommandResult should be concise. Large logs belong to future log collection capabilities.

---

## 28. Summary

Commands are the controlled delivery mechanism for Opstage（运维舞台） operations.

CE（社区版） v0.1 should implement a small but complete Command loop:

```text
UI action request
    ↓
Backend Command
    ↓
Agent polling
    ↓
Local action handler
    ↓
CommandResult
    ↓
AuditEvent
```

This makes Capsule Service（胶囊服务） operations visible, safe, and auditable while keeping CE（社区版） lightweight.

---

## 11. CE v0.1 实现补充：敏感 Payload 与长耗时 Command

### 11.1 Payload 保存与展示

Backend 创建 `ACTION_EXECUTE` Command 时，必须把原始 payload 保存到 `commands.payloadJson`，否则 Agent 无法收到密码、token、API key 等敏感字段。

但 Admin API / UI 展示 Command 时，必须对 payload 做脱敏展示。推荐规则：

```text
agent polling response: raw payload, for execution only
admin command response: redacted payload, for display/audit only
```

示例：

```json
{
  "actionName": "setEmailOtpConfig",
  "payload": {
    "imapUser": "your-inbox@gmail.com",
    "imapPassword": "[REDACTED]"
  }
}
```

### 11.2 长耗时 Command

登录、重建浏览器上下文、账号巡检等动作可能超过普通 UI 等待时间。UI 不应一直阻塞等待这类 Command 完成，而应：

1. 创建 Command 后立即显示 Command id；
2. 后台轮询 Command 列表或服务健康详情；
3. 通过 Capsule Service health details 中的账号状态展示 `RUNNING` / `SUCCEEDED` / `FAILED`；
4. 必要时允许用户在 Commands 页面取消、重试或查看结果。

长耗时 action 应设置合理的 `timeoutSeconds`，例如：

```json
{
  "name": "rebuildAccountContext",
  "timeoutSeconds": 900
}
```
