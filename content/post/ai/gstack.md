---
title: "Gstack：把 AI Agent 组织成虚拟软件团队的 23 个专家角色"
date: 2026-04-25T19:00:34+08:00
description: "深度解析 Garry Tan 开源的 gstack 框架——23 个专家 Skill + 8 个 Power Tool，如何将单个 AI 编程代理变成一支完整的软件工程团队"
author: "shaun"
featured: true
draft: false
toc: false
usePageBundles: false
codeMaxLines: 10
codeLineNumbers: false
figurePositionShow: true
categories:
  - AI
tags:
  - Agent
---

## 引子

> "I don't think I've typed like a line of code probably since December."

这句话来自 Andrej Karpathy。而在 2025 到 2026 年间，Y Combinator CEO **Garry Tan** 用实际行动证明了这句话的分量——他借助一套名为 **gstack** 的开源框架，在全职运营 YC 的同时，用 AI 编码工具完成了 **3 个生产服务和 40 多个功能**的交付。据他自己测算，生产效率达到了 2013 年手敲代码时的约 **810 倍**（日均逻辑行数 11,417 vs 14）。

gstack 在 GitHub 上开源后迅速走红，同时也引发了开发者社区的激烈讨论：有人惊叹于它把 AI 编程从"聊天窗口"升级为"工程流水线"，也有人质疑它的安全性。这篇博客将深入拆解 gstack 的架构、技能体系和核心设计理念。

---

## 一、gstack 是什么？

**gstack** 是 Garry Tan 开源的 Claude Code 增强框架，采用 **MIT 协议**，核心思路可以用一句话概括：

> AI Agent 需要的是组织结构图，而不仅仅是一堆提示词。

具体来说，gstack 将单个 AI 编程代理（如 Claude Code）变成了一支拥有 **23 个专家角色** 和 **8 个独立工具** 的虚拟软件工程团队。它不写一行代码本身，而是通过 **Markdown 格式的 Skill 指令集**，给 AI 代理赋予结构化的工作流。

### 1.1 核心定位

| 对比维度 | Superpowers | gstack |
|---------|-------------|--------|
| 侧重方向 | 偏软件研发执行层 | 更高层级，拟人化的角色分工 |
| 工作方式 | 单角色提示词增强 | 多角色阶段化流水线 |
| 产出物 | 代码 | Skills（可复用的指令集） |

gstack 比 Superpowers 更抽象、更接近"管理层"。它关心的不是"怎么写好这段代码"，而是"谁该来写、什么时候写、写完之后谁来审"。

### 1.2 兼容范围

虽然最初为 Claude Code 设计，但 gstack 目前已兼容 **10+ AI 编码代理**，包括 Claude Code、OpenAI Codex CLI、OpenCode、Cursor、Kiro 等，并能自动检测当前使用的代理类型。

---

## 二、架构设计

gstack 的工作流分为 **7 个阶段**，形成一个闭环：

```
Think（思考）→ Design（设计）→ Build（构建）→ Review（评审）→ Test（测试）→ Ship（交付）→ Reflect（回顾）
```

### 2.1 整体架构图

![gstack 架构图](/images/ai/ai_006.png)

### 2.2 关键设计决策

- **全 Markdown**：除了浏览器组件，其余全部是 Markdown 指令——可审计、可修改、可版本控制
- **Skill 间数据流**：前一个 Skill 的输出会成为后一个 Skill 的输入，形成流水线
  - 例如 `/office-hours` 生成文档 → `/plan-ceo-review` 读取该文档
- **本地优先**：遥测默认关闭，检查点存储在本地
- **100% 测试覆盖率目标**：`/qa` 修复后自动生成回归测试
- **并行执行**：通过 Conductor 模式支持 10-15 个 Sprint 并行运行

---

## 三、23 个专家 Skill 详解

gstack 的 23 个 Skill 以**斜杠命令**的形式存在，分为 7 大类：

### 3.1 Think（思考阶段）

这个阶段的核心是**重新定义问题**——在动手之前先思考"是否该做"和"做什么"。

| 命令 | 角色 | 功能 |
|------|------|------|
| `/office-hours` | YC Office Hours | 6 个强制性问题，帮你重新框定产品方向 |
| `/plan-ceo-review` | CEO/创始人 | 战略性挑战，4 种范围模式 |
| `/plan-eng-review` | 工程经理 | 架构分析、数据流梳理、边界情况检查 |
| `/plan-design-review` | 高级设计师 | 0-10 分设计评分，AI 低质内容检测 |
| `/plan-devex-review` | 开发者体验负责人 | DX 审计，20-45 个问题 |
| `/autoplan` | 评审流水线 | 自动执行 CEO → 设计 → 工程 → DX 全流程 |

