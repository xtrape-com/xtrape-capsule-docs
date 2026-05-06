# xtrape-capsule Public Review Account Setup Plan

## Purpose

This document lists the external platforms/accounts to prepare for promoting `xtrape-capsule` during the Public Review stage.

Current positioning:

```text
Xtrape Capsule is a lightweight, self-hosted, agent-based runtime governance control plane for Capsule Services.
```

Current stage:

```text
Public Review before v0.1.0 Public Preview
```

The goal is not a large launch yet. The goal is to collect early technical feedback from developers, self-hosting users, Node.js users, DevOps engineers, and open-source reviewers.

---

# Account Ownership Principle

Because `xtrape.com` is a **product domain**, not the company legal name, do not bind all core infrastructure ownership to `@xtrape.com`.

Recommended principle:

```text
Infrastructure ownership:
  personal account now;
  future company/team account later.

Product-facing contact:
  @xtrape.com email.

Legal / billing / tax / contracts:
  future company domain email, not xtrape.com unless company uses that domain.
```

---

# Recommended Product Emails

Create these first:

```text
hello@xtrape.com
security@xtrape.com
opensource@xtrape.com
```

## Email usage

| Email | Purpose | Public? |
|---|---|---|
| `hello@xtrape.com` | General contact, product/community contact | Yes |
| `security@xtrape.com` | Security vulnerability reports, SECURITY.md | Yes |
| `opensource@xtrape.com` | Open-source ecosystem contact, optional | Yes / optional |
| Personal email | GitHub/npm owner account for now | No / limited |
| Future company email | Legal, billing, ownership transfer later | No / official later |

Minimum recommended setup:

```text
hello@xtrape.com
security@xtrape.com
```

---

# Immediate Accounts

These should be prepared before the first Public Review Call.

---

## 1. GitHub

Status:

```text
Already exists.
```

Recommended organization:

```text
xtrape-com
```

Repositories:

```text
xtrape-capsule-site
xtrape-capsule-ce
xtrape-capsule-agent-node
xtrape-capsule-contracts-node
```

Recommended public contact:

```text
hello@xtrape.com
```

Recommended security contact:

```text
security@xtrape.com
```

Usage:

```text
1. Public Review issue;
2. issue templates;
3. repository landing pages;
4. release notes;
5. source of truth for external feedback.
```

Account name recommendation:

```text
Organization: xtrape-com
Personal maintainer: keep current personal GitHub account
```

Notes:

```text
- Do not move ownership hastily.
- Keep personal GitHub as owner/maintainer for now.
- Later add a company/team account as second owner.
- Enable 2FA.
- Store recovery codes securely.
```

---

## 2. npm

Status:

```text
Already using personal npm account.
```

Recommended package scope:

```text
@xtrape
```

Packages:

```text
@xtrape/capsule-contracts-node
@xtrape/capsule-agent-node
```

Recommended account owner:

```text
Personal npm account for now.
```

Recommended future setup:

```text
npm organization: @xtrape
maintainers:
  - personal npm account
  - future company/team npm account
```

Usage:

```text
1. Publish contracts package;
2. publish agent SDK package;
3. let CE use npm semver dependencies;
4. support external users with pnpm add.
```

Recommended email:

```text
Personal email for account ownership now.
hello@xtrape.com or opensource@xtrape.com for public contact if needed.
```

Security requirements:

```text
- Enable 2FA.
- Save recovery codes.
- Use granular access token for future CI publish.
- Use public-review tag for prerelease package.
```

Recommended publish version:

```text
0.1.0-public-review.0
```

Recommended dist-tag:

```text
public-review
```

---

## 3. DEV Community

Platform:

```text
https://dev.to/
```

Priority:

```text
High
```

Recommended account name options:

```text
xtrape
xtrape-com
xtrape-dev
personal technical account
```

Recommended email:

```text
hello@xtrape.com
```

Usage:

```text
English technical article / feedback request.
```

First article title:

```text
Looking for feedback: a lightweight control plane for small services and agent runtimes
```

Suggested tags:

```text
opensource
devops
node
selfhosted
typescript
```

Notes:

```text
- Do not write like a product launch.
- Write as a technical feedback request.
- Link to the GitHub Public Review issue.
```

---

## 4. Reddit

Platform:

```text
https://www.reddit.com/
```

Priority:

```text
High, but careful
```

Recommended account name options:

```text
xtrape
xtrape_com
xtrape_dev
personal long-term account
```

Recommended email:

```text
hello@xtrape.com
```

Recommended first subreddit:

