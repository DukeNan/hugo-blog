---
title: "OpenClaw Python：自托管个人 AI 助手网关"
date: 2026-03-10T16:15:00+08:00
description: "OpenClaw Python 是一个自托管的个人 AI 助手网关，连接 20+ 消息渠道与多种 LLM 提供商，支持工具调用、沙箱执行和 ACP 协议，适合个人助手、开发自动化和多渠道客服场景。"
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

**OpenClaw Python 是一个自托管的个人 AI 助手网关**，它连接消息渠道与大型语言模型（LLM），让用户能够通过熟悉的聊天界面（Telegram、飞书、Discord 等）与 AI 助手进行交互。

<!-- more -->

## 简介

OpenClaw Python 是 TypeScript 版本 OpenClaw 的 Python 实现，核心定位是**连接消息渠道与大型语言模型的统一网关**。项目采用 Python 3.11+ 开发，使用 FastAPI + WebSocket + asyncio 作为核心框架。

### 核心特性

| 特性 | OpenClaw | 一般 ChatBot 框架 |
|------|----------|-------------------|
| 架构定位 | 网关 + 运行时分离 | 通常紧耦合 |
| 协议支持 | ACP（AI 通信协议）+ WebSocket | 多为私有协议 |
| 渠道覆盖 | 20+ 消息渠道（含企业级） | 通常 3-5 个 |
| 工具生态 | 文件、Shell、浏览器、子代理、定时任务 | 多为简单函数调用 |
| 沙箱执行 | Docker 隔离 | 通常无 |
| 模型切换 | 运时动态切换 + 故障转移 | 通常静态配置 |

### 能力矩阵

![OpenClaw 能力全景](/images/ai/ai_004.drawio.png)

### 技术栈

- **语言**: Python 3.11+
- **核心框架**: FastAPI + WebSocket + asyncio
- **CLI 框架**: Typer + Rich
- **配置**: Pydantic Settings + JSON5
- **依赖管理**: uv (Astral)

## 架构设计

OpenClaw 采用分层架构设计，实现 UI/渠道层与业务逻辑的完全分离。

![OpenClaw 架构设计](/images/ai/ai_002.drawio.png)

### 核心数据流

![OpenClaw 核心数据流](/images/ai/ai_003.drawio.png)

### 设计原则

1. **分层与解耦**: UI/渠道层与业务逻辑完全分离，同一 Agent 逻辑可同时服务多个渠道
2. **事件驱动架构**: 所有组件通过事件流通信，天然支持流式输出
3. **依赖注入与自动装配**: 工具通过依赖注入获取运行时上下文
4. **运行时抽象**: `PiAgentRuntime` 封装底层复杂性，提供统一的 `run_turn()` 接口

## 安装与配置

### 安装

使用 uv 进行依赖管理：

```bash
# 克隆仓库
git clone https://github.com/openxjarvis/openclaw-python.git
cd openclaw-python

# 安装依赖
uv sync
```

### 配置文件

配置文件位于 `~/.openclaw/openclaw.json`，支持 JSON5 格式（注释 + 尾随逗号）：

```json5
// ~/.openclaw/openclaw.json
{
  // 网关配置
  "gateway": {
    "mode": "local",
    "port": 18789,
    "bind": "127.0.0.1"
  },

  // LLM 配置
  "llm": {
    "provider": "gemini",
    "model": "google/gemini-2.0-flash",
    "apiKey": "${GEMINI_API_KEY}",
    "fallbackModels": ["google/gemini-1.5-pro"]
  },

  // 渠道配置
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "${TELEGRAM_BOT_TOKEN}",
      "dmPolicy": "pairing"  // pairing | allowlist | open | disabled
    },
    "feishu": {
      "enabled": true,
      "appId": "${FEISHU_APP_ID}",
      "appSecret": "${FEISHU_APP_SECRET}",
      "useWebSocket": true
    }
  },

  // 工具安全策略
  "tools": {
    "exec": {
      "security": "allowlist",  // deny | allowlist | full
      "safe_bins": ["python", "git", "node"],
      "ask": "on-miss"  // never | on-miss | always
    }
  }
}
```

### 配置特性

**$include 指令**：支持配置文件拆分和模块化：

```json
{
  "channels": {"$include": "./channels.json"},
  "llm": {"$include": ["./gemini.json", "./fallback.json"]}
}
```

**环境变量替换**：使用 `${ENV_VAR}` 语法引用环境变量。

### 启动服务

```bash
# 启动 OpenClaw 服务
uv run openclaw start

# 指定端口
uv run openclaw start --port 18789
```

