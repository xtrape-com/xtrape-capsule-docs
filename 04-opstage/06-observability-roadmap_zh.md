---
status: draft
audience: architects
stability: unstable
last_reviewed: 2026-05-05
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 06-observability-roadmap.md
翻译状态 / Translation Status: 已翻译 / Translated
生成时间 / Generated: 2026-05-01 09:28:54
================================================================================
注意 / Notes:
- 技术术语如 Capsule Service、Agent、Opstage 等保留英文或采用中英对照
- 代码块中的内容不翻译
- 文件路径和 URL 不翻译
- 保持原有的 Markdown 格式结构
================================================================================
-->

# Observability Roadmap

- Status: 实施指南
- Edition: 共享
- Priority: Medium
- Audience: architects, backend developers, frontend developers, agent SDK developers, platform engineers, SRE teams, AI coding agents

This document 定义 the **Observability Roadmap** for Opstage（运维舞台）.

Observability helps operators understand Agent（代理） status, Capsule Service（胶囊服务） health, freshness, Command outcomes,
and operational signals. In CE（社区版）, observability should remain lightweight. EE（企业版） and Cloud（云版） may extend
observability into history, alerting, dashboards, and integrations.

The current implementation focus is **Opstage（运维舞台） CE（社区版）**. EE（企业版） and Cloud（云版） observability capabilities are
future planning tracks and must not expand the CE（社区版） v0.1 implementation scope.

---

## 1. Purpose

The purpose of the Observability Roadmap is to define:

- what observability means for Opstage（运维舞台）;
- what CE（社区版） v0.1 must implement;
- what CE（社区版） v0.1 should not implement;
- how Agent（代理） and Capsule Service（胶囊服务） status should be visible;
- how health, freshness, Commands, and AuditEvents relate to observability;
- how logs, metrics, traces, alerts, and dashboards may evolve in EE（企业版） and Cloud（云版）;
- how to avoid turning CE（社区版） into a full observability platform too early.

The key rule is:

> CE（社区版） should make the governance loop visible; EE（企业版） and Cloud（云版） may make it observable at scale.

---

## 2. Observability Positioning

In Opstage（运维舞台）, observability means:

> The ability to understand the runtime governance state of Agents and Capsule Services.

Opstage（运维舞台） observability focuses on the governance layer:

```text
Agent connectivity
Capsule Service health
Freshness
Command lifecycle
Action results
Audit traceability
```

It does not initially mean:

- centralized application logs;
- full metrics platform;
- distributed tracing platform;
- full SIEM system;
- general-purpose observability replacement;
- Kubernetes observability dashboard.

---

## 3. Observability Questions

Opstage（运维舞台） should help operators answer these questions.

### 3.1 Agent（代理） questions

- Which Agents are registered?
- Which Agents are online?
- Which Agents are offline?
- When did an Agent（代理） last heartbeat?
- Which Capsule Services does an Agent（代理） report?
- Is an Agent（代理） disabled or revoked?

### 3.2 Capsule Service（胶囊服务） questions

- Which Capsule Services exist?
- Which services are healthy?
- Which services are unhealthy?
- Which services are stale?
- Which Agent（代理） manages each service?
- When was the service last reported?
- What health message did the service report?

### 3.3 Command questions

- Which Commands were created?
- Which Commands are pending, dispatched, successful, failed, or expired?
- What result did an action return?
- Which service and Agent（代理） were involved?
- When did the operation happen?

### 3.4 Audit questions

- Who requested an action?
- Which resource was affected?
- What was the result?
- What sanitized request/result details are available?

---

## 4. CE（社区版） Observability Scope

CE（社区版） v0.1 should implement lightweight governance observability.

Required CE（社区版） capabilities:

- Agent（代理） list with status;
- Agent（代理） detail with last heartbeat;
- Capsule Service（胶囊服务） list with effective status;
- Capsule Service（胶囊服务） detail with health and freshness;
- latest HealthReport display;
- config metadata display;
- action metadata display;
- Command list;
- Command detail;
- CommandResult display;
- AuditEvent list;
- basic dashboard summary;
- system health endpoint;
- structured backend logs to stdout/stderr.

CE（社区版） should provide enough visibility for a single-node self-hosted user to understand the runtime state.

---

## 5. CE（社区版） Observability Non-Goals

