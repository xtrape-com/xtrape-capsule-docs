# Command Specification

- Status: Draft
- Edition: Shared
- Priority: High
- Audience: backend developers, frontend developers, agent SDK developers, AI coding agents

This document defines the **Command** specification for the `xtrape-capsule` domain.

A Command is an instruction created by Opstage Backend and executed by an authorized Agent. Commands are the delivery mechanism for operational requests such as predefined Capsule Service actions.

In CE v0.1, Commands are primarily used to execute predefined actions through the Node.js embedded Agent SDK.

---

## 1. Purpose

The Command Specification defines:

- what a Command is;
- how Backend creates Commands;
- how Agents fetch Commands;
- how Agents execute Commands;
- how CommandResult is reported;
- Command status lifecycle;
- timeout and expiration behavior;
- idempotency requirements;
- audit requirements;
- CE v0.1 required subset;
- future EE and Cloud extension points.

Commands provide a safe and auditable way for Opstage to operate Capsule Services without giving the UI arbitrary remote execution power.

---

## 2. Core Rule

Opstage UI must not directly call Agents or Capsule Services.

Operational requests should flow through Backend-created Commands.

Correct CE v0.1 flow:

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

CE v0.1 must not support arbitrary shell command execution.

---

## 3. Command Scope

In CE v0.1, a Command should represent one operational instruction targeting one Agent and usually one Capsule Service.

Typical CE command:

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

CE v0.1 should implement only the action-execution command path.

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

CE v0.1 must implement:

```text
ACTION
```

Other command types are reserved for future versions.

### 4.1 `ACTION`

Execute a predefined Capsule Service action.

Example:

```json
{
  "commandType": "ACTION",
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

Reserved for future Agent control operations.

### 4.6 `CUSTOM`

Reserved for future controlled extension.

`CUSTOM` must not become arbitrary shell execution.

---

## 5. Command Object

### 5.1 Minimum CE v0.1 Command

```json
{
  "id": "cmd_001",
  "agentId": "agt_001",
  "serviceId": "svc_001",
  "serviceCode": "demo-capsule-service",
  "commandType": "ACTION",
  "actionName": "runHealthCheck",
  "payload": {},
  "status": "PENDING",
  "createdAt": "2026-04-30T10:22:00Z",
  "expiresAt": "2026-04-30T10:27:00Z"
}
```

### 5.2 Recommended Command

```json
{
  "id": "cmd_001",
  "workspaceId": "wks_default",
  "agentId": "agt_001",
  "serviceId": "svc_001",
  "serviceCode": "demo-capsule-service",
  "commandType": "ACTION",
  "actionName": "refreshSession",
  "payload": {
    "sessionId": "ses_001"
  },
  "status": "PENDING",
  "createdBy": "usr_001",
  "createdAt": "2026-04-30T10:22:00Z",
  "expiresAt": "2026-04-30T10:27:00Z",
  "dispatchedAt": null,
  "startedAt": null,
  "finishedAt": null,
  "idempotencyKey": "cmd-refresh-session-ses-001-20260430",
  "metadata": {
    "source": "ui",
    "dangerLevel": "MEDIUM"
  }
}
```

---

## 6. Command Fields

### 6.1 `id`

Unique Command identifier.

Required.

Recommended prefix:

```text
cmd_
```

### 6.2 `workspaceId`

Workspace boundary.

Required in data model where Workspaces are present.

CE v0.1 may use a default Workspace.

### 6.3 `agentId`

Target Agent that should execute the Command.

Required.

### 6.4 `serviceId`

Target Capsule Service.

Required for service-level commands.

### 6.5 `serviceCode`

Stable service code.

Recommended in Agent-facing payload because it is easier for Agent SDK to route to local service handlers.

### 6.6 `commandType`

Type of Command.

Required.

CE v0.1 supports:

```text
ACTION
```

### 6.7 `actionName`

Name of the action to execute.

Required when `commandType = ACTION`.

### 6.8 `payload`

Command input payload.

Optional.

For action commands, this is passed to the action handler.

Must be JSON-serializable.

### 6.9 `status`

Current Command status.

Required.

Allowed values are defined in the status lifecycle section.

### 6.10 `createdBy`

User or system actor that created the Command.

CE v0.1 may store a user id or `system`.

### 6.11 `createdAt`

Command creation timestamp.

Required.

### 6.12 `expiresAt`

Expiration timestamp.

Required or recommended.

Expired Commands should not be delivered to Agents.

### 6.13 `dispatchedAt`

Timestamp when Backend delivered the Command to Agent.

Optional.

### 6.14 `startedAt`

Timestamp when execution started.

May be reported by Agent.

### 6.15 `finishedAt`

Timestamp when execution finished.

May be reported by Agent.

### 6.16 `idempotencyKey`

Optional key used to avoid duplicate command creation or duplicate execution.

CE v0.1 may store this field but does not need a full idempotency engine.

### 6.17 `metadata`

Optional free-form metadata.

Examples:

```json
{
  "source": "ui",
  "dangerLevel": "LOW"
}
```

---

## 7. Command Status Lifecycle

Allowed Command statuses:

```text
PENDING
DISPATCHED
RUNNING
SUCCESS
FAILED
EXPIRED
CANCELLED
```

### 7.1 `PENDING`

Command has been created and is waiting for Agent delivery.

### 7.2 `DISPATCHED`

Command has been delivered to Agent through polling or another channel.

### 7.3 `RUNNING`

Agent has started executing the Command.

CE v0.1 may skip this state if execution is short and the Agent reports only final result.

### 7.4 `SUCCESS`

Command completed successfully.

### 7.5 `FAILED`

Command execution failed.

Failure should include an error message or structured error in CommandResult.

### 7.6 `EXPIRED`

Command expired before completion.

### 7.7 `CANCELLED`

Command was cancelled before completion.

CE v0.1 does not need to implement cancellation UI.

---

## 8. Status Transitions

Recommended transitions:

```text
PENDING -> DISPATCHED
PENDING -> EXPIRED
PENDING -> CANCELLED

