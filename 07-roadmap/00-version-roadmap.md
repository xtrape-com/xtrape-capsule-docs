---
status: draft
audience: founders
stability: evolving
last_reviewed: 2026-05-07
---

# Version Roadmap

- Status: Implementation Guidance
- Edition: Shared
- Priority: Medium
- Audience: founders, architects, product managers, backend developers, frontend developers, agent SDK developers, AI coding agents

This document defines the version roadmap for the `xtrape-capsule` product family.

The current implementation focus is **CE v0.1**. CE v0.1 should prove the complete lightweight Capsule governance loop with Opstage Backend, Opstage UI, SQLite, and the Node.js Embedded Agent SDK.

EE and Cloud are future commercialization tracks. They should influence extension-point design, but they must not expand the CE v0.1 implementation scope.

The roadmap is now organized around four progressive concerns:

```text
1. Governance kernel
2. Productized CE operation
3. Lightweight service coordination
4. Private AI service stack integration
```

The most important roadmap rule is:

> Build the smallest complete governance loop first, then automate its maintenance, then add lightweight service coordination, and only then expand into enterprise, cloud, and AI-native runtime integration.

---

## 1. Purpose

The purpose of this roadmap is to define:

- what should be built first;
- what belongs to CE v0.1;
- what belongs to later CE stabilization;
- when AI-assisted product maintenance becomes relevant;
- when lightweight service communication becomes relevant;
- when Capsule Bus becomes relevant;
- when xtrape-hammers integration becomes relevant;
- when vieup-forge integration becomes relevant;
- when Agent modes should expand;
- when EE private deployment should become relevant;
- when Cloud SaaS should become relevant;
- how to avoid mixing future roadmap items into the current implementation.

The key rule is:

> CE v0.1 proves the governance loop. Later versions may improve automation, communication, AI runtime integration, and commercial packaging, but they must not dilute the CE v0.1 kernel.

---

## 2. Roadmap Principle

The roadmap follows this sequence:

```text
1. CE v0.1 — prove the governance loop
2. CE v0.2 — stabilize the CE kernel and productized release process
3. CE v0.3 — introduce experimental OpHub Runtime plus capability/event metadata
4. CE v0.4 — introduce experimental Capsule Bus concepts
5. CE v0.5 — introduce Capsule Catalog metadata and discovery
6. CE v0.6 — introduce Capsule Registry metadata
7. CE v0.7 — introduce Private Capsule Marketplace concepts
8. CE v1.0 — publish a reliable community edition and ecosystem foundation
9. Private AI Stack Track — integrate xtrape-hammers and vieup-forge as managed services
10. EE — add enterprise private-deployment capabilities
11. Cloud — add hosted SaaS capabilities
```

Do not build EE or Cloud infrastructure before CE proves the product kernel.

Do not implement Capsule Bus before static internal communication, service manifests, and service identity are stable.

Do not turn xtrape-capsule into an AI runtime. AI runtime belongs to `xtrape-hammers`; task-flow automation belongs to `vieup-forge`.

---

## 3. Product Kernel

The product kernel is the Capsule governance loop:

```text
Agent registration
    ↓
Service report
    ↓
Heartbeat and health
    ↓
Config visibility
    ↓
Predefined action request
    ↓
Command polling
    ↓
Command result
    ↓
Audit log
```

Every roadmap stage should preserve this kernel.

Future versions may add scale, security, identity, observability, service communication, AI runtime integration, and commercialization, but they should not redefine the kernel.

---

## 4. Roadmap Layers

The roadmap should be understood as layered expansion, not feature accumulation.

```text
Layer 1: Governance Kernel
  Agent registration, service report, heartbeat, command lifecycle, audit log.

Layer 2: Product Operation Automation
  Release process, AI-maintenance documents, issue triage readiness, CI/CD, changelog, docs sync.

Layer 3: Lightweight Service Communication
  Service manifest, endpoint metadata, internal URLs, service capabilities, service identity.

Layer 4: Capsule Bus
  Future bus-style internal communication for commands, events, and request/reply.

Layer 5: Private AI Stack Integration
  xtrape-hammers as AI runtime service, vieup-forge as TaskFlow automation/control plane.

Layer 6: Enterprise and Cloud Expansion
  RBAC, SSO, HA, Kubernetes, hosted service, billing, usage metering.
```

