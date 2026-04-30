# ADR 0004: CE v0.1 Security Defaults

- Status: Accepted
- Edition: CE
- Priority: Current
- Audience: architects, backend developers, frontend developers, agent SDK developers, security reviewers, AI coding agents

## Decision

CE v0.1 security must protect the core governance loop without introducing enterprise security complexity.

## Admin Authentication

Recommended default:

```text
username + password
HTTP-only session cookie
SameSite=Lax
```

Password hashing:

```text
argon2 preferred
bcrypt acceptable fallback
```

No default `admin/admin` credential is allowed.

## Admin Bootstrap

CE v0.1 should support environment-variable bootstrap:

```text
OPSTAGE_ADMIN_USERNAME
OPSTAGE_ADMIN_PASSWORD
OPSTAGE_SESSION_SECRET
```

Bootstrap behavior (CE v0.1 decision):

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

It must not silently create weak credentials. There is no first-run UI wizard in CE v0.1.

Admin session:

```text
Session secret: OPSTAGE_SESSION_SECRET (required, minimum 32 characters)
Session TTL: 8 hours (non-configurable in CE v0.1)
Session store: in-process memory (SQLite-backed session store is EE+)
```

## Token Rules

Registration tokens and Agent tokens:

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

Tokens are already high-entropy random values; bcrypt/argon2 are not required and would slow down every Agent API call. SHA-256 is sufficient and performant.

## ID Generation

All entity IDs use a prefixed random identifier:

```text
<prefix> + nanoid(21)
```

Required prefixes:

```text
agt_   — Agent
svc_   — CapsuleService
cmd_   — Command
evt_   — AuditEvent
reg_   — RegistrationToken
wks_   — Workspace
usr_   — User
```

Example: `agt_V1StGXR8_Z5jdHi6B-myT`

## Agent Authorization

After registration, all Agent API calls must validate:

- Agent token hash;
- Agent status;
- path `agentId` matches authenticated Agent;
- Agent owns or is assigned the referenced Command or Capsule Service.

Disabled or revoked Agents must not heartbeat, poll Commands, report services, or report CommandResults.

## Secret and Config Safety

CE v0.1 should avoid raw secret storage. Config metadata should prefer:

```text
valuePreview
secretRef
sensitive
```

If `sensitive = true`, Backend and UI must not expose raw current values.

## Forbidden Capabilities

CE v0.1 must not provide:

```text
remote shell
arbitrary script execution
generic exec API
browser-triggered raw command execution
```
