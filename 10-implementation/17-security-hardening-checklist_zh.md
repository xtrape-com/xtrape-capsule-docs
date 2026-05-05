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

# CE 安全部署 Checklist

- Status: Implementation Guidance
- Edition: CE
- Priority: High
- Audience: CE owners, operators, security reviewers, AI coding agents

在把 Opstage CE 暴露到本地开发机之外前，使用本 checklist 检查安全配置。

---

## 1. 必需 Secrets

- [ ] `OPSTAGE_SESSION_SECRET` 是随机值且至少 32 字符。
- [ ] `OPSTAGE_ADMIN_PASSWORD` 已从示例/placeholder 更换，且至少 12 字符。
- [ ] `.env` 未提交到 git。
- [ ] Agent token files 未提交到 git。
- [ ] SQLite backups 未提交到 git。

---

## 2. HTTPS 和反向代理

- [ ] CE 通过 HTTPS 提供服务。
- [ ] 反向代理保留 `Set-Cookie`。
- [ ] 反向代理转发 `X-CSRF-Token`。
- [ ] 对外暴露时，`OPSTAGE_PUBLIC_BASE_URL` 设置为规范 HTTPS URL。
- [ ] 通过 HTTPS 提供服务时启用 Secure cookies。

---

## 3. 用户和角色管理

- [ ] 至少有两个 active `owner` 用户用于 break-glass 访问。
- [ ] 日常操作员使用 `operator`，而不是 `owner`。
- [ ] 审计员和业务观察者使用 `viewer`。
- [ ] 定期审查 disabled users。
- [ ] owner 的密码重置流程已记录。

---

## 4. Agent Registration 和 Tokens

- [ ] Registration tokens 设置较短有效期，或使用后立即 revoke。
- [ ] Raw registration token 只在必要时安全保存。
- [ ] 未使用 registration tokens 已 revoke。
- [ ] 定期审查 revoked/disabled Agents。
- [ ] Agent token files 有严格文件权限。
- [ ] Agent 主机的重新注册流程已记录。

---

## 5. Actions 和 Commands

- [ ] 破坏性 action 需要 confirmation。
- [ ] Action payloads 和 CommandResults 不暴露 raw secrets。
- [ ] 大日志/产物不以内联 CommandResult data 返回。
- [ ] `OPSTAGE_COMMAND_RESULT_MAX_BYTES` 配置合理。
- [ ] 操作员知道如何查看 prepare diagnostics 和 command failures。

---

## 6. Audit、Metrics 和 Diagnostics

- [ ] 通过 `OPSTAGE_AUDIT_RETENTION_DAYS` 配置 audit retention。
- [ ] Audit exports 受到保护并安全存储。
- [ ] Runtime diagnostics 不在未认证情况下暴露。
- [ ] 事故响应时会查看 metrics。
- [ ] CE 和 Agent 主机系统时间已同步。

---

## 7. Backups

- [ ] 定期创建 SQLite backups。
- [ ] Backups 存储在 CE 宿主机之外。
- [ ] 当包含敏感运维 metadata 时，对 backups 加密。
- [ ] 已在一次性环境中测试 restore。
- [ ] Backup retention 符合合规要求。

---

## 8. 网络暴露

- [ ] 除非必要，CE admin UI 不直接暴露到公网。
- [ ] Firewall/security groups 限制可信网络访问。
- [ ] Agent 到 Backend 的网络路径已记录。
- [ ] 跨网络 Agent 访问使用 TLS 和稳定 DNS，或受控 tunnel。
