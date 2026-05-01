<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 03-cloud-agent-connectivity.md
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

# Cloud（云版） Agent（代理） Connectivity

- Status: Planning
- Edition: Cloud（云版）
- Priority: Future
- Audience: architects, cloud engineers, backend developers, agent SDK developers, security reviewers, AI coding agents

This document 定义 the planned Agent（代理） connectivity model for **Opstage（运维舞台） Cloud（云版）**.

Opstage（运维舞台） Cloud（云版） is the future hosted SaaS edition of the `xtrape-capsule` product family. Cloud（云版） Agent（代理） connectivity is a future capability, not a CE（社区版） v0.1 implementation requirement.

---

## 1. Purpose

The purpose of this document is to define:

- how customer-side Agents should connect to Opstage（运维舞台） Cloud（云版）;
- why outbound-first connectivity is the default model;
- how CE（社区版） heartbeat and command polling can evolve into Cloud（云版） connectivity;
- what an Agent（代理） Gateway may do;
- how network restrictions, proxies, NAT, and firewalls should be handled;
- how command delivery may evolve;
- what diagnostics Cloud（云版） should provide;
- which connectivity features must not be pulled into CE（社区版） v0.1.

The key rule is:

> Agents connect outbound to Opstage（运维舞台） Cloud（云版）. Cloud（云版） should not require inbound access into customer environments.

---

## 2. Connectivity Goal

The goal of Cloud（云版） Agent（代理） connectivity is:

> Allow Agents running in customer-controlled environments to securely and reliably connect to Opstage（运维舞台） Cloud（云版） using outbound network connections, while keeping Capsule Services private by default.

This 支持:

- home servers;
- VPS hosts;
- private data centers;
- NAT networks;
- firewalled environments;
- customer-controlled infrastructure;
- future managed Agent（代理） Gateway.

---

## 3. Core Connectivity Principle

Cloud（云版） should use an outbound-first model:

```text
Customer Environment
└── Agent
    ↓ outbound HTTPS / WebSocket / streaming
Opstage Cloud
```

Cloud（云版） should not require:

```text
Opstage Cloud -> Customer Agent inbound connection
```

This is important because many customers cannot or should not expose internal service ports to the public internet.

---

## 4. Relationship with CE（社区版）

CE（社区版） v0.1 uses simple HTTP communication:

```text
Agent -> Backend heartbeat
Agent -> Backend service report
Agent -> Backend command polling
Agent -> Backend command result report
```

This model is already Cloud（云版）-friendly because the Agent（代理） initiates all communication.

CE（社区版） v0.1 should not implement:

- Agent（代理） Gateway;
- WebSocket command channel;
- gRPC streaming;
- multi-tenant Agent（代理） routing;
- Cloud（云版） connection diagnostics;
- Cloud（云版） rate limiting;
- Cloud（云版） regional routing.

CE（社区版） should keep its HTTP polling model simple while preserving compatibility with future Cloud（云版） connectivity.

---

## 5. Connectivity 架构

Future Cloud（云版） connectivity may use this architecture:

```text
Customer Environment
├── Capsule Service A
│   └── Embedded Agent
├── Capsule Service B
│   └── Sidecar Agent
└── External Agent
    ↓ outbound HTTPS / WebSocket

Opstage Cloud Edge
└── Agent Gateway
    ↓ internal routing

Cloud Backend
├── Agent Service
├── Command Service
├── Health Service
├── Audit Service
└── Workspace / Tenant Context
```

The Agent（代理） Gateway may be introduced later to handle Cloud（云版）-specific scale, routing, and connection management.

---

## 6. Connectivity Modes

Cloud（云版） may support multiple Agent（代理） connectivity modes over time.

### 6.1 HTTP polling mode

This is the CE（社区版）-compatible mode.

Agent（代理） periodically calls:

```text
POST /api/agents/{agentId}/heartbeat
POST /api/agents/{agentId}/services/report
GET  /api/agents/{agentId}/commands
POST /api/agents/{agentId}/commands/{commandId}/result
```

Pros:

- simple;
- easy to debug;
- works through most proxies;
- compatible with CE（社区版）;
- sufficient for early Cloud（云版） MVP.

Cons:

- higher command latency;
- less efficient for large Agent（代理） fleets;
- more repeated requests.

### 6.2 Long polling mode

Agent（代理） opens a request and Cloud（云版） holds it until a command is available or timeout occurs.

Pros:

- lower latency than fixed polling;
- still HTTP-friendly;
- works in many proxy environments.

Cons:

- more complex server resource management;
- still not ideal for high-scale real-time delivery.

### 6.3 WebSocket mode

Agent（代理） maintains a WebSocket connection to Cloud（云版）.

Pros:

- lower latency;
- bidirectional logical channel;
- better for command push and status streaming;
- useful for Agent（代理） Gateway.

Cons:

- may be blocked by some networks;
- requires connection management;
- more complex reconnect behavior;
- more complex scaling.

### 6.4 gRPC streaming mode

Agent（代理） uses gRPC streaming to Cloud（云版）.

Pros:

- strong typed protocol;
- streaming-friendly;
- good for advanced Agent（代理） Gateway design.

Cons:

- less friendly in some proxy environments;
- more operational complexity;
- not necessary for CE（社区版） v0.1.

### 6.5 Queue-backed delivery mode

Cloud（云版） uses internal queues to buffer command delivery and Agent（代理） events.

This is mostly a Cloud（云版）-internal capability.

Agents may still communicate using HTTP or WebSocket.

---

## 7. Recommended Evolution Path

Recommended connectivity evolution:

```text
Phase 1: CE-compatible HTTP polling
    ↓
Phase 2: Cloud HTTP polling with Agent Gateway routing
    ↓
Phase 3: Long polling or WebSocket for lower-latency command delivery
    ↓
Phase 4: Advanced streaming / queue-backed reliability for large fleets
```

Cloud（云版） should not jump directly to complex streaming before the core governance model is validated.

---

## 8. Agent（代理） Gateway

### 8.1 Definition

Agent（代理） Gateway is a Cloud（云版）-side component that terminates Agent（代理） connectivity and routes Agent（代理） traffic to internal Cloud（云版） services.

### 8.2 Responsibilities

Agent（代理） Gateway may handle:

- Agent（代理） token validation;
- tenant/workspace context resolution;
- request routing;
- connection lifecycle;
- WebSocket session management;
- rate limiting;
- abuse prevention;
- regional routing;
- command delivery optimization;
- Agent（代理） protocol version negotiation;
- connection telemetry;
- diagnostics.

### 8.3 Non-responsibilities

Agent（代理） Gateway should not own:

- business logic of Capsule Services;
- final Command execution;
- raw customer secrets;
- UI authentication;
- billing logic;
- audit retention logic.

### 8.4 CE（社区版） relationship

CE（社区版） v0.1 does not need Agent（代理） Gateway.

CE（社区版） Backend can directly expose Agent（代理） APIs.

---

## 9. Agent（代理） 认证 in Cloud（云版）

Agent（代理） authentication should be token-based.

Agent（代理） sends:

```http
Authorization: Bearer <agentToken>
```

Cloud（云版） must derive Agent（代理） context from the token:

```text
agentToken -> Agent -> Workspace -> Organization -> Tenant
```

Cloud（云版） must not trust tenant or workspace identity from arbitrary Agent（代理） payload fields.

Bad:

```json
{
  "tenantId": "ten_001",
  "workspaceId": "wks_001"
}
```

if accepted without token-derived validation.

Good:

```text
Authenticated Agent token determines the ownership boundary.
```

---

## 10. Registration Connectivity

Cloud（云版） Agent（代理） registration should also be outbound.

Registration flow:

```text
User creates Workspace-scoped registration token in Cloud UI
    ↓
Agent starts with registration token
    ↓
Agent calls Cloud registration endpoint
    ↓
Cloud validates token
    ↓
Cloud creates Agent under Workspace
    ↓
Cloud issues Agent token
    ↓
Agent stores Agent token locally
```

Registration tokens should be:

- workspace-scoped;
- one-time or short-lived;
- revocable;
- shown only once;
- stored as hashes.

---

## 11. Command Delivery in Cloud（云版）

Cloud（云版） command delivery should preserve the same Command model.

### 11.1 CE（社区版）-compatible command polling

Initial Cloud（云版） can use:

```text
Agent polls Cloud for Commands.
```

This is simple and compatible with CE（社区版）.

### 11.2 Push-like command delivery

Future Cloud（云版） may push command notifications over:

```text
WebSocket
SSE
gRPC stream
```

Even in push-like mode, Command and CommandResult should remain explicit records.

### 11.3 Reliability rule

Command transport may change, but Cloud（云版） should still track:

```text
Command created
Command delivered or dispatched
Command started
Command completed or failed
Command expired or cancelled
AuditEvent created
```

---

## 12. Network Environments

Cloud（云版） Agents should be designed for varied network environments.

### 12.1 NAT and private networks

Outbound-first connectivity 支持 Agents behind NAT.

No public inbound port should be required for the Agent（代理）.

### 12.2 Firewalls

Agents should work with standard outbound HTTPS:

```text
TCP 443
```

Where possible, Cloud（云版） should avoid requiring unusual ports.

### 12.3 Corporate proxies

Agent（代理） SDKs and external Agents should support proxy configuration.

Potential environment variables:

```text
HTTPS_PROXY
HTTP_PROXY
NO_PROXY
OPSTAGE_PROXY_URL
```

### 12.4 Intermittent networks

Agents should tolerate temporary Cloud（云版） connectivity loss.

Expected behavior:

- keep Capsule Service（胶囊服务） running;
- retry connection;
- resume heartbeat;
- re-report service metadata if needed;
- avoid duplicate command execution where practical.

---

## 13. Reconnect Behavior

Agent（代理） reconnect behavior should be predictable.

Recommended flow:

```text
Connection fails
    ↓
Agent logs warning
    ↓
Agent backs off and retries
    ↓
Agent reconnects
    ↓
Agent sends heartbeat
    ↓
Agent reports manifest if needed
    ↓
Agent resumes command polling or stream
```

Backoff strategy:

```text
initial delay: 1-5 seconds
max delay: 60-300 seconds
jitter: recommended
```

Exact values should be SDK-specific.

---

## 14. Offline and Stale Detection

Cloud（云版） should distinguish:

```text
Agent disconnected
Agent offline
Service stale
Service unhealthy
```

Recommended model:

- Agent（代理） is disconnected when active connection is lost;
- Agent（代理） is offline when heartbeat is stale beyond threshold;
- Capsule Service（胶囊服务） is stale when its managing Agent（代理） is offline or report is stale;
- HealthStatus should not be shown as fresh when Agent（代理） is stale.

This aligns with CE（社区版） 状态 Model.

---

## 15. Agent（代理） Version Compatibility

Cloud（云版） should track Agent（代理） version.

Agent（代理） heartbeat or registration should include:

```text
agent version
SDK version
runtime
protocol version
supported capabilities
```

Cloud（云版） may display warnings:

```text
Agent version is outdated.
Agent protocol is deprecated.
Feature requires newer Agent version.
```

CE（社区版） v0.1 may store version fields but does not need advanced compatibility enforcement.

---

## 16. Protocol Versioning

Cloud（云版） connectivity should support protocol evolution.

Recommended fields:

```text
protocolVersion
agentVersion
sdkVersion
capabilities
```

Rules:

- older Agents should continue working when possible;
- new optional fields should be additive;
- breaking protocol changes should be versioned;
- Cloud（云版） should provide clear error messages for unsupported protocol versions.

---

## 17. Rate Limiting

Cloud（云版） should protect itself from excessive Agent（代理） traffic.

Possible rate limits:

- heartbeat rate per Agent（代理）;
- registration attempts per token/IP;
- command polling frequency;
- failed authentication attempts;
- service report frequency;
- command result report volume.

Rate limiting is not needed in CE（社区版） v0.1 except basic defensive checks if easy.

---

## 18. Agent（代理） Diagnostics

Cloud（云版） should provide Agent（代理） connectivity diagnostics.

Possible diagnostic fields:

```text
Agent status
Connection status
Last connected at
Last disconnected at
Last heartbeat at
Last service report at
Last command poll at
Last command result at
Agent IP or region
Protocol version
SDK version
Recent errors
Token status
```

Possible UI sections:

```text
Connectivity
Heartbeat
Protocol
Recent Errors
Token State
```

CE（社区版） v0.1 may show only last heartbeat and Agent（代理） status.

---

## 19. Connection 状态 Values

Cloud（云版） may introduce connection-specific status values.

Possible values:

```text
CONNECTED
DISCONNECTED
RECONNECTING
AUTH_FAILED
RATE_LIMITED
UNKNOWN
```

These are different from AgentStatus.

AgentStatus may remain:

```text
ONLINE
OFFLINE
DISABLED
REVOKED
```

Do not confuse transport connection status with governance Agent（代理） status.

---

## 20. 安全 Considerations

Cloud（云版） Agent（代理） connectivity must handle security carefully.

