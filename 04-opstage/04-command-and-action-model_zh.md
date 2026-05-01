<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 04-command-and-action-model.md
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

# Command and Action Model

- Status: 实施指南
- Edition: 共享
- Priority: 高
- Audience: backend developers, frontend developers, agent SDK developers, Capsule Service（胶囊服务） developers, architects, security reviewers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/` (OpenAPI / Prisma) disagree, the ADRs and contracts win for CE（社区版） v0.1. In particular: CE（社区版） v0.1 Command states are `PENDING | RUNNING | SUCCEEDED | FAILED | EXPIRED | CANCELLED` (no `DISPATCHED`), CommandResult uses `success / message / data / error`, ActionDefinition uses `requiresConfirmation`, and `dangerLevel` is `LOW | MEDIUM | HIGH` (no `CRITICAL`). Sections that still mention older terminology are kept for historical context but should not be implemented.

This document 定义 the **Command and Action Model** for Opstage（运维舞台）.

Commands and Actions are the core operation mechanism that allows Opstage（运维舞台） UI users to request safe, predefined operations on Capsule Services through Agents.

The current implementation focus is **Opstage（运维舞台） CE（社区版）**. EE（企业版） and Cloud（云版） command capabilities are future planning tracks and must not expand the CE（社区版） v0.1 implementation scope.

---

## 1. Purpose

The purpose of the Command and Action Model is to provide a safe and auditable operation path.

The model should answer:

- What operations can a Capsule Service（胶囊服务） expose?
- How are operations described to Opstage（运维舞台）?
- How does a UI user request an operation?
- How does Backend turn that request into a durable Command?
- How does Agent（代理） receive and execute the Command?
- How is the result reported?
- How is the operation audited?
- How are unsafe arbitrary operations avoided?

The key rule is:

> Opstage（运维舞台） executes only predefined actions through durable Commands and auditable CommandResults.

---

## 2. Core Concepts

The model 包含 three primary concepts:

```text
ActionDefinition
Command
CommandResult
```

### 2.1 ActionDefinition

An ActionDefinition 描述 an operation that a Capsule Service（胶囊服务） explicitly exposes to Opstage（运维舞台）.

Examples:

```text
echo
runHealthCheck
reloadConfig
refreshSession
rotateAccount
clearCache
```

### 2.2 Command

A Command is a durable operation request created by Backend and assigned to an Agent（代理）.

A Command represents:

```text
who requested what operation on which service with what payload
```

### 2.3 CommandResult

A CommandResult is the execution result reported by Agent（代理） after running the local predefined action handler.

A CommandResult represents:

```text
what happened when the Agent executed the Command
```

---

## 3. Model Relationship

Recommended relationship:

```text
Capsule Service
    ↓ reports
ActionDefinition
    ↓ selected by UI user
Backend creates
Command
    ↓ polled by Agent
Agent executes local action handler
    ↓ reports
CommandResult
    ↓ recorded as
