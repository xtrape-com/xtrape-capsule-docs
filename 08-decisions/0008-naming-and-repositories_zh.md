<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: 0008-naming-and-repositories.md
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

# ADR 0008: Naming and Repositories

- Status: Accepted
- Edition: 共享 (CE（社区版） v0.1 actionable; EE（企业版）/Cloud（云版） aligned)
- Priority: Current
- Audience: founders, architects, backend developers, frontend developers, agent SDK developers, DevOps engineers, AI coding agents

## Decision

Opstage（运维舞台） CE（社区版） v0.1 ships as **four repositories** under a single GitHub organization, with strict separation between edition-bound and edition-agnostic codebases. All names, scopes, and registries below are **normative**: implementation MUST follow them and downstream documentation MUST reference them by these exact strings.

This ADR is the single source of truth for repository names, package names, container image names, GitHub organization, and npm scope. Older documents (including `03-editions/ce/11-ce-open-source-strategy.md` §6 and `10-implementation/00-repository-structure.md`) MUST defer to this ADR when they disagree.

## Identity

```text
GitHub organization      : xtrape
npm scope                : @xtrape
GHCR namespace           : ghcr.io/xtrape
Container image registry : ghcr.io
PyPI namespace (future)  : xtrape-*
Maven group  (future)    : com.xtrape
Go module prefix (future): github.com/xtrape/...
```

The organization name `xtrape` is fixed and used everywhere. There is no "xtrape-capsule" sub-organization.

## Repositories (CE（社区版） v0.1)

||#|Repository|版本|Language|Purpose||
|---|---|---|---|---|
||1|`xtrape-capsule-docs`|shared|n/a|设计 docs, ADRs, OpenAPI / JSON spec SSOT (Layer 1 contracts)||
||2|`xtrape-capsule-contracts-node`|shared|TypeScript|Node bindings of the wire contracts (Layer 2). Codegens from `xtrape-capsule-docs/09-contracts/spec/`.||
||3|`xtrape-capsule-agent-node`|shared|TypeScript|Node Agent（代理） SDK. Depends on `@xtrape/capsule-contracts-node`.||
||4|`xtrape-capsule-ce`|**CE（社区版）-bound**|TypeScript|Opstage（运维舞台） CE（社区版） backend + UI + demo + deploy. pnpm workspace monorepo.||

### Future repositories (NOT in CE（社区版） v0.1 scope, named here for forward-compatibility)

```text
xtrape-capsule-contracts-python      (when Python Agent ships)
xtrape-capsule-contracts-java        (when Java Agent ships)
xtrape-capsule-contracts-go          (when Go Agent ships)

xtrape-capsule-agent-python
xtrape-capsule-agent-java
xtrape-capsule-agent-go

xtrape-capsule-opstage-ee            (EE backend, may be Node or Java)
xtrape-capsule-opstage-cloud         (Cloud backend, multi-tenant)
```

The naming pattern is:

```text
xtrape-capsule-<role>[-<language>]   when role is "agent" or "contracts"
xtrape-capsule-<role>-<edition>      when role is "opstage" (the control plane app)
xtrape-capsule-<role>                when role is product-wide ("docs")
```

## Naming Rules

### Rule 1: 版本 prefix appears ONLY on edition-bound repos

||Repo type|版本 prefix?||
|---|---|
||Backend / UI / deploy (control plane)|**Yes** — `xtrape-capsule-ce`, future `xtrape-capsule-opstage-ee`, `xtrape-capsule-opstage-cloud`||
||Agent（代理） SDK (per language)|**No** — `xtrape-capsule-agent-node`, never `-ce-agent-`, never `-ee-agent-`||
||Contracts bindings (per language)|**No** — `xtrape-capsule-contracts-node`, never `-ce-contracts-`||
||文档|**No** — `xtrape-capsule-docs`||

Reason: agents and contracts are wire-level; the same SDK and the same TS bindings MUST work against CE（社区版）, EE（企业版）, and Cloud（云版） backends without recompilation.

### Rule 2: Reverse-dependency prohibition

版本-agnostic repos MUST NOT depend on edition-bound repos. Specifically:

- ❌ `xtrape-capsule-contracts-node` MUST NOT depend on `xtrape-capsule-ce` (or any edition repo)
- ❌ `xtrape-capsule-agent-node` MUST NOT depend on `xtrape-capsule-ce` (or any edition repo)
- ❌ `xtrape-capsule-docs` MUST NOT contain edition-specific implementation code

Allowed dependency arrows (single-direction only):

```text
xtrape-capsule-docs (spec SSOT)
        │  (sync via CI; NOT a runtime dep)
        ▼
xtrape-capsule-contracts-node ───► npm: @xtrape/capsule-contracts-node
        │                                  │
        │  npm                              │  npm
        ▼                                   ▼
xtrape-capsule-agent-node            xtrape-capsule-ce
        │                                   │
        └──────────► npm ───────────────────┤
              @xtrape/capsule-agent-node    │
                                            ▼
                                      (demo-capsule-service inside CE)
```

CE（社区版） consumes both `@xtrape/capsule-contracts-node` and `@xtrape/capsule-agent-node` from npm. Agent（代理）-node consumes `@xtrape/capsule-contracts-node` from npm. Nothing depends on CE（社区版）.

### Rule 3: Language suffix in repo and package matches

When a repo name carries a language suffix, the npm/PyPI/Maven package name MUST match exactly:

||Repo|Package||
|---|---|
||`xtrape-capsule-contracts-node`|`@xtrape/capsule-contracts-node` (npm)||
||`xtrape-capsule-agent-node`|`@xtrape/capsule-agent-node` (npm)||
||`xtrape-capsule-contracts-python`|`xtrape-capsule-contracts-python` (PyPI, hyphen-cased)||
||`xtrape-capsule-agent-python`|`xtrape-capsule-agent-python` (PyPI)||
||`xtrape-capsule-contracts-java`|`com.xtrape:capsule-contracts-java` (Maven)||
||`xtrape-capsule-agent-java`|`com.xtrape:capsule-agent-java` (Maven)||
||`xtrape-capsule-contracts-go`|`github.com/xtrape/xtrape-capsule-contracts-go` (Go module)||
||`xtrape-capsule-agent-go`|`github.com/xtrape/xtrape-capsule-agent-go` (Go module)||

Note: the Node SDK historical name `@xtrape/capsule-agent-node` (without "ce") is preserved.

## CE（社区版） v0.1 Public npm Packages

Only two packages are published to public npm in CE（社区版） v0.1:

```text
@xtrape/capsule-contracts-node    (from xtrape-capsule-contracts-node)
@xtrape/capsule-agent-node        (from xtrape-capsule-agent-node)
```

CE（社区版）-internal packages (inside `xtrape-capsule-ce` monorepo) are **NOT published** and exist only as workspace packages:

```text
@xtrape/opstage-backend           (private; apps/opstage-backend)
@xtrape/opstage-ui                (private; apps/opstage-ui)
@xtrape/demo-capsule-service      (private; apps/demo-capsule-service)
@xtrape/capsule-db                (private; packages/db)
@xtrape/capsule-shared            (private; packages/shared)
@xtrape/capsule-test-utils        (private; packages/test-utils)
```

Every private workspace package MUST set `"private": true` in its `package.json` to prevent accidental npm publish.

## Container Images

CE（社区版） v0.1 publishes the following images to GHCR:

```text
ghcr.io/xtrape/opstage-ce:vX.Y.Z         (backend + bundled UI static assets, single container)
ghcr.io/xtrape/opstage-ce:latest
ghcr.io/xtrape/demo-capsule-service:vX.Y.Z
ghcr.io/xtrape/demo-capsule-service:latest
```

Notes:

- The image name `opstage-ce` (NOT `xtrape-capsule-ce` and NOT `opstage`) is the public, deployable artifact name.
- `demo-capsule-service` is published as a separate image so users can `docker compose up` and immediately see a connected Capsule Service（胶囊服务） without cloning the repo.
- Future EE（企业版）/Cloud（云版） will publish under `ghcr.io/xtrape/opstage-ee:*` / `ghcr.io/xtrape/opstage-cloud:*` (NOT in CE（社区版） v0.1 scope).
- Images MUST be built multi-arch: `linux/amd64` and `linux/arm64`.
- Images MUST attach SBOM and SLSA provenance per ADR 0006 and `10-implementation/08-supply-chain.md`.

## Repository Descriptions (used in GitHub "About" field)

Use these exact strings:

