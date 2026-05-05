---
status: draft
audience: founders
stability: unstable
last_reviewed: 2026-05-05
edition: ce
phase: current
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 05-ce-deployment-model.md
翻译状态 / Translation Status: 已翻译 / Translated
生成时间 / Generated: 2026-05-01 09:28:53
================================================================================
注意 / Notes:
- 技术术语如 Capsule Service、Agent、Opstage 等保留英文或采用中英对照
- 代码块中的内容不翻译
- 文件路径和 URL 不翻译
- 保持原有的 Markdown 格式结构
================================================================================
-->

# CE（社区版） 部署 Model

- Status: 实现 Target
- Edition: CE（社区版）
- Priority: Current
- Audience: architects, backend developers, frontend developers, DevOps engineers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/0004-security-defaults.md` or `09-contracts/` disagree, the ADRs and contracts win for CE（社区版） v0.1.

This document 定义 the deployment model for **Opstage（运维舞台） CE（社区版） v0.1**.

CE（社区版） deployment should be lightweight, self-hosted, easy to start, and suitable for open-source community users. It
should not require Kubernetes, external databases, message queues, or cloud services for the first version.

---

## 1. 部署 Goal

The goal of CE（社区版） deployment is:

> A developer or small team can run Opstage（运维舞台） CE（社区版） locally or on a small private server with minimal operational overhead.

The preferred first deployment experience should be:

```text
single container
single exposed port
SQLite data volume
no external SaaS dependency
```

CE（社区版） should also support local development with separate Backend, UI, and demo service processes.

---

## 2. 部署 Principles

CE（社区版） v0.1 deployment should follow these principles:

1. Keep the first deployment simple.
2. Use SQLite by default.
3. Use a persistent data volume.
4. Expose only one HTTP port for Opstage（运维舞台） CE（社区版） by default.
5. Do not require Kubernetes.
6. Do not require Redis, RabbitMQ, Kafka, or other queues.
7. Do not require MySQL/PostgreSQL in CE（社区版） v0.1.
8. Do not require external SaaS services.
9. Keep the Agent（代理） connection outbound-first.
10. Preserve future paths for EE（企业版） and Cloud（云版） deployment models.

---

## 3. Supported 部署 Modes

CE（社区版） v0.1 should support three deployment modes.

### 3.1 Local development mode

Used by developers working on the project.

```text
Developer Machine
├── Backend dev server
├── UI dev server
├── SQLite local database file
└── Demo Capsule Service process
```

This mode should support hot reload or fast rebuilds.

### 3.2 Single-container mode

Primary user-facing deployment mode for CE（社区版） v0.1.

```text
Docker Host
└── opstage-ce container
    ├── Backend server
    ├── built UI static assets
    └── SQLite database file mounted from volume
```

This mode is recommended for most CE（社区版） users.

### 3.3 Docker Compose mode

Optional convenience mode.

Useful when running Opstage（运维舞台） CE（社区版） together with a demo Capsule Service（胶囊服务）.

```text
Docker Host
├── opstage-ce container
│   ├── Backend
│   ├── UI static assets
│   └── SQLite data volume
└── demo-capsule-service container
    └── Node.js Embedded Agent SDK
```

Docker Compose is optional but recommended for examples and development demos.

---

## 4. Local 开发 Mode

### 4.1 Purpose

Local development mode is for contributors and developers.

It should make it easy to run:

- Backend;
- UI;
- Agent（代理） SDK package;
- demo Capsule Service（胶囊服务）;
- SQLite database.

### 4.2 Recommended commands

Example commands:

```bash
pnpm install
pnpm dev
```

or separate commands:

```bash
pnpm --filter @xtrape/opstage-backend dev
pnpm --filter @xtrape/opstage-ui dev
pnpm --filter @xtrape/demo-capsule-service dev
```

Exact package names may change, but the README should provide simple commands.

### 4.3 Local development ports

Recommended default ports:

```text
Backend: 8080
UI dev server: 5173
Demo Capsule Service: 3101 if it exposes any local endpoint
```

The demo Capsule Service（胶囊服务） may not need to expose a public port if it uses only embedded Agent（代理） communication.

---

## 5. Single-Container Mode

### 5.1 Purpose

Single-container mode is the preferred CE（社区版） user deployment.

It should package:

- Backend server;
- built UI static assets;
- Prisma client and migrations;
- runtime configuration;
- SQLite data path.

### 5.2 Target user command

Preferred first command:

```bash
# Generate strong values first; never use literal placeholders in production.
ADMIN_PASS="$(openssl rand -base64 24)"
SESSION_SECRET="$(openssl rand -base64 32)"