Capsule owns service governance and operation.

Hammers owns AI sessions, contexts, providers, prompts, and AI runtime calls.

Forge owns TaskFlow, Gate, task spiral, automation planning, and execution visibility.

---

## 5. CE v0.1 Goal

CE v0.1 goal:

> Deliver a lightweight, open-source, self-hosted, single-node Opstage prototype that proves the full Capsule governance loop.

CE v0.1 should be good enough for:

- local development;
- demo use;
- early open-source feedback;
- validating the Capsule/Agent model;
- proving the UI + Backend + Agent vertical slice;
- guiding future architecture decisions.

CE v0.1 does not need to be enterprise-grade.

---

## 6. CE v0.1 Scope

CE v0.1 should include:

```text
Opstage Backend
Opstage UI
SQLite persistence
local admin login
registration token
Agent token authentication
Node.js Embedded Agent SDK
Node.js demo Capsule Service
Agent heartbeat
service manifest report
health report
config metadata visibility
predefined action metadata
action request from UI
Command creation
command polling
CommandResult reporting
basic AuditEvents
Dashboard summary
System health endpoint
Docker quick start
minimal release notes
minimal troubleshooting guide
```

This is the current implementation target.

---

## 7. CE v0.1 Non-Goals

CE v0.1 should not include:

```text
Tenant system
Organization system
billing
subscription
usage metering
enterprise RBAC
SSO / OIDC / LDAP / SAML
PostgreSQL/MySQL requirement
Redis requirement
Queue requirement
Kubernetes requirement
Agent Gateway
Sidecar Agent
External Agent
Java Agent SDK
Python Agent SDK
Go Agent SDK
full observability platform
alert rule engine
secret vault
license enforcement
remote shell
arbitrary script execution
Capsule Bus
internal service gateway
service mesh
AI runtime calling layer
xtrape-hammers integration
vieup-forge integration
AI-assisted issue triage automation
AI-assisted release automation
```

These are future roadmap items.

---

## 8. CE v0.1 Recommended Implementation Order

Recommended implementation order:

```text
1. Backend project scaffold
2. UI project scaffold
3. SQLite schema and persistence
4. Local admin authentication
5. Registration token model
6. Agent registration API
7. Agent token authentication
8. Node.js Agent SDK scaffold
9. Agent heartbeat
10. Service manifest report
11. Agent and service UI pages
12. Health and config metadata visibility
13. ActionDefinition model
14. Command creation from UI
15. Command polling from SDK
16. CommandResult reporting
17. AuditEvent model and UI
18. Dashboard summary
19. System health endpoint
20. Node.js demo Capsule Service
21. Docker quick start
22. Minimal documentation and release notes
```

The order may be adjusted during implementation, but the vertical governance loop should remain the priority.

---

## 9. CE v0.1 Acceptance Criteria

CE v0.1 is acceptable when:

- user can start Opstage locally;
- user can log in as local admin;
- user can create a registration token;
- Node.js demo Capsule Service can register;
- Agent appears in UI;
- Capsule Service appears in UI;
- heartbeat status is visible;
- health status is visible;
- config metadata is visible;
- predefined actions are visible;
- user can run `echo` action;
- user can run `runHealthCheck` action;
- Backend creates Commands;
- Agent polls Commands;
- Agent reports CommandResults;
- UI displays CommandResult;
- AuditEvents are created and visible;
- stale/offline state is visible;
- sensitive values are masked;
- raw tokens are not logged;
- no arbitrary shell execution exists;
- Docker quick start can demonstrate the loop.

---

## 10. CE v0.2 Direction — Kernel Stabilization and Release Discipline

CE v0.2 should stabilize the CE kernel after v0.1 feedback.

Possible focus areas:

- improve UI usability;
- improve error handling;
- improve SDK developer experience;
- improve dashboard clarity;
- improve status and freshness calculation;
- improve audit filtering;
- improve Docker packaging;
- add better local development scripts;
- add more tests;
- add migration discipline;
- improve documentation;
- add release checklist;
- add changelog discipline;
- add basic contribution guide;
- add issue and PR templates.

CE v0.2 should still avoid EE/Cloud complexity.

CE v0.2 should not add Capsule Bus or AI runtime capabilities.

---

## 11. CE v0.3 Direction — OpHub Runtime, Capsule Events, and Capability Metadata

