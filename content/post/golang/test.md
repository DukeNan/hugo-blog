---
title: "Go 语言测试（go test）使用说明" # Title of the blog post.
date: 2025-12-16T14:28:46+08:00 # Date of post creation.
description: "go test" # Description used for search engine.
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
  - Golang
# comment: false # Disable comment if false.
---

Go 语言内置了强大的测试框架，通过 go test 命令可以方便地进行单元测试、基准测试和示例测试。

<!-- more -->

## 基本概念

- 测试文件以 `_test.go` 结尾
- 测试函数以 `Test` 开头，参数为 `*testing.T`
- 基准测试函数以 `Benchmark` 开头，参数为 `*testing.B`
- 示例函数以 `Example` 开头，无参数

## 常用命令


```bash
go test                    # 运行当前目录下的所有测试
go test -v                 # 显示详细输出
go test -run TestName      # 运行指定的测试函数
go test ./...              # 递归测试所有子目录
go test -cover             # 显示测试覆盖率
go test -bench .           # 运行基准测试
go test -timeout 30s       # 设置测试超时时间
```

## 完整示例

下面提供一个包含单元测试、表格驱动测试、基准测试和示例测试的完整案例：

{{< code lang="go" file="assets/code/golang/test/calculator.go" >}}
{{< code lang="go" file="assets/code/golang/test/calculator_test.go" >}}


## 运行测试的命令示例
```bash
# 基本测试
go test

# 详细输出
go test -v

# 运行特定测试
go test -run TestAdd
go test -run TestIsPrime

# 运行包含特定名称的测试
go test -run Prime

# 测试覆盖率
go test -cover
go test -coverprofile=coverage.out
go tool cover -html=coverage.out  # 生成HTML覆盖率报告

# 运行基准测试
go test -bench .
go test -bench BenchmarkAdd
go test -benchmem  # 显示内存分配统计

# 并行测试
go test -parallel 4

# 设置超时
go test -timeout 10s
```

## 测试最佳实践

1. **使用表格驱动测试**：可以用更少的代码测试更多场景
2. **使用子测试**：通过 `t.Run()` 组织相关测试
3. **测试错误情况**：不仅测试正常流程，也要测试异常情况
4. **使用有意义的测试名称**：便于识别失败的测试
5. **避免测试间依赖**：每个测试应该独立运行
6. **使用 `t.Helper()`**：标记辅助函数，使错误报告更准确
7. **合理使用 Mock**：对于复杂依赖，使用接口和 Mock 简化测试

这些示例涵盖了 Go 测试的主要用法，可以根据实际需求进行调整和扩展。
