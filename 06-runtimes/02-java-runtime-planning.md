# Java Runtime Planning

- Status: Planning
- Edition: Shared
- Priority: Future

本文件属于 `xtrape-capsule` 文档集。`xtrape-capsule` 是面向轻服务 / Capsule Service 的领域体系；`xtrape-capsule-opstage` 是该体系下的统一运行态治理平台。

当前实现重点是 CE 开源社区版。EE 私有化商业版与 Cloud SaaS 版属于未来规划，CE 需要保留扩展点，但不应在早期版本实现其完整能力。

运行时文档定义不同语言生态下如何接入 Capsule 规范和 Agent 能力。当前优先 Node.js，Java/Python 作为后续规划。

# Java Runtime Planning

- Status: Planning
- Edition: EE
- Priority: Future
- Audience: architects, Java developers, Spring Boot developers, agent SDK developers, backend developers, AI coding agents

This document defines the planned **Java Runtime** integration for the `xtrape-capsule` product family.

Java Runtime is a future extension. It is not a CE v0.1 implementation requirement.

The current CE implementation focus is **Node.js**. Java Runtime planning exists to keep the Capsule governance model compatible with enterprise Java and Spring-based services in future EE or later CE versions.

---

## 1. Purpose

The purpose of Java Runtime planning is to define how Java services may become Capsule Services governed by Opstage.

Java Runtime should eventually define:

- Java service identity conventions;
- Java Agent SDK package structure;
- Spring Boot starter direction;
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

Java Runtime should adapt the Capsule model to Java idioms without redefining the model.

---

## 2. Runtime Scope

Future Java Runtime may include:

```text
Java Embedded Agent SDK
Spring Boot starter
service identity declaration
health provider bridge
config metadata provider
predefined action registry
HTTP polling command delivery
CommandResult reporting
file-based or environment-based Agent token store
safe logging
Spring Boot demo service
```

Java Runtime should not initially include:

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

Java Runtime is not required for CE v0.1.

CE may reserve shared concepts that make Java integration easier later:

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

But CE should not implement Java SDK, Maven artifacts, or Spring Boot starter in v0.1.

---

## 4. Target Java Ecosystems

Java Runtime should primarily target:

```text
Spring Boot
Spring Cloud
plain Java services
xtrape Java ecosystem services
```

Recommended first target:

```text
Spring Boot
```

because it provides mature lifecycle hooks, configuration conventions, actuator health concepts, and enterprise adoption.

---

## 5. Package Direction

Possible Maven artifact names:

```text
xtrape-capsule-agent-java
xtrape-capsule-agent-spring-boot-starter
```

Possible group ID:

```text
io.xtrape.capsule
```

or:

```text
com.xtrape.capsule
```

The final group/package naming should follow the broader xtrape repository and publishing conventions.

Recommended package roles:

| Artifact | Purpose |
|---|---|
| `xtrape-capsule-agent-java` | core Java Agent SDK |
| `xtrape-capsule-agent-spring-boot-starter` | Spring Boot auto-configuration and annotations |
| `xtrape-capsule-agent-test` | future test helpers if needed |

---

## 6. Java Embedded Agent Model

The first Java Runtime model should be Embedded Agent.

Recommended structure:

```text
Java / Spring Boot process
├── business logic
├── Spring context
└── Java Embedded Agent SDK
    ├── registration client
    ├── token store
    ├── heartbeat scheduler
    ├── manifest reporter
    ├── health provider bridge
    ├── config metadata provider
    ├── action registry
    ├── command polling scheduler
    └── CommandResult reporter
```

The Java Agent should run inside the service process but should avoid destabilizing the business runtime.

---

## 7. Spring Boot Starter Direction

A Spring Boot starter may provide:

- auto-configuration;
- configuration properties;
- Agent bean creation;
- lifecycle integration;
- scheduled heartbeat;
- scheduled command polling;
- Actuator health bridge;
- annotation-based action registration;
- config metadata provider discovery;
- safe logging defaults.

Possible starter class:

```java
@Configuration
@EnableConfigurationProperties(CapsuleAgentProperties.class)
public class CapsuleAgentAutoConfiguration {
}
```

This is planning only and not a CE v0.1 implementation target.

---

## 8. Configuration Model

Spring Boot configuration may use properties:

```yaml
xtrape:
  capsule:
    agent:
      enabled: true
      backend-url: http://localhost:8080
      registration-token: ${OPSTAGE_REGISTRATION_TOKEN:}
      token-file: ./data/agent-token.json
      code: local-java-agent
      name: Local Java Agent
      heartbeat-interval: 30s
      command-poll-interval: 5s
    service:
      code: demo-java-capsule-service
      name: Demo Java Capsule Service
      description: A demo Java Capsule Service for Opstage.
      version: 0.1.0
      runtime: java
```

Environment variables may map naturally through Spring Boot relaxed binding.

Sensitive values such as registration token must not be logged.

---

## 9. Service Identity

Java Capsule Service identity should be stable.

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

```yaml
xtrape:
  capsule:
    service:
      code: demo-java-capsule-service
      name: Demo Java Capsule Service
      version: 0.1.0
      runtime: java
```

Rules:

- `code` must be stable across restarts;
- `runtime` should be `java`;
- version should match application version where practical;
- metadata should not contain raw secrets.

---

## 10. Agent Token Store

Java Runtime may support a file-based token store first.

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

- OS keychain;
- Kubernetes Secret;
- Vault-backed token store;
- custom TokenStore interface.

---

## 11. Health Integration

Spring Boot Runtime may integrate with Spring Boot Actuator Health.

Potential mapping:

```text
Actuator UP       -> Capsule HealthStatus UP
Actuator DOWN     -> Capsule HealthStatus DOWN
Actuator OUT_OF_SERVICE -> Capsule HealthStatus DEGRADED or DOWN
unknown/error     -> Capsule HealthStatus UNKNOWN
```

Possible custom provider interface:

```java
public interface CapsuleHealthProvider {
    CapsuleHealthReport health();
}
```

Rules:

- health provider should be lightweight;
- exceptions should not crash the service;
- health output must not include raw secrets;
- dependency details should be sanitized.

---

## 12. Config Metadata Integration

Java Runtime may expose config metadata from explicit providers.

Possible interface:

```java
public interface CapsuleConfigProvider {
    List<CapsuleConfigItem> configs();
}
```

Possible item fields:

```text
key
label
type
currentValue
defaultValue
editable
sensitive
source
description
validation
metadata
```

Rules:

- report metadata, not full config-center behavior;
- sensitive values must be masked or represented as `secretRef`;
- raw passwords, tokens, cookies, and API keys must not be reported;
- config editing and publishing are future EE capabilities.

---

## 13. Action Registration

Java Runtime may support two action registration styles.

### 13.1 Programmatic registry

Example:

```java
capsuleAgent.action(CapsuleActionDefinition.builder()
    .name("runHealthCheck")
    .label("Run Health Check")
    .dangerLevel(DangerLevel.LOW)
    .handler(context -> ActionResult.success("Health check completed"))
    .build());
```

### 13.2 Annotation-based registration

Example:

```java
@CapsuleAction(
    name = "reloadCache",
    label = "Reload Cache",
    dangerLevel = DangerLevel.MEDIUM
)
public ActionResult reloadCache(ReloadCacheRequest request) {
    return ActionResult.success("Cache reloaded");
}
```

The first implementation should prefer the simpler programmatic registry unless annotation processing is clearly needed.

---

## 14. Command Execution

Java Runtime should follow the same Command flow as Node.js:

```text
Agent polls Backend for Commands
    ↓
Backend returns Commands assigned to this Agent
    ↓
Agent validates command type and action name
    ↓
Agent executes local Java action handler
    ↓
Agent captures success or failure
    ↓
Agent reports CommandResult
```

Initial supported command type:

```text
ACTION
```

Java Runtime must not expose arbitrary shell execution.

---

## 15. CommandResult Reporting

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

## 16. Lifecycle Integration

Spring Boot starter may hook into application lifecycle.

Recommended behavior:

```text
ApplicationReadyEvent
    ↓
Agent loads token or registers
    ↓
Agent reports manifest
    ↓
Agent starts heartbeat scheduler
    ↓
Agent starts command polling scheduler
```

On shutdown:

```text
ContextClosedEvent
    ↓
Agent stops schedulers
    ↓
Agent lets in-flight command finish if practical
```

Backend should infer offline state from heartbeat timeout.

---

## 17. Backend Downtime Behavior

Java Runtime should tolerate Opstage Backend downtime.

If Backend is unavailable, Java Agent should:

- keep business service running by default;
- retry heartbeat/reporting/polling with backoff;
- avoid log spam;
- re-report manifest after reconnect if needed;
- resume command polling after recovery.

A strict mode may be added for services that require governance availability.

Default behavior should favor service availability.

---

## 18. Sensitive Data Rules

Java Runtime must avoid leaking sensitive data.

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
```

Rules:

- do not log registration token;
- do not log Agent token;
- do not report raw secrets in configs;
- do not return raw secrets in CommandResult;
- do not include raw secrets in health details;
- use `secretRef` for sensitive references;
- sanitize logs and errors where practical.

---

## 19. Demo Java Service Direction

A future Java demo service should prove:

- Spring Boot application starts;
- Agent registers with Opstage;
- Agent token is stored and reused;
- heartbeat works;
- manifest report works;
- health bridge works;
- config metadata provider works;
- actions are reported;
- `echo` action works;
- `runHealthCheck` action works;
- CommandResult is reported;
- AuditEvent appears in Opstage;
- Backend downtime does not crash the service by default.

This demo is future work, not CE v0.1.

---

## 20. Testing Direction

Future Java Runtime tests should cover:

- configuration binding;
- token store read/write;
- registration success/failure;
- Agent token invalid handling;
- heartbeat success/failure;
- manifest construction;
- health provider success/error;
- Actuator health mapping if supported;
- config provider output;
- action registration;
- command polling;
- action execution success/failure;
- CommandResult reporting;
- Backend unavailable behavior;
- sensitive data sanitization.

Tests should use mocked HTTP clients or local test servers.

---

## 21. Maven and Build Direction

Future Java SDK may use:

```text
Maven or Gradle
Java 17+
Spring Boot 3.x for starter
JUnit 5
Mockito or equivalent
```

Recommended baseline:

```text
Java 17+
Spring Boot 3.x
```

because modern Spring Boot enterprise environments commonly target Java 17 or newer.

The exact build system should align with the broader xtrape repository strategy.

---

## 22. Future EE Direction

Future EE may include Java Runtime as an enterprise feature because many enterprise systems are Java-based.

Possible EE capabilities:

- official Java Agent SDK;
- Spring Boot starter;
- Spring Cloud integration examples;
- Actuator health bridge;
- enterprise deployment guide;
- Java diagnostics;
- Java compatibility matrix;
- token rotation support;
- secret provider hooks;
- command progress support;
- config reload helper.

---

## 23. Future Cloud Direction

Future Cloud may include Java Runtime support through:

- Cloud enrollment snippets;
- workspace-scoped registration token examples;
- Agent Gateway configuration;
- Cloud connection diagnostics;
- Java-specific quick start;
- managed alert hints;
- usage metering metadata.

These are future planning items.

---

## 24. Anti-Patterns

Avoid these patterns.

### 24.1 Java SDK before Node.js CE is stable

The first milestone is proving the governance loop with Node.js.

### 24.2 Java Runtime redefines the Capsule model

Java should adapt the shared model, not create a separate one.

### 24.3 Spring Boot starter hides all behavior

Auto-configuration should be convenient, but action exposure and security-sensitive behavior must remain explicit.

### 24.4 Java Runtime exposes shell execution

Remote shell is not the Capsule operation model.

### 24.5 Health/config providers leak secrets

Use `secretRef` or masking.

### 24.6 Backend outage crashes business service by default

Governance outage should not automatically become business outage.

---

## 25. Acceptance Criteria for Future Java Runtime

A future Java Runtime implementation is acceptable when:

- Java/Spring Boot service can include the Java Agent dependency;
- service identity is declared;
- Agent can register with registration token;
- Agent token is stored and reused;
- heartbeat works;
- manifest report works;
- health provider or Actuator bridge works;
- config provider works;
- actions are reported;
- `echo` action works;
- `runHealthCheck` action works;
- CommandResult is reported;
- Opstage UI shows Agent, service, health, configs, actions, Commands, and AuditEvents;
- Backend downtime does not crash the service by default;
- raw tokens are not logged;
- raw secrets are not reported;
- no arbitrary shell execution is provided by default.

---

## 26. Summary

Java Runtime is a future integration direction for enterprise Java and Spring-based Capsule Services.

It should reuse the same Capsule governance contract proven by Node.js while providing idiomatic Java and Spring Boot integration.

The most important Java Runtime rule is:

> Add Java support as a compatible extension of the shared Capsule governance model, not as a second framework with different semantics.