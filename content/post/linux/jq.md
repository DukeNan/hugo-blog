---
title: "Jq 命令行 JSON 处理神器" # Title of the blog post.
date: 2026-04-03T11:49:29+08:00 # Date of post creation.
description: "深入了解 jq 命令行工具，掌握 JSON 数据的高效处理、过滤和转换技巧" # Description used for search engine.
author: "shaun"
featured: true # Sets if post is a featured post, making appear on the home page side bar.
draft: false # Sets whether to render this page. Draft of true will not be rendered.
toc: false # Controls if a table of contents should be generated for first-level links automatically.
# menu: main
usePageBundles: false # Set to true to group assets like images in the same folder as this post.
codeMaxLines: 10 # Override global value for how many lines within a code block before auto-collapsing.
codeLineNumbers: false # Override global value for showing of line numbers within code block.
figurePositionShow: true # Override global value for showing the figure label.
categories:
  - Technology
tags:
  - Linux
# comment: false # Disable comment if false.
---

jq 是一个轻量级且强大的命令行 JSON 处理器，类似于 sed 用于 JSON 数据。它允许你切片、过滤、映射和转换结构化数据，是处理 API 响应、配置文件和日志分析的必备工具。

## 安装

### macOS
```bash
brew install jq
```

### Linux
```bash
# Debian/Ubuntu
sudo apt-get install jq

# CentOS/RHEL
sudo yum install jq

# Alpine
apk add jq
```

### 验证安装
```bash
jq --version
# jq 1.7
```

## 基本语法

jq 的基本用法：
```bash
jq [options] 'filter' [file]
```

如果没有指定文件，jq 会从标准输入读取。

## 核心概念

### 1. 身份过滤器 (`.`)

最简单的过滤器，输出输入的内容不变：
```bash
echo '{"name": "Alice", "age": 30}' | jq '.'
# {
#   "name": "Alice",
#   "age": 30
# }
```

### 2. 对象属性访问

使用 `.key` 访问对象属性：
```bash
echo '{"name": "Alice", "age": 30}' | jq '.name'
# "Alice"

# 嵌套对象
echo '{"user": {"name": "Alice", "age": 30}}' | jq '.user.name'
# "Alice"
```

### 3. 数组操作

访问数组元素：
```bash
echo '[1, 2, 3, 4, 5]' | jq '.[0]'      # 第一个元素: 1
echo '[1, 2, 3, 4, 5]' | jq '.[-1]'     # 最后一个元素: 5
echo '[1, 2, 3, 4, 5]' | jq '.[2:4]'    # 切片: [3, 4]
echo '[1, 2, 3, 4, 5]' | jq '.[:3]'     # 前三个: [1, 2, 3]
```

### 4. 数组迭代 (`.[]`)

遍历数组元素：
```bash
echo '[{"name": "Alice"}, {"name": "Bob"}]' | jq '.[].name'
# "Alice"
# "Bob"
```

## 常用操作

### 过滤数据

使用 `select()` 条件过滤：
```bash
echo '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]' | \
  jq '.[] | select(.age > 28)'
# {
#   "name": "Alice",
#   "age": 30
# }
```

### 映射和转换

使用 `map` 转换数组：
```bash
echo '[1, 2, 3]' | jq 'map(. * 2)'
# [2, 4, 6]

# 提取字段
echo '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]' | \
  jq 'map(.name)'
# ["Alice", "Bob"]
```

### 创建新对象

使用 `{}` 构建新对象：
```bash
echo '{"firstName": "Alice", "lastName": "Smith"}' | \
  jq '{name: .firstName, full: "\(.firstName) \(.lastName)"}'
# {
#   "name": "Alice",
#   "full": "Alice Smith"
# }
```

### 数组操作

```bash
# 排序
echo '[3, 1, 4, 1, 5, 9]' | jq 'sort'
# [1, 1, 3, 4, 5, 9]

# 反转
echo '[1, 2, 3]' | jq 'reverse'
# [3, 2, 1]

# 去重
echo '[1, 1, 2, 2, 3]' | jq 'unique'
# [1, 2, 3]

# 分组
echo '[{"a": 1}, {"a": 1}, {"a": 2}]' | jq 'group_by(.a)'
# [[{"a": 1}, {"a": 1}], [{"a": 2}]]

# 统计
echo '[1, 2, 2, 3, 3, 3]' | jq 'group_by(.) | map({value: .[0], count: length})'
# [{"value": 1, "count": 1}, {"value": 2, "count": 2}, {"value": 3, "count": 3}]
```

## 高级技巧

### 管道操作符 (`|`)

链式处理数据：
```bash
echo '{"users": [{"name": "Alice", "active": true}, {"name": "Bob", "active": false}]}' | \
  jq '.users | map(select(.active)) | map(.name)'
# ["Alice"]
```

### 条件表达式

使用 `if-then-else`：
```bash
echo '[1, 2, 3, 4, 5]' | jq 'map(if . % 2 == 0 then "even" else "odd" end)'
# ["odd", "even", "odd", "even", "odd"]
```

### 字符串操作

```bash
# 分割字符串
echo '{"path": "/usr/local/bin"}' | jq '.path | split("/")'
# ["", "usr", "local", "bin"]

# 连接字符串
echo '["a", "b", "c"]' | jq 'join("-")'
# "a-b-c"

# 大小写转换
echo '{"name": "Alice"}' | jq '.name | ascii_downcase'
# "alice"
```

### 数学运算

```bash
echo '[1, 2, 3, 4, 5]' | jq 'add'        # 求和: 15
echo '[1, 2, 3, 4, 5]' | jq 'min'        # 最小值: 1
echo '[1, 2, 3, 4, 5]' | jq 'max'        # 最大值: 5
echo '[1, 2, 3, 4, 5]' | jq 'length'     # 长度: 5
echo '[1, 2, 3, 4, 5]' | jq 'unique | length'  # 唯一值数量
```

