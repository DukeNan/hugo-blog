---
title: "三器合一：OpenSpec 管需求，Superpowers 管质量，gstack 管全流程"
date: 2026-05-14T10:00:00+08:00
description: "OpenSpec + Superpowers + gstack 三套工具如何在同一个 Claude Code 会话中自动串联，实现从需求到发布的完整 AI 工程流水线"
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
  - agent
---

**OpenSpec 管需求，Superpowers 管质量，gstack 管全流程——三个工具解决三个不同的问题，装在一起不冲突。** 关键不是"三个工具都装上"，而是它们之间怎么自动串联。本文用一个完整案例讲清楚三套工具如何从需求到发布无缝衔接。

<!-- more -->

![三器合一概览](/images/ai/ai_007.png)

## 三套工具，三个层次

| 工具 | 管什么 | 核心机制 |
|------|--------|----------|
| OpenSpec | 做什么 | DAG 产物依赖图，写代码前先对齐需求 |
| Superpowers | 做得好 | HARD-GATE + TDD 铁律，自动拦截低质量代码 |
| gstack | 怎么做、怎么发 | Browse 引擎 + 7 阶段 Sprint 管线 |

## 安装：三者共存的方式

图片中的命令如下：

```bash
# gstack：全局安装，./setup 自动配置 Claude Code 技能目录
git clone https://github.com/garrytan/gstack.git && cd gstack && ./setup

# Superpowers：Claude Code 插件，装完自动生效
# 在 Claude Code 中运行：/plugins install superpowers

# OpenSpec：npm 全局包，init 时生成 Claude Code 的 slash 命令
npm install -g @fission-ai/openspec@latest
cd your-project && openspec init --tools claude
```

装完之后，三个工具在同一个 Claude Code 会话里共存。OpenSpec 的 `/opsx:*` 命令、Superpowers 的 TDD 铁律、gstack 的 `/ship` `/review` `/qa` 技能，全部在同一个 REPL 里可用。

它们不互相覆盖，因为管的层次不同。OpenSpec 的产物存在 `openspec/` 目录，Superpowers 的规则存在 CLAUDE.md 和 skill 文件里，gstack 的状态存在 `.gstack/` 目录。三套状态互不干扰。

## 核心问题：它们之间怎么串联

![串联机制](/images/ai/ai_008.png)

这是最关键的部分。三个工具不是"你用完我再用"的接力赛，而是**在同一个会话里自动触发、互相衔接**。

### 串联点 1：OpenSpec 的产物 → gstack 的评审输入

OpenSpec 的 `/opsx:propose` 会生成四个文件：`proposal.md`、`specs/`、`design.md`、`tasks.md`。这些文件落盘后，gstack 的 `/autoplan` 能直接读取它们作为评审输入。

具体机制：`/autoplan` 启动 CEO → design → eng → DX 四类评审。每个评审角色会读取当前工作区的文件。因为 OpenSpec 的产物就在 `openspec/changes/<change-id>/` 目录下，评审角色自然能读到 proposal 和 specs。

你不需要手动复制粘贴。OpenSpec 写完产物，gstack 的评审直接读文件。

### 串联点 2：Superpowers 的 HARD-GATE → 自动拦截编码

Superpowers 的 `brainstorming` skill 有一个 HARD-GATE：

```
Do NOT invoke any implementation skill, write any code, scaffold
any project, or take any implementation action until you have
presented a design and the user has approved it.
```

这意味着：即使你跳过了 OpenSpec 直接说"帮我加个功能"，Superpowers 也会强制你先走设计流程。它不需要知道 OpenSpec 的存在——它只关心"设计有没有被批准"。

如果 OpenSpec 已经生成了 `design.md`，你把它展示给 Superpowers 看，它会把这份设计当作"已批准的设计"，HARD-GATE 自动放行。这就是串联：OpenSpec 的产物满足了 Superpowers 的门禁条件。

### 串联点 3：Superpowers 的 TDD → gstack 的 /review 自动生效

Superpowers 的 TDD 铁律要求"先写失败测试再写代码"。这个过程不需要你手动触发——它是 skill 文件里的规则，Claude Code 每次写代码时自动遵守。

写完代码后，你运行 gstack 的 `/review`。`/review` 不关心代码是怎么写出来的——它只看 diff。但它会发现：因为 TDD 铁律的存在，每个功能都有对应的测试。`/review` 的审查质量因此更高，因为它有测试作为行为契约。

### 串联点 4：gstack 的 /ship → OpenSpec 的 /opsx:archive

`/ship` 发布完成后，你运行 `/opsx:archive`。归档过程读取 `openspec/changes/<change-id>/` 下的 Delta 规范，自动合并到 `openspec/specs/` 主规范里。

