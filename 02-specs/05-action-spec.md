# Action Specification

- Status: Specification
- Edition: Shared
- Priority: High
- Audience: backend developers, frontend developers, agent SDK developers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/` (OpenAPI / Prisma) disagree, the ADRs and contracts win for CE v0.1.

This document defines the shared Action model for the `xtrape-capsule` domain.

An **Action** is a predefined operation exposed by a Capsule Service and executed through an authorized Agent under Opstage governance.

Actions are the safe operational interface between Opstage and Capsule Services.

---

## 1. Purpose

The Action Specification defines:

- how Capsule Services describe executable actions;
- how Opstage displays actions in the UI;
- how Backend creates commands for action execution;
- how Agents execute actions;
- how action results are reported;
- how actions are audited;
- what CE v0.1 must implement;
- what future EE and Cloud editions may extend.

The Action model must prevent unsafe remote operation patterns, especially arbitrary shell execution in CE v0.1.

---

## 2. Core Rule

Actions must be:

- explicit;
- predefined;
- named;
- typed;
- permission-checkable;
- auditable;
- executed through an Agent;
- associated with a Capsule Service.

CE v0.1 must not expose arbitrary command execution from the UI.

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

An **ActionDefinition** describes an action that a Capsule Service supports.

The ActionDefinition may be reported by:

- the embedded Agent SDK;
- the Capsule manifest;
- a Capsule management endpoint;
- future sidecar or external Agent configuration.

### 3.1 Minimum CE v0.1 ActionDefinition

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
- unique within one Capsule Service;
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

CE v0.1 allowed values (must match OpenAPI `DangerLevel`):

```text
LOW
MEDIUM
HIGH
```

Recommended meaning:

| Level | Meaning | Examples |
|---|---|---|
| LOW | Read-only or low-risk operation | `runHealthCheck` |
| MEDIUM | Changes local runtime state but is usually safe | `reloadConfig`, `refreshSession` |
| HIGH | May disrupt service behavior, user resources, or cause data loss / credential reset | `clearExpiredSessions`, `disableAccount`, `purgeData` |

`CRITICAL` is reserved for future EE/Cloud editions and is **not** part of CE v0.1.

CE v0.1 should display `dangerLevel` in UI and require confirmation for `HIGH` actions.

### 4.5 `enabled`

Whether this action is currently available.

If `enabled` is false, UI should display the action as disabled or hide it.

### 4.6 `inputSchema`

Optional JSON-schema-like definition for action input.

CE v0.1 supports simple object input and common UI hints for generated forms. Services MAY include these field-level hints in `inputSchema.properties`:

| Hint | Type | Meaning |
|---|---|---|
| `title` | string | Human-readable field label. |
| `description` | string | Tooltip/help text. |
| `default` | any | Initial value used by prepare/UI. |
| `enum` + `enumLabels` | array | Select options and optional display labels. |
| `format: "password"` | string | Render as a password/secret input. |
| `format: "textarea"` | string | Render as a multi-line text input. |
| `placeholder` | string | Input placeholder. |
| `readOnly` | boolean | Render as read-only where supported. |
| `maxLength` | number | Input maximum length where supported. |

Future versions may use this schema to generate richer dynamic UI forms.

These hints only affect the console rendering and operator experience. The
service MUST still validate all submitted payloads when executing the action.

### 4.7 `resultSchema`

Optional JSON-schema-like definition for structured action result.

CE v0.1 may store result as JSON without strict validation.

### 4.8 `requiresConfirmation`

Whether UI should ask for confirmation before creating a command.

Recommended default:

```text
LOW      false
MEDIUM   false or true depending on action
HIGH     true
```

(Older drafts called this field `confirmRequired`. The CE v0.1 contract name is `requiresConfirmation` — see OpenAPI `ActionDefinition`.)

### 4.9 `timeoutSeconds`

Optional maximum expected execution duration.

If omitted, Backend may use a default timeout.

CE v0.1 may store this value but does not need advanced timeout enforcement.

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

Actions are not executed directly by Opstage Backend.

Opstage Backend creates a Command, and the Agent executes the action.

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

The Agent polls this Command (transitioning it to `RUNNING`), maps `actionName` to a local handler, executes it, and reports a CommandResult.

---

## 7. Action Request

The UI should not call Agent directly.

The UI uses the same Action resource URL for two different phases, separated by HTTP method.

```http
GET  /api/admin/capsule-services/{serviceId}/actions/{actionName}
POST /api/admin/capsule-services/{serviceId}/actions/{actionName}
```

| Method | Phase | Creates Command | Purpose |
|---|---|---:|---|
| `GET` | Prepare / open action panel | Yes: `ACTION_PREPARE` | Record the preparation command, return action metadata, `inputSchema`, `initialPayload`, and optional current state for UI rendering. |
| `POST` | Execute / run action | Yes: `ACTION_EXECUTE` | Validate payload, create a durable execution Command, and let the Agent execute it. |

Service reports should treat `actions` as an **Action Catalog**. The catalog is intentionally stable and should only contain button/list metadata: `name`, `label`, `description`, `dangerLevel`, `requiresConfirmation`, `category`, `order`, and optional timeout/display metadata. Dynamic form details such as `inputSchema`, enum options, default values, account lists, and current runtime state should be returned by the `GET` prepare phase, not by periodic service report.

Recommended catalog display fields:

| Field | Purpose |
|---|---|
| `category` | Stable UI grouping key, e.g. `account`, `session`, `runtime-config`, `diagnostics`, `advanced`. |
| `order` | Stable numeric order within a category. Lower values appear first. |

### 7.1 Prepare Action Panel

`GET` must be side-effect free with respect to service operation. It records an `ACTION_PREPARE` Command and dispatches it to the Agent prepare handler so dynamic metadata can be generated at open time. The prepare handler must be side-effect free for service operation and must not run the action execution handler.

Example response:

```json
{
  "action": {
    "name": "refreshSession",
    "label": "Refresh Session",
    "requiresConfirmation": true,
    "inputSchema": {
      "type": "object",
      "required": ["sessionId"],
      "properties": {
        "sessionId": { "type": "string", "title": "Session ID" }
      }
    }
  },
  "initialPayload": {
    "sessionId": ""
  },
  "currentState": {
    "service": { "id": "svc_001", "status": "HEALTHY" }
  },
  "prepareCommand": {
    "id": "cmd_prepare_001",
    "type": "ACTION_PREPARE",
    "status": "SUCCEEDED"
  }
}
```

`initialPayload` should be generated by the Agent prepare handler from current state and `inputSchema` defaults when possible. Dynamic enum values, account choices, and contextual hints belong in this prepare response.

If prepare fails or times out, Backend SHOULD return a normal error envelope and include non-sensitive `error.details` that help the console diagnose the problem. Recommended details include `commandId`, `commandStatus`, `actionName`, `agentId`, and `serviceId`. UI MAY keep the action panel open and offer a retry button based on these details.

### 7.2 Execute Action

The UI requests action execution from Backend using `POST`. `POST` creates an `ACTION_EXECUTE` Command that is eligible for Agent polling/execution.

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

In embedded Agent mode, an action handler is registered inside the Capsule Service process.

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

CE v0.1 does not need to finalize this exact TypeScript API, but the SDK design should follow this shape.

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

The Agent should wrap ActionResult into CommandResult before reporting to Backend.

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

## 11. Action Status

Actions themselves are definitions. Execution status belongs to Command and CommandResult.

Do not create separate long-running ActionExecution status unless future requirements justify it.

Use Command statuses (CE v0.1 baseline):

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

Minimum CE v0.1 AuditEvent fields (matches OpenAPI `AuditEvent` and Prisma `AuditEvent`):

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

CE v0.1 may implement a simple local admin model.

However, ActionDefinition and Command should be designed so that future permission checks can be added.

Future permission dimensions:

- workspace;
- service;
- action name;
- danger level;
- user role;
- Agent permission;
- environment;
- approval requirement.

CE v0.1 minimum rule:

> Only authenticated admin users can request action execution.

---

## 14. Safety Rules

### 14.1 No arbitrary shell execution in CE v0.1

CE v0.1 must not provide a generic shell execution feature from UI.

### 14.2 Predefined handlers only

The Agent should execute only registered action handlers.

### 14.3 Validate action existence

Backend must verify that the action exists in the latest known ActionDefinition list before creating a Command.

### 14.4 Validate service manageability

Backend must verify that:

- the service exists;
- the service has an associated Agent;
- the Agent is not revoked or disabled;
- the service is not disabled;
- the command can be delivered or queued.

### 14.5 Confirm dangerous actions

UI should require confirmation for `HIGH` actions or any action with `requiresConfirmation = true`.

### 14.6 Audit every action

Every action request should generate an AuditEvent.

Every action result should update or create an AuditEvent or related audit record.

---

## 15. CE v0.1 Required Actions

The demo Capsule Service should implement at least these actions:

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

`echo` may be removed from production examples later, but it is useful for CE v0.1 validation.

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

CE v0.1 UI should support:

- listing available actions on service detail page;
- showing action label and danger level;
- disabling unavailable actions;
- requesting confirmation for dangerous actions;
- submitting action payload if simple input is needed;
- showing created Command status;
- showing final CommandResult.

CE v0.1 UI may keep input handling simple. Dynamic schema-based forms can be added later.

---

## 18. Backend Requirements

CE v0.1 Backend should support:

- storing ActionDefinitions from service report or manifest;
- exposing actions to UI;
- creating Commands for action requests;
- exposing pending commands to Agent;
- receiving CommandResults;
- updating Command status;
- writing AuditEvents.

---

## 19. Agent SDK Requirements

CE v0.1 Node.js embedded Agent SDK should support:

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
- EE and Cloud may add permission, approval, scheduling, and workflow metadata.
- CE should not be forced to implement advanced EE/Cloud fields.

---

## 21. Anti-Patterns

Avoid these patterns:

### 21.1 Generic shell action

Do not define a generic `runShell` or `exec` action in CE v0.1.

### 21.2 Hidden high-risk action

Do not mark a destructive action as `LOW` risk.

### 21.3 Backend-side business action implementation

Do not implement Capsule-specific business logic directly in Backend.

### 21.4 Untracked action execution

Do not execute an action without Command and AuditEvent records.

### 21.5 Agent executing unknown action

The Agent must reject commands for unknown or unregistered actions.

---

## 22. Summary

Actions are the safe operational interface between Opstage and Capsule Services.

CE v0.1 should implement a small but complete Action loop:

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

This loop proves that Capsule Services can be operated through Opstage without exposing arbitrary remote command execution.

---

## 10. CE v0.1 Implementation Note: Action Prepare / Execute and Form Fields

The Action Catalog should report only stable list and display metadata, such as `name`, `label`, `category`, `order`, `dangerLevel`, `requiresConfirmation`, and `timeoutSeconds`. When an action panel is opened, UI uses GET prepare to create an `ACTION_PREPARE` Command, then renders the dynamic `inputSchema` and `initialPayload` returned by the Agent.

Sensitive fields should allow sufficiently long values. Passwords, tokens, API keys, and private keys may use:

```json
{
  "type": "string",
  "title": "Password / Token / API Key",
  "maxLength": 4096
}
```

When executing an action, POST execute creates an `ACTION_EXECUTE` Command. Backend should redact payloads for Admin display, but payloads delivered to the Agent must retain raw values.

---

## 11. Action Result List Display Convention

For business-facing list actions, a Capsule Service MAY return a `list` object inside `CommandResult.data`. When present, Opstage UI SHOULD render the `list` as a table above the raw JSON result. The raw JSON result MUST remain available as a fallback/debug view.

Minimum shape:

```json
{
  "list": {
    "title": "API Keys",
    "data": [
      {
        "id": "apk_xxx",
        "name": "default-client",
        "keyPreview": "demo_a…9zQ",
        "status": "ACTIVE"
      }
    ]
  }
}
```

Full shape:

```json
{
  "list": {
    "title": "API Keys",
    "data": [],
    "emptyText": "No API keys",
    "pageSize": 10,
    "columns": [
      { "key": "name", "label": "Name" },
      { "key": "id", "label": "ID", "format": "code", "copyable": true },
      { "key": "status", "label": "Status", "format": "status" },
      { "key": "expiresAt", "label": "Expires At", "format": "datetime" }
    ],
    "rowActions": [
      {
        "label": "Disable",
        "action": "disableApiKey",
        "payload": { "id": "$row.id" },
        "danger": true,
        "confirm": true
      }
    ]
  }
}
```

### 11.1 Columns

If `columns` is omitted, UI MAY infer columns from the first row. Column fields:

| Field | Type | Required | Description |
|---|---|---:|---|
| `key` | string | yes | Row field path. Dot paths such as `metadata.status` MAY be supported by UI. |
| `label` | string | no | Human-readable column label. Defaults to `key`. |
| `format` | string | no | Suggested display format: `text`, `status`, `datetime`, `boolean`, `code`, `duration`, `relativeTime`, or `bytes`. |
| `copyable` | boolean | no | Whether UI should offer a copy affordance for the cell value. |
| `ellipsis` | boolean | no | Whether UI should truncate long cell text with a tooltip where supported. |
| `width` | number/string | no | Suggested column width where supported. |

List-level optional fields:

| Field | Type | Description |
|---|---|---|
| `emptyText` | string | Empty-state text when `data` is empty. |
| `pageSize` | number | Suggested page size for UI pagination. |

### 11.2 Row Actions

`rowActions` describes row-level operators. A row action creates a normal `ACTION_EXECUTE` command for the referenced action.

| Field | Type | Required | Description |
|---|---|---:|---|
| `label` | string | yes | Button label. |
| `action` | string | yes | Target action name in the same Capsule Service. |
| `payload` | object | no | Payload template. String values of the form `$row.<path>` are substituted from the clicked row. |
| `danger` | boolean | no | UI hint for destructive operations. |
| `confirm` | boolean | no | UI hint that confirmation should be required before creating the command. |

Example payload substitution:

```json
{
  "payload": {
    "accountId": "$row.id",
    "clearCooldown": true
  }
}
```

If the UI does not support `list`, `columns`, or `rowActions`, it MUST still display the raw JSON result. Services MUST NOT depend on row actions for correctness; they are UI affordances over normal actions.

After a row action finishes, UI MAY re-run the current list action with the current filters/payload to refresh `list.data`. For long-running row actions, UI MAY keep polling the created Command and refresh the list after the Command reaches a terminal status. UI SHOULD expose row-level loading/disabled states while a row action is running.

GET prepare MAY expose list filters through the existing `inputSchema` and `initialPayload`; execute receives the filter values as its normal payload and may return a filtered `list.data`.
