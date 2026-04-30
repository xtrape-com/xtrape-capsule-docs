# Capsule Management Contract

- Status: Specification
- Edition: Shared
- Priority: High
- Audience: backend developers, agent SDK developers, Capsule Service developers, AI coding agents

This document defines the **Capsule Management Contract** for the `xtrape-capsule` domain.

The Capsule Management Contract is the service-side governance interface that describes how a Capsule Service can expose or provide its manifest, health, configuration metadata, actions, resources, events, and metrics to an Agent or to Opstage.

This contract is shared by CE, EE, and Cloud. CE v0.1 may implement only a subset through the Node.js embedded Agent SDK.

---

## 1. Purpose

The Capsule Management Contract defines:

- how a Capsule Service describes itself;
- how an Agent obtains service metadata;
- how health information is retrieved or reported;
- how configuration metadata is retrieved;
- how predefined actions are listed and executed;
- how resources may be listed in future versions;
- how events and metrics may be exposed in future versions;
- what CE v0.1 must implement;
- how sidecar and external Agents can integrate later.

This contract does not define the business API of a Capsule Service.

It defines the **management surface** of a Capsule Service.

---

## 2. Contract Shape

The Capsule Management Contract may be implemented in three ways:

1. **Embedded Agent Provider**
2. **HTTP Management Endpoint**
3. **External Agent Target Configuration**

All three forms should map to the same logical contract.

---

## 3. Embedded Agent Provider

In CE v0.1, the primary implementation is the Node.js embedded Agent SDK.

In this mode, the Capsule Service provides management information directly to the Agent SDK through functions or configuration objects.

Example TypeScript shape:

```ts
const agent = new CapsuleAgent({
  service: {
    code: 'demo-capsule-service',
    name: 'Demo Capsule Service',
    version: '0.1.0',
    runtime: 'nodejs',
  },
  manifest: async () => ({ ... }),
  health: async () => ({ status: 'UP', details: {} }),
  configs: async () => ([ ... ]),
  actions: [ ... ],
});
```

The SDK reports the management data to Opstage Backend.

This is the only contract implementation required for CE v0.1.

---

## 4. HTTP Management Endpoint

A Capsule Service may expose a local management HTTP surface.

This is useful for future sidecar and external Agent modes.

Recommended endpoint prefix:

```text
/_capsule
```

Recommended endpoints:

```http
GET  /_capsule/manifest
GET  /_capsule/health
GET  /_capsule/configs
GET  /_capsule/actions
POST /_capsule/actions/{actionName}
GET  /_capsule/resources
GET  /_capsule/resources/{resourceName}
GET  /_capsule/events
GET  /_capsule/metrics
```

CE v0.1 does not need to implement these HTTP endpoints, but the embedded SDK should use compatible data shapes.

---

## 5. External Agent Target Configuration

In external Agent mode, a standalone Agent may manage a service using target configuration.

Example future target configuration:

```yaml
kind: CapsuleTarget
code: capi-chatgpt
name: ChatGPT CAPI Service
runtime: nodejs
agentMode: external

connect:
  baseUrl: http://127.0.0.1:3101
  managementPath: /_capsule

filesystem:
  workDir: /opt/capsules/capi-chatgpt
  configDir: /opt/capsules/capi-chatgpt/config
  logDir: /opt/capsules/capi-chatgpt/logs
  dataDir: /opt/capsules/capi-chatgpt/data
```

This is a future target and is not required for CE v0.1.

---

## 6. Contract Sections

The logical management contract contains these sections:

```text
manifest
health
configs
actions
resources
events
metrics
```

CE v0.1 required sections:

```text
manifest
health
configs
actions
```

CE v0.1 may keep `resources`, `events`, and `metrics` as future placeholders.

---

## 7. Manifest Contract

The manifest describes the Capsule Service identity and management surface.

Reference:

```text
02-specs/01-capsule-manifest-spec.md
```

### 7.1 Embedded Provider Shape

```ts
type ManifestProvider = () => Promise<CapsuleManifest> | CapsuleManifest;
```

### 7.2 HTTP Endpoint

```http
GET /_capsule/manifest
```

Example response:

```json
{
  "kind": "CapsuleService",
  "schemaVersion": "1.0",
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
    }
  ],
  "configs": []
}
```

### 7.3 CE v0.1 Requirement

CE v0.1 must support manifest reporting from the Node.js embedded Agent SDK to Backend.

