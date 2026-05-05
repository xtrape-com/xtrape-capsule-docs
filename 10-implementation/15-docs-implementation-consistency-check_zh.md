# 文档 / 实现一致性检查

- Status: Implementation Guidance
- Edition: CE
- Priority: Current
- Audience: maintainers, reviewers, AI coding agents

当 Opstage CE 的 command、action、Agent、config 或 UI 行为变化时，使用本 checklist 检查文档和实现是否一致。

---

## 1. Source of Truth 顺序

文档冲突时按以下优先级处理：

```text
1. 08-decisions/ 中的 ADR
2. 02-specs/ 和 09-contracts/ 中的 contracts/specs
3. 10-implementation/ 中的 implementation guides
4. 04-opstage/ 和 05-agents/ 中的 Opstage / Agent guides
5. README / quickstart / examples
```

不要在不更新设计的情况下让实现静默偏离 ADR 或 contracts。必要时先更新已接受设计，或新增 decision record。

---

## 2. 当前 CE 需要保持一致的行为

以下已实现行为必须保持文档同步：

| 领域 | 已实现行为 | 主要文档 |
|---|---|---|
| Action Catalog | Service report 只携带稳定的 action 按钮 metadata。 | `02-specs/05-action-spec*`, `10-implementation/13-service-action-design-guide*` |
| Prepare | 打开 action panel 通过 GET 创建 `ACTION_PREPARE`。 | `02-specs/05-action-spec*`, `02-specs/07-command-spec*` |
| Execute | 执行 action 通过 POST 创建 `ACTION_EXECUTE`。 | `02-specs/05-action-spec*`, `04-opstage/04-command-and-action-model*` |
| Prepare diagnostics | Prepare 失败/超时时返回非敏感 `error.details`。 | `02-specs/05-action-spec*` |
| Result list | `data.list` 可渲染为表格，支持 columns、formats、rowActions、emptyText、pageSize。 | `02-specs/05-action-spec*`, `10-implementation/13-service-action-design-guide*` |
| Row action refresh | UI 可在 row action 完成后刷新当前 list。 | `02-specs/05-action-spec*` |
| Command polling limit | Agent poll command 可带 `limit`，backend 会限制到安全范围。 | `02-specs/07-command-spec*` |
| Agent execution locks | Agent 可按资源/action 类型应用更严格内部锁。 | `02-specs/07-command-spec*` |
| Service health report | 启动/catalog 变化上报完整 service report；heartbeat 可携带 service health。 | `02-specs/03-agent-registration-spec*`, `02-specs/04-health-spec*` |
| Secrets | Secret 脱敏；一次性生成 secret 必须明确设计。 | `02-specs/06-config-spec*`, `08-decisions/0004-security-defaults*` |

---

## 3. Review Checklist

每次相关实现变化时检查：

- [ ] Backend tests 覆盖新行为或失败模式。
- [ ] UI tests/typecheck 覆盖变化的渲染或 helper 逻辑。
- [ ] 英文和中文文档都已更新。
- [ ] Action spec 示例仍与实现一致。
- [ ] Command spec 生命周期仍与实现一致。
- [ ] Ops manual 说明了操作员可见行为。
- [ ] Smoke test runbook 仍可执行。
- [ ] 任意 OpenAPI/error-code 变化后，`pnpm contracts:check` 通过。
- [ ] 敏感数据和 error details 仍被脱敏。
- [ ] 文档中的默认值与代码默认值一致。
- [ ] 新增环境变量已记录。

---

## 4. 快速命令

在 `xtrape-capsule-ce` 中：

```bash
pnpm --filter @xtrape/opstage-backend typecheck
pnpm --filter @xtrape/opstage-backend test
pnpm --filter @xtrape/opstage-ui typecheck
pnpm --filter @xtrape/opstage-ui test
pnpm smoke:ui
pnpm contracts:check
```

在 `xtrape-capsule-docs` 中：

```bash
git diff -- 02-specs 04-opstage 05-agents 10-implementation
```

当变化影响共享行为时，手动确认英文和 `_zh` 文件都已更新。
