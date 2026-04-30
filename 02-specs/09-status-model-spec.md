# Status Model Specification

- Status: Draft
- Edition: Shared
- Priority: High

本文件属于 `xtrape-capsule` 文档集。`xtrape-capsule` 是面向轻服务 / Capsule Service 的领域体系；`xtrape-capsule-opstage` 是该体系下的统一运行态治理平台。

当前实现重点是 CE 开源社区版。EE 私有化商业版与 Cloud SaaS 版属于未来规划，CE 需要保留扩展点，但不应在早期版本实现其完整能力。

## Scope

本规范是 CE / EE / Cloud 共享的长期契约。CE 可以只实现最小子集，但命名、状态、接口和数据结构应尽量保持向后兼容。

## Compatibility Rule

- CE v0.x 可以标记实验字段。
- 稳定字段不应随意破坏。
- EE / Cloud 可以扩展能力，但不应反向污染 CE MVP。

# Status Model Specification

- Status: Draft
- Edition: Shared
- Priority: High
- Audience: backend developers, frontend developers, agent SDK developers, AI coding agents

This document defines the shared **Status Model** for the `xtrape-capsule` domain.

Status values are used by Opstage Backend, Opstage UI, Agents, and Capsule Services to describe current state, reported state, effective state, health state, command state, token state, and freshness.

A consistent status model is required so that CE, EE, and Cloud can share the same mental model and avoid ambiguous UI behavior.

---

## 1. Purpose

The Status Model Specification defines:

- Agent status values;
- Capsule Service status values;
- Health status values;
- Command status values;
- Token status values;
- Audit result values;
- freshness status values;
- mapping rules between health, Agent status, and service status;
- CE v0.1 required subset;
- future extension rules.

This document should be used by:

- backend data model;
- backend status calculation logic;
- frontend status display;
- Agent SDK state reporting;
- audit and command handling.

---

## 2. Core Concepts

### 2.1 Reported Status

**Reported status** is the status reported by an Agent or Capsule Service.

Example:

```json
{
  "reportedStatus": "ONLINE"
}
```

Reported status may become stale if the Agent stops sending heartbeat.

### 2.2 Effective Status

**Effective status** is the status calculated by Opstage Backend based on reported status, Agent heartbeat freshness, disabled state, token state, and health report freshness.

Example:

```json
{
  "reportedStatus": "ONLINE",
  "effectiveStatus": "STALE",
  "reason": "Agent has not sent heartbeat for 15 minutes."
}
```

UI should primarily show effective status, while still making last reported status visible when useful.

### 2.3 Health Status

**Health status** describes operational health of a service or dependency.

Allowed values:

```text
UP
DOWN
DEGRADED
UNKNOWN
```

### 2.4 Freshness

**Freshness** describes whether a status or report is still current.

Example:

```text
FRESH
STALE
UNKNOWN
```

---

## 3. Status Naming Rules

Status values should be:

- uppercase;
- stable;
- explicit;
- reusable across backend, UI, and Agent SDK;
- not tied to a single UI color;
- not localized in stored data.

Good values:

```text
ONLINE
OFFLINE
STALE
DISABLED
REVOKED
```

Bad values:

```text
green
red
ok
bad
maybe
```

UI may localize labels, but stored and API values should remain stable English uppercase identifiers.

---

## 4. AgentStatus

AgentStatus describes the governance and connectivity state of an Agent.

Recommended full values:

```text
PENDING
REGISTERED
ONLINE
OFFLINE
DISABLED
REVOKED
ERROR
```

CE v0.1 required values:

```text
PENDING
ONLINE
OFFLINE
DISABLED
REVOKED
```

### 4.1 `PENDING`

A registration token or Agent record exists, but the Agent has not successfully registered yet.

### 4.2 `REGISTERED`

The Agent has registered before, but it is not currently known to be online.

CE v0.1 may skip this value and use `OFFLINE` after heartbeat timeout.

### 4.3 `ONLINE`

The Agent has sent a valid heartbeat within the online freshness window.

### 4.4 `OFFLINE`

The Agent has not sent a heartbeat within the offline threshold.

