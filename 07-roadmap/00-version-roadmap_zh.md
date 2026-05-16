---
status: draft
audience: founders
stability: evolving
last_reviewed: 2026-05-07
---

# 版本路线图

- 状态：实施指导
- 版本：共享版
- 优先级：中等
- 受众：创始人、架构师、产品经理、后端开发者、前端开发者、Agent SDK开发者、AI编码助手

本文档定义了 `xtrape-capsule` 产品系列的版本路线图。

当前的实施重点是 **CE v0.1**。CE v0.1 应该通过 Opstage 后端、Opstage UI、SQLite 和 Node.js 嵌入式 Agent SDK 来证明完整的轻量级 Capsule 治理循环。

EE（企业版）和 Cloud（云版）是未来的商业化轨道。它们应该影响扩展点设计，但不能扩大 CE v0.1 的实施范围。

路线图现在围绕四个渐进的关注点组织：

```text
1. 治理内核
2. 产品化的 CE 运营
3. 轻量级服务协调
4. 私有 AI 服务栈集成
```

最重要的路线图规则是：

> 首先构建最小的完整治理循环，然后自动化其维护，接着添加轻量级服务协调，最后才扩展到企业版、云版和 AI 原生运行时集成。

---

## 1. 目的

本路线图的目的是定义：

- 什么应该首先构建；
- 什么属于 CE v0.1；
- 什么属于后续的 CE 稳定化；
- 何时 AI 辅助的产品维护变得相关；
- 何时轻量级服务通信变得相关；
- 何时 Capsule Bus 变得相关；
- 何时 xtrape-hammers 集成变得相关；
- 何时 vieup-forge 集成变得相关；
- 何时 Agent 模式应该扩展；
- 何时 EE 私有部署变得相关；
- 何时 Cloud SaaS 变得相关；
- 如何避免将未来路线图项目混入当前实施中。

关键规则是：

> CE v0.1 证明治理循环。后续版本可能会改进自动化、通信、AI 运行时集成和商业化包装，但不能稀释 CE v0.1 内核。

---

## 2. 路线图原则

路线图遵循以下顺序：

```text
1. CE v0.1 — 证明治理循环
2. CE v0.2 — 稳定 CE 内核和产品化发布流程
3. CE v0.3 — 改进 DX、打包、诊断和 AI 维护准备度
4. CE v0.4 — 引入轻量级服务通信元数据
5. CE v0.5 — 引入早期内部协调和 Capsule Bus 规划
6. CE v1.0 — 发布可靠的社区版
7. 私有 AI 栈轨道 — 将 xtrape-hammers 和 vieup-forge 作为托管服务集成
8. EE — 添加企业私有部署能力
9. Cloud — 添加托管 SaaS 能力
```

在 CE 证明产品内核之前，不要构建 EE 或 Cloud 基础设施。

在静态内部通信、服务清单和服务身份稳定之前，不要实现 Capsule Bus。

不要将 xtrape-capsule 变成 AI 运行时。AI 运行时属于 `xtrape-hammers`；任务流自动化属于 `vieup-forge`。

---

## 3. 产品内核

产品内核是 Capsule 治理循环：

```text
Agent 注册
    ↓
服务报告
    ↓
心跳和健康检查
    ↓
配置可见性
    ↓
预定义操作请求
    ↓
命令轮询
    ↓
命令结果
    ↓
审计日志
```

每个路线图阶段都应该保留这个内核。

未来版本可能会添加规模、安全性、身份、可观察性、服务通信、AI 运行时集成和商业化，但不应该重新定义内核。

---

## 4. 路线图层级

路线图应该被理解为分层扩展，而不是功能累积。

```text
第 1 层：治理内核
  Agent 注册、服务报告、心跳、命令生命周期、审计日志。

第 2 层：产品运营自动化
  发布流程、AI 维护文档、问题分类准备度、CI/CD、变更日志、文档同步。

第 3 层：轻量级服务通信
  服务清单、端点元数据、内部 URL、服务能力、服务身份。

第 4 层：Capsule Bus
  用于命令、事件和请求/回复的未来总线式内部通信。

第 5 层：私有 AI 栈集成
  xtrape-hammers 作为 AI 运行时服务，vieup-forge 作为 TaskFlow 自动化/控制平面。

第 6 层：企业和云扩展
  RBAC、SSO、HA、Kubernetes、托管服务、计费、使用量计量。
```