归档不触发发布，发布不触发归档。它们是两个独立步骤，但顺序固定：先 `/ship` 上线，再 `/opsx:archive` 收尾。

## 实战案例：给应用加暗色模式

一个功能从想法到上线的完整流程。重点不是"做了什么"，而是**每一步怎么触发下一步、工具之间怎么衔接**。

### 第 1 步：OpenSpec 生成需求产物

```
/opsx:propose add-dark-mode
```

```
给应用加暗色模式：
1. 设置页加主题切换开关
2. 支持跟随系统偏好
3. 用户选择持久化到 localStorage
4. 所有页面即时切换
```

OpenSpec 的 DAG 引擎解析依赖关系，自动生成四个产物：

```
openspec/changes/add-dark-mode/
├── proposal.md          ← 为什么做
├── specs/ui/spec.md     ← 需求场景（GIVEN/WHEN/THEN）
├── design.md            ← 技术方案（CSS 变量 + Context）
├── tasks.md             ← 任务清单（4 组 8 个子任务）
└── .openspec.yaml       ← 变更元数据
```

DAG 引擎告诉你：proposal 已完成，specs 和 design 可以并行创建，tasks 等它们都完成才能开始。你不需要手动管理这个顺序——`/opsx:propose` 一次性生成全部产物。

**串联触发：** 产物落盘后，gstack 的评审角色可以直接读取这些文件。

### 第 2 步：gstack /autoplan 读取产物做评审

```
/autoplan
```

`/autoplan` 自动串起四类评审。每个评审角色读取 `openspec/changes/add-dark-mode/` 下的文件：

- **CEO 评审**读 `proposal.md`：暗色模式是不是当前优先级最高的？范围是否合理？
- **工程评审**读 `design.md`：CSS 变量方案的浏览器兼容性？Context Provider 的性能影响？
- **设计评审**读 `specs/ui/spec.md`：暗色模式的色彩对比度是否符合 WCAG 标准？
- **DX 评审**读 `tasks.md`：任务拆分是否合理？其他开发者能否扩展暗色主题？

评审结论写入 gstack 的计划文件，锁住设计约束：必须用 CSS 自定义属性，不能用 CSS-in-JS。

**串联触发：** 评审通过后，进入编码阶段。此时 Superpowers 的 HARD-GATE 检查"设计是否已批准"——OpenSpec 的 `design.md` + gstack 的评审结论满足了这个条件，HARD-GATE 自动放行。

### 第 3 步：Superpowers TDD 铁律自动生效

你没有手动调用 Superpowers 的任何命令。TDD 铁律是 skill 文件里的规则，Claude Code 写代码时自动遵守。

开始实现 tasks.md 里的第一个任务"创建 ThemeContext"：

```javascript
// 1. 先写失败测试
test('default theme should be light', () => {
  const { result } = renderHook(() => useTheme());
  expect(result.current.theme).toBe('light'); // ← 失败！useTheme 不存在
});

// 2. 写最小实现
function useTheme() {
  return { theme: 'light' };
}

// 3. 测试变绿。写下一个失败测试
test('toggleTheme should switch to dark', () => {
  const { result } = renderHook(() => useTheme());
  act(() => result.current.toggleTheme());
  expect(result.current.theme).toBe('dark'); // ← 失败！toggleTheme 不存在
});

// 4. 写实现。测试变绿。重构。
```

子代理驱动（如果启用）：每个 tasks.md 里的任务用一个全新的子代理执行。子代理读取 `openspec/changes/add-dark-mode/specs/ui/spec.md` 作为需求输入，读取 `design.md` 作为技术约束。执行完后做两阶段审查：先查是否符合 specs/，再查代码质量。

**串联触发：** 所有任务实现完成后，运行 gstack 的 `/review`。

### 第 4 步：gstack /review 审查代码

```
/review
```

`/review` 扫描当前分支的 diff。因为 Superpowers 的 TDD 铁律确保了每个功能都有测试，`/review` 的审查质量更高——它可以用测试作为行为契约来验证实现是否正确。

`/review` 找出一个问题：`localStorage.setItem` 没有 try-catch，在 Safari 隐私模式下会抛异常。修复后继续。

**串联触发：** 审查通过后，运行 `/qa` 做真实浏览器验收。

### 第 5 步：gstack /qa 浏览器验收

```
/qa
```

`/qa` 用 Playwright Chromium 打开应用，执行真实用户操作：

