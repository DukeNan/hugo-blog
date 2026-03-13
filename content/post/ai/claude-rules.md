---
title: "CLAUDE.md 项目规范"
date: 2026-03-13T14:00:00+08:00
description: "深入解析 Claude Code 的 .claude/rules/ 规则拆分系统和自动记忆机制，解决 CLAUDE.md 臃肿问题，让 Claude 自动从工作中学习项目规范。"
author: "shaun"
featured: true
draft: false
toc: false
usePageBundles: false
codeMaxLines: 10
codeLineNumbers: false
figurePositionShow: true
categories:
  - Technology
tags:
  - AI
  - Claude
---

**当你开始认真使用 Claude Code 时，会发现两个问题：单个 CLAUDE.md 文件变得臃肿，超过 200 行后 Claude 遵守度下降；有些知识你不需要手动写，Claude 完全可以从工作中自动学习。今天我们来解决这两个问题。**

<!-- more -->

## 简介

Claude Code 提供了两套互补的机制来解决项目规范管理问题：

### `.claude/rules/` 规则拆分系统

| 特性 | 说明 |
|------|------|
| **模块化维护** | 每个规则文件专注一个主题 |
| **路径特定规则** | 规则只在处理特定文件时生效 |
| **符号链接支持** | 跨项目共享规则 |
| **用户级规则** | 适用于所有项目的个人偏好 |

### 自动记忆系统

| 特性 | 说明 |
|------|------|
| **自动学习** | Claude 在工作中自动记录笔记 |
| **智能筛选** | 只记录对未来对话有用的信息 |
| **机器本地** | 不在机器间共享，避免冲突 |
| **200 行限制** | 保持高效，避免臃肿 |

## 为什么需要 `.claude/rules/`

### 单文件的问题

想象一下这个场景：你的项目有 50 行技术栈说明、30 行 TypeScript 规则、40 行 React 规范、25 行测试要求、20 行 API 设计指南……

一个 CLAUDE.md 文件超过 200 行后，会出现什么问题？

- **上下文消耗增加**：每次会话都要加载整个文件
- **遵守度下降**：Claude 可能遗漏重要规则
- **团队协作困难**：多人维护一个文件容易冲突

### 规则拆分的优势

使用 `.claude/rules/` 目录拆分规则后：

```
.claude/
├── CLAUDE.md           # 核心配置（50 行）
└── rules/
    ├── typescript.md   # TypeScript 规则（50 行）
    ├── react.md        # React 规则（40 行）
    ├── testing.md      # 测试规则（30 行）
    └── api/            # 按主题分组
        └── design.md   # API 设计规则（25 行）
```

**效果**：

- 主文件清晰，快速浏览
- 各主题独立维护
- 按需加载，节省上下文
- 团队分工明确

## `.claude/rules/` 详解

### 基本设置

**第一步**：创建规则目录

```bash
mkdir -p .claude/rules
```

**第二步**：创建规则文件

每个文件应涵盖一个主题，使用描述性文件名：

```
your-project/
├── .claude/
│   ├── CLAUDE.md           # 主项目指令
│   └── rules/
│       ├── code-style.md   # 代码样式指南
│       ├── testing.md      # 测试约定
│       └── security.md     # 安全要求
```

{{< notice info >}}
所有 `.md` 文件都被递归发现，你可以将规则组织到子目录中。
{{< /notice >}}

**加载顺序**：

- 没有 `paths` frontmatter 的规则在启动时加载
- 优先级与 `.claude/CLAUDE.md` 相同

### 路径特定规则

这是 `.claude/rules/` 最强大的功能：**让规则只在处理特定文件时生效**。

#### 问题场景

你的项目有前端和后端代码，它们有不同的规范：

| 需求 | 前端 | 后端 |
|------|------|------|
| 组件风格 | 函数式组件 | 不适用 |
| API 设计 | 不适用 | RESTful + OpenAPI |
| 样式方案 | Tailwind CSS | 不适用 |

如果把所有规则放在一个文件，处理前端代码时会加载后端规则（浪费上下文），反之亦然。

#### 解决方案

使用 YAML frontmatter 的 `paths` 字段限定规则范围：

```yaml
---
paths:
  - "src/api/**/*.ts"
---

# API 开发规则

- 所有 API 端点必须包括输入验证
- 使用标准错误响应格式
- 包括 OpenAPI 文档注释
```