docker run \
  -p 8080:8080 \
  -v ./opstage-data:/app/data \
  -e OPSTAGE_ADMIN_USERNAME=admin \
  -e OPSTAGE_ADMIN_PASSWORD="$ADMIN_PASS" \
  -e OPSTAGE_SESSION_SECRET="$SESSION_SECRET" \
  ghcr.io/xtrape/opstage-ce:v0.1.0
```

The Backend refuses to start when `OPSTAGE_ADMIN_PASSWORD` or `OPSTAGE_SESSION_SECRET` is empty (see ADR 0004 §"Bootstrap"). There is no built-in default password.

### 5.3 Container responsibilities

The container should:

1. start Backend server;
2. serve built UI static assets;
3. initialize or migrate SQLite database;
4. create default Workspace if missing;
5. bootstrap admin user if configured;
6. expose one HTTP port.

### 5.4 Internal process model

CE（社区版） v0.1 may run as one Node.js process serving both Admin APIs, Agent（代理） APIs, and UI static assets.

Recommended structure:

```text
Node.js server
├── Admin API
├── Agent API
├── static UI assets
└── SQLite access
```

This is acceptable for CE（社区版） v0.1.

Future EE（企业版） may split UI and Backend.

---

## 6. Docker Compose Mode

### 6.1 Purpose

Docker Compose mode is useful for:

- demo setup;
- local smoke testing;
- documentation examples;
- users who prefer declarative deployment.

### 6.2 Example compose shape

```yaml
services:
  opstage:
    image: ghcr.io/xtrape/opstage-ce:v0.1.0
    ports:
      - "8080:8080"
    volumes:
      - opstage-data:/app/data
    environment:
      OPSTAGE_PORT: "8080"
      OPSTAGE_DATABASE_URL: "file:/app/data/opstage.db"
      OPSTAGE_ADMIN_USERNAME: "admin"
      # Required: source these from a .env file or secrets manager. Backend exits if either is empty.
      OPSTAGE_ADMIN_PASSWORD: "${OPSTAGE_ADMIN_PASSWORD:?required}"
      OPSTAGE_SESSION_SECRET: "${OPSTAGE_SESSION_SECRET:?required}"

  demo-capsule-service:
    image: xtrape/demo-capsule-service:0.1.0
    environment:
      OPSTAGE_BACKEND_URL: "http://opstage:8080"
      OPSTAGE_REGISTRATION_TOKEN: "opstage_reg_xxx"
    depends_on:
      - opstage

volumes:
  opstage-data:
```

The registration token may be created manually in UI, bootstrapped through environment variables, or generated through a setup command depending on implementation.

---

## 7. Data Persistence

### 7.1 SQLite database path

Recommended default path inside container:

```text
/app/data/opstage.db
```

Recommended environment variable:

```text
OPSTAGE_DATABASE_URL=file:/app/data/opstage.db
```

### 7.2 Data volume

The `/app/data` directory should be mounted as a persistent volume.

Example:

```bash
-v ./opstage-data:/app/data
```

### 7.3 Data stored in volume

The data volume may contain:

```text
opstage.db
migration metadata
uploaded or generated local files if needed later
```

CE（社区版） v0.1 should avoid storing large logs or large binary files in the SQLite database.

---

## 8. Database Migration

CE（社区版） v0.1 should provide a simple migration mechanism.

Recommended behavior:

```text
Container starts
    ↓
Backend checks database schema
    ↓
Backend runs pending migrations
    ↓
