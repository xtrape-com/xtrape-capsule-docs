# ADR 0005: CE v0.1 Technology Stack Decision

- Status: Accepted
- Edition: CE
- Priority: Current
- Audience: architects, backend developers, frontend developers, agent SDK developers, DevOps engineers, AI coding agents

## Decision

CE v0.1 uses a lightweight TypeScript-first stack:

```text
Language:        TypeScript
Backend:         Fastify + TypeScript
Validation:      Zod
ORM:             Prisma
Database:        SQLite
UI:              React + TypeScript + Ant Design
Agent SDK:       Node.js + TypeScript
Package Manager: pnpm
Monorepo:        pnpm workspace
UI Build:        Vite
Package Build:   tsup or tsdown
Container:       Docker
Deployment:      single Opstage container first, Docker Compose optional
```

## Rationale

Fastify is selected for CE v0.1 because it is lightweight, fast to implement, easy to package, and sufficient for the first API surface.

NestJS remains acceptable for future productization if the project needs heavier module structure, dependency injection patterns, or enterprise-scale backend organization.

## SQLite Rules

CE v0.1 uses SQLite by default. Recommended runtime conventions:

```text
OPSTAGE_DATA_DIR=/app/data
SQLite file=/app/data/opstage.db
```

CE v0.1 is single-node only. Running multiple Backend instances against the same SQLite database file is unsupported.

The implementation should prefer portable column types and JSON text fields for flexible metadata.
