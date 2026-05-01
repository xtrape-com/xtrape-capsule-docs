<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 00-repository-structure.md
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

# CE（社区版） v0.1 Repository Structure

- Status: 实施指南
- Edition: CE（社区版）
- Priority: Current
- Audience: architects, backend developers, frontend developers, agent SDK developers, DevOps engineers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs disagree, the ADRs win for CE（社区版） v0.1. The authoritative naming and repository decisions live in [ADR 0008](../08-decisions/0008-naming-and-repositories.md) and [ADR 0009](../08-decisions/0009-contracts-spec-and-bindings.md).

## 1. 概述

Opstage（运维舞台） CE（社区版） v0.1 is delivered as **four repositories** under the `xtrape` GitHub organization. The split exists because two of the four are **edition-agnostic** (the wire contracts and the Node Agent（代理） SDK) and must not be tied to any specific edition's release cycle.

```text
xtrape-capsule-docs              ← design docs, ADRs, Layer 1 contract SSOT (you are here)
xtrape-capsule-contracts-node    ← Node-language bindings of the contracts (Layer 2)
xtrape-capsule-agent-node        ← Node Agent SDK
xtrape-capsule-ce                ← CE backend, UI, demo, deploy (the only edition-bound code repo)
```

Future Java/Python/Go agents follow the same shape: each gets its own `xtrape-capsule-contracts-<lang>` and `xtrape-capsule-agent-<lang>` repo. EE（企业版） / Cloud（云版） editions get their own `xtrape-capsule-opstage-<edition>` repos.

## 2. Dependency Graph

```text
xtrape-capsule-docs (Layer 1 SSOT — JSON / YAML)
        │
        │  (sync via per-repo upstream-bump workflow; NOT a runtime dep)
        ▼
xtrape-capsule-contracts-node ───► npm: @xtrape/capsule-contracts-node
        │                                  │
        │  npm                              │  npm
        ▼                                   ▼
xtrape-capsule-agent-node            xtrape-capsule-ce
        │                                   │
        └──────────► npm ───────────────────┤
              @xtrape/capsule-agent-node    │
                                            ▼
                              ghcr.io/xtrape/opstage-ce:vX.Y.Z
                              ghcr.io/xtrape/demo-capsule-service:vX.Y.Z
```

**Strict rule (enforced by CI in each repo)**: nothing depends on `xtrape-capsule-ce`. 版本-agnostic repos MUST NOT import from edition-bound repos. See ADR 0008 §"Reverse-dependency prohibition".

## 3. `xtrape-capsule-ce` — CE（社区版） Monorepo

This is the only repository where pnpm workspace is meaningful. It 包含 the CE（社区版） backend, UI, demo Capsule Service（胶囊服务）, deployment assets, and CE（社区版）-internal helper packages.

### 3.1 Layout

```text
xtrape-capsule-ce/
├── apps/
│   ├── opstage-backend/                @xtrape/opstage-backend         (private)
│   ├── opstage-ui/                     @xtrape/opstage-ui              (private; Vue 3)
│   └── demo-capsule-service/           @xtrape/demo-capsule-service    (private)
├── packages/
│   ├── db/                             @xtrape/capsule-db              (private)
│   ├── shared/                         @xtrape/capsule-shared          (private)
│   └── test-utils/                     @xtrape/capsule-test-utils      (private)
├── deploy/
│   ├── docker/
│   │   ├── opstage-ce.Dockerfile
│   │   └── demo-capsule-service.Dockerfile
│   └── compose/
│       └── docker-compose.yml
├── .changeset/                         (changesets manage CE-internal versions; nothing here is published)
├── .github/workflows/
│   ├── ci.yml
│   ├── security.yml
│   └── release.yml                     (publishes ghcr.io/xtrape/opstage-ce:vX.Y.Z + demo-capsule-service)
├── package.json
├── pnpm-workspace.yaml
├── tsconfig.base.json
├── eslint.config.js
├── prettier.config.js
└── README.md
```

There is **no** `packages/contracts/` and **no** `packages/agent-node/` in the CE（社区版） monorepo. Both come from npm:

```jsonc
// xtrape-capsule-ce/apps/opstage-backend/package.json
{
  "dependencies": {
    "@xtrape/capsule-contracts-node": "^0.1.0"
    // backend does NOT depend on @xtrape/capsule-agent-node
  }
}

// xtrape-capsule-ce/apps/opstage-ui/package.json
{
  "dependencies": {
    "@xtrape/capsule-contracts-node": "^0.1.0"
    // UI does NOT depend on @xtrape/capsule-agent-node
  }
}

// xtrape-capsule-ce/apps/demo-capsule-service/package.json
{
  "dependencies": {
    "@xtrape/capsule-contracts-node": "^0.1.0",
    "@xtrape/capsule-agent-node": "^0.1.0"
  }
}
```

### 3.2 Workspace Packages

#### `apps/opstage-backend`

Fastify API server implementing:

- Admin API;
- Agent（代理） API;
- System API;
- auth/session handling (cookie + CSRF; see ADR 0004);
- persistence through `@xtrape/capsule-db` (workspace);
- Zod validation via schemas from `@xtrape/capsule-contracts-node` (npm).

#### `apps/opstage-ui`

Vue 3 + Ant 设计 Vue UI per [ADR 0007](../08-decisions/0007-ui-state-and-data-fetching.md). See [`02-ui-scaffold-plan.md`](./02-ui-scaffold-plan.md) for full details.

#### `apps/demo-capsule-service`

Minimal Node.js service consuming `@xtrape/capsule-agent-node` from npm.

It must register with Opstage（运维舞台）, report manifest/health/config/actions, and expose demo actions:

```text
echo
runHealthCheck
```

Demo config:

```text
demo.message
```

#### `packages/db`

Prisma schema, client, migrations, and DB bootstrap logic. The schema is the **authoritative** copy of `xtrape-capsule-docs/09-contracts/prisma/schema.prisma`; CI MUST verify they remain identical.

Responsibilities:

- Prisma client export;
- default Workspace bootstrap;
- local admin bootstrap;
- migration scripts;
- DB-level ID generation helpers if any.

#### `packages/shared`

Small shared utilities (CE（社区版）-internal):

- `newId(prefix)` helper (uses `enums/id-prefixes.json` from contracts);
- `newToken(kind)` helper (uses `tokenPrefixes` from contracts);
- date/time helpers;
- redaction helpers;
- effective-status calculation helpers (CapsuleService.status derivation);
- safe JSON helpers.

This package MUST NOT contain large business modules; if a module is touched by both backend and UI, prefer putting it in `@xtrape/capsule-contracts-node` instead.

#### `packages/test-utils`

共享 integration test helpers used by `apps/opstage-backend` and `apps/demo-capsule-service`. NOT published; consumed via workspace protocol (`"@xtrape/capsule-test-utils": "workspace:*"`).

Module layout:

```text
packages/test-utils/src/
├── index.ts                  # re-exports
├── db/
│   ├── temp-database.ts      # createTempDatabase()    → returns prisma + cleanup
│   └── seed.ts               # seedWorkspaceAndAdmin(), seedRegistrationToken(), seedAgent()
├── server/
│   └── start-test-server.ts  # boots Fastify on a random port with overridden config
├── clients/
│   ├── admin-client.ts       # authenticated admin fetch wrapper (cookie + csrf)
│   └── agent-client.ts       # bearer-token agent fetch wrapper for /api/agents/*
├── time/
│   └── fake-clock.ts         # deterministic clock injectable into Backend
└── polling/
    └── wait-for.ts           # waitFor(predicate, { timeoutMs, intervalMs })
```

Public API (excerpt):

```ts
export interface TempDatabase {
  prisma: PrismaClient;
  databaseUrl: string;        // file:./<random>.sqlite
  reset(): Promise<void>;     // truncates all tables
  destroy(): Promise<void>;   // disconnect + delete file
}
export function createTempDatabase(): Promise<TempDatabase>;

export interface TestServer {
  url: string;                // http://127.0.0.1:<random>
  app: FastifyInstance;
  close(): Promise<void>;
}
export interface TestServerOptions {
  database: TempDatabase;
  clock?: FakeClock;
  envOverrides?: Partial<AppConfig>;
}
export function startTestServer(opts: TestServerOptions): Promise<TestServer>;

export interface AdminClient {
  login(username?: string, password?: string): Promise<void>;
  get<T>(path: string): Promise<T>;
  post<T>(path: string, body?: unknown): Promise<T>;
  csrfToken: string;
}
export function makeAdminClient(server: TestServer): AdminClient;

export interface AgentClient {
  agentId: string;
  agentToken: string;
  heartbeat(body?: unknown): Promise<void>;
  reportServices(services: ReportedService[]): Promise<void>;
  pollCommands(limit?: number): Promise<Command[]>;
  reportResult(commandId: string, result: ReportCommandResultRequest): Promise<void>;
}
export async function registerTestAgent(
  server: TestServer,
  registrationToken: string,
  spec: { code: string; mode: "embedded" },
): Promise<AgentClient>;

export interface FakeClock {
  now(): Date;
  set(date: Date): void;
  advance(ms: number): void;
}
export function createFakeClock(initial?: Date): FakeClock;

export function waitFor<T>(
  predicate: () => Promise<T | undefined>,
  opts?: { timeoutMs?: number; intervalMs?: number },
): Promise<T>;
```

