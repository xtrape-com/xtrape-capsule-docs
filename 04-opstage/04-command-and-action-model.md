# Command and Action Model

- Status: Draft
- Edition: Shared
- Priority: Medium

本文件属于 `xtrape-capsule` 文档集。`xtrape-capsule` 是面向轻服务 / Capsule Service 的领域体系；`xtrape-capsule-opstage` 是该体系下的统一运行态治理平台。

当前实现重点是 CE 开源社区版。EE 私有化商业版与 Cloud SaaS 版属于未来规划，CE 需要保留扩展点，但不应在早期版本实现其完整能力。

Opstage 是 xtrape-capsule 的统一运行态治理平台，由 UI、Backend 和 Agent 接入机制组成。CE 实现轻量闭环，EE/Cloud 在此基础上扩展规模化能力。

# Command and Action Model

- Status: Implementation Guidance
- Edition: Shared
- Priority: High
- Audience: backend developers, frontend developers, agent SDK developers, Capsule Service developers, architects, security reviewers, AI coding agents

This document defines the **Command and Action Model** for Opstage.

Commands and Actions are the core operation mechanism that allows Opstage UI users to request safe, predefined operations on Capsule Services through Agents.

The current implementation focus is **Opstage CE**. EE and Cloud command capabilities are future planning tracks and must not expand the CE v0.1 implementation scope.

---

## 1. Purpose

The purpose of the Command and Action Model is to provide a safe and auditable operation path.

The model should answer:

- What operations can a Capsule Service expose?
- How are operations described to Opstage?
- How does a UI user request an operation?
- How does Backend turn that request into a durable Command?
- How does Agent receive and execute the Command?
- How is the result reported?
- How is the operation audited?
- How are unsafe arbitrary operations avoided?

The key rule is:

> Opstage executes only predefined actions through durable Commands and auditable CommandResults.

---

## 2. Core Concepts

The model contains three primary concepts:

```text
ActionDefinition
Command
CommandResult
```

### 2.1 ActionDefinition

An ActionDefinition describes an operation that a Capsule Service explicitly exposes to Opstage.

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

A Command is a durable operation request created by Backend and assigned to an Agent.

A Command represents:

```text
who requested what operation on which service with what payload
```

### 2.3 CommandResult

A CommandResult is the execution result reported by Agent after running the local predefined action handler.

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

The Agent executes only local predefined action handlers.

---

## 4. CE Scope

CE v0.1 should implement the minimum complete Command and Action loop.

Required CE capabilities:

- Agent reports ActionDefinitions;
- Backend stores ActionDefinitions;
- UI displays ActionDefinitions;
- UI allows user to request an action;
- Backend validates action request;
- Backend creates Command;
- Agent polls Commands;
- Agent executes local predefined handler;
- Agent reports CommandResult;
- Backend stores CommandResult;
- Backend updates Command status;
- Backend creates AuditEvents for important operation steps;
- UI displays Command and result.

---

## 5. CE Non-Goals

CE v0.1 should not implement:

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
- cross-Agent command routing;
- action marketplace;
- plugin-based action packs.

These may be future EE or Cloud capabilities if explicitly designed.

---

## 6. ActionDefinition

ActionDefinition is reported by Agent as part of the Capsule Service manifest or service report.

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

- unique within a Capsule Service;
- stable across service restarts;
- lower camelCase or kebab-case is acceptable;
- should not include whitespace;
- should not be localized;
- should not contain secrets;
- should not be user-generated at runtime in CE.

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

Description explains the operation.

Example:

```text
Runs an immediate health check and returns the current dependency status.
```

Labels and descriptions may be localized in future editions, but CE v0.1 may store simple English text.

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

CE demo actions should usually be `LOW`.

---

## 10. Action Enabled State

ActionDefinition should include whether the action is enabled.

```text
enabled: true | false
```

If an action is disabled:

- UI should show it as disabled or hide the Run button;
- Backend must reject execution requests;
- Agent should also reject execution if somehow received.

Backend validation is required even if UI hides disabled actions.

---

## 11. Input Schema

ActionDefinition may include an input schema.

Recommended field:

```text
inputSchemaJson
```

CE v0.1 may use a simple JSON Schema-compatible structure or plain JSON metadata.

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

CE UI may initially use a raw JSON editor instead of generating dynamic forms from schema.

Backend should still validate basic JSON shape where practical.

---

## 12. Result Schema

ActionDefinition may include a result schema.

Recommended field:

```text
resultSchemaJson
```

CE v0.1 may store this for display and future compatibility without enforcing it strictly.

Future EE may use result schema for:

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

CE v0.1 supports only:

```text
commandType = ACTION
```

Future editions may add other command types, but CE should not need them.

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

CE v0.1 should implement only `ACTION`.

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

## 16. Command Status

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

CE v0.1 may use a simpler subset:

```text
PENDING
DISPATCHED
SUCCESS
FAILED
EXPIRED
```

But the model should not block future `RUNNING` or `CANCELLED`.

---

## 17. Command Status Meaning

### 17.1 PENDING

Command was created and is waiting for Agent polling.

### 17.2 DISPATCHED

Command was returned to Agent by the Backend.

### 17.3 RUNNING

Agent reported or implied that execution has started.

CE v0.1 may skip explicit RUNNING if action execution is short.

### 17.4 SUCCESS

Agent reported successful execution.

### 17.5 FAILED