DISPATCHED -> RUNNING
DISPATCHED -> SUCCESS
DISPATCHED -> FAILED
DISPATCHED -> EXPIRED

RUNNING -> SUCCESS
RUNNING -> FAILED
RUNNING -> EXPIRED
RUNNING -> CANCELLED
```

Invalid transitions should be rejected or ignored.

Examples of invalid transitions:

```text
SUCCESS -> RUNNING
FAILED -> SUCCESS
EXPIRED -> SUCCESS
CANCELLED -> SUCCESS
```

CE v0.1 may implement a simplified lifecycle:

```text
PENDING -> DISPATCHED -> SUCCESS
PENDING -> DISPATCHED -> FAILED
PENDING -> EXPIRED
```

---

## 9. Command Creation

Backend creates Commands in response to an authenticated and authorized operation request.

For CE v0.1, the main creation path is:

```http
POST /api/admin/capsule-services/{serviceId}/actions/{actionName}
```

Backend responsibilities:

1. authenticate user;
2. validate target service;
3. validate associated Agent;
4. verify Agent is not disabled or revoked;
5. verify action exists and is enabled;
6. validate payload if schema is available;
7. check danger level and confirmation policy;
8. create Command;
9. write AuditEvent;
10. return Command summary to UI.

---

## 10. Command Polling

CE v0.1 should use polling for command delivery.

Agent polls Backend:

```http
GET /api/agents/{agentId}/commands
Authorization: Bearer <agentToken>
```

Response:

```json
{
  "commands": [
    {
      "commandId": "cmd_001",
      "serviceId": "svc_001",
      "serviceCode": "demo-capsule-service",
      "commandType": "ACTION",
      "actionName": "runHealthCheck",
      "payload": {},
      "issuedAt": "2026-04-30T10:22:00Z",
      "expiresAt": "2026-04-30T10:27:00Z"
    }
  ]
}
```

Backend responsibilities:

1. authenticate Agent token;
2. verify Agent is active;
3. fetch pending Commands assigned to Agent;
4. exclude expired Commands;
5. mark delivered Commands as `DISPATCHED` if appropriate;
6. return Commands in stable order, usually by `createdAt`.

---

## 11. Command Execution

Agent receives a Command and executes it locally.

For `ACTION` commands:

1. find Capsule Service by `serviceCode`;
2. find registered action handler by `actionName`;
3. pass `payload` to handler;
4. catch errors;
5. build CommandResult;
6. report result to Backend.

Agent must reject unknown actions.

Unknown action result example:

```json
{
  "status": "FAILED",
  "errorMessage": "Action not found: refreshSession",
  "resultJson": {
    "errorCode": "ACTION_NOT_FOUND"
  }
}
```

---

## 12. CommandResult Object

### 12.1 Minimum CommandResult

```json
{
  "commandId": "cmd_001",
  "status": "SUCCESS",
  "outputText": "Health check completed.",
  "resultJson": {
    "status": "UP"
  },
  "startedAt": "2026-04-30T10:22:01Z",
  "finishedAt": "2026-04-30T10:22:02Z"
}
```

### 12.2 Recommended CommandResult Fields

```text
id
workspaceId
commandId
agentId
serviceId
status
outputText
errorMessage
resultJson
startedAt
finishedAt
createdAt
```

### 12.3 Success Result

```json
{
  "status": "SUCCESS",
  "outputText": "Action completed.",
  "resultJson": {
    "success": true,
    "message": "Action completed.",
    "data": {}
  }
}
```

### 12.4 Failed Result

```json
{
  "status": "FAILED",
  "outputText": "Action failed.",
  "errorMessage": "Action handler threw an error.",
  "resultJson": {
    "success": false,
    "error": {
      "code": "ACTION_FAILED",
      "message": "Action handler threw an error."
    }
  }
}
```

---

## 13. Command Result Reporting

Agent reports CommandResult to Backend:

```http
POST /api/agents/{agentId}/commands/{commandId}/result
Authorization: Bearer <agentToken>
```

Request:

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

Backend responsibilities:

1. authenticate Agent token;
2. verify Command belongs to Agent;
3. verify Command is not terminal if strict transition is enforced;
4. store CommandResult;
5. update Command status;
6. set `finishedAt` if provided;
7. write AuditEvent;
8. expose result to UI.

---

## 14. Timeout and Expiration

Commands should have an expiration time.

Recommended CE v0.1 defaults:

```text
defaultCommandTtlSeconds = 300
```

Rules:

- expired Commands should not be delivered to Agents;
- Backend may mark expired Commands as `EXPIRED` during polling or periodic cleanup;
- if Agent reports result after expiration, Backend may reject it or accept it with a warning depending on policy;
- CE v0.1 may accept late results if the Command was previously dispatched, but should record actual finish time.

Recommended simple CE rule:

```text
If command is PENDING and now > expiresAt:
    mark EXPIRED and do not dispatch