---

## 8. Health Contract

Health describes the current operational status of the Capsule Service.

Reference:

```text
02-specs/04-health-spec.md
```

### 8.1 Health Status Values

Allowed values:

```text
UP
DOWN
DEGRADED
UNKNOWN
```

### 8.2 Embedded Provider Shape

```ts
export type HealthProvider = () => Promise<CapsuleHealthReport> | CapsuleHealthReport;

export interface CapsuleHealthReport {
  status: 'UP' | 'DOWN' | 'DEGRADED' | 'UNKNOWN';
  details?: Record<string, unknown>;
  checkedAt?: string;
}
```

### 8.3 HTTP Endpoint

```http
GET /_capsule/health
```

Example response:

```json
{
  "status": "UP",
  "details": {
    "database": "UP",
    "browser": "UP",
    "queue": "DEGRADED"
  },
  "checkedAt": "2026-04-30T10:21:00Z"
}
```

### 8.4 CE v0.1 Requirement

CE v0.1 must support health reporting through the embedded Agent SDK.

The Backend should store the latest health state and expose it to UI.

---

## 9. Config Contract

Configs describe manageable configuration metadata.

Reference:

```text
02-specs/06-config-spec.md
```

A config item describes how Opstage should display or manage a configuration value.

### 9.1 Embedded Provider Shape

```ts
export type ConfigProvider = () => Promise<CapsuleConfigItem[]> | CapsuleConfigItem[];

export interface CapsuleConfigItem {
  key: string;
  label: string;
  type: 'string' | 'number' | 'boolean' | 'select' | 'json' | 'secretRef';
  currentValue?: unknown;
  defaultValue?: unknown;
  editable?: boolean;
  sensitive?: boolean;
  options?: Array<{ label: string; value: string }>;
  metadata?: Record<string, unknown>;
}
```

### 9.2 HTTP Endpoint

```http
GET /_capsule/configs
```

Example response:

```json
[
  {
    "key": "demo.message",
    "label": "Demo Message",
    "type": "string",
    "currentValue": "hello",
    "defaultValue": "hello",
    "editable": true,
    "sensitive": false
  }
]
```

### 9.3 CE v0.1 Requirement

CE v0.1 may implement config visibility only.

Full config editing, publishing, rollback, and approval are future capabilities.

---

## 10. Action Contract

Actions describe predefined operations that Opstage may request through an Agent.

Reference:

```text
02-specs/action-spec.md
```

### 10.1 Embedded Action Definition

```ts
export interface CapsuleActionDefinition {
  name: string;
  label: string;
  description?: string;
  dangerLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  enabled?: boolean;
  inputSchema?: Record<string, unknown>;
  resultSchema?: Record<string, unknown>;
  confirmRequired?: boolean;
  timeoutSeconds?: number;
  metadata?: Record<string, unknown>;
}
```

### 10.2 Embedded Action Handler

```ts
export type CapsuleActionHandler = (
  payload: unknown,
  context: CapsuleActionContext
) => Promise<CapsuleActionResult> | CapsuleActionResult;

export interface CapsuleActionContext {
  commandId: string;
  actionName: string;
  serviceCode: string;
  agentId: string;
  requestedAt: string;
}

export interface CapsuleActionResult {
  success: boolean;
  message?: string;
  data?: unknown;
  error?: {
    code?: string;
    message: string;
    details?: unknown;
  };
}
```

### 10.3 HTTP Endpoints

List actions:

```http
GET /_capsule/actions
```

Execute action:

```http
POST /_capsule/actions/{actionName}
```

Request body:

```json
{
  "payload": {}
}
```

Example response:

```json
{
  "success": true,
  "message": "Action completed.",
  "data": {}
}
```

### 10.4 CE v0.1 Requirement

CE v0.1 must support predefined actions through the embedded Agent SDK.

CE v0.1 must not support arbitrary shell command execution from the UI.

---

## 11. Resource Contract

Resources describe manageable business or runtime objects owned by a Capsule Service.

Examples:

```text
account
session
job
queue
proxy
connector
agentRun
```

### 11.1 Future Endpoint

```http
GET /_capsule/resources
GET /_capsule/resources/{resourceName}
```

### 11.2 Future Response Example

```json
[
  {
    "name": "sessions",
    "label": "Sessions",
    "type": "session",
    "description": "Managed browser sessions."
  }
]
```

