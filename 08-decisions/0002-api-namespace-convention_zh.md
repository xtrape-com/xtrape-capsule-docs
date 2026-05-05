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
原始文件 / Original File: 0002-api-namespace-convention.md
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

# ADR 0002: API Namespace Convention

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
- Audience: backend developers, frontend developers, agent SDK developers, AI coding agents

## Decision

CE（社区版） v0.1 uses these API namespaces:

```text
/api/admin/*   Admin UI API, authenticated as a human user
/api/agents/*  Agent API, authenticated as a registered Agent after registration
/api/system/*  System health and version API
```

## Admin API

Canonical CE（社区版） v0.1 Admin API paths:

```text
POST /api/admin/auth/login
POST /api/admin/auth/logout
GET  /api/admin/auth/me

GET  /api/admin/dashboard/summary

GET  /api/admin/agents
GET  /api/admin/agents/{agentId}
POST /api/admin/agents/{agentId}/disable
POST /api/admin/agents/{agentId}/enable
POST /api/admin/agents/{agentId}/revoke

POST /api/admin/registration-tokens
GET  /api/admin/registration-tokens
POST /api/admin/registration-tokens/{tokenId}/revoke

GET  /api/admin/capsule-services
GET  /api/admin/capsule-services/{serviceId}
GET  /api/admin/capsule-services/{serviceId}/manifest
GET  /api/admin/capsule-services/{serviceId}/health
GET  /api/admin/capsule-services/{serviceId}/configs
GET  /api/admin/capsule-services/{serviceId}/actions
POST /api/admin/capsule-services/{serviceId}/actions/{actionName}

GET  /api/admin/commands
GET  /api/admin/commands/{commandId}

GET  /api/admin/audit-events
GET  /api/admin/audit-events/{auditEventId}
```

## Agent（代理） API

Canonical CE（社区版） v0.1 Agent（代理） API paths:

```text
POST /api/agents/register
POST /api/agents/{agentId}/heartbeat
POST /api/agents/{agentId}/services/report
GET  /api/agents/{agentId}/commands
POST /api/agents/{agentId}/commands/{commandId}/result
```

## System API

Canonical CE（社区版） v0.1 System API paths:

```text
GET /api/system/health
GET /api/system/version
```

System API responses must not expose secrets, token values, database file paths, or sensitive environment configuration.
