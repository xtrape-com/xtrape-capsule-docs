# xtrape-capsule Documentation

- Status: Draft
- Edition: Shared
- Priority: High
- Audience: product designers, architects, developers, AI coding agents

`xtrape-capsule` is the lightweight service architecture domain of Xtrape. It defines the concept, specifications, runtime governance model, agent integration model, and edition strategy for Capsule Services.

This documentation set is for the whole `xtrape-capsule` domain. `xtrape-capsule-opstage` is only one core subsystem under this domain.

## Current Focus

The current implementation focus is **CE / Community Edition**.

CE should be implemented as a lightweight, open-source, self-hosted prototype that proves the core Capsule Service governance model:

- Capsule Service concept
- Agent-based registration
- Backend-managed control plane
- Web UI for human operation
- Node.js embedded agent SDK
- SQLite-first lightweight deployment
- Single-image or simple Docker deployment
- Basic health, status, command, action, config visibility, and audit capabilities

EE and Cloud are future editions. They should guide extension-point design, but they must not make the CE implementation unnecessarily heavy.

## Documentation Sections

The recommended reading order is:

```text
docs/
├── README.md
├── 01-capsule/
├── 02-specs/
├── 03-editions/
│   ├── 01-ce/
│   ├── 02-ee/
│   └── 03-cloud/
├── 04-opstage/
├── 05-agents/
├── 06-runtimes/
└── 07-roadmap/
```

### `01-capsule/`

Defines the overall domain:

- what a Capsule Service is;
- why Capsule Services are different from traditional microservices;
- the core domain model;
- the design principles of the xtrape-capsule architecture.

Read this section first before discussing implementation details.

### `02-specs/`

Defines cross-edition specifications shared by CE, EE, and Cloud:

- capsule manifest;
- management contract;
- agent registration;
- health model;
- action model;
- config model;
- command model;
- audit event model;
- status model.

Specifications in this section should remain relatively stable. CE implementation may support only a subset at first, but it should not violate these long-term contracts.

### `03-editions/`

Defines the boundaries between CE, EE, and Cloud.

- `03-editions/01-ce/`: current implementation target;
- `03-editions/02-ee/`: future private-deployment commercial edition;
- `03-editions/03-cloud/`: future SaaS cloud edition.

Only CE documents marked as `Implementation Target` should be treated as current development requirements.

### `04-opstage/`

Defines the Opstage subsystem.

Opstage is the runtime governance platform for Capsule Services. It includes:

- UI;
- backend;
- agent integration;
- command and action management;
- audit;
- observability roadmap.

### `05-agents/`

Defines the Agent system.

Agents connect Capsule Services to Opstage. The long-term model includes:

- embedded agents;
- sidecar agents;
- external agents;
- Node.js agent SDK;
- permission and token models.

CE v0.1 focuses on the Node.js embedded agent SDK.

### `06-runtimes/`

Defines runtime support plans.

CE v0.1 focuses on Node.js. Java and Python runtimes are planning targets.

### `07-roadmap/`

Defines product and engineering roadmap across CE, EE, and Cloud.

## Development Rules

### 1. CE-first implementation

Current development should prioritize CE.

Do not implement EE or Cloud features in CE v0.1 unless they are explicitly marked as CE requirements.

### 2. Keep CE lightweight

CE v0.1 should prefer:

- SQLite by default;
- simple local admin authentication;
- HTTP heartbeat;
- command polling;
- Node.js embedded agent SDK;
- single workspace;
- single-node deployment;
- basic audit log.

Avoid introducing heavy dependencies such as Kubernetes, distributed queues, full observability stacks, enterprise RBAC, SSO, or multi-tenant billing into CE v0.1.

### 3. Preserve extension points

Although CE should stay lightweight, it must keep room for EE and Cloud evolution.

CE should reserve extension points for:

- MySQL / PostgreSQL;
- multiple workspaces;
- RBAC;
- sidecar and external agents;
- WebSocket or streaming command channel;
- centralized logs and metrics;
- secret references;
- hosted Cloud backend;
- enterprise deployment.

### 4. Use Agent-based registration

Opstage must not directly assume access to arbitrary services.

Capsule Services are managed through registered and authorized Agents.

The core flow is:

```text
Capsule Service
    ↓ embedded / sidecar / external agent
Opstage Backend
    ↓
Opstage UI
```

For CE v0.1, the implemented flow is:

```text
Node.js Capsule Service
    ↓ Node.js embedded agent SDK
Opstage Backend
    ↓
Opstage UI
```

