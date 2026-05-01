# CE v0.1 Database Implementation

- Status: Implementation Record
- Edition: CE
- Priority: Current
- Audience: backend developers, operators, architects, AI coding agents

This document records the implemented CE v0.1 persistence model. It complements the conceptual specs in `02-specs/` and the API contracts in `09-contracts/`.

## 1. Runtime database

CE v0.1 uses SQLite at runtime through `better-sqlite3`. The Prisma schema in `packages/db/schema.prisma` is kept as the relational contract and validation reference.

Default runtime configuration:

```text
DATABASE_URL=file:./data/opstage.db
OPSTAGE_DATA_DIR=./data
OPSTAGE_BACKUP_DIR=./data/backups
```

Docker deployments mount `/app/data` as the persistent volume. Losing this volume loses all persisted state, including admin users, Agent tokens, service inventory, commands, audit history, and backup files.

## 2. Workspace model

CE v0.1 is single-workspace in product behavior. The database still stores a `Workspace` row so the schema can evolve toward multi-workspace or EE features without breaking core tables.

Implemented default workspace:

```text
id:  wks_default
code: default
name: Default Workspace
```

All workspace-scoped tables carry `workspaceId`.

## 3. Core tables

| Table | Purpose | Important constraints/indexes |
| --- | --- | --- |
| `workspaces` | Logical tenant boundary. | `code` unique. |
| `users` | Admin console accounts. | `username` unique; `role` is `owner`, `operator`, or `viewer`; `status` is `ACTIVE` or `DISABLED`. |
| `registration_tokens` | One-time Agent bootstrap tokens. | `tokenHash` unique; token raw value is shown once and never stored. |
| `agents` | Registered embedded/sidecar/external Agents. | Unique `(workspaceId, code)`; indexed by status. |
| `agent_tokens` | Long-lived bearer tokens used by Agents. | `tokenHash` unique; active tokens are revoked when an Agent is revoked. |
| `capsule_services` | Last reported Capsule Service inventory. | Unique `(workspaceId, code)`; linked to current Agent. |
| `health_reports` | Time-series-ish health snapshots. | Indexed by `serviceId, reportedAt` and `agentId, reportedAt`. |
| `config_items` | Reported config metadata. | Unique `(serviceId, configKey)`; sensitive values are not persisted as previews/defaults. |
| `action_definitions` | Reported action catalog. | Unique `(serviceId, name)`; carries danger and confirmation metadata. |
| `commands` | Admin-requested action executions. | Indexed by workspace/status, agent/status, and service/create time. |
| `command_results` | Agent-reported terminal result. | One result per command. |
| `audit_events` | Security and governance audit log. | Indexed by time, actor, and target. |
| `system_settings` | Reserved key/value settings. | Unique `(workspaceId, key)`. |

## 4. Token storage rules

Raw secrets are never stored:

- Registration tokens are generated as `opstage_reg_*`; only `tokenHash` is persisted.
- Agent tokens are generated as `opstage_agent_*`; only `tokenHash` is persisted.
- The Node Agent SDK stores the Agent-side token file locally as:

```json
{
  "agentId": "agt_...",
  "agentToken": "opstage_agent_...",
  "savedAt": "..."
}
```

The token file must be treated as a secret and should use file mode `0600` where the host filesystem supports it.

## 5. Registration and service-report flow

1. An operator or owner creates a registration token.
2. Backend stores only the token hash and returns the raw token once.
3. Agent calls `POST /api/agents/register` with the raw registration token and optional first service report.
4. Backend marks the registration token `USED`, creates/updates an `agents` row, creates an active `agent_tokens` row, and returns the raw Agent token.
5. Agent uses the Agent token for heartbeat, service report, command polling, and command result reporting.
6. Service reports upsert `capsule_services`, replace current `config_items` and `action_definitions` for that service, and append `health_reports` when health is present.

## 6. Status persistence

Agent statuses are stored on `agents.status`:

```text
PENDING, ONLINE, OFFLINE, DISABLED, REVOKED
```

Service effective statuses are stored on `capsule_services.status`:

```text
UNKNOWN, HEALTHY, UNHEALTHY, STALE, OFFLINE
```

Health status is separately stored on `capsule_services.healthStatus` and `health_reports.status`:

```text
UP, DEGRADED, DOWN, UNKNOWN
```

The maintenance task transitions stale online Agents to `OFFLINE` and marks their services `OFFLINE` or stale according to the implemented CE rule set.

## 7. Command lifecycle persistence

Commands are created by admin APIs and consumed by Agents:

```text
PENDING -> RUNNING -> SUCCEEDED
PENDING -> RUNNING -> FAILED
PENDING/RUNNING -> CANCELLED
PENDING/RUNNING -> EXPIRED
```

`commands.expiresAt` is set when a command is created. Maintenance expires pending/running commands after that time. A successful Agent result creates one `command_results` row and moves the command to `SUCCEEDED`; a failed Agent result moves it to `FAILED`.

## 8. Audit retention

Audit events are append-only during normal operation. Maintenance prunes records older than:

```text
OPSTAGE_AUDIT_RETENTION_DAYS=90
```

Set it to `0` to prune all older-than-now events during maintenance; use with care.

## 9. Backup and restore notes

Owners can trigger SQLite backup through the UI or `POST /api/admin/backup/sqlite`. The backend writes the backup under `OPSTAGE_BACKUP_DIR` before streaming it to the caller.

Recommended restore pattern:

1. Stop the Opstage container/process.
2. Copy the backup database file into the configured `DATABASE_URL` path.
3. Start Opstage.
4. Check `/api/system/health` and login.

Downgrade restore is not supported for CE v0.1.