```text
r/selfhosted
```

Later possible subreddits:

```text
r/node
r/devops
r/opensource
r/typescript
```

First post style:

```text
Feedback request, not launch announcement.
```

Suggested first title:

```text
Looking for feedback on a self-hosted control plane for small services and agent runtimes
```

Notes:

```text
- Do not post to many subreddits at once.
- Do not use Reddit only for self-promotion.
- Reply to comments seriously.
- Avoid marketing tone.
```

---

## 5. V2EX

Platform:

```text
https://www.v2ex.com/
```

Priority:

```text
High
```

Recommended account name options:

```text
xtrape
xtrape_com
xtrape_dev
personal technical account
```

Recommended email:

```text
hello@xtrape.com
```

Recommended boards:

```text
/go/programmer
/go/create
/go/opensource
```

First post title:

```text
我在做一个轻量级 Agent-based 服务治理工具，想请大家 review 一下定位和文档
```

Usage:

```text
Chinese technical feedback from early developers.
```

Notes:

```text
- Use discussion tone.
- Do not ask for stars.
- Ask people to review positioning, Quick Start, SDK, and security boundary.
```

---

## 6. 掘金

Platform:

```text
https://juejin.cn/
```

Priority:

```text
High
```

Recommended account name options:

```text
Xtrape
Xtrape Capsule
个人技术账号
```

Recommended email:

```text
hello@xtrape.com
```

First article title:

```text
我为什么做 xtrape-capsule：AI 时代小型服务越来越多后，如何统一治理？
```

Recommended category:

```text
后端
架构
开源
Node.js
DevOps
```

Article focus:

```text
1. Problem background;
2. why small services / workers / agent runtimes need governance;
3. why not just config center or monitoring;
4. Capsule Service / Opstage model;
5. Public Review request.
```

Notes:

```text
- Article should explain the problem, not only introduce the project.
- Put GitHub Public Review issue at the end.
```

---

## 7. 知乎

Platform:

```text
https://www.zhihu.com/
```

Priority:

```text
Medium-high
```

Recommended account name options:

```text
Xtrape
Xtrape Capsule
个人技术账号
```

Recommended email:

```text
hello@xtrape.com
```

First article title:

```text
AI 时代会出现越来越多“小服务”，它们的运维和治理应该怎么做？
```

Article style:

```text
Opinion / analysis first, project second.
```

Notes:

```text
- Zhihu is better for explaining the idea and trend.
- Avoid making it look like a pure ad.
- Use xtrape-capsule as an open-source attempt at the end.
```

---

# Reserve / Placeholder Accounts

These accounts can be registered now to reserve names, but should not be used for a major launch yet.

---

## 8. Hacker News

Platform:

```text
https://news.ycombinator.com/
```

Priority:

```text
Register now, post later
```

Recommended account name options:

```text
xtrape
xtrape_com
personal technical account
```

Recommended email:

```text
hello@xtrape.com or personal email
```

Usage later:

```text
Show HN
Ask HN
```

Do not post `Show HN` until:

```text
1. CE fresh install works;
2. npm packages are available;
3. Quick Start is reliable;
4. screenshots exist;
5. public review issue exists;
6. at least one feedback round has been processed.
```

Possible later title:

```text
Show HN: Xtrape Capsule – a lightweight control plane for small services
```

---

## 9. Product Hunt

Platform:

```text
https://www.producthunt.com/
```

Priority:

```text
Register now, launch much later
```

Recommended account name options:

```text
Xtrape
Xtrape Capsule
personal founder account
```

Recommended email:

```text
hello@xtrape.com
```

Use later for:

```text
Public Preview / v0.1.0 or later product launch.
```

Do not launch now.

Requirements before Product Hunt:

```text
1. website polished;
2. screenshots;
3. demo video or GIF;
4. self-hosted install works;
5. clear target users;
6. several real early feedback items;
7. project has a stronger visual identity.
```

---

## 10. X / Twitter

Platform:

```text
https://x.com/
```

Priority:

```text
Medium
```

Recommended account name options:

```text
@xtrape
@xtrape_dev
@xtrape_com
@xtrapehq
@xtrape_io
```

Recommended email:

```text
hello@xtrape.com
```

Usage:

```text
1. short updates;
2. development notes;
3. public review announcement;
4. follow self-hosted / devtools / opensource people.
```

Notes:

```text
- Not required for first review.
- Useful for long-term distribution.
```

---

## 11. LinkedIn

Platform:

```text
https://www.linkedin.com/
```

Priority:

```text
Medium
```

Recommended account type:

```text
Personal account first.
Company/product page later.
```

Recommended email:

```text
Personal email for personal account.
hello@xtrape.com if creating a product page later.
```

Usage:

```text
B2B / product positioning / professional network.
```

First post style:

```text
I’m preparing Public Review for an open-source self-hosted control plane for small services and agent runtimes.
```

Notes:

```text
- Personal founder-style posts are usually better than a cold product page early.
```

---

## 12. Medium

Platform:

```text
https://medium.com/
```

Priority:

```text
Low-medium
```

Recommended account name:

```text
Xtrape
Xtrape Capsule
personal technical account
```

Recommended email:

```text
hello@xtrape.com
```

Usage:

```text
Optional English long-form backup.
```

Notes:

```text
- If DEV.to is used, Medium can wait.
- Avoid duplicating effort too early.
```

---

# Deferred Accounts

Do not prioritize these yet:

```text
Discord
Slack community
Telegram channel
YouTube
Bilibili
微信公众号
CSDN
SegmentFault
开源中国专栏
```

Reason:

```text
The project is still in Public Review, not broad community operation.
```

---

# Recommended Setup Order

## Step 1 - Infrastructure and required package accounts

```text
1. npm
2. GitHub public review issue / org metadata
```

## Step 2 - First Public Review channels

```text
3. V2EX
4. 掘金
5. DEV.to
6. Reddit
7. 知乎
```

## Step 3 - Reserve later launch channels

```text
8. Hacker News
9. Product Hunt
10. X / Twitter
11. LinkedIn
```

---

# Recommended Account Naming

## Product/organization names

Preferred:

```text
xtrape
xtrape-com
xtrape-dev
xtrapehq
```

Avoid:

```text
xtrape-capsule-only names
```

Reason:

```text
Xtrape Capsule may be one product under the broader Xtrape ecosystem.
```

## Chinese platform display names

Preferred:

```text
Xtrape
Xtrape Capsule
Xtrape 开源
```

Avoid overly promotional names:

```text
Xtrape 官方
Xtrape 商业平台
```

unless the project is already formally operated as a company/product brand.

---

# Recommended Bios

## English bio

```text
Xtrape Capsule — lightweight self-hosted control plane for Capsule Services, automation workers, private tools, and agent runtimes.
```

## Short English bio

```text
Self-hosted control plane for small services and agent runtimes.
```

## Chinese bio

```text
Xtrape Capsule：轻量、可私有化部署、基于 Agent 的 Capsule Service 运行态治理控制面。
```

## Short Chinese bio

```text
面向小型服务和 Agent Runtime 的轻量治理控制面。
```

---

# Link Strategy

If a platform allows only one link, use:

```text
https://xtrape-com.github.io/xtrape-capsule-site/
```

In article body, include:

```text
GitHub Public Review issue
xtrape-capsule-ce repository
agent-node repository
contracts-node repository
```

For Public Review phase, the main CTA should be:

```text
Please review the positioning, Quick Start, Agent SDK, and security boundary.
```

Not:

```text
Please star the project.
```

---

# First Posting Sequence

Recommended cadence:

```text
Day 0:
  Create GitHub Public Review issue.

Day 1:
  V2EX feedback post.

Day 2:
  掘金 technical article.

Day 3:
  DEV.to English feedback post.

Day 4:
  Reddit r/selfhosted feedback request.

Day 5:
  知乎 opinion article.

Day 7:
  Summarize feedback and update docs/issues.
```

Do not post to all platforms at once.

---

# Account Security Checklist

For every important account:

```text
[ ] Use unique password.
[ ] Enable 2FA.
[ ] Store recovery codes.
[ ] Use a password manager.
[ ] Do not reuse npm tokens across platforms.
[ ] Do not commit .npmrc with token.
[ ] Keep product contact email separate from personal owner email.
```

For npm specifically:

```text
[ ] Enable 2FA.
[ ] Save recovery codes.
[ ] Use granular access token for future CI publishing.
[ ] Prefer package-scoped token.
[ ] Use public-review tag for prerelease.
```

---

# Current Recommendation

Use personal accounts for ownership now:

```text
GitHub owner: personal account
npm owner: personal account
```

Use product domain for public contact:

```text
hello@xtrape.com
security@xtrape.com
```

Later, when the project is commercialized or team-operated, add:

```text
future company/team GitHub owner
future company/team npm owner
company legal/billing email
```

Do not confuse:

```text
xtrape.com = product domain
company domain = future legal/company identity
```
