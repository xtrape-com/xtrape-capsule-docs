# CE MVP

- Status: Implementation Target
- Edition: CE
- Priority: Current
- Audience: product designers, architects, backend developers, frontend developers, agent SDK developers, AI coding agents

This document defines the **Minimum Viable Product** for **Opstage CE v0.1**.

The MVP must prove the smallest complete governance loop for Capsule Services:

```text
Agent registration
    ↓
Service report
    ↓
Heartbeat and health
    ↓
UI visibility
    ↓
Predefined action request
    ↓
Command polling
    ↓
Command result
    ↓
Audit log
```

---

## 1. MVP Goal

The goal of CE v0.1 MVP is:

> A developer can run Opstage CE locally, start a demo Node.js Capsule Service with an embedded Agent SDK, see it in the UI, trigger a predefined action, see the command result, and inspect the audit log.

This goal is intentionally narrow.

The MVP should prove that the `xtrape-capsule` model works end to end without building a full enterprise platform.

---

## 2. MVP Product Promise

CE v0.1 should deliver this promise:

> In a few minutes, a developer can self-host Opstage CE and bring a Node.js Capsule Service under basic governance.

The user should be able to answer:

- Which Agents are connected?
- Which Capsule Services are reported?
- Is the service online, unhealthy, stale, or offline?
- What does the service manifest look like?
- What health status did it report?
- What config metadata did it expose?
- What actions can I run?
- Did my action command succeed or fail?
- What happened according to the audit log?

---

## 3. MVP User Stories

### 3.1 Start Opstage CE

As a developer, I want to start Opstage CE locally so that I can manage Capsule Services without external SaaS dependencies.

Acceptance:

- Backend starts successfully.
- UI is accessible in the browser.
- SQLite database is initialized.
- Default Workspace exists.
- Admin login is available.

### 3.2 Register an Agent

As a developer, I want a demo Capsule Service to register through a Node.js embedded Agent so that it appears in Opstage.

Acceptance:

- Registration token exists.
- Agent registers with Backend.
- Backend issues Agent token.
- Agent token is stored as hash in Backend.
- UI shows the Agent.

### 3.3 Report a Capsule Service

As a developer, I want the Agent to report a Capsule Service manifest so that Opstage can display the service.

Acceptance:

- Agent reports manifest.
- Backend validates required fields.
- Backend stores manifest JSON.
- Backend creates or updates CapsuleService record.
- UI shows service list and service detail.

### 3.4 View health and status

As an operator, I want to see Agent and service status so that I know whether the service is currently governable.

Acceptance:

- Agent heartbeat updates `lastHeartbeatAt`.
- UI shows Agent online/offline status.
- Agent reports service health.
- UI shows HealthStatus.
- Backend calculates effective Capsule Service status.
- Stale status is shown when Agent stops heartbeating.

### 3.5 View config metadata

As an operator, I want to see configuration metadata so that I understand how the service is configured without exposing secrets.

Acceptance:

- Demo service reports at least one ConfigItem.
- UI displays config key, label, type, default value, editability, and sensitivity.
- Sensitive values are masked or represented as `secretRef`.

### 3.6 Execute a predefined action

As an operator, I want to trigger a predefined action so that I can safely operate the service.

Acceptance:

- UI lists available actions.
- User triggers `runHealthCheck` or `echo`.
- Backend creates an `ACTION` Command.
- Agent polls the Command.
- Agent executes a registered action handler.
- Agent reports CommandResult.
- UI shows success or failure.

### 3.7 Inspect audit logs

As an operator, I want to inspect audit logs so that I can trace important operations.

Acceptance:

- Login is audited.
- Agent registration is audited.
- Command creation is audited.
- Command result is audited.
- UI shows audit list.

---

## 4. MVP Functional Requirements

### 4.1 Authentication

MVP must include:

- local admin user;
- login API;
- logout API or session clearing;
- login audit event;
- failed login audit event.

MVP may use simple authentication, but it must not expose the UI without authentication by default.

### 4.2 Workspace

MVP must include:

- one default Workspace;
- all core data associated with the default Workspace where practical.

MVP does not need:

- Workspace creation UI;
- Workspace switcher;
- tenant or organization model.

### 4.3 Agent registration

MVP must include:

- registration token generation or bootstrap;
- Agent registration endpoint;
- Agent token issuance;
- token hash storage;
- Agent status model;
- Agent list UI;
- Agent detail UI.

Required AgentStatus values:

```text
PENDING
ONLINE
OFFLINE
DISABLED
REVOKED
```

### 4.4 Agent heartbeat

MVP must include:

- heartbeat endpoint;
- heartbeat interval returned to Agent;
- last heartbeat storage;
- online/offline calculation.

Recommended defaults:

```text
heartbeatIntervalSeconds = 30
agentOfflineThresholdSeconds = 90
```

### 4.5 Capsule Service report

MVP must include:

- service report endpoint;
- manifest validation;
- manifest JSON storage;
- extracted service fields;
- service list UI;
- service detail UI.

