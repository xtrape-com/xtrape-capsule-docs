---
status: implemented
audience: ai-coding-agents
stability: evolving
last_reviewed: 2026-05-05
edition: ce
phase: current
---

# Capsule Service Action Design Guide

- Status: Implementation Guidance
- Edition: Shared / CE-first
- Priority: High
- Audience: Capsule Service developers, Agent SDK developers, Opstage UI developers, AI coding agents

This guide translates the Action and Command specs into practical rules for designing Capsule Service actions.

Use this document together with:

```text
02-specs/05-action-spec.md
02-specs/07-command-spec.md
04-opstage/04-command-and-action-model.md
```

---

## 1. Core Model

Each service action has two phases:

| Phase | HTTP | Command type | Responsibility |
|---|---|---|---|
| Prepare | `GET /api/admin/capsule-services/{serviceId}/actions/{actionName}` | `ACTION_PREPARE` | Build dynamic UI metadata, default payload, enum options, current state. Must not perform the business operation. |
| Execute | `POST /api/admin/capsule-services/{serviceId}/actions/{actionName}` | `ACTION_EXECUTE` | Validate payload and perform the operation. |

The service report only publishes the **Action Catalog**. Dynamic form details belong in prepare.

---

## 2. Action Catalog Rules

Action Catalog should be stable and small. It is used to render buttons and groups before the action panel opens.

Recommended fields:

```json
{
  "name": "listAccounts",
  "label": "List Accounts",
  "description": "View account status.",
  "category": "account",
  "order": 10,
  "dangerLevel": "LOW",
  "requiresConfirmation": false,
  "timeoutSeconds": 30,
  "enabled": true
}
```

Guidelines:

- Keep `name` stable; changing it breaks old Commands and row actions.
- Use `category` for UI grouping, for example `account`, `api-key`, `session`, `runtime-config`, `diagnostics`, `advanced`.
- Use `order` for stable button ordering.
- Set `requiresConfirmation: true` for destructive, security-sensitive, or long-running operations.
- Do not put large account lists, config values, or runtime state in the periodic service report.

---

## 3. Prepare Handler Rules

Prepare runs when an operator opens an action panel.

Prepare should return:

```json
{
  "action": {
    "name": "rebuildAccountContext",
    "label": "Rebuild Account Browser Context",
    "requiresConfirmation": true,
    "inputSchema": {
      "type": "object",
      "required": ["accountId"],
      "properties": {
        "accountId": {
          "type": "string",
          "title": "Account",
          "enum": ["account-a37c76affd5b"],
          "enumLabels": ["account-a37c76affd5b (ethan.w….com)"]
        },
        "clearCooldown": {
          "type": "boolean",
          "title": "Clear Cooldown",
          "default": true
        }
      }
    }
  },
  "initialPayload": {
    "accountId": "account-a37c76affd5b",
    "clearCooldown": true
  },
  "currentState": {
    "accounts": []
  }
}
```

Prepare MUST:

- be safe to retry;
- avoid business side effects;
- generate dynamic enum options from current state;
- generate initial payload defaults;
- avoid returning secrets.

Prepare SHOULD:

- include useful field `title` and `description`;
- use `format: "password"` for secret input;
- use `format: "textarea"` for multi-line values;
- use `enumLabels` for readable account/config/API-key choices;
- return empty options with helpful descriptions instead of failing when no resource exists.

---

## 4. Execute Handler Rules

Execute receives the payload generated or edited in the action panel.

Execute MUST:

- validate all required fields again;
- enforce type and enum constraints server-side / agent-side;
- check resource ownership and existence;
- redact secrets in logs, audit metadata, and results;
- return bounded result data;
- report a clear `error.code` when failing.

Example success result:

```json
{
  "success": true,
  "message": "Account disabled.",
  "data": {
    "accountId": "account-a37c76affd5b"
  }
}
```

Example failure result:

```json
{
  "success": false,
  "message": "Account not found.",
  "error": {
    "code": "ACCOUNT_NOT_FOUND"
  }
}
```

---

## 5. List Action Design

List actions should return both raw data and display metadata:

```json
{
  "success": true,
  "data": {
    "accounts": [],
    "list": {
      "title": "Accounts",
      "emptyText": "No accounts",
      "pageSize": 10,
      "data": [],
      "columns": [
        { "key": "label", "label": "Account", "format": "code", "copyable": true, "ellipsis": true },
        { "key": "enabled", "label": "Enabled", "format": "boolean" },
        { "key": "loginState", "label": "Login State", "format": "status" },
        { "key": "cooldownRemainingMs", "label": "Cooldown", "format": "duration" }
      ],
      "rowActions": [
        {
          "label": "Disable",
          "action": "disableAccount",
          "payload": { "accountId": "$row.id" },
          "danger": true,
          "confirm": true
        }
      ]
    }
  }
}
```

Guidelines:

- Keep raw data for API/debug compatibility.
- Put UI table metadata under `data.list`.
- Use `rowActions` only as a UI convenience over normal actions.
- Ensure row action payload templates reference stable row fields.
- Design list filters as normal `inputSchema` fields in prepare.

---

## 6. Long-Running Action Design

Examples: login, rebuild browser context, database migration, remote sync.

Rules:

- Set `timeoutSeconds` high enough for expected execution.
- Use `requiresConfirmation: true` if the operation affects sessions, credentials, account availability, or data integrity.
- Return quickly only if the operation is intentionally asynchronous and exposes progress elsewhere.
- Update health/current state while running when possible.
- Expose status through list actions or health details, for example `operationStatus`, `operationName`, `operationMessage`, `operationStartedAt`.

Recommended states:

```text
IDLE
RUNNING
SUCCEEDED
FAILED
```

Domain-specific status fields such as `loginState` may be added to list rows or health details.

---

## 7. Security and Sensitive Data

Never return raw secrets in:

- service report;
- health details;
- action prepare result;
- command result, except one-time generated secrets explicitly intended to be copied once;
- audit metadata;
- logs.

For one-time generated secrets, return a clearly named field such as `generatedKey` and document that it is only shown once.

Use these UI hints:

| Hint | Usage |
|---|---|
| `format: "password"` | Passwords, app passwords, API tokens, private keys. |
| `sensitive: true` in config metadata | Values that must not be previewed. |
| `secretRef` | Reference to externally stored secret, not the secret itself. |

---

## 8. Concurrency and Resource Locks

Agents should set command polling `limit` to their remaining local capacity.

Agents may still apply stricter locks internally:

| Action class | Suggested lock |
|---|---|
| Read-only list/config/API-key metadata | May run concurrently. |
| Browser/session/login/account context | Serialize per service or per account. |
| Destructive data operations | Serialize by affected resource. |

The backend command model records execution. The agent is responsible for local runtime safety.

---

## 9. Checklist

Before adding a new action, verify:

- [ ] Catalog fields are stable and small.
- [ ] Prepare is side-effect free.
- [ ] Prepare returns labels, descriptions, defaults, and dynamic enums.
- [ ] Execute validates payload independently.
- [ ] Results are bounded and do not leak secrets.
- [ ] Long-running behavior is visible through command status, health, or list rows.
- [ ] Row actions call existing normal actions.
- [ ] Documentation examples are updated.
