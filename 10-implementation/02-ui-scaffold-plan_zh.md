---
status: draft
audience: ai-coding-agents
stability: unstable
last_reviewed: 2026-05-05
edition: ce
phase: current
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 02-ui-scaffold-plan.md
翻译状态 / Translation Status: 已翻译 / Translated
生成时间 / Generated: 2026-05-01 09:28:55
================================================================================
注意 / Notes:
- 技术术语如 Capsule Service、Agent、Opstage 等保留英文或采用中英对照
- 代码块中的内容不翻译
- 文件路径和 URL 不翻译
- 保持原有的 Markdown 格式结构
================================================================================
-->

# CE（社区版） v0.1 UI Scaffold Plan

- Status: 实施指南
- Edition: CE（社区版）
- Priority: Current
- Audience: frontend developers, product designers, backend developers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs (especially ADR 0007) or `09-contracts/openapi/opstage-ce-v0.1.yaml` disagree, the ADRs and OpenAPI contract win for CE（社区版） v0.1.

## 1. Goal

Build the Opstage（运维舞台） CE（社区版） UI as a simple, useful governance console for the CE（社区版） v0.1 loop, using React 18 + Ant Design (antd 5.x).

The UI MUST conform to:

```text
09-contracts/openapi/opstage-ce-v0.1.yaml
```

## 2. Package

Lives inside the CE（社区版） monorepo (`xtrape-capsule-ce`):

```text
xtrape-capsule-ce/apps/opstage-ui          (workspace package: @xtrape/opstage-ui — private)
```

## 3. Stack

Per [ADR 0007](../08-decisions/0007-ui-state-and-data-fetching.md):

```text
React                   18.x
TypeScript              5.x     (strict)
Vite                    5.x
antd                    5.x     (Ant Design React)
@tanstack/react-query   5.x
react-router-dom        7.x
Zod                     3.x     (re-exported from @xtrape/capsule-contracts-node)
Vitest                  2.x
Playwright                        optional, for happy-path E2E
```

State boundaries:

```text
Server state    → TanStack React Query
Form state      → antd Form（内置）+ Zod 用于 schema 验证
Client UI state → React context（session, csrfToken）
URL state       → React Router（page/pageSize/sort/filter 作为 search params）
Component state → useState / useReducer
```

## 4. Dependencies on `@xtrape/capsule-contracts-node`

The UI MUST install the contracts package from npm (NEVER from a workspace `link:` path in committed code):

```jsonc
// xtrape-capsule-ce/apps/opstage-ui/package.json
{
  "dependencies": {
    "@xtrape/capsule-contracts-node": "^0.1.0",
    "antd": "^5.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "react-router-dom": "^7.0.0",
    "@tanstack/react-query": "^5.0.0",
    "zod": "^3.0.0"
  }
}
```

The UI consumes from the contracts package:

- TypeScript types for every request/response shape;
- Zod schemas for client-side validation;
- status enum constants (`AgentStatus`, `CapsuleServiceStatus`, etc.);
- error code constants and the `ErrorEnvelope` shape;
- ID prefix constants (mostly for display formatting).

## 5. Page Structure

Routes are defined in `src/router/index.tsx` using React Router 7 lazy loading:

```text
/login                              LoginPage.tsx
/dashboard                          DashboardPage.tsx
/agents                             AgentListPage.tsx
/agents/:agentId                    AgentDetailPage.tsx
/registration-tokens                RegistrationTokenListPage.tsx
/capsule-services                   CapsuleServiceListPage.tsx
/capsule-services/:serviceId        CapsuleServiceDetailPage.tsx
/capsule-services/:serviceId/...    (tabs=overview|manifest|configs|actions|commands|audit)
/commands                           CommandListPage.tsx
/commands/:commandId                CommandDetailPage.tsx
/audit-events                       AuditEventListPage.tsx
/audit-events/:auditEventId         AuditEventDetailPage.tsx
/settings                           SettingsPage.tsx
```

A `<RequireAuth>` wrapper component redirects to `/login` if the session context is empty after `GET /api/admin/auth/me` resolves.

## 6. Layout

Common layout (`src/components/AppShell.tsx`):

