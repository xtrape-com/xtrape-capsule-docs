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
09-contracts/prisma/schema.prisma
09-contracts/prisma/prisma.config.ts
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

## 6. Validation

Recommended checks:

```bash
ruby -e "require 'yaml'; YAML.load_file('09-contracts/openapi/opstage-ce-v0.1.yaml')"
npx prisma validate --schema 09-contracts/prisma/schema.prisma
```

The included `prisma.config.ts` follows the Prisma ORM v7 convention where datasource URLs live in config instead of the schema file. It should be copied to the implementation package root or invoked with Prisma's `--config` option after Prisma is installed locally.
