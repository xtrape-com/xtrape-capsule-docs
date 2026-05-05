---
status: proposed
audience: founders
stability: evolving
last_reviewed: 2026-05-05
edition: ee
phase: future
---

# EE Agent Expansion

- Status: Planning
- Edition: EE
- Priority: Future
- Audience: architects, agent SDK developers, backend developers, platform engineers, DevOps engineers, AI coding agents

This document defines the planned Agent expansion model for **Opstage EE / Enterprise Edition**.

Opstage EE is the future private commercial edition of the `xtrape-capsule` product family. Agent expansion capabilities are not CE v0.1 implementation requirements.

---

## 1. Purpose

The purpose of this document is to define:

- how EE may expand beyond the CE Node.js embedded Agent;
- what Agent modes should exist in the long-term model;
- how sidecar and external Agents may work;
- how Java, Python, and Go Agent SDKs may be introduced;
- how Agent protocol compatibility should be preserved;
- how Agent diagnostics, upgrades, and version management may work;
- which Agent concepts CE should reserve without implementing EE complexity.

The key rule is:

> EE may expand Agent modes and runtimes, but all Agents must preserve the same core governance contract.

---

## 2. Agent Expansion Goal

The goal of EE Agent expansion is:

> Allow different types of Capsule Services and enterprise runtimes to become governable by Opstage without forcing all services to embed the same Node.js SDK.

EE Agent expansion should support:

- non-Node.js services;
- legacy services;
- services that cannot embed an SDK;
- sidecar deployment patterns;
- external management patterns;
- enterprise runtime diversity;
- larger Agent fleets;
- stronger diagnostics and version management.

---

## 3. EE Agent Expansion Is Not CE v0.1

CE v0.1 must not implement full Agent expansion.

Out of scope for CE v0.1:

- sidecar Agent;
- external Agent;
- host Agent;
- Kubernetes Agent;
- Java Agent SDK;
- Python Agent SDK;
- Go Agent SDK;
- Agent Gateway;
- WebSocket or gRPC Agent protocol;
- Agent upgrade manager;
- Agent fleet diagnostics;
- Agent marketplace;
- automatic service discovery.

CE v0.1 should implement only:

```text
Node.js embedded Agent SDK
HTTP heartbeat
service report
command polling
CommandResult reporting
predefined action execution
```

---

## 4. Relationship with CE Agent

CE Agent model:

```text
Node.js Capsule Service
    ↓ in-process SDK
Node.js Embedded Agent
    ↓ HTTP Agent API
Opstage Backend
```

EE should extend this model to support additional modes:

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

## 5. Agent Mode Overview

Recommended long-term Agent modes:

| Mode | Description | CE v0.1 |
|---|---|---|
| embedded | Agent runs inside Capsule Service process | Implement Node.js only |
| sidecar | Agent runs beside one service and talks locally | Not implemented |
| external | Agent manages one or more services from outside | Not implemented |
| host | Agent manages services on a host | Not implemented |
| kubernetes | Agent manages services in a Kubernetes cluster | Not implemented |

The `agentMode` field should be preserved in Agent and Manifest models.

---

## 6. Embedded Agent

### 6.1 Definition

An embedded Agent runs inside the same process as the Capsule Service.

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
- Agent failure may affect process if not isolated carefully;
- harder to manage legacy services that cannot embed SDK.

### 6.4 CE relationship

CE v0.1 implements only Node.js embedded Agent.

EE may add embedded SDKs for:

```text
Java
Python
Go
```

---

## 7. Sidecar Agent

### 7.1 Definition

A sidecar Agent runs as a separate process close to a Capsule Service.

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

A sidecar Agent may communicate with the Capsule Service through:

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

A sidecar Agent may:

- register with Opstage;
- report service manifest;
- collect health from local endpoint;
- read config metadata from local files or endpoint;
- expose predefined actions mapped to local management APIs;
- poll Commands;
- invoke local service management operations;
- report CommandResults.

### 7.4 Requirements

A sidecar Agent requires a local management contract.

Possible service-side endpoints:

```text
GET  /_capsule/manifest
GET  /_capsule/health
GET  /_capsule/configs
GET  /_capsule/actions
POST /_capsule/actions/{actionName}
```

This endpoint set is future planning and should not be required by CE v0.1.

