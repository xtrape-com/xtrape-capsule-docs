---
status: implemented
audience: maintainers
stability: stable
last_reviewed: 2026-05-05
---

# Sensitive Content Checklist

## Purpose

This repository is private, so design discussions may include sensitive or future-looking terms. The goal is not to ban
those terms. The goal is to identify content that must be reviewed before any public release, migration, screenshot, or
extraction into `xtrape-capsule-site`.

## Suggested Scan

Run from the repository root:

```bash
rg -n "CAPI|capi|patent|专利|moat|护城河|secret|token|cookie|session|API key|apikey|pricing|billing|license|Cloud|EE|SaaS|password|credential"
```

## Private-Allowed Content

The following may be acceptable in this private repository when intentional:

- architecture trade-offs;
- future EE/Cloud planning;
- internal implementation constraints;
- security model drafts;
- threat model notes;
- commercial planning drafts;
- migration notes for public wording.

## Public-Unsafe Content

Review or remove before public extraction:

- raw tokens, passwords, API keys, cookies, OTPs, browser session data;
- private URLs, private account emails, customer names, and internal environment names;
- sensitive exploit details;
- pricing or licensing plans not approved for public release;
- moat/patent/commercial strategy;
- unapproved CAPI-specific positioning;
- screenshots containing operational or account data.

## Before Making This Repository Public

- [ ] Run the scan command above.
- [ ] Review all matches manually.
- [ ] Remove `.DS_Store` and generated files.
- [ ] Confirm public claims are accurate.
- [ ] Confirm Chinese translation drafts are not presented as final docs.
- [ ] Confirm future EE/Cloud items are clearly marked as future/planned.
