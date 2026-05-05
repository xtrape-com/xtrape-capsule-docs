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
原始文件 / Original File: 05-ee-agent-expansion.md
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

# EE（企业版） Agent（代理） Expansion

- Status: Planning
- Edition: EE（企业版）
- Priority: Future
- Audience: architects, agent SDK developers, backend developers, platform engineers, DevOps engineers, AI coding agents

This document 定义 the planned Agent（代理） expansion model for **Opstage（运维舞台） EE（企业版） / Enterprise 版本**.

Opstage（运维舞台） EE（企业版） is the future private commercial edition of the `xtrape-capsule` product family. Agent（代理）
expansion capabilities are not CE（社区版） v0.1 implementation requirements.

---

## 1. Purpose

The purpose of this document is to define:

- how EE（企业版） may expand beyond the CE（社区版） Node.js embedded Agent（代理）;
- what Agent（代理） modes should exist in the long-term model;
- how sidecar and external Agents may work;
- how Java, Python, and Go Agent（代理） SDKs may be introduced;
- how Agent（代理） protocol compatibility should be preserved;
- how Agent（代理） diagnostics, upgrades, and version management may work;
- which Agent（代理） concepts CE（社区版） should reserve without implementing EE（企业版） complexity.

The key rule is:

> EE（企业版） may expand Agent（代理） modes and runtimes, but all Agents must preserve the same core governance contract.

---

## 2. Agent（代理） Expansion Goal

The goal of EE（企业版） Agent（代理） expansion is:

> Allow different types of Capsule Services and enterprise runtimes to become governable by Opstage（运维舞台） without forcing all services to embed the same Node.js SDK.

EE（企业版） Agent（代理） expansion should support:

- non-Node.js services;
- legacy services;
- services that cannot embed an SDK;
- sidecar deployment patterns;
- external management patterns;
- enterprise runtime diversity;
- larger Agent（代理） fleets;
- stronger diagnostics and version management.

---

## 3. EE（企业版） Agent（代理） Expansion Is Not CE（社区版） v0.1

CE（社区版） v0.1 must not implement full Agent（代理） expansion.

Out of scope for CE（社区版） v0.1:

- sidecar Agent（代理）;
- external Agent（代理）;
- host Agent（代理）;
- Kubernetes Agent（代理）;
- Java Agent（代理） SDK;
- Python Agent（代理） SDK;
- Go Agent（代理） SDK;
- Agent（代理） Gateway;
- WebSocket or gRPC Agent（代理） protocol;
- Agent（代理） upgrade manager;
- Agent（代理） fleet diagnostics;
- Agent（代理） marketplace;
- automatic service discovery.

CE（社区版） v0.1 should implement only:

```text
Node.js embedded Agent SDK
HTTP heartbeat
service report
command polling
CommandResult reporting
predefined action execution
```

---

## 4. Relationship with CE（社区版） Agent（代理）

CE（社区版） Agent（代理） model:

```text
Node.js Capsule Service
    ↓ in-process SDK
Node.js Embedded Agent
    ↓ HTTP Agent API
Opstage Backend
```

EE（企业版） should extend this model to support additional modes:

```text
Embedded Agent
Sidecar Agent
External Agent
Host Agent
Kubernetes Agent
```

But all modes should preserve the same shared concepts:

```text
Agent
CapsuleService
Manifest
HealthReport
ConfigItem
ActionDefinition
Command
CommandResult
AuditEvent
Status values
secretRef
```

---

## 5. Agent（代理） Mode 概述

Recommended long-term Agent（代理） modes:

||Mode|Description|CE（社区版） v0.1||
|---|---|---|
||embedded|Agent（代理） runs inside Capsule Service（胶囊服务） process|Implement Node.js only||
||sidecar|Agent（代理） runs beside one service and talks locally|Not implemented||
||external|Agent（代理） manages one or more services from outside|Not implemented||
||host|Agent（代理） manages services on a host|Not implemented||
||kubernetes|Agent（代理） manages services in a Kubernetes cluster|Not implemented||

The `agentMode` field should be preserved in Agent（代理） and Manifest models.

---

## 6. Embedded Agent（代理）

### 6.1 Definition

An embedded Agent（代理） runs inside the same process as the Capsule Service（胶囊服务）.

Example:

```text
Node.js service process
├── business logic
└── embedded Agent SDK
```

