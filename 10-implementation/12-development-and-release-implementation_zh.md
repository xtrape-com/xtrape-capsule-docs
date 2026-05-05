---
status: draft
audience: ai-coding-agents
stability: unstable
last_reviewed: 2026-05-05
edition: ce
phase: current
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

# CE v0.1 开发与发布实现说明

- Status: 实现记录
- Edition: CE
- Priority: Current
- Audience: maintainers, release managers, AI coding agents

本文记录 CE v0.1 分仓后的实现级仓库结构、本地开发、验证和发布流程。

## 1. 仓库拆分

CE v0.1 以多个独立仓库实现：

| Repository | Package | 职责 |
| --- | --- | --- |
| `xtrape-capsule-docs` | n/a | 产品、架构、合约、实现文档。 |
| `xtrape-capsule-contracts-node` | `@xtrape/capsule-contracts-node` | OpenAPI/spec artifacts、Zod schemas、TypeScript types、共享 errors/enums/id helpers。 |
| `xtrape-capsule-agent-node` | `@xtrape/capsule-agent-node` | Node embedded Agent SDK。依赖 contracts package。 |
| `xtrape-capsule-ce` | private app repo | Opstage Backend、UI、demo service、CE 自有 DB/shared/test utilities、Docker/deploy/release artifacts。 |

CE repo 内不得包含 `packages/contracts` 或 `packages/agent-node`。CE 通过 npm semver 依赖消费两个 package：

```text
@xtrape/capsule-contracts-node: ^0.1.0
@xtrape/capsule-agent-node:    ^0.1.0
```

## 2. 本地开发顺序

当修改共享 contracts 时，推荐顺序：

1. 修改 `xtrape-capsule-contracts-node`。
2. 运行 contracts 验证。
3. 修改 `xtrape-capsule-agent-node` 以消费新 contract。
4. 运行 Agent SDK 验证。
5. 修改 `xtrape-capsule-ce` 以消费新的 package 版本。
6. 运行 CE 验证。
7. 发布 packages 后，从 registry 刷新 CE lockfile。

本地验证可以临时使用 symlink，但不得将 `link:` / `file:` 依赖提交到面向 CI/release 的 package manifests 或 lockfiles。

## 3. 验证命令

Contracts package：

```bash
cd xtrape-capsule-contracts-node
pnpm install
pnpm typecheck
pnpm test
pnpm build
```

Agent package：

```bash
cd xtrape-capsule-agent-node
pnpm install
pnpm typecheck
pnpm test
pnpm build
```

CE repo：

```bash
cd xtrape-capsule-ce
pnpm install
pnpm contracts:check
pnpm db:validate
pnpm typecheck
pnpm test
pnpm smoke:demo
pnpm test:docker-smoke
pnpm repo:check
```

如果 SQLite native binding 是在不同 Node 版本下构建的，运行：

```bash
pnpm rebuild better-sqlite3
```

## 4. CE 边界检查

CE 中的 `pnpm contracts:check` 会执行边界检查：

- `packages/contracts` 不存在于 CE。
- `packages/agent-node` 不存在于 CE。
- Backend 使用 npm semver 依赖 `@xtrape/capsule-contracts-node`。
- Demo service 使用 npm semver 依赖 `@xtrape/capsule-agent-node`。

该检查用于防止回退到 all-in-one monorepo 布局。

## 5. 构建输出和忽略文件

生成目录不提交：

```text
node_modules/
dist/
data/
coverage/
*.tsbuildinfo
.env
```

CE Docker build 使用 multi-stage image 编译 Backend/UI/packages，并以单 Backend 进程同时提供 API 和 static UI。

## 6. 发布顺序

干净的 CE v0.1 发布流程：

1. Tag 并发布 `@xtrape/capsule-contracts-node@0.1.0`。
2. Tag 并发布 `@xtrape/capsule-agent-node@0.1.0`。
3. 从 npm registry 刷新 CE install/lockfile。
4. 运行完整 CE 验证。
5. 将 `xtrape-capsule-ce` tag 为 `v0.1.0`。
6. 构建/发布 Docker image。
7. 发布 GitHub release notes。

如果 packages 发布前已经创建 CE release draft，应保持 draft，直到 registry 和 clean-install 验证完成。

## 7. 运行时配置参考

重要 CE 环境变量：

| Variable | Default | Notes |
| --- | --- | --- |
| `OPSTAGE_HOST` | `0.0.0.0` | Backend bind host。 |
| `OPSTAGE_PORT` | `8080` | Backend port。 |
| `DATABASE_URL` | `file:./data/opstage.db` | SQLite database URL。 |
| `OPSTAGE_ADMIN_USERNAME` | none | 首次启动 bootstrap admin 需要。 |
| `OPSTAGE_ADMIN_PASSWORD` | none | 至少 12 字符。 |
| `OPSTAGE_SESSION_SECRET` | none | 至少 32 字符；必需。 |
| `OPSTAGE_SESSION_TTL_SECONDS` | `28800` | Session max age。 |
| `OPSTAGE_STATIC_DIR` | `apps/opstage-ui/dist` | Built UI directory。 |
| `OPSTAGE_AGENT_OFFLINE_THRESHOLD_SECONDS` | `120` | Agent freshness threshold。 |
| `OPSTAGE_AUDIT_RETENTION_DAYS` | `90` | Audit retention。 |
| `OPSTAGE_MAINTENANCE_INTERVAL_SECONDS` | `60` | 后台维护间隔；`0` 关闭 timer。 |
| `OPSTAGE_BACKUP_DIR` | `./data/backups` | SQLite backup 输出目录。 |

Demo/Agent 变量：

| Variable | Notes |
| --- | --- |
| `OPSTAGE_BACKEND_URL` | Agent SDK 访问 Backend 的 base URL。 |
| `OPSTAGE_REGISTRATION_TOKEN` | 首次注册使用的一次性 raw registration token。 |
| `OPSTAGE_AGENT_TOKEN_FILE` | 本地 Agent token 文件路径。 |
| `DEMO_MESSAGE` | Demo service config preview value。 |