Required manifest fields:

```text
kind
code
name
version
runtime
agentMode
```

### 4.6 Health

MVP must include:

- health provider in Agent SDK;
- health report from Agent;
- latest health storage;
- service effective status calculation;
- health display in UI.

Required HealthStatus values:

```text
UP
DOWN
DEGRADED
UNKNOWN
```

### 4.7 Config visibility

MVP must include:

- config metadata provider or manifest configs;
- config storage or manifest extraction;
- config display in UI;
- sensitive value masking;
- `secretRef` support.

MVP does not need config editing.

### 4.8 Actions

MVP must include:

- ActionDefinition shape;
- action metadata reporting;
- action list UI;
- action request API;
- predefined action handler execution through Agent.

Required demo actions:

```text
runHealthCheck
echo
```

Forbidden:

```text
arbitrary shell execution
```

### 4.9 Commands

MVP must include:

- `ACTION` command type;
- Command creation from action request;
- Command polling endpoint;
- CommandResult reporting endpoint;
- command status lifecycle;
- basic expiration;
- command UI.

Required CommandStatus values:

```text
PENDING
DISPATCHED
SUCCESS
FAILED
EXPIRED
```

### 4.10 Audit

MVP must include:

- AuditEvent storage;
- audit event creation for important operations;
- audit list UI;
- basic request/result sanitization.

Required audit events:

```text
user.login
user.login.failed
agent.registered
agent.service.reported
command.created
command.completed
command.failed
service.action.requested
service.action.completed
service.action.failed
```

The implementation may reduce duplicate events if traceability is preserved.

---

## 5. MVP Non-Functional Requirements

### 5.1 Lightweight deployment

MVP must run locally with SQLite.

Preferred deployment:

```text
single container
single exposed port
SQLite data volume
```

### 5.2 No external SaaS dependency

MVP must not require any external SaaS service to run.

### 5.3 Safe defaults

MVP must:

- require UI authentication;
- store only token hashes;
- avoid raw secrets in manifest, configs, commands, health, or audit events;
- execute only predefined actions;
- show stale status correctly.

### 5.4 Simple developer experience

MVP should provide:

- quick start command;
- demo service command;
- clear environment variables;
- basic troubleshooting notes.

### 5.5 Portable architecture

MVP should keep room for:

- MySQL/PostgreSQL;
- sidecar/external Agent;
- EE and Cloud editions;
- richer UI;
- stronger security.

But these must not complicate v0.1 unnecessarily.

---

## 6. MVP UI Pages

MVP should include these pages.

### 6.1 Login

Required:

- username/password login;
- failed login message;
- session/token persistence.

### 6.2 Dashboard

Required summary cards:

- number of Agents;
- number of online Agents;
- number of Capsule Services;
- number of unhealthy or stale services;
- recent Commands;
- recent Audit Events.

### 6.3 Agents

Required:

- Agent list;
- status;
- mode;
- runtime;
- last heartbeat;
- detail link.

### 6.4 Agent Detail

Required:

- Agent identity;
- status;
- heartbeat information;
- reported services;
- recent commands if available.

### 6.5 Capsule Services

Required:

- service list;
- code;
- name;
- runtime;
- version;
- effective status;
- health status;
- last reported time;
- associated Agent.

### 6.6 Capsule Service Detail

Required tabs:

```text
Overview
Manifest
Health
Configs
Actions
Commands
Audit
```

### 6.7 Commands

Required:

- command list;
- status;
- service;
- action name;
- created time;
- result summary.

### 6.8 Audit Logs

Required:

- audit list;
- time;
- actor;
- action;
- resource;
- result;
- description.

### 6.9 System Setup or Settings

Required or optional depending on bootstrap approach.

Useful fields:

- system version;
- default Workspace;
- heartbeat settings;
- command polling settings;
- registration token bootstrap status.

---

## 7. MVP Backend Modules

MVP Backend should include these conceptual modules:

```text
auth
workspaces
agents
agent-tokens
capsule-services
health
configs
actions
commands
audit
system
```

The physical implementation may combine modules, but the conceptual boundaries should stay clear.

---

## 8. MVP Agent SDK

The Node.js embedded Agent SDK should provide a minimal developer-facing API.

Example target shape:

```ts
const agent = new CapsuleAgent({
  backendUrl: process.env.OPSTAGE_BACKEND_URL,
  registrationToken: process.env.OPSTAGE_REGISTRATION_TOKEN,
  service: {
    code: 'demo-capsule-service',
    name: 'Demo Capsule Service',
    version: '0.1.0',
    runtime: 'nodejs',
  },
});

agent.health(async () => ({
  status: 'UP',
  message: 'Demo service is healthy.',
}));

agent.configs(() => ([
  {
    key: 'demo.message',
    label: 'Demo Message',
    type: 'string',
    defaultValue: 'hello capsule',
    editable: true,
    sensitive: false,
  },
]));

agent.action({
  name: 'echo',
  label: 'Echo',
  dangerLevel: 'LOW',
  handler: async (payload) => ({
    success: true,
    data: payload,
  }),
});

await agent.start();
```

