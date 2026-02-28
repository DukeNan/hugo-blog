---
title: "Zoxide - 更智能的目录跳转工具"
date: 2026-02-28T10:36:57+08:00
description: "Zoxide 是一个更智能的 cd 命令替代工具，能够记住你常用的目录，让你用更少的按键快速跳转。"
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
  - Linux
---

**Zoxide 是一个更智能的 cd 命令，它会记住你最常使用的目录，让你能够用更少的按键快速跳转。**

## 简介

Zoxide 是 `autojump` 和 `z` 等 tools 的现代替代品，使用 Rust 编写。它采用 **frecency**（frequency + recency）算法，综合访问频率和最近访问时间来排序目录，让常用目录更容易被找到。

### 主要特点

- **跨 Shell 支持**：支持 Bash、Zsh、Fish、PowerShell 等主流 Shell
- **智能排序**：基于访问频率和时间智能排序搜索结果
- **快速模糊匹配**：只需输入目录名的部分字符即可跳转
- **交互式搜索**：支持与 fzf 集成进行交互式目录选择
- **轻量高效**：Rust 编写，响应速度快

## 安装

### macOS

```bash
# Homebrew（推荐）
brew install zoxide

# MacPorts
port install zoxide

# Cargo
cargo install zoxide --locked
```

### Linux

```bash
# Debian/Ubuntu
apt install zoxide

# Arch Linux/Manjaro
pacman -S zoxide

# Fedora
dnf install zoxide

# Nix
nix-env -iA nixpkgs.zoxide
```

### 其他方式

```bash
# asdf
asdf plugin add zoxide https://github.com/nyrst/asdf-zoxide.git
asdf install zoxide latest

# Conda
conda install -c conda-forge zoxide
```

## Shell 集成

安装后需要在 Shell 配置文件中添加初始化命令。

### Bash

编辑 `~/.bashrc`：

```bash
eval "$(zoxide init bash)"
```

### Zsh

编辑 `~/.zshrc`：

```bash
eval "$(zoxide init zsh)"
```

### Fish

编辑 `~/.config/fish/config.fish`：

```fish
zoxide init fish | source
```

### Nushell

编辑 `$env.NU_LIB_DIRS` 中的配置文件：

```nu
zoxide init nushell | save -f ~/.zoxide.nu
```

然后在配置中添加：

```nu
source ~/.zoxide.nu
```

### POSIX Shell

适用于 dash、sh 等：

```sh
eval "$(zoxide init posix --hook prompt)"
```

### 初始化选项

```bash
# 使用 z 命令替代 cd（推荐）
eval "$(zoxide init bash --cmd z)"

# 同时保留 z 和 zi 命令
eval "$(zoxide init bash --cmd z)"

# 自定义命令名称
eval "$(zoxide init bash --cmd cd)"  # 替换原 cd
```

## 基本使用

### 添加目录到数据库

```bash
# 访问目录时自动添加（需要 Shell 集成）
cd /path/to/project

# 手动添加目录
zoxide add /path/to/project

# 添加多个目录
zoxide add ~/projects ~/work ~/documents
```

### 跳转目录

```bash
# 基本跳转（使用完整或部分路径）
z project        # 跳转到包含 "project" 的目录
z proj           # 模糊匹配也有效
z /usr/lo        # 跳转到 /usr/local

# 跳转到子目录
z project src    # 跳转到 project 下的 src 目录

# 跳转到家目录
z

# 返回上一个目录
z -

# 使用绝对路径
z /etc/nginx
```

### 交互式搜索

使用 `zi` 命令配合 fzf 进行交互式选择：

```bash
# 安装 fzf
brew install fzf        # macOS
apt install fzf         # Debian/Ubuntu

# 交互式搜索
zi

# 带过滤条件的交互式搜索
zi project
```

### 管理数据库

```bash
# 查看数据库中的目录
zoxide query -l

# 查看带分数的目录列表
zoxide query -l -s

# 搜索目录
zoxide query project

# 移除目录
zoxide remove /path/to/project

# 编辑数据库（打开数据库文件编辑）
zoxide edit
```

## 命令详解

### `zoxide add`

添加目录到数据库或增加其排名。

```bash
zoxide add /path/to/dir     # 添加指定目录
zoxide add .                # 添加当前目录
zoxide add ~/projects       # 支持路径展开
```

### `zoxide query`

搜索数据库中的目录。

