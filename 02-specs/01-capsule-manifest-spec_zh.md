---
status: draft
audience: architects
stability: unstable
last_reviewed: 2026-05-05
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 01-capsule-manifest-spec.md
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

# Capsule Manifest 规范

- Status: 规范
- Edition: 共享
- Priority: 高
- Audience: backend developers, frontend developers, agent SDK developers, Capsule Service（胶囊服务） developers, AI coding agents

> **Precedence rule**: When this document and `09-contracts/openapi/opstage-ce-v0.1.yaml` `CapsuleManifest` schema disagree, the OpenAPI contract wins for CE（社区版） v0.1.

This document 定义 the **Capsule Manifest** specification for the `xtrape-capsule` domain.

A Capsule Manifest is the structured metadata document that 描述 a Capsule Service（胶囊服务）'s identity, runtime,
capabilities, resources, actions, configuration surface, and governance metadata.

The manifest is one of the primary contracts between Capsule Services, Agents, and Opstage（运维舞台）.

---

## 1. Purpose

The Capsule Manifest 规范 定义:

- how a Capsule Service（胶囊服务） identifies itself;
- how an Agent（代理） reports service metadata to Opstage（运维舞台）;
- how Opstage（运维舞台） stores and displays Capsule Service（胶囊服务） metadata;
- how actions, config items, capabilities, and resources are declared;
- what CE（社区版） v0.1 must support;
- what fields are reserved for EE（企业版） and Cloud（云版） expansion.

The manifest should be stable enough to serve as a cross-runtime contract for Node.js, Java, Python, Go, and future runtimes.

---

## 2. Manifest Role

A Capsule Manifest answers these questions:

- What is this Capsule Service（胶囊服务）?
- Which runtime does it use?
- Which Agent（代理） mode is used?
- Which capabilities does it provide?
- Which resources does it manage?
- Which actions can Opstage（运维舞台） request?
- Which configuration items can Opstage（运维舞台） view or manage?
- Which health dependencies are worth reporting?
- Which documentation or operational hints are available?

In CE（社区版） v0.1, the manifest is primarily used for:

- service registration and display;
- service detail page;
- action listing;
- config visibility;
- health metadata;
- future compatibility.

---

## 3. Manifest Sources

A manifest may come from different sources depending on Agent（代理） mode.

### 3.1 Embedded Agent（代理）

In embedded Agent（代理） mode, the manifest is usually provided through the Agent（代理） SDK by the Capsule Service（胶囊服务） itself.

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

CE（社区版） v0.1 focuses on this mode.

### 3.2 Management Endpoint

A Capsule Service（胶囊服务） may expose a management endpoint:

```http
GET /_capsule/manifest
```

This is useful for sidecar or external Agent（代理） modes.

### 3.3 External Agent（代理） 配置

An external Agent（代理） may read manifest-like metadata from a target configuration file.

Example:

```yaml
kind: CapsuleService
code: integration-worker
name: Example integration service
runtime: nodejs
agentMode: external
```

This is a future target and is not required for CE（社区版） v0.1.

---

## 4. Minimum CE（社区版） v0.1 Manifest

CE（社区版） v0.1 must support the following minimum manifest structure:

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

CE（社区版） v0.1 may store the full manifest as JSON in the backend database.

---

## 5. Recommended Full Manifest

A future-ready manifest may look like this:

```json
{
  "kind": "CapsuleService",
  "schemaVersion": "1.0",
  "code": "integration-worker",
  "name": "Example integration service",
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
    "documentation": "https://example.com/docs/integration-worker",
    "repository": "https://example.com/repo/integration-worker"
  },
  "metadata": {
    "category": "integration",
    "tags": ["chatgpt", "browser", "automation"]
  }
}
```

CE（社区版） v0.1 does not need to implement every field, but it should ignore unknown fields gracefully.

---

## 6. Top-Level Fields

### 6.1 `kind`

Resource kind.

Required.

Allowed value for this specification:

```text
CapsuleService
```

Future kinds may be introduced later, but CE（社区版） v0.1 should only require `CapsuleService`.

### 6.2 `schemaVersion`

Manifest schema version.

Optional in CE（社区版） v0.1.

Recommended default:

```text
1.0
```

If missing, CE（社区版） v0.1 may treat it as experimental or default schema.

### 6.3 `code`

Stable technical identifier of the Capsule Service（胶囊服务）.

Required.

Rules:

- lowercase;
- kebab-case;
- unique within one Workspace;
- stable across service restarts;
- should not include environment-specific random suffixes.

Good examples:

