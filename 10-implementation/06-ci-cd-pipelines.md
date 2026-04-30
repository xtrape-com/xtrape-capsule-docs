# CE v0.1 CI/CD Pipelines

- Status: Implementation Guidance
- Edition: CE
- Priority: Current
- Audience: DevOps engineers, backend developers, frontend developers, agent SDK developers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs disagree, the ADRs win for CE v0.1.

## 1. Goal

Define the CI/CD pipeline for Opstage CE v0.1 on GitHub Actions. Pipelines should:

- run on every PR;
- block merge on test/lint/typecheck/contract failures;
- publish Docker images on tag pushes;
- never publish a release with failing checks.

CE v0.1 targets GitHub Actions specifically because it is the de-facto standard for open-source repos. Mirroring to GitLab CI / CircleCI is out of scope.

## 2. Pipeline Stages

```text
1. install                pnpm install --frozen-lockfile
2. lint                   pnpm -r lint
3. typecheck              pnpm -r typecheck
4. contracts              validate OpenAPI + Prisma + ID/token unit tests
5. unit                   pnpm -r test --reporter=junit
6. integration            backend + agent contract tests against temp SQLite
7. build                  pnpm -r build
8. docker (optional)      build + push opstage image (only on tag push)
```

Stages 1-7 run on every PR; stage 8 only runs on tags matching `v*.*.*`.

## 3. Required GitHub Actions Workflows

The implementation MUST add at least the following workflow files. Pseudo-content is provided; teams may iterate but the surface MUST stay equivalent.

### 3.1 `.github/workflows/ci.yml`

```yaml
name: ci
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm -r lint
      - run: pnpm -r typecheck
      - run: pnpm --filter @xtrape/capsule-contracts run check
      - run: pnpm --filter @xtrape/capsule-db run validate
      - run: pnpm -r test -- --run --reporter=verbose
      - run: pnpm -r build
      - name: Upload coverage
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: '**/coverage/**'
          if-no-files-found: ignore
```

### 3.2 `.github/workflows/contracts.yml`

```yaml
name: contracts
on:
  pull_request:
    paths:
      - 'xtrape-capsule-docs/09-contracts/**'
      - 'packages/contracts/**'
      - 'packages/db/**'
permissions:
  contents: read
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - name: Validate OpenAPI
        run: pnpm --package=@redocly/cli dlx redocly lint xtrape-capsule-docs/09-contracts/openapi/opstage-ce-v0.1.yaml
      - name: Validate Prisma schema
        run: pnpm dlx prisma@latest validate --schema xtrape-capsule-docs/09-contracts/prisma/schema.prisma
      - name: Contract drift check
        run: pnpm --filter @xtrape/capsule-contracts run drift-check
```

`drift-check` is a script in `packages/contracts` that compares generated TypeScript types against the OpenAPI YAML and exits non-zero on diff (recommended via `openapi-typescript` + `git diff --exit-code`).

### 3.3 `.github/workflows/release.yml`

```yaml
name: release
on:
  push:
    tags: ['v*.*.*']
permissions:
  contents: write
  packages: write
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-qemu-action@v3
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - name: Build and push opstage image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: deploy/docker/opstage.Dockerfile
          platforms: linux/amd64,linux/arm64
          push: true
          provenance: true
          sbom: true
          tags: |
            ghcr.io/${{ github.repository_owner }}/opstage:${{ github.ref_name }}
            ghcr.io/${{ github.repository_owner }}/opstage:latest
      - name: Generate SBOM (CycloneDX)
        run: pnpm dlx @cyclonedx/cdxgen@^11 -t pnpm -o sbom.json
      - name: Attach SBOM and changelog to GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          files: sbom.json
```

Tag rules:

- `vX.Y.Z` triggers a Docker push and creates a GitHub Release.
- Pre-release tags (`vX.Y.Z-rc.N`) push to `:rc-X.Y.Z-rc.N` only.
- Branch pushes to `main` MUST NOT publish images.

### 3.4 `.github/workflows/security.yml`

```yaml
name: security
on:
  schedule:
    - cron: '0 7 * * 1'   # weekly, Mondays 07:00 UTC
  pull_request:
    branches: [main]
permissions:
  contents: read
  security-events: write
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - name: pnpm audit (high+)
        run: pnpm audit --prod --audit-level=high
      - name: License scan
        run: pnpm dlx license-checker --production --onlyAllow "MIT;Apache-2.0;BSD-2-Clause;BSD-3-Clause;ISC;0BSD;Unlicense;CC0-1.0;Python-2.0;BlueOak-1.0.0"
  codeql:
    uses: github/codeql-action/.github/workflows/codeql-analysis.yml@v3
    with:
      languages: javascript-typescript
```

## 4. Required Status Checks

Branch protection on `main` MUST require:

```text
ci / build
contracts / validate     (when matching paths change)
security / audit
security / codeql
```

PRs that fail any of these MUST NOT be merged. Force-merge by maintainers is allowed only when the failure is an infra outage (documented in PR comments).

## 5. Caching

- pnpm cache via `cache: pnpm` on `actions/setup-node` (built-in).
- Vitest result cache: `.vitest-cache/` is part of the pnpm cache key automatically.
- Prisma engines: prefer pinning Prisma version so that `~/.cache/prisma` reuses across runs.
- Docker buildx layer cache: enabled by `docker/build-push-action@v6` automatically when the runner caches `/tmp/.buildx-cache`.

## 6. Secrets

Only the following GitHub repository secrets are needed for CE v0.1:

```text
NPM_TOKEN              (only if publishing @xtrape/capsule-agent-node to npm)
```

`GITHUB_TOKEN` is sufficient for pushing to `ghcr.io`. Do NOT add personal access tokens for normal CI flows.

## 7. Local Equivalents

To make CI failures reproducible locally, the repo MUST expose:

```bash
pnpm install --frozen-lockfile
pnpm -r lint
pnpm -r typecheck
pnpm -r test
pnpm --filter @xtrape/capsule-contracts run check
pnpm --filter @xtrape/capsule-db run validate
```

A single `pnpm verify` script SHOULD bundle all of the above so contributors can run "is this PR-ready?" in one command.

## 8. Acceptance Criteria

- Every PR that lands in `main` has all required status checks green.
- A `vX.Y.Z` tag produces an image at `ghcr.io/<org>/opstage:vX.Y.Z` with multi-arch (amd64, arm64) and an SBOM artifact attached to the GitHub Release.
- License scan blocks the PR when a transitive dependency lands a non-allowed license.
- Weekly security workflow runs even when there are no commits.
