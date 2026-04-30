# EE Observability

- Status: Planning
- Edition: EE
- Priority: Future
- Audience: architects, platform engineers, SRE teams, backend developers, DevOps engineers, AI coding agents

This document defines the planned observability capabilities for **Opstage EE / Enterprise Edition**.

Opstage EE is the future private commercial edition of the `xtrape-capsule` product family. Enterprise observability capabilities are not CE v0.1 implementation requirements.

---

## 1. Purpose

The purpose of this document is to define:

- how EE should extend CE health visibility;
- what observability data Opstage should own;
- what observability data should remain in external systems;
- how logs, metrics, health, traces, alerts, and dashboards may be integrated;
- how Agent and Capsule Service observability should be modeled;
- how audit differs from observability;
- which observability concepts CE should reserve without implementing EE complexity.

The key rule is:

> EE should integrate with enterprise observability systems and expose Capsule governance visibility, but it should not try to replace every observability platform.

---

## 2. Observability Goal

The goal of EE observability is:

> Help enterprise operators understand the runtime state, freshness, health, activity, and operational outcomes of Agents and Capsule Services.

EE observability should answer:

- Which Agents are online, offline, stale, or unhealthy?
- Which Capsule Services are healthy, degraded, down, or stale?
- Which Commands are pending, running, successful, failed, expired, or cancelled?
- Which actions fail frequently?
- Which services are becoming stale repeatedly?
- Which Agents are unstable or outdated?
- What operational events require alerting?
- Where should operators go for deeper logs, metrics, or traces?

---

## 3. EE Observability Is Not CE v0.1

CE v0.1 must not implement full EE observability capabilities.

Out of scope for CE v0.1:

- centralized log collection;
- log search platform;
- metrics database;
- Prometheus integration;
- Grafana dashboards;
- Loki / Elasticsearch integration;
- OpenTelemetry tracing;
- alert rule engine;
- notification routing;
- incident management integration;
- uptime history dashboards;
- long-term health history analytics;
- command analytics dashboards.

CE v0.1 should only provide:

- latest Agent heartbeat;
- latest Capsule Service health;
- effective status and freshness;
- command status and result;
- basic audit logs;
- simple backend application logs.

---

## 4. Relationship with CE

CE provides the observability kernel:

```text
Agent heartbeat
    ↓
Agent online/offline status
    ↓
Capsule Service report
    ↓
HealthStatus
    ↓
Effective service status
    ↓
Command status and result
    ↓
AuditEvent
```

EE should extend this kernel with:

```text
health history
Agent uptime history
command analytics
alert rules
notification channels
external log integration
external metric integration
trace integration
enterprise dashboards
```

EE must preserve the CE status and freshness model.

---

## 5. Observability Scope

Opstage EE should focus on **Capsule governance observability**.

In scope:

- Agent connectivity and heartbeat;
- Capsule Service health and freshness;
- manifest/report freshness;
- Command lifecycle;
- action execution result;
- config change/reload outcome if implemented;
- Agent version and protocol compatibility;
- operational errors from Agent communication;
- alerting on governance events;
- integration links to external logs/metrics/traces.

Out of primary scope:

- arbitrary application log storage;
- full distributed tracing platform;
- full metrics backend;
- full SIEM replacement;
- business analytics;
- customer business data analytics.

---

## 6. Observability Data Categories

EE observability data may include:

```text
AgentHeartbeat
AgentConnectionEvent
AgentStatusSnapshot
CapsuleServiceStatusSnapshot
HealthReport
CommandLifecycleEvent
ActionExecutionMetric
ConfigOperationMetric
AlertEvent
NotificationEvent
ExternalObservabilityLink
```

Not all of these need to be implemented early.

CE v0.1 should not implement these as separate first-class models unless required.

---

## 7. Agent Observability

Agent observability is central to Opstage.

### 7.1 Agent status

EE should show:

```text
AgentStatus
Connection status
Last heartbeat
Last service report
Last command poll
Last command result
Runtime
Agent version
SDK version
Protocol version
Hostname
OS
Architecture
```

### 7.2 Agent uptime history

Possible capabilities:

- uptime timeline;
- offline periods;
- reconnect count;
- heartbeat latency;
- heartbeat failure count;
- stale duration;
- Agent instability score.

### 7.3 Agent compatibility

EE may display warnings:

```text
Agent version outdated
Protocol version deprecated
Runtime unsupported
SDK feature missing
```

### 7.4 Agent diagnostics

Possible diagnostics:

- recent authentication failures;
- rejected command polls;
- service report errors;
- command result report failures;
- token expiration warning;
- revoked/disabled status.

---

## 8. Capsule Service Observability

Capsule Service observability focuses on managed service state.

### 8.1 Service status

EE should show:

```text
Effective Status
Reported Status
HealthStatus
FreshnessStatus
Last Reported At
Last Health At
Managing Agent
Reason
```

### 8.2 Health history

Possible capabilities:

- health status timeline;
- dependency health history;
- status transition history;
- stale duration;
- degraded duration;
- downtime summary;
- recurring failure summary.

### 8.3 Dependency health

HealthReport may include dependencies:

```text
name
type
status
message
latency
checkedAt
```

Example dependency types:

```text
database
cache
external-api
browser-session
account-pool
storage
queue
```

### 8.4 Service inventory changes

EE may track:

- first seen;
- last seen;
- version changes;
- manifest changes;
- action definition changes;
- config metadata changes;
- capability changes.

---

## 9. Command Observability

Commands are operational events and should be observable.

### 9.1 Command lifecycle

EE may track:

```text
CREATED
QUEUED
DISPATCHED
RUNNING
SUCCESS
FAILED
EXPIRED
CANCELLED
```

CE v0.1 may only need:

```text
PENDING
DISPATCHED
SUCCESS
FAILED
EXPIRED
```

### 9.2 Command metrics

Possible metrics:

- command count;
- success rate;
- failure rate;
- expiration rate;
- average dispatch latency;
- average execution duration;
- action-specific failure rate;
- service-specific command volume;
- user-triggered vs system-triggered commands.

### 9.3 Command timeline

Command detail may show:

```text
createdAt
dispatchedAt
startedAt
finishedAt
result reportedAt
```

### 9.4 Long-running command progress

Future EE may support progress updates.

Possible fields:

```text
progressPercent
progressMessage
lastProgressAt
```

This is not CE v0.1.

---

## 10. Action Observability

Actions are predefined operations exposed by Capsule Services.

EE may show:

- action execution count;
- action success/failure rate;
- average action duration;
- high-risk action history;
- action failure reasons;
- action usage by user;
- action usage by service;
- action approval outcomes if approval workflow exists.

Action observability should be linked to:

```text
Command
CommandResult
AuditEvent
ActionDefinition
```

---

## 11. Config Operation Observability

If EE implements config management, config operations should be observable.

Possible events:

- config edit requested;
- config approved;
- config published;
- config applied;
- config reload command created;
- config reload succeeded;
- config rollback executed;
- config drift detected.

Config operation observability should remain auditable and should not expose raw secrets.

---

## 12. Logs Strategy

EE should distinguish Opstage logs from Capsule Service logs.

### 12.1 Opstage application logs

Opstage Backend, UI server, workers, and schedulers may produce application logs.

These logs should support:

- startup diagnostics;
- API errors;
- Agent communication errors;
- command processing errors;
- database errors;
- integration errors.

### 12.2 Capsule Service logs

Capsule Service logs should usually remain in the customer's logging system.

EE may provide links or integrations rather than storing all logs directly.

### 12.3 Log integrations

Possible integrations:

```text
Loki
Elasticsearch
OpenSearch
Splunk
enterprise log platform
```

### 12.4 Log safety

Logs must not contain raw secrets:

```text
password
token
accessToken
refreshToken
cookie
apiKey
privateKey
credential
secret
```

### 12.5 CE relationship

CE v0.1 should only log to stdout/stderr and avoid centralized log collection.

---

## 13. Metrics Strategy

EE may expose or collect metrics.

### 13.1 Opstage internal metrics

Possible metrics:

```text
opstage_agent_heartbeat_total
opstage_agent_online_count
opstage_capsule_service_total
opstage_capsule_service_status_count
opstage_command_total
opstage_command_duration_seconds
opstage_command_failed_total
opstage_audit_event_total
opstage_api_request_total
opstage_api_request_duration_seconds
```

### 13.2 Agent and service governance metrics

Possible metrics:

- Agent online count;
- Agent offline count;
- service online count;
- service stale count;
- service unhealthy count;
- command success/failure rate;
- action execution duration;
- heartbeat latency;
- report freshness.

### 13.3 Metrics integrations

Possible integrations:

```text
Prometheus
OpenTelemetry Metrics
Grafana dashboards
enterprise metrics platform
```

### 13.4 CE relationship

CE v0.1 does not need Prometheus metrics.

A basic `/api/system/health` endpoint is enough.

---

## 14. Tracing Strategy

EE may integrate with tracing, but tracing should not be the first observability priority.

Possible tracing scope:

- Backend API request tracing;
- Agent API request tracing;
- command creation to result lifecycle correlation;
- external integration tracing;
- database query tracing.

Possible integrations:

```text
OpenTelemetry
Jaeger
Tempo
enterprise tracing platform
```

Capsule Service application traces should remain customer-controlled unless explicitly integrated.

---

## 15. Alerting Strategy

EE may provide alert rules for Capsule governance events.

### 15.1 Alert rule examples

Possible alert conditions:

```text
Agent offline for more than N minutes
Capsule Service stale for more than N minutes
HealthStatus DOWN
HealthStatus DEGRADED for more than N minutes
Command failed
Command failure rate above threshold
Command expired
Registration token used
Agent token revoked
High-risk action executed
```

### 15.2 Alert severity

Possible severities:

```text
INFO
WARNING
ERROR
CRITICAL
```

### 15.3 Alert lifecycle

Possible alert states:

```text
OPEN
ACKNOWLEDGED
RESOLVED
SUPPRESSED
```

### 15.4 Notification channels

Possible channels:

```text
email
webhook
Slack
Telegram
Microsoft Teams
PagerDuty
Opsgenie
enterprise incident system
```