### 5. Separate specification from implementation

Specifications describe long-term contracts.

CE implementation may implement only the minimum subset required by v0.1, but it should not introduce incompatible concepts that block future EE or Cloud editions.

### 6. Documentation is part of the development contract

Before implementing a feature, check the corresponding document:

- concept: `01-capsule/`;
- protocol or schema: `02-specs/`;
- CE scope: `03-editions/01-ce/`;
- Opstage behavior: `04-opstage/`;
- Agent behavior: `05-agents/`.

If a feature is not clearly described, update the documentation before or together with the implementation.

## Suggested Reading Path for Developers

For CE v0.1 implementation, read in this order:

```text
README.md
01-capsule/00-overview.md
01-capsule/01-capsule-service-concept.md
02-specs/03-agent-registration-spec.md
02-specs/02-capsule-management-contract.md
03-editions/01-ce/README.md
03-editions/01-ce/01-ce-scope.md
03-editions/01-ce/02-ce-mvp.md
03-editions/01-ce/03-ce-architecture.md
03-editions/01-ce/04-ce-technology-stack.md
03-editions/01-ce/12-ce-extension-points.md
05-agents/04-node-agent-sdk.md
```

## Edition Status

| Edition | Status | Purpose |
|---|---|---|
| CE | Current implementation target | Open-source, lightweight, self-hosted edition |
| EE | Future planning | Private-deployment commercial edition |
| Cloud | Future planning | Hosted SaaS edition |

## Current Development Target

The first milestone is **CE v0.1 Prototype**.

CE v0.1 should deliver:

- backend service;
- web UI;
- SQLite persistence;
- Node.js embedded agent SDK;
- demo Capsule Service;
- agent registration;
- heartbeat;
- service status display;
- health report;
- basic command/action execution;
- basic audit log;
- simple Docker-based deployment.

---

# xtrape-capsule 文档集

- 状态：草案
- 版本范围：共享文档
- 优先级：高
- 面向对象：产品设计者、架构师、开发者、AI 编码代理

`xtrape-capsule` 是 Xtrape 体系中的轻服务架构领域。它用于定义 Capsule Service 的核心概念、跨版本规范、运行态治理模型、Agent 接入模型，以及 CE / EE / Cloud 三个版本的产品策略。

本文档集面向整个 `xtrape-capsule` 领域，而不是只面向 `xtrape-capsule-opstage`。`xtrape-capsule-opstage` 只是该领域下的一个核心子系统。

## 当前重点

当前实现重点是 **CE / Community Edition / 开源社区版**。

CE 应该实现为一个轻量、开源、可私有化部署的原型版本，用于验证 Capsule Service 的核心治理模型：

- Capsule Service 轻服务概念；
- 基于 Agent 的注册机制；
- Backend 管理的控制面；
- 面向人工操作的 Web UI；
- Node.js 嵌入式 Agent SDK；
- SQLite 优先的轻量部署；
- 单镜像或简单 Docker 部署；
- 基础健康状态、服务状态、命令、动作、配置可见性和审计能力。

EE 和 Cloud 是未来版本。它们应当指导 CE 的扩展点设计，但不能让 CE 的第一版实现变得过重。

## 文档分区

推荐阅读顺序如下：

```text
docs/
├── README.md
├── 01-capsule/
├── 02-specs/
├── 03-editions/
│   ├── 01-ce/
│   ├── 02-ee/
│   └── 03-cloud/
├── 04-opstage/
├── 05-agents/
├── 06-runtimes/
└── 07-roadmap/
```

### `01-capsule/`

定义整体领域，包括：

- 什么是 Capsule Service；
- Capsule Service 与传统微服务的区别；
- 核心领域模型；
- xtrape-capsule 架构的设计原则。

在讨论实现细节之前，应先阅读这一部分。

### `02-specs/`

定义 CE、EE 和 Cloud 共享的跨版本规范，包括：

- Capsule Manifest；
- Management Contract；
- Agent Registration；
- Health Model；
- Action Model；
- Config Model；
- Command Model；
- Audit Event Model；
- Status Model。

该目录下的规范应尽量保持稳定。CE 第一版可以只实现其中的一个子集，但不应引入与长期规范冲突的概念。

### `03-editions/`

定义 CE、EE 和 Cloud 三个版本的边界。

- `03-editions/01-ce/`：当前实现目标；
- `03-editions/02-ee/`：未来私有化商业版；
- `03-editions/03-cloud/`：未来 SaaS 云服务版。

只有标记为 `Implementation Target` 的 CE 文档才应被视为当前开发需求。

