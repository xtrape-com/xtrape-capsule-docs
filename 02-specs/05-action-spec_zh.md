<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 05-action-spec.md
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

# Action 规范

- Status: 规范
- Edition: 共享
- Priority: 高
- Audience: backend developers, frontend developers, agent SDK developers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/` (OpenAPI / Prisma) disagree, the ADRs and contracts win for CE（社区版） v0.1.

This document 定义 the shared Action model for the `xtrape-capsule` domain.

An **Action** is a predefined operation exposed by a Capsule Service（胶囊服务） and executed through an authorized Agent（代理） under Opstage（运维舞台） governance.

Actions are the safe operational interface between Opstage（运维舞台） and Capsule Services.

---

## 1. Purpose

The Action 规范 定义:

- how Capsule Services describe executable actions;
- how Opstage（运维舞台） displays actions in the UI;
- how Backend creates commands for action execution;
- how Agents execute actions;
- how action results are reported;
- how actions are audited;
- what CE（社区版） v0.1 must implement;
- what future EE（企业版） and Cloud（云版） editions may extend.

The Action model must prevent unsafe remote operation patterns, especially arbitrary shell execution in CE（社区版） v0.1.

---

## 2. Core Rule

Actions must be:

- explicit;
- predefined;
- named;
- typed;
- permission-checkable;
- auditable;
- executed through an Agent（代理）;
- associated with a Capsule Service（胶囊服务）.

CE（社区版） v0.1 must not expose arbitrary command execution from the UI.

Correct model:

```text
User clicks predefined action in UI
    ↓
Backend creates Command
    ↓
Agent fetches Command
    ↓
Agent invokes predefined action handler
    ↓
Agent reports CommandResult
    ↓
Backend writes AuditEvent
```

Incorrect model:

```text
User types shell command in UI
    ↓
Backend sends arbitrary command to Agent
    ↓
