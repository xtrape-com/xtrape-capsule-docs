# AGENTS.md

## Repository Role

This repository owns long-form planning, architecture, decisions, and promotion materials for Xtrape Capsule.

It should reflect implemented or intentionally planned behavior without defining runtime behavior by itself.

## Version / Release Train Rules

During development:
- Before starting implementation, run `git fetch --all --prune` and check whether the current branch is behind its upstream. Pull or rebase the latest upstream code before editing, unless local uncommitted work must first be stashed or committed.
- Do not assume unpublished npm versions, Docker tags, or release artifacts exist.
- Keep roadmap wording aligned with CE, Agent SDK, Contracts, Demo, OpHub, and Site implementation state.

## Documentation Rules

- Mark future or experimental work explicitly.
- Do not document future behavior as shipped.
- Keep roadmap, ADRs, and implementation notes consistent when release scope changes.

## Development Commands

This repository is mostly Markdown. Use repository-local checks if they are added later.
