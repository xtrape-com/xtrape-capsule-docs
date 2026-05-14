---
status: accepted
audience: ai-coding-agents
stability: stable
last_reviewed: 2026-05-14
translation: machine-assisted
---

# ADR 0010:一次性 Action 密钥(临时生成密钥)

## 状态

已采纳(CE v0.2)

## 日期

2026-05-14

## 背景

部分 Capsule action handler 会生成新密钥——注册令牌、轮换的 API key、一次性口令、临时会话凭据——操作员需要**仅有一次**机会读取该值。

最朴素的做法(持久化到 `command_results.body`,读取时再 redact)有两个泄漏点:

1. 任何能拿到数据库的人都能从备份里恢复明文;
2. 审计子系统本身就会写 `command_results` 行,明文会落到与审计保留期相同的磁盘文件中。

另一个极端(完全不持久化,只在 POST 同步响应里返回)又破坏了长轮询/异步命令模型——Opstage UI 取命令状态是和 dispatch 调用分开的,modal 刷新就会丢值。

v0.1 实现选择把明文存到 `command_results.body.data.generatedKey`,依赖 redactor 在后续读取中屏蔽,这违反了上面第 1 条。

## 决策

CE v0.2 为 action 生成密钥引入**进程内临时缓存**,独立于 `command_results`:

- 缓存键为 `commandId`,值为 `generatedKey` 明文 + 元数据(`createdAt`、`ttlMs`、`consumerHint`)。
- TTL 默认 5 分钟;缓存按 TTL 过期清理,进程重启即丢失。
- 缓存**进程本地**——不复制、不落盘。CE v0.x 设计上即单节点(见 ADR-0004 安全默认),这一点成立。
- 已认证 owner 首次调用 `GET /api/admin/commands/:id` 时,API 在 `result.data.generatedKey` 返回明文;同一次读取后即从缓存中移除该条目。
- 后续调用 `result.data.generatedKey` 返回字符串字面值 `"[REDACTED]"`。
- 涉及生成密钥的 `command.result.recorded` 审计事件使用基于值的 `redactAuditMetadata`;明文绝不写入 `audit_events.metadata`。
- 从 agent 上报 result 开始,`command_results.body` 中的 `"generatedKey"` 字段始终为 `"[REDACTED]"`,明文从不进入该行。

UI 侧(Opstage 控制台 action modal)在黄色 alert 中一次性展示该值并附复制按钮。操作员若未复制即关闭,值不可恢复。

## 影响

**正面:**

- 数据库备份不含明文。
- 单进程明文暴露窗口被 TTL 限定。
- 行为对操作员易于理解。

**负面:**

- 操作员只有一次复制机会,action handler 应在 `description` 中明确说明。
- 若 CE 进程在 TTL 内重启,缓存丢失,操作必须重跑。
- 在 dispatch 与 modal 显示之间若有第二个已认证读取者读取同一命令,会代替原请求者消费掉密钥。

## 考虑过的替代方案

1. **`command_results` 落盘加密**——需 KMS 或环境变量驻留密钥,超出 v0.x 安全默认(ADR-0004)范围;且仍留下长期密文可供离线破解。否决。
2. **仅在同步 POST 响应中返回**——破坏既有长轮询模型;UI 须对 "generatedKey" action 做特殊路径。否决。
3. **显式过期的持久化**——折中方案;否决,因为它和"明文落盘"风险等价,却增加管道复杂度,相对进程内缓存收益边际。

## 实施备注

- 后端模块:`apps/opstage-backend/src/lib/ephemeral-command-secrets.ts`(CE 仓)。
- Wire 层:`serializeCommand` 中的 result transformer。
- 审计安全:`apps/opstage-backend/src/lib/redactor.ts` 中的 `redactAuditMetadata`(基于值)。
- 站点侧操作员说明:`docs/opstage-ce/admin-ui.md` § Actions and Commands。
- CE 仓 `docs/adr/0001-ephemeral-action-secrets.md` 留有本 ADR 的公开镜像,供未授权访问私库的读者参考。

## 取代 / 被取代

取代任何发出 `generatedKey` 的 action 在 v0.1 的隐式行为(行内明文 + 基于键名的 redactor)。
