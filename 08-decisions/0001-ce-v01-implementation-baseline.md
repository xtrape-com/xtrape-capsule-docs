---
status: accepted
audience: ai-coding-agents
stability: stable
last_reviewed: 2026-05-05
---

# ADR 0001: CE v0.1 Implementation Baseline

## Status

Accepted

## Date

2026-05-05

## Context

This ADR records an architecture or implementation decision for the current Xtrape Capsule CE design baseline. See the original decision notes below for the detailed background.

## Decision

Use the decision content below as the current baseline for this topic.

## Consequences

This decision constrains CE implementation work, related specifications, and future documentation maintenance. Detailed trade-offs are captured in the original decision notes below where available.

## Alternatives Considered

Not separately captured in this standardized template section. If alternatives are described in the original decision notes below, those notes remain authoritative.

## Implementation Notes

Implementation and documentation updates should follow this ADR status first, then align related `02-specs/` and current CE `10-implementation/` documents.

## Supersedes / Superseded By

None.

## Original Decision Notes


- Status: Accepted
- Edition: CE
- Priority: Current
- Audience: founders, product designers, architects, backend developers, frontend developers, agent SDK developers, AI coding agents

## 1. Decision

CE v0.1 will implement the smallest complete Capsule Service governance loop:

```text
Admin login
    ↓
Agent registration
    ↓
Service report
    ↓
Heartbeat and health
    ↓
Config metadata visibility
    ↓
Predefined action request
    ↓
Command polling
    ↓
Command result
    ↓
Audit log
```

CE v0.1 is a lightweight, self-hosted implementation target. It must be useful as an open-source product, but it must not include EE or Cloud complexity.

## 2. Product Baseline

CE v0.1 should allow a developer to:

1. start Opstage CE locally or with Docker;
2. initialize or log in as a local admin user;
3. create a registration token;
4. start a demo Node.js Capsule Service using the Node Embedded Agent SDK;
5. see the Agent and Capsule Service in the UI;
6. view manifest, health, config metadata, and action metadata;
7. trigger a predefined action;
8. see Command and CommandResult state;
9. inspect AuditEvents for important operations.

The primary user is a developer or small team operating lightweight internal services, workers, automation services, or
AI-related service capsules without adopting Kubernetes, service mesh, or SaaS-only tooling.

## 3. Architecture Baseline

CE v0.1 consists of:

```text
Opstage UI
    ↓ Admin API
Opstage Backend
    ↓ SQLite
Local database file

Node.js Capsule Service
    ↓ Node Embedded Agent SDK outbound HTTP
Opstage Backend Agent API
```

The Backend is the control plane. The Agent SDK is the governance bridge. The Capsule Service owns business logic and local execution.

## 4. API Namespace Baseline

CE v0.1 uses three API namespaces:

```text
/api/admin/*   UI-facing authenticated Admin API
/api/agents/*  Agent-facing authenticated Agent API, except initial registration
/api/system/*  system health and version API
```

The canonical service resource name is:

```text
capsule-services
```

Do not use `/api/admin/services` for CE v0.1 public API paths.

## 5. Technology Baseline

CE v0.1 uses:

```text
Language:        TypeScript
Backend:         Fastify + TypeScript
Validation:      Zod
ORM:             Prisma
Database:        SQLite
UI:              React 18 + TypeScript + Ant Design (antd 5.x)
                 (+ TanStack React Query + React Router 7.x; see ADR 0007)
Agent SDK:       Node.js + TypeScript (separate repo: xtrape-capsule-agent-node)
Contracts:       @xtrape/capsule-contracts-node from npm (separate repo)
Package Manager: pnpm
Monorepo:        pnpm workspace inside xtrape-capsule-ce only (4-repo polyrepo overall; see ADR 0008)
Build:           Vite for UI, tsup or tsdown for packages
Deployment:      single container first (ghcr.io/xtrape/opstage-ce), Docker Compose optional
```

NestJS remains a future or alternative option, but it is not the CE v0.1 baseline. The UI stack and the multi-repo split
are pinned by [ADR 0007](./0007-ui-state-and-data-fetching.md) and [ADR 0008](./0008-naming-and-repositories.md)
respectively, which supersede earlier drafts of this baseline.

## 6. Command and Action Baseline

Actions are predefined operations reported by the Agent SDK. Opstage does not execute shell commands and does not create arbitrary scripts.

Command states:

```text
PENDING
RUNNING
SUCCEEDED
FAILED
EXPIRED
CANCELLED
```

