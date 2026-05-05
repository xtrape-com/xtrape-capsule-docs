# CE v0.1 User and Operations Manual

- Status: Implementation Record
- Edition: CE
- Priority: Current
- Audience: CE operators, evaluators, support engineers, AI coding agents

This manual describes how the implemented CE v0.1 product is operated after installation.

## 1. Roles

| Role | Intended user | Permissions |
| --- | --- | --- |
| `owner` | System administrator | Full access, including user management, backup, maintenance, Agent lifecycle, tokens, commands. |
| `operator` | Day-to-day operator | Can create/revoke registration tokens, execute/cancel commands, disable/revoke Agents, run maintenance. Cannot manage users or create backups. |
| `viewer` | Read-only observer | Can view dashboard, inventory, commands, audits, diagnostics. Cannot mutate state. |

At least one active owner must remain. The backend rejects attempts to demote or disable the last active owner.

## 2. First boot

Required production-like environment variables:

```text
OPSTAGE_ADMIN_USERNAME
OPSTAGE_ADMIN_PASSWORD       # at least 12 chars
OPSTAGE_SESSION_SECRET       # at least 32 chars
DATABASE_URL                 # default: file:./data/opstage.db
OPSTAGE_STATIC_DIR           # default: apps/opstage-ui/dist
```

On first boot, the backend creates the default workspace and the initial admin user. Later changes to `OPSTAGE_ADMIN_USERNAME` and `OPSTAGE_ADMIN_PASSWORD` do not overwrite existing users.

## 3. Login and session behavior

1. Open the CE console.
2. Login with the bootstrapped admin username/password.
3. Backend sets an HTTP-only signed `opstage_session` cookie and returns a CSRF token.
4. UI sends `X-CSRF-Token` on mutating admin requests.

Session TTL is controlled by:

```text
OPSTAGE_SESSION_TTL_SECONDS=28800
```

Rotating `OPSTAGE_SESSION_SECRET` invalidates all active sessions.

## 4. Creating users

Owner flow:

1. Open Settings / Users.
2. Create a user with role `owner`, `operator`, or `viewer`.
3. Password must be at least 12 characters.
4. Owners can reset passwords and disable users.

Recommended operations model:

- Keep two owners for break-glass access.
- Use operator accounts for daily action execution.
- Use viewer accounts for auditors and stakeholders.

## 5. Connecting an Agent or demo service

1. Open Registration Tokens.
2. Create a token. Copy the raw token immediately; it is shown once.
3. Start an Agent with:

```text
OPSTAGE_BACKEND_URL=http://localhost:8080
OPSTAGE_REGISTRATION_TOKEN=opstage_reg_...
OPSTAGE_AGENT_TOKEN_FILE=./data/agent-token.json
```

The Agent registers once, stores its Agent token file, and then uses that file on later restarts. If the token file is deleted, the Agent needs a new registration token unless another valid Agent token is provided.

## 6. Monitoring Agents and Services

Use the console pages:

- Dashboard: count summary and recent activity.
- Agents: status, heartbeat, runtime, disable/revoke operations.
- Capsule Services: manifest, health, config, actions.
- Commands: action execution history and terminal result.
- Audit Events: security and governance trail.

Common status interpretation:

| Object | Status | Meaning |
| --- | --- | --- |
| Agent | `PENDING` | Registered but no successful heartbeat yet. |
| Agent | `ONLINE` | Recently heartbeating. |
| Agent | `OFFLINE` | Missed heartbeat stale threshold. |
| Agent | `DISABLED` | Operator paused the Agent. |
| Agent | `REVOKED` | Agent token is invalidated. |
| Service | `HEALTHY` | Agent online and latest health is `UP`. |
| Service | `UNHEALTHY` | Latest health is degraded/down according to CE rules. |
| Service | `OFFLINE` / `STALE` | Agent/service is no longer fresh. |

Stale detection uses:

```text
OPSTAGE_AGENT_OFFLINE_THRESHOLD_SECONDS=90
OPSTAGE_MAINTENANCE_INTERVAL_SECONDS=60
```

