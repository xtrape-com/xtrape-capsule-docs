---
status: proposed
audience: architects
stability: evolving
last_reviewed: 2026-05-05
---

# Capsule Service Concept

- Status: Conceptual Guidance
- Edition: Shared
- Priority: High
- Audience: architects, developers, AI coding agents

This document defines the concept of **Capsule Service**, the core service unit in the `xtrape-capsule` domain.

A Capsule Service is the main object that Opstage observes, configures, audits, and operates through registered Agents.

---

## 1. Definition

A **Capsule Service** is a lightweight, self-contained, independently runnable, agent-governed service unit that
provides a clear capability, connector, worker process, automation function, account resource, session resource, or
runtime adapter.

A Capsule Service is not defined by a specific language, framework, protocol, or deployment model. It is defined by its governance shape:

- it can identify itself;
- it can run independently;
- it can expose or report health;
- it can expose or report manageable resources;
- it can expose or report configuration metadata;
- it can expose or execute predefined actions;
- it can emit auditable events;
- it can be connected to Opstage through an Agent.

The shortest definition is:

> A Capsule Service is a lightweight service unit that remains independently runnable but becomes governable after being connected to Opstage through an authorized Agent.

---

## 2. Why Capsule Service Exists

AI-era systems tend to generate many small capability services:

- a integration adapter for a third-party web platform;
- a Playwright-based browser automation worker;
- an account pool service;
- an OTP reader;
- a proxy checker;
- a session refresher;
- a connector to a messaging platform;
- a small AI agent runtime;
- a task worker for one specific job.

These services are usually too small to justify a full microservice framework, but they are too important to remain unmanaged.

Capsule Service is introduced to solve this problem:

> Keep small services lightweight, but make them visible, operable, auditable, and governable.

---

## 3. Core Characteristics

A Capsule Service should have the following characteristics.

### 3.1 Lightweight

A Capsule Service should not require a heavy framework just to become manageable.

It may be implemented as:

- a Node.js service;
- a Java service;
- a Python worker;
- a Go binary;
- a browser automation worker;
- a containerized process;
- a local script wrapped by an Agent.

### 3.2 Self-contained

A Capsule Service should have a clear responsibility and boundary.

It should not be an unbounded collection of unrelated functions.

Good examples:

- `integration-worker`;
- `account-pool`;
- `browser-session-worker`;
- `otp-mail-reader`;
- `proxy-health-checker`.

Bad examples:

- `misc-tools`;
- `all-platform-adapters`;
- `everything-worker`;
- `random-automation-service`.

### 3.3 Independently runnable

A Capsule Service must be able to start and perform its core business function without Opstage being available.

Opstage provides runtime governance, not mandatory runtime existence.

This principle prevents the following failure mode:

```text
Opstage is down
    ↓
All Capsule Services cannot start
```

A correct model is:

```text
Opstage is down
    ↓
Capsule Services continue core work
    ↓
Governance features are temporarily unavailable
```

### 3.4 Agent-governed

A Capsule Service enters Opstage governance through an Agent.

The Agent may be:

- embedded in the service process;
- deployed as a sidecar;
- deployed externally and configured to manage the service.

CE v0.1 implements only the Node.js embedded Agent model.

### 3.5 Observable

A Capsule Service should provide or report enough state for Opstage to answer:

- Is the service online?
- Is the service healthy?
- When was it last seen?
- Which Agent reported it?
- Which version is running?
- Which runtime is used?
- What is the last known status?

### 3.6 Configurable

A Capsule Service should expose configuration metadata, not just raw configuration values.

A configuration item should describe:

- key;
- label;
- type;
- current value if safe to expose;
- default value;
- editability;
- validation constraints;
- sensitivity.

CE v0.1 may implement configuration visibility only. Full configuration publishing can be added later.

### 3.7 Operable

A Capsule Service should expose predefined actions that can be executed through Opstage.

Examples:

- `refreshSession`;
- `clearExpiredSessions`;
- `reloadConfig`;
- `runHealthCheck`;
- `disableAccount`;
- `rotateProxy`.

Actions must be explicit and predefined. CE v0.1 should not support arbitrary shell command execution from the UI.

### 3.8 Auditable

Actions and important state changes should be auditable.

At minimum, Opstage should be able to record:

- who initiated an action;
- which Agent executed it;
- which Capsule Service was targeted;
- what action was executed;
- whether it succeeded or failed;
- when it happened.

---

## 4. What Is Not a Capsule Service

Not every process or service should be treated as a Capsule Service.