```text
<Layout>
  <Layout.Header>      (top bar: logo, user dropdown)
  <Layout>
    <Layout.Sider>     (sidebar navigation)
    <Layout.Content>   (router outlet + ErrorBoundary)
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

## 7. Core Pages

### 7.1 Login

Responsibilities:

- username/password login via antd `Form`;
- on success: hydrate session context, redirect to dashboard;
- on failure: show generic antd `Alert` (do not reveal which field failed).

### 7.2 Dashboard

Show:

- `<Statistic>` cards: Agent（代理） counts by status, Capsule Service（胶囊服务） counts by status;
- `<Table>`: recent failed Commands (last 10);
- `<Table>`: recent AuditEvents (last 10);
- `<Card>`: quick start checklist (only when no Agents are registered yet).

### 7.3 Agent（代理） List / Detail

List columns (`<Table>`):

```text
code
name
mode
runtime
status (with <Tag color={statusColor}>)
lastHeartbeatAt
createdAt
```

Detail sections (`<Tabs>`):

- basic info;
- status and heartbeat history;
- related Capsule Services;
- recent Commands;
- admin actions: disable, enable, revoke (each behind `<Popconfirm>` for confirmation).

### 7.4 Capsule Service（胶囊服务） List / Detail

List columns:

```text
code
name
runtime
version
status (effective)
healthStatus (last reported)
agent
lastReportedAt
```

Detail tabs (`<Tabs>`):

```text
Overview
Manifest
Health
Configs
Actions
Commands
Audit Events
```

This is the core CE（社区版） v0.1 page. Tab content is route-driven (`/capsule-services/:serviceId/<tab>`).

### 7.5 Action Execution UX

Action execution flow:

1. user opens action dialog (`<Modal>`);
2. UI displays action label, description, danger level (`<Tag color="red|orange|blue">`), confirmation requirement, and input schema if available;
3. user enters JSON payload via `<Input.TextArea>` (validated against `inputSchema` using `ajv`);
4. HIGH or `requiresConfirmation` actions require an explicit second-step confirmation checkbox + `<Popconfirm>`;
5. UI calls `POST /api/admin/capsule-services/{serviceId}/actions/{actionName}` via `useExecuteAction()` mutation;
6. UI links to the created Command's detail page.

UI MUST NOT expose shell, exec, or arbitrary script execution as a normal CE（社区版） feature.

### 7.6 Commands

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
- payload JSON (`<json-viewer>`-style component or just `<pre>`);
- result JSON;
- error details (with mapped friendly text from `useApiErrorMessage`);
- audit trail if available.

### 7.7 Audit Events

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

Filter chips above the table for: `actorType`, `targetType`, `result`, date range.

Detail page shows the full metadata JSON with sensitive fields redacted (the backend already redacts; UI just displays).

### 7.8 Settings

CE（社区版） v0.1 settings should include:

- create registration token (with one-time `rawToken` reveal in a `<Modal>` after creation; can be copied once, never shown again);
- list/revoke registration tokens;
- system version (read from `GET /api/system/version`);
- system health (`GET /api/system/health`).

Avoid EE（企业版）/Cloud（云版） settings such as tenant, billing, SSO, license, and RBAC.

## 8. UI Safety Rules

- Do not show raw registration tokens after the initial creation modal closes.
- Do not show raw Agent（代理） tokens, ever.
- Mask sensitive config values (the backend does this server-side; UI just renders).
- Require confirmation (`<Popconfirm>` or HIGH-action modal) for dangerous actions.
- Do not treat stale/offline services as healthy — `<Tag color="orange">` for STALE.
- Do not call Agent（代理） endpoints (`/api/agents/*`) directly from the browser — UI uses `/api/admin/*` only.
- Do not embed user-supplied HTML; use React's default escaping (never use `dangerouslySetInnerHTML`).

## 8.1 API Client Rules

A single fetch wrapper at `apps/opstage-ui/src/api.ts` is the only allowed `fetch` caller (enforced by ESLint `no-restricted-globals: ["fetch"]`).

- always sends `credentials: "include"`;
- adds `X-CSRF-Token` from session context on every non-GET request;
- on `401`: clears session context, navigates to `/login`;
- on `403 CSRF_INVALID`: refreshes via `GET /api/admin/auth/csrf` and retries once;
- maps `ErrorEnvelope` to a typed `ApiError` instance with `httpStatus`, `code`, `message`, `details`.

See ADR 0007 for the implementation sketch.

## 8.2 TanStack React Query Conventions

```text
queryKey         [<resource>, <id?>, <params?>]
staleTime        30_000 ms (matches heartbeat cadence)
gcTime           300_000 ms
refetchOnWindowFocus  true
retry            1 (only on 5xx and NETWORK_ERROR)
```

Mutations MUST invalidate the relevant list query on success. CE（社区版） v0.1 does NOT use optimistic updates.

The `QueryClient` is configured in `src/lib/query-client.ts` and provided via `<QueryClientProvider>` in `src/main.tsx`.

## 9. Vite 配置

```ts
// apps/opstage-ui/vite.config.ts (sketch)
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": "http://localhost:8080",
    },
  },
  build: {
    outDir: "../opstage-backend/public",   // backend serves built static assets
    emptyOutDir: true,
  },
});
```

## 10. Test Plan

Minimum UI tests (`vitest run`):

- login screen renders;
- dashboard renders authenticated summary;
- Agent（代理） list renders;
- Capsule Service（胶囊服务） detail renders core tabs;
- action dialog creates Command (mocked API);
- command detail shows result;
- audit event list renders;
- sensitive config value is masked.

Component tests use `@testing-library/react` for user-interaction-style assertions. Avoid testing implementation details.

## 11. Migration Note (for future EE（企业版）)

If EE（企业版） later requires:

- i18n: wrap all strings in `t("...")` in CE（社区版） v0.1 already, so swapping in `vue-i18n` is purely additive;
- RBAC: feature hooks already accept the `user` from session context; gating logic added at the hook level only;
- multi-tenant: every `useAgents()`-style composable already passes `workspaceId` to the URL — wiring multiple workspaces is route-level only.

These hooks are documented to keep CE（社区版） v0.1 simple while not blocking EE（企业版）.
