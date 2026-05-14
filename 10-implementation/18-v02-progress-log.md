---
status: in-progress
audience: ai-coding-agents
stability: evolving
last_reviewed: 2026-05-14
edition: ce
phase: v0.2
---

# CE v0.2 Implementation Progress Log

This log records what was actually shipped on the `v0.2` branches of the four public repositories during the Public Preview cycle. It is the implementation-side complement to `07-roadmap/01-ce-roadmap.md` § 18 (CE v0.2 Direction).

## Repository state at log time

| Repo | Branch | PR | Status |
| --- | --- | --- | --- |
| `xtrape-capsule-ce` | `v0.2` | [#16](https://github.com/xtrape-com/xtrape-capsule-ce/pull/16) | open |
| `xtrape-capsule-agent-node` | `v0.2` | [#7](https://github.com/xtrape-com/xtrape-capsule-agent-node/pull/7) | open |
| `xtrape-capsule-contracts-node` | `v0.2` | [#9](https://github.com/xtrape-com/xtrape-capsule-contracts-node/pull/9) | open |
| `xtrape-capsule-site` | `v0.2` | [#6](https://github.com/xtrape-com/xtrape-capsule-site/pull/6) | open |

## Shipped surfaces

### Runtime maturity (CE)

- **Effective status freshness.** `effectiveStatus` now folds agent online/offline state and heartbeat freshness, not only the last reported `healthStatus`. Service responses additionally carry `storedStatus` so historical/tooling consumers can still see the last persisted value.
- **Heartbeat write throttle.** The heartbeat handler no longer writes `agents.status` on every poll; only on `OFFLINE → ONLINE` transitions. Freshness is read from `lastHeartbeatAt` alone, removing one row write per agent per heartbeat interval.
- **System endpoints.** `/api/system/health` (SQLite probe + uptime + version + edition) and `/api/system/version` (commit + build timestamp from OCI labels) are now fully wired. Docker image build embeds OCI metadata at build time.
- **Command failure surface.** When the agent reports `success: false`, the backend lifts `errorCode` / `errorMessage` onto the `commands` row directly. Commands list endpoint + UI both render these without joining `command_results`. `durationMs` is computed at serialize time from `completedAt - startedAt`.
- **Metrics enhancement.** `/api/admin/metrics` now reports `commandDurations.{p50Ms,p95Ms,maxMs,meanMs,sampleSize}`, a `topErrorCodes` array, and an `agents.{total,online,offline,stale}` breakdown alongside the existing operational counters.

### UI refactor (CE)

- **ADR-0007 conformance complete.** `apps/opstage-ui/src/App.tsx` was split incrementally from 1193 lines down to 124 lines. New module layout under `apps/opstage-ui/src/`:
  - `lib/` — `types.ts`, `list-helpers.ts`, `format.ts`, `metrics.ts`.
  - `pages/` — one component per route: `LoginPage`, `DashboardPage`, `UsersPage`, `RegistrationTokensPage`, `AgentsPage`, `CommandsPage`, `AuditEventsPage`, `SettingsPage`, `LanguageSwitcher`.
  - `pages/services/` — `helpers.tsx` (schema/result/payload/account utilities), `SchemaPayloadFields.tsx`, `ActionResult.tsx` (four action-result components), `ServiceDrawer.tsx`, `ServicesPage.tsx`.
- Back-compat re-exports preserved on `App.tsx` for the symbols still imported by `action-result-list.test.tsx` (`formatBytes`, `formatDurationMs`, `diagnosticRows`, `hasMetricWarning`, `metricRows`, `formatRelativeTime`, `renderListCell`, `resolveRowPayload`, `resultRowKey`).
- Verified: `pnpm typecheck` clean, 8/8 UI tests pass, `pnpm build` green.

### Agent SDK (`xtrape-capsule-agent-node`)

- **Typed errors.** New `RegistrationError`, `AgentAuthError`, `NetworkError` subclasses. Registration / auth failures are non-retryable (thrown straight through); transport failures are retryable inside the SDK's backoff budget and surface as `NetworkError` after the budget exhausts. Replaces the previous untyped `Error` surface.
- **Structured logger sink.** Optional `onLog` callback receives `{ level, event, context, data }` records suitable for log aggregators. Falls back to the existing console-shaped sink when not supplied — pure addition, no breaking change to existing consumers.
- **`examples/` directory.** Runnable scripts (register, heartbeat, command execution) for new adopters.

### Contracts (`xtrape-capsule-contracts-node`)

- **`newId()` helper removed.** Together with the `nanoid` runtime dependency it pulled in. Intentional breaking change — verified that CE has no `newId` references. External consumers that minted local IDs from this helper must wire their own factory.

### Site (`xtrape-capsule-site`)

- New `docs/version-compatibility.md` (pinned-minor matrix), `docs/troubleshooting.md` (failure runbook), `docs/agents/lifecycle.md` (register → heartbeat → token rotation → revoke).
- `docs/releases/v0.2.0.md` draft + Releases nav restructure.
- v0.2 surface docs added: `Typed errors` + `Structured logging` sections in `node-embedded-agent.md`, system + metrics endpoint specs added to `concepts/management-contract.md`, one-time `generatedKey` operator paragraph added to `opstage-ce/admin-ui.md`.

## Cross-cutting decisions captured

- **ADR-0010** (this corpus): ephemeral action-secrets cache. Mirrors public CE ADR `docs/adr/0001-ephemeral-action-secrets.md`.
- **Audit metadata redactor split** — `redactAuditMetadata` (value-based) replaces the key-based pass inside `writeAudit`; legitimate field names like `revokedTokens` no longer get clobbered.
- **Agent token rotation on re-register** — re-registering an existing agent revokes prior ACTIVE tokens and writes `agent.token.rotated`. Previously prior tokens remained ACTIVE until explicit Revoke Agent.
- **Cookie `Secure` default-on** — strict `SESSION_SECRET` schema (≥ 32 chars) is now required.

## Deferred from v0.2

- **CE #13** (route UI `apiList` through `apiFetch`). Out of scope for this cut; deferred to v0.3. Release notes updated to reflect this.
- **zh-CN site translation** for the new v0.2 pages. Tracked, not delivered in this cut.

## Verification at log time

```
xtrape-capsule-ce/apps/opstage-ui:        pnpm typecheck ✅  pnpm test 8/8 ✅  pnpm build ✅
xtrape-capsule-ce/apps/opstage-backend:   pnpm test 24/24 ✅
xtrape-capsule-agent-node:                pnpm test 30/30 ✅
xtrape-capsule-contracts-node:            pnpm test 33/33 ✅
xtrape-capsule-site:                      pnpm docs:build ✅
```