### 4.5 `DISABLED`

The Agent has been disabled by an administrator.

A disabled Agent may be re-enabled.

### 4.6 `REVOKED`

The Agent token is no longer trusted.

A revoked Agent must not communicate unless re-enrolled or issued a new trusted token.

### 4.7 `ERROR`

The Agent is in an error state reported by itself or detected by Backend.

CE v0.1 may not need this status.

---

## 5. CapsuleServiceStatus

CapsuleServiceStatus describes the governance-facing status of a Capsule Service.

Recommended values:

```text
UNKNOWN
ONLINE
UNHEALTHY
OFFLINE
STALE
DISABLED
REMOVED
```

CE v0.1 required values:

```text
UNKNOWN
ONLINE
UNHEALTHY
OFFLINE
STALE
DISABLED
```

### 5.1 `UNKNOWN`

Opstage cannot determine the service status.

Examples:

- service has never reported health;
- manifest exists but no heartbeat has been received;
- status calculation lacks enough information.

### 5.2 `ONLINE`

The service is currently considered available and healthy.

Typical condition:

```text
Agent ONLINE + Health UP
```

### 5.3 `UNHEALTHY`

The service is reachable or reported, but health is degraded or partially failed.

Typical condition:

```text
Agent ONLINE + Health DEGRADED
```

### 5.4 `OFFLINE`

The service is reported as unavailable while the Agent is still online, or health is clearly down.

Typical condition:

```text
Agent ONLINE + Health DOWN
```

### 5.5 `STALE`

The last known service status is no longer fresh because the Agent or health report is stale.

Typical condition:

```text
Agent OFFLINE + last reported service status exists
```

### 5.6 `DISABLED`

The service has been disabled administratively.

### 5.7 `REMOVED`

The service has been removed from governance.

CE v0.1 may not need this status.

---

## 6. HealthStatus

HealthStatus describes operational health.

Allowed values:

```text
UP
DOWN
DEGRADED
UNKNOWN
```

### 6.1 `UP`

The target is operationally healthy.

### 6.2 `DOWN`

The target is not operationally usable.

### 6.3 `DEGRADED`

The target is partially usable but has issues.

### 6.4 `UNKNOWN`

The health cannot be determined.

HealthStatus is defined in detail in:

```text
02-specs/04-health-spec.md
```

---

## 7. CommandStatus

CommandStatus describes the lifecycle state of a Command.

Allowed values:

```text
PENDING
DISPATCHED
RUNNING
SUCCESS
FAILED
EXPIRED
CANCELLED
```

CE v0.1 required values:

```text
PENDING
DISPATCHED
SUCCESS
FAILED
EXPIRED
```

### 7.1 `PENDING`

Command has been created and is waiting for Agent delivery.

### 7.2 `DISPATCHED`

Command has been delivered to Agent.

### 7.3 `RUNNING`

Agent has started executing the Command.

CE v0.1 may skip this status for short-running action commands.

### 7.4 `SUCCESS`

Command completed successfully.

### 7.5 `FAILED`

Command failed.

### 7.6 `EXPIRED`

Command expired before completion.

### 7.7 `CANCELLED`

Command was cancelled.

CE v0.1 does not need cancellation UI.

---

## 8. TokenStatus

TokenStatus describes the lifecycle of registration tokens and Agent tokens.

Allowed values:

```text
ACTIVE
USED
REVOKED
EXPIRED
```

### 8.1 `ACTIVE`

Token is valid and may be used.

### 8.2 `USED`

Registration token has already been used.

Usually applies to one-time registration tokens.

### 8.3 `REVOKED`

Token has been revoked and must not be accepted.

### 8.4 `EXPIRED`

Token is past its expiration time.

---

## 9. AuditResult

AuditResult describes the result of an audited operation.

Allowed values:

```text
SUCCESS
FAILED
DENIED
ERROR
PENDING
```

### 9.1 `SUCCESS`

Operation completed successfully.

### 9.2 `FAILED`

Operation attempted but failed in normal business or runtime flow.

### 9.3 `DENIED`

Operation was rejected by authorization or policy.

