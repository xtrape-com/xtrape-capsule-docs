---
status: draft
audience: founders
stability: unstable
last_reviewed: 2026-05-05
edition: ee
phase: future
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 04-ee-cluster-and-ha.md
翻译状态 / Translation Status: 已翻译 / Translated
生成时间 / Generated: 2026-05-01 09:28:54
================================================================================
注意 / Notes:
- 技术术语如 Capsule Service、Agent、Opstage 等保留英文或采用中英对照
- 代码块中的内容不翻译
- 文件路径和 URL 不翻译
- 保持原有的 Markdown 格式结构
================================================================================
-->

# EE（企业版） Cluster and 高 Availability

- Status: Planning
- Edition: EE（企业版）
- Priority: Future
- Audience: architects, platform engineers, SRE teams, backend developers, DevOps engineers, AI coding agents

This document 定义 the planned cluster and high availability model for **Opstage（运维舞台） EE（企业版） / Enterprise 版本**.

Opstage（运维舞台） EE（企业版） is the future private commercial edition of the `xtrape-capsule` product family. Cluster and high
availability capabilities are not CE（社区版） v0.1 implementation requirements.

---

## 1. Purpose

The purpose of this document is to define:

- what high availability means for Opstage（运维舞台） EE（企业版）;
- which components may need to be split from the CE（社区版） single-process model;
- how Backend, UI, workers, schedulers, database, cache, queue, and Agent（代理） connectivity may evolve;
- how Commands and Agent（代理） communication should behave in a clustered deployment;
- how failover, recovery, backup, restore, and upgrade should be approached;
- which HA concepts CE（社区版） should reserve without implementing EE（企业版） complexity.

The key rule is:

> EE（企业版） may support clustered and highly available deployment, but CE（社区版） v0.1 must remain single-node, lightweight, and easy to run.

---

## 2. HA Goal

The goal of EE（企业版） high availability is:

> Keep the Opstage（运维舞台） control plane available and recoverable for enterprise users even when individual application instances, workers, or infrastructure nodes fail.

EE（企业版） HA should improve:

- UI availability;
- Admin API availability;
- Agent（代理） API availability;
- Command dispatch reliability;
- CommandResult persistence;
- AuditEvent durability;
- health and status freshness;
- upgrade safety;
- backup and recovery.

HA should not change the core Capsule governance model.

---

## 3. EE（企业版） HA Is Not CE（社区版） v0.1

CE（社区版） v0.1 must not implement full cluster or HA capabilities.

Out of scope for CE（社区版） v0.1:

- multi-node Backend cluster;
- Kubernetes requirement;
- Helm chart;
- Redis requirement;
- message queue requirement;
- distributed scheduler;
- distributed lock;
- external database requirement;
- high availability database setup;
- zero-downtime rolling upgrade;
- multi-region deployment;
- disaster recovery automation.

CE（社区版） v0.1 should remain:

```text
single container
single process or simple process model
SQLite by default
single exposed port
local volume
```

---

## 4. Relationship with CE（社区版） 部署

CE（社区版） deployment model:

```text
Single container
├── Backend server
├── static UI assets
└── SQLite data volume
```

EE（企业版） clustered deployment may evolve to:

```text
Load Balancer
├── Opstage Backend instance 1
├── Opstage Backend instance 2
└── Opstage Backend instance N

Workers / Schedulers
├── Worker instance 1
├── Worker instance 2
└── Scheduler instance

Shared Infrastructure
├── PostgreSQL / MySQL
├── Redis / Cache
├── Queue
├── Object Storage
└── Observability integrations
```

CE（社区版） should reserve extension points, but must not require these components.

---

## 5. Availability Scope

EE（企业版） HA should focus on these availability areas:

```text
UI serving
Admin API
Agent API
Command creation
Command delivery
Command result reporting
Audit writing
Health/status calculation
Background jobs
Database availability
Queue/cache availability
Backup and restore
Upgrade continuity
```

Not all areas need the same availability level in the first EE（企业版） release.