### 处理 JSON 文件

```bash
# 格式化 JSON
jq '.' data.json

# 压缩 JSON
jq -c '.' data.json

# 提取特定字段
jq '.users[].name' data.json

# 原地编辑（需要 -i 标志，但 jq 不支持，需用临时文件）
tmp=$(mktemp)
jq '.version = "2.0"' config.json > "$tmp" && mv "$tmp" config.json
```

## 实战案例

### 案例 1：处理 API 响应

```bash
# 获取 GitHub 用户信息
curl -s 'https://api.github.com/users/github' | \
  jq '{login, name, public_repos, followers}'

# {
#   "login": "github",
#   "name": "GitHub",
#   "public_repos": 158,
#   "followers": 28456
# }
```

### 案例 2：分析日志文件

```bash
# 统计各状态码出现次数
cat access.log | jq -r '.status' | sort | uniq -c | sort -rn

# 提取慢请求
cat access.log | jq 'select(.duration > 1000) | {path: .request.path, duration}'

# 提取错误日志
cat app.log | jq 'select(.level == "error") | {timestamp, message}'
```

### 案例 3：转换数据格式

```bash
# JSON 转 CSV
echo '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]' | \
  jq -r '(["name", "age"] | @csv), (.[] | [.name, .age] | @csv)'
# "name","age"
# "Alice",30
# "Bob",25

# CSV 转 JSON（需要配合其他工具）
echo 'name,age
Alice,30
Bob,25' | python3 -c "import csv, json, sys; print(json.dumps([dict(r) for r in csv.DictReader(sys.stdin)]))" | jq '.'
# [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]
```

### 案例 4：批量修改配置

```bash
# 更新嵌套配置值
jq '.database.connection.timeout = 30 | .database.connection.pool_size = 10' config.json

# 合并配置
jq -s '.[0] * .[1]' default.json override.json

# 删除字段
jq 'del(.unused_field)' config.json
```

### 案例 5：复杂过滤

```bash
# 多条件过滤
echo '[{"name": "Alice", "age": 30, "active": true},
       {"name": "Bob", "age": 25, "active": false},
       {"name": "Charlie", "age": 35, "active": true}]' | \
  jq '[.[] | select(.active == true and .age >= 30)]'
# [{"name": "Alice", "age": 30, "active": true}, {"name": "Charlie", "age": 35, "active": true}]

# 按条件分组统计
echo '[{"category": "A", "value": 10},
       {"category": "A", "value": 20},
       {"category": "B", "value": 15}]' | \
  jq 'group_by(.category) | map({category: .[0].category, total: map(.value) | add})'
# [{"category": "A", "total": 30}, {"category": "B", "total": 15}]
```

## 常用命令行选项

| 选项 | 说明 |
|------|------|
| `-c` | 紧凑输出（单行） |
| `-r` | 原始字符串输出（不带引号） |
| `-n` | 使用 null 作为输入 |
| `-e` | 如果结果为 false 或 null，退出码为 1 |
| `-f FILE` | 从文件读取过滤器 |
| `-s` | 读取所有输入到一个数组 |
| `--tab` | 使用 tab 缩进 |
| `-S` | 对象键排序输出 |
| `--color-output` | 强制彩色输出 |
| `--monochrome-output` | 禁用彩色输出 |

## 调试技巧

### 使用 `debug` 输出中间结果

```bash
echo '[1, 2, 3]' | jq 'map(. * 2) | debug | map(. + 1)'
# ["DEBUG:",[2,4,6]]
# [3, 5, 7]
```

### 查看类型

```bash
echo '["hello", 123, true, null, {"a": 1}]' | jq '.[] | type'
# "string"
# "number"
# "boolean"
# "null"
# "object"
```

### 错误处理

```bash
# 使用 ? 忽略错误
echo '[1, "two", 3]' | jq '.[] | . * 2?'
# 2
# 6

# 使用 try-catch
echo '[1, "two", 3]' | jq '.[] | if type == "number" then . * 2 else "not a number" end'
# 2
# "not a number"
# 6
```

## 性能优化

```bash
# 使用 --stream 处理大文件
jq --stream 'select(.[0][-1] == "id") | .[1]' large-file.json

# 流式处理（逐行处理 JSON 数组）
cat data.json | jq -c '.[]' | while read -r item; do
  echo "$item" | jq '.name'
done
```

## 快速参考

### 常用过滤器速查

```bash
.              # 输入本身
.key           # 对象属性
.[index]       # 数组索引
.[]            # 数组迭代
|              # 管道
,              # 多个输出
[]             # 数组构造器
{}             # 对象构造器
select(bool)   # 条件过滤
map(f)         # 数组映射
sort           # 排序
unique         # 去重
group_by(f)    # 分组
add            # 求和
length         # 长度
keys           # 获取键名
values         # 获取值
to_entries     # 对象转键值对数组
from_entries   # 键值对数组转对象
```

## 总结

jq 是处理 JSON 数据的瑞士军刀，掌握它可以大幅提升命令行数据处理效率。从简单的字段提取到复杂的数据转换，jq 都能优雅地处理。建议从基础命令开始练习，逐步掌握高级技巧，将其融入日常工作流程中。

## 参考资源

- [jq 官方手册](https://stedolan.github.io/jq/manual/)
- [jq GitHub 仓库](https://github.com/stedolan/jq)
- [jq 在线练习](https://jqplay.org/)
- [jq 速查表](https://lzone.de/cheat-sheet/jq)