```text
integration-worker
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

Required in CE（社区版） v0.1.

CE（社区版） v0.1 may treat this as a simple string.

Examples:

```text
0.1.0
2026.04.30
local-dev
```

### 6.7 `runtime`

实现 runtime.

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

CE（社区版） v0.1 primarily 支持:

```text
nodejs
```

### 6.8 `agentMode`

Agent（代理） integration mode.

Required.

Allowed values:

```text
embedded
sidecar
external
```

CE（社区版） v0.1 implements only:

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

CE（社区版） v0.1 may ignore this field.

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

CE（社区版） v0.1 may ignore this field or store it as metadata.

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
  "category": "integration",
  "tags": ["chatgpt", "automation"]
}
```

CE（社区版） v0.1 may store this field in `manifestJson` without interpretation.

---

## 7. `capabilities`

`capabilities` 描述 named abilities provided by the Capsule Service（胶囊服务）.

CE（社区版） v0.1 may accept either simple string array or object array.

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

Future EE（企业版）/Cloud（云版） may use capabilities for:

- routing;
- quotas;
- entitlement;
- billing;
- marketplace listing;
- provider selection.

CE（社区版） v0.1 should store capabilities but does not need advanced capability routing.

---

## 8. `resources`

`resources` 描述 types of resources managed by the Capsule Service（胶囊服务）.

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

CE（社区版） v0.1 may store resources in the manifest only. It does not need to generate dynamic resource admin pages yet.

---

## 9. `actions`

`actions` declares predefined operations supported by the Capsule Service（胶囊服务）.

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
- arbitrary shell commands must not be exposed in CE（社区版） v0.1;
- every action execution should create a Command;
- every action result should create or update a CommandResult;
- every action should be auditable.

---

## 10. `configs`

`configs` declares manageable configuration metadata.

A config item 描述 how Opstage（运维舞台） should display or manage a configuration value.

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

CE（社区版） v0.1 may implement configuration visibility only.

Full configuration publishing, versioning, approval, and rollback are future capabilities.

---

## 11. `health`

`health` 描述 health-reporting metadata.

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

CE（社区版） v0.1 may store this field without deep interpretation.

Actual health status should be reported through heartbeat or health report payloads.

---

## 12. `links`

`links` 提供 documentation and source references.

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

CE（社区版） v0.1 may display these links on the service detail page if available.

---

## 13. Manifest Reporting

In CE（社区版） v0.1, the Node.js embedded Agent（代理） SDK should report the manifest to Backend during:

- initial registration;
- service report;
- periodic heartbeat if metadata changes;
- manual refresh if supported.

Recommended Agent（代理） API flow:

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

CE（社区版） v0.1 may store the manifest in the `CapsuleService` table as JSON.

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

Do not over-normalize all manifest fields in CE（社区版） v0.1.

---

## 15. Validation Rules

CE（社区版） v0.1 should validate at least:

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

CE（社区版） v0.1 should reject invalid required fields but ignore unknown optional fields.

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

### 16.4 CE（社区版） / EE（企业版） / Cloud（云版） Boundary

EE（企业版） and Cloud（云版） may extend the manifest, but they should not require CE（社区版） v0.1 to implement heavy fields such as billing, tenant isolation, SSO, or cluster metadata.

---

## 17. 安全 Rules

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

Manifest must not define generic shell execution actions for CE（社区版） v0.1.

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

## 18. CE（社区版） v0.1 Requirements

CE（社区版） v0.1 must support:

- manifest reporting from Node.js embedded Agent（代理）;
- minimum manifest validation;
- storing full manifest JSON;
- extracting service identity fields;
- displaying manifest data in UI;
- listing actions from manifest;
- listing config items from manifest;
- ignoring unknown fields;
- rejecting invalid required fields.

CE（社区版） v0.1 does not need to support:

- manifest version migration;
- remote manifest endpoint discovery;
- dynamic resource admin generation;
- config publishing workflow;
- manifest approval workflow;
- manifest marketplace metadata;
- tenant-specific manifest overlays.

---

## 19. Example CE（社区版） v0.1 Demo Manifest

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
integration-worker-local-20260430-random
```

The service code should be stable.

### 20.2 Raw secrets in manifest

Do not include passwords, cookies, or tokens.

### 20.3 Arbitrary shell action

Do not define `runShell`, `exec`, `bash`, or similar actions in CE（社区版） v0.1.

### 20.4 Overloaded manifest

Do not put large runtime state or logs into manifest.

Manifest is metadata, not a runtime event stream.

### 20.5 Required EE（企业版）/Cloud（云版）-only fields

Do not require tenant, billing, cluster, or SSO fields for CE（社区版） v0.1 manifests.

---

## 21. Summary

The Capsule Manifest is the primary metadata contract for Capsule Services.

CE（社区版） v0.1 should implement a small but stable manifest subset:

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
