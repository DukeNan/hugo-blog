---
title: "Delve (dlv) - Go 调试工具完整指南" # Title of the blog post.
date: 2025-12-16T11:36:51+08:00 # Date of post creation.
description: "Golang中Delve调试器" # Description used for search engine.
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

Delve是Go语言专用调试工具，支持断点、单步执行和变量查看。通过go install安装后可用dlv debug调试程序，dlv test调试测试，支持命令行与VS Code等IDE集成，提升开发效率。

<!--more-->

在Go语言开发中，调试是排查问题的重要环节。Delve（dlv）是专为Go设计的调试器，功能强大且使用方便。它支持断点、变量查看、单步执行等常见调试操作，特别适合在命令行或IDE中集成使用。


### 安装 Delve

```bash
# 方法1: 使用 go install (推荐)
go install github.com/go-delve/delve/cmd/dlv@latest

# 方法2: 从源码安装
git clone https://github.com/go-delve/delve.git
cd delve
go install github.com/go-delve/delve/cmd/dlv
#
# 验证安装
dlv version
```

### 实战案例：调试一个 Web API 服务
我们将创建一个有 bug 的 Web 服务，然后使用 dlv 来调试它。

#### 项目结构

```bash
debug-demo/
├── main.go
├── handlers/
│   └── user.go
├── models/
│   └── user.go
└── utils/
    └── calculator.go
```

#### 示例代码

#### main.go

```go
package main

import (
    "fmt"
    "log"
    "net/http"

    "debug-demo/handlers"
)

func main() {
    fmt.Println("Starting server on :8080...")

    http.HandleFunc("/api/users", handlers.GetUsers)
    http.HandleFunc("/api/user/", handlers.GetUserByID)
    http.HandleFunc("/api/calculate", handlers.Calculate)

    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

#### handlers/user.go

```go
package handlers

import (
    "encoding/json"
    "fmt"
    "net/http"
    "strconv"
    "strings"

    "debug-demo/models"
    "debug-demo/utils"
)

var users = []models.User{
    {ID: 1, Name: "Alice", Age: 25, Email: "alice@example.com"},
    {ID: 2, Name: "Bob", Age: 30, Email: "bob@example.com"},
    {ID: 3, Name: "Charlie", Age: 35, Email: "charlie@example.com"},
}

