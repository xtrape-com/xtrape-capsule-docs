---
status: implemented
audience: ai-coding-agents
stability: evolving
last_reviewed: 2026-05-05
edition: ce
phase: current
---

# CE Backup and Restore Runbook

- Status: Implementation Guidance
- Edition: CE
- Priority: High
- Audience: CE operators, owners, support engineers, AI coding agents

This runbook describes how to back up and restore the Opstage CE SQLite database.

---

## 1. What Must Be Backed Up

Back up the persistent data directory behind:

```text
DATABASE_URL=file:./data/opstage.db
OPSTAGE_BACKUP_DIR=./data/backups
```

The SQLite database contains:

- users and password hashes;
- registration tokens and their state;
- Agents and Agent token hashes;
- Capsule Services, configs, actions, health reports;
- Commands and CommandResults;
- Audit Events;
- maintenance settings.

Agent-side token files are not stored in the CE database. Back them up separately when you control the Agent host:

```text
OPSTAGE_AGENT_TOKEN_FILE=./data/agent-token.json
```

---

## 2. Create a Backup from UI

Owner flow:

1. Login as `owner`.
2. Open Settings / Diagnostics.
3. Click **Download SQLite Backup** or trigger the backup action.
4. Store the downloaded file outside the application host.

Backend writes server-side backups under `OPSTAGE_BACKUP_DIR` when using the backup endpoint.

---

## 3. Filesystem Backup

Preferred safe flow:

```bash
# 1. Stop CE backend/container.
# 2. Copy the SQLite database and WAL/SHM files if present.
cp ./data/opstage.db ./backup/opstage.db
cp ./data/opstage.db-wal ./backup/opstage.db-wal 2>/dev/null || true
cp ./data/opstage.db-shm ./backup/opstage.db-shm 2>/dev/null || true
# 3. Restart CE backend/container.
```

If the backend must stay online, use SQLite backup tooling or the CE backup endpoint instead of copying a hot database file.

---

## 4. Restore Procedure

1. Stop CE backend/container.
2. Move the current database aside:

```bash
mv ./data/opstage.db ./data/opstage.db.before-restore.$(date +%Y%m%d%H%M%S)
rm -f ./data/opstage.db-wal ./data/opstage.db-shm
```

3. Copy the backup into place:

```bash
cp ./backup/opstage.db ./data/opstage.db
```

4. Ensure file ownership and permissions match the runtime user.
5. Start CE backend/container.
6. Validate:
   - `GET /api/system/health` returns `UP`;
   - owner login works;
   - Dashboard loads;
   - Agents and Capsule Services are visible;
   - Commands and Audit Events are visible.

---

## 5. Agent Reconnect After Restore

After restoring an older database:

- Agents whose token hashes exist in the restored DB can reconnect using their existing Agent token files.
- Agents registered after the backup timestamp may no longer exist in the restored DB and must register again with a new registration token.
- Registration tokens created after the backup timestamp are lost.
- Commands created after the backup timestamp are lost.

If an Agent stays offline:

1. Check Agent logs for `UNAUTHORIZED` / invalid token.
2. Revoke stale Agent row if needed.
3. Create a new registration token.
4. Delete the Agent-side token file only when you intentionally want the Agent to register again.
5. Restart the Agent.

---

## 6. Backup Policy Recommendations

- Keep at least daily backups for small CE deployments.
- Store backups outside the CE host.
- Encrypt backup storage when audit data or service metadata is sensitive.
- Test restore regularly using a disposable environment.
- Retain backups according to your audit retention policy.
- Do not commit SQLite backups or Agent token files to git.