**效果**：只有处理 `src/api/**/*.ts` 文件时，这些规则才会加载。

#### Glob 模式参考

| 模式 | 匹配 |
|------|------|
| `**/*.ts` | 任何目录中的所有 TypeScript 文件 |
| `src/**/*` | `src/` 目录下的所有文件 |
| `*.md` | 项目根目录中的 Markdown 文件 |
| `src/components/*.tsx` | 特定目录中的 React 组件 |

#### 多模式匹配

你可以指定多个模式，使用大括号扩展匹配多个扩展名：

```yaml
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---

# TypeScript 和测试规则
...
```

{{< notice warning >}}
路径范围规则在 Claude **读取匹配文件时触发**，而不是每次工具使用时。这意味着 Claude 打开 `src/api/users.ts` 时加载 API 规则，不会对每个文件操作都重新加载。
{{< /notice >}}

### 使用符号链接跨项目共享规则

如果你有多个项目，维护多份相同的规则很麻烦。`.claude/rules/` 支持符号链接：

```bash
# 链接整个共享目录
ln -s ~/shared-claude-rules .claude/rules/shared

# 链接单个文件
ln -s ~/company-standards/security.md .claude/rules/security.md
```

**特性**：

- 符号链接被正常加载
- 循环符号链接被检测并处理
- 适合维护公司级标准

### 用户级规则

`~/.claude/rules/` 中的个人规则适用于**所有项目**：

```
~/.claude/rules/
├── preferences.md    # 你的个人编码偏好
└── workflows.md      # 你的首选工作流
```

**加载顺序**：用户级规则在项目规则**之前**加载

**优先级**：项目规则更高（可以覆盖用户级规则）

**适合放什么**：

- 跨项目的个人偏好（如 2 空格缩进）
- 个人工具习惯（如优先使用 pnpm）
- 沟通风格（如中文回复、英文注释）

## 自动记忆系统详解

### 什么是自动记忆

**定义**：Claude 在工作时为自己保存笔记，无需你手动编写。

**Claude 会记录**：

- 构建命令（如 `npm run dev`、`cargo build`）
- 调试见解（如"这个错误通常是因为…"）
- 架构笔记（如"数据流经过这里…"）
- 代码样式偏好（如"这个项目用 camelCase"）
- 工作流习惯（如"测试前需要启动 Redis"）

{{< notice info >}}
关键特性：Claude 根据信息在未来对话中是否有用来决定**值得记住什么**。它不会每个会话都保存所有内容。
{{< /notice >}}

### 存储位置

每个项目在 `~/.claude/projects/<project>/memory/` 获得自己的记忆目录：

```
~/.claude/projects/<project>/memory/
├── MEMORY.md          # 简洁索引，加载到每个会话
├── debugging.md       # 关于调试模式的详细笔记
├── api-conventions.md # API 设计决策
└── ...                # Claude 创建的任何其他主题文件
```

**`<project>` 路径来源**：

- 在 git 仓库中：基于 git 仓库路径
- 同一仓库的所有 worktrees 和子目录**共享一个自动记忆目录**
- 在 git 仓库外：使用项目根目录

{{< notice warning >}}
自动记忆是**机器本地**的，不在机器或云环境之间共享。
{{< /notice >}}

### 工作原理

#### 加载机制

| 文件 | 加载时机 | 加载内容 |
|------|----------|----------|
| `MEMORY.md` | 每次对话开始 | **前 200 行** |
| 主题文件（如 `debugging.md`） | 按需读取 | 完整内容 |

**关键点**：

- `MEMORY.md` 的前 200 行在每次对话开始时加载
- 第 200 行之后的内容在会话开始时不加载
- 主题文件在启动时不加载，Claude 按需读取

#### Claude 如何保持 `MEMORY.md` 简洁

通过将详细笔记移到单独的主题文件中：

```markdown
# MEMORY.md（简洁索引）

## 构建命令
- 启动：`npm run dev`
- 构建：`npm run build`

## 调试笔记
详见 @debugging.md

## API 约定
详见 @api-conventions.md
```

#### 你会看到的提示

在 Claude Code 界面中，你可能看到：

- **"Writing memory"**：Claude 正在更新记忆文件
- **"Recalled memory"**：Claude 正在读取记忆文件

### 启用或禁用

**默认状态**：开启

#### 方法一：通过 `/memory` 切换