AuditEvent
```

The UI does not execute actions directly.

The Backend does not execute service actions directly.

The Agent（代理） executes only local predefined action handlers.

---

## 4. CE（社区版） Scope

CE（社区版） v0.1 should implement the minimum complete Command and Action loop.

Required CE（社区版） capabilities:

- Agent（代理） reports ActionDefinitions;
- Backend stores ActionDefinitions;
- UI displays ActionDefinitions;
- UI allows user to request an action;
- Backend validates action request;
- Backend creates Command;
- Agent（代理） polls Commands;
- Agent（代理） executes local predefined handler;
- Agent（代理） reports CommandResult;
- Backend stores CommandResult;
- Backend updates Command status;
- Backend creates AuditEvents for important operation steps;
- UI displays Command and result.

---

## 5. CE（社区版） Non-Goals

CE（社区版） v0.1 should not implement:

- arbitrary shell execution;
- custom script execution;
- remote terminal;
- workflow engine;
- batch command orchestration;
- scheduled commands;
- command approval workflow;
- command cancellation UI;
- command retry policy engine;
- long-running progress stream;
- WebSocket command delivery;
- queue-backed command delivery;
- cross-Agent（代理） command routing;
- action marketplace;
- plugin-based action packs.

These may be future EE（企业版） or Cloud（云版） capabilities if explicitly designed.

---

## 6. ActionDefinition

ActionDefinition is reported by Agent（代理） as part of the Capsule Service（胶囊服务） manifest or service report.

Recommended fields:

```text
id
workspaceId
serviceId
name
label
description
dangerLevel
enabled
inputSchemaJson
resultSchemaJson
metadataJson
createdAt
updatedAt
```

The service-facing manifest may not include database fields such as `id`, `workspaceId`, `serviceId`, `createdAt`, or `updatedAt`. Backend assigns those fields when persisting.

---

## 7. Action Name

Action name is the stable technical identifier.

Rules:

- unique within a Capsule Service（胶囊服务）;
- stable across service restarts;
- lower camelCase or kebab-case is acceptable;
- should not include whitespace;
- should not be localized;
- should not contain secrets;
- should not be user-generated at runtime in CE（社区版）.

Recommended examples:

```text
echo
runHealthCheck
reloadConfig
refreshAccountPool
clearCache
```

Avoid names that imply arbitrary execution:

```text
runShell
exec
bash
customCommand
runScript
```

---

## 8. Action Label and Description

Action label is human-facing.

Example:

```text
Run Health Check
```

Description 解释 the operation.

Example:

```text
Runs an immediate health check and returns the current dependency status.
```

Labels and descriptions may be localized in future editions, but CE（社区版） v0.1 may store simple English text.

---

## 9. Danger Level

Danger level communicates operation risk.

Recommended values:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

### 9.1 LOW

Safe read-like or diagnostic action.

Examples:

```text
echo
runHealthCheck
getRuntimeSummary
```

### 9.2 MEDIUM

Action may affect runtime state but is usually reversible or low impact.

Examples:

```text
clearCache
refreshSession
reloadConfig
```

### 9.3 HIGH

Action may affect availability, accounts, sessions, external systems, or customer-visible behavior.

Examples:

```text
restartWorker
rotateAccount
rebuildIndex
```

### 9.4 CRITICAL

Action is highly sensitive or destructive.

Examples:

```text
revokeAllSessions
purgeData
forceFailover
```

CE（社区版） demo actions should usually be `LOW`.

---

## 10. Action Enabled State

ActionDefinition should include whether the action is enabled.

```text
enabled: true | false
```

If an action is disabled:

- UI should show it as disabled or hide the Run button;
- Backend must reject execution requests;
- Agent（代理） should also reject execution if somehow received.

Backend validation is required even if UI hides disabled actions.

---

## 11. Input Schema

ActionDefinition may include an input schema.

Recommended field:

```text
inputSchemaJson
```

CE（社区版） v0.1 may use a simple JSON Schema-compatible structure or plain JSON metadata.

Example:

```json
{
  "type": "object",
  "properties": {
    "message": {
      "type": "string",
      "title": "Message"
    }
  },
  "required": ["message"]
}
```

CE（社区版） UI may initially use a raw JSON editor instead of generating dynamic forms from schema.

Backend should still validate basic JSON shape where practical.

---

## 12. Result Schema

ActionDefinition may include a result schema.

Recommended field:

```text
resultSchemaJson
```

CE（社区版） v0.1 may store this for display and future compatibility without enforcing it strictly.

Future EE（企业版） may use result schema for:

- result rendering;
- validation;
- dashboards;
- automation;
- typed SDKs.

---

## 13. Command

Command is created by Backend after a UI user requests an action.

Recommended fields:

```text
id
workspaceId
agentId
serviceId
commandType
actionName
status
payloadJson
createdByActorType
createdByActorId
createdAt
dispatchedAt
startedAt
finishedAt
expiresAt
metadataJson
```

CE（社区版） v0.1 支持 only:

```text
commandType = ACTION
```

Future editions may add other command types, but CE（社区版） should not need them.

---

## 14. Command Type

Recommended command type values:

```text
ACTION
```

Reserved future values may include:

```text
CONFIG_APPLY
CONFIG_RELOAD
AGENT_CONTROL
SERVICE_CONTROL
```

CE（社区版） v0.1 should implement only `ACTION`.

---

## 15. Command Payload

Command payload is the action input data.

Recommended field:

```text
payloadJson
```

Payload rules:

- must be JSON-serializable;
- must match input schema if schema validation is implemented;
- must not contain raw secrets by default;
- should use `secretRef` for sensitive references;
- should be sanitized before being stored in AuditEvent.

Bad payload:

```json
{
  "password": "plain-password"
}
```

Good payload:

```json
{
  "accountSecretRef": "agent-local://agent-001/secrets/chatgpt/account-001"
}
```

---

## 16. Command 状态

Recommended Command status values:

```text
PENDING
DISPATCHED
RUNNING
SUCCESS
FAILED
EXPIRED
CANCELLED
```

CE（社区版） v0.1 may use a simpler subset:

```text
PENDING
DISPATCHED
SUCCESS
FAILED
EXPIRED
```

But the model should not block future `RUNNING` or `CANCELLED`.

---

## 17. Command 状态 Meaning

### 17.1 PENDING

Command was created and is waiting for Agent（代理） polling.

### 17.2 DISPATCHED

Command was returned to Agent（代理） by the Backend.

### 17.3 RUNNING

Agent（代理） reported or implied that execution has started.

CE（社区版） v0.1 may skip explicit RUNNING if action execution is short.

### 17.4 SUCCESS

Agent（代理） reported successful execution.

### 17.5 FAILED

Agent（代理） reported failure or Backend marked failure.

### 17.6 EXPIRED

Command was not dispatched or completed before `expiresAt`.

### 17.7 CANCELLED

Command was cancelled before completion.

This is future work for CE（社区版）.

---

## 18. Command Lifecycle

Recommended lifecycle:

```text
PENDING
    ↓ Agent polls
