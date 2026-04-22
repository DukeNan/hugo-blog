---
title: "Fzf: 命令行模糊查找神器" # Title of the blog post.
date: 2026-04-22T10:26:34+08:00 # Date of post creation.
description: "fzf 是一个通用的命令行模糊查找工具，支持文件、命令历史、进程等的快速搜索。本文介绍 fzf 的安装配置和实用技巧。" # Description used for search engine.
author: "shaun"
featured: false # Sets if post is a featured post, making appear on the home page side bar.
draft: false # Sets whether to render this page. Draft of true will not be rendered.
toc: false # Controls if a table of contents should be generated for first-level links automatically.
# menu: main
codeMaxLines: 10 # Override global value for how many lines within a code block before auto-collapsing.
codeLineNumbers: false # Override global value for showing of line numbers within code block.
figurePositionShow: true # Override global value for showing the figure label.
categories:
  - Technology
tags:
  - Linux
# comment: false # Disable comment if false.
---

[fzf](https://github.com/junegunn/fzf) 是一个用 Go 语言编写的通用命令行模糊查找工具。它可以与 Bash、Zsh、Fish 等多种 Shell 配合使用，极大地提升命令行操作效率。

## 安装

### macOS

```bash
# 使用 Homebrew
brew install fzf

# 安装 Shell 集成（启用快捷键绑定和自动补全）
$(brew --prefix)/opt/fzf/install
```

### Linux

```bash
# Ubuntu/Debian
sudo apt install fzf

# Arch Linux
sudo pacman -S fzf

# 从源码安装
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
```

安装完成后，执行 `source ~/.bashrc` 或 `source ~/.zshrc` 使配置生效。

## 基本用法

### 直接运行

在终端输入 `fzf` 即可启动模糊查找：

```bash
fzf
```

这会列出当前目录下的所有文件，输入关键字进行模糊匹配。按 Enter 键选择，选中的内容会输出到标准输出。

### 与其他命令结合

```bash
# 用 vim 打开查找到的文件
vim $(fzf)

# 用 cd 切换到选中的目录
cd $(find . -type d | fzf)
```

### 预览文件内容

使用 `--preview` 参数可以在右侧面板预览文件内容：

```bash
fzf --preview 'cat {}'
```

更好的预览效果可以使用 `bat` 或 `highlight`：

```bash
fzf --preview 'bat --style=numbers --color=always {} | head -500'
```

## 快捷键绑定

安装脚本会自动配置以下快捷键：

| 快捷键 | 功能 |
|--------|------|
| `Ctrl-T` | 查找文件并粘贴到命令行 |
| `Ctrl-R` | 搜索命令历史 |
| `Alt-C` | 递归切换目录 |

### Ctrl-T：查找文件

按下 `Ctrl-T` 后，fzf 会列出当前目录及子目录下的文件，选择后会粘贴到命令行：

```bash
# 按 Ctrl-T 后选择文件，结果类似：
vim /path/to/selected/file.txt
```

### Ctrl-R：搜索历史命令

按下 `Ctrl-R` 后，可以模糊搜索命令历史：

```bash
# 搜索之前执行过的 docker 命令
# 按 Ctrl-R，输入 docker，选择历史命令
```

### Alt-C：快速切换目录

按下 `Alt-C` 后，列出子目录，选择后直接 `cd` 进入。

## 高级技巧

### 自定义查找命令

使用 `FZF_DEFAULT_COMMAND` 环境变量自定义查找命令：

```bash
# 在 ~/.bashrc 或 ~/.zshrc 中添加
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_ALT_C_COMMAND='fd --type d --hidden --follow --exclude .git'
```

这里使用 [fd](https://github.com/sharkdp/fd) 替代 `find`，速度更快且更智能。

### 自定义默认选项

```bash
export FZF_DEFAULT_OPTS='
  --height 80%
  --layout=reverse
  --border
  --preview-window=right:60%
  --color=fg:#f8f8f2,bg:#282a36,hl:#bd93f9
  --color=fg+:#f8f8f2,bg+:#44475a,hl+:#bd93f9
  --color=info:#ffb86c,prompt:#50fa7b,pointer:#ff79c6
  --color=marker:#ff79c6,spinner:#ffb86c,header:#6272a4
'
```

### 进程管理

结合 `ps` 查找并杀死进程：

```bash
# 创建别名
alias fkill='ps -ef | fzf --header="Select process to kill" --multi | awk "{print \$2}" | xargs kill'
```

### Git 集成

```bash
# 查找并切换 Git 分支
alias gco='git branch | fzf | xargs git checkout'

# 查找并查看 Git 日志
alias glog='git log --oneline | fzf --multi | cut -d" " -f1 | xargs git show'
```

### 搜索文件内容

使用 `grep` 或 `ripgrep` 搜索文件内容：

```bash
# 使用 ripgrep 搜索内容
rg --line-number "" | fzf --delimiter=: --nth=2.. | cut -d: -f1 | xargs vim
```

## 多选模式

使用 `--multi` 或按 `Tab` 键选择多个项目：

```bash
# 选择多个文件删除
rm $(fzf --multi)
```

- `Tab` / `Shift-Tab`：选择/取消选择
- `Ctrl-A`：选择所有

## 与 tmux 集成

fzf 提供了 tmux 集成，可以在弹出窗口中运行：

```bash
# 在 tmux 弹出窗口中运行 fzf
fzf-tmux -p 80%
```

## 实用别名配置

将以下配置添加到 `~/.bashrc` 或 `~/.zshrc`：

```bash
# 快速查找文件并用 vim 打开
alias vf='vim $(fzf)'

# 快速 cd 到子目录
alias cf='cd $(find . -type d | fzf)'

# 快速查看 git diff
alias gdf='git diff $(git branch | fzf)'

# 快速切换 git 分支
alias gcf='git checkout $(git branch | fzf)'
```

## 总结

fzf 是提升命令行效率的利器，主要优势：

1. **模糊匹配**：不需要精确输入，智能匹配候选
2. **快速响应**：异步处理，毫秒级响应
3. **高度可定制**：支持主题、预览、快捷键等配置
4. **广泛集成**：与 Shell、Git、tmux 等无缝配合

建议结合 [fd](https://github.com/sharkdp/fd)、[ripgrep](https://github.com/BurntSushi/ripgrep)、[bat](https://github.com/sharkdp/bat) 等现代命令行工具一起使用，获得更好的体验。
