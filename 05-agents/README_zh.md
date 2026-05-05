---
status: draft
audience: architects
stability: unstable
last_reviewed: 2026-05-05
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: README.md
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

# Agent（代理） Documents

- Status: 实施指南
- Edition: 共享
- Priority: 高
- Audience: architects, backend developers, agent SDK developers, Capsule Service（胶囊服务） developers, security reviewers, AI coding agents

This directory 包含 the Agent（代理）-related documents for the `xtrape-capsule` product family.

An Agent（代理） is the authorized runtime bridge that connects Capsule Services to Opstage（运维舞台） governance.

The current implementation focus is **CE（社区版）**. CE（社区版） v0.1 implements only the **Node.js Embedded Agent（代理） SDK**.
Sidecar Agent（代理）, External Agent（代理）, multi-language SDKs, Agent（代理） Gateway, and advanced Agent（代理） policy
capabilities are future EE（企业版）/Cloud（云版） extension tracks and must not expand the CE（社区版） v0.1 implementation scope.

---

## 1. Purpose of This Directory

The purpose of this directory is to define how Agents work in the Capsule governance model.

It 涵盖:

- the overall Agent（代理） concept;
- the Embedded Agent（代理） model;
- future Sidecar Agent（代理） direction;
- future External Agent（代理） direction;
- the Node.js Agent（代理） SDK implementation target;
- Agent（代理） permissions and ownership boundaries;
- Agent（代理） security rules;
- CE（社区版） implementation scope;
- EE（企业版） and Cloud（云版） extension points.

Agents are the runtime-side entry point into Opstage（运维舞台）.

---

## 2. Agent（代理） Positioning

An Agent（代理） is:

> The authorized governance bridge between Opstage（运维舞台） Backend and one or more Capsule Services.

An Agent（代理） enables Opstage（运维舞台） to:

- register runtime participants;
- authenticate Agent（代理） communication;
- receive heartbeat signals;
- receive service manifests;
- receive health reports;
- receive config metadata;
- receive predefined action metadata;
- deliver Commands;
- receive CommandResults;
- support AuditEvents;
- calculate freshness and effective status.

An Agent（代理） should not become an unrestricted runtime controller.

---

## 3. Current CE（社区版） Agent（代理） Boundary

CE（社区版） v0.1 should implement only:

```text
Node.js Embedded Agent SDK
```

CE（社区版） Agent（代理） implementation should support:

- registration with registration token;
- Agent（代理） token storage;
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

CE（社区版） should not implement Sidecar Agent（代理） or External Agent（代理） in v0.1.

---

## 4. CE（社区版） Agent（代理） Non-Goals

CE（社区版） v0.1 should not implement:

- Sidecar Agent（代理）;
- External Agent（代理）;
- Host Agent（代理）;
- Kubernetes Agent（代理）;
- Java Agent（代理） SDK;
- Python Agent（代理） SDK;
- Go Agent（代理） SDK;
- Agent（代理） Gateway;
- WebSocket/gRPC command delivery;
- multi-target management;
- automatic service discovery;
- Agent（代理） fleet management;
- Agent（代理） auto-upgrade;
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

For CE（社区版） implementation, focus on:

```text
00-agent-overview.md
01-embedded-agent.md
04-node-agent-sdk.md
05-agent-permission-model.md
```

For future EE（企业版） planning, read:

```text
02-sidecar-agent.md
03-external-agent.md
```

---

## 6. Document List

### 6.1 `00-agent-overview.md`

Defines the overall Agent（代理） concept.

Use it to understand:

- Agent（代理） positioning;
- Agent（代理） responsibilities;
- relationship with Capsule Services;
- relationship with Opstage（运维舞台）;
- Agent（代理） modes;
- CE（社区版） Agent（代理） scope;
- future EE（企业版）/Cloud（云版） Agent（代理） directions;
- security and data boundaries.

### 6.2 `01-embedded-agent.md`

Defines the Embedded Agent（代理） model.

Use it to understand and implement:

- in-process Agent（代理） runtime;
- Node.js Embedded Agent（代理） responsibilities;
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

Defines the future Sidecar Agent（代理） model.

Use it for EE（企业版） planning around:

- separate nearby Agent（代理） process;
- local management interface;
- local HTTP management contract;
- sidecar deployment models;
- sidecar security boundary;
- comparison with Embedded Agent（代理）.

This is not a CE（社区版） v0.1 implementation target.

