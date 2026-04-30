# CE v0.1 Supply Chain (SBOM and License Scanning)

- Status: Implementation Guidance
- Edition: CE
- Priority: Current
- Audience: DevOps engineers, security reviewers, founders, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs disagree, the ADRs win for CE v0.1.

This document describes the supply-chain hygiene requirements for Opstage CE v0.1. Goals:

- make it easy to answer "what's in the image?" for security reviews;
- catch incompatible OSS licenses before merge;
- expose dependency vulnerabilities at PR time.

## 1. License Policy

CE v0.1 is published under a permissive open-source license (see top-level `LICENSE`). All transitive dependencies MUST carry an SPDX-recognised license that is compatible with that policy.

Allowed licenses (from `pnpm dlx license-checker --onlyAllow`):

```text
MIT
Apache-2.0
BSD-2-Clause
BSD-3-Clause
ISC
0BSD
Unlicense
CC0-1.0
Python-2.0
BlueOak-1.0.0
```

Not allowed (PR MUST be blocked):

```text
GPL-*       # any GPL family — viral, incompatible with permissive distribution
AGPL-*      # never
LGPL-*      # only via dynamic-link runtime; case-by-case ADR required
SSPL        # not OSI; never
EPL-1.0/2.0 # case-by-case ADR required
Custom commercial / proprietary
```

Exception process:

1. Open an issue describing the dependency, the license, and the reason it cannot be replaced.
2. Open an ADR under `08-decisions/00NN-license-exception-<package>.md`.
3. Update the allowed list above only after the ADR is accepted.

## 2. SBOM

CE v0.1 publishes a CycloneDX SBOM with every release.

```text
Format:    CycloneDX 1.5 (JSON)
Tool:      @cyclonedx/cdxgen   (preferred; multi-language)
Scope:     production runtime  (no devDependencies)
Artifacts: sbom.json           (attached to the GitHub Release)
           sbom.json           (also baked into the image at /app/sbom.json)
```

Generation command (also wired into `release.yml`, see `06-ci-cd-pipelines.md` §3.3):

```bash
pnpm dlx @cyclonedx/cdxgen@^11 -t pnpm -o sbom.json
```

The Docker image MUST embed `/app/sbom.json` and expose it via:

```text
GET /api/system/sbom        (System API; unauthenticated; returns CycloneDX JSON)
```

Adding this endpoint is OPTIONAL for CE v0.1; the GitHub Release attachment is the primary distribution channel. If implemented, the endpoint MUST be served from the System API namespace per ADR 0002.

## 3. Vulnerability Scanning

Three layers, each running automatically:

| Layer            | Tool                            | Trigger                            | Failure                                         |
|------------------|---------------------------------|------------------------------------|-------------------------------------------------|
| Dep manifest     | `pnpm audit --audit-level=high` | every PR + weekly cron             | block PR on `high`/`critical`                  |
| Static analysis  | GitHub CodeQL (TypeScript)      | every PR + weekly cron             | block PR on new `error`-severity finding        |
| Container image  | Trivy (image scan)              | on tag, against the published image| block release on `CRITICAL` or unfixed `HIGH`   |

Recommended Trivy invocation:

```bash
trivy image --severity HIGH,CRITICAL --exit-code 1 \
  ghcr.io/<org>/opstage:${TAG}
```

The `release.yml` workflow described in `06-ci-cd-pipelines.md` §3.3 SHOULD be extended with a Trivy step before pushing the `:latest` tag.

## 4. Dependency Pinning

- All `package.json` entries MUST use exact-or-caret versions in lockfile (`pnpm-lock.yaml` is the source of truth).
- `pnpm install --frozen-lockfile` is enforced in CI (`06-ci-cd-pipelines.md` §3.1).
- Renovate (or Dependabot) MUST be configured to open weekly grouped PRs for non-breaking updates and immediate PRs for security advisories.

Recommended `renovate.json`:

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended", ":semanticCommits"],
  "labels": ["dependencies"],
  "schedule": ["before 9am on monday"],
  "vulnerabilityAlerts": { "labels": ["security"], "schedule": ["at any time"] },
  "packageRules": [
    { "matchDepTypes": ["devDependencies"], "groupName": "dev deps", "automerge": false },
    { "matchUpdateTypes": ["pin", "patch"], "automerge": true },
    { "matchPackageNames": ["prisma", "@prisma/*"], "groupName": "prisma" },
    { "matchPackageNames": ["fastify", "@fastify/*"], "groupName": "fastify" }
  ]
}
```

## 5. Container Provenance

Tag-triggered builds in `release.yml` set:

```yaml
provenance: true
sbom:       true
```

This ensures GitHub Container Registry stores SLSA build provenance and an in-registry SBOM for `ghcr.io/<org>/opstage:<tag>`.

## 6. Acceptance Criteria

- License-checker step passes locally and in CI on every PR.
- A `vX.Y.Z` GitHub Release has both `sbom.json` and the multi-arch image attached.
- `trivy image --severity HIGH,CRITICAL` exits 0 on the freshly published image.
- CodeQL alerts are clean or have explicit dismissals with rationale committed via PR.
- `pnpm audit --audit-level=high` returns no advisories on `main`.

## 7. Future Extensions (NOT in CE v0.1)

- Sigstore / cosign signing of images.
- in-toto attestations.
- npm provenance for `@xtrape/capsule-agent-node` (planned for the first SDK npm release).
- Reproducible builds.
