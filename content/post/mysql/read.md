---
title: "Mysql脏读、不可重复读、幻读"
date: 2022-09-29T15:56:20+08:00
description: "Article description."
author: "shaun"
featured: true
draft: false
toc: false
# menu: main
usePageBundles: false
codeMaxLines: 10
codeLineNumbers: false
figurePositionShow: true
categories:
  - Technology
tags:
  - sql
# comment: false # Disable comment if false.
---

MySQL 是支持多事务并发执行的。既然事务可以并发操作,这里就有一些问题：一个事务在写数据的时候，另一个事务要读这行数据，该怎么处理？一个事务在写数据，另一个数据也要写这行数据，又该怎么处理这个冲突？这就是并发事务所产生的一些问题。具体来说就是：`脏读`、`不可重复读`和`幻读`。
<!--more-->
### 概念说明

#### 脏读
脏读指的是读到了其他事务未提交的数据，未提交意味着这些数据可能会回滚，也就是可能最终不会存到数据库中，也就是不存在的数据。读到了并一定最终存在的数据，这就是脏读。
<img alt="脏读" style="zoom:80%" src="https://shaun007.oss-cn-shenzhen.aliyuncs.com/blog/images/mysql/read_01.jpg"/>
脏读最大的问题就是可能会读到不存在的数据。比如在上图中，事务B的更新数据被事务A读取，但是事务B回滚了，更新数据全部还原，也就是说事务A刚刚读到的数据并没有存在于数据库中。

**从宏观来看，就是事务A读出了一条不存在的数据，这个问题是很严重的。**

### 不可重复读

不可重复读指的是在一个事务内，最开始读到的数据和事务结束前的任意时刻读到的同一批数据出现不一致的情况。
<img alt="不可重复读" style="zoom:80%" src="https://shaun007.oss-cn-shenzhen.aliyuncs.com/blog/images/mysql/read_02.jpg"/>

**事务A多次读取同一数据，但事务B在事务A多次读取的过程中，对数据作了更新并提交，导致事务A多次读取同一数据时，结果 不一致。**

### 幻读

脏读、不可重复读上面的图文都很好的理解，对于幻读网上有很多文章都是这么解释的

> 幻读错误的理解：说幻读是 事务A 执行两次 select 操作得到不同的数据集，即 select 1 得到 10 条记录，select 2 得到 15 条记录。这其实并不是幻读，既然第一次和第二次读取的不一致，那不还是不可重复读吗，所以这是不可重复读的一种。

正确的理解应该是:

> 幻读，并不是说两次读取获取的结果集不同，幻读侧重的方面是某一次的 select 操作得到的结果所表征的数据状态无法支撑后续的业务操作。更为具体一些：select 某记录是否存在，不存在，准备插入此记录，但执行 insert 时发现此记录已存在，无法插入，此时就发生了幻读。

**举例:**

假设有张用户表,这张表的 id 是主键。表中一开始有4条数据。
<img alt="幻读1" style="zoom:80%" src="https://shaun007.oss-cn-shenzhen.aliyuncs.com/blog/images/mysql/read_03.jpg"/>

我们再来看下出现幻读的场景
<img alt="幻读2" style="zoom:80%" src="https://shaun007.oss-cn-shenzhen.aliyuncs.com/blog/images/mysql/read_04.jpg"/>

这里是在`RR`级别下研究(可重复读),因为`RU/RC`下还会存在脏读、不可重复读，故我们就以`RR`级别来研究幻读，排除其他干扰。

1. 事务A,查询是否存在 id=5 的记录，没有则插入，这是我们期望的正常业务逻辑。
2. 这个时候事务B新增的一条id=5的记录，并提交事务。
3. 事务A,再去查询id=5的时候,发现还是没有记录（因为这里是在RR级别下研究(可重复读)，所以读到依然没有数据）
4. 事务A,插入一条id=5的数据。

最终 事务A 提交事务，发现报错了。这就很奇怪，查的时候明明没有这条记录，但插入的时候却告诉我主键冲突，这就好像幻觉一样。这才是所有的幻读。

**不可重复读侧重表达 读-读，幻读则是说 读-写，用写来证实读的是鬼影。**

### 事务的隔离级别

上述所说的"脏读"，"不可重复读"，"幻读"这些问题，其实就是数据库读一致性问题，必须由数据库提供的事务隔离机制来进行解决。

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
| :------: | ---- | ---------- | ---- |
| 读未提交 | 发生 | 发生       | 发生 |
| 读已提交 | &#x2705;    | 发生 |  发生  |
| 可重复读 | &#x2705;    |     &#x2705;       |  可在next-key lock下解决  |
| 串行化   | &#x2705;    |     &#x2705;       | &#x2705; |

首先说`读未提交`，它是性能最好，也可以说它是最野蛮的方式，因为它压根儿就不加锁，所以根本谈不上什么隔离效果，可以理解为没有隔离。

再来说`串行化`。串行化就相当于上面所说的，处理一个人请求的时候，别的人都等着。读的时候加共享锁，也就是其他事务可以并发读，但是不能写。写的时候加排它锁，其他事务不能并发写也不能并发读。

最后说`读已提交`和`可重复读`。这两种隔离级别是比较复杂的，既要允许一定的并发，又想要兼顾的解决问题。MySQL默认事务隔离级别为`可重复读(RR)`,oracle默认事务隔离级别为`读已提交(RC)`。

数据库的事务隔离越严格，并发副作用越小，但付出的代价越大；因为事务隔离本质就是使事务在一定程度上处于串行状态，这本身就是和并发相矛盾的。

同时，不同的应用对读一致性和事务隔离级别是不一样的，比如许多应用对数据的一致性没那么个高要求，相反，对并发有一定要求。