This exact API may change, but MVP should support the same conceptual capabilities.

---

## 9. MVP Demo Capsule Service

The demo service should be intentionally simple.

Required identity:

```text
code: demo-capsule-service
name: Demo Capsule Service
runtime: nodejs
agentMode: embedded
version: 0.1.0
```

Required health:

```json
{
  "status": "UP",
  "message": "Demo service is healthy."
}
```

Required config:

```json
{
  "key": "demo.message",
  "label": "Demo Message",
  "type": "string",
  "defaultValue": "hello capsule",
  "editable": true,
  "sensitive": false
}
```

Required actions:

```text
runHealthCheck
echo
```

---

## 10. MVP Data Objects

MVP should implement or represent these data objects:

```text
User
Workspace
Agent
AgentToken
CapsuleService
HealthReport
ConfigItem
ActionDefinition
Command
CommandResult
AuditEvent
```

MVP should not implement these as first-class objects:

```text
Tenant
Organization
BillingAccount
ClusterNode
LogStream
MetricSeries
AlertRule
SecretStore
```

---

## 11. MVP API Groups

### 11.1 Admin APIs

Required capability groups:

```text
auth
dashboard
agents
capsule-services
actions
commands
audit-events
system
```

### 11.2 Agent APIs

Required endpoints:

```text
POST /api/agents/register
POST /api/agents/{agentId}/heartbeat
POST /api/agents/{agentId}/services/report
GET  /api/agents/{agentId}/commands
POST /api/agents/{agentId}/commands/{commandId}/result
```

Exact endpoint naming may be adjusted, but these capabilities must exist.

---

## 12. MVP Development Slices

Recommended implementation slices:

### Slice 1: Project skeleton

- monorepo structure;
- Backend app;
- UI app;
- shared types package;
- Agent SDK package;
- demo service package.

### Slice 2: Persistence and auth

- SQLite setup;
- basic schema;
- default Workspace;
- admin user;
- login/logout;
- auth guard.

### Slice 3: Agent registration

- registration token model;
- register API;
- Agent token issuance;
- Agent list UI.

### Slice 4: Heartbeat and service report

- heartbeat API;
- service report API;
- manifest storage;
- status calculation;
- service list UI.

### Slice 5: Agent SDK and demo service

- SDK registration;
- SDK heartbeat;
- SDK service report;
- demo service integration.

### Slice 6: Health and config visibility

- health provider;
- latest health storage;
- config provider;
- service detail UI tabs.

### Slice 7: Actions and commands

- action metadata;
- action request API;
- Command creation;
- command polling;
- action handler execution;
- CommandResult reporting.

### Slice 8: Audit and polish

- audit events;
- audit UI;
- stale status behavior;
- Docker packaging;
- quick-start docs.

---

## 13. MVP Acceptance Test

A successful MVP should pass this manual acceptance test.

### 13.1 Start system

1. Start Opstage CE.
2. Open UI.
3. Log in as admin.
4. Confirm dashboard loads.

### 13.2 Start demo service

1. Start demo Capsule Service with registration token.
2. Confirm Agent appears in UI.
3. Confirm Agent status is `ONLINE`.
4. Confirm Capsule Service appears in UI.

### 13.3 Inspect service

1. Open Capsule Service detail page.
2. Confirm manifest is visible.
3. Confirm health is `UP`.
4. Confirm config `demo.message` is visible.
5. Confirm actions `runHealthCheck` and `echo` are visible.

### 13.4 Execute action

1. Trigger `echo` action.
2. Confirm Backend creates Command.
3. Confirm Agent executes Command.
4. Confirm CommandResult is `SUCCESS`.
5. Confirm UI shows result.
6. Confirm audit log records the action.

### 13.5 Stop demo service

1. Stop demo service.
2. Wait past heartbeat timeout.
3. Confirm Agent becomes `OFFLINE`.
4. Confirm Capsule Service becomes `STALE`.
5. Confirm UI does not show the service as confidently online.

---

## 14. MVP Non-Goals

MVP must not spend time on:

- EE features;
- Cloud features;
- multi-tenant model;
- billing;
- enterprise RBAC;
- SSO;
- HA deployment;
- Kubernetes;
- centralized logs;
- metrics dashboards;
- config publishing;
- secret vault;
- Java/Python SDK;
- sidecar/external Agent;
- arbitrary shell execution.

---

## 15. MVP Completion Definition

CE v0.1 MVP is complete when:

- the end-to-end demo works;
- README can guide a new developer to run the system;
- demo service proves Agent SDK integration;
- UI shows status, health, config, actions, commands, and audit;
- Docker-based deployment works;
- no forbidden MVP non-goal is required for basic usage;
- core docs match the implementation.

---

## 16. Summary

The MVP is not about feature breadth.

It is about proving the core Capsule governance loop with a real, usable, self-hosted implementation.

The most important MVP rule is:

> Build one complete vertical slice before adding breadth.
