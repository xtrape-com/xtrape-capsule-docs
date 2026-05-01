<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 0004-security-defaults.md
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

# ADR 0004: CE（社区版） v0.1 安全 Defaults

- Status: Accepted
- Edition: CE（社区版）
- Priority: Current
- Audience: architects, backend developers, frontend developers, agent SDK developers, security reviewers, AI coding agents

## Decision

CE（社区版） v0.1 security must protect the core governance loop without introducing enterprise security complexity.

## Admin 认证

Recommended default:

```text
username + password
HTTP-only session cookie
SameSite=Lax
```

Password hashing:

```text
argon2id preferred
bcrypt acceptable fallback
```

No default credential is allowed. There is no built-in `admin/admin` or `change-me` value. Backend MUST refuse to start when `OPSTAGE_ADMIN_PASSWORD` is missing or empty (see "Admin Bootstrap").

## Session Cookie Rules

The Backend session cookie has these properties:

```text
Name:        opstage_session
HttpOnly:    true
SameSite:    Lax
Secure:      true when X-Forwarded-Proto=https or NODE_ENV=production; false in local dev
Path:        /
Max-Age:     28800   (8 hours, must match Session TTL)
```

The cookie value is opaque to the client (signed/encrypted server-side; CE（社区版） v0.1 uses Fastify `@fastify/secure-session` or equivalent backed by `OPSTAGE_SESSION_SECRET`).

`SameSite=Lax` is sufficient for CE（社区版） v0.1 because:

- the Admin UI is served from the same origin as the Admin API (single-container deployment);
- there is no cross-origin GET that mutates state;
- all state-changing requests use POST/PUT/PATCH/DELETE.

CE（社区版） v0.1 does NOT issue CORS headers for cross-origin browsers. If a future deployment needs to host the UI on a different origin, the operator must front the deployment with a reverse proxy that re-attaches the cookie.

## CSRF Protection

CE（社区版） v0.1 uses a header-based double-submit token. The Backend keeps the canonical CSRF value bound to the session record server-side; the UI receives a copy in the JSON body and echoes it in a header on every state-changing call.

```text
1. The CSRF token is generated as crypto.randomBytes(32).toString("hex").
   Backend stores it on the session row:
     session.csrfToken = <value>
     session.csrfRotatedAt = now

2. The token is delivered to the UI in JSON, NOT as a cookie:
     POST /api/admin/auth/login    → 200 { data: { user, csrfToken, expiresAt } }
     GET  /api/admin/auth/me       → 200 { data: { user, csrfToken, expiresAt } }
     GET  /api/admin/auth/csrf     → 200 { data: { csrfToken } }   (rotates)

3. UI stores the token in memory (not localStorage, not a cookie) and sends
   it on every state-changing request as:
     X-CSRF-Token: <value>

4. Backend rejects state-changing requests where the header is missing or
   does not equal session.csrfToken with HTTP 403 and code CSRF_INVALID
   (see 09-contracts/errors.md). UI MUST then call /api/admin/auth/csrf to
   obtain a fresh token before retrying.

5. The token MUST be rotated on /api/admin/auth/csrf and on logout. Old
   values stop validating immediately.
```

The Agent（代理） API (`/api/agents/*`) does not use cookies and is not subject to CSRF — it is authenticated via `Authorization: Bearer <agentToken>` only.

The System API (`/api/system/*`) is read-only and unauthenticated; CSRF does not apply.

## 认证 Flow

End-to-end flow as the Backend MUST implement it:

