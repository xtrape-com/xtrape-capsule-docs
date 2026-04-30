# CE v0.1 Demo Capsule Service Plan

- Status: Implementation Guidance
- Edition: CE
- Priority: Current
- Audience: Capsule Service developers, agent SDK developers, backend developers, frontend developers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/openapi/opstage-ce-v0.1.yaml` disagree, the ADRs and OpenAPI contract win for CE v0.1.

## 1. Goal

Build a minimal Node.js demo Capsule Service that proves the full CE v0.1 governance loop.

The demo service should be simple enough for users to understand and copy.

## 2. Package

Recommended package:

```text
apps/demo-capsule-service
```

## 3. Responsibilities

The demo service should:

- start as a normal Node.js process;
- create and start `CapsuleAgent`;
- register with Opstage using a registration token;
- report a manifest;
- report health;
- report config metadata;
- report action metadata;
- handle predefined actions;
- log clear startup instructions.

## 4. Demo Manifest

Minimum manifest:

```json
{
  "kind": "CapsuleService",
  "code": "demo-capsule-service",
  "name": "Demo Capsule Service",
  "description": "A demo Capsule Service for Opstage CE v0.1.",
  "version": "0.1.0",
  "runtime": "nodejs"
}
```

## 5. Demo Configs

Recommended configs:

```text
demo.message       non-sensitive string preview
demo.secretRef     sensitive secretRef example
```

Sensitive configs must not expose raw secret values.

## 6. Demo Actions

### 6.1 `echo`

- danger level: LOW;
- input: arbitrary JSON object;
- output: same payload.

### 6.2 `runHealthCheck`

- danger level: LOW;
- input: none;
- output: latest health report.

### 6.3 Non-goal

The demo service must not include:

```text
shell
exec
bash
arbitrary script runner
```

## 7. Environment Variables

```text
OPSTAGE_BACKEND_URL=http://localhost:8080
OPSTAGE_REGISTRATION_TOKEN=opstage_reg_...
OPSTAGE_AGENT_TOKEN_FILE=./data/agent-token.json
DEMO_MESSAGE=hello capsule
```

## 8. Docker Compose Role

The demo service should be available in the optional CE Docker Compose quick start:

```text
opstage-ce
    exposes UI and Backend

demo-capsule-service
    connects outbound to opstage-ce
```

## 9. Acceptance Criteria

A user can:

1. start Opstage CE;
2. create a registration token;
3. start the demo service with the token;
4. see Agent online;
5. see Capsule Service reported;
6. view health/config/action metadata;
7. run `echo`;
8. run `runHealthCheck`;
9. see CommandResult;
10. see AuditEvents.
