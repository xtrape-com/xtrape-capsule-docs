---
status: accepted
audience: ai-coding-agents
stability: stable
last_reviewed: 2026-05-14
---

# ADR 0010: Ephemeral Action Secrets (One-Time Generated Keys)

## Status

Accepted (CE v0.2)

## Date

2026-05-14

## Context

Several Capsule action handlers mint fresh secrets — registration tokens, rotated API keys, one-time passwords, ephemeral session credentials — and the operator needs to read the secret exactly once.

The naive option (persist the secret in `command_results.body`, then redact on read) leaks two ways:

1. Anyone with database access can recover the plaintext from a backup file.
2. The audit subsystem already writes `command_results` rows, so the plaintext lands in disk-resident artifacts intended to live for the audit retention window.

The opposite extreme (never persist the secret, only return it on the synchronous response of the originating POST) breaks the long-poll / asynchronous command model — the Opstage UI fetches command status separately from the dispatch call, and a refresh of the modal would silently lose the value.

The 0.1 implementation chose to store the secret plaintext in `command_results.body.data.generatedKey` and rely on the redactor to mask it on subsequent reads. This fails objective 1 above.

## Decision

CE v0.2 introduces an **in-process ephemeral cache** for action-generated secrets, separate from `command_results`:

- A key in the cache is `commandId`. The value is the plaintext `generatedKey` plus metadata (`createdAt`, `ttlMs`, `consumerHint`).
- TTL is 5 minutes by default; the cache evicts on TTL expiry and on process restart.
- The cache is **process-local** — there is no replication and no on-disk backing. CE v0.x is single-node by design (see ADR-0004 security defaults), so this is sound.
- On the first call to `GET /api/admin/commands/:id` from an authenticated owner, the API returns the cached `generatedKey` plaintext in `result.data.generatedKey`. The implementation removes that entry from the cache on the same read.
- On subsequent calls, `result.data.generatedKey` returns the literal string `"[REDACTED]"`.
- The audit `command.result.recorded` event for a command carrying a generated key uses the value-based `redactAuditMetadata` redactor; it never writes the plaintext to `audit_events.metadata`.
- `command_results.body` carries `"generatedKey": "[REDACTED]"` from the moment the agent's result is received; the plaintext never touches the row.

The UI side (Opstage console action modal) shows the value once in a yellow alert with a copy button. If the operator dismisses the modal without copying, the value is unrecoverable.

## Consequences

**Positive:**

- Database backups never contain the plaintext.
- Single-process compromise window for the plaintext is bounded to the TTL.
- The behaviour is straightforward to reason about for the operator.

**Negative:**

- The operator has one chance to copy the secret. Action handlers SHOULD make this clear in their `description` field.
- If the originating CE process restarts within the TTL, the cached entry is lost and the action must be re-run.
- A second authenticated reader of the same command between dispatch and modal display will consume the secret on behalf of the original requester.

## Alternatives Considered

1. **Encrypt-at-rest in `command_results`** — requires KMS or env-resident key, expands scope beyond v0.x security defaults (ADR-0004), and still produces a long-lived ciphertext that an attacker can grind on offline. Rejected.
2. **Return on synchronous POST only** — breaks the established long-poll command model; would require the UI to special-case "generatedKey" actions. Rejected.
3. **Persist with explicit expiry** — middle ground; rejected because it concentrates the same on-disk plaintext risk with extra plumbing, for marginal benefit over the in-process cache.

## Implementation Notes

- Backend module: `apps/opstage-backend/src/lib/ephemeral-command-secrets.ts` (CE repo).
- Wire surface: result transformer in `serializeCommand`.
- Audit safety: `redactAuditMetadata` (value-based) in `apps/opstage-backend/src/lib/redactor.ts`.
- Site-level operator note: `docs/opstage-ce/admin-ui.md` § Actions and Commands.
- A mirror of this ADR lives under the CE repo at `docs/adr/0001-ephemeral-action-secrets.md` so external readers can find it without access to the private design corpus.

## Supersedes / Superseded By

Supersedes the implicit v0.1 behaviour (plaintext-in-row + key-based redactor) for any action that emits `generatedKey`.
