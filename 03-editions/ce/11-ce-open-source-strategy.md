# CE Open Source Strategy

- Status: Implementation Target
- Edition: CE
- Priority: Current
- Audience: founders, product designers, architects, developers, open-source contributors, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/` disagree, the ADRs and contracts win for CE v0.1.

This document defines the open-source strategy for **Opstage CE / Community Edition**.

CE should be a real, useful, self-hosted open-source product. It should establish trust, validate the Capsule Service model, and create an adoption path for future EE and Cloud editions without making CE feel like an intentionally crippled product.

---

## 1. Strategy Goal

The goal of the CE open-source strategy is:

> Use CE to establish `xtrape-capsule` as a credible lightweight governance model for small services, AI tools, CAPI services, and automation workers.

CE should help users understand and adopt the core idea:

```text
Lightweight services remain independent,
but become visible, manageable, and auditable through Agents and Opstage.
```

Open source should support three outcomes:

1. build trust;
2. attract early adopters;
3. create a foundation for future commercial editions.

---

## 2. Open Source Positioning

Opstage CE is:

> A lightweight, self-hosted, open-source control plane for Capsule Services.

It is intended for:

- individual developers;
- small teams;
- self-hosted users;
- AI automation builders;
- CAPI service developers;
- internal tooling teams;
- open-source contributors.

CE should be useful without requiring EE or Cloud.

---

## 3. Why CE Should Be Open Source

CE should be open source because the product sits close to sensitive runtime governance data.

It may handle or display:

- service topology;
- Agent status;
- account/session metadata;
- configuration metadata;
- health reports;
- command history;
- audit events;
- secret references.

Users are more likely to trust a self-hosted governance tool when they can inspect the source code.

Open source also helps establish the Capsule Service concept before the commercial product is mature.

---

## 4. What CE Should Prove

CE should prove the minimum complete Capsule governance loop:

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

This is the product kernel.

If this loop is useful, EE and Cloud can grow naturally from it.

---

## 5. Open Source Product Principles

CE should follow these product principles:

1. CE must be genuinely useful.
2. CE should be easy to run.
3. CE should be safe by default.
4. CE should not require external SaaS.
5. CE should not hide critical source code.
6. CE should not feel like a broken trial version.
7. CE should reserve commercial extension points cleanly.
8. CE should document what is free, what is future, and what is commercial.
9. CE should build trust before monetization pressure.
10. CE should prioritize developer adoption and real usage feedback.

---

## 6. Repository Strategy

CE v0.1 ships across **four repositories** under the `xtrape` GitHub organization. The decision and full rationale live in [ADR 0008 — Naming and Repositories](../../08-decisions/0008-naming-and-repositories.md). This section is a public-facing summary.

### 6.1 The four repositories

| Repo | Edition | What it contains |
|---|---|---|
| `xtrape-capsule-docs` | shared | Design docs, ADRs, and the language-agnostic Layer 1 contract SSOT (OpenAPI YAML, JSON enums, error codes). |
| `xtrape-capsule-contracts-node` | shared | Node bindings of the contracts (TypeScript types, Zod schemas, enum constants). Published as `@xtrape/capsule-contracts-node` on npm. |
| `xtrape-capsule-agent-node` | shared | Node Agent SDK. Published as `@xtrape/capsule-agent-node` on npm. |
| **`xtrape-capsule-ce`** | **CE** | The CE control plane: Opstage backend (Fastify), Opstage UI (React 18 + Ant Design (antd)), demo Capsule Service, and Docker deploy. The only edition-bound code repo. |

### 6.2 Why this split

Two principles drove the four-repo decision:

1. **Edition-agnostic vs edition-bound separation.** The wire contracts and the Agent SDK MUST work against future EE and Cloud backends without recompilation, so they live outside any edition's release cycle.
2. **One language per binding repo.** Future Java / Python / Go agents will get their own `xtrape-capsule-contracts-{lang}` and `xtrape-capsule-agent-{lang}` repos, each with its own native toolchain. Path C in [ADR 0009](../../08-decisions/0009-contracts-spec-and-bindings.md).

### 6.3 Repository descriptions (used in GitHub "About" field)

| Repo | Description |
|---|---|
| `xtrape-capsule-docs` | Design documents, ADRs, and wire-contract SSOT for the Opstage / Capsule Service product family. |
| `xtrape-capsule-contracts-node` | TypeScript bindings (types, Zod schemas, enums, error codes) for the Opstage wire contracts. |
| `xtrape-capsule-agent-node` | Node.js Agent SDK for embedding Capsule Services into the Opstage governance loop. |
| `xtrape-capsule-ce` | Opstage CE — a lightweight, self-hosted, open-source control plane for Capsule Services. |

### 6.4 `xtrape-capsule-ce` internal layout

Inside `xtrape-capsule-ce` (the CE monorepo), pnpm workspace packages are arranged as follows:

```text
xtrape-capsule-ce/
├── apps/
│   ├── opstage-backend/                @xtrape/opstage-backend         (private)
│   ├── opstage-ui/                     @xtrape/opstage-ui              (private; React 18 + Ant Design)
│   └── demo-capsule-service/           @xtrape/demo-capsule-service    (private)
├── packages/
│   ├── db/                             @xtrape/capsule-db              (private)
│   ├── shared/                         @xtrape/capsule-shared          (private)
│   └── test-utils/                     @xtrape/capsule-test-utils      (private)
├── deploy/
│   ├── docker/
│   └── compose/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
└── ROADMAP.md
```

`@xtrape/capsule-contracts-node` and `@xtrape/capsule-agent-node` come from npm; they are NOT workspace packages here. See [`10-implementation/00-repository-structure.md`](../../10-implementation/00-repository-structure.md) for the full details.

### 6.5 Public documentation

Each of the four repositories should include clear public documentation:

- `xtrape-capsule-docs`: full design docs (this directory).
- `xtrape-capsule-contracts-node` README: project overview, npm install snippet, compatibility table (binding version ↔ spec version), pointer to docs repo.
- `xtrape-capsule-agent-node` README: SDK overview, install snippet, minimal example, pointer to docs repo.
- `xtrape-capsule-ce` README: project overview, quick start (`docker compose up`), demo guide, Agent SDK guide, API overview, architecture overview, security model, CE/EE/Cloud edition explanation, roadmap, contribution guide.

Per ADR 0008, repository names, npm scope (`@xtrape`), GHCR namespace (`ghcr.io/xtrape`), and image names (`opstage-ce`, `demo-capsule-service`) are normative — implementation MUST follow them.

---

## 7. License Strategy

### 7.1 Candidate licenses

Possible licenses:

```text
Apache-2.0
MIT
AGPL-3.0
Elastic License / custom source-available license
```

### 7.2 Recommended CE license

Recommended license for CE:

```text
Apache-2.0
```

### 7.3 Rationale

Apache-2.0 is recommended because:

- it is business-friendly;
- it is widely trusted;
- it includes explicit patent grant;
- it encourages adoption;
- it works well for infrastructure and developer tools;
- it does not scare away enterprise evaluators.

### 7.4 Alternative: AGPL-3.0

AGPL-3.0 may protect against cloud competitors using the code without contributing back.

However, it may reduce adoption by companies and make integration more difficult.

For this project, broad adoption and trust are more important in the CE phase.

### 7.5 Commercial editions

EE and Cloud can remain commercial while CE is Apache-2.0.

The key is to keep CE useful and define commercial features clearly.

---

## 8. CE / EE / Cloud Boundary

The open-source strategy must clearly define edition boundaries.

### 8.1 CE should include

CE should include:

- self-hosted deployment;
- SQLite default database;
- local admin login;
- Node.js embedded Agent SDK;
- Agent registration;
- heartbeat;
- Capsule Service report;
- health visibility;
- config visibility;
- predefined actions;
- command polling;
- command results;
- basic audit logs;
- demo Capsule Service;
- Docker deployment.

### 8.2 EE may include

Future EE may include:

- MySQL/PostgreSQL official support;
- enterprise installer;
- high availability;
- cluster deployment;
- RBAC;
- SSO/OIDC/LDAP;
- advanced audit retention;
- centralized logs;
- metrics dashboards;
- alert rules;
- secret vault integration;
- Java/Python Agent SDKs;
- sidecar/external Agents;
- enterprise support.

### 8.3 Cloud may include

Future Cloud may include:

- hosted Opstage Backend;
- multi-tenant workspaces;
- subscription billing;
- managed Agent gateway;
- managed alerting;
- managed audit retention;
- team collaboration;
- usage dashboards;
- commercial SLA.

### 8.4 Boundary principle

The boundary should be based on scale, enterprise governance, and managed service value, not on disabling the core CE loop.

Good boundary:

```text
CE = single-node self-hosted governance
EE = enterprise private deployment and governance
Cloud = hosted SaaS governance
```

Bad boundary:

```text
CE cannot run actions
CE cannot see audit logs
CE cannot use Agent SDK properly
```

---

## 9. Open-Core Strategy

The recommended model is:

```text
Open-core with a genuinely useful CE
```

CE should contain the product kernel.

EE and Cloud should add advanced operational, organizational, and enterprise capabilities.

### 9.1 What should remain open

The following should remain open in CE:

- core Backend;
- Web UI for CE features;
- Node.js embedded Agent SDK;
- shared specifications;
- shared types;
- demo service;
- Docker deployment;
- basic audit and command loop.

### 9.2 What may become commercial

The following may be commercial:

- enterprise RBAC;
- SSO integrations;
- advanced Agent modes;
- advanced databases and HA support;
- log and metrics platform integration;
- alert rules;
- managed secrets;
- compliance audit packages;
- Cloud tenancy and billing;
- enterprise deployment tooling.

---

## 10. First Public Release Strategy

### 10.1 Release target

First public release should be:

```text
v0.1.0-alpha
```

or:

```text
v0.1.0
```

if the MVP is stable enough.

Recommended:

```text
v0.1.0-alpha
```

because the data model and APIs may still change.

### 10.2 Release contents

First public release should include:

- working Backend;
- working UI;
- SQLite persistence;
- Node.js embedded Agent SDK;
- demo Capsule Service;
- Docker quick start;
- README;
- basic docs;
- security notes;
- roadmap.

### 10.3 Release non-goals

Do not wait for:

- EE features;
- Cloud features;
- perfect UI;
- full observability;
- multiple Agent languages;
- Kubernetes deployment;
- advanced RBAC.

The first release should prove the vertical slice.

---

## 11. README Strategy

The README should answer quickly:

1. What is Opstage CE?
2. What problem does it solve?
3. What is a Capsule Service?
4. How do I run it?
5. How do I start the demo service?
6. How do I create a registration token?
7. How do I embed the Agent SDK?
8. What is included in CE?
9. What is planned for EE/Cloud?
10. How can I contribute?

Recommended README structure:

```text
Project tagline
Problem statement
Core concepts
Quick start
Demo walkthrough
Agent SDK example
Screenshots
Architecture overview
Edition comparison
Roadmap
Contributing
License
```

---

## 12. Documentation Strategy

Public docs should be practical and developer-facing.

Required docs for first release:

```text
docs/overview.md
docs/quick-start.md
docs/concepts/capsule-service.md
docs/concepts/agent.md
docs/agent-node.md
docs/api.md
docs/security.md
docs/deployment.md
docs/editions.md
docs/roadmap.md
```

Design documents may remain in a separate docs repository or be included under:

```text
docs/design/
```

If included publicly, design docs should be cleaned and aligned with implementation.

---

## 13. Community Strategy

### 13.1 Initial community goal

The initial goal is not to build a large community immediately.

The initial goal is to attract:

- early testers;
- AI automation developers;
- self-hosted developers;
- CAPI builders;
- people managing many small internal tools.

### 13.2 Community channels

Possible channels:

- GitHub Issues;
- GitHub Discussions;
- Discord or Telegram later;
- documentation site;
- blog posts;
- demo videos.

For v0.1, GitHub Issues and Discussions are enough.

### 13.3 Contribution types

Useful contributions:

- bug reports;
- Agent SDK feedback;
- UI improvements;
- documentation improvements;
- demo Capsule Services;
- new action examples;
- deployment examples;
- future Agent SDK language proposals.

---

## 14. Governance Strategy

CE repository governance can start simple.

Required files:

```text
CONTRIBUTING.md
CODE_OF_CONDUCT.md
SECURITY.md
LICENSE
ROADMAP.md
```

### 14.1 Maintainer model

Initial maintainer model:

```text
single-maintainer or small core team
```

This is acceptable for early stage.

### 14.2 Contribution acceptance

Contributions should be evaluated against:

- CE scope;
- design principles;
- security model;
- compatibility with EE/Cloud extension path;
- implementation quality;
- documentation quality.

### 14.3 Avoiding scope creep

Do not accept large enterprise features into CE v0.1 before the core loop is stable.

Examples to defer:

- full RBAC;
- SSO;
- metrics platform;
- Kubernetes operator;
- arbitrary command execution;
- plugin marketplace.

---

## 15. Issue and Roadmap Strategy

### 15.1 Issue labels

Recommended GitHub labels:

```text
type:bug
type:feature
type:docs
type:security
type:question
type:design
area:backend
area:ui
area:agent-sdk
area:docs
area:deployment
edition:ce
edition:ee
edition:cloud
priority:p0
priority:p1
priority:p2
status:needs-design
status:ready
status:blocked
```

### 15.2 Milestones

Recommended milestones:

```text
v0.1.0-alpha
v0.1.0
v0.2.0
CE stabilization
EE planning
Cloud planning
```

### 15.3 Public roadmap

The public roadmap should distinguish:

- implemented CE features;
- planned CE features;
- possible EE features;
- possible Cloud features;
- research ideas.

Avoid promising commercial timelines too early.

---

## 16. Branding and Naming

### 16.1 Product names

Recommended naming:

```text
xtrape-capsule       = domain / architecture concept
Opstage              = governance platform
Opstage CE           = open-source community edition
Opstage EE           = enterprise edition
Opstage Cloud        = SaaS edition
```

### 16.2 Tagline

Recommended tagline:

```text
A lightweight control plane for Capsule Services.
```

Alternative:

```text
Make lightweight services visible, operable, and auditable.
```

### 16.3 Avoid confusing messaging

Avoid describing CE as:

- microservice platform;
- Kubernetes alternative;
- configuration center;
- observability stack;
- remote shell dashboard.

These descriptions will create wrong expectations.

---

## 17. Commercialization Path

Open source CE should support future commercialization without damaging trust.

### 17.1 Recommended path

Recommended sequence:

```text
1. Build CE MVP.
2. Release CE publicly.
3. Collect real user feedback.
4. Improve CE stability and docs.
5. Identify enterprise needs.
6. Design EE around real enterprise requirements.
7. Design Cloud around hosted convenience and team collaboration.
```

### 17.2 Avoid premature monetization

Do not introduce hard commercial gates before CE proves value.

Do not make CE unusable just to force upgrades.

### 17.3 Commercial value areas

Likely commercial value areas:

- enterprise identity;
- large-scale deployment;
- compliance audit;
- observability integration;
- managed secrets;
- high availability;
- professional support;
- hosted Cloud convenience.

---

## 18. Risks

### 18.1 Risk: CE becomes too heavy

Mitigation:

- keep CE v0.1 focused on the vertical slice;
- defer EE/Cloud features;
- use SQLite and single-container deployment.

### 18.2 Risk: CE feels too weak

Mitigation:

- include complete Agent registration, command, action, and audit loop;
- include useful UI;
- include demo service;
- provide clear docs.

### 18.3 Risk: open source attracts cloud cloning

Mitigation:

- use brand, speed, commercial support, and Cloud service quality;
- consider license later if needed;
- keep advanced managed services commercial.

### 18.4 Risk: scope confusion

Mitigation:

- document CE/EE/Cloud boundaries;
- explain what CE is not;
- avoid marketing as config center or observability stack.

### 18.5 Risk: security concern

Mitigation:

- open source the core;
- document security model;
- avoid raw secrets;
- avoid shell execution;
- provide SECURITY.md.

---

## 19. Open Source Acceptance Criteria

The CE open-source strategy is successful when:

- the repository can be understood quickly by a new developer;
- the README explains the problem clearly;
- quick start works;
- demo service proves the core loop;
- CE feels useful without EE/Cloud;
- sensitive security boundaries are documented;
- the license is clear;
- contribution rules are clear;
- roadmap distinguishes CE, EE, and Cloud;
- users can trust the project enough to try it locally.

---

## 20. Summary

Opstage CE should be open source to build trust, validate the Capsule Service model, and create an adoption base.

The most important open-source rule is:

> CE must be a genuinely useful product, not a disabled preview of future commercial editions.
