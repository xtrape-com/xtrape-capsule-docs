---
status: proposed
audience: founders
stability: evolving
last_reviewed: 2026-05-05
edition: cloud
phase: future
---

# Cloud Agent Connectivity

- Status: Planning
- Edition: Cloud
- Priority: Future
- Audience: architects, cloud engineers, backend developers, agent SDK developers, security reviewers, AI coding agents

This document defines the planned Agent connectivity model for **Opstage Cloud**.

Opstage Cloud is the future hosted SaaS edition of the `xtrape-capsule` product family. Cloud Agent connectivity is a future capability, not a CE v0.1 implementation requirement.

---

## 1. Purpose

The purpose of this document is to define:

- how customer-side Agents should connect to Opstage Cloud;
- why outbound-first connectivity is the default model;
- how CE heartbeat and command polling can evolve into Cloud connectivity;
- what an Agent Gateway may do;
- how network restrictions, proxies, NAT, and firewalls should be handled;
- how command delivery may evolve;
- what diagnostics Cloud should provide;
- which connectivity features must not be pulled into CE v0.1.

The key rule is:

> Agents connect outbound to Opstage Cloud. Cloud should not require inbound access into customer environments.

---

## 2. Connectivity Goal

The goal of Cloud Agent connectivity is:

> Allow Agents running in customer-controlled environments to securely and reliably connect to Opstage Cloud using outbound network connections, while keeping Capsule Services private by default.

This supports:

- home servers;
- VPS hosts;
- private data centers;
- NAT networks;
- firewalled environments;
- customer-controlled infrastructure;
- future managed Agent Gateway.

---

## 3. Core Connectivity Principle

Cloud should use an outbound-first model:

```text
Customer Environment
└── Agent
    ↓ outbound HTTPS / WebSocket / streaming
Opstage Cloud
```

Cloud should not require:

```text
Opstage Cloud -> Customer Agent inbound connection
```

This is important because many customers cannot or should not expose internal service ports to the public internet.

---

## 4. Relationship with CE

CE v0.1 uses simple HTTP communication:

```text
Agent -> Backend heartbeat
Agent -> Backend service report
Agent -> Backend command polling
Agent -> Backend command result report
```

This model is already Cloud-friendly because the Agent initiates all communication.

CE v0.1 should not implement:

- Agent Gateway;
- WebSocket command channel;
- gRPC streaming;
- multi-tenant Agent routing;
- Cloud connection diagnostics;
- Cloud rate limiting;
- Cloud regional routing.

CE should keep its HTTP polling model simple while preserving compatibility with future Cloud connectivity.

---

## 5. Connectivity Architecture

Future Cloud connectivity may use this architecture:

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

The Agent Gateway may be introduced later to handle Cloud-specific scale, routing, and connection management.

---

## 6. Connectivity Modes

Cloud may support multiple Agent connectivity modes over time.

### 6.1 HTTP polling mode

This is the CE-compatible mode.

Agent periodically calls:

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
- compatible with CE;
- sufficient for early Cloud MVP.

Cons:

- higher command latency;
- less efficient for large Agent fleets;
- more repeated requests.

### 6.2 Long polling mode

Agent opens a request and Cloud holds it until a command is available or timeout occurs.

Pros:

- lower latency than fixed polling;
- still HTTP-friendly;
- works in many proxy environments.

Cons:

- more complex server resource management;
- still not ideal for high-scale real-time delivery.

### 6.3 WebSocket mode

Agent maintains a WebSocket connection to Cloud.

Pros:

- lower latency;
- bidirectional logical channel;
- better for command push and status streaming;
- useful for Agent Gateway.

Cons:

- may be blocked by some networks;
- requires connection management;
- more complex reconnect behavior;
- more complex scaling.

### 6.4 gRPC streaming mode

Agent uses gRPC streaming to Cloud.

Pros:

- strong typed protocol;
- streaming-friendly;
- good for advanced Agent Gateway design.

