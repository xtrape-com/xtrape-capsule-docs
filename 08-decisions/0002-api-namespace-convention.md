# ADR 0002: API Namespace Convention

- Status: Accepted
- Edition: CE
- Priority: Current
- Audience: backend developers, frontend developers, agent SDK developers, AI coding agents

## Decision

CE v0.1 uses these API namespaces:

```text
/api/admin/*   Admin UI API, authenticated as a human user
/api/agents/*  Agent API, authenticated as a registered Agent after registration
/api/system/*  System health and version API
```

## Admin API

Canonical CE v0.1 Admin API paths:

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

## Agent API

Canonical CE v0.1 Agent API paths:

```text
POST /api/agents/register
POST /api/agents/{agentId}/heartbeat
POST /api/agents/{agentId}/services/report
GET  /api/agents/{agentId}/commands
POST /api/agents/{agentId}/commands/{commandId}/result
```

## System API

Canonical CE v0.1 System API paths:

```text
GET /api/system/health
GET /api/system/version
```

System API responses must not expose secrets, token values, database file paths, or sensitive environment configuration.