||Repo|Description||
|---|---|
||`xtrape-capsule-docs`|设计 documents, ADRs, and wire-contract SSOT for the Opstage（运维舞台） / Capsule Service（胶囊服务） product family.||
||`xtrape-capsule-contracts-node`|TypeScript bindings (types, Zod schemas, enums, error codes) for the Opstage（运维舞台） wire contracts.||
||`xtrape-capsule-agent-node`|Node.js Agent（代理） SDK for embedding Capsule Services into the Opstage（运维舞台） governance loop.||
||`xtrape-capsule-ce`|Opstage（运维舞台） CE（社区版） — a lightweight, self-hosted, open-source control plane for Capsule Services.||

## Branch and Tag Conventions (all repos)

```text
default branch     : main
release tags       : vX.Y.Z (semver)
release-candidates : vX.Y.Z-rc.N
nightly tags       : NOT used in CE v0.1
```

Each repo versions independently; there is no synchronized "Opstage（运维舞台） 0.1" meta-version. Compatibility is documented in each repo's README "Compatibility" section.

## Dependency Direction Enforcement (CI rule)

Each repository's CI MUST enforce these rules at PR time:

||Repo|CI rule||
|---|---|
||`xtrape-capsule-contracts-node`|dependency tree MUST NOT contain `@xtrape/opstage-*` or `@xtrape/capsule-agent-*`||
||`xtrape-capsule-agent-node`|dependency tree MUST NOT contain `@xtrape/opstage-*`||
||`xtrape-capsule-ce`|depends on `@xtrape/capsule-contracts-node` and `@xtrape/capsule-agent-node` from npm (NEVER `link:` or `file:` to a sibling clone in CI)||

A simple `scripts/check-no-reverse-deps.ts` walks `package.json`'s `dependencies`, `devDependencies`, and `peerDependencies` to enforce this.

## Local 开发: Multi-Repo Linking

Developers iterating on contracts and agent simultaneously MAY use pnpm overrides locally:

```jsonc
// xtrape-capsule-agent-node/package.json (local-only — NEVER commit this block)
{
  "pnpm": {
    "overrides": {
      "@xtrape/capsule-contracts-node": "link:../xtrape-capsule-contracts-node"
    }
  }
}
```

Rules:

- The `overrides` block MUST be `.gitignore`-protected via a `package.local.json` pattern OR removed before commit.
- CI MUST verify no `link:` or `file:` paths appear in `pnpm-lock.yaml` for these packages.
- Releases MUST be cut from a tree without local overrides.

## Renovate / Dependabot

Each consumer repo MUST run Renovate (or Dependabot) configured to:

- monitor `@xtrape/capsule-contracts-node` and `@xtrape/capsule-agent-node` versions;
- auto-open a PR when a new version is published;
- run the consumer's full CI (including conformance tests) on the upgrade PR;
- auto-merge when CI is green AND the bump is `patch` (manual review required for `minor`/`major`).

## Acceptance Criteria

- All four CE（社区版） v0.1 repositories exist on GitHub under `xtrape/`.
- Each repo's README opens with one sentence matching the table in the "Repository Descriptions" section.
- `xtrape-capsule-ce` `package.json` declares `@xtrape/capsule-contracts-node` and `@xtrape/capsule-agent-node` as runtime dependencies installed from npm.
- `xtrape-capsule-agent-node` `package.json` declares `@xtrape/capsule-contracts-node` as runtime dependency installed from npm; it has no dependency on `@xtrape/opstage-*`.
- Image `ghcr.io/xtrape/opstage-ce:vX.Y.Z` is multi-arch and ships with SBOM + SLSA provenance.
- A reverse-dep-check script in each repo exits non-zero on any forbidden dependency.

## References

- ADR 0009 — Contracts Spec and Bindings (定义 Layer 1 / Layer 2 model and codegen rules for the contracts repos)
- `09-contracts/README.md` — Layer 1 SSOT location (`xtrape-capsule-docs/09-contracts/spec/`)
- `10-implementation/00-repository-structure.md` — internal layout of the `xtrape-capsule-ce` monorepo and cross-repo dev workflow
- `10-implementation/06-ci-cd-pipelines.md` — per-repo workflows
- `03-editions/ce/11-ce-open-source-strategy.md` §6 — public-facing repository strategy
