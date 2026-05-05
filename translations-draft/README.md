---
status: draft
audience: maintainers, ai-coding-agents
stability: machine-assisted-draft
last_reviewed: 2026-05-05
---

# Translation Drafts

Machine-assisted Chinese translations and translation tooling for the
`xtrape-capsule-docs` knowledge base.

> **Status: machine-assisted draft.** Files in this folder are **not**
> authoritative. English documents in the parent directory are canonical.
> Do not extract content from these drafts directly into public site
> documentation without a human-reviewed pass.

## Contents

- `README_zh.md` — early Chinese translation of the docs root README.
- `TRANSLATION_GUIDE_zh.md` — guidance for the translation pass.
- `TRANSLATION_MANIFEST.txt` — file-level tracking of what has been
  translated and what is still in English.
- `TRANSLATION_TEMPLATE_zh.md` — boilerplate frontmatter and section
  scaffolding for new Chinese pages.
- `translate_to_chinese.py` — helper script used to seed the initial
  drafts.

## Authority order

When private design documents must be referenced, the canonical English
file in the parent directory always wins over the draft Chinese file in
this folder. See `../AI_READING_GUIDE.md`.

## Cleanup status

These drafts are kept here so that future translation work can resume
without starting over. They will be either:

1. promoted to authoritative Chinese pages alongside the English
   originals (after human review), or
2. retired once an authoritative Chinese tree exists.

Until then, treat everything here as **draft**.
