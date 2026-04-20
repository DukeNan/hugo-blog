---
title: "Graphify：Claude Code 生态中被低估的知识工程利器"
date: 2026-04-20T09:53:12+08:00
description: "Graphify 是 Claude Code 生态中增长最快的 Skill 之一，它能将代码、文档、论文、图片转化为可查询的知识图谱，实现 71.5 倍 Token 压缩，零服务器依赖，完全本地运行。"
author: "shaun"
featured: true
draft: false
toc: false
usePageBundles: false
codeMaxLines: 15
codeLineNumbers: true
figurePositionShow: true
categories:
  - Technology
tags:
  - AI
---

Andrej Karpathy 曾提到他有一个 `/raw` 文件夹，里面堆积着论文 PDF、推文截图、随手记下的笔记、白板照片——知识的原始形态。问题是：当需要查找某个概念时，他得手动翻阅这一切。

这不是 Karpathy 一个人的问题。每个程序员、每个研究者、每个试图用 AI 处理复杂信息的人，都面临同样的困境：

- 代码库越来越大，模块之间的关系像 spaghetti
- 论文读了一堆，却想不起哪篇提到了那个关键的优化技巧
- 截图里的架构图、白板上的设计草图，成了"数字废墟"

**Graphify** 的出现，正是为了解决这个困境。它不是又一个向量数据库，不是又一套 RAG 流水线——**它是一套将任意信息（代码、文档、论文、图片）转化为可查询知识图谱的完整工程方案**。

## 从 RAG 到 GraphRAG：检索范式的进化

传统的 RAG（Retrieval-Augmented Generation）工作流程是：

```
文档 → 分块 → Embedding → 向量数据库 → 相似度检索 → LLM 生成
```

这个流程的问题在于：**它丢失了文档之间的结构关系**。当你问"Attention 机制如何影响优化器设计？"时，向量检索可能分别找到关于 Attention 的段落和关于优化器的段落，但无法理解它们之间的逻辑关联。

知识图谱的做法完全不同：

```
文档 → 实体抽取 → 关系抽取 → 图谱构建 → 图遍历检索 → LLM 生成
```

**关键差异**：图谱保留了"概念 A 通过关系 R 影响概念 B"这样的结构化信息。检索不再是"找相似的文本块"，而是"沿着关系路径遍历"。

## Graphify 的三阶段处理流程

Graphify 最值得理解的设计是它对不同文件类型的差异化处理——每种处理方式都有完全不同的数据隐私考量。

### Pass 1: 确定性 AST 提取（代码不离开本地）

对于源代码文件，Graphify 使用 **tree-sitter**——一个确定性、基于规则的解析器。它读取文件、应用形式语法、输出结构化语法树。**不涉及语言模型，不发起网络请求，源代码完全留在本地。**

tree-sitter 支持 23 种语言：Python、TypeScript、JavaScript、Go、Rust、Java、C、C++、Ruby、C#、Kotlin、Scala、PHP 等。输出是一组节点/边字典，编码每个函数、类、import 和调用关系。

AST 提取的关系带有 `EXTRACTED` 置信度标签——这是事实，不是猜测。

### Pass 2: 本地音频转录（录音不离开本地）

如果目录包含音频或视频文件，Graphify 使用 **faster-whisper** 进行转录，它完全在本地机器上运行。音频永远不会上传到任何地方。

```bash
pip install "graphifyy[video]"
```

faster-whisper 是 CTranslate2 加速的 Whisper 模型实现。在现代笔记本上，它能在几分钟内转录一小时的会议音频。

### Pass 3:语义提取（文档和图片发送到你的 AI API）

Markdown、PDF、RST 文档，以及 PNG、JPG、WebP、GIF 图片无法用语法解析。Graphify 会调用你配置的 AI 平台——Anthropic、OpenAI 或其他。

**关键点**：Graphify 使用你已在 AI 平台环境中配置的凭证。它没有中央中继服务器。流量直接从你的机器发送到 Anthropic（或 OpenAI 等），使用你已有的 API key。

Graphify 本身不收集任何数据。SECURITY.md 明确声明："在图分析期间不发起任何网络调用"。项目还声明没有遥测、没有使用追踪、没有任何分析。凭证不被 Graphify 存储。

## 置信度系统：知道图谱知道什么

图谱中的每条边都有三种置信度标签：

| 标签 | 含义 | 示例 |
|------|------|------|
| **EXTRACTED** | 关系明确存在于源文件中 | `validate_card` 被 `process_payment` 调用——这是 AST 中的事实 |
| **INFERRED** | 模型从上下文推理出的关系 | `PaymentService` 和 `FraudDetector` 在文档中总是被一起引用，推断存在依赖 |
| **AMBIGUOUS** | 模型标记为不确定的关系 | 需要人工审核的连接 |

这体现了 Graphify 的核心价值观：**诚实面对不确定性，让用户知道什么是找到的、什么是猜的**。

## 快速上手

### 安装

```bash
pip install graphifyy && graphify install
```

