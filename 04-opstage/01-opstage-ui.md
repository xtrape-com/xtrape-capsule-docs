# Opstage UI

- Status: Implementation Guidance
- Edition: Shared
- Priority: High
- Audience: frontend developers, product designers, backend developers, architects, AI coding agents

This document defines the UI subsystem of **Opstage**.

Opstage UI is the human-facing console for operating Capsule Services through Opstage Backend and Agent-based governance.

The current implementation focus is **Opstage CE**. EE and Cloud UI capabilities are future planning tracks and must not expand the CE v0.1 implementation scope.

---

## 1. Purpose

The purpose of Opstage UI is to make the Capsule governance loop visible and operable.

The UI should help operators answer:

- Which Agents are registered?
- Which Agents are online, offline, disabled, or revoked?
- Which Capsule Services exist?
- Which services are online, unhealthy, stale, or offline?
- What manifest did each service report?
- What health state did each service report?
- What config metadata is visible?
- What predefined actions can be executed?
- What Commands were created?
- What results did Commands return?
- What does the audit log show?

The UI should make lightweight services governable without forcing every Capsule Service to build its own admin console.

---

## 2. Positioning

Opstage UI is:

> The operator console for Capsule Service governance.

It is not:

- a generic low-code admin panel;
- a full observability dashboard;
- a full configuration center UI;
- a remote shell terminal;
- a workflow designer;
- a Kubernetes console;
- a secret vault UI by default;
- a billing portal in CE.

The first UI identity should remain runtime governance for Capsule Services.

---

## 3. Relationship with Opstage Backend

Opstage UI must communicate only with Opstage Backend through Admin APIs.

Recommended relationship:

```text
Browser UI
    ↓ Admin API
Opstage Backend
    ↓ persistence and Agent API coordination
Agents
    ↓ local handlers
Capsule Services
```

The UI must not call Agents directly.

The UI must not bypass Backend authorization or validation.

The UI should not contain business-critical security rules that are not enforced by Backend.

---

## 4. UI Design Principles

Opstage UI should follow these principles:

1. Make runtime status obvious.
2. Distinguish Agent status, service status, health status, and freshness.
3. Prefer simple tables and detail pages over complex dashboards in CE.
4. Expose only predefined actions.
5. Never provide arbitrary shell execution in CE.
6. Mask sensitive values.
7. Show stale and offline states clearly.
8. Make Commands and results traceable.
9. Keep audit logs accessible for basic traceability.
10. Avoid disabled EE/Cloud-only navigation clutter in CE.
11. Work well on desktop and remain readable on mobile browsers.

---

## 5. CE UI Scope

Opstage CE UI should implement the minimum complete governance UI.

Required CE pages:

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

Required CE capabilities:

- local admin login;
- dashboard summary;
- Agent list and detail;
- Capsule Service list and detail;
- manifest viewer;
- health viewer;
- config metadata viewer;
- predefined action execution;
- Command list and detail;
- CommandResult display;
- AuditEvent list and detail;
- registration token creation;
- sensitive value masking.

---

## 6. CE UI Non-Goals

CE v0.1 UI should not implement:

- tenant management;
- organization management;
- team invitations;
- enterprise RBAC management;
- SSO settings;
- billing portal;
- subscription plan UI;
- log search console;
- metrics dashboard;
- alert rule editor;
- secret vault UI;
- workflow designer;
- pipeline designer;
- terminal console;
- arbitrary command execution panel;
- plugin marketplace;
- Cloud support access workflow.

These may be future EE or Cloud features.

---

## 7. Recommended UI Stack

Recommended CE UI stack:

```text
React + TypeScript + Vite + Ant Design
```

Alternative stack:

```text
Vue 3 + TypeScript + Vite + Naive UI / Element Plus
```

Current recommendation:

```text
React + TypeScript + Vite + Ant Design
```

because it provides mature admin-console components and can support tables, forms, drawers, tabs, and layout quickly.

The UI should remain a Web console. A native mobile app is not required for CE v0.1.

---

## 8. Layout Model

Recommended desktop layout:

```text
+------------------------------------------------+
| Top Bar: Opstage, Workspace, User, Logout      |
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

CE has one implicit default Workspace, so a workspace switcher is not required.

If a workspace indicator is shown, it should be passive:

```text
Workspace: default
```

not a full multi-workspace UI.

---

## 9. Navigation

CE navigation should be simple:

```text
Dashboard
Agents
Capsule Services
Commands
Audit Logs
System Settings
```

Do not show disabled future menu items such as:

```text
Organizations
Billing
SSO
RBAC
Alerts
Logs
Metrics
Secrets
Marketplace
```

Future editions may extend navigation later.

---

## 10. Login Page

The Login page authenticates local CE users.

Required fields:

```text
Username
Password
Login button
```

Required behavior:

- show generic error on failed login;
- do not reveal whether username or password is wrong;
- redirect to Dashboard after successful login;
- do not log raw password;
- create backend audit events for login attempts if implemented by Backend.

CE v0.1 does not need:

- SSO login;
- OAuth login;
- MFA;
- password reset;
- user self-registration.

---

## 11. Dashboard Page

The Dashboard gives a quick operational summary.

Recommended cards:

```text
Agents total
Agents online
Agents offline
Capsule Services total
Services online
Services unhealthy
Services stale
Recent Commands
Recent Audit Events
```

Recommended sections:

```text
Status Summary
Stale or Unhealthy Services
Recent Commands
Recent Audit Events
```

CE Dashboard should prioritize clarity over decorative charts.

---

## 12. Agents Page

The Agents page lists registered Agents.

Recommended columns:

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

Recommended filters:

```text
Status
Runtime
Search by code/name
```

Required row action:

```text
View Detail
```

Future actions may include:

```text
Disable
Re-enable
Revoke
Rotate Token
```

but CE v0.1 may defer them unless supported by Backend.

---

## 13. Agent Detail Page

Agent Detail should show Agent identity, connectivity, and reported services.

Recommended sections:

```text
Overview
Heartbeat
Reported Capsule Services
Recent Commands
Recent Audit Events
```

Overview fields:

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

The page must make heartbeat freshness visible.

Example:

```text
Status: Offline
Last heartbeat: 2026-04-30 10:21:00
Reason: heartbeat timeout
```

---

## 14. Capsule Services Page

The Capsule Services page lists managed Capsule Services.

Recommended columns:

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

Recommended filters:

```text
Effective Status
Health Status
Runtime
Agent
Search by code/name
```

Required row action:

```text
View Detail
```

Only show quick action buttons if they are predefined and safe.

---

## 15. Capsule Service Detail Page

Capsule Service Detail is the most important CE UI page.

Recommended tabs:

```text
Overview
Manifest
Health
Configs
Actions
Commands
Audit
```

### 15.1 Overview tab

Show:

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

The UI must distinguish:

```text
Effective Status
Reported Status
Health Status
Agent Status
Freshness
```

### 15.2 Manifest tab

Display manifest JSON in a readable viewer.

Recommended features:

- pretty formatting;
- copy button if practical;
- collapsible nested sections if easy.

### 15.3 Health tab

Show:

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

### 15.4 Configs tab

Show config metadata.

Recommended columns:

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

Sensitive values must be masked or represented as `secretRef`.

### 15.5 Actions tab

Show predefined actions.

Recommended fields:

```text
Name
Label
Description
Danger Level
Enabled
Input Schema
Run Button
```

Action execution flow:

```text
User clicks Run
    ↓
UI shows input form or JSON payload editor
    ↓
UI asks confirmation if high risk
    ↓
UI calls Backend Admin API
    ↓
Backend creates Command
    ↓