The following are not good Capsule Service candidates:

### 4.1 Pure infrastructure dependency

Examples:

- MySQL;
- Redis;
- Nginx;
- MinIO;
- Elasticsearch.

These are infrastructure dependencies. They may be monitored by Opstage in the future, but they are not Capsule Services by default.

### 4.2 Large business domain service without lightweight governance boundary

A large payment or order service may be a traditional microservice. It becomes a Capsule Service only if it
intentionally exposes Capsule governance metadata, health, actions, or management resources.

### 4.3 Random script without identity

A script that has no name, no manifest, no owner, no status, and no management boundary should not be treated as a Capsule Service.

It may be wrapped by an external Agent later, but it must first be assigned a clear Capsule identity.

### 4.4 UI-only application

A static UI or frontend-only app is usually not a Capsule Service unless it has runtime governance needs and is connected through an Agent or a hosting runtime.

---

## 5. Typical Capsule Service Types

Capsule Services can be grouped by function.

### 5.1 Integration service

An integration service wraps the capability of an external platform or website.

Examples:

- `integration-worker`;
- `integration-gemini`;
- `integration-gmail`;
- `integration-telegram`.

Typical resources:

- providers;
- accounts;
- sessions;
- quotas;
- capability routes;
- usage records.

### 5.2 Account Service

An account service manages platform accounts.

Typical resources:

- account;
- credential reference;
- login state;
- risk state;
- quota state;
- ownership;
- session binding.

### 5.3 Session Service

A session service manages login sessions, cookies, browser contexts, or OAuth tokens.

Typical resources:

- session;
- cookie store;
- browser context;
- token reference;
- expiration state;
- refresh action.

### 5.4 Worker Service

A worker service executes background jobs.

Examples:

- browser automation worker;
- OTP reader worker;
- crawler worker;
- media processing worker;
- AI generation worker.

Typical resources:

- job;
- queue state;
- worker status;
- current task;
- error records.

### 5.5 Connector Service

A connector service connects Xtrape or Opstage to an external platform.

Examples:

- Gmail connector;
- Telegram connector;
- Discord connector;
- GitHub connector;
- payment provider connector.

### 5.6 Agent Runtime Service

An agent runtime service hosts or executes AI agents.

Typical resources:

- agent definition;
- tool binding;
- execution session;
- prompt profile;
- task state;
- run history.

---

## 6. Capsule Identity

Every Capsule Service must have a stable identity.

Recommended identity fields:

```json
{
  "code": "integration-worker",
  "name": "Example integration service",
  "version": "0.1.0",
  "runtime": "nodejs",
  "edition": "ce",
  "description": "A Capsule Service that wraps ChatGPT web capabilities."
}
```

### 6.1 Code

`code` is the stable technical identifier.

Rules:

- lowercase;
- kebab-case;
- globally unique within one Opstage workspace;
- should not change after registration unless the service is intentionally renamed.

Examples:

```text
integration-worker
account-pool
browser-session-worker
otp-mail-reader
proxy-health-checker
```

### 6.2 Name

`name` is the human-readable display name.

It may change without breaking identity.

### 6.3 Version

`version` describes the running service version.

CE v0.1 may treat it as a simple string.

### 6.4 Runtime

`runtime` describes the implementation runtime.

Examples:

```text
nodejs
java
python
go
shell
other
```

---

## 7. Capsule Manifest

A Capsule Service should be able to describe itself with a manifest.

The manifest is the primary metadata object that allows Opstage to understand the service.

Minimum CE v0.1 manifest:

```json
{
  "kind": "CapsuleService",
  "code": "demo-capsule-service",
  "name": "Demo Capsule Service",
  "version": "0.1.0",
  "runtime": "nodejs",
  "agentMode": "embedded",
  "capabilities": ["demo.echo"],
  "resources": [],
  "actions": ["echo", "runHealthCheck"]
}
```

Long-term manifest fields may include:

- owner;
- environment;
- workspace;
- resources;
- config schema;
- action schema;
- health dependencies;
- required secrets;
- deployment metadata;
- documentation links.

Detailed manifest rules should be defined in:

```text
02-specs/01-capsule-manifest-spec.md
```

---

## 8. Capsule Lifecycle

A Capsule Service has both a runtime lifecycle and a governance lifecycle.

### 8.1 Runtime lifecycle

Runtime lifecycle describes whether the service process itself is running.

Typical states:

```text
STARTING
RUNNING
DEGRADED
STOPPING
STOPPED
FAILED
UNKNOWN
```