Capsule 负责服务治理和运营。

Hammers 负责 AI 会话、上下文、提供者、提示和 AI 运行时调用。

Forge 负责 TaskFlow、Gate、任务螺旋、自动化规划和执行可见性。

---

## 5. CE v0.1 目标

CE v0.1 目标：

> 交付一个轻量级、开源、自托管、单节点的 Opstage 原型，证明完整的 Capsule 治理循环。

CE v0.1 应该足够好用于：

- 本地开发；
- 演示用途；
- 早期开源反馈；
- 验证 Capsule/Agent 模型；
- 证明 UI + 后端 + Agent 垂直切片；
- 指导未来架构决策。

CE v0.1 不需要达到企业级标准。

---

## 6. CE v0.1 范围

CE v0.1 应该包括：

```text
Opstage 后端
Opstage UI
SQLite 持久化
本地管理员登录
注册令牌
Agent 令牌认证
Node.js 嵌入式 Agent SDK
Node.js 演示 Capsule 服务
Agent 心跳
服务清单报告
健康报告
配置元数据可见性
预定义操作元数据
来自 UI 的操作请求
命令创建
命令轮询
CommandResult 报告
基本 AuditEvents
仪表板摘要
系统健康端点
Docker 快速启动
最小发布说明
最小故障排除指南
```

这是当前的实施目标。

---

## 7. CE v0.1 非目标

CE v0.1 不应包括：

```text
租户系统
组织系统
计费
订阅
使用量计量
企业 RBAC
SSO / OIDC / LDAP / SAML
PostgreSQL/MySQL 要求
Redis 要求
队列要求
Kubernetes 要求
Agent 网关
Sidecar Agent
外部 Agent
Java Agent SDK
Python Agent SDK
Go Agent SDK
完整可观察性平台
告警规则引擎
密钥保险库
许可证强制执行
远程 shell
任意脚本执行
Capsule Bus
内部服务网关
服务网格
AI 运行时调用层
xtrape-hammers 集成
vieup-forge 集成
AI 辅助问题分类自动化
AI 辅助发布自动化
```

这些都是未来的路线图项目。

---

## 8. CE v0.1 推荐实施顺序

推荐的实施顺序：

```text
1. 后端项目脚手架
2. UI 项目脚手架
3. SQLite 模式和持久化
4. 本地管理员认证
5. 注册令牌模型
6. Agent 注册 API
7. Agent 令牌认证
8. Node.js Agent SDK 脚手架
9. Agent 心跳
10. 服务清单报告
11. Agent 和服务 UI 页面
12. 健康和配置元数据可见性
13. ActionDefinition 模型
14. 来自 UI 的命令创建
15. 来自 SDK 的命令轮询
16. CommandResult 报告
17. AuditEvent 模型和 UI
18. 仪表板摘要
19. 系统健康端点
20. Node.js 演示 Capsule 服务
21. Docker 快速启动
22. 最小文档和发布说明
```

实施过程中可以调整顺序，但垂直治理循环应该保持优先级。

---

## 9. CE v0.1 验收标准

当满足以下条件时，CE v0.1 是可接受的：

- 用户可以在本地启动 Opstage；
- 用户可以作为本地管理员登录；
- 用户可以创建注册令牌；
- Node.js 演示 Capsule 服务可以注册；
- Agent 出现在 UI 中；
- Capsule 服务出现在 UI 中；
- 心跳状态可见；
- 健康状态可见；
- 配置元数据可见；
- 预定义操作可见；
- 用户可以运行 `echo` 操作；
- 用户可以运行 `runHealthCheck` 操作；
- 后端创建 Commands；
- Agent 轮询 Commands；
- Agent 报告 CommandResults；
- UI 显示 CommandResult；
- AuditEvents 被创建并可见；
- 陈旧/离线状态可见；
- 敏感值被屏蔽；
- 原始令牌不会被记录；
- 不存在任意 shell 执行；
- Docker 快速启动可以演示循环。

---

## 10. CE v0.2 方向 — 内核稳定化和发布规范

CE v0.2 应该在 v0.1 反馈后稳定 CE 内核。

