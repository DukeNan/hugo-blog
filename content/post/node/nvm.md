---
title: "Node.js 版本管理工具 nvm 完全指南 - 从入门到精通"
date: 2026-01-23T10:17:40+08:00
description: "深入解析 Node.js 版本管理工具 nvm 的安装、配置、使用方法和最佳实践，帮助你轻松管理多版本 Node.js 环境"
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
  - node
---

在 Node.js 开发中，不同项目可能需要不同版本的 Node.js 环境。如何轻松地在多个 Node.js 版本之间切换？**nvm（Node Version Manager）** 是最流行的解决方案之一。它允许你在同一台机器上安装和切换多个 Node.js 版本，为每个项目配置独立的运行环境。本文将系统性地介绍 nvm 的安装、配置、常用命令以及实战技巧。

<!-- more -->

## 简介

### 什么是 nvm

**nvm（Node Version Manager）** 是一个用于管理多个 Node.js 版本的命令行工具。它允许你：

- 在同一台机器上安装多个 Node.js 版本
- 在不同版本之间快速切换
- 为每个项目设置特定的 Node.js 版本
- 方便地升级或降级 Node.js 版本

### 为什么需要 nvm

| 场景 | 问题 | nvm 的作用 |
|------|------|------------|
| **多项目并行开发** | 项目 A 需要 Node 16，项目 B 需要 Node 18 | 快速切换不同版本 |
| **依赖兼容性问题** | 新版 Node.js 与某些包不兼容 | 降级到稳定版本 |
| **测试兼容性** | 需要测试代码在不同 Node 版本下的表现 | 方便地在多个版本间测试 |
| **团队协作** | 团队成员使用不同 Node 版本导致环境差异 | 统一项目指定的 Node 版本 |

### nvm 的版本

nvm 有两个主要版本，针对不同操作系统：

```
nvm
├── nvm（Node Version Manager）
│   ├── 适用于 macOS 和 Linux
│   ├── 使用 bash 脚本
│   └── 功能更完整
│
└── nvm-windows
    ├── 适用于 Windows
    ├── 使用 Go 编写
    └── 命令语法略有不同
```

## 安装 nvm

### macOS / Linux 安装

#### 使用 curl 安装

```bash
# 下载并执行安装脚本
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

#### 使用 wget 安装

```bash
# 下载并执行安装脚本
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

#### 安装后的配置

安装完成后，需要重新加载 shell 配置：

```bash
# 重新加载配置
source ~/.bashrc

# 或使用 zsh
source ~/.zshrc
```

#### 验证安装

```bash
# 检查 nvm 是否安装成功
nvm --version

# 输出示例：0.39.7
```

{{% notice note "注意📢" %}}
如果命令未找到，请确保你的 shell 配置文件（如 `~/.bashrc` 或 `~/.zshrc`）中包含了 nvm 的加载语句。安装脚本通常会自动添加以下内容：

```bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
```
{{% /notice %}}

### Windows 安装

对于 Windows 用户，需要使用 **nvm-windows**（与 Unix 版本的 nvm 不同）。

#### 下载安装包

