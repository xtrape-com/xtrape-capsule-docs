# CE v0.1 Node Agent SDK Scaffold Plan

- Status: Implementation Guidance
- Edition: CE
- Priority: Current
- Audience: agent SDK developers, Capsule Service developers, backend developers, test engineers, AI coding agents

## 1. Goal

Build the Node Embedded Agent SDK for CE v0.1.

The SDK should make it easy for a Node.js Capsule Service to register with Opstage, report metadata, poll Commands, execute predefined actions, and report results safely.

## 2. Package

Recommended package:

```text
packages/agent-node
```

Published name:

```text
@xtrape/capsule-agent-node
```

## 3. Runtime

```text
Node.js 20 LTS or later
TypeScript-first
ESM-first if repository standard allows it
```

## 4. Source Layout

```text
packages/agent-node/src/
├── index.ts
├── capsule-agent.ts
├── types.ts
├── client/
│   ├── agent-api-client.ts
│   └── errors.ts
├── token-store/
│   ├── token-store.ts
│   └── file-token-store.ts
├── providers/
│   ├── health-provider.ts
│   ├── config-provider.ts
│   └── action-registry.ts
├── loops/
│   ├── heartbeat-loop.ts
│   └── command-polling-loop.ts
├── security/
│   └── redaction.ts
└── tests/
```

## 5. Public API

Target usage:

```ts
import { CapsuleAgent } from '@xtrape/capsule-agent-node';

const agent = new CapsuleAgent({
  backendUrl: process.env.OPSTAGE_BACKEND_URL ?? 'http://localhost:8080',
  registrationToken: process.env.OPSTAGE_REGISTRATION_TOKEN,
  tokenStore: {
    file: process.env.OPSTAGE_AGENT_TOKEN_FILE ?? './data/agent-token.json',
  },
  agent: {
    code: process.env.OPSTAGE_AGENT_CODE ?? 'local-node-agent',
    name: process.env.OPSTAGE_AGENT_NAME ?? 'Local Node Agent',
  },
  service: {
    code: 'demo-capsule-service',
    name: 'Demo Capsule Service',
    version: '0.1.0',
    runtime: 'nodejs',
  },
});

agent.health(async () => ({
  status: 'UP',
  message: 'Demo service is healthy.',
}));

agent.configs(() => [
  {
    key: 'demo.message',
    label: 'Demo Message',
    type: 'string',
    valuePreview: 'hello capsule',
    editable: false,
    sensitive: false,
    source: 'env',
  },
]);

agent.action({
  name: 'echo',
  label: 'Echo',
  dangerLevel: 'LOW',
  handler: async payload => ({
    success: true,
    data: payload,
  }),
});

await agent.start();
```

## 6. Required Capabilities

SDK v0.1 must support:

- registration with registration token;
- Agent token persistence;
- heartbeat loop;
- service report;
- health provider;
- config provider;
- action registry;
- command polling loop;
- dispatch to local action handlers;
- CommandResult reporting;
- retry/backoff;
- safe logging and redaction;
- graceful stop.

## 7. Token Store

Default file token store:

```text
./data/agent-token.json
```

Rules:

- create parent directory if needed;
- restrict file permissions where practical;
- never log raw token;
- if Agent token is rejected, surface a clear re-registration error.

## 8. Command Handling

When polling returns Commands, SDK should:

1. find local action handler by `actionName`;
2. if missing, report failure result;
3. execute with timeout if timeout is provided;
4. catch exceptions;
5. report success or failure;
6. avoid leaking secrets in logs.

## 9. Backend Downtime Behavior

SDK should:

- retry transient network failures;
- use backoff with maximum delay;
- continue local service execution;
- avoid crashing the Capsule Service by default;
- expose lifecycle events or callbacks for observability.

## 10. Test Plan

Minimum SDK tests:

- registers with registration token;
- stores Agent token;
- reuses stored Agent token;
- sends heartbeat;
- reports service metadata;
- polls and executes `echo` Command;
- reports failed Command when handler throws;
- redacts tokens from logs;
- retries transient Backend failure.
