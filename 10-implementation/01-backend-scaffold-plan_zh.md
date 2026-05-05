---
status: draft
audience: ai-coding-agents
stability: unstable
last_reviewed: 2026-05-05
edition: ce
phase: current
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 01-backend-scaffold-plan.md
翻译状态 / Translation Status: 已翻译 / Translated
生成时间 / Generated: 2026-05-01 09:28:55
================================================================================
注意 / Notes:
- 技术术语如 Capsule Service、Agent、Opstage 等保留英文或采用中英对照
- 代码块中的内容不翻译
- 文件路径和 URL 不翻译
- 保持原有的 Markdown 格式结构
================================================================================
-->

# CE（社区版） v0.1 Backend Scaffold Plan

- Status: 实施指南
- Edition: CE（社区版）
- Priority: Current
- Audience: backend developers, architects, security reviewers, test engineers, AI coding agents

## 1. Goal

Build the Fastify Backend that implements the CE（社区版） v0.1 governance loop and conforms to:

```text
09-contracts/openapi/opstage-ce-v0.1.yaml
09-contracts/prisma/schema.prisma
```

## 2. Package

Recommended package:

```text
apps/opstage-backend
```

## 3. Stack

```text
Fastify         9.x
TypeScript      5.x
Zod             3.x
Prisma          7.x
SQLite          via better-sqlite3
pino            9.x   (see ADR 0006 for fields and redaction)
ajv             8.x   (JSON Schema for ActionDefinition input/output)
nanoid          5.x   (via packages/shared newId helper)
Vitest          2.x
```

## 4. Suggested Source Layout

```text
apps/opstage-backend/src/
├── main.ts
├── app.ts
├── config/
│   └── env.ts
├── plugins/
│   ├── prisma.ts
│   ├── auth-session.ts
│   ├── csrf.ts              # double-submit token enforcement (see ADR 0004)
│   ├── errors.ts            # maps thrown errors to ErrorEnvelope using 09-contracts/errors.md
│   ├── logger.ts            # pino + redaction + request context
│   └── audit.ts
├── modules/
│   ├── auth/
│   ├── dashboard/
│   ├── agents/
│   ├── registration-tokens/
│   ├── capsule-services/
│   ├── commands/
│   ├── audit-events/
│   ├── system/
│   └── sweeper/             # background jobs (agent-offline, service-stale, command-ttl)
├── security/
│   ├── password.ts
│   ├── tokens.ts
│   └── redaction.ts
└── tests/
```

## 4.1 ID Generation Helper

All entity IDs are produced by a single helper exported from `packages/shared`:

```ts
// packages/shared/src/ids.ts
import { customAlphabet } from "nanoid";

const ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-";
const NANO = customAlphabet(ALPHABET, 21);

export type IdPrefix =
  | "wks_" | "usr_" | "agt_" | "tok_" | "svc_"
  | "hlr_" | "cfg_" | "act_" | "cmd_" | "crs_" | "aud_";

export function newId<P extends IdPrefix>(prefix: P): `${P}${string}` {
  return `${prefix}${NANO()}` as `${P}${string}`;
}
```

Rules:

- `newId(prefix)` is the **only** allowed ID generator. Backend code MUST NOT call `nanoid()` or `crypto.randomUUID()` directly for entity IDs.
- The prefix list MUST match ADR 0004 §"ID Generation". Adding a new prefix requires an ADR update.
- Unit test (in `packages/shared`): assert that `newId("agt_").startsWith("agt_")` and length is `4 + 21`.

## 4.2 Token Generation Helper

A second helper in `packages/shared` produces token strings (used by `RegistrationToken` and `AgentToken`):

```ts
// packages/shared/src/tokens.ts
import { randomBytes, createHash } from "node:crypto";

export type TokenPrefix = "opstage_reg_" | "opstage_agent_";

export function newToken(prefix: TokenPrefix): { raw: string; hash: string } {
  const random = randomBytes(32).toString("base64url");
  const raw = `${prefix}${random}`;
  const hash = createHash("sha256").update(raw).digest("hex");
  return { raw, hash };
}
```

Backend stores only `hash` in the database; `raw` is returned to the caller exactly once.

## 4.3 List Query Helper

