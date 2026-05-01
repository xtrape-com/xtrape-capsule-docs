<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 00-ce-positioning.md
翻译状态 / Translation Status: 已翻译 / Translated
生成时间 / Generated: 2026-05-01 09:28:53
================================================================================
注意 / Notes:
- 技术术语如 Capsule Service、Agent、Opstage 等保留英文或采用中英对照
- 代码块中的内容不翻译
- 文件路径和 URL 不翻译
- 保持原有的 Markdown 格式结构
================================================================================
-->

# CE（社区版） Positioning

- Status: 实现 Target
- Edition: CE（社区版）
- Priority: Current
- Audience: product designers, architects, developers, AI coding agents

This document 定义 the product positioning of **Opstage（运维舞台） CE（社区版） / Community 版本**.

CE（社区版） is the first implementation target of `xtrape-capsule`. It should be a real usable open-source product, not a weakened placeholder for EE（企业版） or Cloud（云版）.

---

## 1. Positioning Statement

Opstage（运维舞台） CE（社区版） is:

> A lightweight, self-hosted, open-source runtime governance platform for Capsule Services.

It helps developers and small teams manage many lightweight services through an Agent（代理）-based control plane.

CE（社区版） focuses on the first practical problem:

> Small services are easy to create, but hard to remember, observe, configure, audit, and operate over time.

---

## 2. Target Users

CE（社区版） is designed for:

- individual developers;
- small teams;
- open-source users;
- self-hosted users;
- AI automation developers;
- CAPI service developers;
- internal tooling teams;
- early adopters of the Capsule Service（胶囊服务） model.

CE（社区版） should be useful even without enterprise contracts or commercial support.

---

## 3. Target Scenarios

Typical CE（社区版） scenarios include:

### 3.1 Local development governance

A developer runs several local Capsule Services and wants a simple UI to see status, health, configs, actions, and audit records.

### 3.2 Small self-hosted deployment

A small team runs Opstage（运维舞台） CE（社区版） on a private server to manage internal tools, workers, connectors, and CAPI services.

### 3.3 CAPI service governance

A team builds multiple CAPI services for platforms such as ChatGPT, Gemini, Gmail, Telegram, or other web capabilities, and needs a shared operational console.

### 3.4 Account and session service visibility

A service manages accounts, sessions, cookies, browser contexts, or OAuth tokens. CE（社区版） 提供 visibility and safe predefined operations without exposing raw secrets.

### 3.5 Worker and automation supervision

Small background workers need heartbeat, health status, basic actions, and audit records.

---

## 4. Core Value Proposition

CE（社区版） 提供 value through five core capabilities.

### 4.1 Remember

CE（社区版） gives every Capsule Service（胶囊服务） a stable identity and visible entry in Opstage（运维舞台）.

Operators can answer:

- which services exist;
- which Agent（代理） reported them;
- when they were last seen;
- which version is running.

### 4.2 Observe

CE（社区版） shows basic status and health information.

Operators can see:

- Agent（代理） online/offline state;
- Capsule Service（胶囊服务） effective status;
- health status;
- stale state;
- last heartbeat time;
- last reported time.

### 4.3 Configure

CE（社区版） 提供 configuration visibility.

Operators can see config metadata, value types, defaults, editability, and sensitive references.

CE（社区版） v0.1 is not a full configuration center.

### 4.4 Operate

CE（社区版） allows safe predefined actions through Commands.

Operators can trigger actions such as:

```text
runHealthCheck
echo
reloadConfig
refreshSession
```

Only predefined actions are allowed. Arbitrary shell execution is not part of CE（社区版） v0.1.

### 4.5 Audit

CE（社区版） records important operations so that users can trace what happened.

Examples:

- Agent（代理） registered;
- service reported;
- command created;
- action completed;
- command failed.

---

## 5. Why CE（社区版） Should Be Open Source

CE（社区版） should be open source because Opstage（运维舞台） is a governance platform.

It may eventually touch sensitive operational metadata such as:

- account status;
- session state;
- token references;
- health reports;
- action history;
- audit events;
- service topology.

Open source improves trust for self-hosted users.

It also helps establish the Capsule Service（胶囊服务） model as a reusable concept and makes the Agent（代理） SDK easier to adopt.

---

## 6. CE（社区版） vs Traditional Tools

CE（社区版） is different from several existing tool categories.

### 6.1 CE（社区版） vs configuration center

Traditional configuration centers focus on configuration values.

CE（社区版） focuses on runtime governance:

- Agent（代理） registration;
- service status;
- health;
- actions;
- commands;
- audit;
- config visibility.

CE（社区版） v0.1 should not attempt to replace Nacos or Apollo.

### 6.2 CE（社区版） vs observability platform

Observability platforms focus on logs, metrics, and traces.

CE（社区版） focuses on basic governance visibility and operation.

CE（社区版） v0.1 should not attempt to replace Prometheus, Grafana, Loki, or ELK.

### 6.3 CE（社区版） vs microservice platform

Microservice platforms focus on large service ecosystems, service discovery, gateways, meshes, and distributed infrastructure.

CE（社区版） focuses on lightweight Capsule Services and Agent（代理）-based governance.

CE（社区版） v0.1 should not become a Kubernetes or Spring Cloud（云版） replacement.

### 6.4 CE（社区版） vs admin panel

A normal admin panel is usually built for one business system.

CE（社区版） is a shared governance console for many Capsule Services.

---

## 7. CE（社区版） Product Boundaries

CE（社区版） should be strong enough to be useful, but small enough to remain lightweight.

### 7.1 CE（社区版） should include

- self-hosted deployment;
- SQLite default storage;
- local admin login;
- Agent（代理） registration;
- Node.js embedded Agent（代理） SDK;
- Capsule Service（胶囊服务） list;
- Agent（代理） list;
- health visibility;
- config visibility;
- predefined actions;
- command polling;
- command result tracking;
- basic audit logs;
- demo Capsule Service（胶囊服务）.

### 7.2 CE（社区版） should not include in v0.1

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
- sidecar Agent（代理）;
- external Agent（代理）;
- Java or Python Agent（代理） SDK;
- arbitrary shell execution.

---

## 8. CE（社区版） and Future Editions

CE（社区版） is the foundation for future EE（企业版） and Cloud（云版） editions.

### 8.1 Relationship with EE（企业版）

EE（企业版） should extend CE（社区版） for enterprise private deployment.

Future EE（企业版） may include:

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

### 8.2 Relationship with Cloud（云版）

Cloud（云版） should extend the same model into a hosted SaaS service.

Future Cloud（云版） may include:

- multi-tenant workspaces;
- subscription billing;
- hosted backend;
- outbound Agent（代理） connectivity;
- cloud-side metadata;
- customer-side secret boundary;
- managed alerting and reporting.

### 8.3 CE（社区版） extension principle

CE（社区版） should reserve extension points for EE（企业版） and Cloud（云版）, but it must not implement their full complexity in v0.1.

The guiding rule is:

> CE（社区版） should be small but not short-sighted.

---

## 9. Product Tone

CE（社区版） should feel like:

- lightweight;
- practical;
- transparent;
- self-hosted;
- developer-friendly;
- safe by default;
- easy to start;
- easy to understand;
- extensible without being heavy.

CE（社区版） should not feel like:

- an enterprise platform with most features disabled;
- a SaaS trial disguised as open source;
- a heavy microservice framework;
- a configuration center clone;
- a remote shell dashboard.

---

## 10. Messaging

Recommended short description:

> Opstage（运维舞台） CE（社区版） is a lightweight, self-hosted, open-source control plane for Capsule Services.

Recommended longer description:

> Opstage（运维舞台） CE（社区版） helps developers and small teams register, observe, configure, operate, and audit lightweight Capsule Services through an Agent（代理）-based governance model.

Repository description:

```text
A lightweight, self-hosted, open-source control plane for Capsule Services.
```

---

## 11. Success Criteria

CE（社区版） positioning is successful if users understand that:

- Capsule Service（胶囊服务） is lighter than a traditional microservice;
- Opstage（运维舞台） CE（社区版） is not a full enterprise operations suite;
- CE（社区版） is useful for real small-team self-hosted governance;
- Agent（代理） registration is the core onboarding mechanism;
- Node.js embedded Agent（代理） SDK is the first integration path;
- SQLite and Docker make the first deployment simple;
- EE（企业版） and Cloud（云版） are future extensions, not CE（社区版） v0.1 requirements.

---

## 12. Summary

Opstage（运维舞台） CE（社区版） should establish the first usable product shape of `xtrape-capsule`.

It should prove that small services can remain lightweight and independent while becoming visible, operable, and auditable through Opstage（运维舞台） and Agents.

The most important product rule is:

> CE（社区版） must be genuinely useful as an open-source tool, while keeping a clean path for EE（企业版） and Cloud（云版） evolution.
