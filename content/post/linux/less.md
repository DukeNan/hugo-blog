---
title: "Linux之less命令"
date: 2022-12-27T17:14:50+08:00
description: "Linux Less"
author: "shaun"
featured: true
draft: false

# menu: main
usePageBundles: false
codeMaxLines: 10
codeLineNumbers: false
figurePositionShow: true
categories:
  - Technology
tags:
  - linux
# comment: false # Disable comment if false.
---

`Linux`中的`less`命令主要用来浏览文件内容，与`more`命令的用法相似，不同于`more`命令的是，`less`命令可往回卷动浏览以看过的部分。less的用法比起more更加的有弹性。在more的时候,我们并没有办法向前面翻,只能往后面看，但若使用了less时，就可以使用 `［pageup］` `［pagedown]`等按键的功能来往前往后翻看文件，更容易用来查看一个文件的内容！除此之外，在less里头可以拥有更多的搜索功能，不止可以向下搜，也可以向上搜。
<!--more-->

### 命令格式

less [参数] 文件

### 命令功能

> less和more类似,但是使用less可以随意浏览文件,而more仅能向前移动,却不能向后移动,more启动时会加载整个文件。而且less在查看之前不会加载整个文件。

### 命令参数

- Down arrow，Enter，e，或者j --向前移动一行。
- Up arrow，y或k -- 向后移动一行。
- Space bar 要么 f – 前进一页。
- b – 向后移动一页。
- /pattern – 向前搜索匹配的模式。
- ?pattern – 向后搜索匹配的模式。
- n – 重复上一个搜索。
- N – 反向重复先前的搜索。
- g – 转到文件的第一行。
- Ng – 转到文件中的第N行。
- G – 转到文件的最后一行。
- p – 转到文件开头。
- Np – 进入文件的N％。
- h – 显示帮助。
- q – 退出less。

### 查看文件

```bash
$ less rumenz.txt
```

### ps查看进程信息并通过less分页显示

```bash
$ ps -ef | less
```

### 查看命令历史使用记录并通过less分页显示

```bash
$ history | less
```

### 浏览多个文件

```bash
# 输入:n后,切换到 1.txt 输入:p后,切换到 2.txt

$ less 1.txt 2.txt

```

### 全屏导航

```text
ctrl + F - 向前移动一屏
ctrl + B - 向后移动一屏
ctrl + D - 向前移动半屏
ctrl + U - 向后移动半屏
```
### 单行导航

```text
j - 向前移动一行
k - 向后移动一行
```
### 其他功能

```text
G - 移动到最后一行
g - 移动到第一行
q / ZZ - 退出 less 命令
```

### 搜索功能

```text
# 1.打开文件
less -RN demo.log
# 2.跳至行尾
shift + g
# 3.查找字符串
?get_date

n – 向前查找前一个匹配的文本
N – 向后查找下一个匹配的文本
```