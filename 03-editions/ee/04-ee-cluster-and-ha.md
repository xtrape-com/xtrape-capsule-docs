# EE Cluster and High Availability

- Status: Planning
- Edition: EE
- Priority: Future

## Position

EE 是未来私有化商业版规划，不是 CE v0.1 的实现要求。

## Planned Direction

- 企业级 RBAC、SSO、OIDC/LDAP。
- 高可用、集群部署、更强数据库支持。
- 集中日志、日志检索、指标监控、监控大屏。
- Secret Vault、合规审计、商业 License。
- Sidecar / External Agent、多语言 Agent SDK。
- 企业安装包、升级迁移、技术支持。

## CE Reservation

CE 应保留 workspace、agent mode、database provider、command delivery、secretRef、audit event 等扩展点。

# EE Cluster and High Availability

- Status: Planning
- Edition: EE
- Priority: Future
- Audience: architects, platform engineers, SRE teams, backend developers, DevOps engineers, AI coding agents

This document defines the planned cluster and high availability model for **Opstage EE / Enterprise Edition**.

Opstage EE is the future private commercial edition of the `xtrape-capsule` product family. Cluster and high availability capabilities are not CE v0.1 implementation requirements.

---

## 1. Purpose

The purpose of this document is to define:

- what high availability means for Opstage EE;
- which components may need to be split from the CE single-process model;
- how Backend, UI, workers, schedulers, database, cache, queue, and Agent connectivity may evolve;
- how Commands and Agent communication should behave in a clustered deployment;
- how failover, recovery, backup, restore, and upgrade should be approached;
- which HA concepts CE should reserve without implementing EE complexity.

The key rule is:

> EE may support clustered and highly available deployment, but CE v0.1 must remain single-node, lightweight, and easy to run.

---

## 2. HA Goal

The goal of EE high availability is:

> Keep the Opstage control plane available and recoverable for enterprise users even when individual application instances, workers, or infrastructure nodes fail.

EE HA should improve:

- UI availability;
- Admin API availability;
- Agent API availability;
- Command dispatch reliability;
- CommandResult persistence;
- AuditEvent durability;
- health and status freshness;
- upgrade safety;
- backup and recovery.

HA should not change the core Capsule governance model.

---

## 3. EE HA Is Not CE v0.1

CE v0.1 must not implement full cluster or HA capabilities.

Out of scope for CE v0.1:

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

CE v0.1 should remain:

```text
single container
single process or simple process model
SQLite by default
single exposed port
local volume
```

---

## 4. Relationship with CE Deployment

CE deployment model:

```text
Single container
├── Backend server
├── static UI assets
└── SQLite data volume
```

EE clustered deployment may evolve to:

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

CE should reserve extension points, but must not require these components.

---

## 5. Availability Scope

EE HA should focus on these availability areas:

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

Not all areas need the same availability level in the first EE release.

---

## 6. Target Deployment Models

EE may support multiple deployment models over time.

### 6.1 Single-node production deployment

A production-like single-node EE deployment may use:

```text
Backend + UI
External PostgreSQL/MySQL
Optional Redis
Optional worker
```

This may be the first EE step beyond CE.

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

Future EE may support Kubernetes with Helm.

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

This is long-term EE work.

---

## 7. Component Split

CE may serve UI and APIs from one process.

EE may split components.

### 7.1 UI

UI can be served by:

- Backend static file serving;
- dedicated web server;
- CDN or internal static hosting;
- reverse proxy.

For private EE, serving UI behind the same enterprise ingress may be simplest.

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

### 7.5 Agent Gateway

EE may or may not need a separate Agent Gateway.

For many private deployments, Backend Agent APIs may be enough.

An Agent Gateway may become useful for:

- very large Agent fleets;
- WebSocket or streaming connections;
- rate limiting;
- protocol routing;
- connection diagnostics.

---

## 8. Stateless Backend Principle