## 核心子系统

### Gateway 网关层

Gateway 是 OpenClaw 的**中央协调器**，负责：

- 配置加载与验证（24 步初始化序列）
- 渠道生命周期管理（启动/停止/健康检查）
- 会话管理（创建/恢复/持久化）
- 工具注册与策略执行
- 定时任务调度（Cron）
- 技能热加载

### Agent 执行引擎

OpenClaw 使用 `PiAgentRuntime` 作为 Agent 运行时，基于 pi-mono-python 实现：

```python
# openclaw/gateway/pi_runtime.py
class PiAgentRuntime:
    """
    Gateway 级运行时，基于 pi_coding_agent.AgentSession

    维护 AgentSession 实例池，每个 session_id 对应一个实例
    提供兼容的 run_turn() 异步生成器接口
    """

    def __init__(
        self,
        model: str = "google/gemini-2.0-flash",
        fallback_models: list[str] | None = None,
        cwd: str | Path | None = None,
        system_prompt: str | None = None,
    ):
        self.model_candidates: list[str] = [model] + list(fallback_models or [])
        # 会话池: session_id → AgentSession
        self._pool: dict[str, Any] = {}
```

### 工具系统

工具分为以下类别：

| 类别 | 工具 | 功能描述 |
|------|------|----------|
| **文件系统** | `read` / `write` / `edit` / `apply_patch` | 文件读写、编辑、应用补丁 |
| **执行环境** | `exec` (bash) / `process` | Shell 命令执行、进程管理 |
| **Web** | `web_search` / `web_fetch` | 网页搜索、内容抓取 |
| **浏览器** | `browser` | CDP 浏览器控制 |
| **子代理** | `subagents` / `sessions_spawn` | 子 Agent 创建与管理 |
| **定时任务** | `cron` | Cron 表达式调度 |
| **记忆** | `memory_search` / `memory_get` | 向量记忆检索 |
| **媒体** | `image` / `tts` | 图像生成、语音合成 |

### ACP 协议层

**ACP (AI Communication Protocol)** 是 OpenClaw 定义的 IDE 与 Agent 之间的通信协议，类比于 LSP 对于编程语言的意义。

核心特性：

- **传输**: NDJSON over stdin/stdout 或 WebSocket
- **消息格式**: JSON-RPC 2.0 风格
- **会话管理**: 支持多会话、会话恢复
- **流式输出**: 支持增量消息更新

## 安全与权限模型

OpenClaw 采用**四层独立权限模型**：

![OpenClaw 四层权限模型](/images/ai/ai_005.drawio.png)

### Docker 沙箱

```python
async def create_sandbox_container(
    name: str,
    workspace_dir: Path,
    image: str = DEFAULT_SANDBOX_IMAGE,
) -> dict[str, Any]:
    """
    创建隔离的 Docker 容器用于代码执行

    安全特性：
    - 只读挂载工作空间
    - 网络隔离（可选）
    - 资源限制（CPU/内存）
    - 非 root 用户运行
    """
```

## 适用场景

### 个人 AI 助手

通过 Telegram/飞书与 AI 交互，实现日常任务自动化。

```bash
uv run openclaw start
```

### 开发工作流自动化

代码审查、文件操作、Shell 执行，使用 `read` / `write` / `edit` / `exec` 工具。

### 多渠道客服系统

统一回复 Telegram、Discord、Slack 消息，支持多账户配置。

### 定时任务调度

自动报告生成、数据同步，使用 `cron` + `subagents` 工具。

### IDE 集成

通过 ACP 协议集成到 Zed、VS Code，实现流式代码补全和辅助。

### 安全代码执行

使用 Docker 沙箱执行不可信代码，配置 `sandbox.enabled = true`。

## 总结

OpenClaw Python 是一个**工程化程度很高的个人 AI 助手网关**，它在以下方面表现出色：

- **架构清晰**: 分层设计让渠道、协议、引擎、工具各司其职
- **协议先行**: ACP 协议的设计让 IDE 集成成为可能
- **安全周全**: 四层权限 + Docker 沙箱的组合拳
- **生态兼容**: 与 TypeScript 版本共享协议和配置格式

项目代表了**个人 AI 基础设施**的发展趋势：不是简单的 ChatBot 封装，而是一个完整的、可扩展的、安全的 AI 运行时环境。

## 参考资源

- [OpenClaw Python 主仓库](https://github.com/openxjarvis/openclaw-python)
- [pi-mono-python 依赖仓库](https://github.com/openxjarvis/pi-mono-python)
- [原版 TypeScript 实现](https://github.com/badlogic/pi-mono)