CE（社区版） v0.1 should not implement:

- centralized log collection;
- log search UI;
- metrics database;
- time-series database;
- Prometheus exporter requirement;
- Grafana dashboard requirement;
- OpenTelemetry tracing;
- alert rule engine;
- notification routing;
- incident management integration;
- uptime analytics;
- long-term health history analytics;
- command analytics dashboards;
- service topology graph;
- dependency graph;
- SIEM integration.

These are future EE（企业版） or Cloud（云版） capabilities.

---

## 6. Observability Data Types

Opstage（运维舞台） observability may involve several data types.

CE（社区版） should implement only the first set.

### 6.1 CE（社区版） data types

```text
Agent.lastHeartbeatAt
Agent.status
CapsuleService.effectiveStatus
CapsuleService.healthStatus
CapsuleService.lastReportedAt
CapsuleService.lastHealthAt
HealthReport latest
Command.status
CommandResult
AuditEvent
System health
```

### 6.2 Future EE（企业版）/Cloud（云版） data types

```text
AgentHeartbeat history
AgentConnectionEvent
AgentStatusSnapshot
CapsuleServiceStatusSnapshot
HealthReport history
CommandLifecycleEvent
ActionExecutionMetric
AlertEvent
NotificationEvent
ExternalObservabilityLink
MetricSample
TraceReference
```

CE（社区版） should not need the future data types in v0.1.

---

## 7. Agent（代理） Observability

CE（社区版） should show Agent（代理） runtime state clearly.

Recommended fields:

```text
Agent code
Agent name
Agent status
Agent mode
Runtime
Version
Hostname
OS
Architecture
Registered at
Last heartbeat at
```

Agent（代理） status should be calculated from:

```text
disabled/revoked state
lastHeartbeatAt
offline threshold
```

Recommended CE（社区版） status values:

```text
ONLINE
OFFLINE
DISABLED
REVOKED
UNKNOWN
```

Do not show an Agent（代理） as online if heartbeat is stale.

---

## 8. Capsule Service（胶囊服务） Observability

CE（社区版） should show Capsule Service（胶囊服务） status clearly.

Recommended fields:

```text
Service code
Service name
Runtime
Version
Managing Agent
Reported status
Health status
Effective status
Last reported at
Last health at
Freshness reason
```

The UI should make these concepts distinct:

```text
Reported Status
Health Status
Effective Status
Freshness
Agent Status
```

Important rule:

> A service with an offline Agent（代理） should not be shown as healthy simply because its last HealthReport was UP.

---

## 9. Health Observability

CE（社区版） should display the latest HealthReport.

Recommended fields:

```text
status
message
checkedAt
receivedAt
dependenciesJson
detailsJson
```

Recommended HealthStatus values:

```text
UP
DOWN
DEGRADED
UNKNOWN
```

Dependency health may include:

```text
name
type
status
message
```

CE（社区版） does not need long-term health history in v0.1.

---

## 10. Freshness Model

Freshness determines whether a status is still trustworthy.

Freshness may depend on:

```text
Agent.lastHeartbeatAt
CapsuleService.lastReportedAt
HealthReport.checkedAt
HealthReport.receivedAt
configured thresholds
```

Recommended freshness states:

```text
FRESH
STALE
UNKNOWN
```

Freshness should be visible in UI.

Example display:

```text
Effective Status: STALE
Last Health Status: UP
Reason: Agent heartbeat timeout
```

---

## 11. Command Observability

CE（社区版） should show Command state and result.

Recommended Command statuses:

```text
PENDING
DISPATCHED
SUCCESS
FAILED
EXPIRED
```

Future statuses may include:

```text
RUNNING
CANCELLED
```

CE（社区版） UI should show:

- Command target service;
- Command target Agent（代理）;
- action name;
- status;
- created time;
- dispatched time if available;
- finished time if available;
- result summary;
- error message if failed.

---

## 12. Action Result Observability

Action result visibility should be simple and safe.

CommandResult may include:

```text
status
outputText
errorMessage
resultJson
startedAt
finishedAt
reportedAt
```

Rules:

- keep result concise;
- do not store large logs;
- do not display raw secrets;
- show sanitized error messages;
- link CommandResult to related Command and AuditEvent.

---

## 13. Audit Observability

AuditEvents provide traceability, not operational telemetry.