```text
1. UI loads → calls GET /api/admin/auth/me
   - 200: session valid, render dashboard, store csrfToken in memory.
   - 401: redirect to /login.

2. UI POST /api/admin/auth/login { username, password }
   - 200: Set-Cookie: opstage_session=...; HttpOnly; Secure; SameSite=Lax; Max-Age=28800
          Body:       { data: { user, csrfToken, expiresAt } }
   - 401: AUTH_INVALID — bad username or password.
   - 422: VALIDATION_FAILED — body shape wrong.

3. UI calls protected endpoints with:
     Cookie:        opstage_session=...
     X-CSRF-Token:  <stored csrfToken>
   - 401: session expired → re-login.
   - 403 with code CSRF_INVALID: rotate token via /api/admin/auth/csrf
     and retry once.

4. UI POST /api/admin/auth/logout (with X-CSRF-Token)
   - 200: Set-Cookie: opstage_session=; Max-Age=0  (clears cookie).
          Backend invalidates session row server-side.
```

## Admin Bootstrap

CE（社区版） v0.1 should support environment-variable bootstrap:

```text
OPSTAGE_ADMIN_USERNAME
OPSTAGE_ADMIN_PASSWORD
OPSTAGE_SESSION_SECRET
```

Bootstrap behavior (CE（社区版） v0.1 decision):

```text
1. On startup, check if any admin user exists in the database.
2. If no admin user exists:
   a. If OPSTAGE_ADMIN_USERNAME and OPSTAGE_ADMIN_PASSWORD are set → create the admin user.
   b. If bootstrap variables are missing → log a clear error and exit with a non-zero code.
      Do NOT start the server without credentials.
3. If an admin user already exists:
   a. Ignore bootstrap variables (do not overwrite password automatically).
   b. To reset a password, use a future admin CLI command or direct database operation.
```

It must not silently create weak credentials. There is no first-run UI wizard in CE（社区版） v0.1.

Admin session:

```text
Session secret: OPSTAGE_SESSION_SECRET (required, minimum 32 characters)
Session TTL: 8 hours (non-configurable in CE v0.1)
Session store: in-process memory (SQLite-backed session store is EE+)
```

## Token Rules

Registration tokens and Agent（代理） tokens:

- are shown only once;
- are stored only as hashes;
- are never logged;
- are revocable;
- must have recognizable prefixes.

Required prefixes:

```text
opstage_reg_
opstage_agent_
```

Token generation format:

```text
<prefix> + base62(crypto.randomBytes(32))
```

Example: `opstage_agent_4xKj8mNpQ2rT...` (prefix + 43 base62 characters ≈ 256 bits of entropy)

Token hash algorithm:

```text
SHA-256 (hex digest)
```

Tokens are already high-entropy random values; bcrypt/argon2 are not required and would slow down every Agent（代理） API call. SHA-256 is sufficient and performant.

## ID Generation

All entity IDs use a prefixed random identifier:

```text
<prefix> + nanoid(21)
```

Required prefixes (must match `09-contracts/openapi/opstage-ce-v0.1.yaml`):

```text
wks_   — Workspace
usr_   — User
agt_   — Agent
tok_   — RegistrationToken            (also AgentToken row id)
svc_   — CapsuleService
hlr_   — HealthReport
cfg_   — ConfigItem
act_   — ActionDefinition
cmd_   — Command
crs_   — CommandResult
aud_   — AuditEvent
```

Example: `agt_V1StGXR8_Z5jdHi6B-myT`

Recommended helper: a single `newId(prefix)` utility in `packages/shared` should be the only ID generator. See `10-implementation/01-backend-scaffold-plan.md`.

## Agent（代理） 授权

After registration, all Agent（代理） API calls must validate:

- Agent（代理） token hash;
- Agent（代理） status;
- path `agentId` matches authenticated Agent（代理）;
- Agent（代理） owns or is assigned the referenced Command or Capsule Service（胶囊服务）.

Disabled or revoked Agents must not heartbeat, poll Commands, report services, or report CommandResults.

## Secret and Config Safety

CE（社区版） v0.1 should avoid raw secret storage. Config metadata should prefer:

```text
valuePreview
secretRef
sensitive
```

If `sensitive = true`, Backend and UI must not expose raw current values.

## Forbidden Capabilities

CE（社区版） v0.1 must not provide:

```text
remote shell
arbitrary script execution
generic exec API
browser-triggered raw command execution
```
