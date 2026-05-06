# xtrape-capsule Public Review Promotion Plan

## Purpose

This plan defines how to run a **Public Review** for the `xtrape-capsule` project before announcing a formal `v0.1.0 Public Preview`.

Public Review is not a product launch.

Its purpose is to:

```text
1. Validate whether external developers understand the Capsule Service concept.
2. Verify whether users can run Opstage CE from the public documentation.
3. Verify whether developers can understand the Agent SDK and Contracts packages.
4. Collect early feedback on positioning, architecture, documentation, security, and developer experience.
5. Avoid wasting a major public launch before the project is fully packaged.
```

---

## Current Product Positioning

Use this public positioning consistently:

> Xtrape Capsule is a lightweight, self-hosted, agent-based runtime governance control plane for Capsule Services.

Expanded version:

> Xtrape Capsule helps teams connect small services, automation workers, integration adapters, background jobs, private tools, and agent runtimes to a unified Opstage console through an embedded Agent SDK.

Avoid saying:

```text
CAPI platform
unofficial API platform
generic config center
generic monitoring dashboard
Backstage replacement
full DevOps platform
enterprise-grade production system
```

---

## Public Review Scope

Public Review should cover these repositories:

```text
xtrape-capsule-site
xtrape-capsule-ce
xtrape-capsule-agent-node
xtrape-capsule-contracts-node
```

Do not use `xtrape-capsule-docs` as the public entry point.

`xtrape-capsule-docs` should remain or become private design documentation.

---

## Review Status Label

Use the following status in all public-facing materials:

```text
Status: Public Review / Pre-v0.1 Public Preview
```

Suggested wording:

```md
> Xtrape Capsule is currently in Public Review before the v0.1.0 Public Preview release.
> APIs, contracts, deployment instructions, and SDK interfaces may still change.
```

---

# 1. Public Review Readiness Checklist

Before inviting external reviewers, complete the following minimum requirements.

## P0: Must Complete

```text
[ ] Public repositories are CAPI-free.
[ ] xtrape-capsule-site homepage is readable and formatted.
[ ] xtrape-capsule-site Quick Start is executable.
[ ] xtrape-capsule-ce README is public-facing.
[ ] xtrape-capsule-agent-node README has install status and a minimal example.
[ ] xtrape-capsule-contracts-node README has validation examples.
[ ] GitHub About metadata is completed for public repositories.
[ ] GitHub Pages site is reachable.
[ ] Docker/NPM status is clearly stated.
[ ] At least one screenshot or architecture diagram exists.
```

## P1: Strongly Recommended

```text
[ ] Dashboard screenshot.
[ ] Agent registration flow diagram.
[ ] One demo GIF or short screen recording.
[ ] SECURITY.md for CE and Agent SDK.
[ ] CONTRIBUTING.md for CE, Agent SDK, and Contracts.
[ ] Public Review feedback issue template.
[ ] v0.1.0 roadmap page.
```

---

# 2. Target Reviewer Groups

Do not start with broad public promotion. Start with controlled review groups.

## Group A: Trusted Technical Reviewers

Target:

```text
senior backend developers
system architects
DevOps engineers
Node.js developers
open-source maintainers
```

Goal:

```text
Validate architecture, documentation clarity, security concerns, and implementation credibility.
```

Expected feedback:

```text
What is unclear?
What looks unsafe?
What feels over-engineered?
What is missing from the README?
Can the project be understood in 30 seconds?
```

---

## Group B: Potential Early Users

Target users who have:

```text
many small internal services
automation workers
integration services
background jobs
private tools
agent runtimes
```

Goal:

```text
Validate whether the problem is real and whether Opstage solves a recognizable pain.
```

Expected feedback:

```text
Would you use this?
What would you manage with it?
What feature is missing before adoption?
Would you prefer embedded agent or sidecar agent?
```

---

## Group C: AI Coding Agent / Tooling Users

Target:

```text
users of Claude Code
Codex
Cursor
OpenClaw
Playwright automation
private AI tooling builders
```

Goal:

```text
Validate whether the project narrative fits AI-era lightweight service governance.
```

Expected feedback:

```text
Does Capsule Service make sense?
Does Agent registration make sense?
Would this help manage AI tools/workers?
```

---

# 3. Public Review Channels

## Phase 1: Private / Semi-private Channels

Use first:

```text
1. Personal technical contacts
2. Small trusted developer groups
3. Private WeChat/Telegram/Discord groups
4. GitHub issues from invited reviewers
5. Direct messages to known open-source developers
```

Avoid first:

```text
Hacker News
Product Hunt
Reddit
Dev.to front-page style post
large WeChat group blast
large-scale LinkedIn/X launch
```

Reason:

```text
Public Review is for feedback quality, not exposure volume.
```