### 6.2 Strengths

- easiest first implementation;
- direct access to service internals;
- simple action handler registration;
- simple health provider registration;
- no extra process required.

### 6.3 Weaknesses

- requires code change in service;
- tied to runtime language;
- Agent（代理） failure may affect process if not isolated carefully;
- harder to manage legacy services that cannot embed SDK.

### 6.4 CE（社区版） relationship

CE（社区版） v0.1 implements only Node.js embedded Agent（代理）.

EE（企业版） may add embedded SDKs for:

```text
Java
Python
Go
```

---

## 7. Sidecar Agent（代理）

### 7.1 Definition

A sidecar Agent（代理） runs as a separate process close to a Capsule Service（胶囊服务）.

Example:

```text
Service Runtime
├── Capsule Service process
└── Sidecar Agent process
```

or in container form:

```text
Pod / Compose service group
├── app container
└── agent container
```

### 7.2 Communication with service

A sidecar Agent（代理） may communicate with the Capsule Service（胶囊服务） through:

```text
local HTTP management endpoint
Unix domain socket
local TCP port
local IPC
shared configuration file
mounted directory
stdout/log file observation
```

### 7.3 Responsibilities

A sidecar Agent（代理） may:

- register with Opstage（运维舞台）;
- report service manifest;
- collect health from local endpoint;
- read config metadata from local files or endpoint;
- expose predefined actions mapped to local management APIs;
- poll Commands;
- invoke local service management operations;
- report CommandResults.

### 7.4 Requirements

A sidecar Agent（代理） requires a local management contract.

Possible service-side endpoints:

```text
GET  /_capsule/manifest
GET  /_capsule/health
GET  /_capsule/configs
GET  /_capsule/actions
POST /_capsule/actions/{actionName}
```

This endpoint set is future planning and should not be required by CE（社区版） v0.1.

### 7.5 Risks

- local endpoint security;
- version compatibility;
- service discovery;
- action mapping complexity;
- deployment complexity;
- local secret boundary.

---

## 8. External Agent（代理）

### 8.1 Definition

An external Agent（代理） manages one or more Capsule Services from outside their process and immediate sidecar context.

Example:

```text
External Agent
├── manages service A through HTTP management endpoint
├── manages service B through config directory
└── manages service C through process supervisor
```

### 8.2 Use cases

External Agents may be useful for:

- legacy services;
- services that cannot embed SDK;
- services managed by file directories;
- account/session pools;
- browser automation runtimes;
- multi-process worker groups;
- small service fleets on a host.

### 8.3 Management targets

External Agent（代理） may manage targets through:

```text
HTTP management endpoint
filesystem directory
config file
process supervisor
container runtime
local script adapter
log directory
service registry
```

### 8.4 Risks

External Agent（代理） can become too powerful.

安全 rules:

- avoid arbitrary shell execution by default;
- use predefined target adapters;
- require explicit target configuration;
- audit all operations;
- use secretRef for sensitive data;
- avoid broad host-level permissions unless necessary.

---

## 9. Host Agent（代理）

### 9.1 Definition

A host Agent（代理） runs on a machine and manages multiple services on that host.

Example:

```text
Host
├── Host Agent
├── Capsule Service A
├── Capsule Service B
└── Capsule Service C
```

### 9.2 Possible responsibilities

- discover configured services;
- monitor process health;
- read service manifests;
- read config metadata;
- execute predefined host-level actions;
- report host-level metadata;
- report service status.

### 9.3 Risks

Host Agent（代理） requires strong security review because it may have broader access.

Potential risks:

- excessive filesystem access;
- process control risk;
- privilege escalation;
- secret exposure;
- arbitrary command temptation.

Host Agent（代理） should be long-term EE（企业版） work, not early EE（企业版） MVP.

---

## 10. Kubernetes Agent（代理）

### 10.1 Definition

A Kubernetes Agent（代理） manages Capsule Services running inside a Kubernetes cluster.

### 10.2 Possible responsibilities

- discover annotated workloads;
- read Kubernetes metadata;
- report Capsule Services;
- map Pods/Deployments to services;
- observe health and readiness;
- trigger predefined actions through Kubernetes APIs or service endpoints;
- integrate with ConfigMaps and Secrets by reference;
- report cluster-scoped diagnostics.

### 10.3 Possible deployment

