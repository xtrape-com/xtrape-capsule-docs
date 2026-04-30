# xtrape-capsule Design Principles

- Status: Conceptual Guidance
- Edition: Shared
- Priority: High
- Audience: architects, developers, AI coding agents, reviewers

This document defines the design principles of the `xtrape-capsule` domain.

These principles should guide all CE, EE, and Cloud designs. CE v0.1 should follow them strictly while keeping implementation lightweight.

---

## 1. Principle Summary

`xtrape-capsule` follows these core principles:

1. Capsule Services must remain independently runnable.
2. Opstage is a governance plane, not a business runtime dependency.
3. Services enter governance through registered and authorized Agents.
4. Agent communication should be outbound-first.
5. CE must stay lightweight and self-hosted first.
6. Specifications should be stable across languages and editions.
7. Implementation may be partial, but it must not violate long-term contracts.
8. Sensitive data should be referenced, not casually stored.
9. Actions must be explicit, predefined, and auditable.
10. Status freshness must be visible.
11. UI, backend, and agent responsibilities must stay separated.
12. CE should reserve extension points for EE and Cloud without implementing their full complexity.

---

## 2. Independent Capsule Runtime

A Capsule Service must be able to start and perform its core business work without Opstage being online.

Correct model:

```text
Capsule Service starts
    ↓
Capsule Service performs core work
    ↓
Agent connects to Opstage if available
    ↓
Opstage provides governance features
```

Incorrect model:

```text
Opstage is unavailable
    ↓
Capsule Service cannot start
```

### Rationale

Opstage provides governance, not mandatory runtime existence.

If every Capsule Service depends on Opstage for startup, Opstage becomes a single point of failure for all services.

### CE v0.1 Requirement

The demo Capsule Service must be able to start even if Opstage Backend is unavailable.

The embedded Agent should retry registration or heartbeat in the background without preventing the service from running.

---

## 3. Governance Plane, Not Business Runtime

Opstage should observe, configure, command, audit, and govern Capsule Services.

Opstage should not become the place where every Capsule Service's business logic is implemented.

Opstage responsibilities:

- service listing;
- Agent registration;
- status display;
- health visibility;
- command creation;
- action result tracking;
- configuration metadata visibility;
- audit logging;
- future observability and enterprise governance.

Capsule Service responsibilities:

- business logic;
- external platform integration;
- worker execution;
- account/session handling;
- local runtime behavior;
- execution of predefined actions;
- reporting status back through Agent.

### Anti-pattern

Do not implement service-specific business operations directly inside Opstage Backend.

If an operation belongs to a Capsule Service, Opstage should issue a command or action request and let the Capsule Service execute it through its Agent.

---

## 4. Agent-Based Registration

Opstage must not directly assume access to arbitrary services.

A Capsule Service enters governance through a registered and authorized Agent.

The core model is:

```text
Capsule Service
    ↓
Agent
    ↓
Opstage Backend
    ↓
Opstage UI
```

### Registration Rules

1. An Agent uses a registration token for first registration.
2. Opstage validates the registration token.
3. Opstage issues an Agent token.
4. The Agent uses the Agent token for ongoing communication.
5. Opstage stores only token hashes.
6. Tokens must be revocable.

### CE v0.1 Requirement

CE v0.1 must implement:

- registration token;
- Agent token;
- Agent heartbeat;
- Agent status;
- Capsule Service report;
- command polling;
- command result reporting.

---

## 5. Outbound-First Agent Communication

Agents should actively connect to Opstage Backend.

Opstage should not require direct inbound access to Agents or Capsule Services in CE v0.1.

Preferred CE flow:

```text
Agent -> Backend: register
Agent -> Backend: heartbeat
Agent -> Backend: report service status
Agent -> Backend: fetch pending commands
Agent -> Backend: report command result
```

### Rationale

Outbound-first communication works better for:

- local development;
- self-hosted deployments;
- NAT environments;
- customer-side servers;
- future Cloud SaaS model;
- fewer exposed inbound ports.

### Future Extension

Future versions may support:

- WebSocket channels;
- gRPC streaming;
- message queues;
- long-running log streams;
- interactive operation sessions.