### 9.4 `ERROR`

Unexpected system error occurred.

### 9.5 `PENDING`

Operation was accepted but not completed yet.

---

## 10. FreshnessStatus

FreshnessStatus describes whether a report is still current.

Allowed values:

```text
FRESH
STALE
UNKNOWN
```

### 10.1 `FRESH`

Report is recent enough to be trusted as current.

### 10.2 `STALE`

Report exists but is too old to be treated as current.

### 10.3 `UNKNOWN`

Freshness cannot be determined.

---

## 11. Effective Status Calculation

Opstage Backend should calculate effective statuses rather than blindly showing reported statuses.

### 11.1 Agent effective status

Recommended CE v0.1 defaults:

```text
heartbeatIntervalSeconds = 30
agentOfflineThresholdSeconds = 90
```

Rule:

```text
if agent.status in [DISABLED, REVOKED]:
    effectiveStatus = agent.status
else if now - lastHeartbeatAt > agentOfflineThresholdSeconds:
    effectiveStatus = OFFLINE
else:
    effectiveStatus = ONLINE
```

### 11.2 Service effective status

Recommended mapping:

| Agent Effective Status | HealthStatus | Service Effective Status |
|---|---|---|
| ONLINE | UP | ONLINE |
| ONLINE | DEGRADED | UNHEALTHY |
| ONLINE | DOWN | OFFLINE |
| ONLINE | UNKNOWN | UNKNOWN |
| OFFLINE | any | STALE |
| DISABLED | any | STALE or DISABLED |
| REVOKED | any | STALE |

CE v0.1 recommended rule:

```text
if service is disabled:
    effectiveStatus = DISABLED
else if agent effective status == OFFLINE:
    effectiveStatus = STALE
else if agent effective status == REVOKED:
    effectiveStatus = STALE
else if health == UP:
    effectiveStatus = ONLINE
else if health == DEGRADED:
    effectiveStatus = UNHEALTHY
else if health == DOWN:
    effectiveStatus = OFFLINE
else:
    effectiveStatus = UNKNOWN
```

---

## 12. Last Reported vs Current Effective

UI should avoid showing stale data as current truth.

Recommended display model:

```json
{
  "reportedStatus": "ONLINE",
  "effectiveStatus": "STALE",
  "freshness": "STALE",
  "lastReportedAt": "2026-04-30T10:21:00Z",
  "reason": "Agent offline"
}
```

Recommended UI display:

```text
Current: Stale
Last reported: Online
Last reported at: 2026-04-30 10:21
Reason: Agent offline
```

Bad UI display:

```text
Online
```

when the Agent has been offline for hours.

---

## 13. Status Color Guidelines

Status values are not colors, but UI may use consistent color mapping.

Recommended mapping:

| Status | Suggested UI Meaning |
|---|---|
| ONLINE / UP / SUCCESS / ACTIVE / FRESH | positive |
| DEGRADED / UNHEALTHY / PENDING / DISPATCHED / RUNNING | warning or in-progress |
| OFFLINE / DOWN / FAILED / ERROR / EXPIRED / REVOKED | negative |
| STALE / UNKNOWN | neutral or warning |
| DISABLED / CANCELLED / USED | neutral |

Do not store color names in backend status fields.

---

## 14. Status Transition Rules

### 14.1 AgentStatus transitions

Recommended transitions:

```text
PENDING -> ONLINE
ONLINE -> OFFLINE
OFFLINE -> ONLINE
ONLINE -> DISABLED
OFFLINE -> DISABLED
DISABLED -> ONLINE
ONLINE -> REVOKED
OFFLINE -> REVOKED
DISABLED -> REVOKED
```

Invalid or discouraged transitions:

```text
REVOKED -> ONLINE
REVOKED -> DISABLED
```

A revoked Agent should require token rotation or re-enrollment.

### 14.2 CommandStatus transitions

Recommended transitions:

```text
PENDING -> DISPATCHED
PENDING -> EXPIRED
PENDING -> CANCELLED
DISPATCHED -> RUNNING
DISPATCHED -> SUCCESS
DISPATCHED -> FAILED
DISPATCHED -> EXPIRED
RUNNING -> SUCCESS
RUNNING -> FAILED
RUNNING -> EXPIRED
RUNNING -> CANCELLED
```

