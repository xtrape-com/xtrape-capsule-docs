# CE v0.1 Development and Release Implementation

- Status: Implementation Record
- Edition: CE
- Priority: Current
- Audience: maintainers, release managers, AI coding agents

This document records the implementation-level repository, local development, verification, and release workflow after the CE v0.1 repository split.

## 1. Repository split

CE v0.1 is implemented as separate repositories:

| Repository | Package | Responsibility |
| --- | --- | --- |
| `xtrape-capsule-docs` | n/a | Product, architecture, contract, implementation documentation. |
| `xtrape-capsule-contracts-node` | `@xtrape/capsule-contracts-node` | OpenAPI/spec artifacts, Zod schemas, TypeScript types, shared error/enums/id helpers. |
| `xtrape-capsule-agent-node` | `@xtrape/capsule-agent-node` | Node embedded Agent SDK. Depends on contracts package. |
| `xtrape-capsule-ce` | private app repo | Opstage Backend, UI, demo service, CE-owned DB/shared/test utilities, Docker/deploy/release artifacts. |

The CE repo must not contain `packages/contracts` or `packages/agent-node`. It consumes the two packages through npm semver dependencies:

```text
@xtrape/capsule-contracts-node: ^0.1.0
@xtrape/capsule-agent-node:    ^0.1.0
```

## 2. Local development order

Recommended order when changing shared contracts:

1. Update `xtrape-capsule-contracts-node`.
2. Run its validation.
3. Update `xtrape-capsule-agent-node` to consume the new contract.
4. Run its validation.
5. Update `xtrape-capsule-ce` to consume the new package versions.
6. Run CE validation.
7. Publish packages, then refresh CE lockfile from registry.

Local symlinks may be used for manual validation, but `link:` / `file:` dependencies must not be committed in package manifests or lockfiles intended for CI/release.

## 3. Validation commands

Contracts package:

```bash
cd xtrape-capsule-contracts-node
pnpm install
pnpm typecheck
pnpm test
pnpm build
```

Agent package:

```bash
cd xtrape-capsule-agent-node
pnpm install
pnpm typecheck
pnpm test
pnpm build
```

CE repo:

```bash
cd xtrape-capsule-ce
pnpm install
pnpm contracts:check
pnpm db:validate
pnpm typecheck
pnpm test
pnpm smoke:demo
pnpm test:docker-smoke
pnpm repo:check
```

If native SQLite bindings were built under a different Node version, run:

```bash
pnpm rebuild better-sqlite3
```

## 4. CE boundary check

`pnpm contracts:check` in CE runs a boundary check that verifies:

- `packages/contracts` does not exist in CE.
- `packages/agent-node` does not exist in CE.
- Backend depends on `@xtrape/capsule-contracts-node` using npm semver.
- Demo service depends on `@xtrape/capsule-agent-node` using npm semver.

This prevents regression to an all-in-one monorepo layout.

## 5. Build outputs and ignored artifacts

Generated directories are not committed:

```text
node_modules/
dist/
data/
coverage/
*.tsbuildinfo
.env
```

CE Docker builds compile Backend/UI/packages in a multi-stage image and run the Backend as the single process serving API plus static UI.

## 6. Release order

For a clean CE v0.1 release:

1. Tag and publish `@xtrape/capsule-contracts-node@0.1.0`.
2. Tag and publish `@xtrape/capsule-agent-node@0.1.0`.
3. Refresh CE install/lockfile from npm registry.
4. Run full CE validation.
5. Tag `xtrape-capsule-ce` as `v0.1.0`.
6. Build/publish Docker image.
7. Publish GitHub release notes.

If a CE release draft exists before package publication, keep it as draft until registry and clean-install verification are complete.

## 7. Runtime configuration reference

Important CE environment variables:

| Variable | Default | Notes |
| --- | --- | --- |
| `OPSTAGE_HOST` | `0.0.0.0` | Backend bind host. |
| `OPSTAGE_PORT` | `8080` | Backend port. |
| `DATABASE_URL` | `file:./data/opstage.db` | SQLite database URL. |
| `OPSTAGE_ADMIN_USERNAME` | none | Required on first boot for bootstrap admin. |
| `OPSTAGE_ADMIN_PASSWORD` | none | Min 12 chars. |
| `OPSTAGE_SESSION_SECRET` | none | Min 32 chars; required. |
| `OPSTAGE_SESSION_TTL_SECONDS` | `86400` | Session max age. |
| `OPSTAGE_STATIC_DIR` | `apps/opstage-ui/dist` | Built UI directory. |
| `OPSTAGE_AGENT_STALE_SECONDS` | `120` | Agent freshness threshold. |
| `OPSTAGE_AUDIT_RETENTION_DAYS` | `90` | Audit retention. |
| `OPSTAGE_MAINTENANCE_INTERVAL_SECONDS` | `60` | Background maintenance interval; `0` disables timer. |
| `OPSTAGE_BACKUP_DIR` | `./data/backups` | SQLite backup output directory. |

Demo/Agent variables:

| Variable | Notes |
| --- | --- |
| `OPSTAGE_BACKEND_URL` | Backend base URL for Agent SDK. |
| `OPSTAGE_REGISTRATION_TOKEN` | Raw one-time registration token for first registration. |
| `CAPSULE_AGENT_TOKEN_FILE` | Local Agent token file path. |
| `DEMO_MESSAGE` | Demo service config preview value. |