Agent executes shell directly
```

---

## 3. ActionDefinition

An **ActionDefinition** 描述 an action that a Capsule Service（胶囊服务） 支持.

The ActionDefinition may be reported by:

- the embedded Agent（代理） SDK;
- the Capsule manifest;
- a Capsule management endpoint;
- future sidecar or external Agent（代理） configuration.

### 3.1 Minimum CE（社区版） v0.1 ActionDefinition

```json
{
  "name": "runHealthCheck",
  "label": "Run Health Check",
  "description": "Run a manual health check for this Capsule Service.",
  "dangerLevel": "LOW",
  "enabled": true
}
```

### 3.2 Recommended Full ActionDefinition

```json
{
  "name": "refreshSession",
  "label": "Refresh Session",
  "description": "Refresh the selected account session.",
  "dangerLevel": "MEDIUM",
  "enabled": true,
  "inputSchema": {
    "type": "object",
    "properties": {
      "sessionId": {
        "type": "string",
        "title": "Session ID"
      }
    },
    "required": ["sessionId"]
  },
  "resultSchema": {
    "type": "object",
    "properties": {
      "refreshed": { "type": "boolean" },
      "expiresAt": { "type": "string" }
    }
  },
  "requiresConfirmation": true,
  "timeoutSeconds": 60,
  "metadata": {
    "category": "session",
    "icon": "refresh"
  }
}
```

---

## 4. ActionDefinition Fields

### 4.1 `name`

Stable technical name of the action.

Rules:

- required;
- camelCase is recommended;
- unique within one Capsule Service（胶囊服务）;
- should be stable across versions;
- should describe intent, not implementation.

Good examples:

```text
runHealthCheck
reloadConfig
refreshSession
clearExpiredSessions
rotateProxy
disableAccount
```

Bad examples:

```text
exec
runShell
bash
cmd1
doIt
```

### 4.2 `label`

Human-readable label displayed in UI.

Rules:

- required for UI display;
- may be localized in future versions;
- should be short and action-oriented.

Examples:

```text
Run Health Check
Reload Config
Refresh Session
Clear Expired Sessions
```

### 4.3 `description`

Optional human-readable explanation of the action.

The description should help the operator understand:

- what the action does;
- whether it is safe;
- when it should be used;
- what resource it affects.

### 4.4 `dangerLevel`

The operational risk level of the action.

CE（社区版） v0.1 allowed values (must match OpenAPI `DangerLevel`):

```text
LOW
MEDIUM
HIGH
```

Recommended meaning:

||Level|Meaning|Examples||
|---|---|---|
||LOW|Read-only or low-risk operation|`runHealthCheck`||
||MEDIUM|Changes local runtime state but is usually safe|`reloadConfig`, `refreshSession`||
||HIGH|May disrupt service behavior, user resources, or cause data loss / credential reset|`clearExpiredSessions`, `disableAccount`, `purgeData`||

`CRITICAL` is reserved for future EE（企业版）/Cloud（云版） editions and is **not** part of CE（社区版） v0.1.

CE（社区版） v0.1 should display `dangerLevel` in UI and require confirmation for `HIGH` actions.

### 4.5 `enabled`

Whether this action is currently available.

If `enabled` is false, UI should display the action as disabled or hide it.

### 4.6 `inputSchema`

Optional JSON-schema-like definition for action input.

CE（社区版） v0.1 may support only simple object input or no input.

Future versions may use this schema to generate dynamic UI forms.

### 4.7 `resultSchema`

Optional JSON-schema-like definition for structured action result.

CE（社区版） v0.1 may store result as JSON without strict validation.

### 4.8 `requiresConfirmation`

Whether UI should ask for confirmation before creating a command.

Recommended default:

```text
LOW      false
MEDIUM   false or true depending on action
HIGH     true
```

(Older drafts called this field `confirmRequired`. The CE（社区版） v0.1 contract name is `requiresConfirmation` — see OpenAPI `ActionDefinition`.)

### 4.9 `timeoutSeconds`

Optional maximum expected execution duration.

If omitted, Backend may use a default timeout.

CE（社区版） v0.1 may store this value but does not need advanced timeout enforcement.

### 4.10 `metadata`

Optional free-form metadata for UI or future extensions.

Examples:

```json
{
  "category": "session",
  "icon": "refresh",
  "uiOrder": 10
}
```

---

## 5. Action Execution Model

Actions are not executed directly by Opstage（运维舞台） Backend.

Opstage（运维舞台） Backend creates a Command, and the Agent（代理） executes the action.

```text
UI
  ↓ request action execution
Backend
  ↓ create Command
Agent
  ↓ execute action handler
Capsule Service
  ↓ return result
Agent
  ↓ report CommandResult
Backend
  ↓ update status and audit
UI
  ↓ show result
```

---

## 6. Command Mapping

Every action execution request should create a Command. Field names match OpenAPI `Command`.

```json
{
  "type": "ACTION",
  "actionName": "runHealthCheck",
  "serviceId": "svc_001",
  "agentId": "agt_001",
  "payload": {},
  "status": "PENDING",
  "expiresAt": "2026-04-30T10:30:00Z"
}
```

The Agent（代理） polls this Command (transitioning it to `RUNNING`), maps `actionName` to a local handler, executes it, and reports a CommandResult.

---

## 7. Action Request

The UI should not call Agent（代理） directly.

The UI requests action execution from Backend.

Example Admin API:

```http
POST /api/admin/capsule-services/{serviceId}/actions/{actionName}
```

Request body:

```json
{
  "payload": {
    "sessionId": "ses_001"
  }
}
```

Backend responsibilities:

1. authenticate user;
2. check service exists;
3. check service is manageable;
4. check action exists and is enabled;
5. validate payload if schema exists;
6. check action danger level and confirmation policy;
7. create Command;
8. write AuditEvent;
9. return Command summary to UI.

---

## 8. Action Handler

In embedded Agent（代理） mode, an action handler is registered inside the Capsule Service（胶囊服务） process.

Example TypeScript shape:

```ts
export type CapsuleActionHandler = (payload: unknown, context: CapsuleActionContext) => Promise<CapsuleActionResult>;

export interface CapsuleActionContext {
  actionName: string;
  commandId: string;
  serviceCode: string;
  agentId: string;
  requestedAt: string;
}

