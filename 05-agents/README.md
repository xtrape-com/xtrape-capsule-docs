# Agent Overview

- Status: Draft
- Edition: Shared
- Priority: High

本文件属于 `xtrape-capsule` 文档集。`xtrape-capsule` 是面向轻服务 / Capsule Service 的领域体系；`xtrape-capsule-opstage` 是该体系下的统一运行态治理平台。

当前实现重点是 CE 开源社区版。EE 私有化商业版与 Cloud SaaS 版属于未来规划，CE 需要保留扩展点，但不应在早期版本实现其完整能力。

Agent 是 Capsule Service 加入 Opstage 治理体系的授权入口。CE 第一版实现 Node.js Embedded Agent，Sidecar 和 External Agent 属于后续扩展。

# Agent Documents

- Status: Implementation Guidance
- Edition: Shared
- Priority: High
- Audience: architects, backend developers, agent SDK developers, Capsule Service developers, security reviewers, AI coding agents

This directory contains the Agent-related documents for the `xtrape-capsule` product family.

An Agent is the authorized runtime bridge that connects Capsule Services to Opstage governance.

The current implementation focus is **CE**. CE v0.1 implements only the **Node.js Embedded Agent SDK**. Sidecar Agent, External Agent, multi-language SDKs, Agent Gateway, and advanced Agent policy capabilities are future EE/Cloud extension tracks and must not expand the CE v0.1 implementation scope.

---

## 1. Purpose of This Directory

The purpose of this directory is to define how Agents work in the Capsule governance model.

It covers:

- the overall Agent concept;
- the Embedded Agent model;
- future Sidecar Agent direction;
- future External Agent direction;
- the Node.js Agent SDK implementation target;
- Agent permissions and ownership boundaries;
- Agent security rules;
- CE implementation scope;
- EE and Cloud extension points.

Agents are the runtime-side entry point into Opstage.

---

## 2. Agent Positioning

An Agent is:

> The authorized governance bridge between Opstage Backend and one or more Capsule Services.

An Agent enables Opstage to:

- register runtime participants;
- authenticate Agent communication;
- receive heartbeat signals;
- receive service manifests;
- receive health reports;
- receive config metadata;
- receive predefined action metadata;
- deliver Commands;
- receive CommandResults;
- support AuditEvents;
- calculate freshness and effective status.

An Agent should not become an unrestricted runtime controller.

---

## 3. Current CE Agent Boundary

CE v0.1 should implement only:

```text
Node.js Embedded Agent SDK
```

CE Agent implementation should support:

- registration with registration token;
- Agent token storage;
- authenticated heartbeat;
- service manifest report;
- health provider;
- config provider;
- action registry;
- command polling;
- predefined action execution;
- CommandResult reporting;
- safe retry/backoff;
- safe logging;
- sensitive data avoidance.

CE should not implement Sidecar Agent or External Agent in v0.1.

---

## 4. CE Agent Non-Goals

CE v0.1 should not implement:

- Sidecar Agent;
- External Agent;
- Host Agent;
- Kubernetes Agent;
- Java Agent SDK;
- Python Agent SDK;
- Go Agent SDK;
- Agent Gateway;
- WebSocket/gRPC command delivery;
- multi-target management;
- automatic service discovery;
- Agent fleet management;
- Agent auto-upgrade;
- enterprise secret provider integration;
- arbitrary shell execution;
- remote terminal.

These are future planning topics.

---

## 5. Recommended Reading Order

Read the documents in this directory in the following order:

```text
05-agents/README.md
05-agents/00-agent-overview.md
05-agents/01-embedded-agent.md
05-agents/04-node-agent-sdk.md
05-agents/05-agent-permission-model.md
05-agents/02-sidecar-agent.md
05-agents/03-external-agent.md
```

For CE implementation, focus on:

```text
00-agent-overview.md
01-embedded-agent.md
04-node-agent-sdk.md
05-agent-permission-model.md
```

For future EE planning, read:

```text
02-sidecar-agent.md
03-external-agent.md
```

---

## 6. Document List

### 6.1 `00-agent-overview.md`

Defines the overall Agent concept.

Use it to understand:

- Agent positioning;
- Agent responsibilities;
- relationship with Capsule Services;
- relationship with Opstage;
- Agent modes;
- CE Agent scope;
- future EE/Cloud Agent directions;
- security and data boundaries.

### 6.2 `01-embedded-agent.md`

Defines the Embedded Agent model.

Use it to understand and implement:

- in-process Agent runtime;
- Node.js Embedded Agent responsibilities;
- SDK lifecycle;
- registration;
- token store;
- heartbeat;
- manifest report;
- health/config/action providers;
- command polling;
- CommandResult reporting;
- safe offline behavior.

### 6.3 `02-sidecar-agent.md`

Defines the future Sidecar Agent model.

Use it for EE planning around:

- separate nearby Agent process;
- local management interface;
- local HTTP management contract;
- sidecar deployment models;
- sidecar security boundary;
- comparison with Embedded Agent.

