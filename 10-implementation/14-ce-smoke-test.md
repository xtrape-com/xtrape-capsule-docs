# CE Smoke Test Runbook

- Status: Implementation Guidance
- Edition: CE
- Priority: Current
- Audience: CE maintainers, QA engineers, operators, AI coding agents

This runbook verifies the core Opstage CE flow after changes to backend, UI, command/action contracts, or Agent integration.

---

## 1. Scope

The smoke test verifies:

1. Backend starts and exposes health.
2. UI can login.
3. Registration token can be created.
4. Agent registers and becomes online.
5. Capsule Service is reported.
6. Action prepare works.
7. Action execute creates a Command.
8. Agent polls and reports CommandResult.
9. Result list / row action UX can be inspected when the service supports it.
10. Audit events and command history are visible.

This runbook is intentionally service-agnostic. Use the demo service, Capi-Chatgpt, or any embedded Agent service that exposes at least one safe action.

---

## 2. Pre-flight Checks

From `xtrape-capsule-ce` repository root:

```bash
pnpm install
pnpm --filter @xtrape/opstage-backend typecheck
pnpm --filter @xtrape/opstage-backend test
pnpm --filter @xtrape/opstage-ui typecheck
pnpm --filter @xtrape/opstage-ui test
```

Expected:

```text
Backend tests pass.
UI tests pass.
No TypeScript errors.
```

### Automated local smoke script

The CE repository also provides an in-process smoke script that starts the backend with a temporary SQLite database, registers an embedded demo Agent, verifies action prepare, action execute, list results, row action metadata, and sensitive config redaction:

```bash
cd xtrape-capsule-ce
node --import tsx scripts/smoke-demo.mjs
# or, after builds are required in your workflow:
pnpm smoke:demo
```

Use the manual steps below when you need to verify browser/UI behavior or a real external service.

---

## 3. Start CE Locally

Use a clean local database for smoke testing:

```bash
export DATABASE_URL=file:./data/opstage-smoke.db
export OPSTAGE_ADMIN_USERNAME=admin@example.local
export OPSTAGE_ADMIN_PASSWORD=change-me-before-running
export OPSTAGE_SESSION_SECRET=local-smoke-session-secret-at-least-32-chars
export OPSTAGE_STATIC_DIR=apps/opstage-ui/dist

pnpm --filter @xtrape/opstage-ui build
pnpm --filter @xtrape/opstage-backend start
```

Health check:

```bash
curl -s http://localhost:8080/api/system/health | jq .
```

Expected:

```json
{ "success": true, "data": { "status": "UP" } }
```

---

## 4. Login and Create Registration Token

1. Open `http://localhost:8080`.
2. Login with the configured admin account.
3. Open **Registration Tokens**.
4. Create a token.
5. Copy the raw token immediately; it is shown once.

Expected:

- Token row appears in Registration Tokens.
- Audit event is created for token creation.

---

## 5. Start an Agent-backed Service

Start your service with the registration token:

```bash
OPSTAGE_BACKEND_URL=http://localhost:8080 \
OPSTAGE_REGISTRATION_TOKEN=opstage_reg_... \
OPSTAGE_AGENT_TOKEN_FILE=./data/smoke-agent-token.json \
<service start command>
```

Expected in CE UI:

- Agent appears under **Agents**.
- Agent status becomes `ONLINE` after polling/heartbeat.
- Capsule Service appears under **Capsule Services**.
- Service has manifest, actions, configs, and health.

If the service uses command polling as heartbeat, keep it running for at least one polling interval.

---

## 6. Verify Action Prepare

Open the Capsule Service detail drawer and click a safe action.

Expected:

- Action panel opens.
- Prepare loading state is shown briefly.
- Dynamic fields and initial JSON are rendered.
- If prepare fails, the panel remains open and shows diagnostics such as `commandId`, `commandStatus`, `agentId`, and `serviceId`.

Recommended safe actions:

- `runHealthCheck`
- `listAccounts`
- `listApiKeys`
- demo `echo`

---

## 7. Verify Action Execute

Run a safe action.

Expected:

- A Command is created.
- Command status moves through `PENDING` / `RUNNING` to `SUCCEEDED` or `FAILED`.
- Action panel shows command result.
- Commands page contains the command.
- Audit Events contains command lifecycle entries.

For list actions, verify:

- `data.list` renders as a table.
- Empty state is readable when there is no data.
- Row count appears in the card title.
- Raw result JSON is still available.

---

## 8. Verify Row Actions

If the list result exposes `rowActions`:

1. Click a non-destructive row action, or use a destructive one in a disposable test environment.
2. Confirm if prompted.
3. Observe row-level loading and disabled states.
4. Wait for completion.

Expected:

- Row action creates a normal Command.
- The row shows loading while the action runs.
- The current list is refreshed after completion.
- Long-running row actions refresh after their Command reaches a terminal status.

---

## 9. Verify Failure Modes

Recommended failure checks:

| Scenario | Expected result |
|---|---|
| Stop Agent, then open an action | Backend returns agent offline/stale error. |
| Start Agent without token file and without registration token | Service logs configuration error. |
| Use revoked registration token | Registration fails. |
| Force prepare failure in a test service | UI shows prepare diagnostics and retry. |
| Return oversized command result | Backend rejects with `COMMAND_RESULT_TOO_LARGE`. |

---

## 10. Cleanup

```bash
# Stop service and backend first.
rm -f ./data/opstage-smoke.db ./data/smoke-agent-token.json
```

If using Docker Compose:

```bash
docker compose down -v
```

---

## 11. Pass Criteria

The smoke test passes when:

- CE backend and UI start successfully.
- Login works.
- Agent registers and stays online while running.
- Capsule Service reports actions and health.
- At least one prepare and one execute command succeed.
- Command result is visible.
- Audit events are produced.
- Failure diagnostics are understandable for at least one negative scenario.

## 12. Browser UI Smoke Extension

Use this extension after the automated script passes and when UI behavior changed. A human tester or browser automation tool should verify:

1. Login page renders and rejects an invalid password.
2. Login succeeds with the owner account.
3. Capsule Services list refresh button updates data.
4. Opening an action shows the prepare loading state.
5. Prepare failure keeps the panel open and displays diagnostics.
6. A list action renders table rows, empty state, row count, and raw JSON.
7. A row action shows row-level loading and disables sibling row buttons.
8. A long-running action shows command status updates and refreshes service/account status after completion.
9. Commands page can open the command detail and show result/error JSON.
10. Audit Events page shows command lifecycle events.

For local browser automation in Codex sessions, use the Browser Use plugin against `http://localhost:8080` after starting CE and a test Agent.
