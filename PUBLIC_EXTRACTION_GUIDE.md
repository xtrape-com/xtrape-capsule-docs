---
status: implemented
audience: maintainers
stability: stable
last_reviewed: 2026-05-05
---

# Public Extraction Guide

## Purpose

This guide defines how stable private design content can be rewritten into public product documentation.

## Public Target

The public-facing target repository is:

```text
xtrape-capsule-site
```

The private design repository should never be copied wholesale into the public site.

## Rules

1. Do not copy internal planning text directly.
2. Remove commercial planning details unless approved.
3. Remove patent, moat, pricing, security-sensitive, and internal roadmap details.
4. Rewrite design language into user-facing language.
5. Prefer examples using:
   - integration services;
   - automation workers;
   - background jobs;
   - account pools;
   - agent runtimes.
6. Do not mention CAPI in public docs unless explicitly approved.
7. Public docs should be concise, actionable, stable, and verifiable.
8. Do not publish claims about npm packages, Docker images, GitHub Releases, or hosted services until they are actually available.

## Extraction Checklist

- [ ] Source doc status is `accepted` or `implemented`.
- [ ] No internal-only business content remains.
- [ ] No sensitive implementation details remain.
- [ ] No raw tokens, credentials, private URLs, or screenshots with private data remain.
- [ ] Public wording is aligned with `xtrape-capsule-site` positioning.
- [ ] Links are updated to public URLs.
- [ ] Future EE/Cloud capabilities are marked as planned/future.
- [ ] A maintainer has reviewed the extracted public text.