---

## 6. Target 部署 Models

EE（企业版） may support multiple deployment models over time.

### 6.1 Single-node production deployment

A production-like single-node EE（企业版） deployment may use:

```text
Backend + UI
External PostgreSQL/MySQL
Optional Redis
Optional worker
```

This may be the first EE（企业版） step beyond CE（社区版）.

### 6.2 Docker Compose deployment

Useful for private deployment and small teams.

Possible components:

```text
opstage-backend
opstage-ui
opstage-worker
postgresql
redis
reverse-proxy
```

### 6.3 Kubernetes deployment

Future EE（企业版） may support Kubernetes with Helm.

Possible components:

```text
Deployment: backend
Deployment: worker
Deployment: scheduler
Service: backend
Ingress: UI/API
StatefulSet or external DB reference
ConfigMap / Secret
HorizontalPodAutoscaler
```

### 6.4 Air-gapped or restricted deployment

Some enterprise customers may require restricted-network deployment.

This may require:

- offline images;
- private registry;
- offline license file;
- local documentation bundle;
- manual upgrade package.

This is long-term EE（企业版） work.

---

## 7. Component Split

CE（社区版） may serve UI and APIs from one process.

EE（企业版） may split components.

### 7.1 UI

UI can be served by:

- Backend static file serving;
- dedicated web server;
- CDN or internal static hosting;
- reverse proxy.

For private EE（企业版）, serving UI behind the same enterprise ingress may be simplest.

### 7.2 Backend API

Backend API should become horizontally scalable where practical.

To support scaling, Backend should be mostly stateless.

### 7.3 Worker

Workers may handle:

- command expiration;
- stale status recalculation;
- retention cleanup;
- alert evaluation;
- notification dispatch;
- audit export jobs;
- scheduled service refresh;
- integration sync.

### 7.4 Scheduler

A scheduler may create periodic jobs.

In a cluster, only one scheduler should actively schedule the same job set.

This may require:

- leader election;
- distributed lock;
- database-based scheduler lock;
- queue-backed scheduling.

### 7.5 Agent（代理） Gateway

EE（企业版） may or may not need a separate Agent（代理） Gateway.

For many private deployments, Backend Agent（代理） APIs may be enough.

An Agent（代理） Gateway may become useful for:

- very large Agent（代理） fleets;
- WebSocket or streaming connections;
- rate limiting;
- protocol routing;
- connection diagnostics.

---

## 8. Stateless Backend Principle

EE（企业版） Backend instances should be designed to be stateless where practical.

Backend instances should not rely on:

- local SQLite file;
- local in-memory sessions only;
- local in-memory command queues;
- local in-memory Agent（代理） state as source of truth;
- local filesystem for persistent data.

共享 state should live in:

```text
Database
Cache
Queue
Object storage
```

depending on feature maturity.

CE（社区版） can remain simpler.

---

## 9. Session and 认证 in Cluster

If EE（企业版） uses multiple Backend instances, user sessions must work across instances.

Possible options:

### 9.1 JWT

Pros:

- stateless;
- easy horizontal scaling.

Cons:

- revocation and rotation require careful design;
- token storage must be secure.

### 9.2 共享 session store

Examples:

```text
Redis-backed sessions
Database-backed sessions
```

Pros:

- easier revocation;
- familiar browser session model.

Cons:

- requires shared store.

### 9.3 Recommendation

CE（社区版） may use simple sessions or JWT.

EE（企业版） should choose a cluster-compatible auth strategy before HA support is claimed.

---

## 10. Database HA

EE（企业版） should support production databases.

Primary candidates:

```text
PostgreSQL
MySQL
```

### 10.1 Database responsibilities

Database stores durable control-plane state:

- users;
- workspaces;
- Agents;
- Capsule Services;
- HealthReports;
- ConfigItems;
- ActionDefinitions;
- Commands;
- CommandResults;
- AuditEvents;
- system settings;
- job state if used.

### 10.2 HA database setup

