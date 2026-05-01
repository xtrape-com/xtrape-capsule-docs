# CE UI Design

- Status: Implementation Target
- Edition: CE
- Priority: Current
- Audience: product designers, frontend developers, backend developers, AI coding agents

This document defines the UI design for **Opstage CE v0.1**.

The CE UI should be a lightweight Web console that allows operators to see, understand, and operate Capsule Services through Opstage Backend.

---

## 1. UI Design Goal

The goal of the CE UI is to make the Capsule governance loop visible and operable:

```text
Agent registration
    ↓
Service report
    ↓
Heartbeat and health
    ↓
Status visibility
    ↓
Predefined action request
    ↓
Command result
    ↓
Audit trace
```

The UI should help users answer:

- Which Agents are connected?
- Which Capsule Services exist?
- Which services are online, unhealthy, offline, or stale?
- What did the service report in its manifest?
- What health state did it report?
- What configuration metadata is visible?
- What actions can be executed safely?
- What Commands were created and what happened?
- What does the audit log say?

---

## 2. UI Principles

CE v0.1 UI should follow these principles:

1. Be simple enough for first-time users.
2. Make status and freshness visible.
3. Distinguish Agent status, Service status, and Health status.
4. Expose only predefined actions.
5. Never expose arbitrary shell execution.
6. Mask sensitive values.
7. Prefer clear tables and detail pages over complex dashboards.
8. Work well on desktop and remain readable on mobile browsers.
9. Avoid EE/Cloud-only features in CE v0.1.
10. Keep UI behavior aligned with shared specs.

---

## 3. Recommended UI Stack

CE v0.1 UI stack (decided by [ADR 0007](../../08-decisions/0007-ui-state-and-data-fetching.md)):

```text
Vue 3 + TypeScript + Ant Design Vue + Vite
+ TanStack Vue Query  (server state)
+ Pinia               (client UI state)
+ Vue Router          (URL state)
+ Vee-Validate + Zod  (forms)
```

Ant Design Vue provides the same mature admin-console components as the React Ant Design ecosystem.

The UI must remain a Web console. A native mobile app is not required for CE v0.1.

---

## 4. Information Architecture

The CE UI should contain these primary sections:

```text
Login
Dashboard
Agents
Capsule Services
Commands
Audit Logs
System
```

Recommended navigation:

```text
Dashboard
Agents
Capsule Services
Commands
Audit Logs
System Settings
```

Each page should use consistent layout, status tags, timestamps, and action buttons.

---

## 5. Layout Model

### 5.1 Desktop layout

Recommended desktop layout:

```text
+------------------------------------------------+
| Top Bar: Product Name, Current User, Logout    |
+----------------------+-------------------------+
| Sidebar Navigation   | Main Content            |
|                      |                         |
| Dashboard            | Page Header             |
| Agents               | Filters / Actions       |
| Capsule Services     | Table / Detail          |
| Commands             |                         |
| Audit Logs           |                         |
| System Settings      |                         |
+----------------------+-------------------------+
```

### 5.2 Mobile layout

CE v0.1 should be mobile-readable, not a full mobile application.

Recommended mobile behavior:

- collapse sidebar into drawer;
- tables may become horizontally scrollable;
- detail pages remain readable;
- action buttons remain accessible;
- dense admin data is acceptable if not broken.

---

## 6. Required Pages

CE v0.1 should implement at least these pages:

```text
Login
Dashboard
Agents
Agent Detail
Capsule Services
Capsule Service Detail
Commands
Command Detail
Audit Logs
System Settings
```

`Command Detail` may be implemented as a drawer or modal if a full page is not needed.

---

## 7. Login Page

### 7.1 Purpose

The Login page authenticates local CE users.

### 7.2 Required fields

```text
Username
Password
Login button
```

### 7.3 Required behavior

- show error on failed login;
- do not reveal whether username or password is wrong;
- redirect to Dashboard after successful login;
- create audit events for successful and failed login;
- do not log raw password.

### 7.4 Out of scope

CE v0.1 does not need:

- SSO login;
- OAuth login;
- MFA;
- password reset workflow;
- user self-registration.

---

## 8. Dashboard Page

### 8.1 Purpose

The Dashboard gives a quick overview of the runtime governance state.

### 8.2 Required cards

```text
Agents total
Agents online
Capsule Services total
Services online
Services unhealthy
Services stale
Recent Commands
Recent Audit Events
```

### 8.3 Recommended sections

```text
Status Summary
Recent Commands
Recent Audit Events
Stale or Unhealthy Services
```

### 8.4 Dashboard behavior

Dashboard should prioritize operational clarity over visual complexity.

CE v0.1 does not need charts or monitoring panels.

---

## 9. Agents Page

### 9.1 Purpose

The Agents page lists registered Agents.

### 9.2 Required columns

```text
Status
Code
Name
Mode
Runtime
Version
Last Heartbeat
Registered At
Actions
```

### 9.3 Required filters

Optional but useful:

```text
Status
Runtime
Search by code/name
```

