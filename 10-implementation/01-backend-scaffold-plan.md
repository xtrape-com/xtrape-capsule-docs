# CE v0.1 Backend Scaffold Plan

- Status: Implementation Guidance
- Edition: CE
- Priority: Current
- Audience: backend developers, architects, security reviewers, test engineers, AI coding agents

## 1. Goal

Build the Fastify Backend that implements the CE v0.1 governance loop and conforms to:

```text
09-contracts/openapi/opstage-ce-v0.1.yaml
09-contracts/prisma/schema.prisma
```

## 2. Package

Recommended package:

```text
apps/opstage-backend
```

## 3. Stack

```text
Fastify
TypeScript
Zod
Prisma
SQLite
pino
Vitest
```

## 4. Suggested Source Layout

```text
apps/opstage-backend/src/
├── main.ts
├── app.ts
├── config/
│   └── env.ts
├── plugins/
│   ├── prisma.ts
│   ├── auth-session.ts
│   ├── errors.ts
│   └── audit.ts
├── modules/
│   ├── auth/
│   ├── dashboard/
│   ├── agents/
│   ├── registration-tokens/
│   ├── capsule-services/
│   ├── commands/
│   ├── audit-events/
│   └── system/
├── security/
│   ├── password.ts
│   ├── tokens.ts
│   ├── redaction.ts
│   └── csrf.ts
└── tests/
```

## 5. Backend Modules

### 5.1 Auth

Routes:

```text
POST /api/admin/auth/login
POST /api/admin/auth/logout
GET  /api/admin/auth/me
```

Responsibilities:

- local admin login;
- password hash verification;
- session creation;
- failed login audit;
- successful login audit;
- logout audit if practical.

### 5.2 Registration Tokens

Routes:

```text
POST /api/admin/registration-tokens
GET  /api/admin/registration-tokens
POST /api/admin/registration-tokens/{tokenId}/revoke
```

Rules:

- raw token shown once;
- hash only in DB;
- prefix `opstage_reg_`;
- revocable;
- optional expiry.

### 5.3 Agent API

Routes:

```text
POST /api/agents/register
POST /api/agents/{agentId}/heartbeat
POST /api/agents/{agentId}/services/report
GET  /api/agents/{agentId}/commands
POST /api/agents/{agentId}/commands/{commandId}/result
```

Rules:

- registration uses registration token;
- all later calls require Agent bearer token;
- path `agentId` must match authenticated Agent;
- disabled/revoked Agents are rejected;
- Agent token prefix `opstage_agent_`;
- raw Agent token returned only once.

### 5.4 Capsule Services

Routes:

```text
GET  /api/admin/capsule-services
GET  /api/admin/capsule-services/{serviceId}
GET  /api/admin/capsule-services/{serviceId}/manifest
GET  /api/admin/capsule-services/{serviceId}/health
GET  /api/admin/capsule-services/{serviceId}/configs
GET  /api/admin/capsule-services/{serviceId}/actions
POST /api/admin/capsule-services/{serviceId}/actions/{actionName}
```

Responsibilities:

- store and expose service manifest;
- store and expose config metadata;
- store and expose action definitions;
- create Commands for valid predefined actions;
- calculate effective status.

### 5.5 Commands

Routes:

```text
GET /api/admin/commands
GET /api/admin/commands/{commandId}
```

Agent routes handle polling and result reporting.

State machine:

```text
PENDING -> RUNNING -> SUCCEEDED
PENDING -> RUNNING -> FAILED
PENDING/RUNNING -> EXPIRED
```

`CANCELLED` is reserved.

### 5.6 Audit Events

Routes:

```text
GET /api/admin/audit-events
GET /api/admin/audit-events/{auditEventId}
```

Minimum audited operations:

- login success;
- login failure;
- registration token creation;
- registration token revocation;
- Agent registration;
- Agent disable/enable/revoke;
- Command creation;
- Command result.

### 5.7 System

Routes:

```text
GET /api/system/health
GET /api/system/version
```

Must not expose secrets, token hashes, raw environment, or database file path.

## 6. Bootstrap

At startup:

1. load environment;
2. ensure `OPSTAGE_SESSION_SECRET` exists;
3. initialize DB directory if needed;
4. run or require migrations according to deployment mode;
5. create default Workspace;
6. create admin user from bootstrap variables if no user exists;
7. start API server.

No weak default credentials are allowed.

## 7. Test Plan

Minimum backend tests:

- admin login success/failure;
- registration token creation stores hash only;
- Agent registration returns raw Agent token once;
- revoked Agent cannot heartbeat;
- service report creates/updates CapsuleService;
- action request creates Command;
- Agent polling transitions Command to RUNNING;
- CommandResult transitions Command to SUCCEEDED/FAILED;
- audit events are written;
- system health does not leak sensitive data.
