<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 07-quickstart.md
翻译状态 / Translation Status: 已翻译 / Translated
生成时间 / Generated: 2026-05-01 09:28:55
================================================================================
注意 / Notes:
- 技术术语如 Capsule Service、Agent、Opstage 等保留英文或采用中英对照
- 代码块中的内容不翻译
- 文件路径和 URL 不翻译
- 保持原有的 Markdown 格式结构
================================================================================
-->

# CE（社区版） v0.1 Quickstart

- Status: 实施指南
- Edition: CE（社区版）
- Priority: Current
- Audience: open-source users, evaluators, founders, backend developers, frontend developers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/openapi/opstage-ce-v0.1.yaml` disagree, the ADRs and OpenAPI contract win for CE（社区版） v0.1.

This document is the canonical "first 10 minutes" experience for Opstage（运维舞台） CE（社区版）. The implementation MUST keep the published `README.md` of the repo in sync with the steps below.

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

Compose 部署必须在缺少三个必需环境变量时拒绝启动（per ADR 0004）。容器 ready 后，`docker compose ps` 会显示 `opstage` service healthy，此时 `GET /api/system/health` 返回 `200`。

## 3. First Login

Open `http://localhost:8080`. The login screen accepts the `OPSTAGE_ADMIN_USERNAME` / `OPSTAGE_ADMIN_PASSWORD` you generated above. The Backend created the admin user on first boot and will NOT overwrite it on later boots even if the env values change (per ADR 0004).

After login, the dashboard shows zero Agents and zero Capsule Services.

## 4. Connecting the Demo Capsule Service（胶囊服务）

```bash
# Still in deploy/compose
# 1. In the UI, go to Settings → Registration Tokens → Create.
#    Copy the rawToken value (shown ONCE).
export OPSTAGE_REGISTRATION_TOKEN="opstage_reg_..."

# 2. Start the demo service container
docker compose --profile demo up -d
```

The demo container (defined in `deploy/compose/compose.yaml` under the `demo` profile) reads `OPSTAGE_REGISTRATION_TOKEN` from `.env` and registers itself on first start. The Agent（代理） token is then persisted in the `demo-data` volume so subsequent restarts skip registration.

Within ~30 seconds (one heartbeat cycle), the demo service appears in the UI under Capsule Services with status `HEALTHY`.

## 5. 执行 Action

在 UI 中：

1. 打开 Capsule Services → `demo-capsule-service` → Actions。
2. 点击 `echo` action。
3. 输入 JSON payload，例如 `{ "message": "hello" }`。
4. 提交后，UI 会跳转或展示新的 Command 详情。
5. Agent poll Command 后，状态会从 `PENDING → RUNNING → SUCCEEDED`。
6. 执行 `runHealthCheck`，验证 action 可以调用已注册的 health provider。

Audit Events 页面会出现该 action/command 生命周期相关审计记录。

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

The container runs Prisma migrations at startup. CE（社区版） v0.1 follows additive-only schema changes; downgrading IS NOT supported.

## 8. 生产 Notes

CE（社区版） v0.1 is intended for self-host evaluation, internal tools, and small ops teams.

- ALWAYS terminate TLS in front of Opstage（运维舞台） (Caddy / nginx / cloud LB). The Backend trusts `X-Forwarded-Proto: https` to switch the session cookie to `Secure`.
- Set `OPSTAGE_PUBLIC_BASE_URL` to the canonical HTTPS URL before exposing the UI.
- Mount `/app/data` as a persistent volume; losing it loses all state including Agent（代理） tokens.
- Back up the SQLite file with the container stopped (or `sqlite3 .backup`).
- Rotate `OPSTAGE_SESSION_SECRET` only when prepared for all admin sessions to be invalidated.

## 9. Troubleshooting

||Symptom|Likely cause|Fix||
|----------------------------------------------|-------------------------------------------|----------------------------------------------------------------|
||Container exits with `OPSTAGE_*_REQUIRED`|Env var missing from `.env`|See §2; restart with full `.env`.||
||UI shows "Network error" right after login|Reverse proxy strips `Set-Cookie`|Allow cookies on proxy, ensure `Domain` matches the public URL.||
||`403 CSRF_INVALID` on every POST|`X-CSRF-Token` not forwarded by proxy|Add `X-CSRF-Token` to allowed request headers.||
||Agent（代理） registers but immediately goes OFFLINE|Backend clock vs Agent（代理） clock skew|Synchronise both via NTP; CE（社区版） assumes ≤ 30 s drift.||
||`409 SERVICE_HAS_NO_AGENT` on action click|Service was deregistered|Restart the demo, wait one heartbeat.||

## 10. Next Steps

- Read `04-opstage/04-command-and-action-model.md` to learn the command/action lifecycle.
- Read `05-agents/04-node-agent-sdk.md` to embed the Node Agent（代理） SDK in your own service.
- Review `08-decisions/0004-security-defaults.md` before exposing Opstage（运维舞台） to the public internet.
