---
status: accepted
audience: architects
stability: evolving
last_reviewed: 2026-05-05
---

# Status Model Specification

- Status: Specification
- Edition: Shared
- Priority: High
- Audience: backend developers, frontend developers, agent SDK developers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/` (OpenAPI / Prisma) disagree, the ADRs and contracts win for CE v0.1.

This document defines the shared **Status Model** for the `xtrape-capsule` domain.

Status values are used by Opstage Backend, Opstage UI, Agents, and Capsule Services to describe current state, reported
state, effective state, health state, command state, token state, and freshness.

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

### 2.1 Reported State

**Reported state** is what an Agent last sent: `HealthStatus` from the latest `HealthReport`, plus `lastReportedAt` and
`lastHealthAt` timestamps. CE v0.1 does not persist a separate `reportedStatus` column; reported state is derived from
the latest stored `HealthReport` row.

### 2.2 Effective Status

**Effective status** is the status calculated by Opstage Backend based on Agent heartbeat freshness, Agent
disabled/revoked state, and the latest health report. CE v0.1 stores this on `CapsuleService.status`.

Example response (matches OpenAPI `CapsuleService` + `HealthReport`):

```json
{
  "id": "svc_001",
  "status": "STALE",
  "healthStatus": "UP",
  "lastReportedAt": "2026-04-30T10:21:00Z",
  "lastHealthAt": "2026-04-30T10:21:00Z"
}
```

UI should primarily show `status` (effective), while still surfacing `healthStatus` and timestamps so the operator can see the last known reported state.

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

CE v0.1 required values (must match OpenAPI `AgentStatus`):

```text
PENDING
ONLINE
OFFLINE
DISABLED
REVOKED
```

`REGISTERED` and `ERROR` are reserved for future EE/Cloud editions and are not part of CE v0.1.

### 4.1 `PENDING`

A registration token or Agent record exists, but the Agent has not successfully registered yet.

### 4.2 `ONLINE`

The Agent has sent a valid heartbeat within the offline threshold.

### 4.3 `OFFLINE`

The Agent has not sent a heartbeat within the offline threshold (default 90s — see ADR 0001 §Defaults).

### 4.4 `DISABLED`

The Agent has been disabled by an administrator. A disabled Agent may be re-enabled.

### 4.5 `REVOKED`

The Agent token is no longer trusted. A revoked Agent must not communicate unless re-enrolled with a new registration token.

---

## 5. CapsuleServiceStatus

CapsuleServiceStatus describes the governance-facing status of a Capsule Service.

CE v0.1 required values (must match OpenAPI `CapsuleServiceStatus`):

```text
UNKNOWN
HEALTHY
UNHEALTHY
STALE
OFFLINE
```

`DISABLED` and `REMOVED` are reserved for future EE/Cloud editions and are not part of CE v0.1.

### 5.1 `UNKNOWN`

Opstage cannot determine the service status.

Examples:

- service has never reported health;
- manifest exists but no heartbeat has been received;
- status calculation lacks enough information.

### 5.2 `HEALTHY`

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

The service is reported as unavailable, or its health is clearly DOWN, while the Agent is still online.

Typical condition:

```text
Agent ONLINE + Health DOWN
```

### 5.5 `STALE`

The last known service status is no longer fresh because the Agent is offline or health reports stopped arriving.

Typical condition:

```text
Agent OFFLINE + last reported service status exists
```

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

CE v0.1 required values (must match OpenAPI `CommandStatus`):

```text
PENDING
RUNNING
SUCCEEDED
FAILED
EXPIRED
CANCELLED
```

CE v0.1 may not implement cancellation UI, but the state is reserved.

### 7.1 `PENDING`

Command has been created and is waiting for Agent polling.

### 7.2 `RUNNING`

Agent has polled the Command and Backend has transitioned the row to RUNNING (with `startedAt` set). The Agent SDK is or is about to be executing the local handler.

### 7.3 `SUCCEEDED`

Command completed successfully (Agent reported `success = true`).

### 7.4 `FAILED`

Command execution failed (Agent reported `success = false`).

### 7.5 `EXPIRED`

Command expired before completion (`now > expiresAt`).

### 7.6 `CANCELLED`

Command was cancelled. Reserved for future use; CE v0.1 does not expose cancellation in UI.

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

CE v0.1 required values (must match OpenAPI `AuditResult`):

```text
SUCCESS
FAILURE
```

`DENIED`, `ERROR`, and `PENDING` are reserved for future EE/Cloud editions and are not part of CE v0.1. CE
implementations should map authorization rejections and unexpected errors to `FAILURE` with a descriptive `message`.

### 9.1 `SUCCESS`

Operation completed successfully.

### 9.2 `FAILURE`

Operation failed for any reason (validation rejection, business error, authorization denial, runtime exception). The
`message` field and `metadata.errorCode` carry the specific reason.

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
| ONLINE | UP | HEALTHY |
| ONLINE | DEGRADED | UNHEALTHY |
| ONLINE | DOWN | OFFLINE |
| ONLINE | UNKNOWN | UNKNOWN |
| OFFLINE | any | STALE |
| DISABLED | any | STALE |
| REVOKED | any | STALE |

CE v0.1 required rule:

```text
if agent effective status in [DISABLED, REVOKED, OFFLINE]:
    effectiveStatus = STALE