EE Backend instances should be designed to be stateless where practical.

Backend instances should not rely on:

- local SQLite file;
- local in-memory sessions only;
- local in-memory command queues;
- local in-memory Agent state as source of truth;
- local filesystem for persistent data.

Shared state should live in:

```text
Database
Cache
Queue
Object storage
```

depending on feature maturity.

CE can remain simpler.

---

## 9. Session and Authentication in Cluster

If EE uses multiple Backend instances, user sessions must work across instances.

Possible options:

### 9.1 JWT

Pros:

- stateless;
- easy horizontal scaling.

Cons:

- revocation and rotation require careful design;
- token storage must be secure.

### 9.2 Shared session store

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

CE may use simple sessions or JWT.

EE should choose a cluster-compatible auth strategy before HA support is claimed.

---

## 10. Database HA

EE should support production databases.

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

EE may provide guidance for:

- managed database;
- primary/replica setup;
- backup and restore;
- point-in-time recovery;
- connection pooling;
- migration strategy;
- database monitoring.

### 10.3 Database is source of truth

Commands, CommandResults, Agent status, and AuditEvents should be persisted in database or durable storage.

Do not use in-memory state as source of truth in EE.

---

## 11. Cache and Redis

EE may introduce Redis or another cache.

Possible uses:

- shared session store;
- rate limiting;
- short-lived locks;
- lightweight queue;
- Agent connection metadata;
- dashboard cache;
- deduplication cache.

Redis should not become required for CE v0.1.

If Redis is required by EE, deployment docs must describe its availability and failure behavior.

---

## 12. Queue and Background Jobs

EE may introduce a queue for reliable background processing.

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

The first EE implementation should avoid overengineering.

A database-backed job model may be enough before introducing Kafka-like systems.

---

## 13. Command Reliability in Cluster

Command reliability is a core HA concern.

### 13.1 Durable Command records

Commands must be durable records.

Do not rely on in-memory queues only.

### 13.2 Agent polling mode

In HTTP polling mode, any Backend instance may serve Agent command polling if it can read the shared database.

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
- result report must validate Agent ownership;
- command status transitions should be controlled.

---

## 14. Agent Connectivity in Cluster

Agents may connect to any Backend instance behind a load balancer.

### 14.1 HTTP polling

HTTP polling is naturally compatible with stateless Backend if shared database is used.

### 14.2 WebSocket or streaming

If EE later supports WebSocket or streaming, connection state becomes more complex.

Possible requirements:

- sticky sessions;
- Agent Gateway;
- shared connection registry;
- message routing;
- reconnect handling;
- command delivery fallback.

### 14.3 Recommendation

Do not require WebSocket for first EE HA.

Preserve HTTP polling as a reliable baseline.

---

## 15. Status and Freshness in Cluster

Status calculation must be consistent across instances.

### 15.1 Agent status

Agent status depends on:

```text
lastHeartbeatAt
Agent disabled/revoked state
offline threshold
```

### 15.2 Capsule Service status

Capsule Service effective status depends on:

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

For early EE, calculate-on-read plus update-on-events may be enough.

---

## 16. Audit Durability

AuditEvents are security and compliance records.

In EE:

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

EE may need object storage for:

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

CE v0.1 should avoid large file storage requirements.

---

## 18. Backup and Restore

EE should provide backup and restore guidance.

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
- Agent reconnect behavior after restore.

### 18.3 CE relationship

CE v0.1 may provide simple SQLite backup notes.

EE should provide stronger backup/restore docs.

---

## 19. Disaster Recovery

Disaster recovery is a long-term EE capability.

Possible DR topics:

- recovery time objective;
- recovery point objective;
- database replication;
- backup verification;
- cold standby;
- warm standby;
- multi-zone deployment;
- restore drill process.

EE should avoid making DR promises before validated implementation.

---

## 20. Upgrade and Migration

EE must support safer upgrades than CE.