### `04-opstage/`

定义 Opstage 子系统。

Opstage 是 Capsule Service 的运行态治理平台，包括：

- UI；
- Backend；
- Agent 集成；
- 命令与动作管理；
- 审计；
- 可观测性路线。

### `05-agents/`

定义 Agent 系统。

Agent 用于将 Capsule Service 接入 Opstage。长期模型包括：

- 嵌入式 Agent；
- Sidecar Agent；
- External Agent；
- Node.js Agent SDK；
- 权限与令牌模型。

CE v0.1 聚焦 Node.js 嵌入式 Agent SDK。

### `06-runtimes/`

定义运行时支持计划。

CE v0.1 聚焦 Node.js。Java 和 Python Runtime 属于后续规划目标。

### `07-roadmap/`

定义 CE、EE 和 Cloud 的产品与工程路线图。

## 开发规则

### 1. CE 优先实现

当前开发应优先服务于 CE。

除非某项 EE 或 Cloud 能力被明确标记为 CE 需求，否则不要在 CE v0.1 中实现 EE 或 Cloud 功能。

### 2. 保持 CE 轻量

CE v0.1 应优先采用：

- 默认 SQLite；
- 简单本地管理员认证；
- HTTP 心跳；
- 命令轮询；
- Node.js 嵌入式 Agent SDK；
- 单 Workspace；
- 单节点部署；
- 基础审计日志。

CE v0.1 中应避免引入 Kubernetes、分布式队列、完整可观测性栈、企业级 RBAC、SSO、多租户计费等重型依赖。

### 3. 保留扩展点

虽然 CE 应保持轻量，但必须为 EE 和 Cloud 的演进保留空间。

CE 应为以下方向保留扩展点：

- MySQL / PostgreSQL；
- 多 Workspace；
- RBAC；
- Sidecar Agent 和 External Agent；
- WebSocket 或流式命令通道；
- 集中日志与指标；
- Secret Reference；
- 托管式 Cloud Backend；
- 企业级部署。

### 4. 使用基于 Agent 的注册机制

Opstage 不应默认直接访问任意服务。

Capsule Service 必须通过已注册、已授权的 Agent 被纳入治理。

核心流程是：

```text
Capsule Service
    ↓ embedded / sidecar / external agent
Opstage Backend
    ↓
Opstage UI
```

对于 CE v0.1，实际实现流程是：

```text
Node.js Capsule Service
    ↓ Node.js embedded agent SDK
Opstage Backend
    ↓
Opstage UI
```

### 5. 区分规范与实现

规范描述长期契约。

CE 第一版可以只实现 v0.1 所需的最小子集，但不能引入会阻塞未来 EE 或 Cloud 演进的不兼容概念。

### 6. 文档是开发契约的一部分

实现某项功能前，应检查对应文档：

- 概念：`01-capsule/`；
- 协议或 Schema：`02-specs/`；
- CE 范围：`03-editions/01-ce/`；
- Opstage 行为：`04-opstage/`；
- Agent 行为：`05-agents/`。

如果某项功能没有被清晰描述，应在实现前或实现过程中同步更新文档。

## 面向开发者的推荐阅读路径

实现 CE v0.1 时，建议按以下顺序阅读：

```text
README.md
01-capsule/00-overview.md
01-capsule/01-capsule-service-concept.md
02-specs/03-agent-registration-spec.md
02-specs/02-capsule-management-contract.md
03-editions/01-ce/README.md
03-editions/01-ce/01-ce-scope.md
03-editions/01-ce/02-ce-mvp.md
03-editions/01-ce/03-ce-architecture.md
03-editions/01-ce/04-ce-technology-stack.md
03-editions/01-ce/12-ce-extension-points.md
05-agents/04-node-agent-sdk.md
```

## 版本状态

| 版本 | 状态 | 目标 |
|---|---|---|
| CE | 当前实现目标 | 开源、轻量、可私有化部署的社区版 |
| EE | 未来规划 | 私有化部署的商业版 |
| Cloud | 未来规划 | 托管式 SaaS 云服务版 |

## 当前开发目标

第一个里程碑是 **CE v0.1 Prototype**。

CE v0.1 应交付：

- Backend 服务；
- Web UI；
- SQLite 持久化；
- Node.js 嵌入式 Agent SDK；
- Demo Capsule Service；
- Agent 注册；
- 心跳；
- 服务状态展示；
- 健康状态上报；
- 基础命令 / 动作执行；
- 基础审计日志；
- 简单 Docker 部署。