Terminal states:

```text
SUCCESS
FAILED
EXPIRED
CANCELLED
```

### 14.3 TokenStatus transitions

Recommended transitions:

```text
ACTIVE -> USED
ACTIVE -> REVOKED
ACTIVE -> EXPIRED
```

`USED`, `REVOKED`, and `EXPIRED` are terminal for registration tokens.

Agent tokens may support rotation in future versions.

---

## 15. CE v0.1 Required Status Sets

CE v0.1 must support at least the following status values.

### 15.1 AgentStatus

```text
PENDING
ONLINE
OFFLINE
DISABLED
REVOKED
```

### 15.2 CapsuleServiceStatus

```text
UNKNOWN
ONLINE
UNHEALTHY
OFFLINE
STALE
DISABLED
```

### 15.3 HealthStatus

```text
UP
DOWN
DEGRADED
UNKNOWN
```

### 15.4 CommandStatus

```text
PENDING
DISPATCHED
SUCCESS
FAILED
EXPIRED
```

### 15.5 TokenStatus

```text
ACTIVE
USED
REVOKED
EXPIRED
```

### 15.6 AuditResult

```text
SUCCESS
FAILED
DENIED
ERROR
PENDING
```

### 15.7 FreshnessStatus

```text
FRESH
STALE
UNKNOWN
```

---

## 16. Backend Requirements

CE v0.1 Backend should:

1. validate status values;
2. store reported status and effective status separately for Capsule Services;
3. calculate Agent offline status from heartbeat timeout;
4. calculate service stale status from Agent status;
5. avoid showing stale service reports as online;
6. expose status values clearly to UI;
7. keep status values stable and uppercase;
8. avoid storing UI colors as status.

---

## 17. Frontend Requirements

CE v0.1 UI should:

1. display effective status prominently;
2. show last reported status where useful;
3. show last heartbeat time;
4. show last reported time;
5. show stale reason if available;
6. distinguish Agent status from Capsule Service status;
7. distinguish HealthStatus from CapsuleServiceStatus;
8. avoid showing stale reports as fresh.

Recommended status fields to display on service detail page:

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

## 18. Agent SDK Requirements

CE v0.1 Agent SDK should:

1. report service status consistently;
2. report health status using allowed HealthStatus values;
3. continue retrying heartbeat after Backend failures;
4. avoid blocking service startup because Backend is unavailable;
5. avoid inventing custom status values outside the spec.

---

## 19. Compatibility Rules

- New status values may be added only with documentation.
- Existing stable values should not change meaning.
- UI should handle unknown future status values gracefully.
- Backend should reject invalid known-domain status values in CE v0.1 where validation is practical.
- EE and Cloud may add additional status values, but should preserve CE core values.

---

## 20. Anti-Patterns

Avoid these patterns.

### 20.1 Mixing health and service status

Do not use `UP` as CapsuleServiceStatus. Use `ONLINE` instead.

### 20.2 Showing reported status as current status

Do not show `reportedStatus` as current status without freshness calculation.

### 20.3 Using colors as status values

Do not store `green`, `yellow`, or `red` as status values.

### 20.4 Custom one-off statuses

Do not invent undocumented statuses such as `BAD`, `MAYBE`, or `PARTIAL_OK`.

### 20.5 Ignoring Agent state

Do not calculate service status without considering Agent status.

### 20.6 Treating disabled and revoked as the same

`DISABLED` is administrative and may be reversible.

`REVOKED` means trust has been removed.

---

## 21. Summary

The Status Model keeps Opstage, Agents, Capsule Services, and UI consistent.

The most important CE v0.1 rule is:

> Do not confuse reported status with effective status.

CE v0.1 should implement a simple but correct status model:

```text
Agent heartbeat
    ↓
Agent effective status
    ↓
Health report
    ↓
Capsule Service effective status
    ↓
UI display with freshness
```

This prevents stale or misleading operational views while keeping the system lightweight.