If command is DISPATCHED and result arrives late:
    accept result but keep audit metadata
```

---

## 15. Idempotency

Idempotency prevents duplicate operations.

CE v0.1 may keep idempotency simple.

Recommended behavior:

- store optional `idempotencyKey`;
- avoid creating duplicate active Commands with the same `idempotencyKey` for the same service;
- Agent should avoid executing the same Command ID twice if it already reported a final result.

Agent-side rule:

```text
If commandId was already completed locally:
    do not execute again
    report previous result if available
```

Future EE/Cloud may implement stronger idempotency, deduplication, and exactly-once-like semantics.

---

## 16. Ordering

CE v0.1 should deliver Commands to an Agent in creation order.

Recommended ordering:

```text
createdAt ASC
```

CE v0.1 does not need complex priority queues.

Future versions may add:

- priority;
- scheduling;
- concurrency limits;
- per-service command ordering;
- resource-level locks.

---

## 17. Concurrency

CE v0.1 may keep command execution simple.

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

CE v0.1 does not need to implement these.

---

## 18. Retry

CE v0.1 does not need automatic retry.

If an action fails, the user may manually trigger it again.

Future retry policy may include:

```json
{
  "maxRetries": 3,
  "retryDelaySeconds": 10,
  "retryOn": ["TIMEOUT", "TEMPORARY_FAILURE"]
}
```

Do not implement retry in CE v0.1 unless explicitly required.

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

CE v0.1 minimum audit events:

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

CE v0.1 UI should show:

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

CE v0.1 Backend should implement:

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

## 22. Agent SDK Requirements

CE v0.1 Node.js embedded Agent SDK should implement:

- polling loop;
- command dispatch to local handler;
- unknown action rejection;
- error capture;
- result reporting;
- basic duplicate command protection;
- non-blocking failure behavior.

The Agent SDK must not include a default arbitrary shell execution handler.

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

Error result shape:

```json
{
  "status": "FAILED",
  "errorMessage": "Action not found: refreshSession",
  "resultJson": {
    "success": false,
    "error": {
      "code": "ACTION_NOT_FOUND",
      "message": "Action not found: refreshSession"
    }
  }
}
```

---

## 24. Security Rules

### 24.1 No arbitrary shell execution

CE v0.1 must not provide generic shell command execution.

### 24.2 Agent token required

Agent command polling and result reporting require a valid Agent token.

### 24.3 Agent ownership check

Agent can only fetch and report Commands assigned to itself.

### 24.4 Validate action existence

Backend should create only action Commands for actions declared by the latest known manifest or action report.

### 24.5 Audit every operation

Command creation and final result should be audited.

### 24.6 Avoid sensitive payload leakage

Command payloads and results should avoid raw secrets.

If a payload must refer to a secret, use `secretRef`.

---

## 25. CE v0.1 Required Subset

CE v0.1 must implement:

- `ACTION` command type;
- Command creation from UI action request;
- Command polling by Agent;
- CommandResult reporting;
- statuses: `PENDING`, `DISPATCHED`, `SUCCESS`, `FAILED`, `EXPIRED`;
- basic expiration;
- basic audit;
- command list/detail UI;
- no arbitrary shell execution.

CE v0.1 does not need to implement:

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

Future EE/Cloud may add:

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

### 27.1 UI directly calling Agent

All operations should go through Backend-created Commands.

### 27.2 Shell command as default Command type

Do not create generic shell command execution in CE v0.1.

### 27.3 Command without audit

Do not create or complete Commands without audit records.

### 27.4 Command without Agent ownership validation

Do not allow Agents to fetch or update Commands assigned to other Agents.

### 27.5 Infinite pending Commands

Commands should expire.

### 27.6 Treating command result as logs

CommandResult should be concise. Large logs belong to future log collection capabilities.

---

## 28. Summary

Commands are the controlled delivery mechanism for Opstage operations.

CE v0.1 should implement a small but complete Command loop:

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

This makes Capsule Service operations visible, safe, and auditable while keeping CE lightweight.