Rules:

- the helpers MUST NOT reach into Backend internals beyond `startTestServer`'s public DI hooks;
- `createTempDatabase` MUST run Prisma migrations against the temp file and seed exactly one Workspace and one admin user (configurable);
- `FakeClock` MUST be the only time source the Backend sees in tests (Backend reads `app.clock` from DI), so sweepers and TTL behaviour are deterministic;
- `waitFor` defaults to `timeoutMs: 5000`, `intervalMs: 50`; tests SHOULD use it instead of `setTimeout`-based sleeps.

Example test using these helpers:

```ts
test("expired commands are swept", async () => {
  const db = await createTempDatabase();
  const clock = createFakeClock(new Date("2026-05-01T12:00:00Z"));
  const server = await startTestServer({ database: db, clock });
  try {
    const admin = await makeAdminClient(server);
    await admin.login();
    const reg = await admin.post("/api/admin/registration-tokens", { name: "t1" });
    const agent = await registerTestAgent(server, reg.data.rawToken, { code: "demo", mode: "embedded" });
    // ... create a command, advance the clock past TTL, run the sweeper, assert EXPIRED
    clock.advance(301_000);
    await waitFor(async () => /* ... */);
  } finally {
    await server.close();
    await db.destroy();
  }
});
```

### 3.3 Root Scripts

Recommended root scripts for the CE（社区版） monorepo:

```json
{
  "scripts": {
    "dev": "pnpm -r --parallel dev",
    "build": "pnpm -r build",
    "test": "pnpm -r test",
    "lint": "pnpm -r lint",
    "typecheck": "pnpm -r typecheck",
    "verify": "pnpm install --frozen-lockfile && pnpm -r lint && pnpm -r typecheck && pnpm -r test && pnpm -r build",
    "db:generate": "pnpm --filter @xtrape/capsule-db db:generate",
    "db:migrate": "pnpm --filter @xtrape/capsule-db db:migrate",
    "check:no-reverse-deps": "tsx scripts/check-no-reverse-deps.ts",
    "check:no-link-in-lockfile": "tsx scripts/check-no-link-in-lockfile.ts"
  }
}
```

The `check:*` scripts enforce ADR 0008 rules:

- `check:no-reverse-deps`: verifies `@xtrape/capsule-contracts-node` and `@xtrape/capsule-agent-node` come from the npm registry, not from a local `link:` or `file:` path.
- `check:no-link-in-lockfile`: greps `pnpm-lock.yaml` for forbidden `link:` references.

### 3.4 Environment Variables

Minimum CE（社区版） v0.1 environment variables:

```text
OPSTAGE_HOST=0.0.0.0
OPSTAGE_PORT=8080
OPSTAGE_DATA_DIR=/app/data
DATABASE_URL=file:/app/data/opstage.db
OPSTAGE_ADMIN_USERNAME=admin@example.local
OPSTAGE_ADMIN_PASSWORD=<required on first bootstrap>
OPSTAGE_SESSION_SECRET=<required>
OPSTAGE_PUBLIC_BASE_URL=http://localhost:8080
```

Demo service variables:

```text
OPSTAGE_BACKEND_URL=http://localhost:8080
OPSTAGE_REGISTRATION_TOKEN=opstage_reg_...
OPSTAGE_AGENT_TOKEN_FILE=./data/agent-token.json
```

## 4. `xtrape-capsule-contracts-node`

Per ADR 0009; layout summary:

```text
xtrape-capsule-contracts-node/
├── README.md
├── package.json                       (name: @xtrape/capsule-contracts-node)
├── tsconfig.json
├── tsup.config.ts                     (ESM + CJS + .d.ts)
├── spec/                              ← read-only mirror of xtrape-capsule-docs/09-contracts/
│   ├── .source                        (one line: xtrape-capsule-docs@<sha>)
│   ├── openapi/opstage-ce-v0.1.yaml
│   ├── errors.json
│   ├── enums/{status-enums,audit-actions,id-prefixes}.json
│   └── examples/
├── src/
│   ├── index.ts
│   ├── types.gen.ts                   (generated; openapi-typescript)
│   ├── errors.gen.ts                  (generated; from errors.json)
│   ├── enums.gen.ts                   (generated; from enums/*.json)
│   ├── audit.gen.ts                   (generated)
│   ├── id.ts                          (newId(prefix) using id-prefixes.json)
│   └── schemas.ts                     (hand-written Zod, mirrors OpenAPI components)
├── tests/
│   └── conformance.spec.ts            (parses every spec/examples/*.json)
├── tools/
│   ├── sync-spec.ts
│   └── codegen.ts
├── .github/workflows/
│   ├── ci.yml
│   ├── release.yml                    (changesets → npm publish --provenance)
│   └── upstream-bump.yml              (cron: nightly sync from xtrape-capsule-docs)
└── .changeset/
```

Published to npm as `@xtrape/capsule-contracts-node`.

## 5. `xtrape-capsule-agent-node`

```text
xtrape-capsule-agent-node/
├── README.md
├── package.json                       (name: @xtrape/capsule-agent-node)
├── tsconfig.json
├── tsup.config.ts
├── src/
│   ├── index.ts
│   ├── capsule-agent.ts
│   ├── transport.ts
│   ├── command-loop.ts
│   ├── health.ts
│   ├── manifest.ts
│   └── token-storage.ts
├── examples/
│   └── minimal/                       (~30 lines: how to use the SDK)
├── tests/
│   ├── unit/
│   └── conformance/                   (round-trip wire shapes via @xtrape/capsule-contracts-node)
├── .github/workflows/
│   ├── ci.yml
│   ├── release.yml                    (changesets → npm publish)
│   └── contract-bump.yml              (Renovate auto-PRs new contracts versions)
└── .changeset/
```

Published to npm as `@xtrape/capsule-agent-node`. Depends on `@xtrape/capsule-contracts-node` from npm; MUST NOT depend on any `@xtrape/opstage-*` package.

## 6. Local 开发 Across Repos

When iterating on contracts and agent simultaneously, developers MAY use pnpm overrides locally — but these MUST NOT be committed:

```jsonc
// xtrape-capsule-agent-node/package.json (LOCAL ONLY — git-ignore via package.local.json or strip before commit)
{
  "pnpm": {
    "overrides": {
      "@xtrape/capsule-contracts-node": "link:../xtrape-capsule-contracts-node"
    }
  }
}
```

CI in each repo runs `check:no-link-in-lockfile` to enforce this.

For multi-repo cloning, recommend a top-level workspace folder:

```text
~/code/xtrape/
├── xtrape-capsule-docs/
├── xtrape-capsule-contracts-node/
├── xtrape-capsule-agent-node/
└── xtrape-capsule-ce/
```

## 7. Container Images

Per ADR 0008:

```text
ghcr.io/xtrape/opstage-ce:vX.Y.Z              (backend + bundled UI; single deploy unit)
ghcr.io/xtrape/opstage-ce:latest
ghcr.io/xtrape/demo-capsule-service:vX.Y.Z
ghcr.io/xtrape/demo-capsule-service:latest
```

Both built multi-arch (`linux/amd64` + `linux/arm64`) with SBOM and SLSA provenance attached.

## 8. Packaging Target

CE（社区版） v0.1 should support:

```text
single Opstage container
    ├── Backend API
    ├── built UI static assets (served by backend on the same port)
    └── SQLite data volume

second container (optional, for demo)
    └── demo Capsule Service connecting back over network
```

`docker compose` brings both up together. See [`07-quickstart.md`](./07-quickstart.md) for the user-facing experience.

## 9. Acceptance Criteria

- The four repositories exist on GitHub under the `xtrape` org with names matching ADR 0008.
- `xtrape-capsule-ce/pnpm-lock.yaml` resolves `@xtrape/capsule-contracts-node` and `@xtrape/capsule-agent-node` from the npm registry (no `link:` paths).
- `pnpm verify` from the CE（社区版） repo root runs `lint + typecheck + test + build` for all CE（社区版） workspace packages, green.
- `xtrape-capsule-contracts-node` and `xtrape-capsule-agent-node` each ship a `0.1.0` to npm with provenance.
- `ghcr.io/xtrape/opstage-ce:v0.1.0` exists and is multi-arch.