访问 [nvm-windows Releases](https://github.com/coreybutler/nvm-windows/releases) 页面，下载最新的 `nvm-setup.exe` 安装包。

#### 安装步骤

1. 运行 `nvm-setup.exe`
2. 选择 nvm 的安装路径（默认：`C:\Users\<用户名>\AppData\Roaming\nvm`）
3. 选择 Node.js 的安装路径（默认：`C:\Program Files\nodejs`）
4. 完成安装

#### 验证安装

```cmd
# 在新的命令行窗口中检查
nvm version

# 输出示例：1.1.12
```

### 通过 Homebrew 安装（macOS）

```bash
# 安装 nvm
brew install nvm

# 创建 nvm 目录（如果不存在）
mkdir ~/.nvm

# 添加到 shell 配置（根据你的 shell 选择）

# 对于 zsh（macOS 默认）
echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.zshrc
echo '[ -s "/usr/local/opt/nvm/nvm.sh" ] && . "/usr/local/opt/nvm/nvm.sh"' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc
```

## 基础用法

### 查看 nvm 版本

```bash
nvm --version
```

### 查看已安装的 Node 版本

```bash
# 列出所有已安装的版本
nvm ls

# 输出示例：
#        v14.21.3
# ->     v16.20.2
#        v18.19.0
#        v20.11.1
# default -> v18.19.0
# iojs -> N/A (default)
```

`->` 表示当前激活的版本，`default` 表示默认使用的版本。

### 查看可用的 Node 版本

```bash
# 查看所有可用的远程版本
nvm ls-remote

# 查看特定版本
nvm ls-remote v18
nvm ls-remote v18.19.0

# 查看最新的 LTS 版本
nvm ls-remote --lts
```

{{% notice tip "提示💡" %}}
LTS（Long Term Support）是长期支持版本，更加稳定适合生产环境使用。nvm 在列出远程版本时会标记 LTS 版本，例如 `v20.11.1   (Latest LTS: Iron)`。
{{% /notice %}}

### 安装 Node 版本

```bash
# 安装最新版本
nvm install node

# 安装指定版本
nvm install 18.19.0
nvm install v18.19.0  # 带前缀也可以

# 安装最新的 LTS 版本
nvm install --lts
nvm install --lts=Iron  # 安装特定的 LTS 版本

# 安装多个版本
nvm install 16.20.2
nvm install 18.19.0
nvm install 20.11.1
```

### 切换 Node 版本

```bash
# 切换到已安装的版本
nvm use 18.19.0

# 切换到最新 LTS 版本
nvm use --lts

# 使用主版本号（选择该主版本下的最新安装版本）
nvm use 18
```

### 设置默认版本

```bash
# 设置默认版本（每次打开终端自动使用）
nvm alias default 18.19.0

# 设置为当前版本
nvm alias default node

# 查看默认版本
nvm alias default
```

### 卸载 Node 版本

```bash
# 卸载指定版本
nvm uninstall 16.20.2

# 卸载多个版本
nvm uninstall 14.21.3 16.20.2
```

## 高级用法

### 版本别名

nvm 允许为 Node 版本创建别名，方便管理。

```bash
# 创建别名
nvm alias prod 18.19.0
nvm alias dev 20.11.1

# 使用别名切换
nvm use prod
nvm use dev

# 查看所有别名
nvm alias

# 删除别名
nvm unalias prod
```

### 自动切换版本

通过项目的 `.nvmrc` 文件，nvm 可以自动切换到项目指定的 Node 版本。

#### 创建 .nvmrc 文件

```bash
# 在项目根目录创建 .nvmrc 文件
echo "18.19.0" > .nvmrc
```

#### 自动切换配置

在你的 shell 配置文件（`~/.bashrc` 或 `~/.zshrc`）中添加以下内容：

```bash
# 自动加载 .nvmrc 文件中指定的 Node 版本
autoload -U add-zsh-hook
load-nvmrc() {
  local node_version="$(nvm version)"
  local nvmrc_path="$(nvm_find_nvmrc)"

  if [ -n "$nvmrc_path" ]; then
    local nvmrc_node_version=$(nvm version "$(cat "${nvmrc_path}")")

    if [ "$nvmrc_node_version" = "N/A" ]; then
      nvm install
    elif [ "$nvmrc_node_version" != "$node_version" ]; then
      nvm use
    fi
  elif [ "$node_version" != "$(nvm version default)" ]; then
    echo "Reverting to nvm default version"
    nvm use default
  fi
}

add-zsh-hook chpwd load-nvmrc
load-nvmrc
```

#### 手动切换到 .nvmrc 指定的版本

```bash
# 进入项目目录后手动切换
cd /path/to/project
nvm use

# 找到 .nvmrc 文件并自动切换
# 输出：Found '/path/to/project/.nvmrc' with version <18.19.0>
# 输出：Now using node v18.19.0 (npm v9.2.0)
```

### 同时安装 io.js

nvm 也支持安装和切换 io.js（Node.js 的分支，已合并回 Node.js）：

```bash
# 安装 io.js
nvm install iojs

# 列出 io.js 版本
nvm ls-remote iojs

# 切换到 io.js
nvm use iojs
```

## Windows 版本（nvm-windows）

### nvm-windows 命令差异

nvm-windows 的命令语法与 Unix 版本略有不同：

| 操作 | Unix 版本（nvm） | Windows 版本（nvm-windows） |
|------|------------------|-----------------------------|
| 列出已安装版本 | `nvm ls` | `nvm list` 或 `nvm ls` |
| 列出远程版本 | `nvm ls-remote` | `nvm list available` |
| 安装版本 | `nvm install 18.19.0` | `nvm install 18.19.0` |
| 使用版本 | `nvm use 18.19.0` | `nvm use 18.19.0` |
| 设置默认 | `nvm alias default` | 自动记录最后一次使用的版本 |
| 卸载版本 | `nvm uninstall` | `nvm uninstall` |

### Windows 常用命令

```cmd
# 列出可用的 Node 版本
nvm list available

# 安装指定版本
nvm install 18.19.0

# 切换版本
nvm use 18.19.0

# 查看当前使用的版本
nvm current

# 卸载版本
nvm uninstall 18.19.0
```

## 常见问题排查

### nvm 命令找不到

**问题：** 安装后运行 `nvm` 命令提示 "command not found"

**解决方案：**

1. 确认 nvm 已安装
2. 检查 shell 配置文件是否包含 nvm 加载语句
3. 重新加载 shell 配置或重启终端

```bash
# 检查 nvm 安装目录
ls ~/.nvm

# 手动加载 nvm
source ~/.nvm/nvm.sh
```

### Node 版本切换不生效

**问题：** 运行 `nvm use` 后，`node -v` 仍然显示旧版本

**解决方案：**

1. 检查是否有其他 Node 安装（如通过 Homebrew 或官方安装包）
2. 确保 PATH 中 nvm 的 Node 路径优先

```bash
# 检查 node 的实际路径
which node

# 输出应该是：/Users/username/.nvm/versions/node/v18.19.0/bin/node
# 如果不是，说明使用了其他安装的 Node
```

### npm 的问题

nvm 会为每个 Node 版本安装对应的 npm。

```bash
# 查看当前 npm 版本
npm -v

# 为当前 Node 版本安装特定 npm 版本
npm install -g npm@9.2.0

# 不同 Node 版本可以有不同的 npm 版本
```

### 权限问题

**问题：** 全局安装包时出现权限错误

**解决方案：**

```bash
# 配置 npm 全局安装路径到用户目录
npm config set prefix "$HOME/.npm-global"

# 将路径添加到 PATH
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 卸载 nvm

如果需要完全卸载 nvm：

```bash
# 删除 nvm 目录
rm -rf ~/.nvm

# 从 shell 配置文件中删除 nvm 配置
# 编辑 ~/.bashrc 或 ~/.zshrc，删除 nvm 相关的行
```

## 项目实战

### 场景1：维护多个不同版本的项目

假设你有以下项目：
- 项目 A（生产环境）：使用 Node 16 LTS
- 项目 B（新开发）：使用 Node 18 LTS
- 项目 C（实验性）：使用 Node 20

```bash
# 安装所需版本
nvm install 16.20.2
nvm install 18.19.0
nvm install 20.11.1

# 为每个项目创建 .nvmrc 文件
cd /path/to/project-a
echo "16.20.2" > .nvmrc

cd /path/to/project-b
echo "18.19.0" > .nvmrc

cd /path/to/project-c
echo "20.11.1" > .nvmrc

# 进入项目自动切换
cd /path/to/project-a
nvm use  # 自动切换到 Node 16.20.2
```

### 场景2：团队协作统一 Node 版本

在项目中添加 `.nvmrc` 文件，确保所有开发者使用相同的 Node 版本。

```bash
# .nvmrc 文件内容
18.19.0
```

团队中的其他成员进入项目后，只需要运行：

```bash
# 进入项目目录
cd /path/to/project

# 自动切换版本（如果配置了自动切换）
nvm use

# 或者手动安装指定版本（如果本地未安装）
nvm install
```

可以在 `package.json` 中添加脚本检查 Node 版本：

```json
{
  "scripts": {
    "preinstall": "nvm install || true",
    "start": "node -e \"console.log('Node version:', process.version)\""
  }
}
```

### 场景3：测试代码的跨版本兼容性

使用 nvm 在多个 Node 版本下运行测试：

```bash
# 创建测试脚本 test-all-versions.sh
#!/bin/bash

versions=("16.20.2" "18.19.0" "20.11.1")

for version in "${versions[@]}"; do
  echo "Testing with Node $version"
  nvm use $version
  npm test
  if [ $? -ne 0 ]; then
    echo "Tests failed on Node $version"
    exit 1
  fi
done

echo "All tests passed!"
```

## 最佳实践

### 1. 使用 LTS 版本作为默认

```bash
# 安装最新的 LTS 版本
nvm install --lts

# 设置为默认版本
nvm alias default 'lts/*'
```

### 2. 为每个项目使用 .nvmrc

确保项目的一致性和可移植性：

```bash
# 在项目根目录创建 .nvmrc
echo "$(node -v)" > .nvmrc

# 提交到版本控制
git add .nvmrc
git commit -m "Add .nvmrc for Node version specification"
```

### 3. 定期更新 nvm

```bash
# 更新 nvm 到最新版本
cd ~/.nvm
git fetch origin
git checkout $(git describe --abbrev=0 --tags)
source ~/.nvm/nvm.sh
```

### 4. 保持 Node 版本合理

不要安装过多版本，只保留实际需要的：

```bash
# 查看已安装版本
nvm ls

# 卸载不再使用的版本
nvm uninstall <old-version>
```

### 5. 配置 npm 全局包

为每个 Node 版本单独配置全局包，避免版本冲突：

```bash
# 切换到特定版本
nvm use 18.19.0

# 安装全局包
npm install -g pnpm yarn

# 切换到另一个版本
nvm use 20.11.1

# 重新安装全局包
npm install -g pnpm yarn
```

## 常用命令速查表

| 命令 | 说明 |
|------|------|
| `nvm --version` | 查看 nvm 版本 |
| `nvm ls` | 列出已安装的 Node 版本 |
| `nvm ls-remote` | 列出所有可用的远程版本 |
| `nvm install <version>` | 安装指定版本 |
| `nvm install --lts` | 安装最新的 LTS 版本 |
| `nvm uninstall <version>` | 卸载指定版本 |
| `nvm use <version>` | 切换到指定版本 |
| `nvm alias default <version>` | 设置默认版本 |
| `nvm current` | 显示当前使用的版本 |
| `nvm which <version>` | 显示指定版本的安装路径 |

## 总结

nvm 是 Node.js 开发者必备的工具之一，它简化了多版本管理的复杂性，让开发者能够轻松应对不同项目的需求。

**核心要点：**

1. nvm 允许在同一台机器上安装和管理多个 Node.js 版本
2. 通过 `.nvmrc` 文件可以为项目指定 Node 版本，确保环境一致性
3. LTS 版本更适合生产环境使用
4. Windows 用户需要使用 nvm-windows，命令语法略有差异
5. 定期清理不需要的版本，保持环境整洁

**实践建议：**

- 为每个项目创建 `.nvmrc` 文件
- 使用 LTS 版本作为默认环境
- 定期更新 nvm 到最新版本
- 合理规划 Node 版本，避免安装过多无用版本
- 配置自动切换脚本，提升开发效率

掌握 nvm 的使用，将极大提升 Node.js 开发体验，让你在不同项目间无缝切换，专注于代码本身而不是环境配置。

## 参考资源

- [nvm GitHub 仓库](https://github.com/nvm-sh/nvm)
- [nvm-windows GitHub 仓库](https://github.com/coreybutler/nvm-windows)
- [Node.js 官方网站](https://nodejs.org/)
- [Node.js 版本发布计划](https://github.com/nodejs/Release)