```text
Kubernetes cluster
└── opstage-agent namespace
    ├── Agent Deployment
    ├── ServiceAccount
    ├── RBAC permissions
    └── ConfigMap / Secret
```

### 10.4 Risks

- Kubernetes RBAC complexity;
- cluster security;
- namespace isolation;
- service discovery noise;
- version compatibility;
- customer deployment diversity.

Kubernetes Agent（代理） should come after the core EE（企业版） model is validated.

---

## 11. Runtime SDK Expansion

EE（企业版） may add SDKs for additional languages.

### 11.1 Java Agent（代理） SDK

Useful for:

- Spring Boot services;
- Spring Cloud（云版） services;
- enterprise Java systems;
- existing xtrape Java ecosystem.

Possible features:

- Spring Boot starter;
- health provider integration;
- action annotation or registry;
- config metadata provider;
- Agent（代理） token store;
- HTTP polling client.

### 11.2 Python Agent（代理） SDK

Useful for:

- AI automation workers;
- data processing workers;
- browser automation scripts;
- FastAPI services;
- LangChain/LangGraph services.

Possible features:

- FastAPI integration;
- async health/action handlers;
- file token store;
- simple CLI helper;
- Python package distribution.

### 11.3 Go Agent（代理） SDK

Useful for:

- lightweight agents;
- infrastructure tools;
- single-binary deployment;
- sidecar/external Agent（代理） implementation.

Possible features:

- static binary;
- low resource usage;
- host Agent（代理） candidate;
- strong deployment story.

### 11.4 TypeScript SDK remains first

Node.js/TypeScript SDK should remain the first reference implementation.

Other SDKs should follow shared protocol and contract specs.

---

## 12. 共享 Agent（代理） Contract

All Agent（代理） modes and runtimes should follow the same logical contract.

Required capabilities:

```text
register
heartbeat
report service manifest
report health
report configs
report actions
poll or receive Commands
execute predefined action
report CommandResult
handle token invalidation
handle Backend unavailable
```

The transport may differ, but the logical contract should remain stable.

---

## 13. Agent（代理） Protocol Versioning

Agent（代理） expansion requires protocol versioning.

Recommended fields:

```text
protocolVersion
agentVersion
sdkVersion
runtime
agentMode
capabilities
```

Rules:

- use additive fields where possible;
- preserve backward compatibility where practical;
- reject unsupported versions with clear errors;
- expose compatibility warnings in UI;
- document protocol changes.

CE（社区版） v0.1 may use implicit protocol version, but should reserve schemaVersion/protocolVersion where practical.

---

## 14. Agent（代理） Capability Reporting

Agents should report what they support.

Possible capabilities:

```text
heartbeat
service-report
health-report
config-report
action-command
command-polling
command-progress
config-apply
secret-ref-resolve
log-link-report
metric-link-report
```

Capability reporting helps UI and Backend avoid assuming unsupported features.

CE（社区版） v0.1 may keep this simple.

---

## 15. Agent（代理） Diagnostics

EE（企业版） may provide stronger Agent（代理） diagnostics.

Possible diagnostic fields:

```text
lastHeartbeatAt
lastServiceReportAt
lastCommandPollAt
lastCommandResultAt
lastErrorCode
lastErrorMessage
recentErrorCount
agentVersion
sdkVersion
protocolVersion
runtime
agentMode
hostname
os
arch
connectionStatus
tokenStatus
```

Possible UI tabs:

```text
Overview
Connectivity
Runtime
Protocol
Managed Services
Recent Errors
Token State
```

---

## 16. Agent（代理） Upgrade Management

EE（企业版） may support Agent（代理） upgrade awareness.

Possible capabilities:

- show outdated Agents;
- show incompatible Agents;
- show recommended Agent（代理） version;
- provide upgrade guide;
- block unsupported protocol versions;
- show SDK changelog links;
- report Agent（代理） distribution source;
- provide upgrade health checks.

Automatic Agent（代理） upgrade is complex and should not be early EE（企业版） MVP unless strongly needed.

---

## 17. Agent（代理） Token and Credential Handling

Agent（代理） expansion must preserve token security.

Rules:

- store Agent（代理） token securely in Agent（代理） runtime;
- Backend stores only token hash;
- do not log Agent（代理） token;
- support revocation;
- support token rotation in EE（企业版）;
- validate Agent（代理） ownership for Commands;
- clear local token when revoked if practical.