### 20.1 Upgrade concerns

- database schema migration;
- backward-compatible Agent protocol;
- rolling Backend upgrade;
- worker version compatibility;
- UI/API version compatibility;
- downgrade strategy if needed;
- backup before migration.

### 20.2 Rolling upgrade

Future EE may support rolling upgrade if:

- Backend instances are stateless;
- database migrations are backward compatible;
- Agent APIs are versioned;
- old and new workers do not conflict.

### 20.3 CE relationship

CE can keep upgrade simple:

```text
stop container
backup data
start new version
run migration
```

---

## 21. Scaling Model

EE scaling may include:

### 21.1 Backend scaling

Scale Backend instances horizontally behind a load balancer.

### 21.2 Worker scaling

Scale workers based on job queue volume.

### 21.3 Agent traffic scaling

Scale Agent API or Agent Gateway based on:

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

EE may use a load balancer or ingress.

Load-balanced paths:

```text
Admin UI
Admin API
Agent API
System health endpoint
```

For HTTP polling, no sticky session should be required if sessions and state are shared.

For WebSocket/streaming, sticky sessions or Agent Gateway may be required.

---

## 23. Health Checks

EE components should expose health checks.

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

CE v0.1 may only need `/api/system/health`.

---

## 24. Observability for HA

Clustered EE deployment requires observability.

Needed visibility:

- Backend instance health;
- worker health;
- scheduler status;
- database health;
- queue depth;
- failed jobs;
- Agent API error rate;
- command dispatch latency;
- command result latency;
- audit write errors.

This should integrate with EE observability design.

---

## 25. Security in Cluster

Clustered deployment must preserve security.

Rules:

- all instances use consistent authentication configuration;
- session/JWT secrets are managed safely;
- database credentials are protected;
- internal service communication is secured where required;
- Agent tokens are validated consistently;
- audit writes are durable;
- sensitive logs are redacted;
- support access is controlled.

Future EE may support mTLS between components, but this is not an early requirement.

---

## 26. License and Entitlement in Cluster

If EE includes license enforcement, cluster mode must handle it consistently.

Possible requirements:

- license loaded by all Backend instances;
- license state stored centrally or verified locally;
- license expiration warning visible once, not duplicated noisily;
- feature entitlements consistent across instances;
- license changes audited.

CE does not need license enforcement.

---

## 27. EE HA MVP Candidate

A future EE HA MVP may include:

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

Long-term EE may include:

- Helm chart;
- horizontal autoscaling;
- Agent Gateway cluster;
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

## 29. CE Reservations

CE should reserve these HA-compatible concepts:

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

CE should not implement:

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

SQLite is excellent for CE, but not an EE HA database model.

### 30.2 In-memory Command queue as source of truth

Commands must be durable.

### 30.3 Local-only sessions in multi-instance Backend

User sessions must work across instances.

### 30.4 Duplicate command dispatch

Cluster must prevent unsafe duplicate execution.

### 30.5 WebSocket-only Agent delivery too early

HTTP polling should remain reliable and compatible.

### 30.6 HA complexity in CE v0.1

CE must stay simple.

---

## 31. Acceptance Criteria

EE cluster and HA planning is acceptable when:

- HA is clearly separated from CE v0.1;
- Backend statelessness direction is clear;
- database source-of-truth principle is clear;
- command durability and concurrency are addressed;
- Agent polling remains compatible with clustered Backend;
- session/auth strategy for cluster is identified;
- workers and scheduler responsibilities are clear;
- backup, restore, upgrade, and observability are included;
- CE reservations are clear;
- anti-patterns are explicit.

---

## 32. Summary

Opstage EE cluster and high availability should evolve from the CE control-plane kernel without making the first CE implementation heavy.

The most important HA rule is:

> Make durable state explicit, keep Backend instances stateless where practical, and preserve simple Agent polling as the reliable baseline before introducing complex cluster infrastructure.