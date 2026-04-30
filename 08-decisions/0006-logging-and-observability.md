# ADR 0006: CE v0.1 Logging and Observability

- Status: Accepted
- Edition: CE
- Priority: Current
- Audience: backend developers, agent SDK developers, frontend developers, DevOps engineers, security reviewers, AI coding agents

## Decision

CE v0.1 emits structured JSON logs from every process (Backend, UI server in production, Agent SDK). Operators consume them via stdout/stderr; no log shipper is bundled. EE adds OpenTelemetry; this ADR scopes only what CE v0.1 MUST do.

## Logger

```text
Library:    pino (v9+)
Format:     JSON (one object per line)
Stream:     stdout for level <= info, stderr for level >= warn
Pretty:     pino-pretty in development only (NODE_ENV !== "production")
```

The Backend instantiates one logger in `plugins/logger.ts` and re-uses it everywhere. Every other module obtains the logger from Fastify's `req.log` or via DI; modules MUST NOT call `console.log` / `console.error` (lint rule should enforce this).

## Log Levels

```text
trace   - very verbose; off by default.
debug   - developer-only diagnostic; enable per-process via OPSTAGE_LOG_LEVEL.
info    - lifecycle events: server start, listening port, sweeper tick, command transitions.
warn    - degraded but recoverable: sweeper fell behind, Agent rejected, retry exhausted.
error   - unexpected exceptions, failed transactions, panic-level issues.
fatal   - process about to exit. Used by bootstrap when env validation fails.
```

Default level: `info`. Override via `OPSTAGE_LOG_LEVEL` env var. Tests SHOULD pin to `silent`.

## Required Fields

Every record MUST contain:

```text
level         pino numeric level
time          epoch milliseconds
pid           process id
hostname      from os.hostname()
service       "opstage-backend" | "opstage-ui" | "opstage-agent"
env           value of NODE_ENV
version       package.json version of the emitting service
```

Request-scoped log records MUST additionally contain:

```text
requestId     UUIDv4 generated per HTTP request (Fastify genReqId)
method        HTTP method
url           HTTP path (NEVER the raw query string with secrets — see Redaction)
statusCode    populated on response logs
durationMs    populated on response logs
```

When the authenticated principal is known, the record MUST also include:

```text
actorType     ADMIN_USER | AGENT | SYSTEM
actorId       usr_... | agt_... | "system"
workspaceId   wks_...
```

Domain-specific fields (e.g. `commandId`, `serviceId`, `agentId`) SHOULD be added via `req.log.child({ commandId })` so they propagate through the rest of the request.

## Redaction Rules

The pino logger MUST be constructed with redaction paths. Any field listed below is replaced with `"[REDACTED]"` BEFORE serialization. The Backend MUST also strip these fields from `details` before they reach `ErrorEnvelope`.

```text
*.password
*.passwordHash
*.passwordHashed
*.secret
*.sessionSecret
*.csrfToken
*.token
*.rawToken
*.tokenHash
*.authorization
req.headers.authorization
req.headers.cookie
req.body.password
req.body.password_confirmation
req.body.token
req.body.refreshToken
res.headers["set-cookie"]
config.OPSTAGE_ADMIN_PASSWORD
config.OPSTAGE_SESSION_SECRET
config.DATABASE_URL                   # may contain credentials
```

Logs MUST NOT contain:

- raw registration tokens or Agent tokens (only their `tok_...` row id);
- raw passwords (even hashed values: log only "password verified" or "password mismatch");
- full request bodies for `/api/admin/auth/login` (log only `{ username }`);
- `Set-Cookie` header values;
- file system paths to the SQLite database when `NODE_ENV=production`.

A unit test in `apps/opstage-backend` MUST assert that logging an object containing every redacted key emits `[REDACTED]` for each.

## Required Audit-Adjacent Logs

Some events MUST appear both in the database (`AuditEvent`) and in the structured log:

```text
auth login success/failure        info  / warn
session expired                   info
agent register success/failure    info  / warn
agent disable / enable / revoke   info
registration token revoked        info
command create                    info
command transition                info  (PENDING→RUNNING, RUNNING→SUCCEEDED, ...)
command expired by sweeper        warn
command result reported           info  (level downgrades to warn on failure)
sweeper tick (per job)            debug (info only on first tick after boot)
```

The matching `auditEventId` SHOULD be included as a log field so an operator can grep across the persistent audit trail.

## Request / Response Logging

Backend logs one record on response (Fastify default with custom serializer):

```json
{
  "level": 30, "time": 1746000000000, "service": "opstage-backend",
  "requestId": "8d6f2c4a-…", "method": "POST",
  "url": "/api/admin/capsule-services/svc_…/actions/restart",
  "statusCode": 200, "durationMs": 27,
  "actorType": "ADMIN_USER", "actorId": "usr_…",
  "workspaceId": "wks_…", "commandId": "cmd_…"
}
```

Backend MUST NOT log full request bodies by default. Per-route opt-in is allowed via `req.log.debug({ body }, "...")` but Production builds MUST keep this disabled.

## Agent SDK Logging

Agent SDK uses pino too with these defaults:

```text
service       "opstage-agent"
agentId       agt_... when known (set after first registration)
serviceId     svc_... when reporting a service
```

Agents MUST NOT log:

- raw Agent token (only that one is "present"/"absent");
- decrypted Capsule Service config values;
- arbitrary `payload` content of high-`dangerLevel` Commands beyond the `actionName` and `commandId`.

## UI Logging

The UI SPA logs to the browser console only at `warn` and `error`. The UI server (Vite preview / Caddy / nginx in CE) emits standard access logs already; CE adds nothing.

## File / Rotation Strategy

CE v0.1 writes to stdout and relies on Docker / systemd for rotation. There is no `OPSTAGE_LOG_FILE` config in CE v0.1.

## Future Extensions (NOT in CE v0.1)

- OpenTelemetry traces and metrics (EE).
- Sentry / GlitchTip integration (EE).
- Per-tenant log streaming (Cloud).
- Audit log signing / tamper-evidence (EE).

## Acceptance Criteria

- `apps/opstage-backend` boots, logs JSON on stdout, and includes `requestId` + `actorType` (when authenticated) on every request line.
- `pino-pretty` is wired only in development.
- Redaction unit test passes.
- Docker logs (`docker logs <container>`) on the published image are JSON.
- No raw token, password, or `Set-Cookie` value appears in any log line at any level.
