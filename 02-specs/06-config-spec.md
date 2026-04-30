# Config Specification

- Status: Specification
- Edition: Shared
- Priority: High
- Audience: backend developers, frontend developers, agent SDK developers, Capsule Service developers, AI coding agents

This document defines the **Config** specification for the `xtrape-capsule` domain.

Config describes the manageable configuration metadata of a Capsule Service.

In CE v0.1, Config should focus on **visibility** and **safe metadata reporting**. Full configuration publishing, approval, versioning, rollback, and environment promotion are future capabilities.

---

## 1. Purpose

The Config Specification defines:

- how Capsule Services describe configuration items;
- how Agents report configuration metadata to Opstage;
- how Backend stores and exposes configuration metadata;
- how UI displays configuration items;
- how sensitive values should be handled;
- what CE v0.1 must implement;
- what EE and Cloud may extend later.

Config in `xtrape-capsule` is not intended to be a full replacement for traditional configuration centers in CE v0.1.

It is a governance surface that lets operators understand and, in future versions, safely manage Capsule Service configuration.

---

## 2. Core Concept

A **ConfigItem** describes a configuration value or setting of a Capsule Service.

A ConfigItem is metadata-rich. It should describe not only the raw value, but also:

- key;
- display label;
- value type;
- current value if safe to expose;
- default value;
- editability;
- sensitivity;
- validation hints;
- options;
- description;
- source;
- metadata.

The key idea is:

> Opstage should understand what configuration exists and how it should be displayed or managed, without forcing every Capsule Service into a heavy configuration-center model.

---

## 3. CE v0.1 Scope

CE v0.1 should implement **configuration visibility**.

CE v0.1 should support:

- config metadata reported by Node.js embedded Agent SDK;
- config items stored by Backend;
- config list displayed in UI;
- sensitive values hidden or masked;
- config metadata stored as JSON where needed;
- read-only or metadata-only config management.

CE v0.1 does not need to support:

- remote config publishing;
- config versioning;
- config rollback;
- config approval workflow;
- config environment promotion;
- distributed config synchronization;
- config encryption management;
- dynamic reload orchestration;
- feature flag system.

---

## 4. ConfigItem Structure

### 4.1 Minimum CE v0.1 ConfigItem

```json
{
  "key": "demo.message",
  "label": "Demo Message",
  "type": "string",
  "defaultValue": "hello capsule",
  "editable": true,
  "sensitive": false
}
```

### 4.2 Recommended ConfigItem

```json
{
  "key": "chatgpt.maxConcurrentSessions",
  "label": "Max Concurrent Sessions",
  "description": "Maximum number of concurrent browser sessions allowed for this service.",
  "type": "number",
  "currentValue": 3,
  "defaultValue": 3,
  "editable": true,
  "sensitive": false,
  "required": true,
  "validation": {
    "min": 1,
    "max": 20
  },
  "source": {
    "type": "env",
    "name": "CHATGPT_MAX_CONCURRENT_SESSIONS"
  },
  "metadata": {
    "category": "runtime",
    "uiOrder": 10
  }
}
```

### 4.3 Secret Reference ConfigItem

```json
{
  "key": "chatgpt.accountSecret",
  "label": "ChatGPT Account Secret",
  "description": "Reference to the secret used by this Capsule Service.",
  "type": "secretRef",
  "currentValue": "agent-local://agent-001/secrets/chatgpt/account-001",
  "editable": false,
  "sensitive": true
}
```

---

## 5. ConfigItem Fields

### 5.1 `key`

Stable technical key of the configuration item.

Required.

Rules:

- dot-separated naming is recommended;
- stable across service restarts;
- unique within one Capsule Service;
- should describe logical meaning, not storage implementation only.

Good examples:

```text
demo.message
chatgpt.maxConcurrentSessions
browser.launchTimeoutSeconds
account.sessionRefreshIntervalSeconds
proxy.defaultRegion
```

Bad examples:

```text
config1
value
x
TEMP_SETTING
```

### 5.2 `label`

Human-readable display name.

Required for UI display.

Examples:

```text
Demo Message
Max Concurrent Sessions
Browser Launch Timeout
Session Refresh Interval
```

### 5.3 `description`

Optional description for operators.