Cons:

- less friendly in some proxy environments;
- more operational complexity;
- not necessary for CE v0.1.

### 6.5 Queue-backed delivery mode

Cloud uses internal queues to buffer command delivery and Agent events.

This is mostly a Cloud-internal capability.

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

Cloud should not jump directly to complex streaming before the core governance model is validated.

---

## 8. Agent Gateway

### 8.1 Definition

Agent Gateway is a Cloud-side component that terminates Agent connectivity and routes Agent traffic to internal Cloud services.

### 8.2 Responsibilities

Agent Gateway may handle:

- Agent token validation;
- tenant/workspace context resolution;
- request routing;
- connection lifecycle;
- WebSocket session management;
- rate limiting;
- abuse prevention;
- regional routing;
- command delivery optimization;
- Agent protocol version negotiation;
- connection telemetry;
- diagnostics.

### 8.3 Non-responsibilities

Agent Gateway should not own:

- business logic of Capsule Services;
- final Command execution;
- raw customer secrets;
- UI authentication;
- billing logic;
- audit retention logic.

### 8.4 CE relationship

CE v0.1 does not need Agent Gateway.

CE Backend can directly expose Agent APIs.

---

## 9. Agent Authentication in Cloud

Agent authentication should be token-based.

Agent sends:

```http
Authorization: Bearer <agentToken>
```

Cloud must derive Agent context from the token:

```text
agentToken -> Agent -> Workspace -> Organization -> Tenant
```

Cloud must not trust tenant or workspace identity from arbitrary Agent payload fields.

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

Cloud Agent registration should also be outbound.

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

## 11. Command Delivery in Cloud

Cloud command delivery should preserve the same Command model.

### 11.1 CE-compatible command polling

Initial Cloud can use:

```text
Agent polls Cloud for Commands.
```

This is simple and compatible with CE.

### 11.2 Push-like command delivery

Future Cloud may push command notifications over:

```text
WebSocket
SSE
gRPC stream
```

Even in push-like mode, Command and CommandResult should remain explicit records.

### 11.3 Reliability rule

Command transport may change, but Cloud should still track:

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

Cloud Agents should be designed for varied network environments.

### 12.1 NAT and private networks

Outbound-first connectivity supports Agents behind NAT.

No public inbound port should be required for the Agent.

### 12.2 Firewalls

Agents should work with standard outbound HTTPS:

```text
TCP 443
```

Where possible, Cloud should avoid requiring unusual ports.

### 12.3 Corporate proxies

Agent SDKs and external Agents should support proxy configuration.

Potential environment variables:

```text
HTTPS_PROXY
HTTP_PROXY
NO_PROXY
OPSTAGE_PROXY_URL
```

### 12.4 Intermittent networks

Agents should tolerate temporary Cloud connectivity loss.

Expected behavior:

- keep Capsule Service running;
- retry connection;
- resume heartbeat;
- re-report service metadata if needed;
- avoid duplicate command execution where practical.

---

## 13. Reconnect Behavior

Agent reconnect behavior should be predictable.

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

Cloud should distinguish:

```text
Agent disconnected
Agent offline
Service stale
Service unhealthy
```

Recommended model:

- Agent is disconnected when active connection is lost;
- Agent is offline when heartbeat is stale beyond threshold;
- Capsule Service is stale when its managing Agent is offline or report is stale;
- HealthStatus should not be shown as fresh when Agent is stale.

This aligns with CE Status Model.

---

## 15. Agent Version Compatibility

Cloud should track Agent version.

Agent heartbeat or registration should include:

```text
agent version
SDK version
runtime
protocol version
supported capabilities
```

Cloud may display warnings:

```text
Agent version is outdated.
Agent protocol is deprecated.
Feature requires newer Agent version.
```

CE v0.1 may store version fields but does not need advanced compatibility enforcement.

---

## 16. Protocol Versioning