CE v0.1 should start with simple HTTP and polling.

---

## 6. Lightweight CE First

CE is the current implementation target.

CE v0.1 should be lightweight, open-source, and self-hosted.

Preferred CE v0.1 choices:

- SQLite by default;
- single-node deployment;
- single-image or simple Docker deployment;
- simple local admin authentication;
- Node.js embedded Agent SDK;
- HTTP heartbeat;
- command polling;
- basic audit log;
- basic health visibility;
- predefined actions.

Avoid in CE v0.1:

- Kubernetes requirement;
- service mesh;
- distributed queue;
- enterprise RBAC;
- SSO;
- multi-tenant billing;
- full observability stack;
- arbitrary remote shell execution;
- mandatory MySQL/PostgreSQL;
- Java/Spring-only assumptions.

### Rationale

CE should prove the core model with the lowest possible deployment and adoption cost.

---

## 7. Stable Cross-Language Specifications

`xtrape-capsule` must not be tied to one language or framework.

Specifications should work for:

- Node.js;
- Java;
- Python;
- Go;
- shell workers;
- browser automation workers;
- future runtimes.

Shared specifications include:

- Capsule Manifest Spec;
- Capsule Management Contract;
- Agent Registration Spec;
- Health Spec;
- Action Spec;
- Config Spec;
- Command Spec;
- Audit Event Spec;
- Status Model Spec.

### CE v0.1 Rule

CE v0.1 may implement only a subset of these specifications, but it should not introduce names, fields, or behaviors that contradict the long-term shared specs.

---

## 8. Partial Implementation Without Contract Violation

A specification can be larger than the CE v0.1 implementation.

This is acceptable if CE clearly states what subset it implements.

Example:

```text
Spec supports: embedded, sidecar, external Agent modes
CE v0.1 implements: embedded only
```

This is acceptable.

Bad example:

```text
Spec defines Agent mode as embedded / sidecar / external
CE stores mode as isNodeOnly = true
```

This blocks future evolution and violates the long-term model.

---

## 9. Secret Reference First

Sensitive data should be represented by references when possible.

Examples:

```text
agent-local://agent-id/secrets/chatgpt/account-001
vault://secret/path
opstage-secret://workspace/key
```

CE v0.1 does not need a full secret store, but it should avoid spreading raw secrets into normal fields.

### Rules

- Do not store raw Agent tokens.
- Store only token hashes.
- Do not show sensitive config values in the UI.
- Prefer `secretRef` fields over raw secret values.
- Design future compatibility with external secret stores.

---

## 10. Explicit and Auditable Actions

Actions must be explicit and predefined.

Good examples:

```text
runHealthCheck
reloadConfig
refreshSession
clearExpiredSessions
rotateProxy
```

Bad examples:

```text
runShell
exec
bash
customCommand
```

### CE v0.1 Rule

CE v0.1 should not support arbitrary shell command execution from the UI.

Every action execution should create:

- a Command;
- a CommandResult;
- an AuditEvent.

---

## 11. Status Freshness Must Be Visible

Opstage must distinguish between:

- last reported status;
- effective current status;
- last reported time;
- freshness of the report.

Example:

```json
{
  "reportedStatus": "ONLINE",
  "effectiveStatus": "STALE",
  "lastReportedAt": "2026-04-30T10:21:00Z",
  "reason": "agent offline"
}
```

### Rationale

If an Agent goes offline, Opstage should not keep showing the Capsule Service as confidently online just because the last report was healthy.

### CE v0.1 Requirement

CE v0.1 should calculate offline or stale status based on heartbeat timeout.

---

## 12. Separate UI, Backend, and Agent Responsibilities

The system should be conceptually separated into:

```text
Opstage UI
Opstage Backend
Opstage Agent / Agent SDK
Capsule Service
```

Even if CE v0.1 is packaged as a single deployable application, the code and responsibilities should stay separated.

### UI Responsibilities

- display dashboard;
- list Agents;
- list Capsule Services;
- show service details;
- show health and status;
- trigger predefined actions;
- show command results;
- show audit logs.

### Backend Responsibilities