Required principles:

- use HTTPS;
- validate Agent（代理） tokens;
- derive tenant context from token;
- reject revoked or disabled Agents;
- avoid logging raw tokens;
- avoid raw secrets in payloads;
- rate-limit suspicious traffic;
- audit important registration and command events;
- protect Agent（代理） Gateway from abuse.

Future Cloud（云版） may add:

- token rotation;
- scoped Agent（代理） tokens;
- mTLS for enterprise plans;
- IP allowlists;
- region restrictions;
- device attestation.

These are not CE（社区版） v0.1 requirements.

---

## 21. Data Boundary

Agent（代理） connectivity should respect the Cloud（云版） data boundary.

Agents may send:

- Agent（代理） metadata;
- Capsule Service（胶囊服务） manifest;
- health reports;
- config metadata;
- action metadata;
- command results;
- audit-relevant operation results.

Agents should not send raw secrets by default.

Use:

```text
secretRef
```

for sensitive references.

---

## 22. Failure Modes

### 22.1 Cloud（云版） unavailable

Agent（代理） should:

- keep Capsule Service（胶囊服务） running;
- retry later;
- avoid losing local business function;
- avoid crashing process by default.

### 22.2 Token revoked

Agent（代理） should:

- stop using revoked token;
- clear stored token if safe;
- attempt re-registration only if registration token is available;
- log clear error.

### 22.3 Network blocked

Agent（代理） should:

- show diagnostic error;
- support proxy config;
- retry with backoff.

### 22.4 Command result report failed

Agent（代理） should:

- retry carefully;
- avoid duplicate execution;
- preserve result locally if practical.

### 22.5 Gateway overload

Cloud（云版） should:

- rate-limit;
- return structured retry guidance;
- avoid dropping critical command results where possible.

---

## 23. Agent（代理） Connectivity Metrics

Cloud（云版） may collect connectivity metrics:

```text
active connections
heartbeat rate
command polling rate
command delivery latency
command result latency
Agent reconnect count
failed authentication count
rate-limited request count
```

These are Cloud（云版） operational metrics.

CE（社区版） v0.1 does not need to collect them.

---

## 24. CE（社区版） Reservations

CE（社区版） should preserve these Cloud（云版）-compatible choices:

```text
Agent outbound communication
Agent registration token
Agent token
heartbeat endpoint
service report endpoint
command polling endpoint
command result endpoint
agentMode
runtime
protocol-friendly JSON payloads
status and freshness calculation
```

CE（社区版） should not implement:

```text
Agent Gateway
WebSocket command channel
Cloud connection status
multi-tenant routing
Cloud diagnostics
Cloud rate limiting
Cloud regional routing
```

---

## 25. Anti-Patterns

Avoid these patterns.

### 25.1 Requiring inbound customer network access

Cloud（云版） should not require customer Agents or Capsule Services to expose public inbound ports.

### 25.2 Trusting tenant IDs from Agent（代理） payload

Tenant and workspace context must come from authenticated Agent（代理） identity.

### 25.3 Replacing Command records with transient push messages

Even if WebSocket is used, Commands should remain durable records.

### 25.4 Making WebSocket mandatory too early

HTTP polling should remain available for compatibility and restricted networks.

### 25.5 Pulling Agent（代理） Gateway into CE（社区版） v0.1

Agent（代理） Gateway is Cloud（云版） infrastructure and should not burden CE（社区版）.

### 25.6 Sending raw secrets through connectivity payloads

Use `secretRef` instead.

---

## 26. Acceptance Criteria

Cloud（云版） Agent（代理） connectivity planning is acceptable when:

- outbound-first connectivity is the default;
- CE（社区版） HTTP polling model remains Cloud（云版）-compatible;
- Agent（代理） Gateway responsibilities are clear;
- Cloud（云版） tenant context is derived from Agent（代理） token;
- command model remains stable across transports;
- network restrictions and proxy needs are considered;
- reconnect behavior is defined;
- diagnostics are planned;
- CE（社区版） v0.1 is not required to implement Cloud（云版） connectivity infrastructure.

---

## 27. Summary

Cloud（云版） Agent（代理） connectivity should allow customer-side Agents to connect securely and reliably to a hosted Opstage（运维舞台） control plane without exposing customer environments.

The most important connectivity rule is:

> Agent（代理） connectivity should be outbound-first, token-scoped, command-record-based, and compatible with CE（社区版）'s simple polling model.
