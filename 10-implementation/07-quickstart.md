---
status: implemented
audience: ai-coding-agents
stability: evolving
last_reviewed: 2026-05-05
edition: ce
phase: current
---

# CE v0.1 Quickstart

- Status: Implementation Guidance
- Edition: CE
- Priority: Current
- Audience: open-source users, evaluators, founders, backend developers, frontend developers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/openapi/opstage-ce-v0.1.yaml` disagree, the ADRs and OpenAPI contract win for CE v0.1.

This document is the canonical "first 10 minutes" experience for Opstage CE. The implementation MUST keep the published `README.md` of the repo in sync with the steps below.

## 1. Prerequisites

```text
Docker         24+
docker compose v2+
free port      8080 (Backend) and 3000 (demo service, optional)
```

No Node.js / pnpm / Prisma is needed to run the published images.

## 2. One-Command Start

```bash
# clone, then:
cd deploy/compose

# Generate strong secrets ONCE and store them in .env
{
  echo "OPSTAGE_ADMIN_USERNAME=admin"
  echo "OPSTAGE_ADMIN_PASSWORD=$(openssl rand -base64 24)"
  echo "OPSTAGE_SESSION_SECRET=$(openssl rand -base64 32)"
} > .env

docker compose up -d
```

The Compose deployment MUST refuse to start without the three required env vars (per ADR 0004). After the container is
ready, `docker compose ps` shows the `opstage` service as healthy when `GET /api/system/health` returns `200`.

## 3. First Login

Open `http://localhost:8080`. The login screen accepts the `OPSTAGE_ADMIN_USERNAME` / `OPSTAGE_ADMIN_PASSWORD` you generated above. The Backend created the admin user on first boot and will NOT overwrite it on later boots even if the env values change (per ADR 0004).

After login, the dashboard shows zero Agents and zero Capsule Services.

## 4. Connecting the Demo Capsule Service

Create a registration token in the UI, then run the demo service locally or through a future Compose demo profile. The
current CE repository ships the demo service as a Node workspace app.

```bash
# 1. In the UI, go to Settings → Registration Tokens → Create.
#    Copy the raw token value (shown ONCE).

# 2. Start the demo service from the CE repository root.
OPSTAGE_BACKEND_URL=http://localhost:8080 \
OPSTAGE_REGISTRATION_TOKEN=opstage_reg_... \
OPSTAGE_AGENT_TOKEN_FILE=./data/demo-agent-token.json \
pnpm --filter @xtrape/demo-capsule-service start
```

The demo service registers itself on first start. The Agent token is persisted in `OPSTAGE_AGENT_TOKEN_FILE`, so
subsequent restarts skip registration while that file remains valid.

Within one heartbeat cycle, the demo service appears in the UI under Capsule Services with status `HEALTHY`.

## 5. Run an Action

In the UI:

1. Open Capsule Services → `demo-capsule-service` → Actions.
2. Click the `echo` action.
3. Enter a JSON payload, for example `{ "message": "hello" }`.
4. Submit. UI navigates to or shows the new Command detail.
5. The Agent polls the Command and it moves `PENDING → RUNNING → SUCCEEDED`.
6. Run `runHealthCheck` to verify an action can call the registered health provider.

The Audit Events tab now contains action/command lifecycle rows for the request and completion.

## 6. Tear Down

```bash
docker compose down                  # stops containers, keeps data volume
docker compose down -v               # also removes the SQLite + agent-token volume
```

## 7. Upgrading

```bash
docker compose pull
docker compose up -d
```

The container runs Prisma migrations at startup. CE v0.1 follows additive-only schema changes; downgrading IS NOT supported.

## 8. Production Notes

CE v0.1 is intended for self-host evaluation, internal tools, and small ops teams.

- ALWAYS terminate TLS in front of Opstage (Caddy / nginx / cloud LB). The Backend trusts `X-Forwarded-Proto: https` to switch the session cookie to `Secure`.
- Set `OPSTAGE_PUBLIC_BASE_URL` to the canonical HTTPS URL before exposing the UI.
- Mount `/app/data` as a persistent volume; losing it loses all state including Agent tokens.
- Back up the SQLite file with the container stopped (or `sqlite3 .backup`).
- Rotate `OPSTAGE_SESSION_SECRET` only when prepared for all admin sessions to be invalidated.

## 9. Troubleshooting

| Symptom                                      | Likely cause                              | Fix                                                            |
|----------------------------------------------|-------------------------------------------|----------------------------------------------------------------|
| Container exits with `OPSTAGE_*_REQUIRED`    | Env var missing from `.env`               | See §2; restart with full `.env`.                              |
| UI shows "Network error" right after login   | Reverse proxy strips `Set-Cookie`         | Allow cookies on proxy, ensure `Domain` matches the public URL.|
| `403 CSRF_INVALID` on every POST             | `X-CSRF-Token` not forwarded by proxy     | Add `X-CSRF-Token` to allowed request headers.                 |
| Agent registers but immediately goes OFFLINE | Backend clock vs Agent clock skew         | Synchronise both via NTP; CE assumes ≤ 30 s drift.             |
| `409 SERVICE_HAS_NO_AGENT` on action click   | Service was deregistered                  | Restart the demo, wait one heartbeat.                          |

## 10. Next Steps

- Read `04-opstage/04-command-and-action-model.md` to learn the command/action lifecycle.
- Read `05-agents/04-node-agent-sdk.md` and `10-implementation/10-user-and-ops-manual.md` to embed and operate the Node Agent SDK.
- Review `08-decisions/0004-security-defaults.md` before exposing Opstage to the public internet.