### 7.5 Risks

- local endpoint security;
- version compatibility;
- service discovery;
- action mapping complexity;
- deployment complexity;
- local secret boundary.

---

## 8. External Agent

### 8.1 Definition

An external Agent manages one or more Capsule Services from outside their process and immediate sidecar context.

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

External Agent may manage targets through:

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

External Agent can become too powerful.

Security rules:

- avoid arbitrary shell execution by default;
- use predefined target adapters;
- require explicit target configuration;
- audit all operations;
- use secretRef for sensitive data;
- avoid broad host-level permissions unless necessary.

---

## 9. Host Agent

### 9.1 Definition

A host Agent runs on a machine and manages multiple services on that host.

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

Host Agent requires strong security review because it may have broader access.

Potential risks:

- excessive filesystem access;
- process control risk;
- privilege escalation;
- secret exposure;
- arbitrary command temptation.

Host Agent should be long-term EE work, not early EE MVP.

---

## 10. Kubernetes Agent

### 10.1 Definition

A Kubernetes Agent manages Capsule Services running inside a Kubernetes cluster.

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

Kubernetes Agent should come after the core EE model is validated.

---

## 11. Runtime SDK Expansion

EE may add SDKs for additional languages.

### 11.1 Java Agent SDK

Useful for:

- Spring Boot services;
- Spring Cloud services;
- enterprise Java systems;
- existing xtrape Java ecosystem.

Possible features:

- Spring Boot starter;
- health provider integration;
- action annotation or registry;
- config metadata provider;
- Agent token store;
- HTTP polling client.

### 11.2 Python Agent SDK

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

### 11.3 Go Agent SDK

Useful for:

- lightweight agents;
- infrastructure tools;
- single-binary deployment;
- sidecar/external Agent implementation.

Possible features:

- static binary;
- low resource usage;
- host Agent candidate;
- strong deployment story.

### 11.4 TypeScript SDK remains first

Node.js/TypeScript SDK should remain the first reference implementation.

Other SDKs should follow shared protocol and contract specs.

---

## 12. Shared Agent Contract

All Agent modes and runtimes should follow the same logical contract.

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

## 13. Agent Protocol Versioning

Agent expansion requires protocol versioning.

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

CE v0.1 may use implicit protocol version, but should reserve schemaVersion/protocolVersion where practical.

---

## 14. Agent Capability Reporting

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

CE v0.1 may keep this simple.

---

## 15. Agent Diagnostics

EE may provide stronger Agent diagnostics.

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

## 16. Agent Upgrade Management

EE may support Agent upgrade awareness.

Possible capabilities:

- show outdated Agents;
- show incompatible Agents;
- show recommended Agent version;
- provide upgrade guide;
- block unsupported protocol versions;
- show SDK changelog links;
- report Agent distribution source;
- provide upgrade health checks.

Automatic Agent upgrade is complex and should not be early EE MVP unless strongly needed.

---

## 17. Agent Token and Credential Handling

Agent expansion must preserve token security.

Rules:

- store Agent token securely in Agent runtime;
- Backend stores only token hash;
- do not log Agent token;
- support revocation;
- support token rotation in EE;
- validate Agent ownership for Commands;
- clear local token when revoked if practical.

Different Agent modes may use different local token stores:

```text
file token store
OS keychain
Kubernetes Secret
Vault reference
environment variable for demo only
```

---

## 18. SecretRef and Agent Expansion

Agents are often responsible for resolving `secretRef` locally.

Examples:

```text
agent-local://agent-001/secrets/chatgpt/account-001
vault://secret/path
aws-secretsmanager://region/account/secret-name
k8s-secret://namespace/name/key
```

Agent modes may resolve secrets differently:

| Agent Mode | Secret Resolution |
|---|---|
| embedded | service runtime resolves directly |
| sidecar | sidecar resolves through local provider or service endpoint |
| external | external Agent resolves configured target secrets |
| host | host Agent resolves local or enterprise secret refs |
| kubernetes | Kubernetes Agent resolves Kubernetes or external secret refs |

Default rule:

> Opstage stores secretRef; Agent or customer-controlled runtime resolves the raw secret.

---

## 19. Action Execution Across Agent Modes

All Agent modes should execute only predefined actions.

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

Security rule:

```text
No arbitrary shell execution by default.
```