EE（企业版） may provide guidance for:

- managed database;
- primary/replica setup;
- backup and restore;
- point-in-time recovery;
- connection pooling;
- migration strategy;
- database monitoring.

### 10.3 Database is source of truth

Commands, CommandResults, Agent（代理） status, and AuditEvents should be persisted in database or durable storage.

Do not use in-memory state as source of truth in EE（企业版）.

---

## 11. Cache and Redis

EE（企业版） may introduce Redis or another cache.

Possible uses:

- shared session store;
- rate limiting;
- short-lived locks;
- lightweight queue;
- Agent（代理） connection metadata;
- dashboard cache;
- deduplication cache.

Redis should not become required for CE（社区版） v0.1.

If Redis is required by EE（企业版）, deployment docs must describe its availability and failure behavior.

---

## 12. Queue and Background Jobs

EE（企业版） may introduce a queue for reliable background processing.

Possible queue uses:

- command dispatch workflow;
- alert evaluation;
- notification sending;
- audit export;
- retention cleanup;
- integration sync;
- scheduled health analysis.

Candidate technologies:

```text
BullMQ / Redis-based queue
RabbitMQ
Kafka
database-backed job queue
```

The first EE（企业版） implementation should avoid overengineering.

A database-backed job model may be enough before introducing Kafka-like systems.

---

## 13. Command Reliability in Cluster

Command reliability is a core HA concern.

### 13.1 Durable Command records

Commands must be durable records.

Do not rely on in-memory queues only.

### 13.2 Agent（代理） polling mode

In HTTP polling mode, any Backend instance may serve Agent（代理） command polling if it can read the shared database.

Flow:

```text
User creates Command
    ↓
Command persisted in database
    ↓
Agent polls any Backend instance
    ↓
Backend marks Command as dispatched
    ↓
Agent executes action
    ↓
Agent reports result to any Backend instance
    ↓
CommandResult persisted
```

### 13.3 Dispatch concurrency

Clustered Backend must avoid dispatching the same Command incorrectly.

Possible mechanisms:

- atomic database update;
- row lock;
- optimistic concurrency;
- command lease;
- queue consumer assignment.

### 13.4 Idempotency

Command result reporting should tolerate retries.

Rules:

- one final result per Command;
- duplicate result report should be handled safely;
- result report must validate Agent（代理） ownership;
- command status transitions should be controlled.

---

## 14. Agent（代理） Connectivity in Cluster

Agents may connect to any Backend instance behind a load balancer.

### 14.1 HTTP polling

HTTP polling is naturally compatible with stateless Backend if shared database is used.

### 14.2 WebSocket or streaming

If EE（企业版） later 支持 WebSocket or streaming, connection state becomes more complex.

Possible requirements:

- sticky sessions;
- Agent（代理） Gateway;
- shared connection registry;
- message routing;
- reconnect handling;
- command delivery fallback.

### 14.3 Recommendation

Do not require WebSocket for first EE（企业版） HA.

Preserve HTTP polling as a reliable baseline.

---

## 15. 状态 and Freshness in Cluster

状态 calculation must be consistent across instances.

### 15.1 Agent（代理） status

Agent（代理） status depends on:

```text
lastHeartbeatAt
Agent disabled/revoked state
offline threshold
```

### 15.2 Capsule Service（胶囊服务） status

Capsule Service（胶囊服务） effective status depends on:

```text
reportedStatus
healthStatus
lastReportedAt
lastHealthAt
managing Agent status
freshness threshold
```

### 15.3 Recalculation strategies

Possible strategies:

- calculate on read;
- periodic background recalculation;
- update status on heartbeat/report;
- hybrid model.

For early EE（企业版）, calculate-on-read plus update-on-events may be enough.

---

## 16. Audit Durability

AuditEvents are security and compliance records.

In EE（企业版）:

- audit writes should be durable;
- important operations should not silently skip audit;
- audit payloads must be sanitized;
- audit failure handling should be defined;
- audit export may be supported later;
- immutable audit sink may be long-term.