1. `$B goto http://localhost:3000/settings` — 打开设置页
2. `$B snapshot -i` — 获取可访问性快照，找到主题切换开关
3. `$B click @e5` — 点击切换开关
4. `$B screenshot` — 截图验证暗色模式生效
5. `$B reload` — 刷新页面
6. `$B screenshot` — 验证主题持久化
7. `$B eval prefers-color-scheme` — 验证跟随系统偏好

QA 报告发现 3 个页面的对比度不达标。修复后重新验证，全部通过。

**串联触发：** QA 通过后，运行 `/ship`。

### 第 6 步：gstack /ship 发布

```
/ship
```

`/ship` 自动执行一系列操作：

1. `git fetch origin main` — 同步远程
2. `bun test` — 跑单元测试
3. 覆盖率审计 — 检查新增代码的测试覆盖
4. VERSION 升级 — v1.5.0.0 → v1.6.0.0（MINOR，因为是新功能）
5. CHANGELOG 生成 — 从 git log 提取变更摘要
6. `git push` — 推送代码
7. `gh pr create` — 创建 PR

```
/land-and-deploy
```

合并 PR、等 CI、部署到生产环境。

```
/canary
```

监控部署后 30 分钟的错误率和性能指标。

**串联触发：** 发布完成后，运行 OpenSpec 的归档。

### 第 7 步：OpenSpec /opsx:archive 归档

```
/opsx:archive add-dark-mode
```

归档过程：

1. 读取 `openspec/changes/add-dark-mode/specs/ui/spec.md` 中的 Delta 规范
2. `## ADDED Requirements` 追加到 `openspec/specs/ui/spec.md`
3. `## MODIFIED Requirements` 替换主规范中的同名需求
4. 变更文件夹移入 `openspec/changes/archive/2026-05-12-add-dark-mode/`

归档后，`openspec/specs/` 目录始终反映系统当前状态。下次再加功能时，OpenSpec 的 AI 会读取这些 specs 作为上下文。

## 串联机制总览

整个流程中，你手动输入的命令只有 7 个：

```
/opsx:propose → /autoplan → (写代码) → /review → /qa → /ship → /opsx:archive
```

但背后自动发生的事情远不止这些：

| 你输入的 | 自动发生的 |
|----------|-----------|
| `/opsx:propose` | DAG 引擎解析依赖，生成 4 个产物文件 |
| `/autoplan` | 4 个评审角色读取 OpenSpec 产物，输出评审结论 |
| （写代码） | Superpowers HARD-GATE 检查设计是否批准（是），TDD 铁律自动拦截（先写测试） |
| `/review` | gstack 读取 diff + 测试，找出生产级 bug |
| `/qa` | Playwright Chromium 执行真实浏览器操作 |
| `/ship` | VERSION + CHANGELOG + PR + 推送 |
| `/opsx:archive` | Delta 规范合入主规范，归档变更 |

三个工具之间的衔接不需要你手动传递数据。OpenSpec 的产物落盘后，gstack 的评审角色直接读文件。gstack 的评审结论满足了 Superpowers 的 HARD-GATE 条件。Superpowers 的 TDD 铁律确保了 /review 有测试可依。

这就是"三器合一"的核心：不是三个独立工具的拼凑，而是**三套规则在同一个会话里自动生效、互相补位**。

## 避坑指南

{{< notice warning >}}
不要重复门禁。Superpowers 的 HARD-GATE 已经卡住设计审批了，就不要再用 gstack 的 `/plan-design-review` 重复审查同一份设计。两套门禁同时跑会出矛盾。推荐：Superpowers 管设计门禁（更严），gstack 管代码审查（有浏览器验证）。
{{< /notice >}}

**specs/ 是唯一真相源。** OpenSpec 的 `openspec/specs/` 定义需求，gstack 的设计文档只描述实现细节。需求有冲突时以 specs/ 为准。

**/ship 是唯一发布出口。** OpenSpec 归档只是收尾记录，不是发布。所有代码通过 gstack 的 `/ship` 流向生产。

**TDD 有三个例外。** 一次性原型、生成的代码、配置文件——这三种场景可以跟 AI 说"这是原型，跳过 TDD"。除此之外，Superpowers 的铁律不打折扣。

## 总结

- OpenSpec 在写代码之前把需求锁住，通过 DAG 依赖图确保产物完整
- Superpowers 在写代码的时候把质量卡住，HARD-GATE + TDD 双重保障
- gstack 在写完代码之后把发布包了，从审查到上线一站式完成
- 三套规则同一个会话里自动生效，你只管输入斜杠命令，剩下的串联是自动的
****

## 参考资源

- [gstack GitHub 仓库](https://github.com/garrytan/gstack)
- [Superpowers GitHub 仓库](https://github.com/beshu-tech/superpowers)
- [OpenSpec 项目文档](https://github.com/openspec-dev/openspec)
