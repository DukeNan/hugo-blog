---
title: "SQLite3 完全指南：从基础到进阶的实战教程"
date: 2026-02-25T14:00:15+08:00
description: "深入解析 SQLite3 数据库的安装配置、核心操作、高级特性、性能优化以及在实际项目中的最佳实践，帮助你掌握轻量级数据库的使用技巧"
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
  - sql
---

SQLite 是世界上最广泛部署的数据库引擎，从嵌入式设备到移动应用，再到桌面应用，SQLite 凭借其轻量级、零配置、单文件存储的特点，成为了小型到中型项目的理想选择。本文将从零开始，系统性地介绍 SQLite3 的安装、基础操作、高级特性、性能优化以及在实际项目中的最佳实践。

<!-- more -->

## 简介

### 什么是 SQLite

**SQLite** 是一个轻量级的嵌入式关系型数据库管理系统（RDBMS），由 D. Richard Hipp 于 2000 年创建。与传统数据库（如 MySQL、PostgreSQL）不同，SQLite 不需要独立的服务器进程，而是直接作为库集成到应用程序中。

### SQLite 的特点

| 特性 | 说明 |
|------|------|
| **零配置** | 无需安装配置，开箱即用 |
| **单文件存储** | 整个数据库就是一个普通文件 |
| **跨平台** | 支持 Windows、Linux、macOS、iOS、Android 等 |
| **事务支持** | 完整的 ACID 事务支持 |
| **轻量级** | 核心库小于 500KB |
| **自包含** | 无需外部依赖 |
| **开源** | 公共领域（Public Domain） |

### SQLite 适用场景

**适合使用 SQLite 的场景：**
- 移动应用（iOS、Android）
- 桌面应用
- 嵌入式设备
- 小型网站和原型开发
- 测试和演示项目
- 数据分析和报表工具

**不适合使用 SQLite 的场景：**
- 高并发写入的大型网站
- 需要复杂权限控制的企业应用
- 需要分布式架构的系统
- 需要大量存储的过程和函数的复杂应用

## 安装与配置

### 在不同平台安装 SQLite

#### Linux (Ubuntu/Debian)

```bash
# 安装 SQLite3 命令行工具
sudo apt-get update
sudo apt-get install sqlite3

# 安装开发库（用于编程）
sudo apt-get install libsqlite3-dev

# 验证安装
sqlite3 --version
```

#### macOS

```bash
# macOS 自带 SQLite3
sqlite3 --version

# 如需更新版本，使用 Homebrew
brew install sqlite
```

#### Windows

