<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: README.md
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

# Capsule Domain Documents

- Status: 实施指南
- Edition: 共享
- Priority: 高
- Audience: architects, product designers, backend developers, agent SDK developers, AI coding agents

This directory 定义 the core `xtrape-capsule` domain concepts.

Read these documents before implementing Opstage（运维舞台）, Agents, runtime SDKs, or edition-specific features. They define the shared vocabulary used by the rest of the documentation set.

---

## 1. Purpose of This Directory

The purpose of this directory is to define:

- what a Capsule Service（胶囊服务） is;
- why Capsule Service（胶囊服务） is different from a traditional microservice;
- which domain objects are shared across CE（社区版）, EE（企业版）, and Cloud（云版）;
- which design principles should guide implementation;
- how Opstage（运维舞台） and Agents relate to the Capsule domain.

These documents are conceptual foundations, not edition-specific implementation plans.

---

## 2. Recommended Reading Order

Read the documents in this order:

```text
01-capsule/README.md
01-capsule/00-overview.md
01-capsule/01-capsule-service-concept.md
01-capsule/02-capsule-vs-microservice.md
01-capsule/03-domain-model.md
01-capsule/04-design-principles.md
```

---

## 3. Document List

### 3.1 `00-overview.md`

Introduces the `xtrape-capsule` domain and 解释 why lightweight, Agent（代理）-governed services are needed.

### 3.2 `01-capsule-service-concept.md`

Defines Capsule Service（胶囊服务） as the core governable service unit.

### 3.3 `02-capsule-vs-microservice.md`

Compares Capsule Service（胶囊服务） with traditional microservices and clarifies why Capsule Services are better suited for lightweight capability units, automation workers, account/session services, and AI-era integration services.

### 3.4 `03-domain-model.md`

Defines core domain objects such as CapsuleService, Agent（代理）, Manifest, HealthReport, ConfigItem, ActionDefinition, Command, CommandResult, and AuditEvent.

### 3.5 `04-design-principles.md`

Defines the design principles that keep the model lightweight, extensible, Agent（代理）-governed, predefined-action-based, and safe by default.

---

## 4. Current 实现 Relevance

For CE（社区版） v0.1, these concepts should be implemented as a minimal vertical slice:

```text
CapsuleService
Agent
Manifest
HealthReport
ConfigItem
ActionDefinition
Command
CommandResult
AuditEvent
secretRef boundary
```

CE（社区版） v0.1 should not implement every future capability described in conceptual documents.

The rule is:

```text
Implement the smallest complete governance loop first.
```

---

## 5. Summary

This directory establishes the shared vocabulary for the whole documentation set.

The most important Capsule domain rule is:

> A Capsule Service（胶囊服务） is a lightweight, independently runnable service unit that becomes governable through an authenticated Agent（代理）, predefined metadata, predefined actions, Commands, CommandResults, and AuditEvents.