DISPATCHED
    ↓ Agent starts execution
RUNNING
    ↓ Agent reports result
SUCCESS / FAILED
```

Timeout lifecycle:

```text
PENDING / DISPATCHED / RUNNING
    ↓ expiresAt passed
EXPIRED
```

Future cancellation lifecycle:

```text
PENDING / DISPATCHED / RUNNING
    ↓ user or system cancels
CANCELLED
```

CE（社区版） may implement only the simple lifecycle.

---

## 19. Command Expiration

Commands should have an expiration time.

Recommended field:

```text
expiresAt
```

Recommended CE（社区版） default:

```text
5 minutes to 30 minutes
```

depending on expected action duration.

If a Command expires:

- Backend should not dispatch it to Agent（代理）;
- UI should show `EXPIRED`;
- an AuditEvent may be created;
- Agent（代理） should ignore expired Commands if somehow received.

---

## 20. CommandResult

CommandResult is reported by Agent（代理） after executing a Command.

Recommended fields:

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
reportedAt
metadataJson
```

A Command should normally have one final CommandResult.

Future editions may support progress events or multiple partial results, but CE（社区版） v0.1 does not need them.

---

## 21. CommandResult 状态

Recommended result status values:

```text
SUCCESS
FAILED
```

Optional future values:

```text
PARTIAL
CANCELLED
TIMEOUT
```

CE（社区版） v0.1 should implement `SUCCESS` and `FAILED`.

---

## 22. CommandResult Payload

CommandResult may include:

```text
outputText
errorMessage
resultJson
```

Rules:

- keep result concise;
- do not store large logs;
- do not store raw secrets;
- sanitize error messages where practical;
- use structured `resultJson` for machine-readable output;
- use `outputText` for human-readable summary.

Bad result:

```json
{
  "cookie": "raw-cookie-value"
}
```

Good result:

```json
{
  "success": true,
  "checkedDependencies": 3,
  "failedDependencies": 0
}
```

---

## 23. Action Execution Flow

End-to-end action execution flow:

```text
User opens Capsule Service Detail
    ↓
UI displays ActionDefinitions
    ↓
User selects action and submits payload
    ↓
UI calls Admin API
    ↓
Backend authenticates user
    ↓
Backend validates service
    ↓
Backend validates ActionDefinition
    ↓
Backend validates payload
    ↓
Backend creates Command
    ↓
Agent polls Commands
    ↓
Backend returns Command
    ↓
Agent finds local action handler
    ↓
Agent executes handler
    ↓
Agent reports CommandResult
    ↓
Backend updates Command
    ↓
Backend stores CommandResult
    ↓
Backend creates AuditEvent
    ↓
UI displays result
```

### 23.1 Sequence Diagram (CE（社区版） v0.1)

```mermaid
sequenceDiagram
    autonumber
    actor U as Admin User
    participant UI as Opstage UI
    participant BE as Opstage Backend
    participant DB as SQLite (Prisma)
    participant AG as Agent (in Capsule Service)
    participant SVC as Capsule Service handler

    U->>UI: Click "Restart" on service detail
    UI->>BE: POST /api/admin/capsule-services/{serviceId}/actions/restart\ncookie + X-CSRF-Token + body
    BE->>DB: Tx start
    BE->>DB: Lookup service, action, agent
    BE->>BE: Validate session, CSRF, payload (Zod + JSON Schema)
    BE->>DB: INSERT Command (PENDING)
    BE->>DB: INSERT AuditEvent (action=COMMAND.CREATE, result=SUCCESS)
    BE->>DB: Tx commit
    BE-->>UI: 200 { data: Command(PENDING) }

    loop heartbeat / poll loop
        AG->>BE: GET /api/agents/{agentId}/commands (Bearer)
        BE->>DB: SELECT pending commands for agent\n(LIMIT N, FOR UPDATE in MySQL; SQLite uses BEGIN IMMEDIATE)
        BE->>DB: UPDATE Command SET status=RUNNING, dispatchedAt=now
        BE-->>AG: 200 { data: [Command...] }
    end

    AG->>SVC: Invoke local handler(payload)
    SVC-->>AG: success | failure
    AG->>BE: POST /api/agents/{agentId}/commands/{commandId}/result\n{ success, message, data, error, startedAt, finishedAt }
    BE->>DB: Tx start
    BE->>DB: UPDATE Command SET status=SUCCEEDED|FAILED, finishedAt
    BE->>DB: INSERT CommandResult
    BE->>DB: INSERT AuditEvent (action=COMMAND.COMPLETE, result=SUCCESS|FAILURE)
    BE->>DB: Tx commit
    BE-->>AG: 200 OK

    UI->>BE: GET /api/admin/commands/{commandId} (poll or SSE in EE)
    BE-->>UI: 200 { data: CommandDetail }
```

### 23.2 Backend Pseudocode (`createActionCommand`)

