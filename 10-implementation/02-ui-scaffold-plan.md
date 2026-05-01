# CE v0.1 UI Scaffold Plan

- Status: Implementation Guidance
- Edition: CE
- Priority: Current
- Audience: frontend developers, product designers, backend developers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs (especially ADR 0007) or `09-contracts/openapi/opstage-ce-v0.1.yaml` disagree, the ADRs and OpenAPI contract win for CE v0.1.

## 1. Goal

Build the Opstage CE UI as a simple, useful governance console for the CE v0.1 loop, using Vue 3 + Ant Design Vue.

The UI MUST conform to:

```text
09-contracts/openapi/opstage-ce-v0.1.yaml
```

## 2. Package

Lives inside the CE monorepo (`xtrape-capsule-ce`):

```text
xtrape-capsule-ce/apps/opstage-ui          (workspace package: @xtrape/opstage-ui — private)
```

## 3. Stack

Per [ADR 0007](../08-decisions/0007-ui-state-and-data-fetching.md):

```text
Vue                     3.5.x   (Composition API + <script setup> only)
TypeScript              5.x     (strict)
Vite                    5.x
Ant Design Vue          4.x
@tanstack/vue-query     5.x
Pinia                   2.x
Vue Router              4.x
Vee-Validate            4.x     (+ @vee-validate/zod)
Zod                     3.x     (re-exported from @xtrape/capsule-contracts-node)
@vueuse/core            11.x
Vitest                  2.x
Playwright                        optional, for happy-path E2E
```

State boundaries:

```text
Server state    → TanStack Vue Query
Form state      → Vee-Validate
Client UI state → Pinia (session, csrfToken, theme)
URL state       → Vue Router (page/pageSize/sort/filter)
Component state → ref / reactive
```

## 4. Dependencies on `@xtrape/capsule-contracts-node`

The UI MUST install the contracts package from npm (NEVER from a workspace `link:` path in committed code):

```jsonc
// xtrape-capsule-ce/apps/opstage-ui/package.json
{
  "dependencies": {
    "@xtrape/capsule-contracts-node": "^0.1.0",
    "ant-design-vue": "^4.0.0",
    "vue": "^3.5.0",
    "vue-router": "^4.0.0",
    "pinia": "^2.0.0",
    "@tanstack/vue-query": "^5.0.0",
    "vee-validate": "^4.0.0",
    "@vee-validate/zod": "^4.0.0",
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

Routes are defined in `src/router/index.ts` using Vue Router 4 lazy loading:

```text
/login                              LoginView.vue
/dashboard                          DashboardView.vue
/agents                             AgentListView.vue
/agents/:agentId                    AgentDetailView.vue
/registration-tokens                RegistrationTokenListView.vue
/capsule-services                   CapsuleServiceListView.vue
/capsule-services/:serviceId        CapsuleServiceDetailView.vue
/capsule-services/:serviceId/health CapsuleServiceDetailView.vue (tab=health)
/capsule-services/:serviceId/...    (tabs=overview|manifest|configs|actions|commands|audit)
/commands                           CommandListView.vue
/commands/:commandId                CommandDetailView.vue
/audit-events                       AuditEventListView.vue
/audit-events/:auditEventId         AuditEventDetailView.vue
/settings                           SettingsView.vue
```

A guard composable `useRequireAuth()` redirects to `/login` if the Pinia session is empty after `GET /api/admin/auth/me` resolves.

## 6. Layout

Common layout (`src/components/AppShell.vue`):

```text
<a-layout>
  <a-layout-header>      (top bar: logo, user dropdown, theme toggle)
  <a-layout>
    <a-layout-sider>     (sidebar navigation)
    <a-layout-content>   (router-view + ErrorBoundary)
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

- username/password login via Vee-Validate form;
- on success: hydrate Pinia, redirect to dashboard;
- on failure: show generic Ant Design Vue `a-alert` (do not reveal which field failed).

### 7.2 Dashboard

Show:

- `<a-statistic>` cards: Agent counts by status, Capsule Service counts by status;
- `<a-table>`: recent failed Commands (last 10);
- `<a-table>`: recent AuditEvents (last 10);
- `<a-card>`: quick start checklist (only when no Agents are registered yet).

### 7.3 Agent List / Detail

List columns (`<a-table>`):

```text
code
name
mode
runtime
status (with <a-tag color={statusColor}>)
lastHeartbeatAt
createdAt
```

Detail sections (`<a-tabs>`):

- basic info;
- status and heartbeat history;
- related Capsule Services;
- recent Commands;
- admin actions: disable, enable, revoke (each behind `<a-popconfirm>` for confirmation).

### 7.4 Capsule Service List / Detail

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

Detail tabs (`<a-tabs>`):

