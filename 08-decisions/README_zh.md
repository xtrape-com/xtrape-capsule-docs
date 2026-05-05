---
status: draft
audience: ai-coding-agents
stability: unstable
last_reviewed: 2026-05-05
translation_status: draft-machine-assisted
---

> Translation status: Draft / machine-assisted. Review before use. English docs are canonical unless explicitly stated otherwise.

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

# 架构 Decision Records

- Status: 实施指南
- Edition: 共享
- Priority: 高
- Audience: founders, architects, product designers, backend developers, frontend developers, agent SDK developers, AI coding agents

This directory 包含 architecture and product decisions that constrain implementation.

For CE（社区版） v0.1, read in this order:

```text
08-decisions/0001-ce-v01-implementation-baseline.md
08-decisions/0002-api-namespace-convention.md
08-decisions/0003-command-action-lifecycle.md
08-decisions/0004-security-defaults.md
08-decisions/0005-technology-stack-decision.md
08-decisions/0006-logging-and-observability.md
08-decisions/0007-ui-state-and-data-fetching.md
08-decisions/0008-naming-and-repositories.md
08-decisions/0009-contracts-spec-and-bindings.md
```

When implementation documents disagree, accepted ADRs should be treated as the higher-priority current decision until the conflicting documents are updated.