### 3.2 Design（设计阶段）

| 命令 | 角色 | 功能 |
|------|------|------|
| `/design-consultation` | 设计搭档 | 从零构建设计系统 |
| `/design-shotgun` | 设计探索器 | 生成 4-6 个 AI 模型方案，具备审美记忆 |
| `/design-html` | 设计工程师 | 生产级 HTML（基于 Pretext，30KB，0 依赖） |

### 3.3 Build（构建阶段）

这一组命令关注**安全护栏**，而非编码本身。

| 命令 | 角色 | 功能 |
|------|------|------|
| `/careful` | 安全护栏 | 执行破坏性命令前警告 |
| `/freeze` | 编辑锁 | 限制编辑范围到指定目录 |
| `/guard` | 全面安全 | `/careful` + `/freeze` 组合 |
| `/unfreeze` | 解锁 | 移除冻结边界 |

### 3.4 Review（评审阶段）

| 命令 | 角色 | 功能 |
|------|------|------|
| `/review` | 主任工程师 | 生产级 Bug 检测，自动修复 |
| `/codex` | 第二意见 | 接入 OpenAI Codex CLI 交叉评审 |
| `/cso` | 首席安全官 | OWASP + STRIDE 安全审计 |
| `/design-review` | 会写代码的设计师 | 审计 + 修复，原子化提交 |

### 3.5 Test（测试阶段）

| 命令 | 角色 | 功能 |
|------|------|------|
| `/qa` | QA 负责人 | 真实浏览器测试，回归测试 |
| `/qa-only` | QA 报告员 | 仅报告 Bug，不修改代码 |
| `/browse` | QA 工程师 | 真实 Chromium 浏览器（~100ms/指令） |
| `/open-gstack-browser` | GStack 浏览器 | 带侧边栏的有头模式 |
| `/setup-browser-cookies` | 会话管理器 | 导入真实浏览器 Cookie |
| `/pair-agent` | 多代理协调器 | 跨代理共享浏览器会话 |

### 3.6 Ship（交付阶段）

| 命令 | 角色 | 功能 |
|------|------|------|
| `/ship` | 发布工程师 | 同步 → 测试 → 审计 → 创建 PR |
| `/land-and-deploy` | 发布工程师 | 合并 → CI → 部署 → 验证 |
| `/canary` | SRE | 部署后金丝雀监控 |
| `/benchmark` | 性能工程师 | Core Web Vitals 基线 |
| `/setup-deploy` | 部署配置器 | 一次性平台配置 |

### 3.7 Reflect（回顾阶段）

| 命令 | 角色 | 功能 |
|------|------|------|
| `/retro` | 工程经理 | 每周回顾，跨项目分析 |
| `/document-release` | 技术写手 | 自动更新所有文档 |
| `/investigate` | 调试器 | 根因分析，Iron Law 协议 |

### 3.8 Memory（记忆系统）

| 命令 | 角色 | 功能 |
|------|------|------|
| `/learn` | 记忆 | 管理模式、坑点、偏好 |
| `/context-restore` | 会话恢复 | 从 WIP 提交恢复 |
| `/context-save` | 检查点 | 手动保存检查点 |

---

## 四、8 个 Power Tool

除了 Slash Command 形式的 Skill，gstack 还提供了 8 个独立的 CLI 工具：

| 工具 | 功能 |
|------|------|
| `gstack-model-benchmark` | 跨模型基准测试（Claude/GPT/Gemini）— 延迟、Token 数、成本、LLM 裁判 |
| `gstack-taste-update` | 设计审美学习 — 持久化 `/design-shotgun` 的批准/拒绝记录 |
| `gstack-team-init` | 团队模式启动 — 共享仓库自动更新 |
| `gstack-uninstall` | 干净卸载 — 移除 skills、符号链接、状态、守护进程 |
| `gstack-analytics` | 本地使用数据仪表盘 |
| `gstack-config` | 配置管理 |
| `gstack-brain-init` | GBrain 记忆同步 |
| `gstack-upgrade` | 自更新 |

---

## 五、安全设计

gstack 内置了**分层提示词注入防御系统**：