```ts
// modules/capsule-services/actions.controller.ts (pseudo-code)
async function createActionCommand(req, res) {
  const { serviceId, actionName } = req.params;
  const session = req.session.get("admin");          // 401 if absent
  const body = CreateActionCommandRequest.parse(req.body); // 422 on shape error

  return prisma.$transaction(async (tx) => {
    const service = await tx.capsuleService.findUnique({ where: { id: serviceId }, include: { agent: true } });
    if (!service)                  throw new HttpError(404, "SERVICE_NOT_FOUND",  "Capsule service not found.");
    if (!service.agent)            throw new HttpError(409, "SERVICE_HAS_NO_AGENT","Service is not bound to an agent.");
    if (service.agent.status === "DISABLED" || service.agent.status === "REVOKED")
                                   throw new HttpError(409, "AGENT_NOT_ACTIVE",   `Agent status is ${service.agent.status}.`);

    const action = await tx.actionDefinition.findUnique({
      where: { serviceId_name: { serviceId, name: actionName } },
    });
    if (!action)                   throw new HttpError(404, "ACTION_NOT_FOUND",   "Action not declared by service.");
    if (!action.enabled)           throw new HttpError(409, "ACTION_DISABLED",    "Action currently disabled.");

    if (action.requiresConfirmation && body.confirmation !== true) {
      throw new HttpError(409, "ACTION_REQUIRES_CONFIRMATION", "Action requires explicit confirmation.");
    }

    if (action.inputSchemaJson) {
      const validate = ajv.compile(JSON.parse(action.inputSchemaJson));
      if (!validate(body.payload ?? {})) {
        throw new HttpError(422, "VALIDATION_FAILED", "Action payload failed schema validation.", validate.errors);
      }
    }

    const command = await tx.command.create({
      data: {
        id: newId("cmd_"),
        workspaceId: service.workspaceId,
        agentId:     service.agentId,
        serviceId:   service.id,
        type:        "ACTION",
        actionName:  action.name,
        payloadJson: JSON.stringify(body.payload ?? {}),
        status:      "PENDING",
        expiresAt:   new Date(now().getTime() + defaults.commandTtlSeconds * 1000),
        createdByUserId: session.userId,
        createdAt:   now(),
      },
    });

    await tx.auditEvent.create({
      data: {
        id: newId("aud_"),
        workspaceId: service.workspaceId,
        actorType: "USER",
        actorId:   session.userId,
        action:    "service.action.requested",
        targetType:"Command",
        targetId:  command.id,
        result:    "SUCCESS",
        message:   `Requested action ${actionName} for service ${service.code}.`,
        metadataJson: JSON.stringify({ serviceId, agentId: service.agentId, actionName, dangerLevel: action.dangerLevel }),
        createdAt: now(),
      },
    });

    return res.status(200).send({ success: true, data: serializeCommand(command) });
  });
}
```

Failure rules (these MUST also produce a `COMMAND.CREATE` AuditEvent with `result: FAILURE` and the same target/metadata, except the AuditEvent is written from the error handler so the transaction can roll back the half-built Command):

||Condition|HTTP|error.code||
|-----------------------------------------------|------|----------------------------------|
||service missing|404|`SERVICE_NOT_FOUND`||
||service has no Agent（代理）|409|`SERVICE_HAS_NO_AGENT`||
||Agent（代理） disabled / revoked|409|`AGENT_NOT_ACTIVE`||
||action missing|404|`ACTION_NOT_FOUND`||
||action disabled|409|`ACTION_DISABLED`||
||`requiresConfirmation: true` and not provided|409|`ACTION_REQUIRES_CONFIRMATION`||
||payload fails JSON Schema|422|`VALIDATION_FAILED`||
||body shape invalid (Zod)|422|`VALIDATION_FAILED`||
||CSRF header missing/wrong|403|`CSRF_INVALID`||
||session missing/expired|401|`AUTH_REQUIRED`||

### 23.3 Backend Pseudocode (`pollCommands`)

```ts
async function pollCommands(req, res) {
  const agent = await authenticateAgent(req);   // 401 / 403
  const limit = clamp(req.query.limit ?? 10, 1, 50);

  const commands = await prisma.$transaction(async (tx) => {
    const pending = await tx.command.findMany({
      where: { agentId: agent.id, status: "PENDING" },
      orderBy: { createdAt: "asc" },
      take: limit,
    });
    if (pending.length === 0) return [];

    await tx.command.updateMany({
      where: { id: { in: pending.map((c) => c.id) }, status: "PENDING" },
      data:  { status: "RUNNING", startedAt: now() },
    });

    return pending.map((c) => ({ ...c, status: "RUNNING" }));
  });

  return res.send({ success: true, data: commands.map(serializeCommand) });
}
```

### 23.4 Backend Pseudocode (`reportCommandResult`)