Pagination/sort/filter parsing is shared via `@xtrape/capsule-contracts-node` (the published npm package; see [ADR 0008](../08-decisions/0008-naming-and-repositories.md)):

```ts
// @xtrape/capsule-contracts-node/src/list-query.ts
import { z } from "zod";

export const ListQueryBase = z.object({
  page: z.coerce.number().int().min(1).default(1),
  pageSize: z.coerce.number().int().min(1).max(100).default(20),
  sort: z.string().optional(),
});

export function parseSort(value: string | undefined, allowed: readonly string[]) {
  if (!value) return [];
  return value.split(",").map((raw) => {
    const desc = raw.startsWith("-");
    const field = desc ? raw.slice(1) : raw;
    if (!allowed.includes(field)) {
      throw new HttpError(422, "VALIDATION_FAILED", `Unknown sort field: ${field}`);
    }
    return { field, direction: desc ? "desc" : "asc" } as const;
  });
}

export type Pagination = { page: number; pageSize: number; total: number };

export function paginate<T>(items: T[], page: number, pageSize: number, total: number) {
  return { data: items, pagination: { page, pageSize, total } };
}
```

Per-endpoint Zod schemas extend `ListQueryBase` with their allowed filters (e.g. `agentsListQuery = ListQueryBase.extend({ status: z.array(AgentStatus).optional() })`).

## 4.4 CSRF Plugin

`security/csrf.ts` enforces the double-submit token described in ADR 0004:

```ts
// pseudo-code
export const csrfPlugin = fp(async (app) => {
  app.addHook("preHandler", async (req) => {
    if (!req.url.startsWith("/api/admin/")) return;
    if (req.method === "GET" || req.method === "HEAD" || req.method === "OPTIONS") return;
    if (req.url === "/api/admin/auth/login") return;
    const headerToken = req.headers["x-csrf-token"];
    const session = req.session.get("admin");
    if (!session || !headerToken || headerToken !== session.csrfToken) {
      throw new HttpError(403, "CSRF_INVALID", "CSRF token missing or invalid.");
    }
  });
});
```

The CSRF token is generated with `crypto.randomBytes(32).toString("hex")`, stored in the session record, returned in the
JSON body of `/api/admin/auth/login`, `/api/admin/auth/me`, and `/api/admin/auth/csrf`. Rotated on
`/api/admin/auth/csrf` and on logout.

## 5. Backend Modules

### 5.1 Auth

Routes:

```text
POST /api/admin/auth/login
POST /api/admin/auth/logout
GET  /api/admin/auth/me
```

Responsibilities:

- local admin login;
- password hash verification;
- session creation;
- failed login audit;
- successful login audit;
- logout audit if practical.

### 5.2 Registration Tokens

Routes:

```text
POST /api/admin/registration-tokens
GET  /api/admin/registration-tokens
POST /api/admin/registration-tokens/{tokenId}/revoke
```

Rules:

- raw token shown once;
- hash only in DB;
- prefix `opstage_reg_`;
- revocable;
- optional expiry.

### 5.3 Agent（代理） API

Routes:

```text
POST /api/agents/register
POST /api/agents/{agentId}/heartbeat
POST /api/agents/{agentId}/services/report
GET  /api/agents/{agentId}/commands
POST /api/agents/{agentId}/commands/{commandId}/result
```

Rules:

- registration uses registration token;
- all later calls require Agent（代理） bearer token;
- path `agentId` must match authenticated Agent（代理）;
- disabled/revoked Agents are rejected;
- Agent（代理） token prefix `opstage_agent_`;
- raw Agent（代理） token returned only once.

### 5.4 Capsule Services

Routes:

```text
GET  /api/admin/capsule-services
GET  /api/admin/capsule-services/{serviceId}
GET  /api/admin/capsule-services/{serviceId}/manifest
GET  /api/admin/capsule-services/{serviceId}/health
GET  /api/admin/capsule-services/{serviceId}/configs
GET  /api/admin/capsule-services/{serviceId}/actions
POST /api/admin/capsule-services/{serviceId}/actions/{actionName}
```

Responsibilities:

- store and expose service manifest;
- store and expose config metadata;
- store and expose action definitions;
- create Commands for valid predefined actions;
- calculate effective status.

