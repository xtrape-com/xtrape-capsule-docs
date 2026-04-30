# ADR 0003: Command and Action Lifecycle

- Status: Accepted
- Edition: CE
- Priority: Current
- Audience: backend developers, frontend developers, agent SDK developers, AI coding agents

## Decision

CE v0.1 models predefined operations as Actions and execution requests as Commands.

An Action is reported by a Capsule Service through the Agent SDK. A Command is created by Backend when an authenticated admin requests an Action execution.

## Action Rules

An ActionDefinition should include:

```text
name
label
description
dangerLevel
requiresConfirmation
inputSchemaJson
timeoutSeconds
```

Allowed danger levels:

```text
LOW
MEDIUM
HIGH
```

CE v0.1 must not support arbitrary shell, exec, bash, script, or generic command runner actions as a normal feature.

## Command States

Command status values:

```text
PENDING
RUNNING
SUCCEEDED
FAILED
EXPIRED
CANCELLED
```

CE v0.1 may not expose cancellation in UI, but the state is reserved for compatibility.

## Lifecycle

```text
PENDING
  ↓ Agent polls command
RUNNING
  ↓ Agent reports successful result
SUCCEEDED
```

```text
PENDING or RUNNING
  ↓ Agent reports failed result
FAILED
```

```text
PENDING or RUNNING
  ↓ timeout reached
EXPIRED
```

## Backend Requirements

When creating a Command, Backend must:

1. authenticate the admin user;
2. validate Capsule Service exists;
3. validate service has an active Agent;
4. validate ActionDefinition exists;
5. validate payload is JSON and matches schema when schema validation is available;
6. create Command with `PENDING` status;
7. write AuditEvent.

When an Agent polls Commands, Backend must:

1. authenticate the Agent token;
2. reject disabled or revoked Agents;
3. return only Commands assigned to the Agent;
4. transition returned `PENDING` Commands to `RUNNING`;
5. set `startedAt` and timeout metadata.

When receiving CommandResult, Backend must:

1. authenticate the Agent token;
2. validate Command belongs to the Agent;
3. reject invalid terminal-state updates;
4. store CommandResult;
5. transition Command to `SUCCEEDED` or `FAILED`;
6. write AuditEvent.
