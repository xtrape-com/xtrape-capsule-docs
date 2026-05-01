<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 04-health-spec.md
翻译状态 / Translation Status: 已翻译 / Translated
生成时间 / Generated: 2026-05-01 09:28:53
================================================================================
注意 / Notes:
- 技术术语如 Capsule Service、Agent、Opstage 等保留英文或采用中英对照
- 代码块中的内容不翻译
- 文件路径和 URL 不翻译
- 保持原有的 Markdown 格式结构
================================================================================
-->

# Health 规范

- Status: 规范
- Edition: 共享
- Priority: 高
- Audience: backend developers, frontend developers, agent SDK developers, Capsule Service（胶囊服务） developers, AI coding agents

> **Precedence rule**: When this document and `09-contracts/openapi/opstage-ce-v0.1.yaml` (`HealthStatus`, `HealthReport`, `HealthReportInput`) disagree, the OpenAPI contract wins for CE（社区版） v0.1.

This document 定义 the **Health** specification for the `xtrape-capsule` domain.

Health 描述 the current operational condition of an Agent（代理）, a Capsule Service（胶囊服务）, or a dependency reported by a Capsule Service（胶囊服务）.

Health is one of the core signals used by Opstage（运维舞台） to calculate service visibility, stale state, and operator-facing status.

---

## 1. Purpose

The Health 规范 定义:

- health status values;
- health report structure;
- dependency health structure;
- how Agents report health;
- how Backend stores health;
- how UI displays health;
- how health interacts with Agent（代理） heartbeat;
- how stale status should be calculated;
- what CE（社区版） v0.1 must implement;
- what EE（企业版） and Cloud（云版） may extend later.

Health is not a full observability system. CE（社区版） v0.1 should implement simple health visibility, not a complete metrics, tracing, or logging platform.

---

## 2. Core Concepts

### 2.1 Health

**Health** indicates whether a target is operationally usable at a given time.

A target may be:

- an Agent（代理）;
- a Capsule Service（胶囊服务）;
- a dependency of a Capsule Service（胶囊服务）;
- a future resource or instance.

### 2.2 HealthReport

A **HealthReport** is a timestamped health payload reported by an Agent（代理） or provided by a Capsule Service（胶囊服务）.

### 2.3 DependencyHealth

A **DependencyHealth** 描述 the health of an internal or external dependency that affects a Capsule Service（胶囊服务）.

Examples:

- database;
- browser runtime;
- queue;
- external API;
- local file directory;
- proxy node;
- account/session pool.

### 2.4 Reported status vs effective status

Health reports are raw reported facts.

Opstage（运维舞台） Backend may calculate an effective service status by combining:

- Agent（代理） status;
- last heartbeat time;
- latest health report;
- stale threshold;
- service disabled state.

---

## 3. Health 状态 Values

Allowed health status values:

```text
UP
DOWN
DEGRADED
UNKNOWN
```

### 3.1 `UP`

The target is operationally healthy.

Examples:

- service can process requests;
- worker is running normally;
- dependency is reachable;
- no known critical issue.

### 3.2 `DOWN`

The target is not operationally usable.

Examples:

- process is stopped;
- dependency is unreachable;
- required browser runtime is unavailable;
- critical initialization failed.

### 3.3 `DEGRADED`

The target is partially usable but has non-critical or partial failures.

Examples:

- service is running but one dependency is slow;
- some accounts are limited but others are usable;
- queue is delayed but still processing;
- provider has increased error rate.

### 3.4 `UNKNOWN`

The current health cannot be determined.

Examples:

- service has never reported health;
- Agent（代理） is offline and last health is stale;
- health provider failed without a clear result;
- no health provider is configured.

---

## 4. HealthReport Structure

### 4.1 Minimum CE（社区版） v0.1 HealthReport

```json
{
  "status": "UP",
  "checkedAt": "2026-04-30T10:21:00Z",
  "details": {}
}
```

### 4.2 Recommended HealthReport