CE v0.3 introduces **OpHub Runtime** as an experimental deployment mode and adds
the metadata foundation needed for future Capsule Bus work.

The two Agent modes are:

- **Embedded Agent** — one Capsule Service embeds the Node SDK and talks to Opstage directly.
- **OpHub Runtime** — one OpHub process, sidecar, or base-image deployment represents one or more local Capsule Services.

Required v0.3 focus areas:

- `AgentMode` contract with `embedded` and `ophub`;
- OpHub registration semantics;
- one OpHub reporting one or more Capsule Services;
- stable service identity through OpHub reports;
- command routing from OpHub to local service adapters;
- capability metadata for service discovery;
- event metadata marked design-only unless an actual event runtime is implemented;
- demo profile showing OpHub-managed adapter mode with local services;
- public documentation that keeps Capsule Bus future-facing.

CE v0.3 should not implement full Capsule Bus, a workflow engine, or a service
mesh. It reserves shape and validates the local runtime model.

---

## 12. CE v0.4 Direction — Capsule Bus Experimental

> **Direction change (2026-05-16).** v0.4 and v0.5 themes were swapped
> compared to earlier drafts of this roadmap. The previous v0.5 plan
> (Capsule Bus planning + early prototype) is brought forward into v0.4
> because v0.3 (OpHub Runtime + Capsule Events + Capability Metadata)
> already produced the event envelope and capability metadata that the
> bus needs as input. Pushing service-manifest work to v0.5 lets the
> bus prototype validate the routing model first; the manifest can
> then be designed against real bus traffic instead of speculative
> requirements. See §13 below for the new v0.5 scope.

CE v0.4 introduces an **experimental, default-disabled Capsule Bus**
that performs governed event-to-command routing inside a single
Opstage CE instance.

Capsule Bus v0.4 is **not** a workflow engine, service mesh,
distributed transaction layer, or general-purpose message broker
replacement.

Recommended CE v0.4 scope:

- define `BusRoutingRule`, `BusEventEnvelope`, and `BusCommandRequest`
  schemas in `xtrape-capsule-contracts-node`;
- store events and routes in CE SQLite;
- evaluate enabled routes on `eventType` plus optional
  `sourceServiceCode`;
- emit an `ACTION_EXECUTE` command for each matched route (one
  command per matched route in v0.4 — no fan-out);
- offer a `DRY_RUN` route status that audits matches without creating
  commands;
- gate the entire feature behind `OPSTAGE_CAPSULE_BUS_ENABLED=true`
  (default `false`);
- ship a self-routing demo scenario (`demo-worker` emits
  `demo.item.created`, route fires `demo-worker.notify`);
- record audit events for every routing decision
  (`bus.event.received` / `bus.route.matched` /
  `bus.command.created` / `bus.route.failed` /
  `bus.route.unmatched`);
- enforce a hard max routing depth of 1 (a command's own completion
  must not produce a new bus event that re-enters the router) to
  eliminate loop risk programmatically;
- rate-limit per-agent event ingestion (default 60 events/min);
- add a CE admin UI page for route management + bus audit log.

Capsule Bus v0.4 should still avoid:

```text
service mesh
mTLS everywhere
complex routing algorithms
load balancing
external message broker (Redis, RabbitMQ, NATS, Kafka)
queue infrastructure requirement
fan-out (commands-per-event > 1)
non-Node OpHub runtime
public marketplace or registry workflows
```

The detailed implementation plan lives at
`10-implementation/v0.4-capsule-bus-implementation-plan.md` and the
operator-facing concept page at
`04-opstage/v0.4-capsule-bus-experimental.md`.

---

## 13. CE v0.5 Direction — Capsule Catalog (metadata + discovery)

CE v0.5 introduces the **Capsule Catalog** — a centralised, lightweight
view of every Capsule Service running against an Opstage instance, with
the service-communication metadata needed for the v0.4 bus to address
services symbolically (by `serviceCode` / `capability` rather than by
hardcoded URL).

The v0.4 bus shipped before this on purpose: the catalog can now be
designed against real routing traffic instead of against speculative
requirements.

Recommended CE v0.5 scope:

- Service Manifest v1 (describes a capsule-managed service's internal
  endpoints, capabilities, and visibility);
- internal endpoint metadata (`public` / `admin` / `internal`
  visibility, static URLs, Docker Compose naming convention);
