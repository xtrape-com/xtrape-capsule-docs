# Python Runtime Planning

- Status: Planning
- Edition: EE
- Priority: Future
- Audience: architects, Python developers, AI automation developers, FastAPI developers, agent SDK developers, backend developers, AI coding agents

This document defines the planned **Python Runtime** integration for the `xtrape-capsule` product family.

Python Runtime is a future extension. It is not a CE v0.1 implementation requirement.

The current CE implementation focus is **Node.js**. Python Runtime planning exists to keep the Capsule governance model compatible with AI automation workers, FastAPI services, data-processing workers, browser automation tasks, LangChain/LangGraph services, and other Python-based runtimes in future EE or later CE versions.

---

## 1. Purpose

The purpose of Python Runtime planning is to define how Python services or workers may become Capsule Services governed by Opstage.

Python Runtime should eventually define:

- Python service identity conventions;
- Python Agent SDK package structure;
- FastAPI integration direction;
- async runtime support;
- runtime configuration;
- Agent registration;
- Agent token storage;
- health provider integration;
- config metadata provider integration;
- predefined action registration;
- Command polling and execution;
- CommandResult reporting;
- sensitive data rules;
- testing requirements;
- compatibility with the shared Capsule governance contract.

Python Runtime should adapt the Capsule model to Python idioms without redefining the model.

---

## 2. Runtime Scope

Future Python Runtime may include:

```text
Python Embedded Agent SDK
FastAPI helper
async Agent client
service identity declaration
health provider
config metadata provider
predefined action registry
HTTP polling command delivery
CommandResult reporting
file-based Agent token store
safe logging
Python demo Capsule Service
```

Python Runtime should not initially include:

```text
Sidecar Agent runtime
External Agent runtime
Kubernetes operator
WebSocket/gRPC command delivery
Agent Gateway protocol
full config publishing
secret vault implementation
remote shell
arbitrary script execution
full observability collector
```

These may be separate future designs if needed.

---

## 3. Relationship with CE

CE v0.1 implements Node.js first.

Python Runtime is not required for CE v0.1.

CE may reserve shared concepts that make Python integration easier later:

```text
runtime
agentMode
agentVersion
sdkVersion
protocolVersion
capabilities
secretRef
metadataJson
CommandType
```

But CE should not implement Python SDK, PyPI package publishing, or FastAPI helper in v0.1.

---

## 4. Target Python Ecosystems

Python Runtime may target:

```text
FastAPI services
async workers
AI automation workers
LangChain services
LangGraph services
browser automation scripts
scraping workers
data processing workers
account/session management workers
plain Python services
```

Recommended first target:

```text
FastAPI + async worker-friendly SDK
```

because many AI-era automation services are HTTP/API services or async workers.

---

## 5. Package Direction

Possible PyPI package names:

```text
xtrape-capsule-agent-python
xtrape-capsule-agent
xtrape-opstage-agent
```

Recommended package name:

```text
xtrape-capsule-agent
```

Possible import style:

```python
from xtrape_capsule_agent import CapsuleAgent
```

The final package name should follow the broader repository and publishing conventions.

---

## 6. Python Embedded Agent Model

The first Python Runtime model should be Embedded Agent.

Recommended structure:

```text
Python process
├── FastAPI app / worker / automation logic
└── Python Embedded Agent SDK
    ├── registration client
    ├── token store
    ├── heartbeat task
    ├── manifest reporter
    ├── health provider wrapper
    ├── config metadata provider
    ├── action registry
    ├── command polling task
    └── CommandResult reporter
```

The Python Agent should run inside the service process but should avoid destabilizing the business or automation runtime.

---

## 7. Minimal Usage Direction

A future Python SDK should provide a simple integration style.

Example target API:

```python
from xtrape_capsule_agent import CapsuleAgent

agent = CapsuleAgent(
    backend_url="http://localhost:8080",
    registration_token="opstage_reg_xxx",
    token_file="./data/agent-token.json",
    service={
        "code": "demo-python-capsule-service",
        "name": "Demo Python Capsule Service",
        "description": "A demo Python Capsule Service for Opstage.",
        "version": "0.1.0",
        "runtime": "python",
    },
)

@agent.health
def health():
    return {
        "status": "UP",
        "message": "Python service is healthy.",
    }

@agent.configs
def configs():
    return [
        {
            "key": "demo.message",
            "label": "Demo Message",
            "type": "string",
            "currentValue": "hello capsule",
            "defaultValue": "hello capsule",
            "editable": True,
            "sensitive": False,
            "source": "env",
        }
    ]

@agent.action(name="echo", label="Echo", danger_level="LOW")
def echo(payload, context):
    return {
        "success": True,
        "message": "Echo completed.",
        "data": payload,
    }

agent.start()
```