---

## 20. Service Discovery

EE may support limited service discovery.

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

CE v0.1 does not need discovery beyond embedded SDK manifest report.

---

## 21. Agent Configuration

Different Agent modes need configuration.

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

## 22. Agent Networking

Agent expansion should preserve outbound-first communication.

Recommended rule:

```text
Agent -> Opstage Backend / Gateway
```

Do not require:

```text
Opstage -> Agent inbound connection
```

unless a specific private deployment explicitly supports it.

Agent networking should support:

- HTTP polling baseline;
- proxy configuration;
- retry with backoff;
- offline tolerance;
- future WebSocket/gRPC modes.

---

## 23. Agent Fleet Management

EE may add Agent fleet management.

Possible capabilities:

- Agent list by version;
- Agent list by runtime;
- Agent list by mode;
- outdated Agent report;
- offline Agent report;
- revoked Agent report;
- Agent token expiration report;
- Agent capability matrix;
- Agent upgrade recommendation.

This should come after multiple Agent types exist.

---

## 24. Agent Packaging

Different Agent modes may have different packaging.

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

### 24.3 Documentation

Each Agent package should include:

- installation guide;
- configuration reference;
- security guide;
- example service integration;
- troubleshooting guide.

---

## 25. Compatibility Matrix

EE may maintain an Agent compatibility matrix.

Example:

| Agent Runtime | Agent Mode | Status | Notes |
|---|---|---|---|
| Node.js | embedded | CE reference | first implementation |
| Java | embedded | planned | Spring Boot candidate |
| Python | embedded | planned | AI automation candidate |
| Go | sidecar/external | planned | single-binary candidate |
| Kubernetes | kubernetes | long-term | cluster integration |

This matrix should be updated with real implementation status.

---

## 26. Agent Security Risks

Agent expansion introduces security risks.

Risks:

- overprivileged external Agent;
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

## 27. EE Agent MVP Candidate

A future EE Agent MVP may include:

- Node.js embedded Agent from CE;
- Java embedded Agent prototype;
- sidecar Agent prototype;
- shared Agent protocol version field;
- Agent capability reporting;
- Agent diagnostics UI;
- Agent token rotation;
- Agent compatibility warning;
- explicit sidecar management endpoint contract draft.

This is a candidate only and should be validated by real enterprise needs.

---

## 28. Long-Term Agent Capabilities

Long-term EE Agent expansion may include:

- Python SDK;
- Go SDK;
- external Agent;
- host Agent;
- Kubernetes Agent;
- Agent Gateway;
- WebSocket/gRPC protocol;
- automatic Agent upgrade awareness;
- Agent marketplace;
- verified action packs;
- service discovery integrations;
- enterprise secret provider resolvers;
- offline command queueing.

These should not be implemented before the shared Agent contract is stable.

---

## 29. CE Reservations

CE should reserve these Agent-expansion-compatible concepts:

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

CE should not implement:

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

### 30.1 Agent modes with incompatible contracts

All Agent modes must preserve the shared governance contract.

### 30.2 Arbitrary shell as default Agent power

Predefined actions should remain the safe operation model.

### 30.3 Service discovery without confirmation

Automatic discovery can create noise and security risks.

### 30.4 Agent token in logs

Agent tokens must never be logged.

### 30.5 Local management endpoint exposed publicly

Sidecar/local endpoints should be local and protected.

### 30.6 Building all Agent modes before CE is stable

Agent expansion should follow validated usage.

---

## 31. Acceptance Criteria

EE Agent expansion planning is acceptable when:

- Agent modes are clearly defined;
- CE remains focused on Node.js embedded Agent;
- all future modes preserve the shared contract;
- sidecar and external Agent responsibilities are clear;
- multi-language SDK direction is clear;
- protocol versioning and capability reporting are planned;
- Agent diagnostics and upgrade awareness are included;
- secretRef remains the default secret boundary;
- no arbitrary shell default is introduced;
- CE reservations are clear.

---

## 32. Summary

Opstage EE Agent expansion should allow more runtimes and deployment patterns to become governable without breaking the CE Agent model.

The most important Agent expansion rule is:

> Expand Agent modes and runtimes only through a shared, versioned, safe governance contract centered on manifests, health, configs, actions, commands, results, audit, and secretRef.