Different Agent（代理） modes may use different local token stores:

```text
file token store
OS keychain
Kubernetes Secret
Vault reference
environment variable for demo only
```

---

## 18. SecretRef and Agent（代理） Expansion

Agents are often responsible for resolving `secretRef` locally.

Examples:

```text
agent-local://agent-001/secrets/chatgpt/account-001
vault://secret/path
aws-secretsmanager://region/account/secret-name
k8s-secret://namespace/name/key
```

Agent（代理） modes may resolve secrets differently:

||Agent（代理） Mode|Secret Resolution||
|---|---|
||embedded|service runtime resolves directly||
||sidecar|sidecar resolves through local provider or service endpoint||
||external|external Agent（代理） resolves configured target secrets||
||host|host Agent（代理） resolves local or enterprise secret refs||
||kubernetes|Kubernetes Agent（代理） resolves Kubernetes or external secret refs||

Default rule:

> Opstage（运维舞台） stores secretRef; Agent（代理） or customer-controlled runtime resolves the raw secret.

---

## 19. Action Execution Across Agent（代理） Modes

All Agent（代理） modes should execute only predefined actions.

### 19.1 Embedded

Action handler is registered in-process.

### 19.2 Sidecar

Action maps to local service management endpoint or local adapter.

### 19.3 External

Action maps to configured target adapter.

### 19.4 Host

Action maps to host-level predefined operation.

### 19.5 Kubernetes

Action maps to Kubernetes-safe operation or service endpoint.

安全 rule:

```text
No arbitrary shell execution by default.
```

---

## 20. Service Discovery

EE（企业版） may support limited service discovery.

Possible discovery sources:

```text
explicit config file
management endpoint
Docker labels
Kubernetes annotations
filesystem directory
service registry
manual UI registration
```

Recommended approach:

- start explicit;
- avoid magical discovery early;
- require operator confirmation for discovered services;
- keep service code stable;
- audit service onboarding.

CE（社区版） v0.1 does not need discovery beyond embedded SDK manifest report.

---

## 21. Agent（代理） 配置

Different Agent（代理） modes need configuration.

Possible configuration sources:

```text
environment variables
YAML file
JSON file
command-line flags
Kubernetes ConfigMap
Opstage-issued bootstrap config
```

Common configuration:

```text
backendUrl
registrationToken
agentTokenStore
agentCode
agentName
workspaceCode
heartbeatInterval
commandPollInterval
managedTargets
proxy settings
log level
```

---

## 22. Agent（代理） Networking

Agent（代理） expansion should preserve outbound-first communication.

Recommended rule:

```text
Agent -> Opstage Backend / Gateway
```

Do not require:

```text
Opstage -> Agent inbound connection
```

unless a specific private deployment explicitly 支持 it.

Agent（代理） networking should support:

- HTTP polling baseline;
- proxy configuration;
- retry with backoff;
- offline tolerance;
- future WebSocket/gRPC modes.

---

## 23. Agent（代理） Fleet Management

EE（企业版） may add Agent（代理） fleet management.

Possible capabilities:

- Agent（代理） list by version;
- Agent（代理） list by runtime;
- Agent（代理） list by mode;
- outdated Agent（代理） report;
- offline Agent（代理） report;
- revoked Agent（代理） report;
- Agent（代理） token expiration report;
- Agent（代理） capability matrix;
- Agent（代理） upgrade recommendation.

This should come after multiple Agent（代理） types exist.

---

## 24. Agent（代理） Packaging

Different Agent（代理） modes may have different packaging.

### 24.1 SDK packages

Examples:

```text
npm package for Node.js
Maven artifact for Java
PyPI package for Python
Go module for Go
```

### 24.2 Sidecar/external binaries

Possible packaging:

```text
Docker image
single binary
systemd service package
Kubernetes image
```

### 24.3 文档

Each Agent（代理） package should include:

- installation guide;
- configuration reference;
- security guide;
- example service integration;
- troubleshooting guide.

---

## 25. Compatibility Matrix

EE（企业版） may maintain an Agent（代理） compatibility matrix.

Example:

||Agent（代理） Runtime|Agent（代理） Mode|状态|Notes||
|---|---|---|---|
||Node.js|embedded|CE（社区版） reference|first implementation||
||Java|embedded|planned|Spring Boot candidate||
||Python|embedded|planned|AI automation candidate||
||Go|sidecar/external|planned|single-binary candidate||
||Kubernetes|kubernetes|long-term|cluster integration||

This matrix should be updated with real implementation status.

---

## 26. Agent（代理） 安全 Risks

Agent（代理） expansion introduces security risks.

Risks:

- overprivileged external Agent（代理）;
- arbitrary command execution temptation;
- local management endpoint exposure;
- filesystem over-access;
- secret leakage;
- weak token storage;
- service discovery abuse;
- cross-service command mistakes;
- Kubernetes RBAC overreach.

Mitigations:

- predefined actions only;
- explicit target configuration;
- least privilege;
- token hashing and revocation;
- secretRef boundary;
- audit all operations;
- local endpoint authentication;
- documented deployment security.

---

## 27. EE（企业版） Agent（代理） MVP Candidate

A future EE（企业版） Agent（代理） MVP may include:

- Node.js embedded Agent（代理） from CE（社区版）;
- Java embedded Agent（代理） prototype;
- sidecar Agent（代理） prototype;
- shared Agent（代理） protocol version field;
- Agent（代理） capability reporting;
- Agent（代理） diagnostics UI;
- Agent（代理） token rotation;
- Agent（代理） compatibility warning;
- explicit sidecar management endpoint contract draft.

This is a candidate only and should be validated by real enterprise needs.

---

## 28. Long-Term Agent（代理） Capabilities

Long-term EE（企业版） Agent（代理） expansion may include:

- Python SDK;
- Go SDK;
- external Agent（代理）;
- host Agent（代理）;
- Kubernetes Agent（代理）;
- Agent（代理） Gateway;
- WebSocket/gRPC protocol;
- automatic Agent（代理） upgrade awareness;
- Agent（代理） marketplace;
- verified action packs;
- service discovery integrations;
- enterprise secret provider resolvers;
- offline command queueing.

These should not be implemented before the shared Agent（代理） contract is stable.

---

## 29. CE（社区版） Reservations

CE（社区版） should reserve these Agent（代理）-expansion-compatible concepts:

```text
agentMode
runtime
agentVersion
schemaVersion
protocolVersion if practical
capabilities
Agent token hash
registration token hash
service manifest
health report
config metadata
action definition
Command
CommandResult
secretRef
metadataJson
```

CE（社区版） should not implement:

```text
sidecar Agent
external Agent
host Agent
Kubernetes Agent
Java/Python/Go SDKs
Agent Gateway
Agent upgrade manager
Agent fleet diagnostics
service discovery
WebSocket/gRPC Agent protocol
```

---

## 30. Anti-Patterns

Avoid these patterns.

### 30.1 Agent（代理） modes with incompatible contracts

All Agent（代理） modes must preserve the shared governance contract.

### 30.2 Arbitrary shell as default Agent（代理） power

Predefined actions should remain the safe operation model.

### 30.3 Service discovery without confirmation

Automatic discovery can create noise and security risks.

### 30.4 Agent（代理） token in logs

Agent（代理） tokens must never be logged.

### 30.5 Local management endpoint exposed publicly

Sidecar/local endpoints should be local and protected.

### 30.6 Building all Agent（代理） modes before CE（社区版） is stable

Agent（代理） expansion should follow validated usage.

---

## 31. Acceptance Criteria

EE（企业版） Agent（代理） expansion planning is acceptable when:

- Agent（代理） modes are clearly defined;
- CE（社区版） remains focused on Node.js embedded Agent（代理）;
- all future modes preserve the shared contract;
- sidecar and external Agent（代理） responsibilities are clear;
- multi-language SDK direction is clear;
- protocol versioning and capability reporting are planned;
- Agent（代理） diagnostics and upgrade awareness are included;
- secretRef remains the default secret boundary;
- no arbitrary shell default is introduced;
- CE（社区版） reservations are clear.

---

## 32. Summary

Opstage（运维舞台） EE（企业版） Agent（代理） expansion should allow more runtimes and deployment patterns to become governable without breaking the CE（社区版） Agent（代理） model.

The most important Agent（代理） expansion rule is:

> Expand Agent（代理） modes and runtimes only through a shared, versioned, safe governance contract centered on manifests, health, configs, actions, commands, results, audit, and secretRef.
