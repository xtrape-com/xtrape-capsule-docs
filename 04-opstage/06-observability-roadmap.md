---
status: proposed
audience: architects
stability: evolving
last_reviewed: 2026-05-05
---

# Observability Roadmap

- Status: Implementation Guidance
- Edition: Shared
- Priority: Medium
- Audience: architects, backend developers, frontend developers, agent SDK developers, platform engineers, SRE teams, AI coding agents

This document defines the **Observability Roadmap** for Opstage.

Observability helps operators understand Agent status, Capsule Service health, freshness, Command outcomes, and
operational signals. In CE, observability should remain lightweight. EE and Cloud may extend observability into history,
alerting, dashboards, and integrations.

The current implementation focus is **Opstage CE**. EE and Cloud observability capabilities are future planning tracks and must not expand the CE v0.1 implementation scope.

---

## 1. Purpose

The purpose of the Observability Roadmap is to define:

- what observability means for Opstage;
- what CE v0.1 must implement;
- what CE v0.1 should not implement;
- how Agent and Capsule Service status should be visible;
- how health, freshness, Commands, and AuditEvents relate to observability;
- how logs, metrics, traces, alerts, and dashboards may evolve in EE and Cloud;
- how to avoid turning CE into a full observability platform too early.

The key rule is:

> CE should make the governance loop visible; EE and Cloud may make it observable at scale.

---

## 2. Observability Positioning

In Opstage, observability means:

> The ability to understand the runtime governance state of Agents and Capsule Services.

Opstage observability focuses on the governance layer:

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

Opstage should help operators answer these questions.

### 3.1 Agent questions

- Which Agents are registered?
- Which Agents are online?
- Which Agents are offline?
- When did an Agent last heartbeat?
- Which Capsule Services does an Agent report?
- Is an Agent disabled or revoked?

### 3.2 Capsule Service questions

- Which Capsule Services exist?
- Which services are healthy?
- Which services are unhealthy?
- Which services are stale?
- Which Agent manages each service?
- When was the service last reported?
- What health message did the service report?

### 3.3 Command questions

- Which Commands were created?
- Which Commands are pending, dispatched, successful, failed, or expired?
- What result did an action return?
- Which service and Agent were involved?
- When did the operation happen?

### 3.4 Audit questions

- Who requested an action?
- Which resource was affected?
- What was the result?
- What sanitized request/result details are available?

---

## 4. CE Observability Scope

CE v0.1 should implement lightweight governance observability.

Required CE capabilities:

- Agent list with status;
- Agent detail with last heartbeat;
- Capsule Service list with effective status;
- Capsule Service detail with health and freshness;
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

CE should provide enough visibility for a single-node self-hosted user to understand the runtime state.

---

## 5. CE Observability Non-Goals

CE v0.1 should not implement:

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

These are future EE or Cloud capabilities.

---

## 6. Observability Data Types

Opstage observability may involve several data types.

CE should implement only the first set.

### 6.1 CE data types

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

### 6.2 Future EE/Cloud data types

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

CE should not need the future data types in v0.1.

---

## 7. Agent Observability

CE should show Agent runtime state clearly.

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

Agent status should be calculated from:

```text
disabled/revoked state
lastHeartbeatAt
offline threshold
```

Recommended CE status values:

```text
ONLINE
OFFLINE
DISABLED
REVOKED
UNKNOWN
```

Do not show an Agent as online if heartbeat is stale.

---

## 8. Capsule Service Observability

CE should show Capsule Service status clearly.

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

> A service with an offline Agent should not be shown as healthy simply because its last HealthReport was UP.

---

## 9. Health Observability

CE should display the latest HealthReport.

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

CE does not need long-term health history in v0.1.

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

CE should show Command state and result.

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

CE UI should show:

- Command target service;
- Command target Agent;
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

CE should show AuditEvents for important operations.

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

CE Dashboard should be simple.

Recommended CE dashboard cards:

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

Recommended CE dashboard sections:

```text
Stale or unhealthy services
Recent failed Commands
Recent AuditEvents
```

CE does not need advanced charts in v0.1.

---

## 15. Backend Logs

CE Backend should produce structured application logs to stdout/stderr.

Logs should help developers diagnose:

- server startup;
- database connection;
- login failures;
- Agent registration;
- Agent API errors;
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

CE does not need a log search UI.

---

## 16. Agent Logs

CE Agent SDK should log useful events:

- registration success;
- registration failure without token exposure;
- heartbeat failure;
- service report failure;
- command polling failure;
- action execution failure;
- command result reporting failure.

Agent logs must not include raw tokens or secrets.

Agent logs remain local to the Capsule Service runtime in CE.

---

## 17. System Health Endpoint

CE Backend should expose a system health endpoint.

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

Future EE may add readiness and liveness endpoints.

---

## 18. Metrics Roadmap

CE v0.1 does not need a metrics backend.

Future EE may expose metrics such as:

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

CE v0.1 does not need distributed tracing.

Future EE may integrate with tracing for:

- Backend API requests;
- Agent API requests;
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

Tracing should not be required for CE.

---

## 20. Alerting Roadmap

CE v0.1 does not need alert rules.

Future EE/Cloud may support alert conditions such as:

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

Future EE may allow Capsule Services to report links to external observability systems.

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

This allows Opstage to become a governance entry point without owning every observability backend.

CE v0.1 does not need this feature.

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

Design rule:

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

### 24.1 Phase 1 — CE v0.1 Basic Visibility

Implement:

- dashboard summary;
- Agent status;
- Capsule Service effective status;
- latest HealthReport;
- Command status and result;
- AuditEvent list;
- system health endpoint;
- structured stdout logs.

### 24.2 Phase 2 — CE Improvement

Possible later CE improvements:

- simple health history;
- better dashboard filters;
- recent failures section;
- basic cleanup for old Commands;
- better error classification;
- more useful system info page.

### 24.3 Phase 3 — EE Observability

Possible EE capabilities:

- health history;
- Agent uptime history;
- command metrics;
- Prometheus endpoint;
- Grafana dashboard template;
- alert rules;
- webhook/email notifications;
- external log/metric links.

### 24.4 Phase 4 — Cloud Managed Observability

Possible Cloud capabilities:

- managed health history;
- managed audit retention;
- managed alerts;
- notification channels;
- usage metering;
- Cloud Agent Gateway diagnostics;
- multi-tenant dashboards;
- plan-based retention.

---

## 25. Future EE Extensions

Future EE may add:

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

These are not CE v0.1 requirements.

---

## 26. Future Cloud Extensions

Future Cloud may add:

- Cloud Agent Gateway diagnostics;
- multi-tenant usage dashboards;
- plan-based retention;
- managed alerting;
- notification channels;
- Cloud support diagnostics;
- workspace-level observability;
- organization-level observability;
- billing-related usage metrics.

These are not CE v0.1 requirements.

---

## 27. Anti-Patterns

Avoid these patterns.

### 27.1 Building a full observability platform in CE

CE should focus on governance visibility, not logs/metrics/traces replacement.

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

CE observability is acceptable when:

- Dashboard shows basic summary;
- Agent list shows online/offline status;
- Agent detail shows last heartbeat;
- Capsule Service list shows effective status;
- stale services are visible as stale;
- service detail shows latest HealthReport;
- service detail shows config and action metadata;
- Command list shows command status;
- Command detail shows result;
- AuditEvent list shows meaningful governance operations;
- system health endpoint works;
- backend logs avoid raw secrets;
- Agent logs avoid raw tokens;
- CE does not implement full logs, metrics, tracing, or alerting platform.

---

## 29. Summary

Opstage observability should start with clear governance visibility in CE and evolve into history, alerts, dashboards, and integrations in EE and Cloud.

The most important observability roadmap rule is:

> First make the core governance state correct and visible; only then add history, metrics, alerts, and external observability integrations.