UI shows Command status and link
```

CE v0.1 may use simple JSON input instead of a full dynamic form engine.

### 15.6 Commands tab

Show recent Commands for this service.

Columns:

```text
Status
Action Name
Command Type
Created At
Finished At
Result
```

### 15.7 Audit tab

Show recent AuditEvents for this service.

Columns:

```text
Time
Actor
Action
Result
Description
```

---

## 16. Commands Page

The Commands page provides operation history.

Recommended columns:

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

Recommended filters:

```text
Status
Service
Agent
Command Type
Time Range
```

Command detail should show:

```text
Command metadata
Payload JSON
Result status
Output text
Error message
Result JSON
Related AuditEvents
```

Command detail may be a full page, drawer, or modal.

---

## 17. Audit Logs Page

The Audit Logs page provides traceability.

Recommended columns:

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

Recommended filters:

```text
Action
Actor Type
Resource Type
Result
Time Range
Search
```

Audit detail should show sanitized:

```text
Request JSON
Result JSON
Metadata JSON
```

Raw secrets must not be shown.

---

## 18. System Settings Page

System Settings should show CE runtime information and basic operational settings.

Recommended fields:

```text
System Version
Database Status
Default Workspace
Heartbeat Interval
Agent Offline Threshold
Command Poll Interval
Command TTL
```

Registration token section:

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

## 19. Status Display Rules

UI must distinguish these statuses:

```text
AgentStatus
CapsuleServiceStatus
HealthStatus
CommandStatus
TokenStatus
FreshnessStatus
```

For Capsule Services, show **Effective Status** as the primary status.

Reported status and health status should be visible but secondary.

Do not show stale services as green online.

Example stale display:

```text
Effective Status: Stale
Last Reported Status: Online
Reason: Agent heartbeat timeout
```

---

## 20. Sensitive Data Rules

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
secret
```

Recommended display:

```text
••••••••
```

or:

```text
secretRef: agent-local://agent-001/secrets/chatgpt/account-001
```

JSON viewers should mask sensitive keys where practical.

---

## 21. Action Safety Rules

CE UI must only execute predefined actions.

CE UI must not provide:

```text
terminal panel
shell command input
custom script execution form
arbitrary command execution API
```

For high-risk actions, require confirmation if Backend reports danger level:

```text
HIGH
CRITICAL
```

Confirmation should show:

```text
Action name
Target service
Danger level
Payload summary
```

---

## 22. Empty and Error States

Recommended empty states:

### Empty Agents

```text
No Agents registered yet. Create a registration token and start a Capsule Service with the Agent SDK.
```

### Empty Services

```text
No Capsule Services reported yet. Start a Capsule Service with an embedded Agent.
```

### Empty Commands

```text
No Commands created yet. Run a predefined action from a Capsule Service detail page.
```

### Empty Audit Logs

```text
No Audit Events recorded yet.
```

API errors should show structured, concise messages.

Do not expose raw stack traces in UI.

---

## 23. Refresh Behavior

CE may use simple polling or manual refresh.

Recommended behavior:

- Dashboard: manual refresh or light polling;
- Agent list: manual refresh or light polling;
- Service detail: manual refresh or light polling;
- Command detail: poll while command is pending or dispatched.

Do not require WebSocket in CE v0.1.

---

## 24. Mobile Compatibility

CE UI should be usable on mobile browsers for viewing and simple operations.

Required:

- login works;
- dashboard readable;
- service detail readable;
- action buttons usable;
- tables can scroll horizontally.

Not required:

- native app layout;
- offline mode;
- mobile-first redesign.

---

## 25. EE UI Extension Direction

Future EE UI may add:

- RBAC management;
- SSO settings;
- audit export;
- alert rule editor;
- observability dashboards;
- secret provider settings;
- sidecar/external Agent management;
- database and deployment diagnostics;
- license and support information;
- advanced approval workflows.

These are not CE v0.1 requirements.

---

## 26. Cloud UI Extension Direction

Future Cloud UI may add:

- organization switcher;
- workspace switcher;
- team invitations;
- subscription and billing pages;
- usage dashboards;
- Cloud Agent Gateway diagnostics;
- managed alerting;
- Cloud data export/deletion workflows;
- support access workflows.

These are not CE v0.1 requirements.

---

## 27. Acceptance Criteria

Opstage CE UI is acceptable when:

- user can log in;
- dashboard loads;
- user can create a registration token;
- Agent appears after registration;
- Agent online/offline status is visible;
- Capsule Service appears after service report;
- service detail shows Overview, Manifest, Health, Configs, Actions, Commands, and Audit;
- sensitive values are masked;
- user can run a predefined `echo` or `runHealthCheck` action;
- UI shows created Command;
- UI shows CommandResult;
- Audit Logs page shows related events;
- stale service status is visible;
- UI does not expose arbitrary shell execution;
- UI does not show disabled EE/Cloud-only pages in CE.

---

## 28. Summary

Opstage UI should make Capsule Services understandable and operable through a simple governance console.

The most important UI rule is:

> Make service governability visible, expose only safe predefined operations, and keep CE UI focused on the core governance loop.
