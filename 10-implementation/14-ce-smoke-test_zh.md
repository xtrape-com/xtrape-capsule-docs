# CE Smoke Test Runbook

- Status: Implementation Guidance
- Edition: CE
- Priority: Current
- Audience: CE maintainers, QA engineers, operators, AI coding agents

本文用于在 backend、UI、command/action contract 或 Agent 集成改动后，快速验证 Opstage CE 主流程。

---

## 1. 范围

Smoke test 验证：

1. Backend 可启动并暴露 health。
2. UI 可登录。
3. 可创建 registration token。
4. Agent 可注册并在线。
5. Capsule Service 可上报。
6. Action prepare 正常。
7. Action execute 可创建 Command。
8. Agent 可 poll 并回报 CommandResult。
9. 如果 service 支持 result list / row action，可以检查其 UI 体验。
10. Audit events 和 command history 可见。

本文不绑定具体 service。可以使用 demo service、Capi-Chatgpt，或任意至少暴露一个安全 action 的 embedded Agent service。

---

## 2. 预检查

在 `xtrape-capsule-ce` 仓库根目录执行：

```bash
pnpm install
pnpm --filter @xtrape/opstage-backend typecheck
pnpm --filter @xtrape/opstage-backend test
pnpm --filter @xtrape/opstage-ui typecheck
pnpm --filter @xtrape/opstage-ui test
```

期望：

```text
Backend tests pass.
UI tests pass.
No TypeScript errors.
```

### 自动化本地 smoke 脚本

CE 仓库也提供了一个进程内 smoke 脚本。它会使用临时 SQLite 数据库启动 backend，注册 embedded demo Agent，并验证 action prepare、action execute、list result、row action metadata 和敏感配置脱敏：

```bash
cd xtrape-capsule-ce
node --import tsx scripts/smoke-demo.mjs
# 如果你的流程要求先 build，也可以使用：
pnpm smoke:demo
```

当需要验证浏览器/UI 行为或真实外部 service 时，再使用下面的手动步骤。

---

## 3. 本地启动 CE

使用干净的本地数据库进行 smoke test：

```bash
export DATABASE_URL=file:./data/opstage-smoke.db
export OPSTAGE_ADMIN_USERNAME=admin@example.local
export OPSTAGE_ADMIN_PASSWORD=change-me-before-running
export OPSTAGE_SESSION_SECRET=local-smoke-session-secret-at-least-32-chars
export OPSTAGE_STATIC_DIR=apps/opstage-ui/dist

pnpm --filter @xtrape/opstage-ui build
pnpm --filter @xtrape/opstage-backend start
```

Health check：

```bash
curl -s http://localhost:8080/api/system/health | jq .
```

期望：

```json
{ "success": true, "data": { "status": "UP" } }
```

---

## 4. 登录并创建 Registration Token

1. 打开 `http://localhost:8080`。
2. 使用配置的 admin 账号登录。
3. 打开 **Registration Tokens**。
4. 创建 token。
5. 立即复制 raw token；它只展示一次。

期望：

- Registration Tokens 中出现 token row。
- Audit Events 中出现 token 创建事件。

---

## 5. 启动 Agent-backed Service

使用 registration token 启动 service：

```bash
OPSTAGE_BACKEND_URL=http://localhost:8080 \
OPSTAGE_REGISTRATION_TOKEN=opstage_reg_... \
OPSTAGE_AGENT_TOKEN_FILE=./data/smoke-agent-token.json \
<service start command>
```

CE UI 中期望：

- **Agents** 页面出现 Agent。
- Agent 在 polling/heartbeat 后变为 `ONLINE`。
- **Capsule Services** 中出现 Capsule Service。
- Service 展示 manifest、actions、configs 和 health。

如果 service 使用 command polling 作为 heartbeat，至少保持运行一个 polling interval。

---

## 6. 验证 Action Prepare

打开 Capsule Service 详情抽屉，点击一个安全 action。

期望：

- Action panel 打开。
- 短暂显示 prepare loading。
- 动态字段和初始 JSON 被渲染。
- 如果 prepare 失败，面板保持打开，并展示 `commandId`、`commandStatus`、`agentId`、`serviceId` 等诊断信息。

推荐安全 action：

- `runHealthCheck`
- `listAccounts`
- `listApiKeys`
- demo `echo`

---

## 7. 验证 Action Execute

执行一个安全 action。

期望：

- 创建 Command。
- Command 状态从 `PENDING` / `RUNNING` 进入 `SUCCEEDED` 或 `FAILED`。
- Action panel 展示 command result。
- Commands 页面能看到该 command。
- Audit Events 中有 command lifecycle 事件。

对于 list action，检查：

- `data.list` 以表格展示。
- 无数据时空状态可读。
- card 标题显示 row count。
- 原始 result JSON 仍可查看。

---

## 8. 验证 Row Actions

如果 list result 暴露 `rowActions`：

1. 点击一个非破坏性 row action，或在一次性测试环境中点击破坏性 action。
2. 如有确认提示，点击确认。
3. 观察行级 loading 和 disabled 状态。
4. 等待完成。

期望：

- Row action 创建普通 Command。
- action 运行期间该行显示 loading。
- 完成后当前 list 自动刷新。
- 长任务 row action 在 Command 进入终态后刷新列表。

---

## 9. 验证失败场景

推荐失败检查：

| 场景 | 期望结果 |
|---|---|
| 停止 Agent 后打开 action | Backend 返回 agent offline/stale 错误。 |
| Agent 无 token file 且无 registration token 启动 | Service 日志出现配置错误。 |
| 使用 revoked registration token | 注册失败。 |
| 测试 service 强制 prepare 失败 | UI 展示 prepare diagnostics 和 retry。 |
| 返回超大 command result | Backend 返回 `COMMAND_RESULT_TOO_LARGE`。 |

---

## 10. 清理

```bash
# 先停止 service 和 backend。
rm -f ./data/opstage-smoke.db ./data/smoke-agent-token.json
```

如果使用 Docker Compose：

```bash
docker compose down -v
```

---

## 11. 通过标准

满足以下条件即通过：

- CE backend 和 UI 正常启动。
- 登录成功。
- Agent 注册并在运行期间保持在线。
- Capsule Service 上报 actions 和 health。
- 至少一个 prepare 和一个 execute command 成功。
- Command result 可见。
- Audit events 被生成。
- 至少一个负向场景的诊断信息可理解。