```ts
async function reportCommandResult(req, res) {
  const agent = await authenticateAgent(req);
  const { commandId } = req.params;
  const body = ReportCommandResultRequest.parse(req.body);

  return prisma.$transaction(async (tx) => {
    const cmd = await tx.command.findUnique({ where: { id: commandId } });
    if (!cmd)                              throw new HttpError(404, "COMMAND_NOT_FOUND",     "Command not found.");
    if (cmd.agentId !== agent.id)          throw new HttpError(403, "COMMAND_NOT_OWNED",     "Command not owned by this agent.");
    if (cmd.status === "EXPIRED")          throw new HttpError(410, "COMMAND_EXPIRED",       "Command already expired.");
    if (cmd.status === "SUCCEEDED" || cmd.status === "FAILED" || cmd.status === "CANCELLED")
                                           throw new HttpError(409, "COMMAND_TERMINAL",      `Command already ${cmd.status}.`);

    const finalStatus = body.success ? "SUCCEEDED" : "FAILED";

    await tx.command.update({
      where: { id: commandId },
      data:  { status: finalStatus, completedAt: now() },
    });

    await tx.commandResult.create({
      data: {
        id: newId("crs_"),
        commandId,
        agentId:   agent.id,
        success:   body.success,
        message:   body.message ?? null,
        dataJson:  body.data  != null ? JSON.stringify(body.data)  : null,
        errorJson: body.error != null ? JSON.stringify(body.error) : null,
        reportedAt: now(),
      },
    });

    await tx.auditEvent.create({
      data: {
        id: newId("aud_"),
        workspaceId: cmd.workspaceId,
        actorType: "AGENT",
        actorId:   agent.id,
        action:    body.success ? "command.completed" : "command.failed",
        targetType:"Command",
        targetId:  cmd.id,
        result:    body.success ? "SUCCESS" : "FAILURE",
        message:   body.message ?? null,
        createdAt: now(),
      },
    });

    return res.send({ success: true });
  });
}
```

### 23.5 Ordering Guarantees

- Command creation is committed BEFORE the response, so a failed AuditEvent insert MUST roll back the Command (single transaction).
- 状态 transitions are linear and persisted (no optimistic in-memory state). The Backend MUST never expose `RUNNING → PENDING` transitions.
- Once `SUCCEEDED`, `FAILED`, `EXPIRED`, or `CANCELLED`, a Command is terminal. Retries create a NEW Command.

---

## 24. Backend Validation Rules

Before creating a Command, Backend must validate:

- user is authenticated;
- service exists;
- service belongs to accessible Workspace;
- service has associated Agent（代理）;
- Agent（代理） is not disabled or revoked;
- ActionDefinition exists;
- action is enabled;
- action danger level is known;
- payload is valid JSON;
- payload matches input schema if validation is enabled;
- high-risk confirmation is present if required;
- no raw token or obvious secret is accepted if policy rejects it.

Backend must not rely on UI-only validation.

---

## 25. Agent（代理） Execution Rules

Agent（代理） must validate locally before executing:

- Command is assigned to this Agent（代理）;
- service exists in Agent（代理） registry;
- action handler exists;
- action is enabled locally;
- Command is not expired;
- payload is acceptable to handler;
- execution errors are captured;
- result is sanitized.

If validation fails, Agent（代理） should report `FAILED` CommandResult.

---

## 26. UI Rules

UI should:

- show only reported ActionDefinitions;
- indicate danger level;
- disable Run button for disabled actions;
- require confirmation for `HIGH` and `CRITICAL` actions;
- show generated Command after submission;
- poll Command status until final state;
- show CommandResult;
- show related AuditEvents where practical;
- mask sensitive values.

CE（社区版） UI may use simple JSON payload editor.

---

## 27. Audit Rules

Command and action operations should create AuditEvents.

Recommended audit actions:

```text
action.requested
command.created
command.dispatched
command.succeeded
command.failed
command.expired
```

CE（社区版） does not need to audit every internal state transition if too noisy.

Minimum CE（社区版） audit events:

- action request;
- command success;
- command failure.

Audit payloads must be sanitized.

---

## 28. 安全 Rules

Command and Action security rules:

1. Only predefined actions are executable.
2. No arbitrary shell execution in CE（社区版）.
3. UI cannot call Agent（代理） directly.
4. Backend creates Commands.
5. Agent（代理） only polls assigned Commands.
6. Agent（代理） only reports results for assigned Commands.
7. Backend validates action existence and enabled state.
8. Backend validates Agent（代理） ownership.
9. Payloads and results must avoid raw secrets.
10. 高-risk actions require confirmation where supported.
11. Important operations are audited.