> 注意：PyPI 包名为 `graphifyy`（临时名称，原 `graphify` 名称正在回收中）

可选依赖组：

```bash
pip install "graphifyy[video]"    # 音频/视频转录
pip install "graphifyy[office]"   # Office 文档
pip install "graphifyy[mcp]"      # MCP 服务器
pip install "graphifyy[all]"      # 全部功能
```

### 基础用法

```bash
# 在 Claude Code 中执行
/graphify .                        # 分析当前目录
/graphify ./src --deep             # 深度分析，更激进的关系推断
/graphify ./raw --update           # 只处理变更的文件
/graphify ./raw --watch            # 监视模式
/graphify --install-hooks          # 安装 Git 提交钩子
```

### 查询图谱

```bash
/graphify query "认证流程如何在整个系统中流转？"
/graphify path "UserService" "DatabasePool"
/graphify explain "PaymentProcessor"
```

### 输出结构

```
graphify-out/
├── graph.html          # 交互式图谱可视化
├── obsidian/           # Obsidian 知识库格式
├── wiki/               # Wikipedia 风格文章
├── GRAPH_REPORT.md     # 分析报告：God Nodes、意外连接、建议问题
├── graph.json          # 持久化图谱数据
└── cache/              # SHA256 缓存，增量更新用
```

## Token 效率：71.5 倍压缩是如何实现的

官方基准测试结果：

| 语料库 | 文件数 | Token 压缩比 | 输出 |
|--------|--------|--------------|------|
| Karpathy repos + 5 papers + 4 images | 52 | **71.5x** | 52 个文件的结构化图谱 |
| graphify 源码 + Transformer paper | 4 | **5.4x** | 混合语料图谱 |
| httpx（合成 Python 库） | 6 | ~1x | 小语料结构清晰 |

压缩原理来自三个层面：

**1. 结构压缩**——原始文件包含大量冗余信息，图谱只保留概念和关系的精简表达。

**2. 关系索引**——向量检索需要比较查询与所有文档块的相似度（O(N)），图遍历只需沿着相关边探索，实际访问的节点数通常只有总数的 5-10%。

**3. 语义缓存**——SHA256 缓存每个文件的提取结果。重复运行时，只有变更的文件需要重新处理。

## 适用场景分析

**适合使用 Graphify：**

- 混合媒体项目：代码、架构文档、设计 PDF、会议录音在同一仓库
- 稳定代码库上的重复查询——缓存收益随时间复合增长
- 使用 Claude Code 的团队，希望降低每会话 API 成本
- 复杂调用图项目：语义搜索困难（深度继承链、大量回调架构）

**不适合使用：**

- 少于 ~20 个文件的全新项目——图谱开销不值得
- 全部内容是纯文档的仓库——扁平 RAG 对开放式语义问题可能更好
- AI 提供商的数据处理政策禁止发送文档内容到其 API
- 需要可验证、可复现分析的项目——INFERRED 和 AMBIGUOUS 边可能误导

## 与 MemPalace 的协同

Graphify 与 MemPalace 形成了有趣的互补：

| 维度 | MemPalace | Graphify |
|------|-----------|----------|
| 核心能力 | 记忆存储与检索 | 知识结构化和查询 |
| 数据形态 | 对话历史、笔记 | 代码、论文、图片 |
| 查询方式 | 语义搜索 | 图遍历 |
| 最佳场景 | "我之前讨论过什么" | "这个概念与什么相关" |

协同工作流：

1. 用 MemPalace 记录研究笔记和对话上下文
2. 用 Graphify 构建论文和代码的知识图谱
3. 回答复杂问题时：MemPalace 提供笔记和历史讨论，Graphify 提供论文与代码之间的映射关系

## 总结

Graphify 代表了 AI Agent 知识工程的一个重要方向：**从被动检索到主动结构化**。

它的核心价值在于：

- **一个命令** (`/graphify .`) 完成从原始文件到可查询图谱的完整转换
- **零服务器依赖**，完全本地运行（代码和音频完全不离开本地）
- **多模态原生支持**，代码、文档、论文、图片统一处理
- **诚实的不确定性标注**，每条边都知道自己是 EXTRACTED、INFERRED 还是 AMBIGUOUS

在 Claude Code、OpenAI Codex 等 Agent 框架竞争白热化的今天，Graphify 提供了一个被低估但至关重要的能力：**让 Agent 真正理解复杂信息的结构，而不只是匹配文本片段**。

---

## 参考资源

- **GitHub**: [https://github.com/safishamsi/graphify](https://github.com/safishamsi/graphify)
- **PyPI**: [https://pypi.org/project/graphifyy/](https://pypi.org/project/graphifyy/)
- **Claude Code**: [https://claude.ai/code](https://claude.ai/code)
- **SECURITY.md**: [https://github.com/safishamsi/graphify/blob/main/SECURITY.md](https://github.com/safishamsi/graphify/blob/main/SECURITY.md)

_本文基于 Graphify v1.0 版本撰写，截至 2026 年 4 月 9 日，项目已获得 12,477 GitHub Stars。_