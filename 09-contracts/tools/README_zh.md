<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: README.md
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

# 09-contracts/tools

Markdown renderers that turn the JSON SSOT files in `09-contracts/` into human-readable markdown. These scripts run in CI in `--check` mode; PRs fail if any rendered file is stale.

The scripts intentionally have **no runtime dependencies** beyond Node.js (use `node --experimental-strip-types` on Node 22+, or `tsx`). Do not pull in template engines or markdown libs — just string concatenation.

## Scripts

||Script|Reads|Writes||
|---|---|---|
||`render-errors.ts`|`09-contracts/errors.json`|`09-contracts/errors.md`||
||`render-status-enums.ts`|`09-contracts/enums/status-enums.json`|inline sections of `02-specs/09-status-model-spec.md` (between `<!-- BEGIN GENERATED -->` / `<!-- END GENERATED -->` markers)||
||`render-audit-actions.ts`|`09-contracts/enums/audit-actions.json`|inline section of `02-specs/08-audit-event-spec.md`||

## Conventions

- Each script accepts `--check` to compare against the current file content and exit non-zero on mismatch (used by CI), or no flag to write the file.
- All generated markdown files MUST start with the same banner:

  ```markdown
  > **This file is rendered from `<source>.json` by `09-contracts/tools/<script>.ts`.**
  > Edit the source JSON. CI verifies this file is byte-for-byte equal to the rendered output.
  ```

- Tables MUST use single-space padding around column dividers and align by the longest header.
- Group ordering MUST match the JSON source's array order.

## 实现 sketch

```ts
// render-errors.ts (~80 lines)
import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

type ErrorCode = { code: string; httpStatus: number; meaning: string; reservedFor?: string };
type Group = { name: string; title: string; codes: ErrorCode[] };
type Spec = {
  groups: Group[];
  reservedForFutureEditions: string[];
};

const root = resolve(import.meta.dirname, "..");
const spec: Spec = JSON.parse(readFileSync(`${root}/errors.json`, "utf8"));

const sections: string[] = [];
sections.push(banner());
sections.push(envelopeSection());
spec.groups.forEach((g, i) => {
  sections.push(`## ${i + 2}. ${g.title}\n\n${tableFor(g.codes)}\n\n---`);
});
sections.push(reservedSection(spec.reservedForFutureEditions));
sections.push(auditMappingSection());

const out = sections.join("\n\n") + "\n";
const target = `${root}/errors.md`;

if (process.argv.includes("--check")) {
  const current = readFileSync(target, "utf8");
  if (current !== out) {
    console.error("errors.md is stale; run `pnpm render:errors` to regenerate.");
    process.exit(1);
  }
} else {
  writeFileSync(target, out);
}

function tableFor(codes: ErrorCode[]): string {
  // build pipe-separated markdown table aligned to longest column
}
// ... (envelopeSection, banner, reservedSection, auditMappingSection are static strings)
```

The actual implementation is intentionally simple (no template engine). It is run from the docs repo's CI: `pnpm render --check`.