```text
Overview
Manifest
Health
Configs
Actions
Commands
Audit Events
```

This is the core CE v0.1 page. Tab content is route-driven (`/capsule-services/:serviceId/<tab>`).

### 7.5 Action Execution UX

Action execution flow:

1. user opens action dialog (`<a-modal>`);
2. UI displays action label, description, danger level (`<a-tag color="red|orange|blue">`), confirmation requirement, and input schema if available;
3. user enters JSON payload via `<a-textarea>` (validated against `inputSchema` using `ajv`);
4. HIGH or `requiresConfirmation` actions require an explicit second-step confirmation checkbox + `<a-popconfirm>`;
5. UI calls `POST /api/admin/capsule-services/{serviceId}/actions/{actionName}` via `useExecuteAction()` mutation;
6. UI links to the created Command's detail page.

UI MUST NOT expose shell, exec, or arbitrary script execution as a normal CE feature.

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

CE v0.1 settings should include:

- create registration token (with one-time `rawToken` reveal in a `<a-modal>` after creation; can be copied once, never shown again);
- list/revoke registration tokens;
- system version (read from `GET /api/system/version`);
- system health (`GET /api/system/health`).

Avoid EE/Cloud settings such as tenant, billing, SSO, license, and RBAC.

## 8. UI Safety Rules

- Do not show raw registration tokens after the initial creation modal closes.
- Do not show raw Agent tokens, ever.
- Mask sensitive config values (the backend does this server-side; UI just renders).
- Require confirmation (`<a-popconfirm>` or HIGH-action modal) for dangerous actions.
- Do not treat stale/offline services as healthy — `<a-tag color="orange">` for STALE.
- Do not call Agent endpoints (`/api/agents/*`) directly from the browser — UI uses `/api/admin/*` only.
- Do not embed user-supplied HTML; Vue's default escaping is sufficient if `v-html` is never used (ESLint rule `vue/no-v-html` enforces this).

## 8.1 API Client Rules

A single fetch wrapper at `apps/opstage-ui/src/lib/api-client.ts` is the only allowed `fetch` caller (enforced by ESLint `no-restricted-globals: ["fetch"]`).

- always sends `credentials: "include"`;
- adds `X-CSRF-Token` from the Pinia store on every non-GET request;
- on `401`: clears the Pinia session, pushes `/login`;
- on `403 CSRF_TOKEN_MISMATCH`: refreshes via `GET /api/admin/auth/csrf` and retries once;
- maps `ErrorEnvelope` to a typed `ApiError` instance with `httpStatus`, `code`, `message`, `details`.

See ADR 0007 for the implementation sketch.

## 8.2 TanStack Vue Query Conventions

```text
queryKey         [<resource>, <id?>, <params?>]
staleTime        30_000 ms (matches heartbeat cadence)
gcTime           300_000 ms
refetchOnWindowFocus  true
retry            1 (only on 5xx and NETWORK_ERROR)
```

Mutations MUST invalidate the relevant list query on success. CE v0.1 does NOT use optimistic updates.

The `QueryClient` is configured in `src/lib/query-client.ts` and installed via `app.use(VueQueryPlugin, { queryClient })`.

## 9. Vite Configuration

```ts
// apps/opstage-ui/vite.config.ts (sketch)
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import Components from "unplugin-vue-components/vite";
import { AntDesignVueResolver } from "unplugin-vue-components/resolvers";

export default defineConfig({
  plugins: [
    vue(),
    Components({
      resolvers: [AntDesignVueResolver({ importStyle: false })],
    }),
  ],
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

`unplugin-vue-components` + `AntDesignVueResolver` auto-imports Ant Design Vue components, so SFC files don't need explicit `import { Button } from "ant-design-vue"`. CSS for AntDV is imported once in `main.ts` via `import "ant-design-vue/dist/reset.css"`.

## 10. Test Plan

Minimum UI tests (`vitest run`):

- login screen renders;
- dashboard renders authenticated summary;
- Agent list renders;
- Capsule Service detail renders core tabs;
- action dialog creates Command (mocked API);
- command detail shows result;
- audit event list renders;
- sensitive config value is masked.

Component tests use `@vue/test-utils` + `@testing-library/vue` for user-interaction-style assertions. Avoid testing implementation details (do not snapshot computed refs).

## 11. Migration Note (for future EE)

If EE later requires:

- i18n: wrap all strings in `t("...")` in CE v0.1 already, so swapping in `vue-i18n` is purely additive;
- RBAC: feature composables already accept the `user` from Pinia; gating logic added at the composable level only;
- multi-tenant: every `useAgents()`-style composable already passes `workspaceId` to the URL — wiring multiple workspaces is route-level only.

These hooks are documented to keep CE v0.1 simple while not blocking EE.