---

## Phase 2: Controlled Public Channels

After first round fixes:

```text
1. GitHub repository pinned post
2. Short LinkedIn/X announcement
3. Zhihu/Juejin technical note
4. Dev.to/Medium technical article
5. Small open-source newsletter submission
```

Still avoid Product Hunt / Hacker News until `v0.1.0 Public Preview`.

---

# 4. Review Message Templates

## 4.1 Short Private Message

```text
I’m preparing a Public Review for Xtrape Capsule, a lightweight self-hosted control plane for Capsule Services.

It is designed for teams that run many small services, automation workers, integration adapters, background jobs, private tools, or agent runtimes and want unified visibility, actions, and audit through an Agent-based model.

Could you review the positioning and docs?

Main site:
<site-url>

Main repo:
<ce-repo-url>

I’m especially looking for feedback on:
1. whether the concept is clear;
2. whether the Quick Start is runnable;
3. whether the Agent SDK looks understandable;
4. whether the security boundary feels acceptable.
```

---

## 4.2 Chinese Private Message

```text
我正在准备 xtrape-capsule 的 Public Review。

它不是正式发布，而是想先找一批技术朋友看一下定位和文档是否清楚。

xtrape-capsule 的定位是：
一个轻量、可私有化部署、基于 Agent 的 Capsule Service 运行态治理控制面。

它主要面向这类场景：
很多小型服务、自动化 worker、集成适配器、后台任务、私有工具、Agent Runtime 越来越多，需要统一看状态、配置、动作和审计。

你可以帮我看一下这几个点吗？

1. 第一眼能不能看懂它是什么；
2. Quick Start 是否能跑通；
3. Agent SDK 是否容易理解；
4. 安全边界是否合理；
5. 是否有你觉得应该补充的场景。

站点：
<site-url>

主仓库：
<ce-repo-url>
```

---

## 4.3 GitHub Discussion / Issue Prompt

```md
# Public Review Feedback

Thanks for reviewing Xtrape Capsule.

Please focus on the following questions:

1. Can you understand what Xtrape Capsule is within 30 seconds?
2. Does the Capsule Service concept make sense?
3. Can you follow the Quick Start?
4. Is the Agent registration model clear?
5. Is the security model acceptable?
6. What would block you from trying it?
7. What use case would you expect it to support first?
8. What should be improved before v0.1.0 Public Preview?
```

---

# 5. Review Feedback Questions

Use these questions when collecting feedback.

## Concept Clarity

```text
1. What do you think Xtrape Capsule is?
2. Is "Capsule Service" understandable?
3. Is "Opstage" understandable?
4. Does it sound like a config center, monitoring system, developer portal, or something else?
5. What confused you first?
```

## Developer Experience

```text
1. Could you run the Quick Start?
2. Did any command fail?
3. Was the Docker/NPM status clear?
4. Was the first Capsule Service guide understandable?
5. Was the Agent SDK example realistic?
```

## Security Review

```text
1. Are Agent registration and token handling clear?
2. Do you understand what runs locally vs in Opstage?
3. Are command/action security boundaries acceptable?
4. Would you expose this in your environment?
5. What security documentation is missing?
```

## Product Fit

```text
1. Do you have small services or workers that need this?
2. Would embedded agent or sidecar agent be more useful?
3. Which use case is most convincing?
4. What feature would make you try it?
5. What feature would make you pay for it later?
```

---

# 6. Public Review Success Metrics

## Qualitative Metrics

```text
1. Reviewers can describe the project correctly without your explanation.
2. Reviewers do not confuse it with CAPI, Nacos, Prometheus, or Backstage.
3. Reviewers understand why Agent-based governance is useful.
4. Reviewers understand CE is Public Preview, not production HA.
5. Reviewers identify at least one real use case.
```

## Quantitative Metrics

For the first Public Review round:

```text
Target reviewers: 10-20
Useful feedback items: 20+
Quick Start attempts: 5+
Successful local runs: 3+
GitHub issues/discussions: 5+
Stars are not the primary metric.
```

## Red Flags

```text
1. Most reviewers cannot explain what the project is.
2. Reviewers think it is a CAPI-specific project.
3. Quick Start fails for most users.
4. Agent SDK example cannot run.
5. Reviewers worry about unsafe command execution.
6. Reviewers say the project is too abstract and lacks concrete use cases.
```

---

# 7. Recommended Timeline

## Week 0: Final Cleanup

Before inviting reviewers:

```text
1. Remove all CAPI references.
2. Fix README formatting.
3. Rewrite CE README.
4. Improve Agent and Contracts README.
5. Confirm Quick Start.
6. Confirm GitHub Pages.
7. Add at least one architecture diagram.
```

---

## Week 1: Closed Public Review

Invite 5-10 trusted reviewers.

