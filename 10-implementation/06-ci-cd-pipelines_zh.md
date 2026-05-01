<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 06-ci-cd-pipelines.md
翻译状态 / Translation Status: 已翻译 / Translated
生成时间 / Generated: 2026-05-01 09:28:55
================================================================================
注意 / Notes:
- 技术术语如 Capsule Service、Agent、Opstage 等保留英文或采用中英对照
- 代码块中的内容不翻译
- 文件路径和 URL 不翻译
- 保持原有的 Markdown 格式结构
================================================================================
-->

# CE（社区版） v0.1 CI/CD Pipelines

- Status: 实施指南
- Edition: CE（社区版）
- Priority: Current
- Audience: DevOps engineers, backend developers, frontend developers, agent SDK developers, AI coding agents

> **Precedence rule**: When this document and `08-decisions/` ADRs disagree, the ADRs win for CE（社区版） v0.1. Repository naming and the four-repo split are pinned by [ADR 0008](../08-decisions/0008-naming-and-repositories.md); the contracts sync workflow is pinned by [ADR 0009](../08-decisions/0009-contracts-spec-and-bindings.md).

## 1. Goal

Define the GitHub Actions CI/CD layout for the **four CE（社区版） v0.1 repositories**:

```text
xtrape-capsule-docs
xtrape-capsule-contracts-node
xtrape-capsule-agent-node
xtrape-capsule-ce
```

Each repo has its own `.github/workflows/` directory. Pipelines must:

- run on every PR;
- block merge on test/lint/typecheck/contract failures;
- publish artifacts (npm packages or Docker images) on tag pushes;
- never publish a release with failing checks;
- enforce reverse-dependency prohibition (ADR 0008).

CE（社区版） v0.1 targets GitHub Actions specifically because it is the de-facto standard for open-source repos. Mirroring to GitLab CI / CircleCI is out of scope.

## 2. Per-Repository Pipeline Summary

||Repo|What it builds|Where it publishes|Triggers||
|---|---|---|---|
||`xtrape-capsule-docs`|Markdown lint, JSON SSOT validity, render-parity check, OpenAPI lint|n/a (docs only)|PR + push to `main`||
||`xtrape-capsule-contracts-node`|TypeScript bindings (npm)|`@xtrape/capsule-contracts-node` on npm with provenance|PR + tag `vX.Y.Z` (changesets)||
||`xtrape-capsule-agent-node`|Node Agent（代理） SDK (npm)|`@xtrape/capsule-agent-node` on npm with provenance|PR + tag `vX.Y.Z` (changesets)||
||`xtrape-capsule-ce`|Backend, UI, demo, Docker images|`ghcr.io/xtrape/opstage-ce:vX.Y.Z` and `ghcr.io/xtrape/demo-capsule-service:vX.Y.Z`|PR + tag `vX.Y.Z`||

## 3. Required Workflows per Repository

Pseudo-content is provided; teams may iterate but the surface MUST stay equivalent.

### 3.1 `xtrape-capsule-docs/.github/workflows/`

#### `ci.yml`

```yaml
name: ci
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  validate-spec:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with: { version: 9 }
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - name: OpenAPI YAML validity
        run: ruby -e "require 'yaml'; YAML.load_file('09-contracts/openapi/opstage-ce-v0.1.yaml')"
      - name: OpenAPI lint (Redocly, zero warnings)
        run: pnpm --package=@redocly/cli dlx redocly lint 09-contracts/openapi/opstage-ce-v0.1.yaml --config 09-contracts/openapi/redocly.yaml
      - name: Prisma schema validity
        run: pnpm dlx prisma@latest validate --schema 09-contracts/prisma/schema.prisma
      - name: JSON SSOT validity
        run: |
          for f in 09-contracts/errors.json 09-contracts/enums/*.json 09-contracts/examples/*.json; do
            node -e "JSON.parse(require('fs').readFileSync('$f','utf8'))"
          done
      - name: errors.md render parity
        run: pnpm tsx 09-contracts/tools/render-errors.ts --check
      - name: Markdown lint
        run: pnpm dlx markdownlint-cli2 "**/*.md" "#node_modules"
```

This is the upstream CI. When this passes on `main`, every binding repo's `upstream-bump.yml` (below) becomes free to consume the new commit SHA.

### 3.2 `xtrape-capsule-contracts-node/.github/workflows/`

#### `ci.yml`

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
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with: { version: 9 }
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm typecheck
      - name: Sync-spec drift check
        run: pnpm tsx tools/sync-spec.ts --check
      - name: Codegen drift check
        run: pnpm tsx tools/codegen.ts --check
      - run: pnpm test                                  # includes conformance.spec.ts against spec/examples
      - run: pnpm build
      - name: Reverse-dep check
        run: pnpm tsx tools/check-no-reverse-deps.ts    # forbids @xtrape/opstage-* and @xtrape/capsule-agent-*