可能的关注领域：

- 改进 UI 可用性；
- 改进错误处理；
- 改进 SDK 开发者体验；
- 改进仪表板清晰度；
- 改进状态和新鲜度计算；
- 改进审计过滤；
- 改进 Docker 打包；
- 添加更好的本地开发脚本；
- 添加更多测试；
- 添加迁移规范；
- 改进文档；
- 添加发布检查清单；
- 添加变更日志规范；
- 添加基本贡献指南；
- 添加问题和 PR 模板。

CE v0.2 仍应避免 EE/Cloud 复杂性。

CE v0.2 不应添加 Capsule Bus 或 AI 运行时能力。

---

## 11. CE v0.3 方向 — AI 维护准备度

CE v0.3 应该使 xtrape-capsule 更容易通过 AI 辅助工作流进行维护。

可能的关注领域：

- `AI_MAINTENANCE.md`；
- `RELEASE_AUTOMATION.md`；
- `PRODUCT_BOUNDARY.md`；
- 仓库审查检查清单；
- 版本同步检查清单；
- 文档同步检查清单；
- 标准 AI 任务提示模板；
- 标准发布提示模板；
- 标准问题分类提示模板；
- 更好的演示服务示例；
- 改进的 SDK 日志和诊断；
- 改进的本地设置页面；
- 更好的命令生命周期处理；
- 简单的命令过期清理；
- 如果需要，简单的健康历史；
- 更好的发布打包。

CE v0.3 应该为项目被 `vieup-forge-runtime` 管理做好准备，但不应依赖 vieup-forge。

CE v0.3 的目的是在产品增长之前减少长期维护者负担。

---

## 12. CE v0.4 方向 — Capsule Bus 实验性版本

> **方向调整(2026-05-16)。** v0.4 与 v0.5 的主题已对换。原 v0.5 的
> Capsule Bus 规划提前到 v0.4,原 v0.4 的服务通信元数据移到 v0.5
> Capsule Catalog。本中文版以下段落尚未对齐英文版,以英文版
> `00-version-roadmap.md` §12 / §13 为准。

如果治理内核稳定,CE v0.4 引入实验性的、默认禁用的 Capsule Bus,在单个
Opstage CE 实例内进行受治理的事件到命令路由。

CE v0.4 不是工作流引擎、服务网格、分布式事务层或通用消息代理替代品。

可能的关注领域：

- 服务清单 v1；
- 内部端点元数据；
- 公共/管理/内部端点可见性；
- 服务能力元数据；
- 静态内部 URL 文档；
- Docker Compose 内部服务命名约定；
- 环境变量注入约定；
- 基本服务依赖元数据；
- 如果足够简单，在 Opstage 中的基本服务拓扑视图。

服务清单方向示例：

```yaml
service:
  id: xtrape-hammers
  type: ai-runtime
  version: 0.1.0

network:
  internalBaseUrl: http://xtrape-hammers:8080

endpoints:
  - name: chat
    method: POST
    path: /v1/chat/completions
    visibility: internal
  - name: health
    method: GET
    path: /health
    visibility: internal

capabilities:
  - llm.chat
  - llm.embedding
  - task.plan
```

CE v0.4 仍应避免：

```text
服务网格
全站 mTLS
复杂路由
负载均衡
消息代理要求
队列要求
Capsule Bus 运行时
```

---

## 13. CE v0.5 方向 — Capsule Catalog(元数据 + 发现)

> **方向调整(2026-05-16)。** v0.5 主题改为 Capsule Catalog,吸收原
> v0.4 的服务清单/端点/能力元数据工作,同时增加按 capability 路由
> 的发现机制(给 v0.4 bus 提供输入)。以英文版 §13 为准。

如果 v0.4 实验性 bus 证明了路由模型可用,CE v0.5 引入 Capsule Catalog ——
按 capability 而不是 `serviceCode` 寻址目标服务。

Capsule Bus 是计划中的内部通信层，用于 capsule 管理的轻量级服务。

它旨在通过为命令、事件和请求/回复交互提供轻量级总线式通信模型，减少私有和边缘部署中的直接服务到服务耦合。

推荐的 CE v0.5 范围：