- service capability metadata (canonical capability strings, e.g.
  `llm.chat`, `task.plan`, `health.probe`);
- basic service dependency metadata;
- a Catalog page in Opstage UI listing services + their declared
  endpoints/capabilities;
- discovery-by-capability — bus routes and admin tooling can look up
  a target service by capability rather than by raw `serviceCode`;
- promote the v0.4 bus from experimental to stable if the routing
  model has held up in real use.

Example Service Manifest direction:

```yaml
service:
  id: xtrape-hammers
  type: ai-runtime
  version: 0.1.0

network:
  internalBaseUrl: http://xtrape-hammers:8080

endpoints:
  - name: chat
    method: POST
    path: /v1/chat/completions
    visibility: internal
  - name: health
    method: GET
    path: /health
    visibility: internal

capabilities:
  - llm.chat
  - llm.embedding
  - task.plan
```

CE v0.5 should still avoid:

```text
service mesh
mTLS everywhere
complex routing
load balancing
message broker requirement
queue requirement
public registry across Opstage instances (that is v0.6)
marketplace workflows (that is v0.7)
```

CE v0.5 must not require Redis, RabbitMQ, NATS, Kafka, or any
external queue by default.

---

## 14. CE v1.0 Direction

CE v1.0 should be a reliable community release.

Expected qualities:

- stable core concepts;
- stable Agent API;
- stable Node.js SDK API;
- stable SQLite deployment path;
- documented upgrade path;
- meaningful test coverage;
- reliable Docker quick start;
- clear security notes;
- clear CE/EE/Cloud boundaries;
- useful open-source experience;
- documented service manifest model if introduced before v1.0;
- documented future Capsule Bus direction if introduced before v1.0.

CE v1.0 should still be self-hosted and lightweight.

Capsule Bus is not required for CE v1.0 unless the previous versions prove it is essential.

---

## 15. Private AI Stack Track

The Private AI Stack Track is a future product integration track, not a CE v0.1 requirement.

It connects three projects:

```text
xtrape-capsule
  Service operation plane.

xtrape-hammers
  AI runtime plane.

vieup-forge
  TaskFlow and automation control plane.
```

Recommended relationship:

```text
vieup-forge
  ↓ TaskFlow / Gate / Node execution planning
xtrape-hammers
  ↓ AI session / context / provider / prompt runtime
xtrape-capsule
  ↓ service deployment / health / config / command / audit governance
capsule-managed services
```

This track should begin only after CE can manage a real service reliably.

---

## 16. xtrape-hammers Integration Direction

`xtrape-hammers` should be integrated as a managed Capsule Service, not as part of Capsule core.

Potential integration scope:

- hammers service manifest;
- hammers health and config metadata;
- hammers predefined actions;
- hammers provider status visibility;
- hammers logs and diagnostics through Capsule governance;
- hammers as an example `ai-runtime` capsule service;
- optional hammers demo stack in Docker Compose.

Capsule should not implement AI session management, model provider routing, prompt management, memory, or tool-calling runtime directly.

Those belong to hammers.

---

## 17. vieup-forge Integration Direction

`vieup-forge` should be integrated as an automation/control-plane consumer of Capsule, not as part of Capsule core.

Potential integration scope:

- manage capsule release tasks through TaskFlow;
- generate Capsule maintenance plans;
- triage issues into TaskFlow nodes;
- produce release checklists;
- generate documentation update tasks;
- execute predefined Capsule actions through approved Gates;
- record Capsule maintenance decisions.

Capsule should expose enough metadata for forge to reason about services, agents, commands, and audit events.

Capsule should not implement TaskFlow, Gate, task spiral, or AI planning directly.

Those belong to forge.

---

## 18. Agent Expansion Roadmap

Agent expansion should happen after the CE Embedded Agent model is validated.

Recommended order:

```text
1. Node.js Embedded Agent
2. Sidecar Agent prototype
3. External Agent prototype
4. Java Embedded Agent SDK
5. Python Embedded Agent SDK
6. Go SDK or Go-based Agent runtime
7. Kubernetes Agent
```

This order is not fixed, but the first step is fixed:

```text
Node.js Embedded Agent first
```

Agent expansion should not happen before the Node.js SDK proves the governance contract.

---

## 19. Runtime Expansion Roadmap

Runtime expansion should happen after Node.js is stable.