```

#### `upstream-bump.yml`

```yaml
name: upstream-bump
on:
  schedule:
    - cron: '0 6 * * *'           # daily 06:00 UTC
  workflow_dispatch:
permissions:
  contents: write
  pull-requests: write
jobs:
  bump:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Clone xtrape-capsule-docs
        run: git clone --depth=1 https://github.com/xtrape/xtrape-capsule-docs.git ../docs
      - uses: pnpm/action-setup@v4
        with: { version: 9 }
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - name: Sync spec from docs HEAD
        run: pnpm tsx tools/sync-spec.ts --from ../docs/09-contracts
      - name: Regenerate bindings
        run: pnpm tsx tools/codegen.ts
      - name: Run conformance
        run: pnpm test
      - name: Open PR if changed
        uses: peter-evans/create-pull-request@v6
        with:
          branch: chore/spec-bump
          title: "chore(spec): bump to xtrape-capsule-docs@${{ github.sha }}"
          body: "Automated nightly sync from xtrape-capsule-docs."
          labels: spec-bump,automated
```

If conformance fails, this job exits non-zero **without** opening a PR; instead a separate workflow opens an **issue** with the failure log so a human can decide whether the spec or the binding needs to change.

#### `release.yml`

```yaml
name: release
on:
  push:
    branches: [main]
permissions:
  contents: write
  id-token: write             # for npm provenance
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with: { version: 9 }
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          registry-url: https://registry.npmjs.org
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm build
      - name: Create release PR or publish via Changesets
        uses: changesets/action@v1
        with:
          publish: pnpm changeset publish --provenance
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

