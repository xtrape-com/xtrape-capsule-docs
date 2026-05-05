# CE Positioning

- Status: Implementation Target
- Edition: CE
- Priority: Current
- Audience: product designers, architects, developers, AI coding agents

This document defines the product positioning of **Opstage CE / Community Edition**.

CE is the first implementation target of `xtrape-capsule`. It should be a real usable open-source product, not a weakened placeholder for EE or Cloud.

---

## 1. Positioning Statement

Opstage CE is:

> A lightweight, self-hosted, open-source runtime governance platform for Capsule Services.

It helps developers and small teams manage many lightweight services through an Agent-based control plane.

CE focuses on the first practical problem:

> Small services are easy to create, but hard to remember, observe, configure, audit, and operate over time.

---

## 2. Target Users

CE is designed for:

- individual developers;
- small teams;
- open-source users;
- self-hosted users;
- AI automation developers;
- Integration service developers;
- internal tooling teams;
- early adopters of the Capsule Service model.

CE should be useful even without enterprise contracts or commercial support.

---

## 3. Target Scenarios

Typical CE scenarios include:

### 3.1 Local development governance

A developer runs several local Capsule Services and wants a simple UI to see status, health, configs, actions, and audit records.

### 3.2 Small self-hosted deployment

A small team runs Opstage CE on a private server to manage internal tools, workers, connectors, and integration services.

### 3.3 Lightweight service governance

A team builds multiple integration services for platforms such as ChatGPT, Gemini, Gmail, Telegram, or other web capabilities, and needs a shared operational console.

### 3.4 Account and session service visibility

A service manages accounts, sessions, cookies, browser contexts, or OAuth tokens. CE provides visibility and safe predefined operations without exposing raw secrets.

### 3.5 Worker and automation supervision

Small background workers need heartbeat, health status, basic actions, and audit records.

---

## 4. Core Value Proposition

CE provides value through five core capabilities.

### 4.1 Remember

CE gives every Capsule Service a stable identity and visible entry in Opstage.

Operators can answer:

- which services exist;
- which Agent reported them;
- when they were last seen;
- which version is running.

### 4.2 Observe

CE shows basic status and health information.

Operators can see:

- Agent online/offline state;
- Capsule Service effective status;
- health status;
- stale state;
- last heartbeat time;
- last reported time.

### 4.3 Configure

CE provides configuration visibility.

Operators can see config metadata, value types, defaults, editability, and sensitive references.

CE v0.1 is not a full configuration center.

### 4.4 Operate

CE allows safe predefined actions through Commands.

Operators can trigger actions such as:

```text
runHealthCheck
echo
reloadConfig
refreshSession
```

Only predefined actions are allowed. Arbitrary shell execution is not part of CE v0.1.

### 4.5 Audit

CE records important operations so that users can trace what happened.

Examples:

- Agent registered;
- service reported;
- command created;
- action completed;
- command failed.

---

## 5. Why CE Should Be Open Source

CE should be open source because Opstage is a governance platform.

It may eventually touch sensitive operational metadata such as:

- account status;
- session state;
- token references;
- health reports;
- action history;
- audit events;
- service topology.

Open source improves trust for self-hosted users.

It also helps establish the Capsule Service model as a reusable concept and makes the Agent SDK easier to adopt.

---

## 6. CE vs Traditional Tools

CE is different from several existing tool categories.

### 6.1 CE vs configuration center

Traditional configuration centers focus on configuration values.

CE focuses on runtime governance:

- Agent registration;
- service status;
- health;
- actions;
- commands;
- audit;
- config visibility.

CE v0.1 should not attempt to replace Nacos or Apollo.

### 6.2 CE vs observability platform

Observability platforms focus on logs, metrics, and traces.

CE focuses on basic governance visibility and operation.

CE v0.1 should not attempt to replace Prometheus, Grafana, Loki, or ELK.

### 6.3 CE vs microservice platform

Microservice platforms focus on large service ecosystems, service discovery, gateways, meshes, and distributed infrastructure.

CE focuses on lightweight Capsule Services and Agent-based governance.

CE v0.1 should not become a Kubernetes or Spring Cloud replacement.

### 6.4 CE vs admin panel

A normal admin panel is usually built for one business system.

CE is a shared governance console for many Capsule Services.

---

## 7. CE Product Boundaries

CE should be strong enough to be useful, but small enough to remain lightweight.

### 7.1 CE should include

- self-hosted deployment;
- SQLite default storage;
- local admin login;
- Agent registration;
- Node.js embedded Agent SDK;
- Capsule Service list;
- Agent list;
- health visibility;
- config visibility;
- predefined actions;
- command polling;
- command result tracking;
- basic audit logs;
- demo Capsule Service.

### 7.2 CE should not include in v0.1

- enterprise RBAC;
- SSO;
- multi-tenancy;
- billing;
- Kubernetes deployment requirement;
- high availability;
- centralized logs;
- metrics dashboard;
- alert rules;
- config publishing workflow;
- secret vault integration;
- sidecar Agent;
- external Agent;
- Java or Python Agent SDK;
- arbitrary shell execution.

---

## 8. CE and Future Editions

CE is the foundation for future EE and Cloud editions.

### 8.1 Relationship with EE

EE should extend CE for enterprise private deployment.

Future EE may include:

- MySQL / PostgreSQL official support;
- cluster deployment;
- high availability;
- RBAC;
- SSO / OIDC / LDAP;
- centralized logs;
- metrics dashboards;
- alert rules;
- secret vault integration;
- commercial installer;
- enterprise support.

### 8.2 Relationship with Cloud

Cloud should extend the same model into a hosted SaaS service.

Future Cloud may include:

- multi-tenant workspaces;
- subscription billing;
- hosted backend;
- outbound Agent connectivity;
- cloud-side metadata;
- customer-side secret boundary;
- managed alerting and reporting.

### 8.3 CE extension principle

CE should reserve extension points for EE and Cloud, but it must not implement their full complexity in v0.1.

The guiding rule is:

> CE should be small but not short-sighted.

---

## 9. Product Tone

CE should feel like:

- lightweight;
- practical;
- transparent;
- self-hosted;
- developer-friendly;
- safe by default;
- easy to start;
- easy to understand;
- extensible without being heavy.

CE should not feel like:

- an enterprise platform with most features disabled;
- a SaaS trial disguised as open source;
- a heavy microservice framework;
- a configuration center clone;
- a remote shell dashboard.

---

## 10. Messaging

Recommended short description:

> Opstage CE is a lightweight, self-hosted, open-source control plane for Capsule Services.

Recommended longer description:

> Opstage CE helps developers and small teams register, observe, configure, operate, and audit lightweight Capsule Services through an Agent-based governance model.

Repository description:

```text
A lightweight, self-hosted, open-source control plane for Capsule Services.
```

---

## 11. Success Criteria

CE positioning is successful if users understand that:

- Capsule Service is lighter than a traditional microservice;
- Opstage CE is not a full enterprise operations suite;
- CE is useful for real small-team self-hosted governance;
- Agent registration is the core onboarding mechanism;
- Node.js embedded Agent SDK is the first integration path;
- SQLite and Docker make the first deployment simple;
- EE and Cloud are future extensions, not CE v0.1 requirements.

---

## 12. Summary

Opstage CE should establish the first usable product shape of `xtrape-capsule`.

It should prove that small services can remain lightweight and independent while becoming visible, operable, and auditable through Opstage and Agents.

The most important product rule is:

> CE must be genuinely useful as an open-source tool, while keeping a clean path for EE and Cloud evolution.