- 定义 Capsule Bus 概念文档；
- 定义命令/事件/请求-回复词汇表；
- 定义服务身份要求；
- 定义总线消息信封；
- 定义审计要求；
- 定义安全边界；
- 可选地实现实验性的进程内或本地原型；
- 默认禁用原型。

Capsule Bus 应该支持这些未来的通信模式：

```text
命令
  service-a 请求 service-b 执行操作。

事件
  service-a 发布状态更改供感兴趣的服务使用。

请求/回复
  service-a 向 service-b 请求响应，而无需硬编码直接端点详细信息。
```

CE v0.5 默认不应要求 Redis、RabbitMQ、NATS、Kafka 或任何外部队列。

任何总线实现必须保持可选，直到产品有强有力的证据证明它是必需的。

---

## 14. CE v1.0 方向

CE v1.0 应该是一个可靠的社区发布版本。

预期质量：

- 稳定的核心概念；
- 稳定的 Agent API；
- 稳定的 Node.js SDK API；
- 稳定的 SQLite 部署路径；
- 记录的升级路径；
- 有意义的测试覆盖率；
- 可靠的 Docker 快速启动；
- 清晰的安全说明；
- 清晰的 CE/EE/Cloud 边界；
- 有用的开源体验；
- 如果在 v1.0 之前引入，则记录的服务清单模型；
- 如果在 v1.0 之前引入，则记录的未来 Capsule Bus 方向。

CE v1.0 仍应该是自托管和轻量级的。

除非之前的版本证明它是必需的，否则 Capsule Bus 不是 CE v1.0 所必需的。

---

## 15. 私有 AI 栈轨道

私有 AI 栈轨道是未来的产品集成轨道，不是 CE v0.1 的要求。

它连接三个项目：

```text
xtrape-capsule
  服务运营平面。

xtrape-hammers
  AI 运行时平面。

vieup-forge
  TaskFlow 和自动化控制平面。
```

推荐的关系：

```text
vieup-forge
  ↓ TaskFlow / Gate / 节点执行规划
xtrape-hammers
  ↓ AI 会话 / 上下文 / 提供者 / 提示运行时
xtrape-capsule
  ↓ 服务部署 / 健康 / 配置 / 命令 / 审计治理
capsule 管理的服务
```

此轨道应该仅在 CE 能够可靠地管理真实服务后才开始。

---

## 16. xtrape-hammers 集成方向

`xtrape-hammers` 应该作为托管的 Capsule 服务集成，而不是作为 Capsule 核心的一部分。

潜在的集成范围：

- hammers 服务清单；
- hammers 健康和配置元数据；
- hammers 预定义操作；
- hammers 提供者状态可见性；
- 通过 Capsule 治理的 hammers 日志和诊断；
- hammers 作为示例 `ai-runtime` capsule 服务；
- Docker Compose 中可选的 hammers 演示栈。

Capsule 不应直接实现 AI 会话管理、模型提供者路由、提示管理、内存或工具调用运行时。

这些属于 hammers。

---

## 17. vieup-forge 集成方向

`vieup-forge` 应该作为 Capsule 的自动化/控制平面消费者集成，而不是作为 Capsule 核心的一部分。

潜在的集成范围：

- 通过 TaskFlow 管理 capsule 发布任务；
- 生成 Capsule 维护计划；
- 将问题分类到 TaskFlow 节点；
- 生成发布检查清单；
- 生成文档更新任务；
- 通过批准的 Gates 执行预定义的 Capsule 操作；
- 记录 Capsule 维护决策。

Capsule 应该暴露足够的元数据，让 forge 能够推理服务、agents、commands 和 audit events。

Capsule 不应直接实现 TaskFlow、Gate、task spiral 或 AI 规划。

这些属于 forge。

---

## 18. Agent 扩展路线图

Agent 扩展应该在 CE 嵌入式 Agent 模型得到验证后进行。

推荐的顺序：

```text
1. Node.js 嵌入式 Agent
2. Sidecar Agent 原型
3. 外部 Agent 原型
4. Java 嵌入式 Agent SDK
5. Python 嵌入式 Agent SDK
6. Go SDK 或基于 Go 的 Agent 运行时
7. Kubernetes Agent
```

此顺序不是固定的，但第一步是固定的：

```text
Node.js 嵌入式 Agent 优先
```

