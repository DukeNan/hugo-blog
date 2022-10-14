---
title: "Linux三剑客之awk"
date: 2022-10-13T17:54:00+08:00
description: "Linux三剑客之awk"
author: "shaun"
featured: true
toc: false
# menu: main
usePageBundles: false
codeMaxLines: 10
codeLineNumbers: false
figurePositionShow: true
categories:
  - Technology
tags:
  - linux
---
awk是由Alfred Aho 、Peter Weinberger 和 Brian Kernighan这三个人创造的，awk由这个三个人的姓氏的首个字母组成。awk早期是在unix上实现的，所以，我们现在在linux的所使用的awk其实是gawk，也就是GNU awk，简称为gawk，awk还有一个版本，New awk，简称为nawk，但是linux中最常用的还是gawk。awk其实是一门编程语言，它支持条件判断、数组、循环等功能。所以，我们也可以把awk理解成一个脚本语言解释器。
<!--more-->

### 基本用法

和我们平常使用的 Linux 命令一样， awk 也是遵循着某种格式来使用，格式如下：

使用格式
> awk 执行的事件 文件

例如：
```bash
root@jaking-virtual-machine:~# awk '{print $0}' test.txt
My first language:Python
My second language:Shell
My third language:Java
My fourth language:C
```

其中，print 表示打印，$0 表示一整个记录，test.txt 表示一个文件。所以

awk '{print $0}' test.txt

表示把 test.txt 文件里面的每行记录都打印出来。

$0 表示整个记录，不过 $1, $2, $3.....则表示整个记录中的第一个字段，第二个字段......。

```bash
root@jaking-virtual-machine:~# awk '{print $1}' test.txt
My
My
My
My
root@jaking-virtual-machine:~# awk '{print $2}' test.txt
first
second
third
fourth
root@jaking-virtual-machine:~# awk '{print $3}' test.txt
language:Python
language:Shell
language:Java
language:C
```

刚才我们说字段的默认分隔符是空格或者制表符这些，默认意味着我们可以自己显式着指定分隔符。下面我们用“：”来作为我们的分隔符吧。

```bash
root@jaking-virtual-machine:~#  awk -F ':' '{print $2}' test.txt
Python
Shell
Java
C
```

上面我们用参数 -F 指定了我们的分隔符，即如果想要指定字段的分隔符，可以用参数 -F 指定分隔符。

### 条件限制

在打印文本的时候，我们可以指定一些条件。格式如下：

awk 参数 条件 要执行的动作 文件

例如我们指定分隔符为“：”，条件为第二个字段为"Java"的记录。

\# 打印第二个字段为"Java"的文本

```bash
root@jaking-virtual-machine:~# awk -F ':' '$2 == "Java" {print $2}' test.txt
Java
```

打印奇数行的的第二个字段：

\# 打印奇数行的记录

```bash
root@jaking-virtual-machine:~# awk -F ':' 'NR % 2 == 1 {print $2}' test.txt
Python
Java
```

其中，NR 是一个内置的变量，表示当前正在处理的记录，即当前的记录是第几个记录。

### 条件语句

和我们平常的编程一样，awk 也提供了 if, else, while 等这些条件语句。

例如，打印第二个及其之后的记录：

```
root@jaking-virtual-machine:~# awk '{if(NR > 1) print $2}' test.txt
second
third
fourth
```

注意，上面的字段分隔符是空格了，并且 if 语句是在“{}” 里指定的。

再看一个例子：

```bash
root@jaking-virtual-machine:~# awk '{if($1 < "s") print $1; else print $2}' test.txt
# 如果第一个字段小于“s",则打印第一个字段，否则打印第二个字段
My
My
My
My
root@jaking-virtual-machine:~# awk '{if($1 > "s") print $1; else print $2}' test.txt
first
second
third
fourth
root@jaking-virtual-machine:~# awk '{if($1 < "l") print $1; else print $2}' test.txt
My
My
My
My
root@jaking-virtual-machine:~# awk '{if($1 > "l") print $1; else print $2}' test.txt
first
second
third
fourth
root@jaking-virtual-machine:~# awk '{if($1 > "c") print $1; else print $2}' test.txt
first
second
third
fourth
root@jaking-virtual-machine:~# awk '{if($1 > "d") print $1; else print $2}' test.txt
first
second
third
fourth
root@jaking-virtual-machine:~# awk '{if($1 > "p") print $1; else print $2}' test.txt
first
second
third
fourth
root@jaking-virtual-machine:~# awk '{if($1 < "p") print $1; else print $2}' test.txt
My
My
My
My
root@jaking-virtual-machine:~# awk '{if($3 < "s") print $3; else print $2}' test.txt
language:Python
language:Shell
language:Java
language:C
root@jaking-virtual-machine:~# awk '{if($2 < "s") print $3; else print $2}' test.txt
language:Python
second
third
language:C
root@jaking-virtual-machine:~# awk '{if($2 < "s") print $1; else print $2}' test.txt
My
second
third
My
```

### 函数

awk 提供了一些内置函数来供我们使用，一下常用的函数如下：

```bash
tolower()：字符转为小写。
toupper()：字符转为大写
length()：返回字符串长度。
substr()：返回子字符串。
sqrt()：平方根。
rand()：随机数。
```

```bash
root@jaking-virtual-machine:~# awk '{print toupper($1)}' test.txt
MY
MY
MY
MY
root@jaking-virtual-machine:~# awk '{print tolower($1)}' test.txt
my
my
my
my
root@jaking-virtual-machine:~# awk -F ':' '{print toupper($2)}' test.txt
PYTHON
SHELL
JAVA
C
root@jaking-virtual-machine:~# awk -F ':' '{print tolower($2)}' test.txt
python
shell
java
c
```

### 变量

刚才我们说 NR 是一个表示当前正在处理的记录是第几个记录的内置变量，常用的内置变量如下：

```
NR：表示当前处理的是第几行
NF：表示当前行有多少个字段
FILENAME：当前文件名
FS：字段分隔符，默认是空格和制表符。
RS：行分隔符，用于分割每一行，默认是换行符。
OFS：输出字段的分隔符，用于打印时分隔字段，默认为空格。
ORS：输出记录的分隔符，用于打印时分隔记录，默认为换行符。
```

例如我们要打印每一个记录的最后一个字段，就可以使用变量 NF 了。

```
root@jaking-virtual-machine:~# awk '{print $NF}' test.txt
language:Python
language:Shell
language:Java
language:C
```

对了，刚才那个 NR 的变量也是挺好用的，例如：

```bash
root@jaking-virtual-machine:~# awk '{print NR ". "  $0}' test.txt
1. My first language:Python
2. My second language:Shell
3. My third language:Java
4. My fourth language:C
```