// GetUsers 获取所有用户 (有意留下 bug)
func GetUsers(w http.ResponseWriter, r *http.Request) {
    fmt.Println("GetUsers called")

    // Bug: 这里会导致空指针
    var result []models.User
    for i := 0; i < len(users)+1; i++ { // 故意越界
        if i < len(users) {
            result = append(result, users[i])
        }
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(result)
}

// GetUserByID 根据ID获取用户 (有意留下 bug)
func GetUserByID(w http.ResponseWriter, r *http.Request) {
    fmt.Println("GetUserByID called:", r.URL.Path)

    // 提取 ID
    path := strings.TrimPrefix(r.URL.Path, "/api/user/")
    id, err := strconv.Atoi(path)
    if err != nil {
        http.Error(w, "Invalid user ID", http.StatusBadRequest)
        return
    }

    // Bug: 没有检查数组越界
    user := users[id-1] // 如果 id=0 或 id>len(users) 会 panic

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(user)
}

// Calculate 计算接口
func Calculate(w http.ResponseWriter, r *http.Request) {
    fmt.Println("Calculate called")

    aStr := r.URL.Query().Get("a")
    bStr := r.URL.Query().Get("b")

    a, _ := strconv.Atoi(aStr)
    b, _ := strconv.Atoi(bStr)

    // Bug: 除法可能除以0
    result := utils.Divide(a, b)

    response := map[string]interface{}{
        "a":      a,
        "b":      b,
        "result": result,
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}
```

#### models/user.go

```go
package models

type User struct {
    ID    int    `json:"id"`
    Name  string `json:"name"`
    Age   int    `json:"age"`
    Email string `json:"email"`
}

// ValidateAge 验证年龄 (有意留下 bug)
func (u *User) ValidateAge() bool {
    // Bug: 逻辑错误
    return u.Age > 0 && u.Age < 18 // 应该是 < 150
}
```

#### utils/calculator.go

```go
package utils

import "fmt"

// Divide 除法 (有意留下 bug)
func Divide(a, b int) float64 {
    fmt.Printf("Dividing %d by %d\\\\n", a, b)

    // Bug: 没有检查除以0
    return float64(a) / float64(b)
}

// Add 加法
func Add(a, b int) int {
    result := a + b
    fmt.Printf("Adding %d + %d = %d\\\\n", a, b, result)
    return result
}

// Multiply 乘法 (有意留下 bug)
func Multiply(a, b int) int {
    result := 0
    for i := 0; i < b; i++ {
        result = Add(result, a)
    }
    return result
}
```
### Delve 调试实战

#### 1. 基本启动和运行

```bash
# 编译并启动调试
dlv debug main.go

# 或者先编译，再调试二进制文件
go build -o myapp main.go
dlv exec ./myapp

# 调试测试
dlv test

# 附加到正在运行的进程
dlv attach <pid>
```

#### 2. 常用 dlv 命令

进入 dlv 后的命令：

```bash
# === 断点相关 ===
break (b)                    # 设置断点
  b main.main                # 在 main 函数设置断点
  b handlers/user.go:25      # 在文件第25行设置断点
  b handlers.GetUserByID     # 在函数设置断点

breakpoints (bp)             # 查看所有断点
clear <id>                   # 删除断点
clearall                     # 删除所有断点

# === 执行控制 ===
continue (c)                 # 继续执行到下一个断点
next (n)                     # 单步执行（不进入函数）
step (s)                     # 单步执行（进入函数）
stepout (so)                 # 跳出当前函数
restart (r)                  # 重启程序

# === 变量查看 ===
print (p) <var>              # 打印变量值
  p users                    # 打印 users 变量
  p users[0]                 # 打印数组元素
  p user.Name                # 打印结构体字段

locals                       # 显示所有局部变量
args                         # 显示函数参数
vars                         # 显示包级变量
whatis <var>                 # 显示变量类型

# === 调用栈 ===
goroutines (grs)             # 显示所有 goroutine
goroutine (gr) <id>          # 切换到指定 goroutine
stack (bt)                   # 显示调用栈
frame <n>                    # 切换到指定栈帧

# === 其他 ===
list (ls)                    # 显示源代码
help                         # 显示帮助
quit (q)                     # 退出
```

#### 3. 调试场景演示

#### 场景1: 调试数组越界问题

```bash
# 启动调试
$ dlv debug main.go

(dlv) break handlers.GetUsers
Breakpoint 1 set at 0x... for debug-demo/handlers.GetUsers()

(dlv) continue
Starting server on :8080...

# 在另一个终端发送请求
$ curl <http://localhost:8080/api/users>

# 回到 dlv
(dlv) # 断点命中
> debug-demo/handlers.GetUsers() ./handlers/user.go:18

(dlv) list
   13:    {ID: 3, Name: "Charlie", Age: 35, Email: "charlie@example.com"},
   14: }
   15:
   16: func GetUsers(w http.ResponseWriter, r *http.Request) {
   17:    fmt.Println("GetUsers called")
=> 18:
   19:    var result []models.User
   20:    for i := 0; i < len(users)+1; i++ { // 故意越界
   21:        if i < len(users) {
   22:            result = append(result, users[i])

(dlv) print users
[]debug-demo/models.User len: 3, cap: 3, [
    {ID: 1, Name: "Alice", Age: 25, Email: "alice@example.com"},
    {ID: 2, Name: "Bob", Age: 30, Email: "bob@example.com"},
    {ID: 3, Name: "Charlie", Age: 35, Email: "charlie@example.com"},
]

(dlv) break 20
Breakpoint 2 set at 0x... for debug-demo/handlers.GetUsers()

(dlv) continue

(dlv) print i
0

(dlv) next
(dlv) next
(dlv) print i
1

(dlv) print result
[]debug-demo/models.User len: 1, cap: 1, [
    {ID: 1, Name: "Alice", Age: 25, Email: "alice@example.com"},
]

# 继续观察，发现 i=3 时会访问 users[3]，越界！
(dlv) condition 2 i == 3
(dlv) continue

(dlv) print i
3
(dlv) print len(users)
3
# 发现问题：i < len(users)+1 应该改为 i < len(users)
```

#### 场景2: 调试除零错误

```bash
$ dlv debug main.go

(dlv) break utils.Divide
Breakpoint 1 set at 0x...

(dlv) continue

# 发送请求：curl "<http://localhost:8080/api/calculate?a=10&b=0>"

(dlv) # 断点命中
> debug-demo/utils.Divide() ./utils/calculator.go:6

(dlv) args
a = 10
b = 0

(dlv) print b
0

(dlv) next
(dlv) next

# 可以看到即将执行除法
(dlv) list
    6: func Divide(a, b int) float64 {
    7:     fmt.Printf("Dividing %d by %d\\\\n", a, b)
    8:
=>  9:     return float64(a) / float64(b)  // 即将除以0！
   10: }

(dlv) # 这里应该添加检查
# if b == 0 { return 0 或 报错 }
```

#### 场景3: 调试 Goroutine

```go
// 添加到 main.go
func backgroundTask() {
    ticker := time.NewTicker(2 * time.Second)
    defer ticker.Stop()

    for {
        select {
        case <-ticker.C:
            fmt.Println("Background task running...")
            // 可能有 bug 的代码
        }
    }
}

func main() {
    go backgroundTask() // 启动后台任务
    // ... rest of code
}
```

调试 goroutine:

```bash
(dlv) goroutines
[6 goroutines]
* Goroutine 1 - User: ./main.go:15 main.main (0x...)
  Goroutine 2 - User: /usr/local/go/src/runtime/proc.go:367 runtime.gopark (0x...)
  Goroutine 3 - User: ./main.go:8 main.backgroundTask (0x...)
  Goroutine 4 - User: /usr/local/go/src/net/http/server.go:3070 ...
  ...

(dlv) goroutine 3
Switched from 1 to 3

(dlv) stack
0  0x... in main.backgroundTask
   at ./main.go:8
1  0x... in runtime.goexit
   at /usr/local/go/src/runtime/asm_amd64.s:1598

(dlv) locals
ticker = (*time.Ticker)(0x...)
```

#### 4. 条件断点和监视点

```bash
# 条件断点：只在 id == 2 时中断
(dlv) break handlers.GetUserByID
(dlv) condition 1 id == 2

# 或者在设置时直接指定
(dlv) break handlers.GetUserByID if id == 2

# 查看断点条件
(dlv) breakpoints
Breakpoint 1 at 0x... for handlers.GetUserByID() with condition id == 2
```

#### 5. 修改变量值

```bash
(dlv) break handlers.GetUserByID
(dlv) continue

(dlv) print id
2

# 修改变量值
(dlv) set id = 1
(dlv) print id
1

# 继续执行，现在使用新的 id 值
(dlv) continue
```

#### 6. 调用函数

```bash
(dlv) break handlers.GetUsers
(dlv) continue

# 在断点处调用函数
(dlv) call len(users)
3

(dlv) call utils.Add(10, 20)
30

# 调用方法
(dlv) call users[0].ValidateAge()
false
```

### 高级技巧

#### 1. 使用配置文件

创建 `.dlv/config.yml`:

```yaml
# 自动设置的断点
break:
  - handlers.GetUserByID
  - utils.Divide

# 替换路径（适用于容器调试）
substitute-path:
  - {from: "/go/src/app", to: "/Users/you/project"}
```

#### 2. 远程调试

```bash
# 服务器端启动 headless 模式
dlv debug --headless --listen=:2345 --api-version=2 main.go

# 本地连接
dlv connect localhost:2345
```

#### 3. VS Code 集成

`.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Launch Package",
            "type": "go",
            "request": "launch",
            "mode": "debug",
            "program": "${workspaceFolder}",
            "env": {},
            "args": []
        },
        {
            "name": "Attach to Process",
            "type": "go",
            "request": "attach",
            "mode": "local",
            "processId": 0
        },
        {
            "name": "Connect to Remote",
            "type": "go",
            "request": "attach",
            "mode": "remote",
            "remotePath": "${workspaceFolder}",
            "port": 2345,
            "host": "localhost"
        }
    ]
}
```

#### 4. GoLand/IDEA 集成

GoLand 内置了对 Delve 的支持：

1. 点击行号左侧设置断点
2. 点击 Debug 按钮（小虫子图标）
3. 使用 Variables 窗口查看变量
4. 使用 Watches 添加监视表达式

### 调试最佳实践

#### 1. 编译时保留调试信息

```bash
# 不要使用 -ldflags="-s -w"，这会移除调试信息
go build -gcflags="all=-N -l" -o myapp main.go

# 推荐的调试编译选项
go build -gcflags="all=-N -l" main.go
```

#### 2. 使用日志辅助调试

```go
import "log"

func GetUserByID(w http.ResponseWriter, r *http.Request) {
    log.Printf("[DEBUG] GetUserByID called: %s", r.URL.Path)

    path := strings.TrimPrefix(r.URL.Path, "/api/user/")
    log.Printf("[DEBUG] Extracted ID string: %s", path)

    id, err := strconv.Atoi(path)
    if err != nil {
        log.Printf("[ERROR] Invalid ID: %v", err)
        http.Error(w, "Invalid user ID", http.StatusBadRequest)
        return
    }
    log.Printf("[DEBUG] Parsed ID: %d", id)

    // ... rest of code
}
```

#### 3. 常见调试场景速查

```bash
# Panic 调试
(dlv) break runtime.gopanic
(dlv) continue
(dlv) stack

# 死锁调试
(dlv) goroutines
(dlv) goroutine <id>
(dlv) stack

# 内存泄漏调试
(dlv) break main.main
(dlv) continue
# 使用 pprof 结合分析

# 性能问题调试
(dlv) break mySlowFunction
(dlv) continue
(dlv) # 检查变量和逻辑
```

### 完整调试会话示例

```bash
$ dlv debug main.go

Type 'help' for list of commands.

(dlv) break main.main
Breakpoint 1 set at 0x10a1234 for main.main() ./main.go:10

(dlv) break handlers.GetUserByID
Breakpoint 2 set at 0x10a5678 for handlers.GetUserByID() ./handlers/user.go:28

(dlv) continue
> main.main() ./main.go:10 (hits goroutine(1):1 total:1)
     5: import (
     6:     "fmt"
     7:     "log"
     8:     "net/http"
     9:
=>  10:     "debug-demo/handlers"
    11: )
    12:
    13: func main() {
    14:     fmt.Println("Starting server on :8080...")
    15:

(dlv) next
(dlv) next
(dlv) next
Starting server on :8080...

(dlv) continue

# 在另一个终端: curl <http://localhost:8080/api/user/2>

> handlers.GetUserByID() ./handlers/user.go:28
    23:     Email string `json:"email"`
    24: }
    25:
    26: func GetUserByID(w http.ResponseWriter, r *http.Request) {
    27:     fmt.Println("GetUserByID called:", r.URL.Path)
=>  28:
    29:     path := strings.TrimPrefix(r.URL.Path, "/api/user/")
    30:     id, err := strconv.Atoi(path)
    31:     if err != nil {
    32:         http.Error(w, "Invalid user ID", http.StatusBadRequest)
    33:         return

(dlv) print r.URL.Path
"/api/user/2"

(dlv) next
(dlv) next
(dlv) print path
"2"

(dlv) next
(dlv) print id
2
(dlv) print err
error nil

(dlv) next
(dlv) print len(users)
3

(dlv) # 如果 id=4 会越界，我们可以测试
(dlv) set id = 4
(dlv) next
panic: runtime error: index out of range [3] with length 3

(dlv) stack
0  0x... in runtime.gopanic
   at /usr/local/go/src/runtime/panic.go:884
1  0x... in handlers.GetUserByID
   at ./handlers/user.go:36
2  0x... in net/http.HandlerFunc.ServeHTTP
   at /usr/local/go/src/net/http/server.go:2122

(dlv) quit
```

### 总结

Delve 的核心命令：

- `break` - 设置断点
- `continue` - 继续执行
- `next` - 单步执行
- `step` - 进入函数
- `print` - 查看变量
- `stack` - 查看调用栈
- `goroutines` - 查看 goroutine

调试流程：

1. 设置断点
2. 运行程序
3. 检查变量和状态
4. 单步执行找出问题
5. 修复代码

掌握这些技巧，你就能高效地调试 Go 程序了！