Possible audit failure policy:

```text
For security-critical operations, fail closed if audit cannot be written.
For low-risk operations, log and retry if audit writing fails.
```

This policy must be designed carefully before compliance claims.

---

## 17. File and Object Storage

EE（企业版） may need object storage for:

- audit exports;
- support bundles;
- backup artifacts;
- report exports;
- attachment-like artifacts;
- large command output if ever supported.

Possible storage options:

```text
local filesystem
S3-compatible storage
MinIO
enterprise object storage
```

CE（社区版） v0.1 should avoid large file storage requirements.

---

## 18. Backup and Restore

EE（企业版） should provide backup and restore guidance.

### 18.1 Backup targets

Backup may include:

- database;
- object storage;
- configuration files;
- license files;
- deployment manifests;
- encryption keys or secret references if applicable.

### 18.2 Restore requirements

Restore guidance should cover:

- full restore;
- database restore;
- point-in-time recovery if supported;
- object storage restore;
- post-restore validation;
- Agent（代理） reconnect behavior after restore.

### 18.3 CE（社区版） relationship

CE（社区版） v0.1 may provide simple SQLite backup notes.

EE（企业版） should provide stronger backup/restore docs.

---

## 19. Disaster Recovery

Disaster recovery is a long-term EE（企业版） capability.

Possible DR topics:

- recovery time objective;
- recovery point objective;
- database replication;
- backup verification;
- cold standby;
- warm standby;
- multi-zone deployment;
- restore drill process.

EE（企业版） should avoid making DR promises before validated implementation.

---

## 20. Upgrade and Migration

EE（企业版） must support safer upgrades than CE（社区版）.

### 20.1 Upgrade concerns

- database schema migration;
- backward-compatible Agent（代理） protocol;
- rolling Backend upgrade;
- worker version compatibility;
- UI/API version compatibility;
- downgrade strategy if needed;
- backup before migration.

### 20.2 Rolling upgrade

Future EE（企业版） may support rolling upgrade if:

- Backend instances are stateless;
- database migrations are backward compatible;
- Agent（代理） APIs are versioned;
- old and new workers do not conflict.

### 20.3 CE（社区版） relationship

CE（社区版） can keep upgrade simple:

```text
stop container
backup data
start new version
run migration
```

---

## 21. Scaling Model

EE（企业版） scaling may include:

### 21.1 Backend scaling

Scale Backend instances horizontally behind a load balancer.

### 21.2 Worker scaling

Scale workers based on job queue volume.

### 21.3 Agent（代理） traffic scaling

Scale Agent（代理） API or Agent（代理） Gateway based on:

- heartbeat rate;
- service report rate;
- command polling rate;
- command result volume.

### 21.4 Database scaling

Scale database through:

- tuning;
- read replicas for read-heavy views;
- connection pooling;
- partitioning or archiving later;
- retention policies.

### 21.5 UI scaling

UI can be served statically or through reverse proxy/CDN-like internal hosting.

---

## 22. Load Balancing

EE（企业版） may use a load balancer or ingress.

Load-balanced paths:

```text
Admin UI
Admin API
Agent API
System health endpoint
```

For HTTP polling, no sticky session should be required if sessions and state are shared.

For WebSocket/streaming, sticky sessions or Agent（代理） Gateway may be required.

---

## 23. Health Checks

EE（企业版） components should expose health checks.

Possible endpoints:

```text
GET /api/system/health
GET /api/system/ready
GET /api/system/live
```

Health checks may include:

- application liveness;
- database connectivity;
- cache connectivity;
- queue connectivity;
- migration status;
- worker status.

CE（社区版） v0.1 may only need `/api/system/health`.

---

## 24. Observability for HA

Clustered EE（企业版） deployment requires observability.

Needed visibility:

- Backend instance health;
- worker health;
- scheduler status;
- database health;
- queue depth;
- failed jobs;
- Agent（代理） API error rate;
- command dispatch latency;
- command result latency;
- audit write errors.

