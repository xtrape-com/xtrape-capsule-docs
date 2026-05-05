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

# CE（社区版） v0.1 实现 Plans

- Status: 实施指南
- Edition: CE（社区版）
- Priority: Current
- Audience: architects, backend developers, frontend developers, agent SDK developers, DevOps engineers, test engineers, AI coding agents

This directory translates the CE（社区版） v0.1 decisions and contracts into a concrete implementation plan.

Read this directory after:

```text
08-decisions/
09-contracts/
03-editions/ce/13-ce-v01-implementation-checklist.md
```

## 1. Documents

```text
10-implementation/00-repository-structure.md
10-implementation/01-backend-scaffold-plan.md
10-implementation/02-ui-scaffold-plan.md
10-implementation/03-agent-sdk-scaffold-plan.md
10-implementation/04-demo-service-plan.md
10-implementation/05-implementation-sequence.md
10-implementation/06-ci-cd-pipelines.md
10-implementation/07-quickstart.md
10-implementation/08-supply-chain.md
10-implementation/09-database-implementation.md
10-implementation/10-user-and-ops-manual.md
10-implementation/11-api-and-security-implementation.md
10-implementation/12-development-and-release-implementation.md
10-implementation/13-service-action-design-guide_zh.md
10-implementation/14-ce-smoke-test_zh.md
10-implementation/15-docs-implementation-consistency-check_zh.md
```

## 2. 实现 Rule

实现 should follow this priority:

```text
1. ADRs in 08-decisions/
2. Contracts in 09-contracts/
3. Checklist in 03-editions/ce/13-ce-v01-implementation-checklist.md
4. Plans in 10-implementation/
5. Other CE documents and shared specs
```

If this directory conflicts with accepted ADRs or contracts, update this directory rather than changing the ADRs silently.