Recommended order:

```text
1. Node.js Runtime
2. Java Runtime planning and prototype
3. Python Runtime planning and prototype
4. Go Runtime planning and prototype
5. Sidecar/External runtime adapters
6. Kubernetes runtime integration
```

Runtime expansion should preserve the same governance contract.

Runtime expansion should not redefine service communication or Capsule Bus prematurely.

---

## 20. EE Roadmap Direction

EE should start after CE has a stable kernel and real usage signals.

Potential EE focus areas:

- PostgreSQL/MySQL official support;
- enterprise RBAC;
- SSO / OIDC / LDAP / SAML;
- audit export;
- audit retention configuration;
- alert rules;
- observability integrations;
- secret provider integrations;
- Sidecar Agent;
- External Agent;
- Java/Python/Go Agent SDKs;
- backup and restore tooling;
- high availability;
- Kubernetes / Helm deployment;
- support bundle;
- private deployment package;
- commercial support;
- enterprise service identity;
- enterprise service communication policy;
- managed Capsule Bus only if demand is proven.

EE should sell enterprise value, not cripple CE.

---

## 21. Cloud Roadmap Direction

Cloud should start after CE/EE concepts are sufficiently validated.

Potential Cloud focus areas:

- hosted Backend and UI;
- Tenant / Organization / Workspace model;
- team invitations;
- subscription billing;
- usage metering;
- Cloud Agent Gateway;
- workspace-scoped registration tokens;
- managed audit retention;
- managed alerting;
- Cloud support workflows;
- data export and deletion workflows;
- Cloud operational monitoring;
- SaaS onboarding UX;
- optional hosted Opstage for private agents;
- optional managed coordination layer if Capsule Bus matures.

Cloud should remain compatible with the same Agent governance model.

Cloud should not require customers to expose private service internals unless explicitly configured.

---

## 22. Version Naming

Recommended version naming:

```text
CE v0.1
CE v0.2
CE v0.3
CE v0.4
CE v0.5
CE v1.0
Private AI Stack Alpha
Private AI Stack Beta
EE Alpha
EE Beta
EE v1.0
Cloud Alpha
Cloud Beta
Cloud v1.0
```

Avoid using enterprise or Cloud version names before the CE kernel is stable.

Avoid using Private AI Stack version names before xtrape-hammers and vieup-forge have minimal usable forms.

---

## 23. Release Artifact Direction

CE release artifacts may include:

```text
source code
Docker image
Docker Compose example
Node Agent SDK package
Node demo Capsule Service
migration files
quick start guide
release notes
troubleshooting guide
AI maintenance guide after CE v0.3
service manifest examples after CE v0.5
```

Future Private AI Stack artifacts may include:

```text
capsule + hammers Docker Compose example
hammers service manifest
forge maintenance TaskFlow templates
private AI service stack quick start
AI runtime service demo
```

Future EE artifacts may include:

```text
private Docker images
private deployment package
Helm chart
backup/restore scripts
support bundle tool
security hardening guide
upgrade guide
license or entitlement package if needed
```

Future Cloud artifacts are mainly hosted service releases and customer-facing onboarding flows.

---

## 24. Documentation Roadmap

Documentation should evolve with versions.

### CE v0.1 documentation

Required:

- quick start;
- architecture overview;
- Opstage UI/Backend/Agent docs;
- Node Agent SDK guide;
- Node demo service guide;
- Docker quick start;
- security notes;
- troubleshooting.

### CE v0.2 documentation

Add:

- release checklist;
- contribution guide;
- issue and PR template guide;
- changelog policy;
- local development guide.

### CE v0.3 documentation

Add:

- AI maintenance guide;
- release automation guide;
- product boundary guide;
- AI-assisted issue triage guide;
- AI-assisted docs update guide;
- multi-repository maintenance guide if needed.

### CE v0.4 documentation

Add:

- Capsule Bus experimental concept page;
- bus message envelope (`BusEventEnvelope`) reference;
- routing-rule (`BusRoutingRule`) reference;
- service identity draft (how `sourceServiceCode` is verified);
- audit-event reference (`bus.event.received`, `bus.route.matched`,
  `bus.command.created`, `bus.route.failed`, `bus.route.unmatched`);
- loop / storm safeguard guide (depth=1 hard limit, rate limit);
- feature-flag operator guide (`OPSTAGE_CAPSULE_BUS_ENABLED`);
- Capsule Bus v0.4 non-goals.