### 15.5 CE relationship

CE v0.1 should not implement alert rules or notification routing.

---

## 16. Dashboard Strategy

EE may provide observability dashboards.

Possible dashboards:

```text
Agent Fleet Dashboard
Capsule Service Health Dashboard
Command Operations Dashboard
Action Reliability Dashboard
Audit Activity Dashboard
Workspace Operations Dashboard
```

Dashboards should be practical and operational, not decorative.

Recommended first EE dashboards:

- Agent fleet status;
- Capsule Service status;
- recent failed commands;
- stale services;
- high-risk actions.

---

## 17. External Observability Links

EE may store links to external observability systems.

Examples:

```text
service log search URL
service metric dashboard URL
trace search URL
runbook URL
incident URL
```

These links may be stored in:

- CapsuleService metadata;
- Agent metadata;
- ActionDefinition metadata;
- Workspace settings;
- integration settings.

This allows Opstage to become a governance entry point without owning every observability backend.

---

## 18. Retention Strategy

EE observability data may need retention policies.

Possible retention categories:

```text
HealthReport history
Command history
CommandResult history
Agent status snapshots
Alert events
Notification events
Metrics rollups
```

Retention should be configurable in EE.

CE v0.1 may keep simple data indefinitely or provide basic cleanup later.

---

## 19. Observability vs Audit

Observability and audit are related but different.

### 19.1 Observability

Observability answers:

```text
What is happening operationally?
Is the system healthy?
Where are failures occurring?
What needs attention?
```

### 19.2 Audit

Audit answers:

```text
Who did what?
When did it happen?
What resource was affected?
Was it allowed?
What was the result?
```

### 19.3 Design rule

Do not use AuditEvent as a general log or metrics store.

Do not use observability metrics as a replacement for audit records.

---

## 20. Data Boundary

EE observability must respect the data boundary.

Do not collect by default:

- raw secrets;
- raw cookies;
- raw OAuth tokens;
- private keys;
- customer business records;
- full browser traces;
- large application logs;
- sensitive payloads.

Use:

```text
secretRef
sanitized metadata
external links
summary metrics
```

where possible.

---

## 21. OpenTelemetry Direction

OpenTelemetry may be useful for EE.

Possible usage:

- instrument Opstage Backend;
- export metrics;
- export traces;
- correlate command lifecycle;
- integrate with customer's observability platform.

Recommended approach:

```text
Use OpenTelemetry as an integration standard where useful, but do not make it mandatory for CE v0.1.
```

---

## 22. CE Reservations

CE should reserve these observability-compatible concepts:

```text
Agent.lastHeartbeatAt
CapsuleService.lastReportedAt
CapsuleService.effectiveStatus
CapsuleService.healthStatus
HealthReport
Command
CommandResult
AuditEvent
metadataJson
status values
freshness calculation
```

CE should not implement:

```text
centralized logs
metrics backend
alert rule engine
notification routing
OpenTelemetry exporter
Grafana dashboards
health history analytics
command analytics dashboards
```

---

## 23. Anti-Patterns

Avoid these patterns.

### 23.1 Turning Opstage into a full observability replacement too early

Opstage should focus on Capsule governance visibility first.

### 23.2 Storing large logs in CommandResult

CommandResult should remain concise.

### 23.3 Using AuditEvent as a log database

Audit is for traceability, not general logging.

### 23.4 Showing stale services as healthy

Freshness must always be visible.

### 23.5 Collecting secrets in health or logs

Health, logs, and metrics must be sanitized.

### 23.6 Pulling EE observability into CE v0.1

CE should stay lightweight.

---

## 24. EE Observability MVP Candidate

A future EE observability MVP may include:

- Agent uptime history;
- Capsule Service health history;
- command success/failure metrics;
- stale service list;
- failed command list;
- simple alert rules;
- email or webhook notification;
- Prometheus metrics endpoint;
- basic Grafana dashboard template;
- external log dashboard links.

This is a candidate only and should be validated by real enterprise demand.

---

## 25. Long-Term Observability Capabilities

Long-term EE may include:

- OpenTelemetry integration;
- Loki / Elasticsearch integrations;
- advanced dashboards;
- alert routing and escalation;
- incident management integration;
- metrics rollups;
- command analytics;
- action reliability analytics;
- Agent fleet analytics;
- dependency health graph;
- service topology view;
- SIEM integration.

These should not be implemented before the core governance loop is stable.

---

## 26. Acceptance Criteria

EE observability planning is acceptable when:

- EE extends CE health and status visibility;
- Agent and service freshness are first-class;
- command and action outcomes are observable;
- logs, metrics, traces, alerts, and dashboards are clearly scoped;
- external observability integrations are preferred over replacing all systems;
- audit is clearly separated from observability;
- sensitive data boundaries are respected;
- CE v0.1 remains lightweight.

---

## 27. Summary

Opstage EE observability should make Capsule governance operationally understandable at enterprise scale.

The most important observability rule is:

> Observe the governance layer deeply, integrate with existing observability systems, and avoid turning Opstage into a general-purpose log, metric, and trace platform too early.
