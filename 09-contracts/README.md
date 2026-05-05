---
status: accepted
audience: backend-developers
stability: evolving
last_reviewed: 2026-05-05
---

# CE v0.1 Implementation Contracts

- Status: Implementation Target
- Edition: CE
- Priority: Current
- Audience: architects, backend developers, frontend developers, agent SDK developers, test engineers, AI coding agents

This directory is **Layer 1** of the contracts model: the language-agnostic single source of truth (SSOT) for the CE
v0.1 wire format, error codes, status enumerations, audit actions, ID prefixes, and persistence schema.

> **Read first**: [ADR 0009 — Contracts Spec and Bindings](../08-decisions/0009-contracts-spec-and-bindings.md). It defines the two-layer model (Spec + Bindings), the per-language repository strategy (Path C), and the synchronization rules.

## 1. Two-Layer Model (summary)

| Layer | What it is | Where it lives | Audience |
|---|---|---|---|
| **Layer 1 — Spec** | Language-agnostic, hand-authored, machine-readable | **here** (`xtrape-capsule-docs/09-contracts/`) | Humans + every codegen |
| **Layer 2 — Bindings** | Generated language-native code (types, runtime validators, constants) | per-language repos (see §3) | Application code |

Layer 1 is the SSOT. Layer 2 mirrors Layer 1 and regenerates from it; PRs to a binding repo MUST NOT edit `spec/` directly — see ADR 0009 §"Sync Workflow".

## 2. Layer 1 Files

```text
09-contracts/
├── README.md                 (this file — navigation)
├── openapi/
│   ├── opstage-ce-v0.1.yaml  ★ HTTP wire format (primary spec file)
│   └── redocly.yaml          (lint config)
├── prisma/
│   ├── schema.prisma         (CE persistence schema; review copy)
│   └── prisma.config.ts
├── enums/
│   ├── status-enums.json     ★ AgentStatus, CapsuleServiceStatus, CommandStatus, ...
│   ├── audit-actions.json    ★ canonical AuditEvent.action values
│   └── id-prefixes.json      ★ newId(prefix) prefix table
├── errors.json               ★ canonical error codes + HTTP statuses
├── errors.md                   rendered from errors.json (CI checks parity)
├── examples/                   wire-format fixtures used by every binding's conformance test
└── tools/                      markdown renderers (no language bindings here)
```

Files marked ★ are the four JSON SSOT files. They are the inputs that every binding repo reads.

`prisma/schema.prisma` is included here for review and contract-driven development. The **authoritative** copy lives in `xtrape-capsule-ce/packages/db/schema.prisma` (CE-bound).

## 3. Layer 2 Bindings (per-language repositories)

| Repository | Status | Package | Read |
|---|---|---|---|
| `xtrape-capsule-contracts-node` | **CE v0.1** | `@xtrape/capsule-contracts-node` (npm) | ADR 0009 §"Layer 2 repository skeleton" |
| `xtrape-capsule-contracts-python` | future | `xtrape-capsule-contracts-python` (PyPI) | (when Python Agent ships) |
| `xtrape-capsule-contracts-java` | future | `com.xtrape:capsule-contracts-java` (Maven) | (when Java Agent ships) |
| `xtrape-capsule-contracts-go` | future | `github.com/xtrape/xtrape-capsule-contracts-go` | (when Go Agent ships) |

Repository naming is normative — see [ADR 0008 — Naming and Repositories](../08-decisions/0008-naming-and-repositories.md).

CE v0.1 only ships the Node binding. The remaining three are listed for forward-compatibility; their codegen path is identical (read `09-contracts/`, emit language-native types).

## 4. Contract Priority

When implementing CE v0.1, use this priority order (highest first):

```text
1. Accepted ADRs in 08-decisions/ (especially 0008, 0009)
2. Layer 1 SSOT (this directory)
3. Layer 2 bindings published to npm (`@xtrape/capsule-contracts-node`)
4. CE implementation target documents (03-editions/ce/, 10-implementation/)
5. Shared specifications (02-specs/, 04-opstage/, 05-agents/)
6. Planning documents only as future context (06-runtimes/, 07-roadmap/)
```