It should explain:

- what this config does;
- when to change it;
- what impact it may have;
- whether service reload is needed.

### 5.4 `type`

Required.

Allowed values:

```text
string
number
boolean
select
json
secretRef
```

Future versions may add:

```text
multiSelect
duration
url
cron
filePath
```

CE v0.1 should support at least:

```text
string
number
boolean
select
json
secretRef
```

### 5.5 `currentValue`

Optional current value.

Rules:

- may be omitted;
- must be masked or omitted if sensitive;
- should not contain raw secrets;
- may be displayed in UI if safe.

### 5.6 `defaultValue`

Optional default value.

Useful for UI and documentation.

### 5.7 `editable`

Whether the config item can be edited through Opstage.

In CE v0.1, this field may be displayed but does not require full edit implementation.

Recommended default:

```text
false
```

### 5.8 `sensitive`

Whether the config value is sensitive.

If `sensitive` is true:

- UI must not display raw value;
- Backend should avoid storing raw value if possible;
- Agent SDK should avoid reporting raw value;
- `secretRef` should be preferred.

### 5.9 `required`

Whether the config item is required for service operation.

Optional.

### 5.10 `options`

Allowed options for `select` type.

Example:

```json
{
  "key": "proxy.defaultRegion",
  "label": "Default Proxy Region",
  "type": "select",
  "options": [
    { "label": "Finland", "value": "fi" },
    { "label": "Germany", "value": "de" },
    { "label": "United States", "value": "us" }
  ],
  "defaultValue": "fi"
}
```

### 5.11 `validation`

Optional validation hints.

Examples:

```json
{
  "min": 1,
  "max": 20
}
```

```json
{
  "pattern": "^[a-z][a-z0-9-]*$"
}
```

CE v0.1 may store validation metadata without enforcing it.

### 5.12 `source`

Optional metadata describing where the config comes from.

Examples:

```json
{
  "type": "env",
  "name": "CHATGPT_MAX_CONCURRENT_SESSIONS"
}
```

```json
{
  "type": "file",
  "path": "config/default.json"
}
```

Allowed source types may include:

```text
env
file
database
runtime
secretRef
unknown
```

CE v0.1 may display this field as metadata.

### 5.13 `metadata`

Optional free-form object.

Examples:

```json
{
  "category": "runtime",
  "uiOrder": 10,
  "reloadRequired": true
}
```

---

## 6. Config Provider

In embedded Agent mode, the Capsule Service provides config metadata to the Agent SDK.

Recommended TypeScript shape:

```ts
export type ConfigProvider = () => Promise<CapsuleConfigItem[]> | CapsuleConfigItem[];

export interface CapsuleConfigItem {
  key: string;
  label: string;
  description?: string;
  type: 'string' | 'number' | 'boolean' | 'select' | 'json' | 'secretRef';
  currentValue?: unknown;
  defaultValue?: unknown;
  editable?: boolean;
  sensitive?: boolean;
  required?: boolean;
  options?: Array<{ label: string; value: string }>;
  validation?: Record<string, unknown>;
  source?: {
    type: 'env' | 'file' | 'database' | 'runtime' | 'secretRef' | 'unknown';
    name?: string;
    path?: string;
    metadata?: Record<string, unknown>;
  };
  metadata?: Record<string, unknown>;
}
```

CE v0.1 Node.js embedded Agent SDK should support a config provider with this shape or an equivalent shape.

---

## 7. Config Reporting

Config metadata may be reported in two ways.

### 7.1 Manifest-based config reporting

Configs may be embedded in the Capsule Manifest.

Example:

```json
{
  "configs": [
    {
      "key": "demo.message",
      "label": "Demo Message",
      "type": "string",
      "defaultValue": "hello capsule",
      "editable": true,
      "sensitive": false
    }
  ]
}
```

### 7.2 Dedicated config report

Future Agent API may support separate config reports.

Example future endpoint:

```http
POST /api/agents/{agentId}/services/{serviceId}/configs/report
Authorization: Bearer <agentToken>
```

CE v0.1 may use manifest-based reporting to keep implementation simple.

---

## 8. Backend Storage

CE v0.1 Backend may store config items in a separate table or inside manifest JSON.

Recommended simple table fields:

```text
id
workspaceId
serviceId
configKey
label
description
valueType
currentValueJson
defaultValueJson
editable
sensitive
required
metadataJson
createdAt
updatedAt
```

If storing in a separate table, Backend should upsert config items by:

```text
serviceId + configKey
```

CE v0.1 may also keep the full original config object in `metadataJson` or `manifestJson` for compatibility.

---

## 9. UI Requirements

CE v0.1 UI should display config items on the Capsule Service detail page.

Recommended columns or fields:

```text
Key
Label
Type
Value
Default
Editable
Sensitive
Source
Description
```

UI behavior:

- show non-sensitive `currentValue` if available;
- mask sensitive values;
- show `secretRef` as a reference, not as a raw secret;
- indicate whether the item is editable;
- do not provide full edit workflow unless explicitly implemented;
- allow viewing raw metadata JSON if useful for debugging.

Example sensitive display:

```text
••••••••
```

or:

```text
secretRef: agent-local://agent-001/secrets/chatgpt/account-001
```

---

## 10. Sensitive Values

Sensitive values require special handling.

A config item should be marked sensitive when it contains or refers to:

- passwords;
- API keys;
- OAuth tokens;
- cookies;
- session tokens;
- private keys;
- account credentials;
- secret references.

### 10.1 Raw secrets are not allowed

Config reports must not include raw secrets.

Bad:

```json
{
  "key": "chatgpt.password",
  "type": "string",
  "currentValue": "plain-text-password",
  "sensitive": true
}
```

Good:

```json
{
  "key": "chatgpt.accountSecret",
  "type": "secretRef",
  "currentValue": "agent-local://agent-001/secrets/chatgpt/account-001",
  "sensitive": true
}
```

### 10.2 Backend storage rule

Backend should avoid storing raw sensitive values.

If a sensitive `currentValue` is accidentally received, Backend should mask or reject it depending on policy.

CE v0.1 recommended behavior:

```text
If sensitive = true and type != secretRef:
    store currentValue as null or masked string
```

---

## 11. SecretRef

`secretRef` is the recommended representation for sensitive configuration.

Examples:

```text
agent-local://agent-001/secrets/chatgpt/account-001
vault://secret/path
opstage-secret://workspace/key
```

CE v0.1 does not need to resolve secret references.

It only needs to display them safely and preserve them in metadata.

Future editions may support:

- Agent-local secrets;
- Opstage-managed secret store;
- external Vault integration;
- cloud provider secret managers;
- secret rotation.

---

## 12. Config Editing

CE v0.1 does not need full config editing.

However, the model should reserve future fields and workflows.

Future config editing flow:

```text
User edits config in UI
    ↓
Backend validates change
    ↓
Backend creates config change command
    ↓
Agent applies config change
    ↓
Capsule Service reloads or confirms
    ↓
Agent reports result
    ↓
Backend records audit event
```

Future capabilities may include:

- validation;
- preview;
- approval;
- versioning;
- rollback;
- environment promotion;
- reload action;
- config drift detection.

CE v0.1 should not implement this full flow.

---

## 13. Config Reload

Some config changes may require reload or restart.

Use metadata to describe this requirement:

```json
{
  "metadata": {
    "reloadRequired": true,
    "restartRequired": false
  }
}
```

Future versions may connect config changes with actions such as:

```text
reloadConfig
restartService
validateConfig
```

CE v0.1 may display reload metadata only.

---

## 14. Config Source

Config source helps operators understand where a value comes from.

Recommended source examples:

### 14.1 Environment variable

```json
{
  "source": {
    "type": "env",
    "name": "BROWSER_LAUNCH_TIMEOUT_SECONDS"
  }
}
```

### 14.2 File

```json
{
  "source": {
    "type": "file",
    "path": "config/default.json"
  }
}
```

### 14.3 Runtime

```json
{
  "source": {
    "type": "runtime"
  }
}
```

### 14.4 Secret reference

```json
{
  "source": {
    "type": "secretRef",
    "name": "chatgpt.accountSecret"
  }
}
```

CE v0.1 may display source metadata but does not need to read the source directly.

---

## 15. Config Status

ConfigItem itself may have status in future versions.

Potential values:

```text
ACTIVE
MISSING
INVALID
STALE
UNKNOWN
```

