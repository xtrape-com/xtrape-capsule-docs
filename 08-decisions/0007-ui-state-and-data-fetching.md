# ADR 0007: CE v0.1 UI State and Data Fetching

- Status: Accepted
- Edition: CE
- Priority: Current
- Audience: frontend developers, product designers, backend developers, AI coding agents

## Decision

Opstage CE UI is a **Vue 3** SPA built with **Ant Design Vue** for components, **TanStack Vue Query** for server state, and **Pinia** for the small slice of client state that does not belong on the server. There is no Vuex, no hand-rolled global event bus, no Composition API helpers reinventing what Vue Router or Pinia already provides.

This ADR replaces the React/Zustand stack proposed in earlier drafts. Frontend lives in `xtrape-capsule-ce/apps/opstage-ui` (CE monorepo).

## Stack

```text
Vue                     3.5.x   (Composition API + <script setup> only)
TypeScript              5.x     (strict)
Vite                    5.x
Ant Design Vue          4.x
@tanstack/vue-query     5.x     (server state)
Pinia                   2.x     (small client state slice)
Vue Router              4.x
Vee-Validate            4.x     (form validation; resolves Zod schemas via @vee-validate/zod)
Zod                     3.x     (shared with Backend via @xtrape/capsule-contracts-node)
@vueuse/core            11.x    (a few primitive composables: useElementVisibility, etc.)
Vitest                  2.x
Playwright                       optional, for happy-path E2E
```

The Vue version, Vue Router, and Pinia choices are normative for CE v0.1. Replacing any of them requires a new ADR.

## State Boundaries

```text
Server state    → TanStack Vue Query                  # everything fetched from /api/*
Form state      → Vee-Validate (driven by Zod)        # transient input
Client UI state → Pinia                               # the small global pieces below
URL state       → Vue Router (query string + params)  # filters, pagination, sort
Component state → ref / reactive                      # everything else
```

The `csrfToken` is stored in a Pinia store and re-hydrated from `GET /api/admin/auth/me` on bootstrap (see ADR 0004). It MUST NOT be persisted to `localStorage` or `sessionStorage`.

## Pinia App Store (CE v0.1)

```ts
// apps/opstage-ui/src/stores/app-store.ts
import { defineStore } from "pinia";
import { ref } from "vue";

export type AdminUser = {
  id: string;
  username: string;
  displayName: string | null;
  role: "owner";
  status: "ACTIVE" | "DISABLED";
};

export const useAppStore = defineStore("app", () => {
  const bootstrapped = ref(false);
  const user = ref<AdminUser | null>(null);
  const csrfToken = ref<string | null>(null);
  const sessionExpiresAt = ref<string | null>(null);
  const theme = ref<"light" | "dark">("light");

  function setSession(s: { user: AdminUser; csrfToken: string; expiresAt: string }) {
    user.value = s.user;
    csrfToken.value = s.csrfToken;
    sessionExpiresAt.value = s.expiresAt;
    bootstrapped.value = true;
  }

  function clearSession() {
    user.value = null;
    csrfToken.value = null;
    sessionExpiresAt.value = null;
  }

  function setCsrfToken(t: string) { csrfToken.value = t; }
  function setTheme(t: "light" | "dark") { theme.value = t; }

  return {
    bootstrapped, user, csrfToken, sessionExpiresAt, theme,
    setSession, clearSession, setCsrfToken, setTheme,
  };
});
```

The store MUST be persisted to neither `localStorage` nor `sessionStorage` (no `pinia-plugin-persistedstate`). The session and CSRF token come from the server on every page load via `GET /api/admin/auth/me`.

## API Client

A single thin fetch wrapper lives in `apps/opstage-ui/src/lib/api-client.ts`. Rules:

- always sends `credentials: "include"` so the session cookie is attached;
- adds `X-CSRF-Token` from the Pinia store on every non-GET request;
- on `401`: clears the Pinia session and pushes the `login` route via `useRouter()`;
- on `403` with `error.code === "CSRF_TOKEN_MISMATCH"`: calls `GET /api/admin/auth/csrf`, updates Pinia, retries the request once;
- on `4xx` errors: throws an `ApiError` with `httpStatus`, `code`, `message`, `details` (parsed from `ErrorEnvelope`);
- on network error: throws an `ApiError` with `code: "NETWORK_ERROR"`.

The wrapper is the only allowed `fetch` caller in the UI; ESLint rule `no-restricted-globals: ["fetch"]` enforces this. Pages and components MUST go through `features/<x>/use*.ts` composables, which in turn call this wrapper — they never call `fetch` directly.

```ts
// apps/opstage-ui/src/lib/api-client.ts (sketch)
import { useAppStore } from "@/stores/app-store";
import type { ErrorEnvelope } from "@xtrape/capsule-contracts-node";

export class ApiError extends Error {
  constructor(
    public httpStatus: number,
    public code: string,
    message: string,
    public details?: Record<string, unknown>,
  ) { super(message); }
}

export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const store = useAppStore();
  const isMutation = init.method && init.method !== "GET";
  const headers = new Headers(init.headers);
  headers.set("Accept", "application/json");
  if (init.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  if (isMutation && store.csrfToken) headers.set("X-CSRF-Token", store.csrfToken);

  const res = await fetch(path, { ...init, headers, credentials: "include" });
  if (res.ok) return (res.status === 204 ? (undefined as T) : await res.json());
  const env = (await res.json().catch(() => undefined)) as ErrorEnvelope | undefined;

  if (res.status === 401) { store.clearSession(); /* router push to /login handled by app shell */ }
  if (res.status === 403 && env?.error.code === "CSRF_TOKEN_MISMATCH" && !init.headers?.["X-Retry"]) {
    const fresh = await fetch("/api/admin/auth/csrf", { credentials: "include" });
    const json = await fresh.json();
    store.setCsrfToken(json.data.csrfToken);
    return apiFetch<T>(path, { ...init, headers: { ...init.headers, "X-Retry": "1" } });
  }
  throw new ApiError(res.status, env?.error.code ?? "INTERNAL_ERROR", env?.error.message ?? res.statusText, env?.error.details);
}
```