This is not a CE v0.1 implementation target.

### 6.4 `03-external-agent.md`

Defines the future External Agent model.

Use it for EE planning around:

- explicit target-based management;
- multi-target Agent process;
- adapter model;
- browser/account/session targets;
- process supervisor targets;
- action allowlists;
- stronger permission and secret boundaries.

This is not a CE v0.1 implementation target.

### 6.5 `04-node-agent-sdk.md`

Defines the CE Node.js Agent SDK implementation target.

Use it to implement:

- npm package structure;
- public SDK API;
- `CapsuleAgent` class;
- options and environment variables;
- file token store;
- Agent registration;
- heartbeat loop;
- manifest construction;
- health provider API;
- config provider API;
- action registration API;
- command polling loop;
- CommandResult reporting;
- retry/backoff;
- logging and sanitization;
- demo Capsule Service integration;
- SDK tests.

This is a CE v0.1 implementation target.

### 6.6 `05-agent-permission-model.md`

Defines Agent permission boundaries.

Use it to implement:

- Agent token authentication;
- Agent identity context;
- Agent-owned service reporting;
- Agent-owned Command polling;
- CommandResult ownership validation;
- Agent token isolation from Admin API;
- disabled/revoked/offline Agent behavior;
- permission-related audit events.

---

## 7. Agent Mode Summary

Long-term Agent modes may include:

| Mode | Description | CE v0.1 |
|---|---|---|
| embedded | Agent runs inside Capsule Service process | Node.js only |
| sidecar | Agent runs beside one Capsule Service | Not implemented |
| external | Agent manages explicit external targets | Not implemented |
| host | Agent manages services on one host | Not implemented |
| kubernetes | Agent manages Kubernetes workloads | Not implemented |

CE should reserve the `agentMode` concept, but implement only `embedded`.

---

## 8. Shared Agent Contract

All Agent modes should preserve the same logical contract:

```text
registration
Agent token authentication
heartbeat
service manifest report
health report
config metadata report
action definition report
Command polling or receiving
predefined action execution
CommandResult reporting
AuditEvent creation by Backend
```

Future Agent modes may use different local integration patterns, but they should not redefine the governance contract.

---

## 9. Agent Security Rules

All Agent documents should follow these security rules:

1. Registration token is used only for enrollment.
2. Agent token authenticates Agent API calls.
3. Backend stores only token hashes.
4. Raw tokens must not be logged.
5. Agent authority is derived from authenticated token identity.
6. Agent can only report its own services.
7. Agent can only poll Commands assigned to itself.
8. Agent can only report CommandResults for its own Commands.
9. Agents execute only predefined actions.
10. Arbitrary shell execution is not part of CE.
11. Raw secrets are not reported to Opstage by default.
12. Sensitive references should use `secretRef`.

---

## 10. Data Boundary

Agents may send governance metadata to Opstage:

- Agent metadata;
- service manifest;
- health status;
- config metadata;
- action metadata;
- CommandResult;
- sanitized errors.

Agents should not send raw sensitive data by default:

- passwords;
- cookies;
- OAuth tokens;
- API keys;
- private keys;
- account credentials;
- raw browser sessions;
- large application logs;
- private customer business records.

Use `secretRef`, masked values, or summaries where needed.

---

## 11. Implementation Priority for CE

Recommended CE Agent implementation order:

```text
1. Node Agent SDK package scaffold
2. CapsuleAgent options and environment loading
3. File token store
4. Registration client
5. Agent token authentication client
6. Manifest builder
7. Health provider
8. Config provider
9. Action registry
10. Heartbeat loop
11. Command polling loop
12. CommandResult reporting
13. Sanitized logging
14. Demo Capsule Service
15. SDK tests
```

This order proves the runtime-side governance loop step by step.

---

## 12. Extension Rules

CE should reserve clean extension points:

```text
agentMode
runtime
agentVersion
sdkVersion
protocolVersion
capabilities
secretRef
metadataJson
commandType
```

CE should not implement future systems just because extension fields exist.

The rule is:

> Keep CE Agent small and complete; make future Agent modes compatible, not required.

---

## 13. Acceptance Criteria

The Agent document set is useful when:

- Agent's role is clear;
- CE Agent boundary is clear;
- Node.js Embedded Agent is clearly the first implementation target;
- Sidecar and External Agents are clearly future planning documents;
- SDK API and lifecycle are concrete enough for implementation;
- Agent permission boundaries are explicit;
- Agent security and data boundaries are explicit;
- arbitrary shell execution is excluded from CE;
- implementation agents can follow the reading order and build the Node Agent SDK.

---

## 14. Summary

This directory defines the Agent side of the Capsule governance model.

The most important Agent directory rule is:

> Build the Node.js Embedded Agent SDK first as a safe, outbound-first, predefined-action-based governance bridge; keep Sidecar, External, and multi-language Agents as future extensions.