### CE v0.5 documentation

Add:

- service manifest guide;
- endpoint visibility guide;
- internal URL convention;
- capability metadata guide;
- discovery-by-capability guide for bus routes;
- Capsule Catalog page reference.

### CE v1.0 documentation

Add:

- upgrade guide;
- API reference;
- SDK reference;
- deployment guide;
- stable contribution guide;
- stable release process.

### Private AI Stack documentation

Add:

- hammers as capsule service guide;
- forge-managed capsule maintenance guide;
- private AI service stack quick start;
- AI runtime service observability guide.

### EE documentation

Add:

- enterprise deployment guide;
- RBAC guide;
- SSO guide;
- audit/compliance guide;
- observability integration guide;
- secret provider integration guide;
- backup/restore guide;
- support guide.

### Cloud documentation

Add:

- signup/onboarding guide;
- organization/workspace guide;
- Agent enrollment guide;
- billing guide;
- data export/deletion guide;
- Cloud support guide.

---

## 25. Roadmap Guardrails

Follow these guardrails:

1. Do not implement EE/Cloud features in CE v0.1.
2. Do not add multiple runtimes before Node.js is stable.
3. Do not add Sidecar/External Agent before Embedded Agent is stable.
4. Do not add alerting before status and freshness are reliable.
5. Do not add billing before Cloud exists.
6. Do not add license enforcement before EE has real commercial demand.
7. Do not add arbitrary shell execution.
8. Do not store raw secrets by default.
9. Do not break CE trust with artificial limitations.
10. Do not redefine the Capsule governance kernel per edition.
11. Do not implement Capsule Bus before service manifest and service identity are clear.
12. Do not turn Capsule into a service mesh.
13. Do not turn Capsule into an AI runtime.
14. Do not implement TaskFlow or Gate inside Capsule core.
15. Do not add external queue requirements to CE by default.
16. Do not expand Private AI Stack before hammers and forge have minimal usable forms.
17. Do not make OpenClaw or any third-party agent runtime a hard dependency.

---

## 26. Decision Checkpoints

Before moving between roadmap stages, review these checkpoints.

### Before CE v0.2

Ask:

- Does the full governance loop work?
- Is the Agent API usable?
- Is the Node SDK developer experience acceptable?
- Are status and freshness understandable?
- Are users able to run demo actions successfully?
- Is Docker quick start reliable?

### Before CE v0.3

Ask:

- Is the release process repeatable?
- Are issue templates and PR templates in place?
- Can AI coding agents understand the project boundaries?
- Is there a documented maintenance process?
- Is the maintainer burden acceptable?

### Before CE v0.4

Ask:

- Is v0.3 tagged + accepted (events + capability metadata stable)?
- Is point-to-point service communication becoming a real pain?
- Are command / event semantics clear enough to route on?
- Is `sourceServiceCode` identity verifiable from the existing agent
  token model?
- Can the prototype stay disabled-by-default and gated by
  `OPSTAGE_CAPSULE_BUS_ENABLED`?
- Are loop / storm risks adequately bounded (`max routing depth = 1`,
  per-agent rate limit)?

### Before CE v0.5

Ask:

- Has the v0.4 experimental bus run long enough to surface the fields
  a manifest must standardise?
- Are service manifests stable enough to extend?
- Do users need internal service endpoint metadata in addition to
  capability metadata?
- Should bus routes start resolving targets by capability rather than
  by `serviceCode`?
- Can the v0.4 bus be promoted from experimental to stable, or does
  it need another minor of bake time?

### Before CE v1.0

Ask:

- Are core APIs stable enough?
- Is upgrade/migration acceptable?
- Is documentation sufficient?
- Is the security boundary clear?
- Is CE useful as an open-source product?
- Are future features clearly separated from stable CE guarantees?

### Before Private AI Stack

Ask:

- Can Capsule manage hammers as a normal service?
- Does hammers have a minimal AI runtime API?
- Does forge have a minimal TaskFlow runtime?
- Is the integration useful without becoming a hard dependency?
- Is the private AI service stack story clear?

### Before EE

Ask:

- Is there real private deployment demand?
- Which enterprise features are actually requested?
- Which database/deployment mode is required first?
- Which Agent expansion has the strongest demand?
- What support burden is acceptable?
- Does enterprise service communication require Capsule Bus or simpler policies?