### 8.2 Governance lifecycle

Governance lifecycle describes whether Opstage can manage the service through an Agent.

Typical states:

```text
DISCOVERED
REGISTERED
ONLINE
UNHEALTHY
OFFLINE
STALE
DISABLED
REMOVED
```

### 8.3 Last known state

If the Agent is offline, Opstage must not pretend the service is still live.

Instead, Opstage should distinguish:

- last reported status;
- effective current status;
- last reported time;
- reason for stale status.

Example:

```json
{
  "reportedStatus": "ONLINE",
  "effectiveStatus": "STALE",
  "lastReportedAt": "2026-04-30T10:21:00Z",
  "reason": "agent offline"
}
```

---

## 9. Relationship with Agent

A Capsule Service is not directly managed by Opstage Backend unless an authorized Agent is involved.

The basic model is:

```text
Capsule Service
    ↓
Agent
    ↓
Opstage Backend
    ↓
Opstage UI
```

Agent responsibilities include:

- registration;
- heartbeat;
- manifest reporting;
- health reporting;
- command polling or command receiving;
- action execution;
- command result reporting;
- event reporting.

CE v0.1 supports:

```text
Node.js Capsule Service
    ↓ embedded Node.js Agent SDK
Opstage Backend
```

Future editions may support:

```text
Capsule Service + Sidecar Agent
External Agent + managed target configuration
```

---

## 10. Relationship with Opstage

Opstage is the governance plane. A Capsule Service should not embed Opstage business logic.

Opstage is responsible for:

- listing services;
- showing status;
- storing last reported metadata;
- issuing commands;
- recording audit logs;
- managing registration and tokens;
- presenting UI.

Capsule Service is responsible for:

- its own business logic;
- its own local runtime behavior;
- exposing or reporting manageable metadata;
- executing only predefined actions;
- reporting action results.

This separation prevents Opstage from becoming a monolithic business system.

---

## 11. Minimum CE v0.1 Requirements

For CE v0.1, a Capsule Service integrated through the Node.js embedded Agent SDK should provide at least:

- `code`;
- `name`;
- `version`;
- `runtime`;
- `agentMode`;
- health provider;
- manifest provider;
- action definitions;
- optional config metadata;
- heartbeat through Agent;
- command result reporting through Agent.

The demo Capsule Service must implement:

- one manifest;
- one health report;
- one example action;
- one optional config item;
- Agent registration using registration token;
- heartbeat;
- command polling;
- command result reporting.

---

## 12. Extension Points

CE v0.1 should reserve extension points for future capabilities.

### 12.1 Agent modes

The data model should support:

```text
embedded
sidecar
external
```

CE v0.1 only implements `embedded`.

### 12.2 Runtime types

The data model should support multiple runtimes:

```text
nodejs
java
python
go
shell
other
```

CE v0.1 only ships Node.js SDK.

### 12.3 Resource model

The manifest and database should allow future resource definitions such as:

- accounts;
- sessions;
- jobs;
- queues;
- quotas;
- connectors;
- tasks.

CE v0.1 may leave resource management minimal.

### 12.4 Secret references

Capsule Service metadata should use secret references where possible, not raw secrets.

Future examples:

```text
agent-local://agent-id/secrets/chatgpt/account-001
vault://secret/path
opstage-secret://workspace/key
```

CE v0.1 does not need a full secret store.

---

## 13. Anti-Patterns

Avoid the following patterns.

### 13.1 Opstage-dependent startup

Do not require Opstage to be online before the Capsule Service can start.

### 13.2 Arbitrary remote command execution

Do not expose arbitrary shell command execution as a normal CE v0.1 feature.

Only predefined actions should be supported.

### 13.3 Unbounded service scope

Do not create Capsule Services that mix unrelated capabilities.

### 13.4 Hidden state with no reporting

Do not keep critical runtime state invisible if Opstage is expected to govern the service.

### 13.5 Direct backend takeover

Do not design Opstage Backend to directly take over services without Agent registration and authorization.

---

## 14. Summary

Capsule Service is the core unit of the `xtrape-capsule` domain.

It is designed for AI-era lightweight service ecosystems where many small capability services need to stay independent but also need unified governance.

A good Capsule Service is:

- small enough to remain lightweight;
- clear enough to have a stable identity;
- independent enough to run without Opstage;
- observable enough to be governed;
- explicit enough to expose predefined actions;
- auditable enough to support long-term operation.

CE v0.1 should implement the minimum useful Capsule Service model through the Node.js embedded Agent SDK and a demo Capsule Service.