This should integrate with EE（企业版） observability design.

---

## 25. 安全 in Cluster

Clustered deployment must preserve security.

Rules:

- all instances use consistent authentication configuration;
- session/JWT secrets are managed safely;
- database credentials are protected;
- internal service communication is secured where required;
- Agent（代理） tokens are validated consistently;
- audit writes are durable;
- sensitive logs are redacted;
- support access is controlled.

Future EE（企业版） may support mTLS between components, but this is not an early requirement.

---

## 26. License and Entitlement in Cluster

If EE（企业版） 包括 license enforcement, cluster mode must handle it consistently.

Possible requirements:

- license loaded by all Backend instances;
- license state stored centrally or verified locally;
- license expiration warning visible once, not duplicated noisily;
- feature entitlements consistent across instances;
- license changes audited.

CE（社区版） does not need license enforcement.

---

## 27. EE（企业版） HA MVP Candidate

A future EE（企业版） HA MVP may include:

- PostgreSQL/MySQL support;
- stateless Backend deployment;
- Docker Compose deployment with external database;
- optional Redis for sessions or cache;
- worker process for expiration/cleanup;
- health/readiness endpoints;
- backup and restore guide;
- migration guide;
- command dispatch concurrency control;
- basic deployment observability;
- documented single-node production deployment.

Full Kubernetes HA may come later.

---

## 28. Long-Term HA Capabilities

Long-term EE（企业版） may include:

- Helm chart;
- horizontal autoscaling;
- Agent（代理） Gateway cluster;
- WebSocket/gRPC connection routing;
- multi-zone deployment;
- queue-backed command delivery;
- distributed scheduler;
- advanced retention jobs;
- disaster recovery automation;
- rolling upgrades;
- blue/green deployment guidance;
- air-gapped HA deployment.

These should be built after real enterprise deployment needs are validated.

---

## 29. CE（社区版） Reservations

CE（社区版） should reserve these HA-compatible concepts:

```text
Database provider abstraction
Command as durable record
CommandResult as durable record
AuditEvent as durable record
Agent token validation
Agent ownership validation
workspaceId
status and freshness calculation
metadataJson
system health endpoint
```

CE（社区版） should not implement:

```text
cluster mode
HA database requirement
Redis requirement
queue requirement
distributed scheduler
leader election
Kubernetes deployment
rolling upgrades
Agent Gateway cluster
multi-node command routing
```

---

## 30. Anti-Patterns

Avoid these patterns.

### 30.1 Claiming HA with SQLite local file

SQLite is excellent for CE（社区版）, but not an EE（企业版） HA database model.

### 30.2 In-memory Command queue as source of truth

Commands must be durable.

### 30.3 Local-only sessions in multi-instance Backend

User sessions must work across instances.

### 30.4 Duplicate command dispatch

Cluster must prevent unsafe duplicate execution.

### 30.5 WebSocket-only Agent（代理） delivery too early

HTTP polling should remain reliable and compatible.

### 30.6 HA complexity in CE（社区版） v0.1

CE（社区版） must stay simple.

---

## 31. Acceptance Criteria

EE（企业版） cluster and HA planning is acceptable when:

- HA is clearly separated from CE（社区版） v0.1;
- Backend statelessness direction is clear;
- database source-of-truth principle is clear;
- command durability and concurrency are addressed;
- Agent（代理） polling remains compatible with clustered Backend;
- session/auth strategy for cluster is identified;
- workers and scheduler responsibilities are clear;
- backup, restore, upgrade, and observability are included;
- CE（社区版） reservations are clear;
- anti-patterns are explicit.

---

## 32. Summary

Opstage（运维舞台） EE（企业版） cluster and high availability should evolve from the CE（社区版） control-plane kernel without making the first CE（社区版） implementation heavy.

The most important HA rule is:

> Make durable state explicit, keep Backend instances stateless where practical, and preserve simple Agent（代理） polling as the reliable baseline before introducing complex cluster infrastructure.
