# CE v0.1 Implementation Sequence

- Status: Implementation Guidance
- Edition: CE
- Priority: Current
- Audience: founders, architects, backend developers, frontend developers, agent SDK developers, test engineers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/` (OpenAPI / Prisma) disagree, the ADRs and contracts win for CE v0.1.

## 1. Goal

Define the recommended build order for CE v0.1.

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

## 4. Phase 2 — Agent Registration and Service Report

Deliver:

- registration token creation/list/revoke;
- Agent registration;
- Agent token auth;
- heartbeat;
- service report persistence;
- Agent and Capsule Service admin list/detail.

Exit criteria:

- fake Agent can register;
- fake Agent can heartbeat;
- fake Agent can report service;
- UI/API can see Agent and service.

## 5. Phase 3 — Command and Action Loop

Deliver:

- action definition persistence from service report;
- action request endpoint;
- Command creation;
- Agent command polling;
- CommandResult reporting;
- Command status transitions;
- audit for Command creation/result.

Exit criteria:

- fake Agent can poll a Command;
- fake Agent can report success/failure;
- Backend shows final Command state.

## 6. Phase 4 — Node Agent SDK

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

## 7. Phase 5 — Demo Capsule Service

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

- single Opstage container;
- static UI served by Backend;
- SQLite data volume;
- Docker Compose with demo service;
- README quick start;
- smoke test script.

Exit criteria:

- clean machine can run the CE v0.1 quick start;
- user can complete demo flow in a few minutes.

## 10. Do Not Start Before Kernel Is Working

Do not prioritize these before Phase 3 works:

- advanced dashboard charts;
- Cloud concepts;
- RBAC;
- SSO;
- plugin marketplace;
- full observability;
- multiple SDK languages;
- Kubernetes deployment.