Focus:

```text
positioning
README clarity
Quick Start
security boundary
SDK understandability
```

Output:

```text
review issue list
FAQ improvements
README changes
Quick Start fixes
```

---

## Week 2: Wider Public Review

Invite 10-20 reviewers from small technical groups.

Focus:

```text
real use cases
developer experience
docs completeness
sidecar/embedded agent preference
```

Output:

```text
prioritized v0.1.0 fixes
use case ranking
missing docs list
```

---

## Week 3: v0.1.0 Public Preview Decision

Decide whether the project is ready for Public Preview.

Minimum condition:

```text
1. Public site is clear.
2. Quick Start works.
3. CE README is clean.
4. SDK README is usable.
5. Security notes are acceptable.
6. Feedback has no blocking confusion.
```

---

# 8. Public Review Content Assets

Prepare these before outreach.

## Required

```text
1. Public site URL
2. Main CE repo URL
3. Agent SDK repo URL
4. Contracts repo URL
5. Architecture diagram
6. Dashboard screenshot
7. Quick Start link
8. First Capsule Service guide
9. Feedback issue/discussion link
```

## Strongly Recommended

```text
1. 60-second demo GIF
2. Agent registration flow diagram
3. Public Review announcement post
4. FAQ page
5. Security page
```

---

# 9. Public Review Announcement Draft

## English Draft

```md
# Xtrape Capsule Public Review

I’m opening a Public Review for Xtrape Capsule before the v0.1.0 Public Preview.

Xtrape Capsule is a lightweight, self-hosted, Agent-based runtime governance control plane for Capsule Services.

It is designed for teams running many small services, automation workers, integration adapters, background jobs, private tools, or agent runtimes that need unified visibility, actions, configuration visibility, and audit trails.

This is not a production-ready release yet. I’m looking for feedback on:

- whether the concept is clear;
- whether the Quick Start works;
- whether the Agent SDK is understandable;
- whether the security model is acceptable;
- which use cases should be prioritized.

Site:
<site-url>

Main repo:
<ce-repo-url>

Feedback:
<discussion-or-issue-url>
```

---

## Chinese Draft

```md
# xtrape-capsule Public Review

我正在开放 xtrape-capsule 的 Public Review，用于准备后续 v0.1.0 Public Preview。

xtrape-capsule 的定位是：

一个轻量、可私有化部署、基于 Agent 的 Capsule Service 运行态治理控制面。

它主要用于管理越来越多的小型服务、自动化 worker、集成适配器、后台任务、私有工具和 Agent Runtime，让它们可以统一接入 Opstage，集中查看状态、配置、动作和审计。

这还不是 production-ready 发布。我希望先收集这些反馈：

- 这个概念是否清楚；
- Quick Start 是否能跑通；
- Agent SDK 是否容易理解；
- 安全边界是否合理；
- 哪些使用场景应该优先支持。

站点：
<site-url>

主仓库：
<ce-repo-url>

反馈入口：
<discussion-or-issue-url>
```

---

# 10. Feedback Triage

Classify feedback into:

```text
P0: Blocks Public Preview
P1: Should fix before wider promotion
P2: Nice to have
Later: Future roadmap
Invalid: Not aligned with current scope
```

## P0 Examples

```text
Quick Start fails
README positioning unclear
CAPI still appears
unsafe command execution concern
SDK example does not compile
site cannot be accessed
```

## P1 Examples

```text
need more screenshots
need sidecar explanation
need better FAQ
need better security notes
need clearer Docker/NPM status
```

## P2 Examples

```text
better theme
more diagrams
more examples
more language translations
```

---

# 11. Do Not Do During Public Review

Avoid:

```text
1. Product Hunt launch.
2. Hacker News Show HN.
3. Calling it production-ready.
4. Over-promising EE/Cloud features.
5. Mentioning CAPI as a public positioning point.
6. Publishing detailed commercial roadmap too early.
7. Asking for paid users before the core concept is validated.
```

---

# 12. Transition to v0.1.0 Public Preview

Move from Public Review to Public Preview when:

```text
[ ] At least 10 reviewers have reviewed the site or repo.
[ ] At least 3 external users have run Quick Start or attempted it.
[ ] Top P0 feedback is fixed.
[ ] Public README and site are CAPI-free.
[ ] Docker/NPM status is clear.
[ ] Security notes are present.
[ ] The project has at least one credible demo path.
```

Then publish:

```text
v0.1.0 Public Preview Release
introductory article
short social posts
selected community posts
```

---

# 13. Final Recommendation

Use Public Review as a controlled validation phase.

Do not chase stars first.

Chase:

```text
clarity
runnability
trust
developer experience
real use-case validation
```

The goal is not to maximize exposure. The goal is to avoid wasting the first real public launch.