```json
{
  "status": "DEGRADED",
  "checkedAt": "2026-04-30T10:21:00Z",
  "message": "Service is running but browser queue is delayed.",
  "details": {
    "activeSessions": 5,
    "queueSize": 18
  },
  "dependencies": [
    {
      "name": "database",
      "type": "sqlite",
      "status": "UP",
      "message": "Database is reachable."
    },
    {
      "name": "browser",
      "type": "local-runtime",
      "status": "DEGRADED",
      "message": "Browser is running but queue is delayed."
    }
  ]
}
```

---

## 5. HealthReport Fields

### 5.1 `status`

Required.

Allowed values:

```text
UP
DOWN
DEGRADED
UNKNOWN
```

### 5.2 `checkedAt`

Optional but recommended.

ISO-8601 timestamp indicating when the health check was performed.

If missing, Backend may use the receive time.

### 5.3 `message`

Optional human-readable summary.

Examples:

```text
Service is healthy.
Database is unavailable.
Browser runtime is degraded.
```

### 5.4 `details`

Optional structured object for additional health details.

Examples:

```json
{
  "activeSessions": 5,
  "queueSize": 18,
  "lastSuccessfulRunAt": "2026-04-30T10:20:00Z"
}
```

CE（社区版） v0.1 may store this as JSON without deep interpretation.

### 5.5 `dependencies`

Optional list of dependency health objects.

Each dependency should follow the DependencyHealth structure.

---

## 6. DependencyHealth Structure

Recommended shape:

```json
{
  "name": "database",
  "type": "sqlite",
  "status": "UP",
  "message": "Database is reachable.",
  "details": {}
}
```

### 6.1 `name`

Required.

Stable dependency name within the Capsule Service（胶囊服务）.

Examples:

```text
database
browser
queue
proxy
providerApi
accountPool
```

### 6.2 `type`

Optional dependency type.

Examples:

```text
sqlite
mysql
postgresql
redis
browser
queue
http-api
local-file
proxy
custom
```

### 6.3 `status`

Required.

Uses the same HealthStatus values:

```text
UP
DOWN
DEGRADED
UNKNOWN
```

### 6.4 `message`

Optional human-readable dependency status message.

### 6.5 `details`

Optional structured dependency-specific details.

---

## 7. Health Provider

In embedded Agent（代理） mode, the Capsule Service（胶囊服务） 提供 a health provider to the Agent（代理） SDK.

Recommended TypeScript shape:

```ts
export type HealthProvider = () => Promise<CapsuleHealthReport> | CapsuleHealthReport;

export interface CapsuleHealthReport {
  status: 'UP' | 'DOWN' | 'DEGRADED' | 'UNKNOWN';
  checkedAt?: string;
  message?: string;
  details?: Record<string, unknown>;
  dependencies?: DependencyHealth[];
}

export interface DependencyHealth {
  name: string;
  type?: string;
  status: 'UP' | 'DOWN' | 'DEGRADED' | 'UNKNOWN';
  message?: string;
  details?: Record<string, unknown>;
}
```

CE（社区版） v0.1 Node.js embedded Agent（代理） SDK should support a health provider with this shape or an equivalent shape.

---

## 8. Health Reporting

Health may be reported in two ways.

### 8.1 Heartbeat with health

Agent（代理） 包括 service health in heartbeat payload.

Example:

```json
{
  "timestamp": "2026-04-30T10:21:00Z",
  "services": [
    {
      "code": "demo-capsule-service",
      "reportedStatus": "ONLINE",
      "health": {
        "status": "UP",
        "checkedAt": "2026-04-30T10:21:00Z",
        "details": {}
      }
    }
  ]
}
```

### 8.2 Dedicated health report

Agent（代理） may report health separately.

Future endpoint:

```http
POST /api/agents/{agentId}/services/{serviceId}/health
Authorization: Bearer <agentToken>
```

CE（社区版） v0.1 may use heartbeat with health to keep implementation simple.

---

## 9. Health Storage

CE（社区版） v0.1 Backend should store at least the latest health state for each Capsule Service（胶囊服务）.

Recommended fields:

```text
id
workspaceId
serviceId
agentId
status
message
detailsJson
dependenciesJson
checkedAt
receivedAt
createdAt
```

CE（社区版） v0.1 may store only recent health history or latest health snapshot.