在 Node.js SDK 证明治理合约之前，不应进行 Agent 扩展。

---

## 19. 运行时扩展路线图

运行时扩展应该在 Node.js 稳定后进行。

推荐的顺序：

```text
1. Node.js 运行时
2. Java 运行时规划和原型
3. Python 运行时规划和原型
4. Go 运行时规划和原型
5. Sidecar/External 运行时适配器
6. Kubernetes 运行时集成
```

运行时扩展应该保留相同的治理合约。

运行时扩展不应过早地重新定义服务通信或 Capsule Bus。

---

## 20. EE 路线图方向

EE 应该在 CE 拥有稳定内核和真实使用信号后开始。

潜在的 EE 关注领域：

- PostgreSQL/MySQL 官方支持；
- 企业 RBAC；
- SSO / OIDC / LDAP / SAML；
- 审计导出；
- 审计保留配置；
- 告警规则；
- 可观察性集成；
- 密钥提供者集成；
- Sidecar Agent；
- 外部 Agent；
- Java/Python/Go Agent SDKs；
- 备份和恢复工具；
- 高可用性；
- Kubernetes / Helm 部署；
- 支持包；
- 私有部署包；
- 商业支持；
- 企业服务身份；
- 企业服务通信策略；
- 如果需求得到证明，则托管 Capsule Bus。

EE 应该销售企业价值，而不是削弱 CE。

---

## 21. Cloud 路线图方向

Cloud 应该在 CE/EE 概念得到充分验证后开始。

潜在的 Cloud 关注领域：

- 托管后端和 UI；
- 租户 / 组织 / 工作区模型；
- 团队邀请；
- 订阅计费；
- 使用量计量；
- Cloud Agent 网关；
- 工作区范围的注册令牌；
- 托管审计保留；
- 托管告警；
- Cloud 支持工作流；
- 数据导出和删除工作流；
- Cloud 运营监控；
- SaaS 入门 UX；
- 可选的私有 agents 托管 Opstage；
- 如果 Capsule Bus 成熟，则可选的托管协调层。

Cloud 应该与相同的 Agent 治理模型保持兼容。

Cloud 不应要求客户暴露私有服务内部细节，除非明确配置。

---

## 22. 版本命名

推荐的版本命名：

```text
CE v0.1
CE v0.2
CE v0.3
CE v0.4
CE v0.5
CE v1.0
私有 AI 栈 Alpha
私有 AI 栈 Beta
EE Alpha
EE Beta
EE v1.0
Cloud Alpha
Cloud Beta
Cloud v1.0
```

在 CE 内核稳定之前，避免使用企业版或 Cloud 版本名称。

在 xtrape-hammers 和 vieup-forge 拥有最小可用形式之前，避免使用私有 AI 栈版本名称。

---

## 23. 发布制品方向

CE 发布制品可能包括：

```text
源代码
Docker 镜像
Docker Compose 示例
Node Agent SDK 包
Node 演示 Capsule 服务
迁移文件
快速入门指南
发布说明
故障排除指南
CE v0.3 之后的 AI 维护指南
```

未来的私有 AI 栈制品可能包括：

```text
capsule + hammers Docker Compose 示例
hammers 服务清单
forge 维护 TaskFlow 模板
私有 AI 服务栈快速入门
AI 运行时服务演示
```

未来的 EE 制品可能包括：

```text
私有 Docker 镜像
私有部署包
Helm chart
备份/恢复脚本
支持包工具
安全加固指南
升级指南
许可证或授权包（如果需要）
```

未来的 Cloud 制品主要是托管服务发布和面向客户的入门流程。

---

## 24. 文档路线图

文档应该随版本演进。

### CE v0.1 文档

必需：

- 快速入门；
- 架构概述；
- Opstage UI/后端/Agent 文档；
- Node Agent SDK 指南；
- Node 演示服务指南；
- Docker 快速入门；
- 安全说明；
- 故障排除。

### CE v0.2 文档

添加：

- 发布检查清单；
- 贡献指南；
- 问题和 PR 模板指南；
- 变更日志策略；
- 本地开发指南。

### CE v0.3 文档

添加：

- AI 维护指南；
- 发布自动化指南；
- 产品边界指南；
- AI 辅助问题分类指南；
- AI 辅助文档更新指南；
- 多仓库维护指南（如果需要）。

