---
status: implemented
audience: maintainers
stability: stable
last_reviewed: 2026-05-14
---

# Design Changelog

## 2026-05-14 — CE v0.2 Public Preview cycle

- Added **ADR-0010** (`08-decisions/0010-ephemeral-action-secrets.md`, plus `_zh`): formalises the v0.2 ephemeral one-time-key cache strategy. Mirrors the public CE ADR `docs/adr/0001-ephemeral-action-secrets.md`.
- Added **v0.2 implementation progress log** (`10-implementation/18-v02-progress-log.md`, plus `_zh`): records what each of the four public repos shipped on its `v0.2` branch, plus deferred items.
- Updated `07-roadmap/01-ce-roadmap.md` § 18 (CE v0.2 Direction) to mark v0.2 deliverables against the original roadmap intent. `_zh` mirror updated.
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
