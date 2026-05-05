# Capsule Service Action 设计指南

- Status: Implementation Guidance
- Edition: Shared / CE-first
- Priority: High
- Audience: Capsule Service developers, Agent SDK developers, Opstage UI developers, AI coding agents

本文把 Action 和 Command 规范整理成面向 Service 开发者的实践规则。

建议结合以下文档阅读：

```text
02-specs/05-action-spec_zh.md
02-specs/07-command-spec_zh.md
04-opstage/04-command-and-action-model_zh.md
```

---

## 1. 核心模型

每个 service action 分为两个阶段：

| 阶段 | HTTP | Command type | 职责 |
|---|---|---|---|
| Prepare | `GET /api/admin/capsule-services/{serviceId}/actions/{actionName}` | `ACTION_PREPARE` | 生成动态 UI metadata、默认 payload、枚举选项、当前状态。不能执行业务操作。 |
| Execute | `POST /api/admin/capsule-services/{serviceId}/actions/{actionName}` | `ACTION_EXECUTE` | 校验 payload 并执行真正操作。 |

service report 只发布 **Action Catalog**。动态表单细节应由 prepare 返回。

---

## 2. Action Catalog 规则

Action Catalog 应保持稳定且较小。它用于在 action 面板打开前渲染按钮和分组。

推荐字段：

```json
{
  "name": "listAccounts",
  "label": "List Accounts",
  "description": "View account status.",
  "category": "account",
  "order": 10,
  "dangerLevel": "LOW",
  "requiresConfirmation": false,
  "timeoutSeconds": 30,
  "enabled": true
}
```

规则：

- `name` 应保持稳定；修改它会影响旧 Command 和 row action。
- 用 `category` 做 UI 分组，例如 `account`、`api-key`、`session`、`runtime-config`、`diagnostics`、`advanced`。
- 用 `order` 做稳定排序。
- 破坏性、安全敏感或长耗时操作应设置 `requiresConfirmation: true`。
- 不要在周期性 service report 中放大账号列表、配置值或运行态状态。

---

## 3. Prepare Handler 规则

Prepare 在操作员打开 action 面板时执行。

Prepare 应返回：

```json
{
  "action": {
    "name": "rebuildAccountContext",
    "label": "Rebuild Account Browser Context",
    "requiresConfirmation": true,
    "inputSchema": {
      "type": "object",
      "required": ["accountId"],
      "properties": {
        "accountId": {
          "type": "string",
          "title": "Account",
          "enum": ["account-a37c76affd5b"],
          "enumLabels": ["account-a37c76affd5b (ethan.w….com)"]
        },
        "clearCooldown": {
          "type": "boolean",
          "title": "Clear Cooldown",
          "default": true
        }
      }
    }
  },
  "initialPayload": {
    "accountId": "account-a37c76affd5b",
    "clearCooldown": true
  },
  "currentState": {
    "accounts": []
  }
}
```

Prepare 必须：

- 可安全重试；
- 不产生业务副作用；
- 根据当前状态生成动态 enum；
- 生成初始 payload 默认值；
- 避免返回 secret。

Prepare 应该：

- 为字段提供有用的 `title` 和 `description`；
- secret 输入使用 `format: "password"`；
- 多行值使用 `format: "textarea"`；
- 使用 `enumLabels` 展示可读的账号/配置/API-key 选项；
- 资源不存在时返回空选项和清晰说明，而不是直接失败。

---

## 4. Execute Handler 规则

Execute 接收 action panel 生成或编辑后的 payload。

Execute 必须：

- 重新校验所有 required 字段；
- 在 service/agent 侧强制校验类型和 enum；
- 检查资源是否存在以及是否属于当前服务；
- 在日志、审计 metadata 和结果中脱敏 secret；
- 返回有边界的结果数据；
- 失败时返回清晰的 `error.code`。

成功结果示例：

```json
{
  "success": true,
  "message": "Account disabled.",
  "data": {
    "accountId": "account-a37c76affd5b"
  }
}
```

失败结果示例：

```json
{
  "success": false,
  "message": "Account not found.",
  "error": {
    "code": "ACCOUNT_NOT_FOUND"
  }
}
```

---

## 5. List Action 设计

List action 应同时返回原始数据和展示 metadata：

```json
{
  "success": true,
  "data": {
    "accounts": [],
    "list": {
      "title": "Accounts",
      "emptyText": "No accounts",
      "pageSize": 10,
      "data": [],
      "columns": [
        { "key": "label", "label": "Account", "format": "code", "copyable": true, "ellipsis": true },
        { "key": "enabled", "label": "Enabled", "format": "boolean" },
        { "key": "loginState", "label": "Login State", "format": "status" },
        { "key": "cooldownRemainingMs", "label": "Cooldown", "format": "duration" }
      ],
      "rowActions": [
        {
          "label": "Disable",
          "action": "disableAccount",
          "payload": { "accountId": "$row.id" },
          "danger": true,
          "confirm": true
        }
      ]
    }
  }
}
```

规则：

- 保留原始数据，便于 API/debug 兼容。
- UI 表格 metadata 放在 `data.list` 下。
- `rowActions` 只是普通 action 上的 UI 便利层。
- row action payload 模板应引用稳定的 row 字段。
- list 筛选条件应作为普通 `inputSchema` 字段在 prepare 中设计。

---

## 6. 长任务 Action 设计

示例：登录、重建浏览器上下文、数据库迁移、远程同步。

规则：

- `timeoutSeconds` 应覆盖预期执行时间。
- 影响 session、credential、账号可用性或数据完整性的操作应设置 `requiresConfirmation: true`。
- 除非明确设计为异步并有进度可见，否则不要过早返回成功。
- 能更新 health/current state 时，应在运行中持续更新。
- 通过 list action 或 health details 暴露状态，例如 `operationStatus`、`operationName`、`operationMessage`、`operationStartedAt`。

推荐基础状态：

```text
IDLE
RUNNING
SUCCEEDED
FAILED
```

也可以在 list rows 或 health details 中增加领域状态，例如 `loginState`。

---

## 7. 安全和敏感数据

以下位置绝不能返回 raw secret：

- service report；
- health details；
- action prepare result；
- command result，除非是明确设计为只展示一次的一次性生成 secret；
- audit metadata；
- logs。

一次性生成 secret 可以返回清晰命名字段，例如 `generatedKey`，并说明只显示一次。

常用 UI hints：

| Hint | 用途 |
|---|---|
| `format: "password"` | 密码、app password、API token、private key。 |
| config metadata 中的 `sensitive: true` | 不能 preview 的配置值。 |
| `secretRef` | 外部 secret 引用，而不是 secret 本身。 |

---

## 8. 并发和资源锁

Agent 应把 command polling `limit` 设置为本地剩余执行容量。

Agent 仍可以在内部应用更严格的资源锁：

| Action class | 建议锁 |
|---|---|
| 只读 list/config/API-key metadata | 可并发执行。 |
| Browser/session/login/account context | 按 service 或 account 串行。 |
| 破坏性数据操作 | 按受影响资源串行。 |

Backend command model 负责记录执行过程；Agent 负责本地运行时安全。

---

## 9. Checklist

新增 action 前检查：

- [ ] Catalog 字段稳定且较小。
- [ ] Prepare 无副作用。
- [ ] Prepare 返回 label、description、default 和动态 enum。
- [ ] Execute 独立校验 payload。
- [ ] Result 有大小边界，且不泄漏 secret。
- [ ] 长任务状态能通过 command status、health 或 list rows 观察。
- [ ] Row actions 调用已有普通 actions。
- [ ] 文档示例已同步更新。