Cloud connectivity should support protocol evolution.

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
- Cloud should provide clear error messages for unsupported protocol versions.

---

## 17. Rate Limiting

Cloud should protect itself from excessive Agent traffic.

Possible rate limits:

- heartbeat rate per Agent;
- registration attempts per token/IP;
- command polling frequency;
- failed authentication attempts;
- service report frequency;
- command result report volume.

Rate limiting is not needed in CE v0.1 except basic defensive checks if easy.

---

## 18. Agent Diagnostics

Cloud should provide Agent connectivity diagnostics.

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

CE v0.1 may show only last heartbeat and Agent status.

---

## 19. Connection Status Values

Cloud may introduce connection-specific status values.

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

Do not confuse transport connection status with governance Agent status.

---

## 20. Security Considerations

Cloud Agent connectivity must handle security carefully.

Required principles:

- use HTTPS;
- validate Agent tokens;
- derive tenant context from token;
- reject revoked or disabled Agents;
- avoid logging raw tokens;
- avoid raw secrets in payloads;
- rate-limit suspicious traffic;
- audit important registration and command events;
- protect Agent Gateway from abuse.

Future Cloud may add:

- token rotation;
- scoped Agent tokens;
- mTLS for enterprise plans;
- IP allowlists;
- region restrictions;
- device attestation.

These are not CE v0.1 requirements.

---

## 21. Data Boundary

Agent connectivity should respect the Cloud data boundary.

Agents may send:

- Agent metadata;
- Capsule Service manifest;
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

### 22.1 Cloud unavailable

Agent should:

- keep Capsule Service running;
- retry later;
- avoid losing local business function;
- avoid crashing process by default.

### 22.2 Token revoked

Agent should:

- stop using revoked token;
- clear stored token if safe;
- attempt re-registration only if registration token is available;
- log clear error.

### 22.3 Network blocked

Agent should:

- show diagnostic error;
- support proxy config;
- retry with backoff.

### 22.4 Command result report failed

Agent should:

- retry carefully;
- avoid duplicate execution;
- preserve result locally if practical.

### 22.5 Gateway overload

Cloud should:

- rate-limit;
- return structured retry guidance;
- avoid dropping critical command results where possible.

---

## 23. Agent Connectivity Metrics

Cloud may collect connectivity metrics:

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

These are Cloud operational metrics.

CE v0.1 does not need to collect them.

---

## 24. CE Reservations

CE should preserve these Cloud-compatible choices:

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

CE should not implement:

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

Cloud should not require customer Agents or Capsule Services to expose public inbound ports.

### 25.2 Trusting tenant IDs from Agent payload

Tenant and workspace context must come from authenticated Agent identity.

### 25.3 Replacing Command records with transient push messages

Even if WebSocket is used, Commands should remain durable records.

### 25.4 Making WebSocket mandatory too early

HTTP polling should remain available for compatibility and restricted networks.

### 25.5 Pulling Agent Gateway into CE v0.1

Agent Gateway is Cloud infrastructure and should not burden CE.

### 25.6 Sending raw secrets through connectivity payloads

Use `secretRef` instead.

---

## 26. Acceptance Criteria

Cloud Agent connectivity planning is acceptable when:

- outbound-first connectivity is the default;
- CE HTTP polling model remains Cloud-compatible;
- Agent Gateway responsibilities are clear;
- Cloud tenant context is derived from Agent token;
- command model remains stable across transports;
- network restrictions and proxy needs are considered;
- reconnect behavior is defined;
- diagnostics are planned;
- CE v0.1 is not required to implement Cloud connectivity infrastructure.

---

## 27. Summary

Cloud Agent connectivity should allow customer-side Agents to connect securely and reliably to a hosted Opstage control plane without exposing customer environments.

The most important connectivity rule is:

> Agent connectivity should be outbound-first, token-scoped, command-record-based, and compatible with CE's simple polling model.