For async runtimes, the SDK should support async handlers and async startup.

---

## 8. Async Runtime Direction

Python Runtime should support async usage because FastAPI, Playwright, and many AI automation libraries are async-friendly.

Possible async API:

```python
@agent.health
async def health():
    return {
        "status": "UP",
        "message": "Async service is healthy.",
    }

@agent.action(name="run_health_check", label="Run Health Check", danger_level="LOW")
async def run_health_check(payload, context):
    result = await agent.run_health()
    return {
        "success": True,
        "message": "Health check completed.",
        "data": result,
    }

await agent.start_async()
```

The SDK should avoid forcing synchronous-only behavior.

---

## 9. FastAPI Integration Direction

A FastAPI helper may integrate Agent lifecycle with application startup and shutdown.

Example target API:

```python
from fastapi import FastAPI
from xtrape_capsule_agent.fastapi import attach_capsule_agent

app = FastAPI()

agent = CapsuleAgent.from_env(
    service={
        "code": "demo-fastapi-service",
        "name": "Demo FastAPI Service",
        "version": "0.1.0",
        "runtime": "python",
    }
)

attach_capsule_agent(app, agent)
```

The helper may:

- start Agent on FastAPI startup;
- stop Agent on shutdown;
- avoid blocking the web server;
- register optional local diagnostic endpoints if explicitly enabled.

This is future planning only.

---

## 10. Configuration Model

Python Runtime may use environment variables and code options.

Recommended environment variables:

```text
OPSTAGE_BACKEND_URL=http://localhost:8080
OPSTAGE_REGISTRATION_TOKEN=opstage_reg_xxx
OPSTAGE_AGENT_TOKEN_FILE=./data/agent-token.json
OPSTAGE_AGENT_CODE=local-python-agent
OPSTAGE_AGENT_NAME=Local Python Agent
OPSTAGE_HEARTBEAT_INTERVAL_SECONDS=30
OPSTAGE_COMMAND_POLL_INTERVAL_SECONDS=5
OPSTAGE_LOG_LEVEL=info
```

Recommended precedence:

```text
explicit code options > environment variables > SDK defaults
```

Registration token and Agent token must not be logged.

---

## 11. Service Identity

Python Capsule Service identity should be stable.

Recommended fields:

```text
code
name
description
version
runtime
metadata
```

Example:

```python
service={
    "code": "demo-python-capsule-service",
    "name": "Demo Python Capsule Service",
    "description": "A demo Python Capsule Service for Opstage.",
    "version": "0.1.0",
    "runtime": "python",
}
```

Rules:

- `code` must be stable across restarts;
- `runtime` should be `python`;
- version should match application version where practical;
- metadata should not contain raw secrets.

---

## 12. Agent Token Store

Python Runtime may support a file-based token store first.

Recommended path:

```text
./data/agent-token.json
```

Rules:

- token file should survive service restart;
- token file should not be committed to source control;
- raw token must not be logged;
- corrupted token file should be handled safely;
- deleting token file should allow re-registration if registration token exists.

Future EE may add:

- OS keyring;
- Kubernetes Secret;
- Vault-backed token store;
- custom TokenStore interface.

---

## 13. Health Integration

Python Runtime may expose health through a function or async function.

Possible provider interface:

```python
@agent.health
def health():
    return {
        "status": "UP",
        "message": "Service is healthy.",
        "dependencies": [
            {
                "name": "database",
                "type": "database",
                "status": "UP",
                "message": "Database is reachable.",
            }
        ],
    }
```

Recommended status values:

```text
UP
DOWN
DEGRADED
UNKNOWN
```

Rules:

- health provider should be lightweight;
- exceptions should not crash the service;
- health output must not include raw secrets;
- dependency details should be sanitized.

---

## 14. Config Metadata Integration

Python Runtime may expose config metadata through a function or async function.

Possible provider interface:

```python
@agent.configs
def configs():
    return [
        {
            "key": "demo.message",
            "label": "Demo Message",
            "type": "string",
            "currentValue": "hello capsule",
            "defaultValue": "hello capsule",
            "editable": True,
            "sensitive": False,
            "source": "env",
        },
        {
            "key": "demo.account_secret",
            "label": "Demo Account Secret",
            "type": "secretRef",
            "currentValue": "agent-local://python-agent/secrets/demo/account",
            "editable": False,
            "sensitive": True,
            "source": "local-secret-store",
        },
    ]
```

Rules:

- report metadata, not full config-center behavior;
- sensitive values must be masked or represented as `secretRef`;
- raw passwords, tokens, cookies, and API keys must not be reported;
- config editing and publishing are future EE capabilities.

---

## 15. Action Registration

Python Runtime may use decorator-based and programmatic action registration.

### 15.1 Decorator-based action

```python
@agent.action(name="echo", label="Echo", danger_level="LOW")
def echo(payload, context):
    return {
        "success": True,
        "message": "Echo completed.",
        "data": payload,
    }
```

### 15.2 Async action

```python
@agent.action(name="validate_sessions", label="Validate Sessions", danger_level="MEDIUM")
async def validate_sessions(payload, context):
    result = await session_manager.validate_all()
    return {
        "success": True,
        "message": "Session validation completed.",
        "data": result.summary(),
    }
```

Rules:

- action names must be unique per service;
- actions must be predefined;
- unknown actions fail safely;
- action output must be JSON-serializable;
- handler exceptions must be captured;
- no built-in arbitrary shell action;
- high-risk actions must declare appropriate danger level.

---

## 16. Command Execution

Python Runtime should follow the same Command flow as Node.js:

```text
Agent polls Backend for Commands
    ↓
Backend returns Commands assigned to this Agent
    ↓
Agent validates command type and action name
    ↓
Agent executes local Python action handler
    ↓
Agent captures success or failure
    ↓
Agent reports CommandResult
```

Initial supported command type:

```text
ACTION
```

Python Runtime must not expose arbitrary shell execution.

---

## 17. CommandResult Reporting

CommandResult should include:

```text
status
outputText
errorMessage
resultJson
startedAt
finishedAt
```

Rules:

- successful handler returns `SUCCESS`;
- failed handler returns `FAILED`;
- exceptions are captured and sanitized;
- raw secrets must not be returned;
- large logs should not be returned as CommandResult;
- result should be concise and JSON-serializable.

---

## 18. Lifecycle Integration

For plain Python services, lifecycle may be manual:

```python
agent.start()
```

For async services:

```python
await agent.start_async()
```

For FastAPI:

```text
FastAPI startup event
    ↓
Agent loads token or registers
    ↓
Agent reports manifest
    ↓
Agent starts heartbeat task
    ↓
Agent starts command polling task
```

On shutdown:

```text
FastAPI shutdown event
    ↓
Agent stops background tasks
    ↓
Agent lets in-flight command finish if practical
```

Backend should infer offline state from heartbeat timeout.

---

## 19. AI Automation Worker Direction

Python Runtime is especially relevant for AI-era automation workers.

Potential Capsule Services:

```text
LangChain workflow worker
LangGraph workflow runner
Playwright automation worker
scraping worker
data extraction worker
account/session validator
RAG ingestion worker
embedding job worker
```

Potential actions:

```text
runHealthCheck
validateSessions
refreshAccountPool
runSmokeTask
rebuildIndex
syncKnowledgeSource
clearExpiredJobs
```

Rules:

- actions must be predefined;
- long-running workflows need future progress design;
- raw credentials and browser sessions must not be sent to Opstage;
- use `secretRef` for sensitive references;
- action results should return summaries, not large logs.

---

## 20. Backend Downtime Behavior

Python Runtime should tolerate Opstage Backend downtime.

If Backend is unavailable, Python Agent should:

- keep business or worker runtime running by default;
- retry heartbeat/reporting/polling with backoff;
- avoid log spam;
- re-report manifest after reconnect if needed;
- resume command polling after recovery.

A strict mode may be added for services that require governance availability.

Default behavior should favor service availability.

---

## 21. Sensitive Data Rules

Python Runtime must avoid leaking sensitive data.

Sensitive examples:

```text
password
token
accessToken
refreshToken
cookie
apiKey
privateKey
credential
secret
authorization
registrationToken
agentToken
browserSession
```

Rules:

- do not log registration token;
- do not log Agent token;
- do not report raw secrets in configs;
- do not return raw secrets in CommandResult;
- do not include raw secrets in health details;
- do not send raw browser session data to Opstage;
- use `secretRef` for sensitive references;
- sanitize logs and errors where practical.

---

## 22. Demo Python Service Direction

A future Python demo service should prove:

- Python application starts;
- Agent registers with Opstage;
- Agent token is stored and reused;
- heartbeat works;
- manifest report works;
- health provider works;
- config metadata provider works;
- actions are reported;
- `echo` action works;
- `runHealthCheck` action works;
- CommandResult is reported;
- AuditEvent appears in Opstage;
- Backend downtime does not crash the service by default.

This demo is future work, not CE v0.1.

---

## 23. Testing Direction

Future Python Runtime tests should cover:

- configuration loading;
- environment variable mapping;
- token store read/write;
- registration success/failure;
- Agent token invalid handling;
- heartbeat success/failure;
- manifest construction;
- health provider success/error;
- config provider output;
- action registration;
- async action registration;
- command polling;
- action execution success/failure;
- CommandResult reporting;
- Backend unavailable behavior;
- sensitive data sanitization.

Tests should use mocked HTTP clients or local test servers.

---

## 24. Packaging and Build Direction

Future Python SDK may use:

```text
Python 3.11+
pyproject.toml
pytest
httpx or aiohttp
pydantic optional
ruff optional
mypy optional
```

Recommended baseline:

```text
Python 3.11+
httpx
pytest
```

The exact tooling should align with the broader repository strategy.

---

## 25. Future EE Direction

Future EE may include Python Runtime because Python is highly relevant for AI automation and data-processing services.

Possible EE capabilities:

- official Python Agent SDK;
- FastAPI helper;
- async worker support;
- LangChain/LangGraph examples;
- Playwright worker examples;
- Python diagnostics;
- token rotation support;
- secret provider hooks;
- command progress support;
- long-running action support;
- account/session worker integration patterns.

---

## 26. Future Cloud Direction

Future Cloud may include Python Runtime support through:

- Cloud enrollment snippets;
- workspace-scoped registration token examples;
- Agent Gateway configuration;
- Cloud connection diagnostics;
- Python-specific quick start;
- managed alert hints;
- usage metering metadata;
- hosted examples for AI automation workers.

These are future planning items.

---

## 27. Anti-Patterns

Avoid these patterns.

### 27.1 Python SDK before Node.js CE is stable

The first milestone is proving the governance loop with Node.js.

### 27.2 Python Runtime redefines the Capsule model

Python should adapt the shared model, not create a separate one.

### 27.3 Python actions become arbitrary script execution

Actions must be predefined and explicit.

### 27.4 Browser/session data leaks into Opstage

Use `secretRef`, local storage, or sanitized summaries.

### 27.5 Long-running AI workflows return huge logs as CommandResult

Return concise summaries and references instead.

### 27.6 Backend outage crashes worker by default

Governance outage should not automatically become business or automation outage.

---

## 28. Acceptance Criteria for Future Python Runtime

A future Python Runtime implementation is acceptable when:

- Python service can install the Python Agent package;
- service identity is declared;
- Agent can register with registration token;
- Agent token is stored and reused;
- heartbeat works;
- manifest report works;
- health provider works;
- config provider works;
- actions are reported;
- sync and async actions can be supported if planned;
- `echo` action works;
- `runHealthCheck` action works;
- CommandResult is reported;
- Opstage UI shows Agent, service, health, configs, actions, Commands, and AuditEvents;
- Backend downtime does not crash the service by default;
- raw tokens are not logged;
- raw secrets are not reported;
- raw browser session data is not reported;
- no arbitrary shell execution is provided by default.

---

## 29. Summary

Python Runtime is a future integration direction for AI automation, FastAPI services, data workers, and workflow runtimes.

It should reuse the same Capsule governance contract proven by Node.js while providing idiomatic Python, async, and FastAPI-friendly integration.

The most important Python Runtime rule is:

> Add Python support as a compatible extension for AI-era services and workers, while preserving predefined actions, secretRef boundaries, and the shared Capsule governance model.
