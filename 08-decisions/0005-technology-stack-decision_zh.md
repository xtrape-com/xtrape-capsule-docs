<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 0005-technology-stack-decision.md
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

# ADR 0005: CE（社区版） v0.1 Technology Stack Decision

- Status: Accepted
- Edition: CE（社区版）
- Priority: Current
- Audience: architects, backend developers, frontend developers, agent SDK developers, DevOps engineers, AI coding agents

## Decision

CE（社区版） v0.1 uses a lightweight TypeScript-first stack:

```text
Language:        TypeScript
Backend:         Fastify + TypeScript
Validation:      Zod
ORM:             Prisma
Database:        SQLite
UI:              Vue 3 + TypeScript + Ant Design Vue       (frontend stack pinned by ADR 0007)
Agent SDK:       Node.js + TypeScript                      (separate repo: xtrape-capsule-agent-node)
Contracts:       @xtrape/capsule-contracts-node from npm   (separate repo: xtrape-capsule-contracts-node)
Package Manager: pnpm
Monorepo:        pnpm workspace inside xtrape-capsule-ce only (4-repo polyrepo per ADR 0008)
UI Build:        Vite
Package Build:   tsup or tsdown
Container:       Docker (ghcr.io/xtrape/opstage-ce)
Deployment:      single Opstage container first, Docker Compose optional
```

## Rationale

Fastify is selected for CE（社区版） v0.1 because it is lightweight, fast to implement, easy to package, and sufficient for the first API surface.

Vue 3 + Ant 设计 Vue is selected for the UI; see [ADR 0007](./0007-ui-state-and-data-fetching.md) for the full stack and rationale.

The four-repository structure (CE（社区版） app + Agent（代理） SDK + Contracts + Docs) is pinned by [ADR 0008](./0008-naming-and-repositories.md), with contracts spec/bindings governance defined by [ADR 0009](./0009-contracts-spec-and-bindings.md).

NestJS remains acceptable for future productization if the project needs heavier module structure, dependency injection patterns, or enterprise-scale backend organization.

## SQLite Rules

CE（社区版） v0.1 uses SQLite by default. Recommended runtime conventions:

```text
OPSTAGE_DATA_DIR=/app/data
SQLite file=/app/data/opstage.db
```

CE（社区版） v0.1 is single-node only. Running multiple Backend instances against the same SQLite database file is unsupported.

The implementation should prefer portable column types and JSON text fields for flexible metadata.
