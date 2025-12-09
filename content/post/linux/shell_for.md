---
title: "Shell 数组与 for 循环最佳实践" # Title of the blog post.
date: 2025-12-09T15:15:33+08:00 # Date of post creation.
description: "Shell 数组与 for 循环最佳实践" # Description used for search engine.
author: "shaun"
featured: true # Sets if post is a featured post, making appear on the home page side bar.
draft: false # Sets whether to render this page. Draft of true will not be rendered.
toc: false # Controls if a table of contents should be generated for first-level links automatically.
# menu: main
usePageBundles: false # Set to true to group assets like images in the same folder as this post.
# featureImage: "/images/path/file.jpg" # Sets featured image on blog post.
# featureImageAlt: 'Description of image' # Alternative text for featured image.
# featureImageCap: 'This is the featured image.' # Caption (optional).
# thumbnail: "/images/path/thumbnail.png" # Sets thumbnail image appearing inside card on homepage.
# shareImage: "/images/path/share.png" # Designate a separate image for social media sharing.
codeMaxLines: 10 # Override global value for how many lines within a code block before auto-collapsing.
codeLineNumbers: false # Override global value for showing of line numbers within code block.
figurePositionShow: true # Override global value for showing the figure label.
categories:
  - Technology
tags:
  - linux
# comment: false # Disable comment if false.
---
Shell 数组和 for 循环的最佳实践在于确保代码的健壮性 (Robustness)，尤其是在处理包含空格或特殊字符的数组元素时。

<!--more-->

## 🧩 一、定义数组的标准写法

```
# ✅ 正确：使用括号 + 双引号，保证空格安全
dirs=(
  "/opt/app/logs"
  "/opt/app data"
  "/tmp/test"
)
```

> ❌ 错误写法：
>
> ```
> dirs=/opt/app/logs /opt/app data /tmp/test
> ```
>
> 这会被当成多个命令执行。

------

## 🔁 二、安全遍历数组

### ✅ 推荐写法

```
for dir in "${dirs[@]}"; do
  echo "Processing directory: $dir"
done
```

- **`${dirs[@]}`**：展开数组中每个元素为独立参数（保留空格）。
- **双引号 `"${dirs[@]}"`**：防止被空格拆分。
- 永远加双引号 —— 这是 Bash 的黄金定律。

------

## 🧠 三、普通 for 遍历（非数组）

```
for file in *.log; do
  echo "Found file: $file"
done
```

✅ 特点：

- 可用于通配符匹配（`*.log`）

- 直接处理命令输出：

  ```
  for line in $(cat /etc/hosts); do
      echo "Host: $line"
  done
  ```

🚫 缺点：

- 空格会被拆开，`"foo bar"` → `"foo"` + `"bar"`
- 不适合结构化或复杂数据

------

## ⚙️ 四、带索引的数组遍历

```
for i in "${!dirs[@]}"; do
  echo "Index: $i → Dir: ${dirs[$i]}"
done
```

- **`${!dirs[@]}`** 表示数组的所有索引。
- 适合需要根据位置做映射或判断的场景。

------

## 🚫 五、常见陷阱与错误示例

| 错误代码             | 问题               | 修正方法               |
| -------------------- | ------------------ | ---------------------- |
| `for x in ${arr[@]}` | 被空格拆开         | `for x in "${arr[@]}"` |
| `for x in $(ls)`     | 文件名带空格时出错 | `for x in *; do`       |
| 忘记 `IFS` 处理输入  | 分隔符错误         | 临时修改 `IFS=$'\n'`   |

------

## 🔒 六、安全处理命令输出（带空格）

有些命令输出路径中带空格，例如：

```
find /data -type d
```

使用 **mapfile / readarray** 最安全：

```
mapfile -t dirs < <(find /data -type d)

for dir in "${dirs[@]}"; do
  echo "Found dir: $dir"
done
```

> ✅ `mapfile -t` 自动按行读取输出，不会被空格拆开。

------

## 🧹 七、IFS（Internal Field Separator）

默认 `IFS` 是空格、Tab、换行。
 如果要按“行”遍历输出，可以这样：

```
IFS=$'\n' read -r -d '' -a lines < <(ls -1)
for line in "${lines[@]}"; do
  echo "Line: $line"
done
```

------

## 🧰 八、综合实战模板（含数组 + 动态命令）

```
#!/bin/bash
set -euo pipefail

# 定义要保留的文件夹天数
keep_days=3

# 找出三天前的目录名
mapfile -t old_dirs < <(find . -maxdepth 1 -type d -name "20*" -mtime +$keep_days)

echo "🧹 Found ${#old_dirs[@]} old directories to delete"

for dir in "${old_dirs[@]}"; do
  echo "Deleting: $dir"
  rm -rf "$dir"
done
```

✅ 特点：

- 使用 `mapfile` 保证安全读取
- 数组循环可防止空格拆分
- 自动跳过当前目录 `.`
- 脚本健壮、可直接上线
