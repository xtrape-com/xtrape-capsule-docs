---
status: implemented
audience: ai-coding-agents
stability: stable
last_reviewed: 2026-05-05
---

# AI Reading Guide

## Purpose

This guide tells AI coding agents how to read this private design repository before modifying Xtrape Capsule code.

This repository is not the public website. It is a private source of design truth containing accepted decisions, drafts,
implementation guidance, future planning, and internal notes.

## Authority Order

When documents disagree, use this authority order:

1. Accepted ADRs in `08-decisions/`.
2. Accepted specs in `02-specs/` and machine-readable contracts in `09-contracts/`.
3. Current CE implementation guidance in `10-implementation/`.
4. Roadmap documents in `07-roadmap/`.
5. Draft or proposed specs.
6. Historical notes, translation drafts, and planning documents.

Do not silently override accepted ADRs. If a code change requires changing architecture, propose an ADR update.

## Required Reading for CE Backend Work

1. `README.md`.
2. `08-decisions/README.md`.
3. `08-decisions/0001-ce-v01-implementation-baseline.md`.
4. `08-decisions/0002-api-namespace-convention.md`.
5. `08-decisions/0004-security-defaults.md`.
6. `09-contracts/openapi/opstage-ce-v0.1.yaml`.
7. Relevant files under `10-implementation/`.

## Required Reading for CE Frontend Work

1. `README.md`.
2. `08-decisions/0007-ui-state-and-data-fetching.md`.
3. `04-opstage/01-opstage-ui.md`.
4. `09-contracts/openapi/opstage-ce-v0.1.yaml`.
5. Relevant files under `10-implementation/`.

## Required Reading for Agent SDK Work

1. `README.md`.
2. `05-agents/00-agent-overview.md`.
3. `05-agents/01-embedded-agent.md`.
4. `05-agents/04-node-agent-sdk.md`.
5. `08-decisions/0003-command-action-lifecycle.md`.
6. `08-decisions/0009-contracts-spec-and-bindings.md`.

## Required Reading for Contract Work

1. `README.md`.
2. `02-specs/README.md`.
3. Relevant spec under `02-specs/`.
4. `08-decisions/0009-contracts-spec-and-bindings.md`.
5. `09-contracts/README.md`.
6. `09-contracts/openapi/opstage-ce-v0.1.yaml`.

## Do Not Treat as Current Requirements

Do not treat these as current CE implementation requirements unless an accepted ADR explicitly says so:

- future EE planning;
- future Cloud planning;
- draft specs;
- obsolete or superseded documents;
- machine-assisted Chinese translations;
- roadmap ideas without implementation status.

## Output Expectations for AI Agents

When making changes:

- cite which docs were followed;
- identify conflicts if found;
- state whether the change follows accepted ADRs;
- keep public wording out of private design notes unless explicitly requested;
- update OpenAPI/contracts/tests when wire behavior changes;
- propose ADR updates when architecture changes are required.