### 6.4 `03-external-agent.md`

Defines the future External Agent（代理） model.

Use it for EE（企业版） planning around:

- explicit target-based management;
- multi-target Agent（代理） process;
- adapter model;
- browser/account/session targets;
- process supervisor targets;
- action allowlists;
- stronger permission and secret boundaries.

This is not a CE（社区版） v0.1 implementation target.

### 6.5 `04-node-agent-sdk.md`

Defines the CE（社区版） Node.js Agent（代理） SDK implementation target.

Use it to implement:

- npm package structure;
- public SDK API;
- `CapsuleAgent` class;
- options and environment variables;
- file token store;
- Agent（代理） registration;
- heartbeat loop;
- manifest construction;
- health provider API;
- config provider API;
- action registration API;
- command polling loop;
- CommandResult reporting;
- retry/backoff;
- logging and sanitization;
- demo Capsule Service（胶囊服务） integration;
- SDK tests.

This is a CE（社区版） v0.1 implementation target.

### 6.6 `05-agent-permission-model.md`

Defines Agent（代理） permission boundaries.

Use it to implement:

- Agent（代理） token authentication;
- Agent（代理） identity context;
- Agent（代理）-owned service reporting;
- Agent（代理）-owned Command polling;
- CommandResult ownership validation;
- Agent（代理） token isolation from Admin API;
- disabled/revoked/offline Agent（代理） behavior;
- permission-related audit events.

---

## 7. Agent（代理） Mode Summary

Long-term Agent（代理） modes may include:

||Mode|Description|CE（社区版） v0.1||
|---|---|---|
||embedded|Agent（代理） runs inside Capsule Service（胶囊服务） process|Node.js only||
||sidecar|Agent（代理） runs beside one Capsule Service（胶囊服务）|Not implemented||
||external|Agent（代理） manages explicit external targets|Not implemented||
||host|Agent（代理） manages services on one host|Not implemented||
||kubernetes|Agent（代理） manages Kubernetes workloads|Not implemented||

CE（社区版） should reserve the `agentMode` concept, but implement only `embedded`.

---

## 8. 共享 Agent（代理） Contract

All Agent（代理） modes should preserve the same logical contract:

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

Future Agent（代理） modes may use different local integration patterns, but they should not redefine the governance contract.

---

## 9. Agent（代理） 安全 Rules

All Agent（代理） documents should follow these security rules:

1. Registration token is used only for enrollment.
2. Agent（代理） token authenticates Agent（代理） API calls.
3. Backend stores only token hashes.
4. Raw tokens must not be logged.
5. Agent（代理） authority is derived from authenticated token identity.
6. Agent（代理） can only report its own services.
7. Agent（代理） can only poll Commands assigned to itself.
8. Agent（代理） can only report CommandResults for its own Commands.
9. Agents execute only predefined actions.
10. Arbitrary shell execution is not part of CE（社区版）.
11. Raw secrets are not reported to Opstage（运维舞台） by default.
12. Sensitive references should use `secretRef`.

---

## 10. Data Boundary

Agents may send governance metadata to Opstage（运维舞台）:

- Agent（代理） metadata;
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

## 11. 实现 优先级 for CE（社区版）

Recommended CE（社区版） Agent（代理） implementation order:

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

CE（社区版） should reserve clean extension points:

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

CE（社区版） should not implement future systems just because extension fields exist.

The rule is:

> Keep CE（社区版） Agent（代理） small and complete; make future Agent（代理） modes compatible, not required.

---

## 13. Acceptance Criteria

The Agent（代理） document set is useful when:

- Agent（代理）'s role is clear;
- CE（社区版） Agent（代理） boundary is clear;
- Node.js Embedded Agent（代理） is clearly the first implementation target;
- Sidecar and External Agents are clearly future planning documents;
- SDK API and lifecycle are concrete enough for implementation;
- Agent（代理） permission boundaries are explicit;
- Agent（代理） security and data boundaries are explicit;
- arbitrary shell execution is excluded from CE（社区版）;
- implementation agents can follow the reading order and build the Node Agent（代理） SDK.

---

## 14. Summary

This directory 定义 the Agent（代理） side of the Capsule governance model.

The most important Agent（代理） directory rule is:

> Build the Node.js Embedded Agent（代理） SDK first as a safe, outbound-first, predefined-action-based governance bridge; keep Sidecar, External, and multi-language Agents as future extensions.