### 9.4 Row actions

Required:

```text
View Detail
```

Optional:

```text
Disable
Re-enable
Revoke
```

Disable and revoke actions may be implemented after the MVP if time is limited, but the UI should not contradict the data model.

---

## 10. Agent Detail Page

### 10.1 Purpose

The Agent Detail page shows identity, connectivity, and reported services for one Agent.

### 10.2 Required sections

```text
Overview
Heartbeat
Reported Capsule Services
Recent Commands
Recent Audit Events
```

### 10.3 Overview fields

```text
Agent ID
Code
Name
Status
Mode
Runtime
Version
Hostname
OS
Architecture
Registered At
Last Heartbeat At
```

### 10.4 Status behavior

The page must make heartbeat freshness visible.

Example:

```text
Status: Offline
Last heartbeat: 2026-04-30 10:21:00
Reason: heartbeat timeout
```

---

## 11. Capsule Services Page

### 11.1 Purpose

The Capsule Services page lists managed Capsule Services.

### 11.2 Required columns

```text
Effective Status
Health Status
Code
Name
Runtime
Version
Agent
Last Reported
Actions
```

### 11.3 Required filters

Recommended filters:

```text
Effective Status
Health Status
Runtime
Agent
Search by code/name
```

### 11.4 Row actions

Required:

```text
View Detail
```

Optional:

```text
Run Health Check
```

Only show quick actions if they are predefined and safe.

---

## 12. Capsule Service Detail Page

### 12.1 Purpose

The Capsule Service Detail page is the most important CE UI page.

It should show everything Opstage knows about a service.

### 12.2 Required tabs

```text
Overview
Manifest
Health
Configs
Actions
Commands
Audit
```

### 12.3 Overview tab

Required fields:

```text
Effective Status
Reported Status
Health Status
Freshness
Code
Name
Description
Runtime
Version
Agent Mode
Associated Agent
Last Reported At
Last Heartbeat At
Reason
```

The Overview tab must distinguish:

```text
Effective Status
Reported Status
Health Status
Agent Status
Freshness
```

### 12.4 Manifest tab

Display the manifest JSON in a readable format.

Recommended behavior:

- pretty JSON viewer;
- copy button if easy;
- collapse nested sections if possible.

### 12.5 Health tab

Display:

```text
Health Status
Message
Checked At
Received At
Dependencies
Details JSON
```

Dependency table columns:

```text
Name
Type
Status
Message
```

### 12.6 Configs tab

Display ConfigItems.

Required columns:

```text
Key
Label
Type
Value
Default
Editable
Sensitive
Source
Description
```

Sensitive values must be masked or shown as `secretRef`.

Bad behavior:

```text
Show raw password/token/cookie
```

### 12.7 Actions tab

Display predefined actions.

Required columns or cards:

```text
Name
Label
Description
Danger Level
Enabled
Input
Run Button
```

Action execution behavior:

1. User clicks Run.
2. UI shows input form if input schema exists.
3. UI asks confirmation for high-risk actions.
4. UI calls Backend action request API.
5. UI shows created Command ID and status.
6. UI links to Command detail.

CE v0.1 does not need a full dynamic form engine. Simple JSON payload input is acceptable if schema rendering is not ready.

### 12.8 Commands tab

Display recent Commands for this service.

Required columns:

```text
Status
Action Name
Command Type
Created At
Finished At
Result
```

### 12.9 Audit tab

Display recent Audit Events related to this service.

Required columns:

```text
Time
Actor
Action
Result
Description
```

---

## 13. Commands Page

### 13.1 Purpose

The Commands page provides an operation history view.

### 13.2 Required columns

```text
Status
Command ID
Service
Agent
Command Type
Action Name
Created At
Dispatched At
Finished At
Result Summary
```

### 13.3 Required filters

Recommended filters:

```text
Status
Service
Agent
Command Type
Time Range
```

### 13.4 Command detail

Command detail should show:

```text
Command metadata
Payload JSON
Result status
Output text
Error message
Result JSON
Related Audit Events
```

Command detail may be a full page, drawer, or modal.

---

## 14. Audit Logs Page

### 14.1 Purpose

The Audit Logs page provides traceability for important operations.

### 14.2 Required columns

```text
Time
Actor Type
Actor
Action
Resource Type
Resource
Result
Description
```

### 14.3 Required filters

Recommended filters:

```text
Action
Actor Type
Resource Type
Result
Time Range
Search
```

### 14.4 Detail view

Audit detail should show sanitized:

```text
Request JSON
Result JSON
Metadata JSON
```

Do not display raw secrets.

---

## 15. System Settings Page

### 15.1 Purpose

System Settings shows CE runtime information and basic settings.

### 15.2 Required fields

```text
System Version
Database Status
Default Workspace
Heartbeat Interval
Agent Offline Threshold
Command Poll Interval
Command TTL
```

### 15.3 Registration token section

CE v0.1 should provide a way to create registration tokens.

Recommended UI:

```text
Create Registration Token
Token Name
Expiration
Generate Button
Show token once
Copy token
```

Security rule:

> The raw registration token must be shown only once.

---

## 16. Status Display Rules

### 16.1 Status types

UI must distinguish these status types:

```text
AgentStatus
CapsuleServiceStatus
HealthStatus
CommandStatus
TokenStatus
FreshnessStatus
```

### 16.2 Effective status first

For Capsule Services, show effective status as the primary status.

Reported status may be shown as secondary information.

### 16.3 Stale status

When service status is stale, UI should show:

```text
Current: Stale
Last reported: Online
Reason: Agent offline or health report stale
```

Do not show stale service as green online.

### 16.4 Suggested visual mapping

Status values are not colors, but UI may use consistent tags.

Recommended mapping:

| Status | UI meaning |
|---|---|
| ONLINE / UP / SUCCESS / ACTIVE / FRESH | positive |
| DEGRADED / UNHEALTHY / PENDING / DISPATCHED | warning or in-progress |
| OFFLINE / DOWN / FAILED / ERROR / EXPIRED / REVOKED | negative |
| STALE / UNKNOWN | neutral or warning |
| DISABLED / CANCELLED / USED | neutral |

---

## 17. Action Interaction Rules

### 17.1 Only predefined actions

UI must show only actions reported by the service manifest or action report.

### 17.2 No shell command UI

CE v0.1 must not provide:

```text
terminal panel
shell command input
arbitrary script execution form
```

### 17.3 Confirmation

Require confirmation for:

```text
HIGH
CRITICAL
```

danger-level actions.

Recommended confirmation content:

```text
Action name
Target service
Danger level
Payload summary
```

### 17.4 Command feedback

After action request succeeds, UI should show:

```text
Command created
Command ID
Initial status
Link to command detail
```

---

## 18. Sensitive Data Display Rules

UI must not display raw secrets.

Sensitive examples:

```text
password
token
accessToken
refreshToken
cookie
apiKey
privateKey
credential
```

Recommended display:

```text
••••••••
```

or:

```text
secretRef: agent-local://agent-001/secrets/chatgpt/account-001
```

Sensitive fields in JSON viewers should be masked if possible.

---

## 19. Empty and Error States

### 19.1 Empty Agents

Message:

```text
No Agents registered yet. Create a registration token and start a Capsule Service with the Agent SDK.
```

### 19.2 Empty Services

Message:

```text
No Capsule Services reported yet. Start a Capsule Service with an embedded Agent.
```

### 19.3 Empty Commands

Message:

```text
No Commands created yet. Run a predefined action from a Capsule Service detail page.
```

### 19.4 Empty Audit Logs

Message:

```text
No Audit Events recorded yet.
```

### 19.5 API error

Show concise error message from structured API error.

Do not expose raw stack traces in UI.

---

## 20. Refresh Behavior

CE v0.1 may use simple polling or manual refresh.

Recommended:

- Dashboard: auto-refresh every 10-30 seconds or manual refresh.
- Agent list: manual refresh or light polling.
- Service detail: manual refresh or light polling.
- Command detail: poll while command is pending/dispatched.

Do not introduce WebSocket dependency in CE v0.1.

---

## 21. Mobile Compatibility

CE v0.1 should be usable on mobile browsers for viewing.

Required:

- login works;
- dashboard readable;
- service detail readable;
- action buttons usable;
- tables can scroll horizontally.

Not required:

- native app layout;
- mobile-first redesign;
- offline mobile mode.

---

## 22. Accessibility and Usability

CE v0.1 should follow basic usability practices:

- clear labels;
- readable timestamps;
- visible loading states;
- visible empty states;
- confirmation for dangerous operations;
- copy buttons for tokens and IDs where useful;
- no hidden destructive actions.

Full accessibility certification is not required for v0.1, but the UI should avoid obvious accessibility issues.

---

## 23. UI Non-Goals

CE v0.1 UI should not include:

- enterprise RBAC management;
- SSO configuration;
- tenant management;
- billing pages;
- log search console;
- metrics dashboards;
- alert rule editor;
- workflow designer;
- pipeline designer;
- terminal console;
- arbitrary command execution UI;
- secret vault UI;
- config publishing workflow.

---

## 24. UI Acceptance Criteria

The CE UI is acceptable when:

- user can log in;
- dashboard loads;
- user can create or obtain a registration token;
- Agent appears after registration;
- Agent online/offline status is visible;
- Capsule Service appears after service report;
- service detail shows Overview, Manifest, Health, Configs, Actions, Commands, and Audit;
- sensitive config values are masked;
- user can run `echo` or `runHealthCheck` action;
- UI shows created Command;
- UI shows CommandResult;
- Audit Logs page shows related events;
- stopping Agent eventually makes service stale;
- UI does not expose arbitrary shell execution.

---

## 25. Summary

The CE UI should make lightweight service governance understandable.

The most important UI rule is:

> Make the current governability of each Capsule Service obvious, and allow only safe predefined operations.