`changesets` drives semver bumps; `--provenance` attaches npm provenance per [SLSA](https://slsa.dev/) v1.

### 3.3 `xtrape-capsule-agent-node/.github/workflows/`

Same shape as `xtrape-capsule-contracts-node` minus the `upstream-bump.yml`. Instead of mirroring `09-contracts/`, it relies on Renovate to bump `@xtrape/capsule-contracts-node` automatically.

#### `ci.yml`

```yaml
name: ci
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with: { version: 9 }
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm typecheck
      - run: pnpm test                                  # unit + conformance against installed @xtrape/capsule-contracts-node
      - run: pnpm build
      - name: Reverse-dep check
        run: pnpm tsx tools/check-no-reverse-deps.ts    # forbids @xtrape/opstage-*
      - name: Lockfile link-check
        run: pnpm tsx tools/check-no-link-in-lockfile.ts
```

#### `release.yml`

Same as `xtrape-capsule-contracts-node/release.yml`, publishing `@xtrape/capsule-agent-node`.

### 3.4 `xtrape-capsule-ce/.github/workflows/`

#### `ci.yml`

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
    timeout-minutes: 25
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with: { version: 9 }
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm -r lint
      - run: pnpm -r typecheck
      - name: DB schema parity (must match xtrape-capsule-docs/09-contracts/prisma/schema.prisma)
        run: pnpm --filter @xtrape/capsule-db run check-schema-parity
      - run: pnpm -r test --reporter=verbose
      - run: pnpm -r build
      - name: Reverse-dep check
        run: pnpm tsx scripts/check-no-reverse-deps.ts
      - name: Lockfile link-check
        run: pnpm tsx scripts/check-no-link-in-lockfile.ts
      - name: Upload coverage
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: '**/coverage/**'
          if-no-files-found: ignore
```

#### `release.yml`

```yaml
name: release
on:
  push:
    tags: ['v*.*.*']
permissions:
  contents: write
  packages: write
  id-token: write
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
      - name: Build and push opstage-ce image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: deploy/docker/opstage-ce.Dockerfile
          platforms: linux/amd64,linux/arm64
          push: true
          provenance: true
          sbom: true
          tags: |
            ghcr.io/${{ github.repository_owner }}/opstage-ce:${{ github.ref_name }}
            ghcr.io/${{ github.repository_owner }}/opstage-ce:latest
      - name: Build and push demo-capsule-service image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: deploy/docker/demo-capsule-service.Dockerfile
          platforms: linux/amd64,linux/arm64
          push: true
          provenance: true
          sbom: true
          tags: |
            ghcr.io/${{ github.repository_owner }}/demo-capsule-service:${{ github.ref_name }}
            ghcr.io/${{ github.repository_owner }}/demo-capsule-service:latest
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

#### `security.yml`

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
        with: { version: 9 }
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

The same `security.yml` is used in `xtrape-capsule-contracts-node` and `xtrape-capsule-agent-node`.

## 4. Cross-Repo Coordination via Renovate

Each consumer repo (`xtrape-capsule-agent-node` and `xtrape-capsule-ce`) MUST run Renovate (or Dependabot) configured to:

```jsonc
// renovate.json (sketch)
{
  "extends": ["config:recommended"],
  "packageRules": [
    {
      "matchPackageNames": ["@xtrape/capsule-contracts-node", "@xtrape/capsule-agent-node"],
      "automerge": true,
      "automergeType": "pr",
      "matchUpdateTypes": ["patch"],
      "labels": ["dep:contracts"]
    },
    {
      "matchPackageNames": ["@xtrape/capsule-contracts-node", "@xtrape/capsule-agent-node"],
      "matchUpdateTypes": ["minor", "major"],
      "automerge": false,
      "labels": ["dep:contracts","needs-review"]
    }
  ],
  "schedule": ["after 1am every weekday"]
}
```

This realizes the sync flow described in [ADR 0009](../08-decisions/0009-contracts-spec-and-bindings.md) §"Sync Workflow".

## 5. Required 状态 Checks

Branch protection on `main` in each repo MUST require:

||Repo|Required checks||
|---|---|
||`xtrape-capsule-docs`|`ci / validate-spec`||
||`xtrape-capsule-contracts-node`|`ci / build`||
||`xtrape-capsule-agent-node`|`ci / build`||
||`xtrape-capsule-ce`|`ci / build`, `security / audit`, `security / codeql`||

PRs that fail any of these MUST NOT be merged. Force-merge by maintainers is allowed only when the failure is an infra outage (documented in PR comments).

## 6. Caching

- pnpm cache via `cache: pnpm` on `actions/setup-node` (built-in).
- Vitest result cache: `.vitest-cache/` is part of the pnpm cache key automatically.
- Prisma engines: prefer pinning Prisma version so that `~/.cache/prisma` reuses across runs.
- Docker buildx layer cache: enabled by `docker/build-push-action@v6` automatically when the runner caches `/tmp/.buildx-cache`.

## 7. Secrets

Per-repository secret needs (CE（社区版） v0.1):

||Repo|Secrets||
|---|---|
||`xtrape-capsule-docs`|none beyond `GITHUB_TOKEN`||
||`xtrape-capsule-contracts-node`|`NPM_TOKEN` (publishing); npm provenance uses GitHub OIDC `id-token`||
||`xtrape-capsule-agent-node`|`NPM_TOKEN`||
||`xtrape-capsule-ce`|`GITHUB_TOKEN` is sufficient for `ghcr.io` push||

Do NOT add personal access tokens for normal CI flows.

## 8. Local Equivalents

To make CI failures reproducible locally, each repo MUST expose:

```bash
# common to all repos
pnpm install --frozen-lockfile
pnpm lint
pnpm typecheck
pnpm test
pnpm build

# xtrape-capsule-docs additions
ruby -e "require 'yaml'; YAML.load_file('09-contracts/openapi/opstage-ce-v0.1.yaml')"
pnpm --package=@redocly/cli dlx redocly lint 09-contracts/openapi/opstage-ce-v0.1.yaml --config 09-contracts/openapi/redocly.yaml
pnpm tsx 09-contracts/tools/render-errors.ts --check

# xtrape-capsule-contracts-node additions
pnpm tsx tools/sync-spec.ts --check
pnpm tsx tools/codegen.ts --check

# xtrape-capsule-ce additions
pnpm --filter @xtrape/capsule-db run check-schema-parity
pnpm tsx scripts/check-no-reverse-deps.ts
pnpm tsx scripts/check-no-link-in-lockfile.ts
```

Each repo SHOULD bundle the relevant subset into a `pnpm verify` root script.

## 9. Acceptance Criteria

- All four repositories have `.github/workflows/` directories with `ci.yml` (and `release.yml` where applicable).
- Every PR that lands in any `main` branch has all required status checks green.
- A `vX.Y.Z` tag in `xtrape-capsule-ce` produces multi-arch images at `ghcr.io/xtrape/opstage-ce:vX.Y.Z` and `ghcr.io/xtrape/demo-capsule-service:vX.Y.Z` with SBOM + provenance attached to the GitHub Release.
- A successful merge to `main` in `xtrape-capsule-contracts-node` (with a changeset) publishes `@xtrape/capsule-contracts-node@X.Y.Z` to npm with provenance.
- Renovate opens a PR in `xtrape-capsule-agent-node` and `xtrape-capsule-ce` within 24h of any contracts publish.
- License scan blocks the PR when a transitive dependency lands a non-allowed license.
- Weekly security workflow runs even when there are no commits.
- Reverse-dep check fails the PR if any forbidden dependency is added (ADR 0008).
