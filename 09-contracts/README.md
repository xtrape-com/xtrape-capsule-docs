# CE v0.1 Implementation Contracts

- Status: Implementation Target
- Edition: CE
- Priority: Current
- Audience: architects, backend developers, frontend developers, agent SDK developers, test engineers, AI coding agents

This directory contains implementation contracts for **Opstage CE v0.1**.

These files translate the product and architecture decisions into concrete API and persistence contracts.

## 1. Contract Files

```text
09-contracts/openapi/opstage-ce-v0.1.yaml
09-contracts/openapi/redocly.yaml         # lint config (zero-warning when applied)
09-contracts/prisma/schema.prisma
09-contracts/prisma/prisma.config.ts
09-contracts/errors.md
```

## 2. Contract Priority

When implementing CE v0.1, use this priority:

```text
1. Accepted ADRs in 08-decisions/
2. Contracts in 09-contracts/
3. CE implementation target documents
4. Shared specifications used by CE
5. Planning documents only as future context
```

## 3. API Contract

The OpenAPI contract defines:

- Admin API under `/api/admin/*`;
- Agent API under `/api/agents/*`;
- System API under `/api/system/*`;
- request and response shapes for the CE governance loop;
- canonical naming for Capsule Service, Command, CommandResult, and AuditEvent resources.

## 4. Persistence Contract

The Prisma schema defines the CE v0.1 baseline persistence model:

- local admin users;
- default Workspace;
- registration tokens;
- Agents and Agent tokens;
- Capsule Services;
- health reports;
- config metadata;
- action definitions;
- Commands and CommandResults;
- AuditEvents;
- SystemSettings.

## 5. Implementation Rule

The contracts are allowed to be stricter than older prose documents. If older prose still shows paths such as `/api/auth/login` or `/api/admin/services`, the contract wins for CE v0.1.

## 6. Field Naming Mapping (Prisma ↔ OpenAPI)

A few persistence column names differ from their API surface names. Backend serializers must translate between them.

| Persistence column (Prisma)   | API field (OpenAPI)            | Notes                                                                  |
|-------------------------------|--------------------------------|------------------------------------------------------------------------|
| `ConfigItem.configKey`        | `ConfigItem.key`               | `key` is reserved in some SQL dialects; column is `configKey`.         |
| `Command.payloadJson`         | `Command.payload`              | TEXT (JSON) on disk, parsed object on the wire.                        |
| `CommandResult.dataJson`      | `CommandResult.data`           | Stored as TEXT, exposed as object.                                     |
| `CommandResult.errorJson`     | `CommandResult.error`          | Stored as TEXT, exposed as object.                                     |
| `CapsuleService.manifestJson` | `CapsuleService.manifest`      | Stored as TEXT, exposed as object.                                     |
| `CapsuleService.metadataJson` | `CapsuleService.metadata`      | Stored as TEXT, exposed as object.                                     |
| `AuditEvent.metadataJson`     | `AuditEvent.metadata`          | Stored as TEXT, exposed as object.                                     |
| `HealthReport.detailsJson`    | `HealthReport.details`         | Stored as TEXT, exposed as object.                                     |
| `HealthReport.dependenciesJson`| `HealthReport.dependencies`   | Stored as TEXT, exposed as array.                                      |
| `ActionDefinition.inputSchemaJson`  | `ActionDefinition.inputSchema`  | JSON Schema draft-2020-12.                                |
| `ActionDefinition.outputSchemaJson` | `ActionDefinition.outputSchema` | JSON Schema draft-2020-12.                                |

`AuditEvent` uses `targetType` / `targetId` on both wire and disk (older drafts called these `resourceType` / `resourceId` — those names are obsolete).

## 7. Validation

Recommended checks:

```bash
# YAML well-formedness (no npm install required, only ruby is needed)
ruby -e "require 'yaml'; YAML.load_file('xtrape-capsule-docs/09-contracts/openapi/opstage-ce-v0.1.yaml')"

# Or with Node.js (after `pnpm add -D js-yaml` somewhere in the workspace)
node -e "require('js-yaml').load(require('fs').readFileSync('xtrape-capsule-docs/09-contracts/openapi/opstage-ce-v0.1.yaml','utf8'))"

# Stricter OpenAPI 3.1 lint (Redocly publishes multiple bins, so use --package)
# A repo-local redocly config disables three benign rules — see below.
pnpm --package=@redocly/cli dlx redocly lint \
  xtrape-capsule-docs/09-contracts/openapi/opstage-ce-v0.1.yaml \
  --config xtrape-capsule-docs/09-contracts/openapi/redocly.yaml

# Prisma schema validation
pnpm dlx prisma@latest validate --schema xtrape-capsule-docs/09-contracts/prisma/schema.prisma
```

Expected lint output:

- With the repo-local `redocly.yaml`, the lint output is **valid with zero warnings**.
- The config disables three rules whose warnings are intentional for CE v0.1:
  - `no-server-example.com`: the canonical deployment is `http://localhost:8080`; production hosts are configured per deployment.
  - `operation-4xx-response`: read-only Admin/System GET endpoints rely on the standard 4xx envelope documented in `info.description` and `09-contracts/errors.md`. Mutating endpoints DO declare them explicitly.
  - `no-unused-components`: `BadRequest` is intentionally retained in `components.responses` for future endpoints.
- Without the config, `redocly lint` produces ~11 warnings (all acceptable) but exits 0.
- `prisma validate` prints `The schema at … is valid 🚀`.

The included `prisma.config.ts` follows the Prisma ORM v7 convention where datasource URLs live in config instead of the schema file. It should be copied to the implementation package root or invoked with Prisma's `--config` option after Prisma is installed locally.