```bash
zoxide query foo            # 搜索包含 foo 的目录
zoxide query -l             # 列出所有目录
zoxide query -l -s          # 列出所有目录及分数
zoxide query --exclude ~ foo # 排除特定目录
zoxide query -i foo         # 交互式搜索（需要 fzf）
```

### `zoxide remove`

从数据库中移除目录。

```bash
zoxide remove /path/to/dir  # 移除指定目录
zoxide remove foo           # 移除匹配的目录
```

### `zoxide edit`

直接编辑数据库文件，可用于批量管理。

```bash
zoxide edit                 # 使用 $EDITOR 打开数据库
```

### `zoxide init`

生成 Shell 初始化脚本。

```bash
zoxide init bash            # 生成 Bash 初始化脚本
zoxide init zsh --cmd j     # 使用 j 作为命令名
zoxide init fish            # 生成 Fish 初始化脚本
```

### `zoxide import`

从其他工具导入数据。

```bash
# 从 autojump 导入
zoxide import --from autojump

# 从 z 导入
zoxide import --from z
```

## 环境变量配置

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `_ZO_DATA_DIR` | 数据文件存储路径 | `~/.local/share/zoxide` (Linux) / `~/.local/share/zoxide` (macOS) |
| `_ZO_ECHO` | 设为 `1` 时，跳转前打印目标目录 | 未设置 |
| `_ZO_EXCLUDE_DIRS` | 排除的目录列表（glob 格式） | 未设置 |
| `_ZO_FZF_OPTS` | 传递给 fzf 的自定义选项 | 未设置 |
| `_ZO_MAXAGE` | 目录的最大存活时间（秒） | 9000 |
| `_ZO_RESOLVE_SYMLINKS` | 设为 `1` 时，存储时解析符号链接 | 未设置 |

### 配置示例

```bash
# ~/.bashrc 或 ~/.zshrc

# 设置数据目录
export _ZO_DATA_DIR="$HOME/.zoxide"

# 跳转前显示目标目录
export _ZO_ECHO=1

# 排除特定目录
export _ZO_EXCLUDE_DIRS="$HOME/.cache:$HOME/.config:$HOME/tmp"

# 配置 fzf 选项
export _ZO_FZF_OPTS="--height 40% --reverse --border"

# 设置最大存活时间（10天）
export _ZO_MAXAGE=864000
```

## 高级用法

### 排除目录

避免将临时目录或缓存目录加入数据库：

```bash
# 在 Shell 配置中添加
export _ZO_EXCLUDE_DIRS="$HOME/.cache:$HOME/tmp:$HOME/Downloads"
```

### 配合 fzf 自定义搜索

```bash
# 使用预览功能
export _ZO_FZF_OPTS="
  --height 80%
  --layout=reverse
  --preview='ls -la {}'
  --preview-window=right:50%:wrap
"
```

### 从其他工具迁移

```bash
# 从 autojump 迁移
zoxide import --from autojump

# 从 z 迁移
zoxide import --from z

# 从 z.lua 迁移
zoxide import --from zlua
```

### 在脚本中使用

```bash
#!/bin/bash
# 获取目录路径而不跳转
dir=$(zoxide query project)
echo "Project directory: $dir"

# 切换目录
cd "$(zoxide query project)"
```

### 与 tmux 配合

```bash
# 在 tmux 新窗口中打开目录
tmux new-window -c "$(zoxide query project)"
```

## 工作原理

Zoxide 使用 **frecency** 算法（frequency + recency）：

1. **频率（Frequency）**：访问次数越多，分数越高
2. **最近访问（Recency）**：最近访问的目录获得更高权重

分数计算公式使常用目录保持在列表顶部，而长时间未访问的目录会逐渐降低排名。

## 常见问题

### zoxide 和 autojump 有什么区别？

| 特性 | zoxide | autojump |
|------|--------|----------|
| 语言 | Rust | Python |
| 速度 | 更快 | 较慢 |
| 依赖 | 无 | Python |
| 数据库格式 | 二进制 | JSON |
| 交互式搜索 | 原生支持 | 需要额外配置 |

### 如何重置数据库？

```bash
rm -rf ~/.local/share/zoxide
# 或使用配置的数据目录
rm -rf "$_ZO_DATA_DIR"
```

### 如何查看当前数据库内容？

```bash
zoxide query -l -s
```

## 参考资源

- [GitHub 仓库](https://github.com/ajeetdsouza/zoxide)
- [官方文档](https://github.com/ajeetdsouza/zoxide#readme)