### 11.3 CE v0.1 Requirement

CE v0.1 does not need full resource management.

It may store resource definitions in the manifest only.

---

## 12. Event Contract

Events describe runtime changes emitted by a Capsule Service.

Examples:

```text
session.expired
account.limited
worker.failed
connector.reconnected
```

### 12.1 Future Endpoint

```http
GET /_capsule/events
```

or event push through Agent:

```text
Agent -> Backend: report events
```

### 12.2 CE v0.1 Requirement

CE v0.1 does not need a full event stream.

Audit events and command results are enough for the first milestone.

---

## 13. Metrics Contract

Metrics describe numeric runtime measurements.

Examples:

```text
active_sessions
request_count
error_count
queue_size
success_rate
```

### 13.1 Future Endpoint

```http
GET /_capsule/metrics
```

### 13.2 CE v0.1 Requirement

CE v0.1 does not need a full metrics system.

Health status is sufficient for the first milestone.

---

## 14. Security Rules

### 14.1 Management surface should not be public by default

If HTTP management endpoints are implemented, they should be bound to local network or protected by Agent-level authentication.

### 14.2 No raw secrets

Management contract responses must not expose raw passwords, cookies, tokens, or credentials.

Use `secretRef` where needed.

### 14.3 No arbitrary shell execution

The contract must not define a generic shell execution endpoint for CE v0.1.

Bad:

```http
POST /_capsule/shell
POST /_capsule/exec
```

### 14.4 Agent authorization required

Opstage should manage Capsule Services only through registered and authorized Agents.

---

## 15. Error Model

Management contract implementations should return structured errors.

Recommended shape:

```json
{
  "success": false,
  "error": {
    "code": "ACTION_NOT_FOUND",
    "message": "Action not found: refreshSession",
    "details": {}
  }
}
```

Recommended error codes:

```text
MANIFEST_INVALID
HEALTH_UNAVAILABLE
CONFIG_NOT_FOUND
ACTION_NOT_FOUND
ACTION_DISABLED
ACTION_FAILED
RESOURCE_NOT_FOUND
UNAUTHORIZED
FORBIDDEN
INTERNAL_ERROR
```

CE v0.1 may keep error handling simple but should preserve structured error shape in Agent SDK and Backend command results.

---

## 16. Versioning and Compatibility

### 16.1 Additive evolution

New optional fields may be added.

Older clients should ignore unknown fields.

### 16.2 Stable core fields

The meaning of core fields should remain stable:

```text
code
name
version
runtime
agentMode
status
actions
configs
resources
```

### 16.3 Partial implementation

CE may implement a subset of the contract.

For example:

```text
Contract supports: manifest, health, configs, actions, resources, events, metrics
CE v0.1 implements: manifest, health, configs, actions
```

This is acceptable.

---

## 17. CE v0.1 Required Subset

CE v0.1 must implement the following logical contract through the Node.js embedded Agent SDK:

```text
manifest
health
configs
actions
```

CE v0.1 must support:

- manifest provider;
- health provider;
- config metadata provider;
- action definitions;
- action handlers;
- command polling;
- command result reporting.

CE v0.1 does not need to support:

- HTTP `/_capsule/*` endpoints;
- dynamic resource browsing;
- event streaming;
- metrics collection;
- config publishing;
- sidecar Agent;
- external Agent.

---

## 18. Anti-Patterns

Avoid these patterns.

### 18.1 Management contract mixed with business API

Do not mix business endpoints and management endpoints without clear boundary.

Recommended management prefix:

```text
/_capsule
```

### 18.2 Opstage calling business internals directly

Opstage should not call arbitrary service internals. It should use the Agent and the management contract.

### 18.3 Raw secrets in management response

Do not expose sensitive values.

### 18.4 Generic remote shell endpoint

Do not define shell execution endpoints in CE v0.1.

### 18.5 Required EE/Cloud fields in CE

Do not require tenant, billing, cluster, or enterprise identity fields in CE v0.1.

---

## 19. Summary

The Capsule Management Contract defines the management surface of a Capsule Service.

The long-term contract includes:

```text
manifest
health
configs
actions
resources
events
metrics
```

CE v0.1 should implement the minimum useful subset through the Node.js embedded Agent SDK:

```text
manifest
health
configs
actions
```

This keeps CE lightweight while preserving a clear path toward sidecar Agents, external Agents, EE, and Cloud.
