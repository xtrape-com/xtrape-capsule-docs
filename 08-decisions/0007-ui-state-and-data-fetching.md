# ADR 0007: CE v0.1 UI State and Data Fetching

- Status: Accepted
- Edition: CE
- Priority: Current
- Audience: frontend developers, product designers, backend developers, AI coding agents

## Decision

Opstage CE UI uses TanStack Query for server state and Zustand for the small slice of client state that does not belong on the server. There is **no** Redux, Recoil, MobX, or hand-rolled Context store in CE v0.1.

## Stack

```text
React           18.x  (function components only)
TypeScript      5.x   (strict)
Vite            5.x
Ant Design      5.x
TanStack Query  5.x   (React Query)
Zustand         4.x
React Router    6.x
React Hook Form 7.x
```

## State Boundaries

```text
Server state    → TanStack Query                # everything fetched from /api/*
Form state      → React Hook Form               # transient input
Client UI state → Zustand                       # the small global pieces below
URL state       → React Router (search params)  # filters, pagination, sort
```

The `csrfToken` is stored in a Zustand slice and re-hydrated from `GET /api/admin/auth/me` on bootstrap (see ADR 0004). It MUST NOT be persisted to localStorage.

## Zustand Store Shape (CE v0.1)

```ts
// apps/opstage-ui/src/stores/app-store.ts
import { create } from "zustand";

type AdminUser = {
  id: string;
  username: string;
  displayName: string | null;
  role: "owner";
  status: "ACTIVE" | "DISABLED";
};

type AppState = {
  // session
  bootstrapped: boolean;
  user: AdminUser | null;
  csrfToken: string | null;
  sessionExpiresAt: string | null;

  // global UI
  theme: "light" | "dark";

  setSession: (s: { user: AdminUser; csrfToken: string; expiresAt: string }) => void;
  clearSession: () => void;
  setCsrfToken: (token: string) => void;
  setTheme: (theme: "light" | "dark") => void;
};

export const useAppStore = create<AppState>((set) => ({
  bootstrapped: false,
  user: null,
  csrfToken: null,
  sessionExpiresAt: null,
  theme: "light",
  setSession: ({ user, csrfToken, expiresAt }) =>
    set({ user, csrfToken, sessionExpiresAt: expiresAt, bootstrapped: true }),
  clearSession: () => set({ user: null, csrfToken: null, sessionExpiresAt: null }),
  setCsrfToken: (csrfToken) => set({ csrfToken }),
  setTheme: (theme) => set({ theme }),
}));
```

The store MUST be persisted to neither `localStorage` nor `sessionStorage`. The session and CSRF token come from the server on every page load via `GET /api/admin/auth/me`.

## API Client

A single thin fetch wrapper lives in `apps/opstage-ui/src/lib/api-client.ts`. Rules:

- always sends `credentials: "include"` so the session cookie is attached;
- adds `X-CSRF-Token` from the Zustand store on every non-GET request;
- on `401`: clears the session and redirects to `/login`;
- on `403` with `error.code === "CSRF_INVALID"`: calls `GET /api/admin/auth/csrf`, updates Zustand, retries the request once;
- on `4xx` errors: throws an `ApiError` with `httpStatus`, `code`, `message`, `details` (parsed from `ErrorEnvelope`);
- on network error: throws an `ApiError` with `code: "NETWORK_ERROR"`.

The wrapper is the only allowed `fetch` caller in the UI; ESLint rule `no-restricted-globals: ["fetch"]` enforces this.

## TanStack Query Conventions

```text
queryKey shape          [<resource>, <id?>, <params?>]
                        e.g. ["agents", { page: 1, pageSize: 20, status: ["ACTIVE"] }]
                             ["agent", "agt_..."]
staleTime (default)     30_000 ms     # match heartbeat cadence
gcTime (default)        300_000 ms
refetchOnWindowFocus    true
refetchOnReconnect      true
retry                   1 (only on 5xx and NETWORK_ERROR)
```

Mutations:

- ALWAYS invalidate the relevant list key on success (`queryClient.invalidateQueries({ queryKey: ["agents"] })`);
- show success/failure via Ant Design `notification`;
- never optimistically update lists in CE v0.1 (keep it simple).

## File / Folder Layout

```text
apps/opstage-ui/src/
├── main.tsx
├── app.tsx
├── routes/
│   ├── login.tsx
│   ├── dashboard.tsx
│   ├── agents/{list,detail}.tsx
│   ├── registration-tokens/list.tsx
│   ├── capsule-services/{list,detail,actions,health,configs,audit}.tsx
│   └── audit-events/{list,detail}.tsx
├── components/         # shared UI
├── features/           # feature-scoped hooks + components
│   ├── auth/           # useSession, useLogin, useLogout
│   ├── agents/         # useAgents, useAgent, useDisableAgent, ...
│   └── ...
├── stores/
│   └── app-store.ts
├── lib/
│   ├── api-client.ts
│   ├── query-client.ts
│   └── format.ts
└── styles/
```

Each `features/<x>` directory exposes a small set of typed hooks that wrap TanStack Query against the OpenAPI contract. Components MUST consume these hooks; they MUST NOT call the API client directly.

## Forms

All forms use React Hook Form + Zod (via `@hookform/resolvers/zod`). The same Zod schemas in `packages/contracts` are used for both Backend and UI validation, so the UI can short-circuit obvious errors before round-tripping the server.

## Error Surface

`ApiError` is converted to user-facing copy via a `useApiErrorMessage(err)` hook that maps `error.code` → friendly text (with a fallback to `error.message`). Authentication-related codes (`AUTH_REQUIRED`, `CSRF_INVALID`) are handled by the api client and never bubble to components.

## Forbidden in CE v0.1

- WebSockets / SSE for live updates (UI polls; query refetch is sufficient);
- Service Worker / offline mode;
- i18n framework (English only — strings live inline, but MUST go through a thin `t("...")` wrapper so EE can switch to react-intl without churn);
- Theme builder UI;
- Any state library other than TanStack Query + Zustand.

## Acceptance Criteria

- `apps/opstage-ui` boots, mounts the `QueryClientProvider`, and bootstraps session via `GET /api/admin/auth/me`.
- All non-GET requests carry `X-CSRF-Token`.
- A 403 `CSRF_INVALID` triggers exactly one silent token refresh + retry; if that retry fails, the user sees a notification.
- A 401 redirects to `/login` and clears the Zustand session.
- `localStorage`/`sessionStorage` is empty after login (verifiable via DevTools).
