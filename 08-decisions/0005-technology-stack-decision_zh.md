---
status: draft
audience: ai-coding-agents
stability: unstable
last_reviewed: 2026-05-05
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

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

## Status

Draft

## Date

2026-05-05

## Context

本 ADR 记录当前 Xtrape Capsule CE 设计基线中的一项架构或实现决策。详细背景见下方原始决策内容。

## Decision

采用下方“Decision/决策”内容作为当前基线。

## Consequences

该决策会影响 CE 当前实现、相关规范和后续文档维护。具体取舍见下方原始内容。

## Alternatives Considered

未在本模板区单独展开；如原始内容中记录了备选方案，以原始内容为准。

## Implementation Notes

实现和文档引用应优先遵循本 ADR 的 accepted/proposed 状态，并与 `02-specs/`、`10-implementation/` 中的当前 CE 文档保持一致。

## Supersedes / Superseded By

None.

## Original Decision Notes


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
UI:              React 18 + TypeScript + Ant Design (antd 5.x)  (frontend stack pinned by ADR 0007)
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

React 18 + Ant Design (antd 5.x) is selected for the UI; see [ADR 0007](./0007-ui-state-and-data-fetching.md) for the full stack and rationale.

The four-repository structure (CE（社区版） app + Agent（代理） SDK + Contracts + Docs) is pinned by [ADR
0008](./0008-naming-and-repositories.md), with contracts spec/bindings governance defined by [ADR
0009](./0009-contracts-spec-and-bindings.md).

NestJS remains acceptable for future productization if the project needs heavier module structure, dependency injection patterns, or enterprise-scale backend organization.

## SQLite Rules

CE（社区版） v0.1 uses SQLite by default. Recommended runtime conventions:

```text
OPSTAGE_DATA_DIR=/app/data
SQLite file=/app/data/opstage.db
```

CE（社区版） v0.1 is single-node only. Running multiple Backend instances against the same SQLite database file is unsupported.

The implementation should prefer portable column types and JSON text fields for flexible metadata.