### CE v0.4 文档

添加：

- 服务清单指南；
- 端点可见性指南；
- 内部 URL 约定；
- 能力元数据指南；
- 轻量级服务通信指南。

### CE v0.5 文档

添加：

- Capsule Bus 概念；
- 总线消息信封草案；
- 命令/事件/请求-回复模型；
- 服务身份草案；
- Capsule Bus 非目标。

### CE v1.0 文档

添加：

- 升级指南；
- API 参考；
- SDK 参考；
- 部署指南；
- 稳定贡献指南；
- 稳定发布流程。

### 私有 AI 栈文档

添加：

- hammers 作为 capsule 服务指南；
- forge 管理的 capsule 维护指南；
- 私有 AI 服务栈快速入门；
- AI 运行时服务可观察性指南。

### EE 文档

添加：

- 企业部署指南；
- RBAC 指南；
- SSO 指南；
- 审计/合规指南；
- 可观察性集成指南；
- 密钥提供者集成指南；
- 备份/恢复指南；
- 支持指南。

### Cloud 文档

添加：

- 注册/入门指南；
- 组织/工作区指南；
- Agent 注册指南；
- 计费指南；
- 数据导出/删除指南；
- Cloud 支持指南。

---

## 25. 路线图护栏

遵循这些护栏：

1. 不要在 CE v0.1 中实施 EE/Cloud 功能。
2. 在 Node.js 稳定之前，不要添加多个运行时。
3. 在嵌入式 Agent 稳定之前，不要添加 Sidecar/外部 Agent。
4. 在状态和新鲜度可靠之前，不要添加告警。
5. 在 Cloud 存在之前，不要添加计费。
6. 在 EE 有真实商业需求之前，不要添加许可证强制执行。
7. 不要添加任意 shell 执行。
8. 默认不要存储原始密钥。
9. 不要通过人为限制破坏 CE 信任。
10. 不要按版本重新定义 Capsule 治理内核。
11. 在服务清单和服务身份清晰之前，不要实现 Capsule Bus。
12. 不要将 Capsule 变成服务网格。
13. 不要将 Capsule 变成 AI 运行时。
14. 不要在 Capsule 核心中实现 TaskFlow 或 Gate。
15. 默认不要向 CE 添加外部队列要求。
16. 在 hammers 和 forge 拥有最小可用形式之前，不要扩展私有 AI 栈。
17. 不要将 OpenClaw 或任何第三方 agent 运行时作为硬依赖。

---

## 26. 决策检查点

在路线图阶段之间移动之前，请审查这些检查点。

### CE v0.2 之前

询问：

- 完整的治理循环是否工作？
- Agent API 是否可用？
- Node SDK 开发者体验是否可接受？
- 状态和新鲜度是否可理解？
- 用户是否能够成功运行演示操作？
- Docker 快速启动是否可靠？

### CE v0.3 之前

询问：

- 发布流程是否可重复？
- 问题模板和 PR 模板是否到位？
- AI 编码助手是否能理解项目边界？
- 是否有记录的维护流程？
- 维护者负担是否可接受？

### CE v0.4 之前

询问：

- 服务清单是否稳定到可以扩展？
- 用户是否需要内部服务端点元数据？
- 是否有需要内部通信的真实示例服务？
- 静态内部 URL 和环境变量是否能解决当前需求？

### CE v0.5 之前

询问：

- 点对点服务通信是否成为真正的痛点？
- 命令/事件/请求-回复语义是否清晰？
- 服务身份是否足够清晰？
- 可选的本地原型是否足够？
- Capsule Bus 能否保持可选？

### CE v1.0 之前

询问：

- 核心 API 是否足够稳定？
- 升级/迁移是否可接受？
- 文档是否足够？
- 安全边界是否清晰？
- CE 作为开源产品是否有用？
- 未来功能是否与稳定的 CE 保证清晰分离？

### 私有 AI 栈之前

询问：

- Capsule 是否能将 hammers 作为普通服务管理？
- hammers 是否有最小的 AI 运行时 API？
- forge 是否有最小的 TaskFlow 运行时？
- 集成是否有用而不成为硬依赖？
- 私有 AI 服务栈故事是否清晰？

### EE 之前