CE（社区版） should show AuditEvents for important operations.

Recommended audit list columns:

```text
Time
Actor
Action
Resource
Result
Description
```

Audit detail may show:

```text
requestJson
resultJson
metadataJson
```

Audit is not a substitute for logs, metrics, or traces.

---

## 14. Dashboard Roadmap

CE（社区版） Dashboard should be simple.

Recommended CE（社区版） dashboard cards:

```text
Agents total
Agents online
Agents offline
Capsule Services total
Services online
Services unhealthy
Services stale
Recent Commands
Recent AuditEvents
```

Recommended CE（社区版） dashboard sections:

```text
Stale or unhealthy services
Recent failed Commands
Recent AuditEvents
```

CE（社区版） does not need advanced charts in v0.1.

---

## 15. Backend Logs

CE（社区版） Backend should produce structured application logs to stdout/stderr.

Logs should help developers diagnose:

- server startup;
- database connection;
- login failures;
- Agent（代理） registration;
- Agent（代理） API errors;
- service report errors;
- command processing errors;
- unexpected exceptions.

Logs must not include:

```text
password
registration token
Agent token
cookie
OAuth token
API key
private key
raw secret
```

CE（社区版） does not need a log search UI.

---

## 16. Agent（代理） Logs

CE（社区版） Agent（代理） SDK should log useful events:

- registration success;
- registration failure without token exposure;
- heartbeat failure;
- service report failure;
- command polling failure;
- action execution failure;
- command result reporting failure.

Agent（代理） logs must not include raw tokens or secrets.

Agent（代理） logs remain local to the Capsule Service（胶囊服务） runtime in CE（社区版）.

---

## 17. System Health Endpoint

CE（社区版） Backend should expose a system health endpoint.

Recommended endpoint:

```http
GET /api/system/health
```

Recommended response fields:

```text
status
version
database status
current time
```

Possible response:

```json
{
  "status": "UP",
  "version": "0.1.0",
  "database": "UP",
  "time": "2026-04-30T12:00:00Z"
}
```

Future EE（企业版） may add readiness and liveness endpoints.

---

## 18. Metrics Roadmap

CE（社区版） v0.1 does not need a metrics backend.

Future EE（企业版） may expose metrics such as:

```text
opstage_agent_online_count
opstage_agent_offline_count
opstage_capsule_service_total
opstage_capsule_service_status_count
opstage_command_total
opstage_command_failed_total
opstage_command_duration_seconds
opstage_audit_event_total
opstage_api_request_total
opstage_api_request_duration_seconds
```

Possible future integrations:

```text
Prometheus
OpenTelemetry Metrics
Grafana
enterprise metrics platform
```

---

## 19. Tracing Roadmap

CE（社区版） v0.1 does not need distributed tracing.

Future EE（企业版） may integrate with tracing for:

- Backend API requests;
- Agent（代理） API requests;
- command creation to result lifecycle;
- database calls;
- external integrations.

Possible future integrations:

```text
OpenTelemetry
Jaeger
Tempo
enterprise tracing platform
```

Tracing should not be required for CE（社区版）.

---

## 20. Alerting Roadmap

CE（社区版） v0.1 does not need alert rules.

Future EE（企业版）/Cloud（云版） may support alert conditions such as:

```text
Agent offline for more than N minutes
Capsule Service stale for more than N minutes
HealthStatus DOWN
HealthStatus DEGRADED
Command failed
Command expired
Command failure rate above threshold
Registration token used
High-risk action executed
```

Possible notification channels:

```text
email
webhook
Slack
Telegram
Microsoft Teams
PagerDuty
Opsgenie
```

Alerting should come after status and freshness are reliable.

---

## 21. External Observability Links

Future EE（企业版） may allow Capsule Services to report links to external observability systems.

Examples:

```text
log dashboard URL
metrics dashboard URL
trace search URL
runbook URL
incident response URL
```

These links may be stored in:

```text
CapsuleService.metadataJson
ActionDefinition.metadataJson
Workspace settings
```

This allows Opstage（运维舞台） to become a governance entry point without owning every observability backend.

CE（社区版） v0.1 does not need this feature.

---

## 22. Observability vs Audit

Observability and audit are different.

Observability answers:

```text
What is happening operationally?
Is the system healthy?
Where are failures occurring?
What needs attention?
```