## 7. Running actions

1. Open a Capsule Service.
2. Select an action.
3. The UI opens an action panel and requests dynamic prepare metadata from the Agent.
4. Provide payload through the schema-driven form or JSON override.
5. Confirm if the action requires confirmation or has high danger.
6. Submit. A Command is created.
7. Agent polls, executes the handler, and reports result.

Action panel behavior operators should know:

- Opening an action creates an `ACTION_PREPARE` Command. This is expected and is used to load dynamic fields, defaults, and current state.
- If prepare times out or fails, the panel remains open and shows diagnostics such as `commandId`, `commandStatus`, `agentId`, and `serviceId`. Use these values to inspect the Commands page and Agent logs.
- Long-running actions continue in the background. The action panel automatically polls the Command and refreshes service/account status when it reaches a terminal state.
- List actions may render a table above the raw JSON result. Raw JSON remains available for troubleshooting.
- Row-level actions in list tables create normal Commands. The clicked row shows loading while the operation runs, and the list refreshes after completion.

The implemented demo service exposes:

- `echo`: returns the submitted payload.
- `runHealthCheck`: returns the current health provider result.

## 8. Maintenance

Maintenance runs periodically when `OPSTAGE_MAINTENANCE_INTERVAL_SECONDS > 0`. Operators and owners can also trigger it manually.

Maintenance currently handles:

- Expiring registration tokens past `expiresAt`.
- Expiring pending/running commands past `expiresAt`.
- Marking stale online Agents offline.
- Updating related service freshness.
- Pruning old audit events based on `OPSTAGE_AUDIT_RETENTION_DAYS`.

Set the interval to `0` to disable the background timer; manual trigger remains available through API/UI for authorized users.

## 9. Backups and audit exports

Owners can create SQLite backups from Settings. The backend writes backup files under:

```text
OPSTAGE_BACKUP_DIR=./data/backups
```

Audit events can be exported as CSV or JSON from the Audit Events page or the export API.

Operational recommendations:

- Back up `/app/data` or the host path behind `DATABASE_URL`.
- Store backups outside the container host for disaster recovery.
- Test restore before relying on backups.

## 10. Diagnostics

The console exposes runtime diagnostics and metrics for operators:

- Node/runtime metadata.
- Uptime and environment summary.
- Count-style metrics for dashboard/state inspection.

Do not expose diagnostics publicly without authentication and TLS.

Operational metrics include command/action counters useful during incident response:

- `operational.agentCommandPolls`: in-memory count of Agent command poll requests since backend start.
- `operational.commandsDispatched`: number of Commands dispatched to Agents.
- `operational.commandsCompleted` / `operational.commandsFailed`: terminal CommandResult counts from audit events.
- `operational.actionPrepareRequested`: action panel prepare requests.
- `operational.actionPrepareTimeouts` / `operational.actionPrepareFailures`: prepare failure indicators.
- `operational.oversizedCommandResultsRejected`: in-memory count of rejected oversized CommandResults since backend start.

## 11. Troubleshooting quick table

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Login fails after restart | Session secret rotated | Login again; if password unknown, restore DB or create migration/admin recovery flow. |
| Registration token not accepted | Token already used/revoked/expired | Create a new registration token. |
| Agent appears offline | Heartbeat stopped or stale threshold too low | Check Agent logs, network, and `OPSTAGE_AGENT_OFFLINE_THRESHOLD_SECONDS`. |
| Action remains pending | Agent is not polling or token revoked | Check Agent status and token file. |
| Action prepare times out | Agent is offline, busy, or not polling prepare commands | Use prepare diagnostics `commandId` and Commands page; check Agent logs and polling interval. |
| Row action succeeds but list looks stale | List refresh failed or service state not updated yet | Click Refresh or run the list action again; inspect the row action Command. |
| `CSRF_INVALID` on POST | Missing `X-CSRF-Token` or cookie issue | Ensure proxy preserves cookies and request headers. |
| Backup endpoint forbidden | User is not owner | Login with owner role. |
