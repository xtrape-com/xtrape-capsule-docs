# Capsule Manifest Specification

- Status: Draft
- Edition: Shared
- Priority: High

本文件属于 `xtrape-capsule` 文档集。`xtrape-capsule` 是面向轻服务 / Capsule Service 的领域体系；`xtrape-capsule-opstage` 是该体系下的统一运行态治理平台。

当前实现重点是 CE 开源社区版。EE 私有化商业版与 Cloud SaaS 版属于未来规划，CE 需要保留扩展点，但不应在早期版本实现其完整能力。

## Scope

本规范是 CE / EE / Cloud 共享的长期契约。CE 可以只实现最小子集，但命名、状态、接口和数据结构应尽量保持向后兼容。

## Compatibility Rule

- CE v0.x 可以标记实验字段。
- 稳定字段不应随意破坏。
- EE / Cloud 可以扩展能力，但不应反向污染 CE MVP。

# Capsule Manifest Specification

- Status: Draft
- Edition: Shared
- Priority: High
- Audience: backend developers, frontend developers, agent SDK developers, Capsule Service developers, AI coding agents

This document defines the **Capsule Manifest** specification for the `xtrape-capsule` domain.

A Capsule Manifest is the structured metadata document that describes a Capsule Service's identity, runtime, capabilities, resources, actions, configuration surface, and governance metadata.

The manifest is one of the primary contracts between Capsule Services, Agents, and Opstage.

---

## 1. Purpose

The Capsule Manifest Specification defines:

- how a Capsule Service identifies itself;
- how an Agent reports service metadata to Opstage;
- how Opstage stores and displays Capsule Service metadata;
- how actions, config items, capabilities, and resources are declared;
- what CE v0.1 must support;
- what fields are reserved for EE and Cloud expansion.

The manifest should be stable enough to serve as a cross-runtime contract for Node.js, Java, Python, Go, and future runtimes.

---

## 2. Manifest Role

A Capsule Manifest answers these questions:

- What is this Capsule Service?
- Which runtime does it use?
- Which Agent mode is used?
- Which capabilities does it provide?
- Which resources does it manage?
- Which actions can Opstage request?
- Which configuration items can Opstage view or manage?
- Which health dependencies are worth reporting?
- Which documentation or operational hints are available?

In CE v0.1, the manifest is primarily used for:

- service registration and display;
- service detail page;
- action listing;
- config visibility;
- health metadata;
- future compatibility.

---

## 3. Manifest Sources

A manifest may come from different sources depending on Agent mode.

### 3.1 Embedded Agent

In embedded Agent mode, the manifest is usually provided through the Agent SDK by the Capsule Service itself.

Example:

```ts
const agent = new CapsuleAgent({
  service: {
    code: 'demo-capsule-service',
    name: 'Demo Capsule Service',
    version: '0.1.0',
    runtime: 'nodejs',
  },
  capabilities: ['demo.echo'],
  actions: [...],
  configs: [...],
});
```

CE v0.1 focuses on this mode.

### 3.2 Management Endpoint

A Capsule Service may expose a management endpoint:

```http
GET /_capsule/manifest
```

This is useful for sidecar or external Agent modes.

### 3.3 External Agent Configuration

An external Agent may read manifest-like metadata from a target configuration file.

Example:

```yaml
kind: CapsuleService
code: capi-chatgpt
name: ChatGPT CAPI Service
runtime: nodejs
agentMode: external
```

This is a future target and is not required for CE v0.1.

---

## 4. Minimum CE v0.1 Manifest