If older prose contradicts the contracts (e.g. legacy paths like `/api/auth/login`), the contracts win for CE v0.1.

## 5. API Contract

`openapi/opstage-ce-v0.1.yaml` defines:

- Admin API under `/api/admin/*`;
- Agent API under `/api/agents/*`;
- System API under `/api/system/*`;
- request and response shapes for the CE governance loop;
- canonical naming for Capsule Service, Command, CommandResult, AuditEvent, RegistrationToken, AgentToken resources;
- standard `ErrorEnvelope` and `SuccessEnvelope` shapes.

## 6. Persistence Contract

`prisma/schema.prisma` defines the CE v0.1 baseline persistence model:

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

The authoritative copy is maintained in `xtrape-capsule-ce/packages/db/`. This directory tracks the same schema for review and for cross-repo drift detection.

## 7. Field Naming Mapping (Prisma ↔ OpenAPI)

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

## 8. Validation

```bash
# OpenAPI YAML well-formedness (no install required, ruby is enough)
ruby -e "require 'yaml'; YAML.load_file('xtrape-capsule-docs/09-contracts/openapi/opstage-ce-v0.1.yaml')"

# Stricter OpenAPI 3.1 lint (Redocly publishes multiple bins, pin via --package)
# A repo-local redocly config disables three benign rules.
pnpm --package=@redocly/cli dlx redocly lint \
  xtrape-capsule-docs/09-contracts/openapi/opstage-ce-v0.1.yaml \
  --config xtrape-capsule-docs/09-contracts/openapi/redocly.yaml

# Prisma schema validation
pnpm dlx prisma@latest validate --schema xtrape-capsule-docs/09-contracts/prisma/schema.prisma

# JSON SSOT validity (every *.json must parse and follow its schema)
node --experimental-strip-types -e "['errors.json','enums/status-enums.json','enums/audit-actions.json','enums/id-prefixes.json'].forEach(p => JSON.parse(require('fs').readFileSync('xtrape-capsule-docs/09-contracts/'+p,'utf8')))"

# Markdown render parity (errors.md must match errors.json output)
pnpm tsx xtrape-capsule-docs/09-contracts/tools/render-errors.ts --check
```

Expected lint output:

- With the repo-local `redocly.yaml`, the lint output is **valid with zero warnings**.
- The config disables three rules whose warnings are intentional for CE v0.1:
  - `no-server-example.com`: the canonical deployment is `http://localhost:8080`; production hosts are configured per deployment.
  - `operation-4xx-response`: read-only Admin/System GET endpoints rely on the standard 4xx envelope documented in `info.description` and `errors.md`. Mutating endpoints DO declare them explicitly.
  - `no-unused-components`: `BadRequest` is intentionally retained in `components.responses` for future endpoints.
- Without the config, `redocly lint` produces ~11 warnings (all acceptable) but exits 0.
- `prisma validate` prints `The schema at … is valid 🚀`.

The included `prisma.config.ts` follows the Prisma ORM v7 convention where datasource URLs live in config instead of the
schema file. It should be copied to the implementation package root (`xtrape-capsule-ce/packages/db/`) or invoked with
Prisma's `--config` option after Prisma is installed locally.

## 9. Editing the SSOT

To change the wire format:

1. Edit one of `openapi/opstage-ce-v0.1.yaml`, `errors.json`, `enums/*.json`, or add a fixture under `examples/`.
2. Run the renderers in `tools/` to regenerate `errors.md` and any `<!-- BEGIN GENERATED -->`-marked sections in spec docs.
3. Open a PR. CI runs:
   - `redocly lint` (zero-warning under `redocly.yaml`);
   - `prisma validate`;
   - JSON parse + JSON Schema check;
   - render-parity check (`--check` mode).
4. After merge, every binding repo's `upstream-bump.yml` workflow opens a PR within ~24h to bump its mirror of `09-contracts/`.

See ADR 0009 §"Sync Workflow" for the full pipeline.