在会话中输入 `/memory`，使用自动记忆切换。

#### 方法二：通过项目设置

```json
{
  "autoMemoryEnabled": false
}
```

#### 方法三：通过环境变量

```bash
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
```

### 审计和编辑

一切都是纯 markdown，你可以随时编辑或删除。

#### 查看记忆

运行 `/memory` 命令：

- 列出所有加载的 CLAUDE.md 和规则文件
- 切换自动记忆开关
- 提供打开自动记忆文件夹的链接

#### 直接编辑

选择任何文件在你的编辑器中打开它：

```bash
# 打开当前项目的记忆
code ~/.claude/projects/$(basename $(pwd))/memory/
```

#### 什么时候需要手动编辑？

- Claude 记错了，需要更正
- 想删除不再相关的旧笔记
- 想重组记忆结构

## CLAUDE.md vs 自动记忆

| 特性 | CLAUDE.md | 自动记忆 |
|------|-----------|----------|
| **谁编写** | 你 | Claude |
| **包含内容** | 指令和规则 | 学习和模式 |
| **作用范围** | 项目、用户或组织 | 每个 worktree |
| **加载方式** | 每个会话完整加载 | 每个会话（前 200 行） |
| **用于** | 编码标准、工作流、架构 | 构建命令、调试见解 |

**核心建议**：

- **指导 Claude 行为** → 使用 CLAUDE.md
- **让 Claude 从更正中学习** → 依赖自动记忆

### 典型工作流

#### 场景一：新项目开始

```bash
# 1. 使用 /init 自动生成基础 CLAUDE.md
/init

# 2. 根据项目特点，拆分到 rules/
mkdir -p .claude/rules
```

#### 场景二：工作中发现规律

```bash
# 你告诉 Claude："这个项目总是用 pnpm，不是 npm"
# Claude 自动保存到自动记忆

# 如果你想确保它遵守所有命令：
# 明确告诉 Claude："将其添加到 CLAUDE.md"
```

#### 场景三：团队协作

```
# 项目级规则（团队共享）
.claude/rules/typescript.md

# 用户级规则（个人偏好）
~/.claude/rules/preferences.md

# 自动记忆（Claude 自己学习）
~/.claude/projects/<project>/memory/
```

## 高级技巧

### 规则优先级

当多个规则文件可能适用时，优先级是：

```
具体路径规则 > 通用规则 > 用户级规则
```

**示例**：

| 规则位置 | 路径 | 内容 | 优先级 |
|----------|------|------|--------|
| `.claude/rules/api.md` | `src/api/**/*.ts` | API 规则 | 最高（最具体） |
| `.claude/rules/typescript.md` | 无路径 | TypeScript 规则 | 中等 |
| `~/.claude/rules/prefs.md` | 无路径 | 个人偏好 | 最低 |

### 大型团队管理

#### 排除无关的 CLAUDE.md

在大型 monorepos 中，其他团队的 CLAUDE.md 可能被拾取。

使用 `claudeMdExcludes` 跳过它们：

```json
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

{{< notice warning >}}
托管策略 CLAUDE.md 文件**无法排除**，确保组织范围指令始终适用。
{{< /notice >}}

#### 组织级规则

```bash
# 部署组织范围的 CLAUDE.md
# macOS
sudo vim "/Library/Application Support/ClaudeCode/CLAUDE.md"

# Linux 和 WSL
sudo vim /etc/claude-code/CLAUDE.md

# Windows
notepad "C:\Program Files\ClaudeCode\CLAUDE.md"
```

### 与 Settings 配合

Claude Code 的设置文件也支持记忆相关配置：

```json
{
  "autoMemoryEnabled": true,
  "claudeMdExcludes": [
    "**/node_modules/**"
  ]
}
```

## 实战案例

### 案例 1：Monorepo 中的规则组织

**项目结构**：

```
company-monorepo/
├── frontend/
│   └── .claude/rules/react.md
├── backend/
│   └── .claude/rules/api.md
└── shared/
    └── .claude/rules/typescript.md
```

**效果**：

- 前端开发者只加载前端规则
- 后端开发者只加载后端规则
- 共享规则（如 TypeScript）在 `shared/` 中

### 案例 2：个人偏好 + 项目规则

**用户级规则**（`~/.claude/rules/prefs.md`）：

```markdown
# 我的个人偏好

