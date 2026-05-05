---
status: implemented
audience: ai-coding-agents
stability: stable
last_reviewed: 2026-05-05
---

# Repository Map

## Repository Role

`xtrape-capsule-docs` is the private design knowledge base and source of design truth for the Xtrape Capsule product family.

The public product documentation lives in `xtrape-capsule-site`.

## Top-level Files

| Path | Purpose |
| --- | --- |
| `README.md` | Repository role, private notice, reading order. |
| `AI_READING_GUIDE.md` | Authority order and task-specific reading paths for AI agents. |
| `PUBLIC_EXTRACTION_GUIDE.md` | Safe process for rewriting private content into public docs. |
| `SENSITIVE_CONTENT_CHECKLIST.md` | Scan terms and review checklist before public extraction. |
| `REPO_MAP.md` | This map. |
| `CHANGELOG.md` | Design documentation change history. |

## Top-level Directories

| Directory | Role | Authority |
| --- | --- | --- |
| `01-capsule/` | Core concepts and domain model. | Foundational, evolving. |
| `02-specs/` | Shared Capsule and Opstage specifications. | Accepted/evolving specs. |
| `03-editions/` | CE/EE/Cloud edition boundaries. | CE current; EE/Cloud future. |
| `04-opstage/` | Opstage runtime governance design. | Current for CE where aligned with ADRs. |
| `05-agents/` | Agent system design. | Current for Node embedded Agent; future for sidecar/external. |
| `06-runtimes/` | Runtime planning. | Node current; Java/Python future. |
| `07-roadmap/` | Product and engineering sequencing. | Planning, not direct requirements. |
| `08-decisions/` | ADRs. | Highest authority when accepted. |
| `09-contracts/` | OpenAPI, Prisma review copy, errors, contract artifacts. | Wire-level implementation authority. |
| `10-implementation/` | Current CE implementation plans and runbooks. | Current when marked CE/current. |

## Authoritative Reading Path Before Coding

1. `AI_READING_GUIDE.md`.
2. Accepted ADRs in `08-decisions/`.
3. Accepted specs in `02-specs/` and `09-contracts/`.
4. CE implementation guidance in `10-implementation/`.
5. Relevant concept or agent/opstage docs.

## Draft / Future / Historical Content

- EE and Cloud docs are future planning unless explicitly marked current.
- Translation files ending in `_zh.md` are draft/machine-assisted unless explicitly reviewed.
- Roadmap docs describe sequencing and intent; they are not implementation contracts by themselves.