Audit answers:

```text
Who did what?
When did it happen?
Which resource was affected?
What was the result?
```

设计 rule:

> Do not use AuditEvent as a general log, metric, or health history table.

---

## 23. Observability Data Boundary

Observability data must respect the data boundary.

Do not collect or display by default:

```text
raw passwords
raw cookies
raw OAuth tokens
raw API keys
private keys
account credentials
customer business records
large application logs
full browser traces
secret-bearing payloads
```

Use:

```text
secretRef
sanitized messages
summary status
external references
```

where needed.

---

## 24. Roadmap Phases

### 24.1 Phase 1 — CE（社区版） v0.1 Basic Visibility

Implement:

- dashboard summary;
- Agent（代理） status;
- Capsule Service（胶囊服务） effective status;
- latest HealthReport;
- Command status and result;
- AuditEvent list;
- system health endpoint;
- structured stdout logs.

### 24.2 Phase 2 — CE（社区版） Improvement

Possible later CE（社区版） improvements:

- simple health history;
- better dashboard filters;
- recent failures section;
- basic cleanup for old Commands;
- better error classification;
- more useful system info page.

### 24.3 Phase 3 — EE（企业版） Observability

Possible EE（企业版） capabilities:

- health history;
- Agent（代理） uptime history;
- command metrics;
- Prometheus endpoint;
- Grafana dashboard template;
- alert rules;
- webhook/email notifications;
- external log/metric links.

### 24.4 Phase 4 — Cloud（云版） Managed Observability

Possible Cloud（云版） capabilities:

- managed health history;
- managed audit retention;
- managed alerts;
- notification channels;
- usage metering;
- Cloud（云版） Agent（代理） Gateway diagnostics;
- multi-tenant dashboards;
- plan-based retention.

---

## 25. Future EE（企业版） Extensions

Future EE（企业版） may add:

- Prometheus metrics endpoint;
- OpenTelemetry integration;
- Grafana dashboards;
- Loki / Elasticsearch / OpenSearch links;
- health history;
- command analytics;
- alert rule engine;
- notification integrations;
- SIEM integration;
- deployment observability;
- HA component health.

These are not CE（社区版） v0.1 requirements.

---

## 26. Future Cloud（云版） Extensions

Future Cloud（云版） may add:

- Cloud（云版） Agent（代理） Gateway diagnostics;
- multi-tenant usage dashboards;
- plan-based retention;
- managed alerting;
- notification channels;
- Cloud（云版） support diagnostics;
- workspace-level observability;
- organization-level observability;
- billing-related usage metrics.

These are not CE（社区版） v0.1 requirements.

---

## 27. Anti-Patterns

Avoid these patterns.

### 27.1 Building a full observability platform in CE（社区版）

CE（社区版） should focus on governance visibility, not logs/metrics/traces replacement.

### 27.2 Showing stale services as healthy

Freshness must affect effective status.

### 27.3 Storing large logs in CommandResult

CommandResult should stay concise.

### 27.4 Using AuditEvent as a metrics table

Audit is traceability, not telemetry storage.

### 27.5 Exposing secrets in health, logs, or results

All observability surfaces must avoid raw secrets.

### 27.6 Adding alerts before status is reliable

Alerting should come after heartbeat, health, and freshness semantics are stable.

---

## 28. Acceptance Criteria

CE（社区版） observability is acceptable when:

- Dashboard shows basic summary;
- Agent（代理） list shows online/offline status;
- Agent（代理） detail shows last heartbeat;
- Capsule Service（胶囊服务） list shows effective status;
- stale services are visible as stale;
- service detail shows latest HealthReport;
- service detail shows config and action metadata;
- Command list shows command status;
- Command detail shows result;
- AuditEvent list shows meaningful governance operations;
- system health endpoint works;
- backend logs avoid raw secrets;
- Agent（代理） logs avoid raw tokens;
- CE（社区版） does not implement full logs, metrics, tracing, or alerting platform.

---

## 29. Summary

Opstage（运维舞台） observability should start with clear governance visibility in CE（社区版） and evolve into history, alerts, dashboards, and integrations in EE（企业版） and Cloud（云版）.

The most important observability roadmap rule is:

> First make the core governance state correct and visible; only then add history, metrics, alerts, and external observability integrations.
