---
status: proposed
audience: architects
stability: evolving
last_reviewed: 2026-05-05
---

# Runtime Documents

- Status: Implementation Guidance
- Edition: Shared
- Priority: Medium
- Audience: architects, runtime SDK developers, Capsule Service developers, backend developers, agent SDK developers, AI coding agents

This directory contains the runtime integration documents for the `xtrape-capsule` product family.

A runtime is a concrete language or execution environment that can host Capsule Services and Agent integrations.

The current implementation focus is **CE**. CE v0.1 prioritizes **Node.js**. Java, Python, Go, Sidecar runtime
integration, External Agent runtime integration, and Kubernetes runtime integration are future EE/Cloud extension tracks
and must not expand the CE v0.1 implementation scope.

---

## 1. Purpose of This Directory

The purpose of this directory is to define how different language and execution runtimes connect to the Capsule governance model.

It covers:

- the shared runtime integration model;
- the Node.js runtime implementation target;
- future Java runtime planning;
- future Python runtime planning;
- future Go/runtime directions if added later;
- runtime SDK design principles;
- runtime data boundary;
- CE implementation scope;
- EE and Cloud runtime extension points.

Runtime documents should adapt the Capsule model to ecosystems, not redefine the Capsule model.

---

## 2. Runtime Positioning

A runtime is:

> A concrete language or execution environment that hosts Capsule Services and Agent integrations.

Examples:

```text
Node.js
Java
Python
Go
container sidecar runtime
external process runtime
Kubernetes runtime
```

Runtime integration exists to make the same Capsule governance contract practical in different ecosystems.

---

## 3. Current CE Runtime Boundary

CE v0.1 should implement only one runtime path:

```text
Node.js Runtime + Node.js Embedded Agent SDK
```

CE runtime implementation should support:

- Node.js Capsule Service conventions;
- TypeScript-first integration;
- `@xtrape/capsule-agent-node` SDK usage;
- service identity declaration;
- health provider;
- config provider;
- action registry;
- command polling;
- CommandResult reporting;
- Docker-friendly demo service;
- safe logging;
- sensitive data avoidance.

CE should prove the governance loop with Node.js before adding more runtimes.

---

## 4. CE Runtime Non-Goals

CE v0.1 should not implement:

- Java runtime SDK;
- Python runtime SDK;
- Go runtime SDK;
- Sidecar runtime adapter;
- External Agent adapter framework;
- Kubernetes runtime integration;
- browser runtime adapter;
- account/session runtime adapter;
- runtime marketplace;
- runtime plugin system;
- multi-language compatibility matrix beyond planning;
- remote shell or arbitrary script runtime.

These are future planning topics.

---

## 5. Recommended Reading Order

Read the documents in this directory in the following order:

```text
06-runtimes/README.md
06-runtimes/00-runtime-overview.md
06-runtimes/01-node-runtime.md
06-runtimes/02-java-runtime-planning.md
06-runtimes/03-python-runtime-planning.md
```

For CE implementation, focus on:

```text
00-runtime-overview.md
01-node-runtime.md
```

For future EE planning, read:

```text
02-java-runtime-planning.md
03-python-runtime-planning.md
```

If Go runtime planning is added later, it should follow Python runtime planning in the reading order.

---

## 6. Document List

### 6.1 `00-runtime-overview.md`

Defines the shared runtime integration overview.

Use it to understand:

- runtime positioning;
- shared runtime contract;
- CE Node.js runtime scope;
- Java/Python/Go future directions;
- sidecar/external/Kubernetes runtime directions;
- runtime SDK design principles;
- runtime data boundary;
- runtime documentation requirements.

### 6.2 `01-node-runtime.md`

Defines the CE Node.js Runtime implementation target.

Use it to implement:

- Node.js Capsule Service conventions;
- `@xtrape/capsule-agent-node` integration;
- service identity;
- runtime configuration;
- Agent token store;
- health provider;
- config provider;
- action registration;
- command execution;
- CommandResult reporting;
- Docker demo;
- local development workflow;
- Node.js runtime tests.

This is a CE v0.1 implementation target.

### 6.3 `02-java-runtime-planning.md`

Defines future Java Runtime planning.

Use it for future design around:

- Java Embedded Agent SDK;
- Spring Boot starter;
- Spring Boot configuration properties;
- Actuator health bridge;
- Java action registration;
- Java token store;
- Spring lifecycle integration;
- enterprise Java compatibility.

This is not a CE v0.1 implementation target.

### 6.4 `03-python-runtime-planning.md`

Defines future Python Runtime planning.

Use it for future design around:

- Python Embedded Agent SDK;
- FastAPI helper;
- async runtime support;
- AI automation workers;
- LangChain/LangGraph workers;
- Playwright/browser automation workers;
- Python action registration;
- Python token store;
- account/session worker governance patterns.

This is not a CE v0.1 implementation target.

---

## 7. Shared Runtime Contract

All runtime integrations should preserve the same logical contract:

```text
Capsule Service identity
Agent integration
registration
heartbeat
manifest report
health report
config metadata report
action definition report
Command execution
CommandResult reporting
AuditEvent creation by Backend
secretRef boundary
```

Runtime-specific SDKs may differ in API style, but the governance semantics must remain consistent.

---

## 8. Runtime Status Summary

| Runtime | Status | CE v0.1 |
|---|---|---|
| Node.js | Implementation Target | Yes |
| Java | Planning | No |
| Python | Planning | No |
| Go | Future Planning | No |
| Sidecar runtime | Future Planning | No |
| External runtime | Future Planning | No |
| Kubernetes runtime | Future Planning | No |

CE should reserve runtime-compatible fields, but implement only Node.js in v0.1.

---

## 9. Runtime SDK Design Rules

Runtime SDKs should follow these rules:

1. Preserve the shared Capsule governance contract.
2. Use idiomatic APIs for each language.
3. Keep service integration small.
4. Keep Agent communication outbound-first.
5. Execute only predefined actions.
6. Avoid arbitrary shell execution.
7. Use `secretRef` for sensitive references.
8. Avoid raw secret reporting.
9. Keep token storage safe.
10. Handle Backend downtime without crashing business runtime by default.
11. Do not add future runtime complexity to CE v0.1.

---

## 10. Runtime Data Boundary

Runtime integrations may report governance metadata:

- service identity;
- runtime metadata;
- health status;
- config metadata;
- action metadata;
- CommandResult;
- sanitized errors.

Runtime integrations should not report raw sensitive data by default:

- passwords;
- cookies;
- OAuth tokens;
- API keys;
- private keys;
- account credentials;
- raw browser sessions;
- large application logs;
- private business records.

Use `secretRef`, masked values, or summaries.

---

## 11. Runtime Compatibility Fields

Shared runtime-related fields may include:

```text
runtime
runtimeVersion
agentMode
agentVersion
sdkVersion
protocolVersion
capabilities
metadataJson
```

CE may reserve these fields but should not implement a full runtime compatibility matrix in v0.1.

Future EE may use them for Agent diagnostics, compatibility warnings, and support workflows.

---

## 12. Implementation Priority for CE

Recommended CE runtime implementation order:

```text
1. Node.js runtime conventions
2. Node.js Agent SDK package
3. Node.js demo Capsule Service
4. Node.js Docker demo
5. Node.js SDK/runtime tests
6. Runtime quick-start documentation
```

Only Node.js runtime work is part of CE v0.1.

---

## 13. Future Runtime Expansion Rules

Future runtimes should be added only when:

- the Node.js CE governance loop is stable;
- the shared Backend Agent API is stable enough;
- the Command and Action model is validated;
- Agent token and permission semantics are validated;
- runtime-specific user demand exists;
- runtime SDKs can preserve the same governance semantics.

Do not add a runtime by copying concepts loosely and creating incompatible semantics.

---

## 14. Anti-Patterns

Avoid these patterns.

### 14.1 Too many runtimes before CE is stable

The first milestone is a working CE governance loop, not broad language coverage.

### 14.2 Runtime-specific semantics drift

Each runtime may use idiomatic APIs, but the governance contract must remain the same.

### 14.3 Runtime SDK exposes shell execution

Remote shell is not the Capsule operation model.

### 14.4 Runtime reports raw secrets

Use `secretRef` or masking.

### 14.5 Runtime integration becomes a framework replacement

Runtime integration should make services governable, not replace the service's application framework.

---

## 15. Acceptance Criteria

The Runtime document set is useful when:

- runtime concept is clear;
- Node.js is clearly the CE v0.1 implementation target;
- Java and Python are clearly future planning tracks;
- future Go/Sidecar/External/Kubernetes runtime directions are not treated as CE requirements;
- shared runtime contract is explicit;
- runtime data boundary is explicit;
- `secretRef` boundary is preserved;
- arbitrary shell execution is excluded;
- implementation agents can follow the reading order and build the Node.js runtime path first.

---

## 16. Summary

This directory defines how the Capsule governance model is adapted to concrete language and execution runtimes.

The most important Runtime directory rule is:

> Build and validate the Node.js runtime path first, then add Java, Python, Go, Sidecar, External, and Kubernetes runtimes only as compatible extensions of the same governance contract.