### Before Cloud

Ask:

- Is there SaaS demand?
- Is multi-tenancy worth the added complexity?
- Is Agent Gateway required?
- Are billing and support workflows ready?
- Is operational responsibility acceptable?
- Are private agent security boundaries clear?

---

## 27. Anti-Patterns

Avoid these roadmap anti-patterns.

### 27.1 Building all future editions at once

This slows CE and makes the product unclear.

### 27.2 CE as a broken demo

CE should be genuinely useful.

### 27.3 Agent expansion before Agent basics

Embedded Agent should be stable before Sidecar/External Agent.

### 27.4 Runtime expansion before Node.js is stable

More runtimes should not come before a validated governance contract.

### 27.5 Commercial packaging before product value

License and entitlement systems should not consume early engineering capacity.

### 27.6 Observability platform before governance visibility

First make Agents, services, health, Commands, and AuditEvents visible.

### 27.7 Service mesh by accident

Lightweight service communication should not become Kubernetes, Istio, or a full service mesh.

### 27.8 AI runtime inside Capsule core

Capsule should manage AI runtime services, not become one.

### 27.9 TaskFlow inside Capsule core

TaskFlow, Gate, and task spiral belong to vieup-forge, not Capsule core.

### 27.10 Bus before metadata, catalog before marketplace

Capsule Bus v0.4 ships **before** the full service-manifest /
discovery-by-capability work in v0.5 on purpose — the bus is the
real-traffic test for which fields the manifest must standardise.
What this rule still forbids:

- A bus that requires an external broker (Redis / Kafka / NATS) in
  CE.
- A bus that ships without service-identity verification on its
  ingestion path.
- Capsule Catalog (v0.5) before the v0.4 bus has surfaced the
  routing-relevant fields.
- Capsule Registry / Marketplace before Catalog has stabilised
  capability strings.

---

## 28. Summary Roadmap

Recommended roadmap summary:

```text
CE v0.1
  Build the lightweight governance loop with Node.js Embedded Agent.

CE v0.2
  Stabilize CE, improve UI, error handling, SDK DX, tests, packaging, and release discipline.

CE v0.3
  Introduce experimental OpHub Runtime plus Capsule Events and Capability Metadata.

CE v0.4
  Introduce experimental Capsule Bus (governed event-to-command routing,
  disabled by default, gated by OPSTAGE_CAPSULE_BUS_ENABLED).

CE v0.5
  Introduce Capsule Catalog: Service Manifest, endpoint visibility,
  capabilities, internal URL convention, discovery-by-capability for
  bus routes; promote v0.4 bus from experimental to stable if proven.

CE v1.0
  Publish a reliable open-source community edition.

Private AI Stack Track
  Integrate xtrape-hammers as an AI runtime service and vieup-forge as an automation/control-plane consumer.

EE
  Add enterprise private-deployment capabilities based on real demand.

Cloud
  Add hosted SaaS capabilities after the governance model is mature.
```

---

## 29. Acceptance Criteria

This roadmap is acceptable when:

- CE v0.1 scope is clear;
- CE v0.1 non-goals are clear;
- Node.js Embedded Agent is clearly first;
- future Agent and runtime expansion is sequenced;
- service communication is staged instead of overbuilt;
- Capsule Bus is future-facing and optional;
- xtrape-hammers is positioned as AI runtime, not Capsule core;
- vieup-forge is positioned as TaskFlow automation/control plane, not Capsule core;
- EE and Cloud are clearly future tracks;
- roadmap guardrails prevent scope creep;
- release and documentation directions are clear;
- CE remains useful and open-source;
- future editions extend the same governance kernel.

---

## 30. Summary

The `xtrape-capsule` roadmap should prioritize a working, lightweight, open-source CE kernel before expanding into enterprise and SaaS editions.

The roadmap now explicitly separates:

```text
Capsule governance
Product maintenance automation
Lightweight service communication
Capsule Bus
AI runtime integration
TaskFlow automation
Enterprise and Cloud packaging
```

The most important roadmap rule is:

> Build the smallest complete governance loop first, then automate maintenance, then introduce lightweight service coordination, then integrate AI runtime and TaskFlow automation, and only then expand scale, runtime coverage, Agent modes, enterprise features, and Cloud hosting.
