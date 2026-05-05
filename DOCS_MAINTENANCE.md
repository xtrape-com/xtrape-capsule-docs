---
status: implemented
audience: maintainers
stability: stable
last_reviewed: 2026-05-05
---

# Docs Maintenance Guide

## Markdown Formatting

This repository intentionally avoids a mandatory Node toolchain for private design docs. Use readable Markdown conventions:

- one heading per line;
- blank line before and after headings;
- blank line before and after fenced code blocks;
- one list item per line;
- readable tables in raw GitHub view;
- avoid very long prose lines;
- do not compress whole documents into a single line.

Suggested optional formatting command if Prettier is available locally:

```bash
prettier --write '**/*.{md,yml,yaml,json}'
```

## Frontmatter Metadata

Major documents should include frontmatter:

```yaml
---
status: draft
audience: architects
stability: evolving
last_reviewed: 2026-05-05
---
```

Use `status`, `audience`, and `stability` to help humans and AI coding agents distinguish current implementation requirements from drafts and future planning.

## Link Checking

If a link checker is available locally, run one of:

```bash
markdown-link-check README.md
lychee README.md "**/*.md"
```

Prioritize internal links between ADRs, specs, contracts, and current implementation docs.

## Translation Files

Files ending in `_zh.md` are draft/machine-assisted unless explicitly reviewed. English documents are canonical unless a document says otherwise.