## 代码风格
- 使用 2 空格缩进
- Git commit message 用英文

## 工具偏好
- 优先使用 pnpm 而非 npm
```

**项目规则**（`.claude/rules/typescript.md`）：

```yaml
---
paths:
  - "src/**/*.ts"
---

# TypeScript 规则

## 必须
- 启用 strict 模式
- 禁止使用 any 类型
```

**效果**：处理 `src/**/*.ts` 文件时，项目规则覆盖个人偏好。

### 案例 3：自动记忆的实际用途

**场景**：你在调试一个复杂的多服务应用。

**Claude 记住了**：

```markdown
# MEMORY.md

## 调试笔记

### API 超时问题
- 通常是因为 Redis 未启动
- 检查：`redis-cli ping`
- 启动：`brew services start redis`

### 数据库迁移
- 迁移前先备份数据库
- 使用 `npm run migrate:down` 回滚
```

下次遇到类似问题时，Claude 会直接回忆起这些经验。

## 常见问题

### Q：Claude 不遵循我的规则怎么办？

**调试步骤**：

1. **运行 `/memory`** 验证规则被加载
2. **检查路径**：文件是否在正确的位置？
3. **检查路径特定规则**：glob 模式是否匹配当前文件？
4. **检查冲突**：是否有多个规则文件提供不同指导？
5. **使指令更具体**："使用 2 空格缩进" 比 "格式化代码好"

### Q：路径特定规则没有生效？

**检查清单**：

- glob 模式是否正确？
- 文件路径是否真的匹配？
- YAML frontmatter 格式是否正确？
- 文件是否以 `.md` 结尾？

**调试命令**：

```bash
# 检查 Claude 看到哪些文件
/memory

# 手动测试 glob 模式
ls -la src/api/**/*.ts
```

### Q：自动记忆保存了错误的内容？

**解决**：

1. 运行 `/memory` 打开记忆文件夹
2. 找到错误的笔记
3. 编辑或删除
4. 告诉 Claude 正确的信息，它会更新记忆

### Q：MEMORY.md 超过 200 行了怎么办？

**Claude 会自动处理**：

Claude 通过将详细笔记移到单独的主题文件中来保持 `MEMORY.md` 简洁。

你也可以手动重组：

```markdown
# MEMORY.md（保持简洁）

## 核心规则
...

## 详细笔记
- 调试：@debugging.md
- API：@api-conventions.md
```

## 最佳实践

### 规则组织

**推荐做法**：

- 每个规则文件专注一个主题
- 使用描述性文件名
- 路径特定规则用于特定文件类型
- 共享规则用符号链接

**避免**：

- 一个文件包含太多主题
- 文件名不清晰（如 `rules1.md`、`stuff.md`）
- 复制粘贴相同内容到多个文件

### 自动记忆

**推荐做法**：

- 让 Claude 自然学习
- 定期审计记忆内容
- 手动更正错误的记忆

**避免**：

- 过度依赖自动记忆（核心规则应在 CLAUDE.md）
- 从不查看 Claude 记住了什么
- 在机器间同步记忆文件（可能导致冲突）

### 团队协作

**推荐做法**：

- 项目规则通过 Git 管理
- 个人规则用 `~/.claude/rules/`
- 使用符号链接共享公司级标准

**避免**：

- 将个人偏好提交到项目 CLAUDE.md
- 在团队中硬编码本地路径（如 `/Users/username/...`）

## 总结

### `.claude/rules/` 的核心价值

- 模块化维护
- 路径特定规则节省上下文
- 符号链接支持跨项目共享
- 用户级规则适用于所有项目

### 自动记忆的核心价值

- Claude 自动学习，无需手动编写
- 记录构建命令、调试见解等实战经验
- 通过 200 行限制保持高效

### 两者配合

- CLAUDE.md 和 rules/ 用于**指导行为**
- 自动记忆用于**从经验中学习**

## 参考资源

- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code 记忆体系详解](https://mp.weixin.qq.com/s?__biz=MzIxMzYwNDM3MQ==&mid=2247484976&idx=1&sn=32d6baf7f09fd1b1f9ffde5a715e021d)
- [真正会用 Claude Code 的人，都先做这一步](https://mp.weixin.qq.com/s?__biz=MzIxMzYwNDM3MQ==&mid=2247484963&idx=1&sn=06fbf47008b153bda2c8953f32668c21)