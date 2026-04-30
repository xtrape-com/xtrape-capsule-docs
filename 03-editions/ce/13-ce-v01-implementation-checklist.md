# CE v0.1 Implementation Checklist

- Status: Implementation Target
- Edition: CE
- Priority: Current
- Audience: product designers, architects, backend developers, frontend developers, agent SDK developers, test engineers, AI coding agents

This checklist defines the minimum implementation acceptance criteria for Opstage CE v0.1.

## 0. Planning Contracts

- [ ] ADRs in `08-decisions/` are reviewed.
- [ ] Contracts in `09-contracts/` are reviewed.
- [ ] Implementation plans in `10-implementation/` are reviewed.
- [ ] Implementation follows `10-implementation/05-implementation-sequence.md`.

## 1. Product Flow

- [ ] User can start Opstage CE locally.
- [ ] User can start Opstage CE with Docker and a persistent data volume.
- [ ] User can initialize or log in as a local admin.
- [ ] User can create a registration token.
- [ ] Demo Node.js Capsule Service can register through the Node Agent SDK.
- [ ] UI shows registered Agent.
- [ ] UI shows reported Capsule Service.
- [ ] UI shows manifest, health, configs, and actions.
- [ ] User can trigger a predefined action.
- [ ] Agent can poll and execute the Command.
- [ ] Agent can report CommandResult.
- [ ] UI shows Command result.
- [ ] Audit log records key operations.

## 2. Backend

- [ ] Fastify API server exists.
- [ ] Zod validation exists for request bodies.
- [ ] Backend routes conform to `09-contracts/openapi/opstage-ce-v0.1.yaml`.
- [ ] Prisma schema and migrations exist.
- [ ] Prisma schema conforms to `09-contracts/prisma/schema.prisma`.
- [ ] SQLite database is initialized under the configured data directory.
- [ ] Default Workspace is bootstrapped.
- [ ] Local admin user bootstrap exists.
- [ ] Admin authentication is enabled by default.
- [ ] Registration tokens are stored as hashes.
- [ ] Agent tokens are stored as hashes.
- [ ] Agent API rejects disabled or revoked Agents.
- [ ] Backend calculates online, stale, offline, and unhealthy statuses.
- [ ] Backend writes AuditEvents for login, failed login, token creation/revocation, Agent registration, Command creation, and Command completion.

## 3. API

- [ ] OpenAPI contract exists and parses successfully.
- [ ] Admin API uses `/api/admin/*`.
- [ ] Agent API uses `/api/agents/*`.
- [ ] System API uses `/api/system/*`.
- [ ] Capsule Service resource path uses `capsule-services`.
- [ ] `/api/system/health` does not expose sensitive data.
- [ ] `/api/system/version` does not expose sensitive data.

## 4. Command and Action

- [ ] ActionDefinition supports `name`, `label`, `description`, `dangerLevel`, `confirmRequired`, `inputSchemaJson`, and `timeoutSeconds`.
- [ ] Command supports `PENDING`, `DISPATCHED`, `SUCCESS`, `FAILED`, and `EXPIRED` states. (`RUNNING` and `CANCELLED` are reserved for future use.)
- [ ] Backend validates action existence before Command creation.
- [ ] Backend validates Agent ownership before Command polling and result submission.
- [ ] Backend prevents terminal Command states from being overwritten incorrectly.
- [ ] No shell, exec, bash, or arbitrary script action is exposed as a normal CE feature.

## 5. UI

- [ ] Login page exists.
- [ ] Dashboard summary exists.
- [ ] Agent list and detail pages exist.
- [ ] Capsule Service list and detail pages exist.
- [ ] Service detail shows manifest, health, configs, actions, recent Commands, and recent AuditEvents.
- [ ] Command list and detail pages exist.
- [ ] AuditEvent list exists.
- [ ] Action execution UI shows danger level and confirmation when required.

## 6. Node Agent SDK

- [ ] SDK can register with registration token.
- [ ] SDK persists Agent token locally.
- [ ] SDK sends heartbeat.
- [ ] SDK reports service manifest.
- [ ] SDK reports health.
- [ ] SDK reports config metadata.
- [ ] SDK reports action metadata.
- [ ] SDK polls Commands.
- [ ] SDK dispatches Commands to local action handlers.
- [ ] SDK reports CommandResult.
- [ ] SDK uses retry/backoff for transient Backend failures.
- [ ] SDK logs do not leak tokens or secrets.

## 7. Security

- [ ] No default weak admin credential exists.
- [ ] Passwords are hashed with argon2 or bcrypt.
- [ ] Session secret is configurable.
- [ ] Registration token raw value is shown only once.
- [ ] Agent token raw value is shown only once to the Agent.
- [ ] Tokens are never logged.
- [ ] Sensitive config values are masked or represented as `secretRef`.
- [ ] UI is not usable without authentication by default.

## 8. Non-Goals Check

- [ ] No tenant system.
- [ ] No billing or subscription system.
- [ ] No enterprise RBAC.
- [ ] No SSO/OIDC/LDAP/SAML.
- [ ] No Redis or queue requirement.
- [ ] No Kubernetes requirement.
- [ ] No Agent Gateway.
- [ ] No Sidecar or External Agent implementation.
- [ ] No Java/Python/Go SDK implementation.
- [ ] No full observability platform.
- [ ] No secret vault.
- [ ] No remote shell.
- [ ] No arbitrary script execution.
