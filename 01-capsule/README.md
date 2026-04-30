# Capsule Domain Documents

- Status: Implementation Guidance
- Edition: Shared
- Priority: High
- Audience: architects, product designers, backend developers, agent SDK developers, AI coding agents

This directory defines the core `xtrape-capsule` domain concepts.

Read these documents before implementing Opstage, Agents, runtime SDKs, or edition-specific features. They define the shared vocabulary used by the rest of the documentation set.

---

## 1. Purpose of This Directory

The purpose of this directory is to define:

- what a Capsule Service is;
- why Capsule Service is different from a traditional microservice;
- which domain objects are shared across CE, EE, and Cloud;
- which design principles should guide implementation;
- how Opstage and Agents relate to the Capsule domain.

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

Introduces the `xtrape-capsule` domain and explains why lightweight, Agent-governed services are needed.

### 3.2 `01-capsule-service-concept.md`

Defines Capsule Service as the core governable service unit.

### 3.3 `02-capsule-vs-microservice.md`

Compares Capsule Service with traditional microservices and clarifies why Capsule Services are better suited for lightweight capability units, automation workers, account/session services, and AI-era integration services.

### 3.4 `03-domain-model.md`

Defines core domain objects such as CapsuleService, Agent, Manifest, HealthReport, ConfigItem, ActionDefinition, Command, CommandResult, and AuditEvent.

### 3.5 `04-design-principles.md`

Defines the design principles that keep the model lightweight, extensible, Agent-governed, predefined-action-based, and safe by default.

---

## 4. Current Implementation Relevance

For CE v0.1, these concepts should be implemented as a minimal vertical slice:

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

CE v0.1 should not implement every future capability described in conceptual documents.

The rule is:

```text
Implement the smallest complete governance loop first.
```

---

## 5. Summary

This directory establishes the shared vocabulary for the whole documentation set.

The most important Capsule domain rule is:

> A Capsule Service is a lightweight, independently runnable service unit that becomes governable through an authenticated Agent, predefined metadata, predefined actions, Commands, CommandResults, and AuditEvents.