---

## 29. Arbitrary Shell Is Not an Action Model

CE（社区版） must not provide a generic shell action.

Do not implement built-in actions such as:

```text
runShell
exec
bash
sh
runScript
customCommand
```

If future EE（企业版） needs operational automation, it should still use:

- predefined actions;
- explicit permissions;
- approval workflows;
- audit logging;
- restricted adapters;
- clear data boundary.

A remote shell is not the default Opstage（运维舞台） operation model.

---

## 30. Idempotency and Duplicate Handling

CE（社区版） should handle duplicate situations safely.

Possible duplicates:

- UI submits same request twice;
- Agent（代理） polls and retries;
- Agent（代理） reports CommandResult twice;
- Backend request times out but operation succeeds.

Recommended behavior:

- Command IDs are unique;
- CommandResult finalization should be idempotent where practical;
- duplicate final result reports should not create multiple final states;
- UI may disable submit button after creating Command;
- future idempotency keys may be added.

CE（社区版） v0.1 may keep this simple but should avoid obvious double-execution UI patterns.

---

## 31. Long-Running Actions

CE（社区版） v0.1 should prefer short-running actions.

Future long-running action support may include:

- RUNNING status;
- progress events;
- progress percentage;
- cancellation;
- heartbeat during execution;
- log tail reference;
- timeout policy.

Do not implement complex long-running orchestration in CE（社区版） v0.1 unless needed by the demo.

---

## 32. Demo Actions

CE（社区版） demo Capsule Service（胶囊服务） should include at least two safe actions.

### 32.1 echo

Purpose:

```text
Return the submitted payload for demonstration.
```

Danger level:

```text
LOW
```

### 32.2 runHealthCheck

Purpose:

```text
Run the service health provider immediately and return result.
```

Danger level:

```text
LOW
```

These actions prove the operation loop without introducing risk.

---

## 33. Future EE（企业版） Extensions

Future EE（企业版） may add:

- command cancellation;
- command retry policy;
- command scheduling;
- command approval workflow;
- command concurrency control;
- resource locks;
- long-running progress reporting;
- action-level RBAC;
- action-level MFA re-check;
- operation window policy;
- sidecar/external Agent（代理） command adapters;
- audit export for Commands.

These are not CE（社区版） v0.1 requirements.

---

## 34. Future Cloud（云版） Extensions

Future Cloud（云版） may add:

- WebSocket command delivery;
- Agent（代理） Gateway command routing;
- multi-tenant command isolation;
- command usage metering;
- plan-based command limits;
- Cloud（云版） notification on command failure;
- managed audit retention for commands;
- command analytics dashboards.

These are not CE（社区版） v0.1 requirements.

---

## 35. Acceptance Criteria

The CE（社区版） Command and Action Model is acceptable when:

- Agent（代理） can report ActionDefinitions;
- Backend stores ActionDefinitions;
- UI shows service Actions tab;
- UI can request `echo` action;
- Backend creates an `ACTION` Command;
- Agent（代理） polls and receives the Command;
- Agent（代理） executes local `echo` handler;
- Agent（代理） reports successful CommandResult;
- UI displays CommandResult;
- UI can request `runHealthCheck` action;
- failed action execution is reported as failed CommandResult;
- Backend validates action existence;
- Backend rejects disabled or unknown actions;
- Agent（代理） rejects unknown action handlers safely;
- AuditEvents are created for action requests and results;
- raw secrets are not included in payloads or results by default;
- no arbitrary shell execution exists.

---

## 36. Summary

The Command and Action Model is the safe operation mechanism of Opstage（运维舞台）.

It converts user intent into durable Commands, executes them only through predefined Agent（代理）-side handlers, and records the result for visibility and audit.

The most important Command and Action rule is:

> Every operation must be predefined, validated, durable, Agent（代理）-scoped, result-recorded, and auditable.
