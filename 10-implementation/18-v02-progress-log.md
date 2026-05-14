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
| `xtrape-capsule-demo` | `v0.2` | [#14](https://github.com/xtrape-com/xtrape-capsule-demo/pull/14) | open |

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
- Post-review consistency pass for rc.1: release-notes banner shifted to "(release candidate)", "Not included in v0.2" section added, version-compatibility opens with the general "pin matching minors" rule, Docker install docs aligned with the actual `docker-publish.yml` tag strategy (no `latest`).

### Demo (`xtrape-capsule-demo`)

- Bumped to `0.2.0-rc.1`. `agent-node` / `contracts-node` dep ranges held on the published `0.1.0-public-review.0` for the rc window; will graduate to `^0.2.x` at the release-cut commit.
- `failOnce` refactored from `throw new Error(...)` to a structured `{ success: false, error: { code: "DEMO_FAILURE", message } }` return — the v0.2 command failure surface (CE lifts `errorCode` + `errorMessage` onto the commands row) needs that shape to render properly.
- New `docs/v0.2-smoke-test.md`: full step-by-step verification of the v0.2 surface — effective-status transitions (HEALTHY → STALE → OFFLINE), command `durationMs`, structured failure, `/health` + `/api/system/{health,version}` (asserts no `0.1.0` fallback in dev mode), and the enriched `/api/admin/metrics` shape.
- README v0.2 banner + Version Compatibility block.

## Review-driven rc.1 fixes (2026-05-14)

Per `12-prompts/019.xtrape-capsule-v0.2-commercial-review-conclusion.md`,
the cross-repo review surfaced these blockers and they have been
addressed on the `v0.2` branches:

- **CE-1**: `deriveEffectiveStatus` — agent stored OFFLINE was mapping to service `STALE`. Tightened so stored OFFLINE → service `OFFLINE`. Added 8 unit tests in `effective-status.test.ts` covering the agent-state matrix.
- **CE-2**: `0.1.0` literal fallback in `/api/system/health`, `/api/system/version`, `runtimeDiagnostics` replaced with a single `BACKEND_FALLBACK_VERSION = "0.2.0-dev"` constant. Build-injected `OPSTAGE_VERSION` still wins.
- **CE-3**: `docker-publish.yml` gets a header comment block documenting the published tag set (edge / branch / semver / major.minor / sha-<long>) and that `latest` is intentionally NOT published.
- **AGENT-1/2**: Example service versions bumped from `"0.1.0"` to `"0.2.0-example"` with clarifying comment; package bumped to `0.2.0-rc.1`.
- **CONTRACTS-1/2**: README "ID Helpers" reworked to "ID generation" with runnable `nanoid` factory example, new "Breaking changes in 0.2.0" section. CHANGELOG `0.2.0-rc.1` entry. Package bumped to `0.2.0-rc.1`.
- **SITE-1/2/3**: Release notes audited line-by-line against actual code; unverifiable claims either confirmed or moved to "Not included in v0.2". Version-compatibility opens with the general "pin matching minors" rule. Docker install docs aligned with workflow tag strategy.
- **Demo alignment** (after the review): demo bumped to `0.2.0-rc.1`, `failOnce` returns structured failure, smoke-test guide added.

## Cross-cutting decisions captured

- **ADR-0010** (this corpus): ephemeral action-secrets cache. Mirrors public CE ADR `docs/adr/0001-ephemeral-action-secrets.md`.
- **Audit metadata redactor split** — `redactAuditMetadata` (value-based) replaces the key-based pass inside `writeAudit`; legitimate field names like `revokedTokens` no longer get clobbered.
- **Agent token rotation on re-register** — re-registering an existing agent revokes prior ACTIVE tokens and writes `agent.token.rotated`. Previously prior tokens remained ACTIVE until explicit Revoke Agent.
- **Cookie `Secure` default-on** — strict `SESSION_SECRET` schema (≥ 32 chars) is now required.

## Deferred from v0.2

- **CE #13** (route UI `apiList` through `apiFetch`). Out of scope for this cut; deferred to v0.3. Release notes updated to reflect this.
- **zh-CN site translation** for the new v0.2 pages. Tracked, not delivered in this cut.
- **Quick-start docs / getting-started polish** — unchanged from v0.1 in this cut.
- **Empty-state / error-message / audit-filter UI polish.**
- **`latest` Docker tag** — workflow intentionally does not publish it; install docs pin to `0.2.0`.

## Verification at log time

```
xtrape-capsule-ce/apps/opstage-ui:        pnpm typecheck ✅  pnpm test 8/8 ✅  pnpm build ✅
xtrape-capsule-ce/apps/opstage-backend:   pnpm test 32/32 ✅  (was 24, +8 effectiveStatus)
xtrape-capsule-agent-node:                pnpm test 30/30 ✅
xtrape-capsule-contracts-node:            pnpm test 33/33 ✅
xtrape-capsule-demo:                      pnpm typecheck ✅  pnpm build ✅
xtrape-capsule-site:                      pnpm docs:build ✅
```