CE v0.1 may omit user-facing cancellation, but the state is reserved.

Command creation flow:

1. Admin triggers `POST /api/admin/capsule-services/{serviceId}/actions/{actionName}`.
2. Backend authenticates the user.
3. Backend validates service, Agent ownership, action definition, and payload.
4. Backend creates a durable Command.
5. Agent polls the Command.
6. Backend marks the Command as running.
7. Agent executes the local registered handler.
8. Agent reports CommandResult.
9. Backend stores result and writes AuditEvent.

## 7. Security Baseline

CE v0.1 must implement:

- authenticated Admin UI by default;
- local admin user;
- password hashing with argon2, or bcrypt if packaging requires it;
- HTTP-only session cookie or carefully handled bearer token;
- hashed registration tokens;
- hashed Agent tokens;
- one-time token display;
- revocable registration and Agent tokens;
- no raw secret storage by default;
- no arbitrary shell, exec, or script execution API;
- AuditEvents for login, failed login, token creation/revocation, Agent registration, Command creation, and Command completion.

## 8. Data Model Baseline

CE v0.1 implements:

```text
User
Workspace
Agent
AgentToken
RegistrationToken
CapsuleService
HealthReport
ConfigItem
ActionDefinition
Command
CommandResult
AuditEvent
SystemSetting
```

CE v0.1 does not implement first-class:

```text
Tenant
Organization
BillingAccount
Role
Permission
SecretStore
MetricSeries
LogStream
AlertRule
ClusterNode
```

Flexible fields should use portable JSON text columns such as `manifestJson`, `payloadJson`, `resultJson`, and `metadataJson`.

## 9. Non-Goals

CE v0.1 must not include:

- tenant system;
- billing;
- subscription;
- enterprise RBAC;
- SSO / OIDC / LDAP / SAML;
- Redis requirement;
- queue requirement;
- Kubernetes requirement;
- Agent Gateway;
- Sidecar Agent;
- External Agent;
- Java/Python/Go SDKs;
- full observability platform;
- centralized log collection;
- metrics database;
- secret vault;
- license enforcement;
- remote shell;
- arbitrary script execution;
- workflow designer;
- plugin marketplace.

## 10. Defaults and Thresholds

CE v0.1 timing defaults are normative. Backend MUST honor these unless explicitly overridden via environment variables.
Agent SDK MUST treat the values returned in `RegisterAgentResponse` / `AgentHeartbeatResponse` as the authoritative
cadence.

```text
heartbeatIntervalSeconds         30      OPSTAGE_AGENT_HEARTBEAT_INTERVAL_SECONDS
agentOfflineThresholdSeconds     90      OPSTAGE_AGENT_OFFLINE_THRESHOLD_SECONDS
commandPollIntervalSeconds        5      OPSTAGE_COMMAND_POLL_INTERVAL_SECONDS
commandTtlSeconds               300      OPSTAGE_COMMAND_TTL_SECONDS
healthStaleThresholdSeconds     120      OPSTAGE_HEALTH_STALE_THRESHOLD_SECONDS  (default: 4 × heartbeatIntervalSeconds)
backgroundSweepIntervalSeconds   30      OPSTAGE_BACKGROUND_SWEEP_INTERVAL_SECONDS
backgroundSweepBatchSize        500      OPSTAGE_BACKGROUND_SWEEP_BATCH_SIZE
sessionTtlSeconds             28800      OPSTAGE_SESSION_TTL_SECONDS              (8 hours)
csrfTokenBytes                   32      not configurable (CE v0.1)
```

Constraints:

- `agentOfflineThresholdSeconds` MUST be at least `2 × heartbeatIntervalSeconds`;
- `commandPollIntervalSeconds` MUST be at least `1` and SHOULD NOT exceed `heartbeatIntervalSeconds`;
- `commandTtlSeconds` MUST be at least `30`;
- `backgroundSweepIntervalSeconds` MUST be at most `agentOfflineThresholdSeconds / 2` so freshness updates do not lag a full Agent offline window;
- `backgroundSweepBatchSize` MUST be a positive integer; SQLite deployments SHOULD keep it at or below 1000;
- defaults are duplicated in `09-contracts/openapi/opstage-ce-v0.1.yaml` schema descriptions for discoverability, but this ADR is the single source of truth.

## 11. Implementation Rule

When documents disagree, CE v0.1 implementation should follow this ADR first, then the contracts in `09-contracts/`,
then the CE implementation target documents, then shared specifications.