询问：

- 是否有真实的私有部署需求？
- 哪些企业功能实际上被请求？
- 首先需要哪种数据库/部署模式？
- 哪种 Agent 扩展需求最强？
- 什么样的支持负担是可接受的？
- 企业服务通信是否需要 Capsule Bus 或更简单的策略？

### Cloud 之前

询问：

- 是否有 SaaS 需求？
- 多租户是否值得增加复杂性？
- 是否需要 Agent 网关？
- 计费和支持工作流是否准备就绪？
- 运营责任是否可接受？
- 私有 agent 安全边界是否清晰？

---

## 27. 反模式

避免这些路线图反模式。

### 27.1 一次性构建所有未来版本

这会减慢 CE 并使产品不清晰。

### 27.2 CE 作为损坏的演示

CE 应该真正有用。

### 27.3 Agent 扩展在 Agent 基础之前

嵌入式 Agent 应该在 Sidecar/外部 Agent 之前稳定。

### 27.4 运行时扩展在 Node.js 稳定之前

更多的运行时不应该在验证治理合约之前出现。

### 27.5 商业包装在产品价值之前

许可证和授权系统不应该消耗早期工程容量。

### 27.6 可观察性平台在治理可见性之前

首先使 Agents、服务、健康、Commands 和 AuditEvents 可见。

### 27.7 意外的服务网格

轻量级服务通信不应该变成 Kubernetes、Istio 或完整的服务网格。

### 27.8 Capsule 核心中的 AI 运行时

Capsule 应该管理 AI 运行时服务，而不是成为其中之一。

### 27.9 Capsule 核心中的 TaskFlow

TaskFlow、Gate 和任务螺旋属于 vieup-forge，不属于 Capsule 核心。

### 27.10 Bus 在清单之前

在服务清单、端点元数据和服务身份清晰之前，不要构建 Capsule Bus。

---

## 28. 路线图摘要

推荐的路线图摘要：

```text
CE v0.1
  使用 Node.js 嵌入式 Agent 构建轻量级治理循环。

CE v0.2
  稳定 CE，改进 UI、错误处理、SDK DX、测试、打包和发布规范。

CE v0.3
  通过维护指南、发布自动化指南、边界和任务模板使项目 AI 维护就绪。

CE v0.4
  通过服务清单、端点可见性、能力、内部 URL 约定添加轻量级服务通信元数据。

CE v0.5
  定义并可选地原型化 Capsule Bus 作为未来的内部服务协调层。

CE v1.0
  发布可靠的开源社区版。

私有 AI 栈轨道
  将 xtrape-hammers 作为 AI 运行时服务集成，将 vieup-forge 作为自动化/控制平面消费者集成。

EE
  根据真实需求添加企业私有部署能力。

Cloud
  在治理模型成熟后添加托管 SaaS 能力。
```

---

## 29. 验收标准

当满足以下条件时，此路线图是可接受的：

- CE v0.1 范围清晰；
- CE v0.1 非目标清晰；
- Node.js 嵌入式 Agent 明确优先；
- 未来 Agent 和运行时扩展已排序；
- 服务通信是分阶段的而不是过度构建的；
- Capsule Bus 是面向未来的且可选的；
- xtrape-hammers 被定位为 AI 运行时，而不是 Capsule 核心；
- vieup-forge 被定位为 TaskFlow 自动化/控制平面，而不是 Capsule 核心；
- EE 和 Cloud 是明确的未来轨道；
- 路线图护栏防止范围蔓延；
- 发布和文档方向清晰；
- CE 保持有用和开源；
- 未来版本扩展相同的治理内核。

---

## 30. 摘要

`xtrape-capsule` 路线图应该优先考虑一个工作、轻量、开源的 CE 内核，然后再扩展到企业版和 SaaS 版本。

路线图现在明确分离了：

```text
Capsule 治理
产品维护自动化
轻量级服务通信
Capsule Bus
AI 运行时集成
TaskFlow 自动化
企业和云包装
```

最重要的路线图规则是：

> 首先构建最小的完整治理循环，然后自动化维护，接着引入轻量级服务协调，然后集成 AI 运行时和 TaskFlow 自动化，最后才扩展规模、运行时覆盖、Agent 模式、企业功能和 Cloud 托管。