export interface CapsuleActionResult {
  success: boolean;
  message?: string;
  data?: unknown;
}
```

Example registration:

```ts
agent.registerAction({
  name: 'runHealthCheck',
  label: 'Run Health Check',
  dangerLevel: 'LOW',
  handler: async () => {
    const health = await checkHealth();
    return {
      success: true,
      message: 'Health check completed.',
      data: health,
    };
  },
});
```

CE（社区版） v0.1 does not need to finalize this exact TypeScript API, but the SDK design should follow this shape.

---

## 9. Action Result

An **ActionResult** is the structured result returned by an action handler.

Recommended shape:

```json
{
  "success": true,
  "message": "Session refreshed successfully.",
  "data": {
    "sessionId": "ses_001",
    "expiresAt": "2026-05-01T10:00:00Z"
  }
}
```

If the action fails:

```json
{
  "success": false,
  "message": "Session refresh failed.",
  "error": {
    "code": "SESSION_EXPIRED",
    "message": "The session is already expired and cannot be refreshed."
  }
}
```

The Agent（代理） should wrap ActionResult into CommandResult before reporting to Backend.

---

## 10. CommandResult Mapping

A completed action produces a CommandResult report (matches OpenAPI `ReportCommandResultRequest`).

Successful example:

```json
{
  "success": true,
  "message": "Session refreshed successfully.",
  "data": {
    "sessionId": "ses_001",
    "expiresAt": "2026-05-01T10:00:00Z"
  }
}
```

Failed example:

```json
{
  "success": false,
  "message": "The session is already expired and cannot be refreshed.",
  "error": {
    "code": "SESSION_EXPIRED",
    "message": "The session is already expired and cannot be refreshed."
  }
}
```

Backend transitions the Command to `SUCCEEDED` (when `success = true`) or `FAILED` (when `success = false`), records `Command.completedAt`, and writes an AuditEvent.

---

## 11. Action 状态

Actions themselves are definitions. Execution status belongs to Command and CommandResult.

Do not create separate long-running ActionExecution status unless future requirements justify it.

Use Command statuses (CE（社区版） v0.1 baseline):

```text
PENDING
RUNNING
SUCCEEDED
FAILED
EXPIRED
CANCELLED
```

---

## 12. Auditing

Every action request and result should be auditable.

Recommended audit event names (`AuditEvent.action`):

```text
service.action.requested
service.action.completed
service.action.failed
```

Minimum CE（社区版） v0.1 AuditEvent fields (matches OpenAPI `AuditEvent` and Prisma `AuditEvent`):

```text
actorType    USER | AGENT | SYSTEM
actorId      string nullable
action       string
targetType   string nullable
targetId     string nullable
result       SUCCESS | FAILURE
message      string nullable
metadata     JSON object nullable
createdAt    datetime
```

Example:

```json
{
  "actorType": "USER",
  "actorId": "usr_001",
  "action": "service.action.requested",
  "targetType": "CapsuleService",
  "targetId": "svc_001",
  "result": "SUCCESS",
  "message": "Requested action runHealthCheck on demo-capsule-service.",
  "metadata": {
    "actionName": "runHealthCheck",
    "payload": {}
  }
}
```

---

## 13. Permission Model

CE（社区版） v0.1 may implement a simple local admin model.

However, ActionDefinition and Command should be designed so that future permission checks can be added.

Future permission dimensions:

- workspace;
- service;
- action name;
- danger level;
- user role;
- Agent（代理） permission;
- environment;
- approval requirement.

CE（社区版） v0.1 minimum rule:

> Only authenticated admin users can request action execution.

---

## 14. Safety Rules

### 14.1 No arbitrary shell execution in CE（社区版） v0.1

CE（社区版） v0.1 must not provide a generic shell execution feature from UI.

### 14.2 Predefined handlers only

The Agent（代理） should execute only registered action handlers.

### 14.3 Validate action existence

Backend must verify that the action exists in the latest known ActionDefinition list before creating a Command.

### 14.4 Validate service manageability

Backend must verify that:

- the service exists;
- the service has an associated Agent（代理）;
- the Agent（代理） is not revoked or disabled;
- the service is not disabled;
- the command can be delivered or queued.

### 14.5 Confirm dangerous actions

UI should require confirmation for `HIGH` actions or any action with `requiresConfirmation = true`.

### 14.6 Audit every action

Every action request should generate an AuditEvent.

Every action result should update or create an AuditEvent or related audit record.

---

## 15. CE（社区版） v0.1 Required Actions

The demo Capsule Service（胶囊服务） should implement at least these actions:

### 15.1 `runHealthCheck`

Purpose:

- manually trigger a health check;
- return a health result.

Danger level:

```text
LOW
```

Input:

```json
{}
```

Result:

```json
{
  "status": "UP",
  "details": {}
}
```

### 15.2 `echo`

Purpose:

- verify command/action roundtrip;
- useful for demo and testing.

Danger level:

```text
LOW
```

Input:

```json
{
  "message": "hello"
}
```

Result:

```json
{
  "message": "hello"
}
```

`echo` may be removed from production examples later, but it is useful for CE（社区版） v0.1 validation.

---

## 16. Optional Future Actions

The following actions are examples for future Capsule Services.

### 16.1 Session actions

```text
refreshSession
clearExpiredSessions
revokeSession
```

### 16.2 Config actions

```text
reloadConfig
validateConfig
```

### 16.3 Account actions

```text
disableAccount
markAccountRisky
refreshAccountQuota
```

### 16.4 Worker actions

```text
pauseWorker
resumeWorker
retryFailedJob
clearQueue
```

### 16.5 Connector actions

```text
testConnection
refreshToken
syncMetadata
```

---

## 17. UI Requirements

CE（社区版） v0.1 UI should support:

- listing available actions on service detail page;
- showing action label and danger level;
- disabling unavailable actions;
- requesting confirmation for dangerous actions;
- submitting action payload if simple input is needed;
- showing created Command status;
- showing final CommandResult.

CE（社区版） v0.1 UI may keep input handling simple. Dynamic schema-based forms can be added later.

---

## 18. Backend Requirements

CE（社区版） v0.1 Backend should support:

- storing ActionDefinitions from service report or manifest;
- exposing actions to UI;
- creating Commands for action requests;
- exposing pending commands to Agent（代理）;
- receiving CommandResults;
- updating Command status;
- writing AuditEvents.

---

## 19. Agent（代理） SDK Requirements

CE（社区版） v0.1 Node.js embedded Agent（代理） SDK should support:

- action registration;
- action metadata reporting;
- command polling;
- action handler invocation;
- error capture;
- command result reporting.

The SDK should not expose a default arbitrary shell execution action.

---

## 20. Compatibility Rules

- New optional fields may be added to ActionDefinition.
- Existing stable fields should not change meaning.
- Unknown fields should be ignored by older clients where possible.
- EE（企业版） and Cloud（云版） may add permission, approval, scheduling, and workflow metadata.
- CE（社区版） should not be forced to implement advanced EE（企业版）/Cloud（云版） fields.

---

## 21. Anti-Patterns

Avoid these patterns:

### 21.1 Generic shell action

Do not define a generic `runShell` or `exec` action in CE（社区版） v0.1.

### 21.2 Hidden high-risk action

Do not mark a destructive action as `LOW` risk.

### 21.3 Backend-side business action implementation

Do not implement Capsule-specific business logic directly in Backend.

### 21.4 Untracked action execution

Do not execute an action without Command and AuditEvent records.

### 21.5 Agent（代理） executing unknown action

The Agent（代理） must reject commands for unknown or unregistered actions.

---

## 22. Summary

Actions are the safe operational interface between Opstage（运维舞台） and Capsule Services.

CE（社区版） v0.1 should implement a small but complete Action loop:

```text
ActionDefinition
    ↓
UI Action Button
    ↓
Backend Command
    ↓
Agent Action Handler
    ↓
CommandResult
    ↓
AuditEvent
```

This loop proves that Capsule Services can be operated through Opstage（运维舞台） without exposing arbitrary remote command execution.