Long-term retention, aggregation, and charting are EE（企业版）/Cloud（云版） observability features.

---

## 10. Health and Service 状态

HealthStatus is not the same as CapsuleServiceStatus.

### 10.1 HealthStatus

HealthStatus is the reported operational health:

```text
UP
DOWN
DEGRADED
UNKNOWN
```

### 10.2 CapsuleServiceStatus

CapsuleServiceStatus is the effective governance-facing service status:

```text
UNKNOWN
ONLINE
UNHEALTHY
OFFLINE
STALE
DISABLED
```

### 10.3 Mapping guidance

Recommended mapping:

||Agent（代理） 状态|HealthStatus|Effective Service 状态||
|---|---|---|
||ONLINE|UP|ONLINE||
||ONLINE|DEGRADED|UNHEALTHY||
||ONLINE|DOWN|OFFLINE or UNHEALTHY||
||ONLINE|UNKNOWN|UNKNOWN||
||OFFLINE|any last health|STALE||
||REVOKED|any last health|STALE or DISABLED||
||DISABLED|any last health|DISABLED||

CE（社区版） v0.1 should implement at least:

```text
Agent ONLINE + health UP        -> service ONLINE
Agent ONLINE + health DEGRADED  -> service UNHEALTHY
Agent ONLINE + health DOWN      -> service OFFLINE
Agent OFFLINE                   -> service STALE
```

---

## 11. 状态 Freshness

Health reports become stale after a timeout.

Required CE（社区版） v0.1 defaults:

```text
heartbeatIntervalSeconds = 30
agentOfflineThresholdSeconds = 90
healthStaleThresholdSeconds = 120
```

Threshold relationship:

```text
agentOfflineThresholdSeconds (90s) < healthStaleThresholdSeconds (120s)
```

This creates a deliberate 30-second grace window (90–120s): an Agent（代理） that has just gone OFFLINE will have its Agent（代理） status set to OFFLINE first, but its last health report is still considered FRESH until 120s passes. This avoids a race condition where a momentary Agent（代理） dropout causes the health display to show STALE immediately.

During the 90–120s window, `effectiveStatus` is STALE (driven by Agent（代理） OFFLINE), but `freshness` is still FRESH. After 120s, both are STALE.

If health is older than the stale threshold, UI MUST display it as stale.

Example stale representation:

```json
{
  "healthStatus": "UP",
  "freshness": "STALE",
  "checkedAt": "2026-04-30T10:21:00Z",
  "reason": "Health report is older than stale threshold."
}
```

Do not show stale health as confidently fresh.

---

## 12. UI Requirements

CE（社区版） v0.1 UI should display:

- service health status;
- effective service status;
- last checked time;
- last heartbeat time if relevant;
- stale indicator;
- dependency health if available;
- health details JSON if available.

Recommended UI labels:

```text
Healthy
Degraded
Down
Unknown
Stale
```

UI should distinguish:

```text
Last reported: UP
Current: STALE
Reason: Agent offline
```

---

## 13. Backend Requirements

CE（社区版） v0.1 Backend should:

1. accept health payloads from Agent（代理） heartbeat;
2. validate health status values;
3. store latest health report;
4. update Capsule Service（胶囊服务） effective status;
5. expose health state to UI;
6. calculate stale status based on heartbeat and health timestamps;
7. avoid treating stale reports as fresh.

---

## 14. Agent（代理） SDK Requirements

CE（社区版） v0.1 Node.js embedded Agent（代理） SDK should:

1. allow registering a health provider;
2. call the health provider periodically or during heartbeat;
3. catch health provider errors;
4. report `UNKNOWN` or `DOWN` if health provider fails, depending on error type;
5. include health payload in heartbeat or service report;
6. avoid blocking core service startup if health reporting fails.

### 14.1 Health provider error behavior

If the health provider throws an error, the Agent（代理） SDK should report:

```json
{
  "status": "UNKNOWN",
  "message": "Health provider failed.",
  "details": {
    "error": "..."
  }
}
```

If the Capsule Service（胶囊服务） explicitly knows it is unusable, it should report:

```json
{
  "status": "DOWN",
  "message": "Required dependency is unavailable."
}
```