1. 访问 [SQLite 官网](https://www.sqlite.org/download.html)
2. 下载预编译的二进制文件（sqlite-tools-win32-*.zip）
3. 解压并将 sqlite3.exe 放到 PATH 环境变量中

```cmd
# 验证安装
sqlite3 --version
```

### Python 环境配置

Python 标准库已内置 SQLite3 支持：

```python
# 检查 SQLite3 版本
import sqlite3
print(f"SQLite version: {sqlite3.sqlite_version}")
print(f"Python sqlite3 module version: {sqlite3.version}")
```

## 基础操作

### 创建数据库

```bash
# 创建新数据库（如果不存在）
sqlite3 my_database.db

# 创建临时数据库（内存数据库）
sqlite3 :memory:
```

**Python 示例：**

```python
import sqlite3

# 连接到数据库（如果不存在会自动创建）
conn = sqlite3.connect('my_database.db')

# 创建内存数据库
# conn = sqlite3.connect(':memory:')

# 创建游标对象
cursor = conn.cursor()

# 关闭连接
conn.close()
```

### 常用命令

```bash
# 进入 SQLite 命令行
sqlite3 my_database.db

# 查看数据库信息
.databases              # 列出所有数据库
.tables                 # 列出所有表
.schema                 # 显示所有表的创建语句
.schema table_name      # 显示指定表的创建语句

# 导入/导出数据
.dump                    # 导出数据库为 SQL 脚本
.read backup.sql         # 导入 SQL 脚本
.mode list              # 设置输出模式（list, line, column, html, csv 等）
.headers on             # 显示列名
.output output.csv      # 将输出重定向到文件
.import data.csv table_name  # 导入 CSV 文件

# 其他有用命令
.quit                   # 退出
.help                   # 显示帮助
.timer on               # 显示执行时间
```

## 数据类型

### SQLite 数据类型

SQLite 使用**动态类型系统**，虽然支持类型亲和性（Type Affinity），但不会严格强制执行类型约束。

| 数据类型 | 说明 | 亲和性 |
|---------|------|--------|
| **INTEGER** | 整数（1、2、3、4、6、8 字节） | INTEGER |
| **REAL** | 浮点数（8 字节 IEEE 浮点） | REAL |
| **TEXT** | 文本字符串（UTF-8、UTF-16） | TEXT |
| **BLOB** | 二进制数据 | NONE |
| **NUMERIC** | 根据内容自动转换为 INTEGER 或 REAL | NUMERIC |

### 数据类型示例

```sql
-- 创建各种数据类型的表
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL DEFAULT 0.0,
    stock INTEGER DEFAULT 0,
    description TEXT,
    image BLOB,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 插入数据
INSERT INTO products (name, price, stock, description)
VALUES ('iPhone 15', 7999.99, 100, '最新款智能手机');

-- 插入不同类型的数据（SQLite 会自动转换）
INSERT INTO products (id, name, price) VALUES (2, '数据转换', '100.50');
-- 价格 '100.50' 会被转换为 REAL 类型
```

### 类型亲和性规则

SQLite 使用类型亲和性来确定如何存储数据：

```sql
-- 查看列的类型信息
PRAGMA table_info(products);

-- 输出示例：
-- cid | name        | type    | notnull | dflt_value | pk
-- ----|-------------|---------|---------|------------|---
-- 0   | id          | INTEGER | 0       | NULL       | 1
-- 1   | name        | TEXT    | 1       | NULL       | 0
-- 2   | price       | REAL    | 0       | 0.0        | 0
-- 3   | stock       | INTEGER | 0       | 0          | 0
-- 4   | description | TEXT    | 0       | NULL       | 0
```

## 数据表操作

### 创建表

```sql
-- 基本表创建
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    age INTEGER CHECK (age >= 0 AND age <= 150),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 带外键约束的表
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    order_no TEXT NOT NULL UNIQUE,
    total_amount REAL NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 创建带索引的表
CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT,
    author TEXT,
    views INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_articles_author ON articles(author);
CREATE INDEX idx_articles_created ON articles(created_at DESC);
```

### 修改表结构

```sql
-- 添加列
ALTER TABLE users ADD COLUMN avatar BLOB;
ALTER TABLE users ADD COLUMN phone TEXT;

-- 重命名表
ALTER TABLE old_table_name RENAME TO new_table_name;

-- 注意：SQLite 不支持直接删除列或修改列类型
-- 需要通过重建表的方式实现：
-- 1. 创建新表（包含需要的列）
-- 2. 将数据从旧表复制到新表
-- 3. 删除旧表
-- 4. 重命名新表
```

### 删除表

```sql
-- 删除表
DROP TABLE users;

-- 删除表（如果存在）
DROP TABLE IF EXISTS users;
```

## 数据操作

### 插入数据

```sql
-- 单条插入
INSERT INTO users (username, email, age)
VALUES ('alice', 'alice@example.com', 25);

-- 多条插入
INSERT INTO users (username, email, age) VALUES
    ('bob', 'bob@example.com', 30),
    ('charlie', 'charlie@example.com', 28),
    ('diana', 'diana@example.com', 32);

-- 插入指定列
INSERT INTO users (username, email) VALUES ('eve', 'eve@example.com');

-- 使用默认值
INSERT INTO users (username, email) VALUES ('frank', 'frank@example.com');
-- age 和 created_at 会使用默认值

-- 插入或更新（UPSERT）
INSERT INTO users (username, email, age)
VALUES ('alice', 'new_email@example.com', 26)
ON CONFLICT(username) DO UPDATE SET
    email = excluded.email,
    age = excluded.age;
```

### 查询数据

```sql
-- 基本查询
SELECT * FROM users;

-- 查询指定列
SELECT username, email FROM users;

-- 条件查询
SELECT * FROM users WHERE age > 25;

-- 多条件查询
SELECT * FROM users WHERE age >= 25 AND age <= 35;

-- 范围查询
SELECT * FROM users WHERE age BETWEEN 25 AND 35;

-- IN 查询
SELECT * FROM users WHERE username IN ('alice', 'bob', 'charlie');

-- 模糊查询
SELECT * FROM users WHERE username LIKE 'a%';  -- 以 a 开头
SELECT * FROM users WHERE email LIKE '%@example.com';

-- 排序
SELECT * FROM users ORDER BY age ASC;
SELECT * FROM users ORDER BY age DESC, username ASC;

-- 限制结果数量
SELECT * FROM users LIMIT 5;
SELECT * FROM users LIMIT 5 OFFSET 2;  -- 分页

-- 去重
SELECT DISTINCT age FROM users;

-- 聚合查询
SELECT COUNT(*) FROM users;
SELECT COUNT(DISTINCT age) FROM users;
SELECT AVG(age) FROM users;
SELECT MAX(age), MIN(age) FROM users;
SELECT SUM(views) FROM articles;

-- 分组查询
SELECT age, COUNT(*) as count
FROM users
GROUP BY age
HAVING count > 1;
```

### 更新数据

```sql
-- 更新单条记录
UPDATE users SET email = 'new_alice@example.com' WHERE username = 'alice';

-- 更新多条记录
UPDATE users SET age = age + 1 WHERE age < 30;

-- 批量更新
UPDATE articles SET views = views + 1 WHERE id = 1;
```

### 删除数据

```sql
-- 删除单条记录
DELETE FROM users WHERE username = 'eve';

-- 删除多条记录
DELETE FROM users WHERE age < 25;

-- 删除所有数据（保留表结构）
DELETE FROM users;

-- 清空表并重置自增 ID
DELETE FROM users;
DELETE FROM sqlite_sequence WHERE name = 'users';

-- 更高效的方式（SQLite 3.7.17+）
TRUNCATE TABLE users;
```

## 高级查询

### 连接查询

```sql
-- 内连接
SELECT u.username, o.order_no, o.total_amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- 左连接
SELECT u.username, o.order_no
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- 多表连接
SELECT u.username, o.order_no, o.total_amount
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id;
```

### 子查询

```sql
-- 标量子查询
SELECT username,
       (SELECT COUNT(*) FROM orders WHERE user_id = users.id) as order_count
FROM users;

-- IN 子查询
SELECT * FROM users
WHERE id IN (SELECT DISTINCT user_id FROM orders WHERE total_amount > 1000);

-- EXISTS 子查询
SELECT * FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.status = 'completed'
);

-- FROM 子查询
SELECT * FROM (
    SELECT username, age,
           RANK() OVER (ORDER BY age DESC) as age_rank
    FROM users
) ranked_users
WHERE age_rank <= 10;
```

### 窗口函数

SQLite 3.25.0+ 支持窗口函数：

```sql
-- 排名函数
SELECT username, age,
       ROW_NUMBER() OVER (ORDER BY age DESC) as row_num,
       RANK() OVER (ORDER BY age DESC) as rank,
       DENSE_RANK() OVER (ORDER BY age DESC) as dense_rank
FROM users;

-- 分组排名
SELECT username, age,
       RANK() OVER (PARTITION BY age DIV 10 ORDER BY username) as group_rank
FROM users;

-- 累计求和
SELECT order_no, total_amount,
       SUM(total_amount) OVER (ORDER BY created_at) as running_total
FROM orders;

-- 移动平均
SELECT order_no, total_amount,
       AVG(total_amount) OVER (
           ORDER BY created_at
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) as moving_avg
FROM orders;
```

### 事务处理

```python
import sqlite3

conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

try:
    # 开始事务
    conn.execute("BEGIN TRANSACTION")

    # 执行多个操作
    cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", ('test', 'test@example.com'))
    cursor.execute("UPDATE users SET age = age + 1 WHERE username = 'alice'")

    # 提交事务
    conn.commit()
    print("事务提交成功")

except Exception as e:
    # 回滚事务
    conn.rollback()
    print(f"事务失败，已回滚: {e}")

finally:
    conn.close()
```

## 性能优化

### 索引优化

```sql
-- 查看表的索引
PRAGMA index_list(users);

-- 查看索引详细信息
PRAGMA index_info(idx_articles_author);

-- 分析索引使用情况
EXPLAIN QUERY PLAN SELECT * FROM users WHERE username = 'alice';

-- 创建复合索引
CREATE INDEX idx_users_age_email ON users(age, email);

-- 创建唯一索引
CREATE UNIQUE INDEX idx_users_username ON users(username);

-- 部分索引（只索引满足条件的行）
CREATE INDEX idx_active_orders ON orders(user_id) WHERE status = 'active';

-- 删除索引
DROP INDEX IF EXISTS idx_articles_author;
```

{{% notice note "注意📢" %}}
索引不是越多越好，每个索引都会增加写入开销。根据查询模式选择合适的索引。在写入频繁的表中，应谨慎添加索引。
{{% /notice %}}

### 查询优化

```sql
-- 使用 EXPLAIN 分析查询计划
EXPLAIN SELECT * FROM users WHERE username = 'alice';

-- 使用 EXPLAIN QUERY PLAN 获取更可读的输出
EXPLAIN QUERY PLAN SELECT * FROM users WHERE username = 'alice';

-- 避免使用 SELECT *
SELECT id, username FROM users;  -- ✅ 推荐
SELECT * FROM users;              -- ❌ 不推荐

-- 使用 LIMIT 限制结果数量
SELECT * FROM users LIMIT 1000;

-- 使用 UNION ALL 代替 UNION（如果不需要去重）
SELECT username FROM users WHERE age > 25
UNION ALL
SELECT username FROM users WHERE age < 20;

-- 使用 EXISTS 代替 IN（子查询）
SELECT * FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);
```

### 配置优化

```python
import sqlite3

conn = sqlite3.connect('my_database.db')

# 性能优化设置

# 设置同步模式（牺牲数据安全性换取性能）
# NORMAL: 每1000毫秒同步一次
# OFF: 不同步（最不安全，最快）
conn.execute("PRAGMA synchronous = NORMAL")

# 设置日记模式
# WAL: 写前日志（Write-Ahead Logging），支持并发读写
conn.execute("PRAGMA journal_mode = WAL")

# 设置缓存大小（KB）
conn.execute("PRAGMA cache_size = -64000")  # 64MB

# 设置临时存储位置（内存）
conn.execute("PRAGMA temp_store = MEMORY")

# 设置页面大小（字节）
conn.execute("PRAGMA page_size = 4096")

# 启用内存映射 I/O
conn.execute("PRAGMA mmap_size = 268435456")  # 256MB

# 设置繁忙超时（毫秒）
conn.execute("PRAGMA busy_timeout = 5000")

# 查看设置
cursor = conn.cursor()
cursor.execute("PRAGMA cache_size")
print(f"Cache size: {cursor.fetchone()[0]}")
```

### 批量插入优化

```python
import sqlite3

def insert_users_batch(users_data):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    # 开始事务
    conn.execute("BEGIN TRANSACTION")

    try:
        # 使用 executemany 批量插入
        cursor.executemany(
            "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
            users_data
        )
        conn.commit()
        print(f"成功插入 {len(users_data)} 条记录")

    except Exception as e:
        conn.rollback()
        print(f"插入失败: {e}")

    finally:
        conn.close()

# 示例数据
users = [
    ('user1', 'user1@example.com', 25),
    ('user2', 'user2@example.com', 30),
    ('user3', 'user3@example.com', 28),
    # ... 更多数据
]

insert_users_batch(users)
```

## 备份与恢复

### 备份数据库

```bash
# 方法1：使用 .dump 命令
sqlite3 my_database.db .dump > backup.sql

# 方法2：直接复制文件（最简单）
cp my_database.db my_database_backup.db

# 方法3：使用 Python 备份
```

```python
import sqlite3

def backup_database(source_db, backup_db):
    # 连接源数据库
    source = sqlite3.connect(source_db)
    # 创建备份
    backup = sqlite3.connect(backup_db)

    # 执行备份
    with backup:
        source.backup(backup)

    source.close()
    backup.close()
    print(f"备份成功: {backup_db}")

backup_database('my_database.db', 'backup.db')
```

### 恢复数据库

```bash
# 从 SQL 备份恢复
sqlite3 my_database.db < backup.sql

# 从文件备份恢复
cp my_database_backup.db my_database.db
```

```python
import sqlite3

def restore_database(backup_db, target_db):
    # 连接目标数据库
    target = sqlite3.connect(target_db)
    # 连接备份
    backup = sqlite3.connect(backup_db)

    # 执行恢复
    with target:
        backup.backup(target)

    target.close()
    backup.close()
    print(f"恢复成功: {target_db}")

restore_database('backup.db', 'my_database.db')
```

## 常见问题

### Q1: 如何处理并发访问？

SQLite 支持多种并发模式：

```python
import sqlite3

# 启用 WAL 模式以支持并发读写
conn = sqlite3.connect('my_database.db')
conn.execute("PRAGMA journal_mode = WAL")

# 设置繁忙超时
conn.execute("PRAGMA busy_timeout = 5000")
```

**并发模式对比：**

| 模式 | 并发读写 | 并发写 | 性能 | 数据安全性 |
|------|---------|--------|------|-----------|
| DELETE | ❌ | ❌ | 低 | 高 |
| TRUNCATE | ❌ | ❌ | 中 | 中 |
| PERSIST | ❌ | ❌ | 中 | 中 |
| MEMORY | ❌ | ❌ | 高 | 低 |
| WAL | ✅ | ❌ | 高 | 高 |

### Q2: 如何处理数据库文件损坏？

```python
import sqlite3

def try_recover_database(db_path):
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA integrity_check")
        result = conn.fetchone()[0]
        if result == "ok":
            print("数据库完整")
        else:
            print(f"数据库可能损坏: {result}")
        conn.close()
    except sqlite3.DatabaseError as e:
        print(f"数据库错误: {e}")

try_recover_database('my_database.db')
```

### Q3: 如何加密 SQLite 数据库？

SQLite 本身不支持加密，但可以使用扩展：

```python
# 使用 pysqlcipher3（需要单独安装）
# pip install pysqlcipher3
"""
from pysqlcipher3 import dbapi2 as sqlite

# 创建加密数据库
conn = sqlite.connect('encrypted.db')
conn.execute("PRAGMA key = 'your_encryption_key'")
conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
conn.commit()
conn.close()

# 打开加密数据库
conn = sqlite.connect('encrypted.db')
conn.execute("PRAGMA key = 'your_encryption_key'")
"""
```

### Q4: 如何优化大数据量查询？

```sql
-- 创建适当的索引
CREATE INDEX idx_composite ON table_name(column1, column2);

-- 使用部分索引
CREATE INDEX idx_active ON orders(user_id) WHERE status = 'active';

-- 使用覆盖索引
CREATE INDEX idx_covering ON users(username, email, age);

-- 分析查询计划
EXPLAIN QUERY PLAN SELECT * FROM users WHERE username = 'alice';

-- 使用 LIMIT
SELECT * FROM large_table LIMIT 1000;

-- 使用分页
SELECT * FROM large_table LIMIT 100 OFFSET 200;
```

### Q5: SQLite 有哪些限制？

| 限制 | 值 |
|------|-----|
| 最大数据库大小 | 140 TB |
| 最大表大小 | 32 TB |
| 最大行大小 | 1 GB |
| 最大列数 | 32767 |
| 最大索引列数 | 255 |
| 最大并发连接数 | 无限制（受系统资源限制） |
| 最大 SQL 语句长度 | 1000000000 字节 |

## 最佳实践

### 1. 使用参数化查询

```python
# ❌ 不安全：SQL 注入风险
username = input("输入用户名: ")
cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")

# ✅ 安全：使用参数化查询
username = input("输入用户名: ")
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

# ✅ 多个参数
cursor.execute(
    "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
    ('alice', 'alice@example.com', 25)
)
```

### 2. 使用上下文管理器

```python
# ✅ 使用 with 语句自动关闭连接
with sqlite3.connect('my_database.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    # 连接会自动关闭
```

### 3. 异常处理

```python
import sqlite3

try:
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", ('test', 'test@example.com'))
    conn.commit()

except sqlite3.IntegrityError as e:
    print(f"数据完整性错误: {e}")
except sqlite3.OperationalError as e:
    print(f"操作错误: {e}")
except sqlite3.Error as e:
    print(f"数据库错误: {e}")
finally:
    if conn:
        conn.close()
```

### 4. 定期维护

```sql
-- 分析表以优化查询计划
ANALYZE;

-- 重建数据库以减少碎片
VACUUM;

-- 清理临时数据
PRAGMA incremental_vacuum;
```

### 5. 监控性能

```python
import sqlite3
import time

def execute_with_timing(conn, query, params=None):
    start_time = time.time()
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    elapsed = time.time() - start_time
    print(f"查询耗时: {elapsed:.4f} 秒")
    return cursor

# 使用示例
conn = sqlite3.connect('my_database.db')
cursor = execute_with_timing(conn, "SELECT * FROM users WHERE age > ?", (25,))
results = cursor.fetchall()
conn.close()
```

## 实战案例

### 案例1：博客系统

```python
import sqlite3
from datetime import datetime

class BlogDatabase:
    def __init__(self, db_path='blog.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        """创建博客相关表"""
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                slug TEXT NOT NULL UNIQUE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                slug TEXT NOT NULL UNIQUE,
                content TEXT NOT NULL,
                excerpt TEXT,
                category_id INTEGER,
                status TEXT DEFAULT 'draft',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_posts_status
            ON posts(status, created_at DESC)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_posts_category
            ON posts(category_id)
        """)

        self.conn.commit()

    def create_post(self, title, content, category_id=None, status='draft'):
        """创建新文章"""
        cursor = self.conn.cursor()
        slug = title.lower().replace(' ', '-')
        cursor.execute("""
            INSERT INTO posts (title, slug, content, category_id, status)
            VALUES (?, ?, ?, ?, ?)
        """, (title, slug, content, category_id, status))
        self.conn.commit()
        return cursor.lastrowid

    def get_published_posts(self, limit=10):
        """获取已发布的文章"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT p.*, c.name as category_name
            FROM posts p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.status = 'published'
            ORDER BY p.created_at DESC
            LIMIT ?
        """, (limit,))
        return cursor.fetchall()

    def get_post_by_slug(self, slug):
        """根据 slug 获取文章"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT p.*, c.name as category_name
            FROM posts p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.slug = ?
        """, (slug,))
        return cursor.fetchone()

    def close(self):
        """关闭数据库连接"""
        self.conn.close()

# 使用示例
blog = BlogDatabase()
blog.create_post(
    title="我的第一篇文章",
    content="这是文章内容...",
    category_id=1,
    status='published'
)
posts = blog.get_published_posts()
blog.close()
```

### 案例2：用户认证系统

```python
import sqlite3
import hashlib
import secrets

class AuthSystem:
    def __init__(self, db_path='auth.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        """创建认证相关表"""
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                is_active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT NOT NULL UNIQUE,
                expires_at DATETIME NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sessions_token
            ON sessions(token)
        """)

        self.conn.commit()

    def _generate_salt(self):
        """生成随机 salt"""
        return secrets.token_hex(16)

    def _hash_password(self, password, salt):
        """密码哈希"""
        return hashlib.sha256((password + salt).encode()).hexdigest()

    def register_user(self, username, email, password):
        """注册用户"""
        cursor = self.conn.cursor()
        salt = self._generate_salt()
        password_hash = self._hash_password(password, salt)

        try:
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, salt)
                VALUES (?, ?, ?, ?)
            """, (username, email, password_hash, salt))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def verify_user(self, username, password):
        """验证用户"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, password_hash, salt, is_active
            FROM users
            WHERE username = ?
        """, (username,))
        user = cursor.fetchone()

        if not user:
            return False

        user_id, stored_hash, salt, is_active = user

        if not is_active:
            return False

        password_hash = self._hash_password(password, salt)
        return secrets.compare_digest(password_hash, stored_hash)

    def create_session(self, user_id, expires_hours=24):
        """创建会话"""
        cursor = self.conn.cursor()
        token = secrets.token_urlsafe(32)
        from datetime import timedelta
        expires_at = datetime.now() + timedelta(hours=expires_hours)

        cursor.execute("""
            INSERT INTO sessions (user_id, token, expires_at)
            VALUES (?, ?, ?)
        """, (user_id, token, expires_at))
        self.conn.commit()
        return token

    def verify_session(self, token):
        """验证会话"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT s.user_id, s.expires_at
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.token = ? AND u.is_active = 1 AND s.expires_at > datetime('now')
        """, (token,))
        return cursor.fetchone()

    def close(self):
        """关闭数据库连接"""
        self.conn.close()

# 使用示例
auth = AuthSystem()
auth.register_user('alice', 'alice@example.com', 'secure_password')
if auth.verify_user('alice', 'secure_password'):
    print("登录成功！")
auth.close()
```

## 总结

SQLite 是一个强大且灵活的轻量级数据库，适合各种规模的项目。

**核心要点：**

**SQLite 特点：**
- 零配置，开箱即用
- 单文件存储，易于管理
- 完整的 ACID 事务支持
- 跨平台兼容性好

**最佳实践：**
1. 使用参数化查询防止 SQL 注入
2. 合理使用索引优化查询性能
3. 启用 WAL 模式支持并发读写
4. 定期执行 VACUUM 和 ANALYZE 维护数据库
5. 使用事务保证数据一致性
6. 适当设置 PRAGMA 参数优化性能

**适用场景：**
- 移动和桌面应用
- 嵌入式设备
- 小型网站和原型
- 测试和演示项目

SQLite 凭借其简洁的设计和出色的性能，成为了轻量级数据库的首选选择。掌握 SQLite 的使用技巧，能够帮助开发者快速构建高效、可靠的数据存储解决方案。

## 参考资源

- [SQLite 官方文档](https://www.sqlite.org/docs.html)
- [Python sqlite3 模块文档](https://docs.python.org/3/library/sqlite3.html)
- [SQL As Understood By SQLite](https://www.sqlite.org/lang.html)
- [SQLite Query Optimization](https://www.sqlite.org/queryplanner.html)
