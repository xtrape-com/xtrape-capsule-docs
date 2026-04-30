# CE v0.1 Monorepo Structure

- Status: Implementation Guidance
- Edition: CE
- Priority: Current
- Audience: architects, backend developers, frontend developers, agent SDK developers, DevOps engineers, AI coding agents

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

Integration test helpers for:

- temporary SQLite DB;
- Backend test server;
- authenticated admin client;
- fake Agent client;
- polling helpers.

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
