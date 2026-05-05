---
status: draft
audience: ai-coding-agents
stability: unstable
last_reviewed: 2026-05-05
edition: ce
phase: current
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 05-implementation-sequence.md
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

# CE（社区版） v0.1 实现 Sequence

- Status: 实施指南
- Edition: CE（社区版）
- Priority: Current
- Audience: founders, architects, backend developers, frontend developers, agent SDK developers, test engineers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/` (OpenAPI / Prisma) disagree, the ADRs and contracts win for CE（社区版） v0.1.

## 1. Goal

Define the recommended build order for CE（社区版） v0.1.

The sequence should reduce integration risk by proving the backend/API/data loop before polishing UI and packaging.

## 2. Phase 0 — Repository Scaffold

Deliver:

- pnpm workspace;
- TypeScript base config;
- lint/format/test tooling;
- package layout;
- copied OpenAPI and Prisma contracts;
- CI placeholder.

Exit criteria:

- `pnpm install` works;
- `pnpm build` works for empty packages;
- `pnpm test` works for placeholder tests.

## 3. Phase 1 — Database and Backend Kernel

Deliver:

- Prisma schema and migrations;
- default Workspace bootstrap;
- admin bootstrap;
- Fastify server;
- system health/version;
- auth login/logout/me;
- structured error envelope;
- audit write helper.

Exit criteria:

- admin can log in;
- system health returns safe response;
- login success/failure audit events exist.

## 4. Phase 2 — Agent（代理） Registration and Service Report

Deliver:

- registration token creation/list/revoke;
- Agent（代理） registration;
- Agent（代理） token auth;
- heartbeat;
- service report persistence;
- Agent（代理） and Capsule Service（胶囊服务） admin list/detail.

Exit criteria:

- fake Agent（代理） can register;
- fake Agent（代理） can heartbeat;
- fake Agent（代理） can report service;
- UI/API can see Agent（代理） and service.

## 5. Phase 3 — Command and Action Loop

Deliver:

- action definition persistence from service report;
- action request endpoint;
- Command creation;
- Agent（代理） command polling;
- CommandResult reporting;
- Command status transitions;
- audit for Command creation/result.

Exit criteria:

- fake Agent（代理） can poll a Command;
- fake Agent（代理） can report success/failure;
- Backend shows final Command state.

## 6. Phase 4 — Node Agent（代理） SDK

Deliver:

- SDK registration;
- file token store;
- heartbeat loop;
- service report;
- action registry;
- command polling loop;
- result reporting;
- retry/backoff;
- safe logging.

Exit criteria:

- SDK integration test runs against Backend;
- SDK executes `echo` Command end to end.

## 7. Phase 5 — Demo Capsule Service（胶囊服务）

Deliver:

- demo service using SDK;
- manifest;
- health provider;
- configs;
- `echo` action;
- `runHealthCheck` action.

Exit criteria:

- demo service proves the complete governance loop.

## 8. Phase 6 — UI

Deliver:

- login;
- dashboard;
- Agents;
- Capsule Services;
- action execution dialog;
- Commands;
- AuditEvents;
- registration token UI;
- system/settings page.

Exit criteria:

- user can complete the MVP flow from browser.

## 9. Phase 7 — Packaging and Release Candidate

Deliver:

- single Opstage（运维舞台） container;
- static UI served by Backend;
- SQLite data volume;
- Docker Compose with demo service;
- README quick start;
- smoke test script.

Exit criteria:

- clean machine can run the CE（社区版） v0.1 quick start;
- user can complete demo flow in a few minutes.

## 10. Do Not Start Before Kernel Is Working

Do not prioritize these before Phase 3 works:

- advanced dashboard charts;
- Cloud（云版） concepts;
- RBAC;
- SSO;
- plugin marketplace;
- full observability;
- multiple SDK languages;
- Kubernetes deployment.