## TanStack Vue Query Conventions

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
- show success/failure via Ant Design Vue `message` / `notification`;
- never optimistically update lists in CE v0.1 (keep it simple).

```ts
// apps/opstage-ui/src/features/agents/use-agents.ts
import { useQuery } from "@tanstack/vue-query";
import { apiFetch } from "@/lib/api-client";

export function useAgents(params: Ref<{ page: number; pageSize: number; status?: string[] }>) {
  return useQuery({
    queryKey: ["agents", params],
    queryFn: () => apiFetch(`/api/admin/agents?${new URLSearchParams(params.value as any)}`),
    staleTime: 30_000,
  });
}
```

## File / Folder Layout

```text
apps/opstage-ui/src/
├── main.ts
├── App.vue
├── router/
│   └── index.ts                  (Vue Router routes; lazy-loaded views)
├── views/                        (route components)
│   ├── LoginView.vue
│   ├── DashboardView.vue
│   ├── agents/
│   │   ├── AgentListView.vue
│   │   └── AgentDetailView.vue
│   ├── registration-tokens/
│   │   └── RegistrationTokenListView.vue
│   ├── capsule-services/
│   │   ├── CapsuleServiceListView.vue
│   │   ├── CapsuleServiceDetailView.vue
│   │   └── tabs/{Overview,Manifest,Health,Configs,Actions,Commands,Audit}.vue
│   └── audit-events/
│       ├── AuditEventListView.vue
│       └── AuditEventDetailView.vue
├── components/                   (shared presentational components)
├── features/                     (feature-scoped composables + components)
│   ├── auth/                       useSession, useLogin, useLogout
│   ├── agents/                     useAgents, useAgent, useDisableAgent, ...
│   ├── capsule-services/
│   ├── commands/
│   └── audit-events/
├── stores/
│   └── app-store.ts
├── lib/
│   ├── api-client.ts
│   ├── query-client.ts             (createQueryClient + VueQueryPlugin install)
│   └── format.ts
└── styles/
```

Rules:

- Each `features/<x>/` directory exposes a small set of typed composables (`useAgents()`, etc.) that wrap TanStack Vue Query against the OpenAPI contract. Components MUST consume these composables; they MUST NOT call `apiFetch` directly.
- Views are thin: they read URL params via `useRoute()`, call composables, and render Ant Design Vue components.
- `<script setup lang="ts">` is the only Vue SFC variant used. Options API is forbidden.

## Forms

All forms use **Vee-Validate 4** with Zod resolvers. The same Zod schemas exported by `@xtrape/capsule-contracts-node` are used for both Backend and UI validation, so the UI can short-circuit obvious errors before round-tripping the server.

```vue
<!-- apps/opstage-ui/src/features/registration-tokens/CreateTokenForm.vue -->
<script setup lang="ts">
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";
import { createRegistrationTokenRequestSchema } from "@xtrape/capsule-contracts-node";

const { handleSubmit, errors, defineField } = useForm({
  validationSchema: toTypedSchema(createRegistrationTokenRequestSchema),
});

const [name] = defineField("name");
const [expiresInSeconds] = defineField("expiresInSeconds");

const onSubmit = handleSubmit(async (values) => {
  // values is fully typed from the Zod schema
  // call useCreateRegistrationToken().mutateAsync(values)
});
</script>
```

## Error Surface

`ApiError` is converted to user-facing copy via a `useApiErrorMessage(err)` composable that maps `error.code` → friendly text (with a fallback to `error.message`). Authentication-related codes (`UNAUTHORIZED`, `CSRF_TOKEN_MISMATCH`) are handled by the API client and never bubble to components.

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

The map MUST stay in sync with `09-contracts/errors.json`; a small script in CI verifies every error code listed there has either a UI mapping or an explicit "internal-only" allow-list entry.

## Forbidden in CE v0.1

- WebSockets / SSE for live updates (UI polls; query refetch is sufficient);
- Service Worker / offline mode;
- i18n framework (English only — strings live inline, but MUST go through a thin `t("...")` wrapper so EE can switch to vue-i18n without churn);
- Theme builder UI;
- Vuex (replaced by Pinia);
- Options API (only `<script setup>`);
- Any state library other than TanStack Vue Query + Pinia;
- `pinia-plugin-persistedstate` (session is server-side, never local-cache);
- Direct `fetch` calls outside `lib/api-client.ts`.

## Acceptance Criteria

- `apps/opstage-ui` boots, mounts the `VueQueryPlugin`, and bootstraps session via `GET /api/admin/auth/me`.
- All non-GET requests carry `X-CSRF-Token`.
- A 403 `CSRF_TOKEN_MISMATCH` triggers exactly one silent token refresh + retry; if that retry fails, the user sees an Ant Design Vue notification.
- A 401 redirects to `/login` and clears the Pinia session.
- `localStorage`/`sessionStorage` is empty after login (verifiable via DevTools).
- Every form imports its Zod schema from `@xtrape/capsule-contracts-node`; no schema is duplicated in the UI.
