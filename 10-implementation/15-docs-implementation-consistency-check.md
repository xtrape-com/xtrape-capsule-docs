---
status: implemented
audience: ai-coding-agents
stability: evolving
last_reviewed: 2026-05-05
edition: ce
phase: current
---

# Docs / Implementation Consistency Check

- Status: Implementation Guidance
- Edition: CE
- Priority: Current
- Audience: maintainers, reviewers, AI coding agents

Use this checklist whenever Opstage CE command, action, Agent, config, or UI behavior changes.

---

## 1. Source of Truth Order

When documents conflict, use this order:

```text
1. ADRs in 08-decisions/
2. Contracts and specs in 02-specs/ and 09-contracts/
3. Implementation guides in 10-implementation/
4. Opstage and Agent guides in 04-opstage/ and 05-agents/
5. README / quickstart / examples
```

Do not silently change implementation against ADRs or contracts. Update the accepted design or create a new decision record first.

---

## 2. Recent CE Behavior to Keep Consistent

The following implemented behaviors must stay documented:

| Area | Implemented behavior | Primary docs |
|---|---|---|
| Action Catalog | Service report carries stable action button metadata only. | `02-specs/05-action-spec*`, `10-implementation/13-service-action-design-guide*` |
| Prepare | Opening action panel creates `ACTION_PREPARE` via GET. | `02-specs/05-action-spec*`, `02-specs/07-command-spec*` |
| Execute | Running action creates `ACTION_EXECUTE` via POST. | `02-specs/05-action-spec*`, `04-opstage/04-command-and-action-model*` |
| Prepare diagnostics | Prepare failure/timeout returns non-sensitive `error.details`. | `02-specs/05-action-spec*` |
| Result list | `data.list` may render as table with columns, formats, rowActions, emptyText, pageSize. | `02-specs/05-action-spec*`, `10-implementation/13-service-action-design-guide*` |
| Row action refresh | UI may refresh current list after row action completes. | `02-specs/05-action-spec*` |
| Command polling limit | Agent polls with optional `limit`, backend clamps to safe range. | `02-specs/07-command-spec*` |
| Agent execution locks | Agent may apply stricter internal per-resource locks. | `02-specs/07-command-spec*` |
| Service health report | Full service report at startup/catalog changes; heartbeat may carry service health. | `02-specs/03-agent-registration-spec*`, `02-specs/04-health-spec*` |
| Secrets | Secrets are redacted; one-time generated secrets must be explicitly designed. | `02-specs/06-config-spec*`, `08-decisions/0004-security-defaults*` |

---

## 3. Review Checklist

For every related implementation change:

- [ ] Backend tests cover the new behavior or failure mode.
- [ ] UI tests/typecheck cover changed rendering or helper logic.
- [ ] English and Chinese docs are both updated.
- [ ] Action spec examples still match implementation.
- [ ] Command spec lifecycle still matches implementation.
- [ ] Ops manual explains operator-facing behavior.
- [ ] Smoke test runbook still works.
- [ ] `pnpm contracts:check` passes after any OpenAPI/error-code change.
- [ ] Sensitive data and error details remain redacted.
- [ ] Default values in docs match default values in code.
- [ ] Any new environment variable is documented.

---

## 4. Quick Commands

From `xtrape-capsule-ce`:

```bash
pnpm --filter @xtrape/opstage-backend typecheck
pnpm --filter @xtrape/opstage-backend test
pnpm --filter @xtrape/opstage-ui typecheck
pnpm --filter @xtrape/opstage-ui test
pnpm smoke:ui
pnpm contracts:check
```

From `xtrape-capsule-docs`:

```bash
git diff -- 02-specs 04-opstage 05-agents 10-implementation
```

Manually check that both English and `_zh` files changed when the change affects shared behavior.
