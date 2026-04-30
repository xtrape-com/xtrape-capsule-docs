# CE v0.1 Monorepo Structure

- Status: Implementation Guidance
- Edition: CE
- Priority: Current
- Audience: architects, backend developers, frontend developers, agent SDK developers, DevOps engineers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs disagree, the ADRs win for CE v0.1.

## 1. Goal

Define the initial pnpm workspace layout for Opstage CE v0.1.

The repository should support:

- Fastify Backend;
- React UI;
- Node Agent SDK;
- shared TypeScript contracts and validation;
- demo Capsule Service;
- Docker packaging;
- contract-driven development from `09-contracts/`.

## 2. Recommended Layout

```text
xtrape-capsule/
├── apps/
│   ├── opstage-backend/
│   ├── opstage-ui/
│   └── demo-capsule-service/
├── packages/
│   ├── contracts/
│   ├── db/
│   ├── agent-node/
│   ├── shared/
│   └── test-utils/
├── docs/
│   └── xtrape-capsule-docs/ or imported docs
├── deploy/
│   ├── docker/
│   └── compose/
├── scripts/
├── package.json
├── pnpm-workspace.yaml
├── tsconfig.base.json
├── eslint.config.js
├── prettier.config.js
└── README.md
```

If docs remain in a separate repository, implementation should still mirror the same package layout.

## 3. Workspace Packages

### 3.1 `apps/opstage-backend`

Fastify API server implementing:

- Admin API;
- Agent API;
- System API;
- auth/session handling;
- persistence through `packages/db`;
- Zod validation from `packages/contracts`.

### 3.2 `apps/opstage-ui`

React + TypeScript + Ant Design UI implementing:

- login;
- dashboard;
- Agents;
- Capsule Services;
- Commands;
- AuditEvents;
- registration token creation;
- settings/system pages.

### 3.3 `apps/demo-capsule-service`

Minimal Node.js service using `packages/agent-node`.

It should register with Opstage, report manifest/health/config/actions, and expose demo actions:

```text
echo
runHealthCheck
```

### 3.4 `packages/contracts`

Shared TypeScript contracts generated or derived from:

```text
09-contracts/openapi/opstage-ce-v0.1.yaml
```

Also contains Zod schemas for request validation.

### 3.5 `packages/db`

Prisma schema, client, migrations, and DB bootstrap logic derived from:

```text
09-contracts/prisma/schema.prisma
```

Responsibilities:

- Prisma client export;
- default Workspace bootstrap;
- local admin bootstrap;
- migration scripts;
- ID generation helpers if DB-specific.

### 3.6 `packages/agent-node`

The published Node Embedded Agent SDK package.

Recommended package name:

```text
@xtrape/capsule-agent-node
```

### 3.7 `packages/shared`

Small shared utilities:

- ID generation;
- date/time helpers;
- redaction helpers;
- status calculation helpers;
- safe JSON helpers.

Avoid putting large business modules here.

### 3.8 `packages/test-utils`

Shared integration test helpers used by `apps/opstage-backend`, `packages/agent-node`, and `apps/demo-capsule-service`. NOT published; consumed via workspace protocol (`"@xtrape/test-utils": "workspace:*"`).

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
  // ...patch/put/delete
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

- the helpers MUST NOT reach into Backend internals beyond `createTestServer`'s public DI hooks;
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

## 4. Root Scripts

Recommended root scripts:

```json
{
  "scripts": {
    "dev": "pnpm -r --parallel dev",
    "build": "pnpm -r build",
    "test": "pnpm -r test",
    "lint": "pnpm -r lint",
    "typecheck": "pnpm -r typecheck",
    "db:generate": "pnpm --filter @xtrape/capsule-db db:generate",
    "db:migrate": "pnpm --filter @xtrape/capsule-db db:migrate",
    "contracts:check": "pnpm --filter @xtrape/capsule-contracts check"
  }
}
```

## 5. Environment Variables

Minimum CE v0.1 environment variables:

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

## 6. Packaging Target

CE v0.1 should support:

```text
single Opstage container
    ├── Backend API
    ├── built UI static assets
    └── SQLite data volume
```

The demo service may run as a second container in Docker Compose.