CE v0.1 must support the following minimum manifest structure:

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
  "actions": [
    {
      "name": "runHealthCheck",
      "label": "Run Health Check",
      "dangerLevel": "LOW",
      "enabled": true
    },
    {
      "name": "echo",
      "label": "Echo",
      "dangerLevel": "LOW",
      "enabled": true
    }
  ],
  "configs": []
}
```

CE v0.1 may store the full manifest as JSON in the backend database.

---

## 5. Recommended Full Manifest

A future-ready manifest may look like this:

```json
{
  "kind": "CapsuleService",
  "schemaVersion": "1.0",
  "code": "capi-chatgpt",
  "name": "ChatGPT CAPI Service",
  "description": "A Capsule Service that wraps ChatGPT web capabilities.",
  "version": "0.1.0",
  "runtime": "nodejs",
  "agentMode": "embedded",
  "edition": "CE",
  "environment": "local",
  "owner": {
    "type": "user",
    "name": "local-admin"
  },
  "capabilities": [
    {
      "code": "chatgpt.chat",
      "name": "ChatGPT Chat",
      "description": "Send chat requests through ChatGPT web automation."
    }
  ],
  "resources": [
    {
      "name": "sessions",
      "label": "Sessions",
      "type": "session",
      "description": "Managed ChatGPT browser sessions."
    }
  ],
  "actions": [
    {
      "name": "runHealthCheck",
      "label": "Run Health Check",
      "description": "Run a manual health check.",
      "dangerLevel": "LOW",
      "enabled": true
    }
  ],
  "configs": [
    {
      "key": "chatgpt.maxConcurrentSessions",
      "label": "Max Concurrent Sessions",
      "type": "number",
      "defaultValue": 3,
      "editable": true,
      "sensitive": false
    }
  ],
  "health": {
    "dependencies": [
      {
        "name": "browser",
        "type": "local-runtime"
      }
    ]
  },
  "links": {
    "documentation": "https://example.com/docs/capi-chatgpt",
    "repository": "https://example.com/repo/capi-chatgpt"
  },
  "metadata": {
    "category": "capi",
    "tags": ["chatgpt", "browser", "automation"]
  }
}
```

CE v0.1 does not need to implement every field, but it should ignore unknown fields gracefully.

---

## 6. Top-Level Fields

### 6.1 `kind`

Resource kind.

Required.

Allowed value for this specification:

```text
CapsuleService
```

Future kinds may be introduced later, but CE v0.1 should only require `CapsuleService`.

### 6.2 `schemaVersion`

Manifest schema version.

Optional in CE v0.1.

Recommended default:

```text
1.0
```

If missing, CE v0.1 may treat it as experimental or default schema.

### 6.3 `code`

Stable technical identifier of the Capsule Service.

Required.

Rules:

- lowercase;
- kebab-case;
- unique within one Workspace;
- stable across service restarts;
- should not include environment-specific random suffixes.

Good examples:

```text
capi-chatgpt
account-pool
browser-session-worker
otp-mail-reader
proxy-health-checker
```

Bad examples:

```text
My Service
service_1
capsule-20260430-random
worker
```

### 6.4 `name`

Human-readable service name.

Required.

The `name` may change without changing service identity.

### 6.5 `description`

Optional description of the service.

Recommended for UI display and documentation.

### 6.6 `version`

Running service version.

Required in CE v0.1.

CE v0.1 may treat this as a simple string.

Examples:

```text
0.1.0
2026.04.30
local-dev
```

### 6.7 `runtime`

Implementation runtime.

Required.

Recommended values:

```text
nodejs
java
python
go
shell
other
```

CE v0.1 primarily supports:

```text
nodejs
```

### 6.8 `agentMode`

Agent integration mode.

Required.

Allowed values:

```text
embedded
sidecar
external
```

CE v0.1 implements only:

```text
embedded
```

However, the field should not be modeled as Node.js-only or embedded-only.

### 6.9 `edition`

Optional product edition context.

Allowed values:

```text
CE
EE
Cloud
```

CE v0.1 may ignore this field.

### 6.10 `environment`

Optional environment label.

Examples:

```text
local
dev
test
staging
prod
```

CE v0.1 may ignore this field or store it as metadata.

### 6.11 `owner`

Optional ownership metadata.

Example:

```json
{
  "type": "user",
  "name": "local-admin"
}
```

Future versions may support teams, organizations, or tenants.

### 6.12 `metadata`

Optional free-form object for additional metadata.

Examples:

```json
{
  "category": "capi",
  "tags": ["chatgpt", "automation"]
}
```

CE v0.1 may store this field in `manifestJson` without interpretation.

---

## 7. `capabilities`

`capabilities` describes named abilities provided by the Capsule Service.

CE v0.1 may accept either simple string array or object array.

### 7.1 Simple Form

```json
{
  "capabilities": ["demo.echo", "chatgpt.chat"]
}
```

### 7.2 Object Form

```json
{
  "capabilities": [
    {
      "code": "chatgpt.chat",
      "name": "ChatGPT Chat",
      "description": "Send chat requests through ChatGPT web automation."
    }
  ]
}
```

### 7.3 Capability Code Rules

Capability codes should be dot-separated and stable.

Examples:

```text
demo.echo
chatgpt.chat
gmail.readOtp
browser.openPage
account.refreshSession
```

Future EE/Cloud may use capabilities for:

- routing;
- quotas;
- entitlement;
- billing;
- marketplace listing;
- provider selection.

CE v0.1 should store capabilities but does not need advanced capability routing.

---

## 8. `resources`

`resources` describes types of resources managed by the Capsule Service.

Examples:

```json
{
  "resources": [
    {
      "name": "sessions",
      "label": "Sessions",
      "type": "session",
      "description": "Managed browser sessions."
    }
  ]
}
```

Recommended resource fields:

```text
name
label
type
description
schema
actions
metadata
```

Common resource types:

```text
account
session
job
queue
proxy
connector
agentRun
custom
```

CE v0.1 may store resources in the manifest only. It does not need to generate dynamic resource admin pages yet.

---

## 9. `actions`

`actions` declares predefined operations supported by the Capsule Service.

The Action model is defined in:

```text
02-specs/action-spec.md
```

Minimum action example:

```json
{
  "name": "runHealthCheck",
  "label": "Run Health Check",
  "dangerLevel": "LOW",
  "enabled": true
}
```

Rules:

- actions must be predefined;
- arbitrary shell commands must not be exposed in CE v0.1;
- every action execution should create a Command;
- every action result should create or update a CommandResult;
- every action should be auditable.

---

## 10. `configs`

`configs` declares manageable configuration metadata.

A config item describes how Opstage should display or manage a configuration value.

Minimum example:

```json
{
  "key": "demo.message",
  "label": "Demo Message",
  "type": "string",
  "defaultValue": "hello",
  "editable": true,
  "sensitive": false
}
```

Recommended fields:

```text
key
label
type
currentValue
defaultValue
editable
sensitive
options
validation
metadata
```

Recommended config types:

```text
string
number
boolean
select
json
secretRef
```

CE v0.1 may implement configuration visibility only.

Full configuration publishing, versioning, approval, and rollback are future capabilities.

---

## 11. `health`

`health` describes health-reporting metadata.

Example:

```json
{
  "health": {
    "dependencies": [
      {
        "name": "database",
        "type": "mysql"
      },
      {
        "name": "browser",
        "type": "local-runtime"
      }
    ]
  }
}
```

CE v0.1 may store this field without deep interpretation.

Actual health status should be reported through heartbeat or health report payloads.

---

## 12. `links`

`links` provides documentation and source references.

Example:

```json
{
  "links": {
    "documentation": "https://example.com/docs/service",
    "repository": "https://example.com/repo/service",
    "dashboard": "https://example.com/dashboard"
  }
}
```

CE v0.1 may display these links on the service detail page if available.

---

## 13. Manifest Reporting

In CE v0.1, the Node.js embedded Agent SDK should report the manifest to Backend during:

- initial registration;
- service report;
- periodic heartbeat if metadata changes;
- manual refresh if supported.

Recommended Agent API flow:

```text
Agent registers
    ↓
