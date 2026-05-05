---
status: accepted
audience: ai-coding-agents
stability: stable
last_reviewed: 2026-05-05
---

# Architecture Decision Records

- Status: Implementation Guidance
- Edition: Shared
- Priority: High
- Audience: founders, architects, product designers, backend developers, frontend developers, agent SDK developers, AI coding agents

This directory contains architecture and product decisions that constrain implementation.

For CE v0.1, read in this order:

```text
08-decisions/0001-ce-v01-implementation-baseline.md
08-decisions/0002-api-namespace-convention.md
08-decisions/0003-command-action-lifecycle.md
08-decisions/0004-security-defaults.md
08-decisions/0005-technology-stack-decision.md
08-decisions/0006-logging-and-observability.md
08-decisions/0007-ui-state-and-data-fetching.md
08-decisions/0008-naming-and-repositories.md
08-decisions/0009-contracts-spec-and-bindings.md
```

When implementation documents disagree, accepted ADRs should be treated as the higher-priority current decision until the conflicting documents are updated.

## ADR Template

New ADRs should use this structure:

```md
# ADR-000X: Title

## Status

Accepted / Proposed / Superseded / Deprecated

## Date

YYYY-MM-DD

## Context

What problem or decision pressure led to this decision?

## Decision

What was decided?

## Consequences

What becomes easier? What becomes harder? What trade-offs are accepted?

## Alternatives Considered

What options were considered and rejected?

## Implementation Notes

Where is this decision reflected in code/docs?

## Supersedes / Superseded By

Optional.
```
