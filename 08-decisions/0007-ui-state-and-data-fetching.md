---
status: accepted
audience: ai-coding-agents
stability: stable
last_reviewed: 2026-05-14
---

# ADR 0007: CE v0.1 UI State and Data Fetching

> **v0.2 conformance note (2026-05-14):** the file-layout intent of this ADR
> (`apps/opstage-ui/src/{lib,pages,context,hooks,components}/`) is now fully
> realised. `App.tsx` was split from 1193 → 124 lines across three incremental
> commits on the `v0.2` branch:
>
> - `lib/` — `types.ts`, `list-helpers.ts`, `format.ts`, `metrics.ts`.
> - `pages/` — one component per route, plus `LanguageSwitcher`.
> - `pages/services/` — `helpers.tsx`, `SchemaPayloadFields`, `ActionResult`,
>   `ServiceDrawer`, `ServicesPage`.
>
> Back-compat re-exports are preserved on `App.tsx` for the symbols still
> imported by `action-result-list.test.tsx`. See
> `10-implementation/18-v02-progress-log.md` for the full record.

## Status

Accepted

## Date

2026-05-05

## Context

This ADR records an architecture or implementation decision for the current Xtrape Capsule CE design baseline. See the original decision notes below for the detailed background.

## Decision

Use the decision content below as the current baseline for this topic.

## Consequences

This decision constrains CE implementation work, related specifications, and future documentation maintenance. Detailed trade-offs are captured in the original decision notes below where available.

## Alternatives Considered

Not separately captured in this standardized template section. If alternatives are described in the original decision notes below, those notes remain authoritative.

## Implementation Notes

Implementation and documentation updates should follow this ADR status first, then align related `02-specs/` and current CE `10-implementation/` documents.

## Supersedes / Superseded By

None.

## Original Decision Notes


- Status: Accepted (supersedes the Vue 3 draft; React 18 is the implemented stack)
- Edition: CE
- Priority: Current
- Audience: frontend developers, product designers, backend developers, AI coding agents

## Decision

Opstage CE UI is a **React 18** SPA built with **Ant Design (antd 5.x)** for components, **TanStack React Query** for
server state, and **React component state plus module-scoped in-memory CSRF state** for the small slice of client state
that does not belong on the server.

Frontend lives in `xtrape-capsule-ce/apps/opstage-ui` (CE monorepo).

## Stack

```text
React                   18.x
TypeScript              5.x     (strict)
Vite                    5.x
antd                    5.x     (Ant Design React)
@tanstack/react-query   5.x     (server state)
react-router-dom        7.x     (URL state + routing)
Zod                     3.x     (shared with Backend via @xtrape/capsule-contracts-node)
Vitest                  2.x
Playwright                       optional, for happy-path E2E
```

## State Boundaries

```text
Server state    → TanStack React Query           # everything fetched from /api/*
Form state      → antd Form (built-in) + Zod     # transient input
Client UI state → React component state + module memory  # session, csrfToken
URL state       → React Router (search params)    # filters, pagination, sort
Component state → useState / useReducer           # everything else
```

The `csrfToken` is stored only in module-scoped memory and re-hydrated from `POST /api/admin/auth/login`, `GET
/api/admin/auth/me`, or `GET /api/admin/auth/csrf` (see ADR 0004). It MUST NOT be persisted to `localStorage` or
`sessionStorage`.

## Session and CSRF State (CE v0.1)

```ts
// apps/opstage-ui/src/api.ts (sketch)
let csrfToken = "";

export function setCsrfToken(token: string) {
  csrfToken = token;
}

export function clearCsrfToken() {
  csrfToken = "";
}

export async function refreshCsrfToken() {
  const res = await fetch("/api/admin/auth/csrf", { credentials: "include" });
  const env = await res.json();
  setCsrfToken(env.data.csrfToken);
}
```

The session and CSRF token MUST NOT be persisted to `localStorage` or `sessionStorage`. They come from the server on
every page load via `GET /api/admin/auth/me`, and CSRF can be refreshed via `GET /api/admin/auth/csrf`.

## API Client

A single thin fetch wrapper lives in `apps/opstage-ui/src/api.ts`. Rules:

- always sends `credentials: "include"` so the session cookie is attached;
- adds `X-CSRF-Token` from module-scoped memory on every non-GET request;
- on `401`: clears session context and navigates to `/login`;
- on `403` with `error.code === "CSRF_INVALID"`: calls `GET /api/admin/auth/csrf`, updates the in-memory token, retries the request once;
- on `4xx` errors: throws an `ApiError` with `httpStatus`, `code`, `message`, `details` (parsed from `ErrorEnvelope`);
- on network error: throws an `ApiError` with `code: "NETWORK_ERROR"`.

The wrapper is the only allowed `fetch` caller in the UI; ESLint rule `no-restricted-globals: ["fetch"]` enforces this.
Pages and components MUST call the wrapper or typed data hooks; they never call `fetch` directly.

```ts
// apps/opstage-ui/src/api.ts (sketch)
import type { ErrorEnvelope } from "@xtrape/capsule-contracts-node";

export class ApiError extends Error {
  constructor(
    public httpStatus: number,
    public code: string,
    message: string,
    public details?: Record<string, unknown>,
  ) { super(message); }
}

let csrfToken = "";
export function setCsrfToken(token: string) { csrfToken = token; }
export function clearCsrfToken() { csrfToken = ""; }

export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const isMutation = init.method && init.method !== "GET";
  const headers = new Headers(init.headers);
  headers.set("Accept", "application/json");
  if (init.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  if (isMutation && csrfToken) headers.set("X-CSRF-Token", csrfToken);

  const res = await fetch(path, { ...init, headers, credentials: "include" });
  if (res.ok) return (res.status === 204 ? (undefined as T) : await res.json());
  const env = (await res.json().catch(() => undefined)) as ErrorEnvelope | undefined;

  if (res.status === 401) { clearCsrfToken(); /* router navigation handled by app shell */ }
  if (res.status === 403 && env?.error.code === "CSRF_INVALID" && !headers.has("X-Retry")) {
    const fresh = await fetch("/api/admin/auth/csrf", { credentials: "include" });
    const json = await fresh.json();
    setCsrfToken(json.data.csrfToken);
    return apiFetch<T>(path, { ...init, headers: { ...Object.fromEntries(headers), "X-Retry": "1" } });
  }
  throw new ApiError(res.status, env?.error.code ?? "INTERNAL_ERROR", env?.error.message ?? res.statusText, env?.error.details);
}
```

## TanStack React Query Conventions

```text
queryKey shape          [<resource>, <id?>, <params?>]
                        e.g. ["agents", { page: 1, pageSize: 20, status: ["ONLINE"] }]
                             ["agent", "agt_..."]
staleTime (default)     30_000 ms     # match heartbeat cadence
gcTime (default)        300_000 ms
refetchOnWindowFocus    true
refetchOnReconnect      true
retry                   1 (only on 5xx and NETWORK_ERROR)
```

Mutations:

- ALWAYS invalidate the relevant list key on success (`queryClient.invalidateQueries({ queryKey: ["agents"] })`);
- show success/failure via antd `message` / `notification`;
- never optimistically update lists in CE v0.1 (keep it simple).

```ts
// apps/opstage-ui/src/hooks/use-agents.ts
import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "@/lib/api-client";

export function useAgents(params: { page: number; pageSize: number; status?: string[] }) {
  return useQuery({
    queryKey: ["agents", params],
    queryFn: () => apiFetch(`/api/admin/agents?${new URLSearchParams(params as any)}`),
    staleTime: 30_000,
  });
}
```

## File / Folder Layout

```text
apps/opstage-ui/src/
├── main.tsx
├── App.tsx
├── router/
│   └── index.tsx                 (React Router routes; lazy-loaded pages)
├── pages/                        (route components)
│   ├── LoginPage.tsx
│   ├── DashboardPage.tsx
│   ├── agents/
│   │   ├── AgentListPage.tsx
│   │   └── AgentDetailPage.tsx
│   ├── registration-tokens/
│   │   └── RegistrationTokenListPage.tsx
│   ├── capsule-services/
│   │   ├── CapsuleServiceListPage.tsx
│   │   ├── CapsuleServiceDetailPage.tsx
│   │   └── tabs/{Overview,Manifest,Health,Configs,Actions,Commands,Audit}.tsx
│   └── audit-events/
│       ├── AuditEventListPage.tsx
│       └── AuditEventDetailPage.tsx
├── components/                   (shared presentational components)
├── hooks/                        (feature-scoped query hooks + mutation hooks)
│   ├── auth/                       useSession, useLogin, useLogout
│   ├── agents/                     useAgents, useAgent, useDisableAgent, ...
│   ├── capsule-services/
│   ├── commands/
│   └── audit-events/
├── context/
│   └── session-context.tsx
├── lib/
│   ├── api-client.ts
│   ├── query-client.ts             (createQueryClient + QueryClientProvider)
│   └── format.ts
└── styles/
```

