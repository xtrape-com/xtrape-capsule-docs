# CE Scope

- Status: Implementation Target
- Edition: CE
- Priority: Current
- Audience: product designers, architects, backend developers, frontend developers, agent SDK developers, AI coding agents

This document defines the implementation scope of **Opstage CE / Community Edition**.

CE v0.1 should deliver the smallest useful version of Opstage that proves the Capsule Service governance model through a Node.js embedded Agent, a Backend control plane, and a Web UI.

---

## 1. Scope Statement

Opstage CE v0.1 must focus on one goal:

> Make a Node.js Capsule Service visible, manageable, and auditable through Opstage using an embedded Agent SDK.

The first version should prove this loop:

```text
Node.js Capsule Service
    ↓ Embedded Agent SDK
Opstage Backend
    ↓
Opstage UI
```

CE v0.1 should be useful, lightweight, self-hosted, and simple to deploy.

---

## 2. In Scope

The following capabilities are in scope for CE v0.1.

### 2.1 Local admin access

CE v0.1 must provide a simple local admin login.

Required:

- initial admin account setup;
- login API;
- session or token-based UI authentication;
- logout;
- failed login handling;
- login audit events.

Not required:

- SSO;
- OIDC;
- LDAP;
- multi-factor authentication;
- enterprise RBAC.

### 2.2 Default Workspace

CE v0.1 must create and use one default Workspace.

Required:

- default Workspace record;
- all core records should be associated with the default Workspace where practical;
- no Workspace management UI is required.

Not required:

- multiple Workspaces;
- organization hierarchy;
- tenant isolation.

### 2.3 Agent registration

CE v0.1 must support Agent registration.

Required:

- registration token creation or bootstrap;
- Agent registration API;
- Agent token issuance;
- Agent token validation;
- token hash storage;
- Agent status;
- Agent list UI;
- Agent detail UI.

Not required:

- token rotation UI;
- device attestation;
- advanced Agent permission policies;
- sidecar Agent;
- external Agent.

### 2.4 Agent heartbeat

CE v0.1 must support Agent heartbeat.

Required:

- heartbeat API;
- last heartbeat timestamp;
- Agent online/offline calculation;
- heartbeat timeout configuration;
- UI display of Agent freshness.

Recommended defaults:

```text
heartbeatIntervalSeconds = 30
agentOfflineThresholdSeconds = 90
```

### 2.5 Capsule Service reporting

CE v0.1 must support Capsule Service metadata reporting through the Agent.

Required:

- service report API;
- manifest validation;
- service upsert by Workspace and service code;
- service-to-Agent association;
- manifest JSON storage;
- extracted display fields;
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

Recommended manifest fields:

```text
capabilities
actions
configs
resources
metadata
```

### 2.6 Health reporting

CE v0.1 must support latest health visibility.

Required:

- health provider support in Node.js embedded Agent SDK;
- health payload in heartbeat or service report;
- health status validation;
- latest health storage;
- service effective status calculation;
- stale state calculation;
- UI display of health status and freshness.

Required HealthStatus values:

```text
UP
DOWN
DEGRADED
UNKNOWN
```

Not required:

- health history charts;
- alert rules;
- Prometheus exporter;
- distributed tracing.

### 2.7 Config visibility

CE v0.1 must support configuration metadata visibility.

Required:

- ConfigItem shape;
- config reporting through manifest or service report;
- config storage or manifest extraction;
- config display in UI;
- sensitive value masking;
- `secretRef` display.

Not required:

- config editing;
- config publishing;
- config rollback;
- config approval workflow;
- distributed configuration synchronization.

### 2.8 Predefined actions

CE v0.1 must support predefined actions.

Required:

- ActionDefinition shape;
- action definitions reported by Agent;
- UI action list;
- action request API;
- confirmation for dangerous actions if present;
- no arbitrary shell execution.

Required demo actions:

```text
runHealthCheck
echo
```

### 2.9 Commands

CE v0.1 must support Commands for action execution.

Required:

- `ACTION` command type;
- Command creation from UI action request;
- Command polling API for Agent;
- CommandResult reporting API;
- command status lifecycle;
- basic expiration;
- UI command list or recent commands view.

Required CommandStatus values:

```text
PENDING
DISPATCHED
SUCCESS
FAILED
EXPIRED
```

Not required:

- WebSocket command delivery;
- gRPC streaming;
- queue-based delivery;
- automatic retry;
- scheduling;
- batch commands;
- cancellation UI.

### 2.10 Audit logs

CE v0.1 must support basic audit logs.

Required audit events:

- user login;
- failed login;
- Agent registration;
- first Capsule Service report;
- command creation;
- command success;
- command failure;
- action request and result if implemented separately.

Required UI:

- audit log list;
- basic audit detail view or expandable row.

Not required:

- audit export;
- immutable audit storage;
- compliance reports;
- SIEM integration;
- retention policy UI.

### 2.11 Web UI

CE v0.1 must provide a Web UI.

Required pages:

```text
Login
Dashboard
Agents
Agent Detail
Capsule Services
Capsule Service Detail
Commands
Audit Logs
System Settings or Setup
```

Minimum Capsule Service detail tabs:

```text
Overview
Manifest
Health
Configs
Actions
Commands
Audit
```

The UI must distinguish:

- Agent status;
- Capsule Service effective status;
- HealthStatus;
- reported status;
- stale state.

### 2.12 Node.js embedded Agent SDK

CE v0.1 must ship a Node.js embedded Agent SDK.

Required SDK capabilities:

- registration;
- Agent token persistence hook or guidance;
- heartbeat;
- manifest reporting;
- health provider;
- config provider;
- action definition registration;
- action handler registration;
- command polling;
- command result reporting;
- retry behavior when Backend is unavailable.

The SDK must not block the Capsule Service from starting if Opstage is unavailable.

### 2.13 Demo Capsule Service

CE v0.1 must include a demo Capsule Service.

The demo must prove:

- registration;
- manifest reporting;
- heartbeat;
- health reporting;
- config visibility;
- action execution;
- command polling;
- command result reporting;
- audit trail.

Required demo manifest:

```text
demo-capsule-service
runtime = nodejs
agentMode = embedded
```

### 2.14 SQLite persistence

CE v0.1 must support SQLite as the default database.

Required:

- SQLite schema;
- local data volume support;
- simple migration mechanism;
- schema designed to avoid obvious MySQL/PostgreSQL blockers.

### 2.15 Docker-based deployment

CE v0.1 must support a simple Docker-based local deployment.

Preferred target:

```bash
docker run -p 8080:8080 -v ./data:/app/data xtrape/capsule-opstage-ce
```

A Docker Compose example is also acceptable.

---

## 3. Optional in CE v0.1

The following items are optional. They may be implemented only if they do not delay the core loop.

### 3.1 Basic registration token UI

A UI page for creating registration tokens is useful, but a bootstrap CLI or setup screen is acceptable for v0.1.

### 3.2 Basic filters

Simple filters for Agents, Services, Commands, and Audit Logs are useful but not mandatory.

### 3.3 Basic config table extraction

Config items may be extracted into a separate table, but storing them in manifest JSON is acceptable for v0.1 if UI can display them.

### 3.4 Basic command detail page

A dedicated command detail page is useful but a command drawer or expandable row is acceptable.

### 3.5 Basic system settings

A basic settings page may show heartbeat timeout, command polling interval, and version information.

---

## 4. Explicitly Out of Scope

The following items are out of scope for CE v0.1.

### 4.1 Enterprise identity

Out of scope:

- SSO;
- OIDC;
- LDAP;
- SAML;
- enterprise RBAC;
- permission policy engine.

### 4.2 Cloud SaaS model

Out of scope:

- multi-tenancy;
- billing;
- subscriptions;
- hosted backend;
- customer organization model;
- tenant isolation;
- usage metering.

### 4.3 High availability and cluster deployment

Out of scope:

- backend cluster;
- database cluster;
- distributed locks;
- leader election;
- high availability deployment;
- Kubernetes operator.

### 4.4 Full observability stack

Out of scope:

- centralized log collection;
- log search;
- metrics dashboards;
- alert rules;
- tracing;
- Prometheus integration;
- Grafana dashboards.

### 4.5 Full configuration center

Out of scope:

- config publishing;
- config versioning;
- config rollback;
- config approval;
- environment promotion;
- feature flags.

### 4.6 Advanced Agent modes

Out of scope:

- sidecar Agent;
- external Agent;
- Java Agent SDK;
- Python Agent SDK;
- Kubernetes Agent;
- Docker host Agent.

### 4.7 Arbitrary remote execution

Out of scope and forbidden:

- generic shell command execution;
- arbitrary script execution from UI;
- unrestricted remote command terminal.

Only predefined actions are allowed.

---

## 5. Scope Boundaries by Component

### 5.1 Backend

Backend is in scope for:

- auth;
- Workspace defaulting;
- Agent registration;
- Agent token validation;
- heartbeat;
- service report;
- health storage;
- config metadata storage or extraction;
- action metadata storage;
- Command creation and polling;
- CommandResult reporting;
- audit storage;
- UI APIs.