CE v0.1 does not need a config status model unless easy to implement.

If used, keep it optional:

```json
{
  "key": "demo.message",
  "status": "ACTIVE"
}
```

---

## 16. Config and Audit

Config visibility itself does not necessarily require audit for every report.

Future config changes must be audited.

Recommended future audit events:

```text
config.reported
config.change.requested
config.change.applied
config.change.failed
config.rollback.requested
config.rollback.completed
```

CE v0.1 minimum audit:

- no audit required for every config report;
- audit optional when manifest or service metadata changes materially.

---

## 17. Backend Requirements

CE v0.1 Backend should:

1. accept config metadata from manifest or service report;
2. validate basic config fields;
3. avoid storing raw sensitive values;
4. store config metadata;
5. expose configs to UI;
6. preserve unknown optional fields where possible;
7. avoid implementing full config publishing workflow.

---

## 18. Agent SDK Requirements

CE v0.1 Node.js embedded Agent SDK should:

1. allow registering static config metadata;
2. allow using a config provider function;
3. include configs in manifest or service report;
4. mark sensitive values safely;
5. avoid reporting raw secrets;
6. keep config reporting failure from blocking service startup.

Example:

```ts
const agent = new CapsuleAgent({
  configs: [
    {
      key: 'demo.message',
      label: 'Demo Message',
      type: 'string',
      defaultValue: 'hello capsule',
      editable: true,
      sensitive: false,
    },
  ],
});
```

---

## 19. Compatibility Rules

- New optional fields may be added to ConfigItem.
- Unknown fields should be ignored by older clients.
- Required fields should remain stable.
- CE may implement config visibility only.
- EE/Cloud may add editing, approval, versioning, rollout, and rollback without changing the basic ConfigItem contract.

Required stable fields:

```text
key
label
type
```

Recommended stable fields:

```text
currentValue
defaultValue
editable
sensitive
required
options
validation
source
metadata
```

---

## 20. CE v0.1 Required Subset

CE v0.1 must support:

- ConfigItem metadata shape;
- manifest-based config reporting;
- config storage or manifest extraction;
- UI config display;
- masking or hiding sensitive values;
- `secretRef` type;
- unknown field preservation where practical.

CE v0.1 does not need to support:

- remote config editing;
- config publishing;
- config approval;
- config rollback;
- config version history;
- environment-specific config overlays;
- distributed config synchronization;
- config drift detection.

---

## 21. Example CE v0.1 Config Flow

```text
Capsule Service defines config metadata
    ↓
Agent includes configs in manifest or service report
    ↓
Backend stores config metadata
    ↓
UI displays config list
    ↓
Sensitive values are masked or shown as secret references
```

Example manifest fragment:

```json
{
  "configs": [
    {
      "key": "demo.message",
      "label": "Demo Message",
      "description": "Message used by the demo echo action.",
      "type": "string",
      "defaultValue": "hello capsule",
      "editable": true,
      "sensitive": false,
      "metadata": {
        "category": "demo"
      }
    }
  ]
}
```

---

## 22. Anti-Patterns

Avoid these patterns.

### 22.1 Building a full config center in CE v0.1

CE v0.1 should not become Nacos, Apollo, or a feature flag platform.

### 22.2 Storing raw secrets

Do not store raw credentials, cookies, API keys, or tokens as config values.

### 22.3 Displaying sensitive values

Do not show raw sensitive values in UI.

### 22.4 Treating config visibility as config ownership

Opstage may display config metadata without becoming the source of truth for all configuration.

### 22.5 Blocking service startup because config reporting fails

Config reporting failure should not prevent the Capsule Service from starting.

### 22.6 Requiring EE/Cloud config workflows in CE

Do not require approval, rollout, rollback, tenant overlays, or multi-environment promotion in CE v0.1.

---

## 23. Summary

Config in `xtrape-capsule` is a governance surface, not necessarily a centralized configuration system.

CE v0.1 should implement a safe and lightweight config visibility loop:

```text
ConfigProvider / Manifest Configs
    ↓
Agent report
    ↓
Backend storage
    ↓
UI display
```

This gives operators visibility into Capsule Service configuration while leaving advanced config management to future EE and Cloud editions.