Backend starts HTTP server
```

Alternative:

```text
explicit migration command
```

The first CE（社区版） version may run migrations on startup if it is reliable and clearly documented.

### 8.1 Migration rules

- migrations should be deterministic;
- migrations should not delete user data without explicit warning;
- schema should remain portable toward MySQL/PostgreSQL where practical;
- migration failures should stop startup and log clear errors.

---

## 9. Bootstrap and Setup

CE（社区版） v0.1 needs a simple first-run setup.

### 9.1 Required bootstrap objects

On first run, Backend should create:

```text
Default Workspace
Admin user
System settings defaults
```

### 9.2 Admin user bootstrap

Required environment variables (no defaults):

```text
OPSTAGE_ADMIN_USERNAME=<required>
OPSTAGE_ADMIN_PASSWORD=<required, plain text on first run only>
OPSTAGE_SESSION_SECRET=<required, >=32 random bytes>
```

Rules (matches ADR 0004):

- Backend MUST refuse to start when any required variable is missing or empty;
- if admin user does not exist, create it with hashed password (argon2id or bcrypt);
- if admin user already exists, never overwrite the password automatically;
- there is no built-in default password — operators MUST set their own value;
- after first successful login, operators are encouraged to remove `OPSTAGE_ADMIN_PASSWORD` from the environment (the hash is already persisted in the database).

### 9.3 Registration token bootstrap

CE（社区版） v0.1 may support one of these approaches:

1. create registration token from UI after login;
2. create registration token through CLI/setup command;
3. bootstrap an initial registration token through environment variable.

Recommended for MVP:

```text
UI or setup page creates registration token after admin login.
```

Environment-based bootstrap is acceptable for demos but should be handled carefully.

---

## 10. Environment Variables

Opstage（运维舞台） CE（社区版） environment variables:

```text
# ---- required, no defaults (Backend exits if missing) ----
OPSTAGE_ADMIN_USERNAME=<required>
OPSTAGE_ADMIN_PASSWORD=<required>
OPSTAGE_SESSION_SECRET=<required, >=32 random bytes>