Rules:

- CE v0.1 currently exposes a small `useQueryData()` helper backed by TanStack React Query. Larger modules may split into `hooks/use*.ts` files as the UI grows.
- Pages are thin: they read URL params via `useSearchParams()`, call hooks, and render antd components.

## Forms

All forms use **antd Form** with Zod for schema validation. The same Zod schemas exported by `@xtrape/capsule-contracts-node` are used for both Backend and UI validation.

```tsx
// apps/opstage-ui/src/features/registration-tokens/CreateTokenForm.tsx
import { Form, Input, InputNumber, Button } from "antd";
import { createRegistrationTokenRequestSchema } from "@xtrape/capsule-contracts-node";

export function CreateTokenForm({ onSubmit }: { onSubmit: (values: unknown) => void }) {
  const [form] = Form.useForm();

  const handleFinish = (values: unknown) => {
    const parsed = createRegistrationTokenRequestSchema.safeParse(values);
    if (!parsed.success) { form.setFields(/* map Zod errors */); return; }
    onSubmit(parsed.data);
  };

  return (
    <Form form={form} onFinish={handleFinish} layout="vertical">
      <Form.Item name="name" label="Name">
        <Input />
      </Form.Item>
      <Form.Item name="expiresInSeconds" label="Expires in (seconds)">
        <InputNumber min={60} />
      </Form.Item>
      <Button type="primary" htmlType="submit">Create</Button>
    </Form>
  );
}
```

## Error Surface

`ApiError` is converted to user-facing copy via a `useApiErrorMessage(err)` hook that maps `error.code` → friendly text
(with a fallback to `error.message`). Authentication-related codes (`UNAUTHORIZED`, `CSRF_INVALID`) are handled by the
API client and never bubble to components.

```ts
// apps/opstage-ui/src/lib/use-api-error-message.ts
import type { ApiError } from "./api-client";

const map: Record<string, string> = {
  AGENT_NOT_FOUND: "This agent no longer exists. Refresh the list.",
  AGENT_DISABLED: "This agent is disabled.",
  ACTION_REQUIRES_CONFIRMATION: "This action requires explicit confirmation.",
  COMMAND_EXPIRED: "This command expired before the agent could complete it.",
  // ... see 09-contracts/errors.json for the full mapping
};

export function useApiErrorMessage(err: ApiError | null | undefined): string {
  if (!err) return "";
  return map[err.code] ?? err.message;
}
```

The map MUST stay in sync with `09-contracts/errors.json`; a small script in CI verifies every error code listed there
has either a UI mapping or an explicit "internal-only" allow-list entry.

## Forbidden in CE v0.1

- WebSockets / SSE for live updates (UI polls; query refetch is sufficient);
- Service Worker / offline mode;
- i18n framework (English only — strings live inline, but MUST go through a thin `t("...")` wrapper so EE can switch to react-i18next without churn);
- Theme builder UI;
- Any state library other than TanStack React Query plus local React state for CE v0.1;
- Session state in `localStorage` or `sessionStorage` (session is server-side);
- Direct `fetch` calls outside `api.ts`;
- `dangerouslySetInnerHTML` (use React's default escaping).

## Acceptance Criteria

- `apps/opstage-ui` boots, mounts `QueryClientProvider`, and bootstraps session via `GET /api/admin/auth/me`.
- All non-GET requests carry `X-CSRF-Token`.
- A 403 `CSRF_INVALID` triggers exactly one silent token refresh + retry; if that retry fails, the user sees an antd notification.
- A 401 redirects to `/login` and clears session context.
- `localStorage`/`sessionStorage` is empty after login (verifiable via DevTools).
- Every form imports its Zod schema from `@xtrape/capsule-contracts-node`; no schema is duplicated in the UI.