Backend is not in scope for:

- business logic of Capsule Services;
- arbitrary command execution;
- enterprise identity;
- Cloud tenant billing;
- cluster orchestration.

### 5.2 UI

UI is in scope for:

- login;
- dashboard;
- Agent status;
- Capsule Service status;
- health display;
- config display;
- predefined action triggering;
- command result display;
- audit logs.

UI is not in scope for:

- workflow designer;
- advanced monitoring dashboard;
- log analysis console;
- multi-tenant admin;
- enterprise permission management.

### 5.3 Agent SDK

Agent SDK is in scope for:

- embedded Node.js integration;
- registration;
- heartbeat;
- manifest reporting;
- health/config/action providers;
- command polling;
- action execution;
- result reporting.

Agent SDK is not in scope for:

- sidecar mode;
- external process supervision;
- Java/Python runtime support;
- browser automation implementation itself;
- secret vault implementation.

### 5.4 Demo Capsule Service

Demo is in scope for proving the full CE loop.

Demo is not in scope for representing a production-grade CAPI implementation.

---

## 6. Required Data Objects

CE v0.1 should implement or represent at least:

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

These may be physical database tables or partially stored as JSON depending on implementation decisions.

Objects that should not be implemented as first-class CE v0.1 objects unless necessary:

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

## 7. Required APIs

CE v0.1 should include APIs in these groups.

### 7.1 Admin UI APIs

```text
POST /api/auth/login
POST /api/auth/logout
GET  /api/dashboard
GET  /api/agents
GET  /api/agents/{agentId}
GET  /api/capsule-services
GET  /api/capsule-services/{serviceId}
POST /api/capsule-services/{serviceId}/actions/{actionName}
GET  /api/commands
GET  /api/commands/{commandId}
GET  /api/audit-events
```

Exact paths may be adjusted, but the capability groups should exist.

### 7.2 Agent APIs

```text
POST /api/agents/register
POST /api/agents/{agentId}/heartbeat
POST /api/agents/{agentId}/services/report
GET  /api/agents/{agentId}/commands
POST /api/agents/{agentId}/commands/{commandId}/result
```

Agent APIs must require Agent token after registration.

---

## 8. Required UI Status Behavior

CE UI must not display stale services as confidently online.

Required behavior:

```text
Agent offline -> service stale
Health UP -> service online only if Agent is online and report is fresh
Health DEGRADED -> service unhealthy
Health DOWN -> service offline or unhealthy
```

Service detail should show:

```text
Effective Status
Reported Status
Health Status
Freshness
Agent Status
Last Heartbeat At
Last Reported At
Reason
```

---

## 9. Security Scope

CE v0.1 security scope includes:

- local admin authentication;
- Agent token authentication;
- token hash storage;
- Agent revocation or disablement model;
- sensitive value masking;
- no raw secrets in audit events;
- no arbitrary shell execution;
- action confirmation for high-risk actions if present.

CE v0.1 security scope does not include:

- full enterprise identity;
- SSO;
- advanced RBAC;
- secret vault;
- policy engine;
- compliance-grade audit immutability.

---

## 10. Acceptance Criteria

CE v0.1 scope is complete when the following scenario works end to end.

### 10.1 Startup

- Opstage Backend starts with SQLite.
- Opstage UI is accessible.
- Default Workspace exists.
- Admin user can log in.

### 10.2 Agent registration

- A registration token can be created or bootstrapped.
- Demo Capsule Service starts with Node.js embedded Agent SDK.
- Agent registers successfully.
- Backend issues Agent token.
- UI shows the Agent.

### 10.3 Service governance

- Agent reports demo Capsule Service manifest.
- UI shows the Capsule Service.
- UI shows manifest fields.
- UI shows health.
- UI shows configs.
- UI shows actions.

### 10.4 Action execution

- User triggers `echo` or `runHealthCheck`.
- Backend creates a Command.
- Agent polls the Command.
- Agent executes the local handler.
- Agent reports CommandResult.
- UI shows success or failure.
- Audit log records the operation.

### 10.5 Offline behavior

- When demo Agent stops, Backend eventually marks Agent as offline.
- Service becomes stale.
- UI shows stale status clearly.

### 10.6 Deployment

- The system can be run locally with SQLite.
- Docker or Docker Compose deployment works.

---

## 11. Summary

CE v0.1 scope is intentionally narrow.

It should implement the complete minimum governance loop:

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

Everything outside this loop should be treated as optional or future work unless explicitly required.