- authenticate users;
- manage Agent registration;
- store Agent state;
- store Capsule Service state;
- create commands;
- receive command results;
- store audit events;
- calculate effective status;
- serve UI API.

### Agent Responsibilities

- register;
- heartbeat;
- report manifest;
- report health;
- fetch commands;
- execute predefined actions;
- report command results.

### Capsule Service Responsibilities

- business function;
- action handlers;
- health provider;
- config metadata provider;
- manifest provider.

---

## 13. CE Extension Points for EE and Cloud

CE should not implement heavy EE or Cloud capabilities in v0.1, but it should preserve extension points.

Important extension points:

| Area | CE v0.1 | Future EE / Cloud |
|---|---|---|
| Database | SQLite | MySQL, PostgreSQL, HA database |
| Workspace | default only | multi-workspace, organization, tenant |
| Auth | local admin | RBAC, SSO, OIDC, LDAP |
| Agent | Node.js embedded | sidecar, external, Java, Python, Docker, Kubernetes |
| Commands | polling | WebSocket, gRPC, queue-based delivery |
| Logs | basic or none | centralized logs, search, retention |
| Metrics | health only | time-series metrics, dashboards |
| Secrets | secretRef-ready | vault integration, managed secret store |
| Deployment | single-node | cluster, HA, cloud-hosted |
| Billing | none | Cloud subscription, usage billing |

---

## 14. Documentation as Development Contract

Documentation is part of the development contract.

Before implementing a feature, check:

- concept documents in `01-capsule/`;
- shared specifications in `02-specs/`;
- CE scope in `03-editions/ce/`;
- Opstage documents in `04-opstage/`;
- Agent documents in `05-agents/`.

If a feature is not described clearly, update the documentation before or together with the implementation.

AI coding agents should treat CE implementation documents as the current source of truth and EE/Cloud documents as future planning references.

---

## 15. Review Checklist

Use this checklist when reviewing a design or implementation.

### 15.1 Independence

- Can the Capsule Service run without Opstage?
- Does the Agent fail gracefully if Backend is unavailable?

### 15.2 Agent Governance

- Does the service enter governance through Agent registration?
- Are Agent tokens handled securely?
- Is every service report associated with an Agent?

### 15.3 Lightweight CE

- Does the implementation avoid unnecessary enterprise features?
- Can it run with SQLite?
- Can it run in a simple local or Docker setup?

### 15.4 Specification Alignment

- Does it use shared names and statuses?
- Does it avoid blocking sidecar or external Agent support?
- Does it avoid Node.js-only assumptions in shared models?

### 15.5 Security

- Are raw tokens avoided in storage?
- Are sensitive values hidden or represented by references?
- Are actions predefined?
- Are operations auditable?

### 15.6 Status Correctness

- Is stale status handled?
- Is heartbeat timeout handled?
- Is last reported status separated from effective status?

### 15.7 Separation of Responsibilities

- Is business logic kept inside Capsule Services?
- Is Opstage kept as governance plane?
- Are UI, Backend, and Agent concerns separated?

---

## 16. Anti-Patterns

Avoid these anti-patterns.

### 16.1 Building a full microservice platform in CE v0.1

CE v0.1 should not become a Spring Cloud, Kubernetes, or service mesh platform.

### 16.2 Making Opstage mandatory for service startup

Opstage should not be required for Capsule Service startup.

### 16.3 Adding arbitrary command execution too early

Arbitrary shell execution creates serious security risk. Use predefined actions first.

### 16.4 Storing secrets directly

Do not store raw tokens, passwords, cookies, or credentials in ordinary fields.

### 16.5 Mixing EE/Cloud requirements into CE prototype

Do not implement multi-tenant billing, SSO, cluster deployment, or full observability stack in CE v0.1.

### 16.6 Over-normalizing the manifest too early

Use JSON for flexible metadata in CE v0.1. Normalize later when the model stabilizes.

---

## 17. Summary

The most important design idea of `xtrape-capsule` is:

> Keep services lightweight and independent, but make them governable through Agents and Opstage.

CE v0.1 should be simple enough to run easily and strong enough to prove the model.

Future EE and Cloud editions should grow from the same principles without forcing CE to become heavy too early.
