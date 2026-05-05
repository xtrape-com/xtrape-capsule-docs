# CE 备份与恢复 Runbook

- Status: Implementation Guidance
- Edition: CE
- Priority: High
- Audience: CE operators, owners, support engineers, AI coding agents

本文说明如何备份和恢复 Opstage CE SQLite 数据库。

---

## 1. 需要备份什么

备份以下持久化数据目录：

```text
DATABASE_URL=file:./data/opstage.db
OPSTAGE_BACKUP_DIR=./data/backups
```

SQLite 数据库包含：

- users 和 password hashes；
- registration tokens 及其状态；
- Agents 和 Agent token hashes；
- Capsule Services、configs、actions、health reports；
- Commands 和 CommandResults；
- Audit Events；
- maintenance settings。

Agent 侧 token 文件不存放在 CE 数据库中。如果你控制 Agent 主机，应单独备份：

```text
OPSTAGE_AGENT_TOKEN_FILE=./data/agent-token.json
```

---

## 2. 通过 UI 创建备份

owner 操作流程：

1. 使用 `owner` 登录。
2. 打开 Settings / Diagnostics。
3. 点击 **Download SQLite Backup** 或触发 backup action。
4. 将下载文件保存到应用宿主机之外的位置。

使用 backup endpoint 时，Backend 会将服务端备份写入 `OPSTAGE_BACKUP_DIR`。

---

## 3. 文件系统备份

推荐安全流程：

```bash
# 1. 停止 CE backend/container。
# 2. 复制 SQLite database，以及存在时的 WAL/SHM 文件。
cp ./data/opstage.db ./backup/opstage.db
cp ./data/opstage.db-wal ./backup/opstage.db-wal 2>/dev/null || true
cp ./data/opstage.db-shm ./backup/opstage.db-shm 2>/dev/null || true
# 3. 重启 CE backend/container。
```

如果 backend 必须保持在线，使用 SQLite backup 工具或 CE backup endpoint，不要直接复制热数据库文件。

---

## 4. 恢复流程

1. 停止 CE backend/container。
2. 先移走当前数据库：

```bash
mv ./data/opstage.db ./data/opstage.db.before-restore.$(date +%Y%m%d%H%M%S)
rm -f ./data/opstage.db-wal ./data/opstage.db-shm
```

3. 将备份复制到原位置：

```bash
cp ./backup/opstage.db ./data/opstage.db
```

4. 确认文件 owner 和权限与运行用户匹配。
5. 启动 CE backend/container。
6. 验证：
   - `GET /api/system/health` 返回 `UP`；
   - owner 可以登录；
   - Dashboard 可加载；
   - Agents 和 Capsule Services 可见；
   - Commands 和 Audit Events 可见。

---

## 5. 恢复后的 Agent 重连

恢复较旧数据库后：

- 如果 Agent token hash 存在于恢复后的 DB，Agent 可以继续使用已有 Agent token file 重连。
- 备份时间之后注册的 Agent 在恢复后的 DB 中可能不存在，需要使用新的 registration token 重新注册。
- 备份时间之后创建的 registration token 会丢失。
- 备份时间之后创建的 command 会丢失。

如果 Agent 一直 offline：

1. 检查 Agent 日志中的 `UNAUTHORIZED` / invalid token。
2. 必要时 revoke 旧 Agent row。
3. 创建新的 registration token。
4. 只有在明确希望 Agent 重新注册时，才删除 Agent 侧 token file。
5. 重启 Agent。

---

## 6. 备份策略建议

- 小型 CE 部署至少保留每日备份。
- 将备份保存到 CE 宿主机之外。
- 当 audit data 或 service metadata 敏感时，加密备份存储。
- 定期在一次性环境中演练恢复。
- 按 audit retention policy 保留备份。
- 不要将 SQLite 备份或 Agent token files 提交到 git。
