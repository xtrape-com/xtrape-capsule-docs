# CE v0.1 UI Scaffold Plan

- Status: Implementation Guidance
- Edition: CE
- Priority: Current
- Audience: frontend developers, product designers, backend developers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/openapi/opstage-ce-v0.1.yaml` disagree, the ADRs and OpenAPI contract win for CE v0.1.

## 1. Goal

Build the Opstage CE UI as a simple, useful governance console for the CE v0.1 loop.

The UI should conform to:

```text
09-contracts/openapi/opstage-ce-v0.1.yaml
```

## 2. Package

Recommended package:

```text
apps/opstage-ui
```

## 3. Stack

Per ADR 0007:

```text
React            18.x
TypeScript       5.x
Vite             5.x
Ant Design       5.x
TanStack Query   5.x      (server state)
Zustand          4.x      (small client state slice)
React Router     6.x
React Hook Form  7.x
Zod              3.x      (shared with backend via packages/contracts)
Vitest           2.x
Playwright              optional, for happy-path E2E
```

State boundaries:

```text
Server state    → TanStack Query
Form state      → React Hook Form
Client UI state → Zustand   (session, csrfToken, theme — see ADR 0007)
URL state       → React Router (page/pageSize/sort/filter)
```

## 4. Page Structure

```text
/login
/dashboard
/agents
/agents/:agentId
/capsule-services
/capsule-services/:serviceId
/commands
/commands/:commandId
/audit-events
/audit-events/:auditEventId
/settings
```

## 5. Layout

Common layout:

```text
Top bar
Sidebar navigation
Content area
Status/error boundary
```

Primary navigation:

```text
Dashboard
Agents
Capsule Services
Commands
Audit Events
Settings
```

## 6. Core Pages

### 6.1 Login

Responsibilities:

- username/password login;
- generic error on failure;
- redirect authenticated user to dashboard.

### 6.2 Dashboard

Show:

- Agent counts by status;
- Capsule Service counts by status;
- recent failed Commands;
- recent AuditEvents;
- quick start checklist.

### 6.3 Agent List / Detail

List columns:

```text
code
name
mode
runtime
status
lastHeartbeatAt
createdAt
```

Detail sections:

- basic info;
- status and heartbeat;
- related Capsule Services;
- recent Commands;
- admin actions: disable, enable, revoke.

### 6.4 Capsule Service List / Detail

List columns:

```text
code
name
runtime
version
status
healthStatus
agent
lastReportedAt
```

Detail tabs:

```text
Overview
Manifest
Health
Configs
Actions
Commands
Audit Events
```

This is the core CE v0.1 page.

### 6.5 Action Execution UX

Action execution flow:

1. user opens action dialog;
2. UI displays action label, description, danger level, confirmation requirement, and input schema if available;
3. user enters JSON payload if needed;
4. HIGH or `requiresConfirmation` actions require explicit confirmation;
5. UI calls `POST /api/admin/capsule-services/{serviceId}/actions/{actionName}`;
6. UI links to Command detail.

UI must not expose shell, exec, or arbitrary script execution as a normal CE feature.

### 6.6 Commands

List columns:

```text
id
service
actionName
status
createdAt
startedAt
completedAt
```

Detail sections:

- command metadata;
- payload JSON;
- result JSON;
- error details;
- audit trail if available.

### 6.7 Audit Events

List columns:

```text
createdAt
actorType
actorId
action
targetType
targetId
result
```

Detail page should show metadata JSON with sensitive fields redacted.

### 6.8 Settings

CE v0.1 settings should include:

- create registration token;
- list/revoke registration tokens;
- system version;
- system health.

Avoid EE/Cloud settings such as tenant, billing, SSO, license, and RBAC.

## 7. UI Safety Rules

- Do not show raw registration tokens after creation.
- Do not show raw Agent tokens.
- Mask sensitive config values.
- Require confirmation for dangerous actions.
- Do not treat stale/offline services as healthy.
- Do not call Agent endpoints directly from browser.

## 7.1 API Client Rules

A single fetch wrapper at `apps/opstage-ui/src/lib/api-client.ts` is the only allowed `fetch` caller (enforced by ESLint).

- always sends `credentials: "include"`;
- adds `X-CSRF-Token` from the Zustand store on every non-GET request;
- on `401`: clears session, redirects to `/login`;
- on `403 CSRF_INVALID`: refreshes the token via `GET /api/admin/auth/csrf` and retries once;
- maps `ErrorEnvelope` to a typed `ApiError` instance with `httpStatus`, `code`, `message`, `details`.

## 7.2 TanStack Query Conventions

```text
queryKey         [<resource>, <id?>, <params?>]
staleTime        30_000 ms (matches heartbeat cadence)
gcTime           300_000 ms
refetchOnWindowFocus  true
retry            1 (only on 5xx and NETWORK_ERROR)
```

Mutations MUST invalidate the relevant list query on success. CE v0.1 does NOT use optimistic updates.

## 8. Test Plan

Minimum UI tests:

- login screen renders;
- dashboard renders authenticated summary;
- Agent list renders;
- Capsule Service detail renders core tabs;
- action dialog creates Command;
- command detail shows result;
- audit event list renders;
- sensitive config value is masked.