### 5.5 Commands

Routes:

```text
GET /api/admin/commands
GET /api/admin/commands/{commandId}
```

Agent（代理） routes handle polling and result reporting.

State machine:

```text
PENDING -> RUNNING -> SUCCEEDED
PENDING -> RUNNING -> FAILED
PENDING/RUNNING -> EXPIRED
```

`CANCELLED` is reserved.

### 5.6 Audit Events

Routes:

```text
GET /api/admin/audit-events
GET /api/admin/audit-events/{auditEventId}
```

Minimum audited operations:

- login success;
- login failure;
- registration token creation;
- registration token revocation;
- Agent（代理） registration;
- Agent（代理） disable/enable/revoke;
- Command creation;
- Command result.

### 5.7 System

Routes:

```text
GET /api/system/health
GET /api/system/version
```

Must not expose secrets, token hashes, raw environment, or database file path.

### 5.8 Sweeper

Module: `modules/sweeper`. See `04-opstage/02-opstage-backend.md` §27.1 for the full spec.

Jobs (CE（社区版） v0.1):

```text
agent-offline-sweep   — Agent.lastSeenAt < now − AGENT_OFFLINE_THRESHOLD_SECONDS
service-stale-sweep   — CapsuleService.lastReportedAt < now − HEALTH_STALE_THRESHOLD_SECONDS
command-ttl-sweep     — Command in PENDING/RUNNING with createdAt + ttlSeconds < now → EXPIRED
```

实现 rules:

- a single `setInterval` started in `main.ts` after the HTTP server is listening;
- batch size capped by `BACKGROUND_SWEEP_BATCH_SIZE` (default 500);
- every transition writes an AuditEvent with `actorType=SYSTEM`;
- expired Commands also produce a synthetic `CommandResult` with `success=false, error.code=COMMAND_EXPIRED`;
- shut down cleanly on `app.close()`.

## 6. Bootstrap

At startup:

1. load environment via Zod schema in `config/env.ts`; **fail fast** if any required variable is missing or empty
(`OPSTAGE_ADMIN_USERNAME`, `OPSTAGE_ADMIN_PASSWORD`, `OPSTAGE_SESSION_SECRET`);
2. ensure `OPSTAGE_SESSION_SECRET` is at least 32 characters;
3. initialize DB directory if needed;
4. run or require migrations according to deployment mode;
5. create default Workspace if missing;
6. if no admin user exists, create one from bootstrap variables;
7. if an admin user already exists, ignore bootstrap password (do not overwrite);
8. start API server.

No weak default credentials are allowed. Backend MUST exit with a non-zero status code (and a clear log line) if step 1 fails.

## 6.1 Error Envelope Plugin

The `plugins/errors.ts` plugin centralizes error → response mapping:

```ts
// pseudo-code
class HttpError extends Error {
  constructor(
    public readonly httpStatus: number,
    public readonly code: string,        // must be from 09-contracts/errors.md
    public readonly publicMessage: string,
    public readonly details?: unknown,
  ) { super(publicMessage); }
}

app.setErrorHandler((err, req, reply) => {
  if (err instanceof HttpError) {
    return reply.status(err.httpStatus).send({
      success: false,
      error: { code: err.code, message: err.publicMessage, details: err.details },
    });
  }
  if (err instanceof ZodError) {
    return reply.status(422).send({
      success: false,
      error: { code: "VALIDATION_FAILED", message: "Request failed validation.", details: err.flatten() },
    });
  }
  req.log.error(err);
  return reply.status(500).send({
    success: false,
    error: { code: "INTERNAL_ERROR", message: "Internal server error." },
  });
});
```

Backend code throws `HttpError` with codes from `09-contracts/errors.md`; the plugin handles the rest.

## 7. Test Plan

Minimum backend tests:

- admin login success/failure;
- registration token creation stores hash only;
- Agent（代理） registration returns raw Agent（代理） token once;
- revoked Agent（代理） cannot heartbeat;
- service report creates/updates CapsuleService;
- action request creates Command;
- Agent（代理） polling transitions Command to RUNNING;
- CommandResult transitions Command to SUCCEEDED/FAILED;
- audit events are written;
- system health does not leak sensitive data.