---

## 15. Health Endpoint for Future Modes

For sidecar or external Agent（代理） modes, a Capsule Service（胶囊服务） may expose:

```http
GET /_capsule/health
```

Response:

```json
{
  "status": "UP",
  "checkedAt": "2026-04-30T10:21:00Z",
  "details": {},
  "dependencies": []
}
```

This endpoint is not required for CE（社区版） v0.1 embedded Agent（代理） mode.

---

## 16. Health vs Metrics

Health is not metrics.

Health answers:

```text
Is the service operationally usable right now?
```

Metrics answer:

```text
How much, how fast, how often, how many, how long?
```

Examples of metrics:

```text
request_count
error_rate
queue_size
latency_ms
active_sessions
```

CE（社区版） v0.1 should not build a full metrics system.

EE（企业版）/Cloud（云版） may add metrics collection and dashboarding later.

---

## 17. Health vs Logs

Health is not logs.

Health is a compact status signal.

Logs are event streams or diagnostic records.

CE（社区版） v0.1 may show health details but does not need centralized log collection.

---

## 18. 安全 Rules

### 18.1 Do not expose sensitive details

Health details must not expose raw passwords, tokens, cookies, credentials, or private session data.

Bad:

```json
{
  "details": {
    "cookie": "raw-cookie-value"
  }
}
```

Good:

```json
{
  "details": {
    "sessionStore": "available",
    "activeSessionCount": 3
  }
}
```

### 18.2 Avoid leaking internal file paths unnecessarily

Health details should not expose sensitive local paths unless required for debugging.

### 18.3 Do not treat health as authorization

Health status is operational information. It must not be used as a security permission decision by itself.

---

## 19. Compatibility Rules

- New optional fields may be added to HealthReport.
- Unknown fields should be ignored by older clients.
- Health status values should remain stable.
- CE（社区版） may implement only latest-health storage.
- EE（企业版）/Cloud（云版） may add history, aggregation, alerting, and dashboards without changing the basic HealthReport contract.

---

## 20. CE（社区版） v0.1 Required Subset

CE（社区版） v0.1 must support:

- health provider in Node.js embedded Agent（代理） SDK;
- health payload in heartbeat or service report;
- health status validation;
- latest health storage;
- health display in UI;
- stale status calculation;
- dependency details display if provided.

CE（社区版） v0.1 does not need to support:

- full metrics collection;
- health history charts;
- alert rules;
- log correlation;
- distributed tracing;
- synthetic checks;
- external monitoring integrations;
- Prometheus exporter.

---

## 21. Example CE（社区版） v0.1 Health Flow

```text
Capsule Service provides health provider
    ↓
Agent calls health provider during heartbeat
    ↓
Agent sends health payload to Backend
    ↓
Backend validates and stores latest health
    ↓
Backend updates service effective status
    ↓
UI displays health and freshness
```

Example heartbeat health payload:

```json
{
  "services": [
    {
      "code": "demo-capsule-service",
      "reportedStatus": "ONLINE",
      "health": {
        "status": "UP",
        "checkedAt": "2026-04-30T10:21:00Z",
        "message": "Service is healthy.",
        "details": {
          "uptimeSeconds": 120
        }
      }
    }
  ]
}
```

---

## 22. Anti-Patterns

Avoid these patterns.

### 22.1 Showing stale health as fresh

Do not show old health reports as current.

### 22.2 Treating health as metrics

Do not overload health with large time-series data.

### 22.3 Putting logs into health details

Do not put large logs in health reports.

### 22.4 Leaking secrets in health details

Do not include raw credentials, cookies, tokens, or private account data.

### 22.5 Blocking service startup because health reporting fails

A failed health report should not prevent the Capsule Service（胶囊服务） from starting.

---

## 23. Summary

Health is the compact operational signal of a Capsule Service（胶囊服务）.

CE（社区版） v0.1 should implement a simple but correct health loop:

```text
HealthProvider
    ↓
Agent heartbeat
    ↓
Backend latest health storage
    ↓
Effective service status calculation
    ↓
UI display with freshness
```

This 提供 useful runtime visibility without turning CE（社区版） into a full observability platform.