Agent reported failure or Backend marked failure.

### 17.6 EXPIRED

Command was not dispatched or completed before `expiresAt`.

### 17.7 CANCELLED

Command was cancelled before completion.

This is future work for CE.

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

CE may implement only the simple lifecycle.

---

## 19. Command Expiration

Commands should have an expiration time.

Recommended field:

```text
expiresAt
```

Recommended CE default:

```text
5 minutes to 30 minutes
```

depending on expected action duration.

If a Command expires:

- Backend should not dispatch it to Agent;
- UI should show `EXPIRED`;
- an AuditEvent may be created;
- Agent should ignore expired Commands if somehow received.

---

## 20. CommandResult

CommandResult is reported by Agent after executing a Command.

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

Future editions may support progress events or multiple partial results, but CE v0.1 does not need them.

---

## 21. CommandResult Status

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

CE v0.1 should implement `SUCCESS` and `FAILED`.

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

---

## 24. Backend Validation Rules

Before creating a Command, Backend must validate:

- user is authenticated;
- service exists;
- service belongs to accessible Workspace;
- service has associated Agent;
- Agent is not disabled or revoked;
- ActionDefinition exists;
- action is enabled;
- action danger level is known;
- payload is valid JSON;
- payload matches input schema if validation is enabled;
- high-risk confirmation is present if required;
- no raw token or obvious secret is accepted if policy rejects it.

Backend must not rely on UI-only validation.

---

## 25. Agent Execution Rules

Agent must validate locally before executing:

- Command is assigned to this Agent;
- service exists in Agent registry;
- action handler exists;
- action is enabled locally;
- Command is not expired;
- payload is acceptable to handler;
- execution errors are captured;
- result is sanitized.

If validation fails, Agent should report `FAILED` CommandResult.

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

CE UI may use simple JSON payload editor.

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

CE does not need to audit every internal state transition if too noisy.

Minimum CE audit events:

- action request;
- command success;
- command failure.

Audit payloads must be sanitized.

---

## 28. Security Rules

Command and Action security rules:

1. Only predefined actions are executable.
2. No arbitrary shell execution in CE.
3. UI cannot call Agent directly.
4. Backend creates Commands.
5. Agent only polls assigned Commands.
6. Agent only reports results for assigned Commands.
7. Backend validates action existence and enabled state.
8. Backend validates Agent ownership.
9. Payloads and results must avoid raw secrets.
10. High-risk actions require confirmation where supported.
11. Important operations are audited.

---

## 29. Arbitrary Shell Is Not an Action Model

CE must not provide a generic shell action.

Do not implement built-in actions such as:

```text
runShell
exec
bash
sh
runScript
customCommand
```

If future EE needs operational automation, it should still use:

- predefined actions;
- explicit permissions;
- approval workflows;
- audit logging;
- restricted adapters;
- clear data boundary.

A remote shell is not the default Opstage operation model.

---

## 30. Idempotency and Duplicate Handling

CE should handle duplicate situations safely.

Possible duplicates:

- UI submits same request twice;
- Agent polls and retries;
- Agent reports CommandResult twice;
- Backend request times out but operation succeeds.

Recommended behavior:

- Command IDs are unique;
- CommandResult finalization should be idempotent where practical;
- duplicate final result reports should not create multiple final states;
- UI may disable submit button after creating Command;
- future idempotency keys may be added.

CE v0.1 may keep this simple but should avoid obvious double-execution UI patterns.

---

## 31. Long-Running Actions

CE v0.1 should prefer short-running actions.

Future long-running action support may include:

- RUNNING status;
- progress events;
- progress percentage;
- cancellation;
- heartbeat during execution;
- log tail reference;
- timeout policy.

Do not implement complex long-running orchestration in CE v0.1 unless needed by the demo.

---

## 32. Demo Actions

CE demo Capsule Service should include at least two safe actions.

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

## 33. Future EE Extensions

Future EE may add:

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
- sidecar/external Agent command adapters;
- audit export for Commands.

These are not CE v0.1 requirements.

---

## 34. Future Cloud Extensions

Future Cloud may add:

- WebSocket command delivery;
- Agent Gateway command routing;
- multi-tenant command isolation;
- command usage metering;
- plan-based command limits;
- Cloud notification on command failure;
- managed audit retention for commands;
- command analytics dashboards.

These are not CE v0.1 requirements.

---

## 35. Acceptance Criteria

The CE Command and Action Model is acceptable when:

- Agent can report ActionDefinitions;
- Backend stores ActionDefinitions;
- UI shows service Actions tab;
- UI can request `echo` action;
- Backend creates an `ACTION` Command;
- Agent polls and receives the Command;
- Agent executes local `echo` handler;
- Agent reports successful CommandResult;
- UI displays CommandResult;
- UI can request `runHealthCheck` action;
- failed action execution is reported as failed CommandResult;
- Backend validates action existence;
- Backend rejects disabled or unknown actions;
- Agent rejects unknown action handlers safely;
- AuditEvents are created for action requests and results;
- raw secrets are not included in payloads or results by default;
- no arbitrary shell execution exists.

---

## 36. Summary

The Command and Action Model is the safe operation mechanism of Opstage.

It converts user intent into durable Commands, executes them only through predefined Agent-side handlers, and records the result for visibility and audit.

The most important Command and Action rule is:

> Every operation must be predefined, validated, durable, Agent-scoped, result-recorded, and auditable.