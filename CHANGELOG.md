---
status: implemented
audience: maintainers
stability: stable
last_reviewed: 2026-05-16
---

# Design Changelog

## 2026-05-16 — CE v0.4 planning reconciliation

After a review pass on the three v0.4 planning artefacts surfaced
hard scope conflicts and several internal contradictions. Resolved
this round:

- **Swapped v0.4 ↔ v0.5 themes in `07-roadmap/00-version-roadmap.md`.**
  v0.4 is now **Capsule Bus Experimental** (was: Service Communication
  Metadata). v0.5 is now **Capsule Catalog** (absorbs the service-
  manifest / endpoint / capability metadata work and adds discovery-
  by-capability). §12 + §13 fully rewritten; §24 (documentation
  roadmap), §26 (decision checkpoints), §27.10 (guardrail), and §28
  (summary roadmap) rebalanced. `_zh` mirror banners added at §12 / §13.
- **Rewrote `10-implementation/v0.4-capsule-bus-implementation-plan.md`.**
  Added explicit v0.3 prerequisite checklist; aligned API paths with
  `/api/admin/bus/routes` + `/api/agents/:id/bus/events`; pinned
  field names (`sourceServiceCode`, `targetServiceCode` + `actionName`,
  `ACTION_EXECUTE`-only); removed `maxCommandsPerEvent` and explicit
  fan-out from v0.4 scope; concrete loop / storm safeguards
  (`max routing depth = 1` hard-enforced, default 60 events/min
  per-agent); pinned feature-flag env var; specified SDK back-compat
  with v0.3 CE; cut Phase 5 OpHub Go work to v0.5+; fixed broken
  References link.
- **Tightened `04-opstage/v0.4-capsule-bus-experimental.md`.** Audit
  events now have a pairing-rules table; non-goals explicit; canonical
  field names + URL paths; SDK back-compat note.
- **Expanded `changelog/v0.4.0.md`.** Added compatibility matrix,
  feature-flag config table, breaking-changes section, v0.3→v0.4
  migration steps, deferred-to-v0.5+ list, known limitations,
  audit-event reference.

## 2026-05-14 — CE v0.2 Public Preview cycle

- Added **ADR-0010** (`08-decisions/0010-ephemeral-action-secrets.md`, plus `_zh`): formalises the v0.2 ephemeral one-time-key cache strategy. Mirrors the public CE ADR `docs/adr/0001-ephemeral-action-secrets.md`.
- Added **v0.2 implementation progress log** (`10-implementation/18-v02-progress-log.md`, plus `_zh`): records what each of the four public repos shipped on its `v0.2` branch, plus deferred items. Subsequently extended with the rc.1 review-fix section and the demo-alignment entry.
- Updated `07-roadmap/01-ce-roadmap.md` § 18 (CE v0.2 Direction) to mark v0.2 deliverables against the original roadmap intent. `_zh` mirror updated. Subsequently updated again to flip "Docker Compose demo" from "deferred" to "partial" after `xtrape-capsule-demo` PR #14.
- Annotated **ADR-0007** (UI state + data fetching) with a `v0.2 conformance note` reflecting the `App.tsx` 1193 → 124 line split. `_zh` mirror updated.

## 2026-05-05

- Marked repository as private design documentation and implementation guidance.
- Added `.gitignore` and removed macOS `.DS_Store` metadata.
- Added status metadata to major Markdown documents.
- Marked Chinese translation files as draft / machine-assisted unless reviewed.
- Added AI reading guide for coding agents.
- Added public extraction guide for safe migration to `xtrape-capsule-site`.
- Added sensitive content checklist.
- Added repository map.