1. **本地 ML 分类器**：22MB 的模型，实时检测注入攻击
2. **Haiku 检查**：使用 Claude Haiku 进行二次验证
3. **Canary Token**：蜜罐令牌，检测越权访问
4. **DeBERTa-v3**：可选的额外检测层

此外，`/careful`、`/freeze` 和 `/guard` 三个 Skill 提供了操作级别的安全护栏，在执行破坏性命令或限制编辑范围时发挥作用。

---

## 六、安装与使用

### 6.1 快速安装

```bash
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup
```

整个过程大约 30 秒。

### 6.2 团队模式

对于共享仓库，可以启用团队模式实现自动更新：

```bash
(cd ~/.claude/skills/gstack && ./setup --team) && ~/.claude/skills/gstack/bin/gstack-team-init required
```

团队模式确保所有成员使用相同版本的 Skill 指令，避免版本漂移。

---

## 七、典型工作流

下面以"从零构建一个 MVP"为例，展示 gstack 的完整工作流：

```
1. /office-hours        → 用 6 个强制性问题重新框定产品
2. /design-consultation → 构建设计系统
3. /plan-ceo-review     → CEO 视角战略挑战
4. /plan-eng-review     → 工程经理架构审查
5. /plan-design-review  → 设计师评分
6. /guard               → 开启安全护栏
7. 编码实施              → AI 代理开始写代码
8. /review              → 主任工程师 Bug 检测
9. /qa                  → 真实浏览器测试
10. /ship               → 创建 PR
11. /retro              → 项目回顾
```

每个阶段的输出都会作为下一阶段的输入，形成完整的信息流。

---

## 八、社区争议

gstack 走红的同时也引发了一些争议：

- **安全性担忧**：有人质疑 gstack 是否构成"木马"，因为它需要较高的系统权限和浏览器控制能力
- **复杂度**：23 个 Skill 对小型项目来说可能过于繁重
- **厂商绑定**：虽然兼容多个代理，但核心设计仍围绕 Claude Code

对于这些争议，gstack 团队采用了 MIT 开源协议、本地优先的架构和分层安全防御来回应。

---

## 九、横向对比

| 维度 | gstack | Superpowers | GSD |
|------|--------|-------------|-----|
| 定位 | 虚拟团队管理 | 软件研发增强 | 项目阶段管理 |
| Skill 数量 | 23 | 较少 | 50+ |
| 浏览器能力 | 内置 Chromium | 无 | 无 |
| 多代理支持 | 10+ 代理 | Claude Code | Claude Code |
| 安全护栏 | `/careful` `/freeze` `/guard` | 基础 | 基础 |
| 记忆系统 | `/learn` + GBrain | 无 | 阶段化文件 |

---

## 十、总结

gstack 代表了一种不同于"堆砌更多代码能力"的 AI 编程进化路径。它的核心洞察是：

> **问题不在于 AI 会不会写代码，而在于谁来决定写什么、什么时候写、写完之后谁来审。**

通过 23 个专家角色和 7 阶段流水线，gstack 把 AI 编程从"聊天窗口"变成了一个有组织结构、有流程约束、有质量把关的虚拟软件团队。

如果你正在用 Claude Code 或类似的 AI 编程工具，并且觉得"每次都是从零开始的对话"，那么 gstack 的流水线思维值得借鉴——即使不直接使用它的 23 个 Skill，其**"Think → Design → Build → Review → Test → Ship → Reflect"** 的闭环理念，本身就是对 AI 编程工作流的一次系统性升级。

---

**参考链接：**

- [gstack GitHub 仓库](https://github.com/garrytan/gstack)
- [gstack 架构文档](https://github.com/garrytan/gstack/blob/main/ARCHITECTURE.md)
- [gstack Skills 文档](https://github.com/garrytan/gstack/blob/main/docs/skills.md)
- [Garry Tan's gstack and the rise of AI agent teams](https://agentscodex.com/posts/2026-03-20-garry-tan-gstack-agent-teams-claude-code/)
- [How Garry Tan Uses GStack to Turn Claude Code Into a Dev Team](https://www.sitepoint.com/gstack-garry-tan-claude-code/)
- [gstack 深度解析（中文）](https://xwuxl.com/2026/03/22/gstack-skill-deep-dive/)
- [gstack Tutorial Series](https://www.ququ123.top/en/2026/04/gstack-tutorial-series-intro/)
- [gstack 通过角色阶段的 AI Coding Skills](https://www.cnblogs.com/rongfengliang/p/19792309)