# ---- optional with defaults ----
OPSTAGE_PORT=8080
OPSTAGE_DATABASE_URL=file:/app/data/opstage.db
OPSTAGE_AGENT_HEARTBEAT_INTERVAL_SECONDS=30
OPSTAGE_AGENT_OFFLINE_THRESHOLD_SECONDS=90
OPSTAGE_COMMAND_POLL_INTERVAL_SECONDS=5
OPSTAGE_COMMAND_TTL_SECONDS=300
OPSTAGE_LOG_LEVEL=info
```

Recommended demo Capsule Service（胶囊服务） environment variables:

```text
OPSTAGE_BACKEND_URL=http://localhost:8080
OPSTAGE_REGISTRATION_TOKEN=opstage_reg_xxx
OPSTAGE_AGENT_TOKEN_FILE=./data/agent-token.json
DEMO_MESSAGE=hello capsule
```

---

## 11. Networking Model

### 11.1 Opstage（运维舞台） CE（社区版） exposed port

Default exposed port:

```text
8080
```

This port serves:

- UI;
- Admin APIs;
- Agent（代理） APIs.

### 11.2 Agent（代理） communication

Agents connect outbound to Opstage（运维舞台） Backend.

```text
Agent -> Opstage Backend
```

CE（社区版） v0.1 should not require Opstage（运维舞台） Backend to connect inbound to Agents.

This 支持:

- local machines;
- NAT environments;
- private servers;
- future Cloud（云版） model;
- fewer exposed service ports.

### 11.3 Reverse proxy

Users may put Opstage（运维舞台） CE（社区版） behind a reverse proxy such as Nginx, Caddy, or Traefik.

This is optional and not required for CE（社区版） v0.1 quick start.

---

## 12. HTTPS

CE（社区版） v0.1 local development may use HTTP.

For production-like self-hosted usage, users should run Opstage（运维舞台） CE（社区版） behind HTTPS using a reverse proxy.

CE（社区版） v0.1 does not need to implement built-in certificate management.

Future EE（企业版）/Cloud（云版） may provide stronger TLS and certificate management guidance.

---

## 13. Upgrade Model

CE（社区版） v0.1 should keep upgrade simple.

Recommended upgrade steps:

```text
1. Stop container.
2. Backup data volume.
3. Pull new image.
4. Start new container.
5. Run migrations automatically or explicitly.
```

### 13.1 Backup before upgrade

Users should back up:

```text
/app/data/opstage.db
```

before upgrade.

### 13.2 Versioning

Use semantic versioning for CE（社区版） images:

```text
0.1.0
0.1.1
0.2.0
```

---

## 14. Backup and Restore

### 14.1 Backup

Basic backup:

```bash
cp ./opstage-data/opstage.db ./backup/opstage-$(date +%Y%m%d).db
```

If container is running, SQLite backup should ideally be done with a safe SQLite backup command or while the container is stopped.

### 14.2 Restore

Basic restore:

```text
1. Stop Opstage CE.
2. Replace opstage.db with backup file.
3. Start Opstage CE.
```

CE（社区版） v0.1 does not need a built-in backup UI.

---

## 15. Observability for 部署

CE（社区版） v0.1 should provide simple operational visibility.

Required:

- application logs to stdout/stderr;
- health endpoint for Opstage（运维舞台） Backend if practical;
- clear startup logs;
- clear migration logs;
- clear errors for database path issues.

Optional endpoint:

```http
GET /api/system/health
```

Response example:

```json
{
  "status": "UP",
  "version": "0.1.0",
  "database": "UP"
}
```

CE（社区版） v0.1 does not need Prometheus metrics or centralized log collection.

---

## 16. Resource Requirements

CE（社区版） v0.1 should run comfortably on small servers.

Recommended minimum target:

```text
CPU: 1 core
Memory: 512 MB to 1 GB
Disk: depends on audit and command history, start with 1 GB+
```

Practical recommendation:

```text
CPU: 2 cores
Memory: 2 GB
Disk: 5 GB+
```

This is not a hard limit, but it should guide implementation choices.

---

## 17. 部署 安全

CE（社区版） v0.1 deployment should follow these rules:

- do not ship with a fixed default admin password;
- require users to provide or change admin password;
- require `OPSTAGE_SESSION_SECRET` or generate a safe local secret;
- store tokens as hashes;
- do not log raw tokens;
- do not log raw passwords;
- do not expose SQLite file publicly;
- recommend HTTPS behind reverse proxy for production-like use;
- allow Agent（代理） APIs only with valid Agent（代理） token.

---

## 18. Out of Scope for CE（社区版） v0.1 部署

The following are out of scope:

- Kubernetes Helm chart;
- high availability deployment;
- multi-node Backend cluster;
- external managed database requirement;
- Redis/RabbitMQ/Kafka requirement;
- built-in TLS certificate management;
- built-in backup scheduler;
- built-in log aggregation;
- multi-tenant SaaS deployment;
- Cloud（云版） Agent（代理） Gateway.

Future EE（企业版）/Cloud（云版） may add these capabilities.

---

## 19. Future 部署 Paths

CE（社区版） deployment should preserve future upgrade paths.

||Area|CE（社区版） v0.1|Future EE（企业版） / Cloud（云版）||
|---|---|---|
||Process|single process|split UI, Backend, workers||
||Database|SQLite|MySQL, PostgreSQL, managed DB||
||部署|single container|Docker Compose, Helm, cluster||
||Command channel|polling|WebSocket, gRPC, queue||
||Storage|local volume|managed persistent storage||
||Logs|stdout/stderr|centralized logging||
||Metrics|optional health endpoint|metrics and dashboards||
||HTTPS|reverse proxy|managed TLS or ingress||
||Backup|manual|scheduled backup and restore||

---

## 20. 部署 Acceptance Criteria

CE（社区版） v0.1 deployment is acceptable when:

- Opstage（运维舞台） CE（社区版） can run locally in development mode;
- Opstage（运维舞台） CE（社区版） can run as a single Docker container;
- UI is served correctly;
- Backend APIs work in the container;
- SQLite data persists across container restarts;
- admin user can be bootstrapped;
- demo Capsule Service（胶囊服务） can connect to Backend;
- Agent（代理） heartbeat and command polling work across container network;
- logs are visible through container logs;
- documentation 提供 quick-start commands.

---

## 21. Summary

Opstage（运维舞台） CE（社区版） deployment should optimize for simplicity and trust.

The first deployment model should be:

```text
single container
single port
SQLite volume
outbound Agent connection
```

The most important deployment rule is:

> CE（社区版） should be easy to run before it becomes powerful to operate at scale.