else if health == UP:
    effectiveStatus = HEALTHY
else if health == DEGRADED:
    effectiveStatus = UNHEALTHY
else if health == DOWN:
    effectiveStatus = OFFLINE
else:
    effectiveStatus = UNKNOWN
```

Note: CE v0.1 does not implement service-level `DISABLED`. EE/Cloud may add it later.

Calculation timing: Backend MUST recalculate `effectiveStatus` on every heartbeat receipt and on every explicit status change (disable, revoke). The Backend MAY also run a background sweep (recommended interval: every 30 seconds) to transition agents that have missed heartbeats to OFFLINE and mark their services as STALE.

FreshnessStatus enum values:

```text
FRESH  — last report is within healthStaleThresholdSeconds
STALE  — last report exceeds healthStaleThresholdSeconds
```

---

## 12. Last Reported vs Current Effective

UI should avoid showing stale data as current truth.

CE v0.1 persists only the **effective** status on `CapsuleService.status`. The "last reported" view is derived from
`lastReportedAt` + `lastHealthAt` + the latest `HealthReport` row, not stored in a separate column.

Recommended UI display:

```text
Current: Stale
Health: Up        (from latest HealthReport)
Last reported at: 2026-04-30 10:21
Reason: Agent offline since 10:22
```

Bad UI display:

```text
Healthy
```

when the Agent has been offline for hours and `effectiveStatus` is `STALE`.

---

## 13. Status Color Guidelines

Status values are not colors, but UI may use consistent color mapping.

Recommended mapping:

| Status | Suggested UI Meaning |
|---|---|
| HEALTHY / ONLINE / UP / SUCCEEDED / SUCCESS / ACTIVE / FRESH | positive |
| DEGRADED / UNHEALTHY / PENDING / RUNNING | warning or in-progress |
| OFFLINE / DOWN / FAILED / FAILURE / EXPIRED / REVOKED | negative |
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

CE v0.1 transitions:

```text
PENDING -> RUNNING       (Agent polled the Command)
PENDING -> EXPIRED       (timeout reached before delivery)
PENDING -> CANCELLED     (reserved for future use)
RUNNING -> SUCCEEDED     (Agent reported success)
RUNNING -> FAILED        (Agent reported failure)
RUNNING -> EXPIRED       (timeout reached during execution)
RUNNING -> CANCELLED     (reserved for future use)
```

Terminal states:

```text
SUCCEEDED
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
HEALTHY
UNHEALTHY
STALE
OFFLINE
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
RUNNING
SUCCEEDED
FAILED
EXPIRED
CANCELLED   (reserved, no UI required)
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

1. validate status values against the enums above;
2. persist only the **effective** `CapsuleService.status` (the last reported state is reconstructed from `lastReportedAt` + the latest `HealthReport` row, see §12);
3. calculate Agent offline status from heartbeat timeout (default 90s — see ADR 0001 §Defaults);
4. calculate service `STALE` status from Agent status;
5. never expose stale service reports as `HEALTHY`;
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
Effective Status (CapsuleService.status)
Health Status    (latest HealthReport.status)
Freshness        (derived from lastHealthAt and lastReportedAt)
Agent Status     (Agent.status, also derived from lastHeartbeatAt)
Last Heartbeat At
Last Reported At
Reason           (e.g. "Agent offline since 10:22")
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

Do not use `UP` (a `HealthStatus` value) as a `CapsuleServiceStatus` value. Use `HEALTHY` instead.

### 20.2 Showing last-reported state as current

Do not display the latest `HealthReport.status` as the service's current status without checking Agent freshness. If the Agent is offline, the service is `STALE`.

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
