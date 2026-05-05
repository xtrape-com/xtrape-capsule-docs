---
status: draft
audience: ai-coding-agents
stability: unstable
last_reviewed: 2026-05-05
edition: ce
phase: current
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 04-demo-service-plan.md
翻译状态 / Translation Status: 已翻译 / Translated
生成时间 / Generated: 2026-05-01 09:28:55
================================================================================
注意 / Notes:
- 技术术语如 Capsule Service、Agent、Opstage 等保留英文或采用中英对照
- 代码块中的内容不翻译
- 文件路径和 URL 不翻译
- 保持原有的 Markdown 格式结构
================================================================================
-->

# CE（社区版） v0.1 Demo Capsule Service（胶囊服务） Plan

- Status: 实施指南
- Edition: CE（社区版）
- Priority: Current
- Audience: Capsule Service（胶囊服务） developers, agent SDK developers, backend developers, frontend developers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs or `09-contracts/openapi/opstage-ce-v0.1.yaml` disagree, the ADRs and OpenAPI contract win for CE（社区版） v0.1.

## 1. Goal

Build a minimal Node.js demo Capsule Service（胶囊服务） that proves the full CE（社区版） v0.1 governance loop.

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
- register with Opstage（运维舞台） using a registration token;
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

The demo service should be available in the optional CE（社区版） Docker Compose quick start:

```text
opstage-ce
    exposes UI and Backend

demo-capsule-service
    connects outbound to opstage-ce
```

## 9. Acceptance Criteria

A user can:

1. start Opstage（运维舞台） CE（社区版）;
2. create a registration token;
3. start the demo service with the token;
4. see Agent（代理） online;
5. see Capsule Service（胶囊服务） reported;
6. view health/config/action metadata;
7. run `echo`;
8. run `runHealthCheck`;
9. see CommandResult;
10. see AuditEvents.