Agent receives Agent token
    ↓
Agent reports Capsule Service manifest
    ↓
Backend upserts CapsuleService record
    ↓
UI displays service metadata
```

---

## 14. Backend Storage

CE v0.1 may store the manifest in the `CapsuleService` table as JSON.

Recommended field:

```text
manifestJson
```

Backend may also extract these fields into normal columns:

```text
code
name
description
version
runtime
agentMode
status
lastReportedAt
```

Do not over-normalize all manifest fields in CE v0.1.

---

## 15. Validation Rules

CE v0.1 should validate at least:

- `kind` must be `CapsuleService`;
- `code` is required;
- `name` is required;
- `version` is required;
- `runtime` is required;
- `agentMode` is required;
- `actions` must be an array if present;
- `configs` must be an array if present;
- `resources` must be an array if present.

Recommended `code` pattern:

```text
^[a-z][a-z0-9-]*[a-z0-9]$
```

CE v0.1 should reject invalid required fields but ignore unknown optional fields.

---

## 16. Compatibility Rules

### 16.1 Additive Evolution

New optional fields may be added in future versions.

Older clients should ignore unknown fields where possible.

### 16.2 Stable Required Fields

The meaning of required fields should remain stable.

Do not change the semantics of:

```text
kind
code
name
version
runtime
agentMode
```

### 16.3 Experimental Fields

Experimental fields may be added under:

```text
metadata
```

or with explicit documentation.

### 16.4 CE / EE / Cloud Boundary

EE and Cloud may extend the manifest, but they should not require CE v0.1 to implement heavy fields such as billing, tenant isolation, SSO, or cluster metadata.

---

## 17. Security Rules

### 17.1 Do not store raw secrets in manifest

Manifest must not contain raw passwords, cookies, tokens, or credentials.

Use secret references instead.

Good:

```json
{
  "key": "chatgpt.accountSecret",
  "type": "secretRef",
  "currentValue": "agent-local://agent-001/secrets/chatgpt/account-001"
}
```

Bad:

```json
{
  "password": "plain-text-password"
}
```

### 17.2 Do not expose arbitrary shell actions

Manifest must not define generic shell execution actions for CE v0.1.

Bad:

```json
{
  "name": "runShell",
  "label": "Run Shell"
}
```

### 17.3 Dangerous actions must be marked

Actions with destructive impact should use:

```text
HIGH
CRITICAL
```

as `dangerLevel`.

---

## 18. CE v0.1 Requirements

CE v0.1 must support:

- manifest reporting from Node.js embedded Agent;
- minimum manifest validation;
- storing full manifest JSON;
- extracting service identity fields;
- displaying manifest data in UI;
- listing actions from manifest;
- listing config items from manifest;
- ignoring unknown fields;
- rejecting invalid required fields.

CE v0.1 does not need to support:

- manifest version migration;
- remote manifest endpoint discovery;
- dynamic resource admin generation;
- config publishing workflow;
- manifest approval workflow;
- manifest marketplace metadata;
- tenant-specific manifest overlays.

---

## 19. Example CE v0.1 Demo Manifest

```json
{
  "kind": "CapsuleService",
  "schemaVersion": "1.0",
  "code": "demo-capsule-service",
  "name": "Demo Capsule Service",
  "description": "A demo Capsule Service used to validate CE v0.1 Agent integration.",
  "version": "0.1.0",
  "runtime": "nodejs",
  "agentMode": "embedded",
  "capabilities": ["demo.echo"],
  "resources": [],
  "actions": [
    {
      "name": "runHealthCheck",
      "label": "Run Health Check",
      "description": "Run a manual health check.",
      "dangerLevel": "LOW",
      "enabled": true
    },
    {
      "name": "echo",
      "label": "Echo",
      "description": "Echo a message to verify command roundtrip.",
      "dangerLevel": "LOW",
      "enabled": true,
      "inputSchema": {
        "type": "object",
        "properties": {
          "message": {
            "type": "string",
            "title": "Message"
          }
        }
      }
    }
  ],
  "configs": [
    {
      "key": "demo.message",
      "label": "Demo Message",
      "type": "string",
      "defaultValue": "hello capsule",
      "editable": true,
      "sensitive": false
    }
  ],
  "metadata": {
    "category": "demo",
    "tags": ["ce", "demo", "nodejs"]
  }
}
```

---

## 20. Anti-Patterns

Avoid these manifest anti-patterns.

### 20.1 Environment-random service code

Bad:

```text
capi-chatgpt-local-20260430-random
```

The service code should be stable.

### 20.2 Raw secrets in manifest

Do not include passwords, cookies, or tokens.

### 20.3 Arbitrary shell action

Do not define `runShell`, `exec`, `bash`, or similar actions in CE v0.1.

### 20.4 Overloaded manifest

Do not put large runtime state or logs into manifest.

Manifest is metadata, not a runtime event stream.

### 20.5 Required EE/Cloud-only fields

Do not require tenant, billing, cluster, or SSO fields for CE v0.1 manifests.

---

## 21. Summary

The Capsule Manifest is the primary metadata contract for Capsule Services.

CE v0.1 should implement a small but stable manifest subset:

```text
kind
code
name
version
runtime
agentMode
capabilities
actions
configs
resources
metadata
```

The manifest should remain lightweight, secure, and forward-compatible.