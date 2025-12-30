---
title: "Chrony 使用指南：Linux 时间同步最佳实践"
date: 2025-12-30T14:45:28+08:00
description: "Chrony 是一款灵活的网络时间协议 (NTP) 实现，适用于 Linux 系统。本文介绍 Chrony 的安装、配置和使用方法，帮助你实现高精度的时间同步。"
author: "shaun"
featured: false
draft: false
toc: false
usePageBundles: false
categories:
  - Technology
tags:
  - linux
---

Chrony 是一款开源的网络时间协议 (NTP) 实现，专为 Linux 系统设计。相比于传统的 ntpd，Chrony 在处理不稳定的网络环境、间歇性网络连接以及虚拟机环境时表现更为出色。

## Chrony vs ntpd

| 特性 | Chrony | ntpd |
|------|--------|------|
| 网络中断恢复 | 快速同步 | 同步较慢 |
| 虚拟机支持 | 优秀 | 一般 |
| 时钟频率调整 | 动态调整 | 固定调整 |
| 配置复杂度 | 简单 | 较复杂 |
| 内存占用 | 较低 | 较高 |

## 安装 Chrony

### Debian/Ubuntu

```bash
sudo apt update
sudo apt install chrony
```

### RHEL/CentOS/Rocky/AlmaLinux

```bash
sudo dnf install chrony
```

### Arch Linux

```bash
sudo pacman -S chrony
```

## 配置文件详解

Chrony 的主配置文件位于 `/etc/chrony.conf`：

```bash
# /etc/chrony.conf

# 使用 NTP 服务器池
pool pool.ntp.org iburst

# 允许特定网段同步时间
allow 192.168.1.0/24

# 启用实时调度（提高精度）
rtc device /dev/rtc

# 设置最大同步偏移量（秒）
makestep 1.0 3

# 启用 drift 文件记录时钟漂移
driftfile /var/lib/chrony/drift

# 日志目录
logdir /var/log/chrony
```

### 关键配置说明

| 参数 | 说明 |
|------|------|
| `server` | 指定单个 NTP 服务器 |
| `pool` | 指定 NTP 服务器池，自动选择多个服务器 |
| `iburst` | 启动时快速发送数据包加速同步 |
| `allow` | 允许哪些客户端同步时间 |
| `makestep` | 当时间偏差超过阈值时立即调整 |
| `driftfile` | 记录系统时钟的漂移特性 |

## 常用命令

### 检查同步状态

```bash
chronyc sources
```

输出示例：

```
MS Name/IP address         Stratum Poll Reach LastRx Last sample
===============================================================================
^* time1.google.com              1   6   377    25   +123us[+234us] +/-   11ms
^- time2.google.com              1   6   377    26   -456us[-345us] +/-   12ms
^+ time3.google.com              1   6   377    27   +789us[+890us] +/-   13ms
```

**状态标识含义：**
- `^*` - 当前同步源
- `^+` - 可接受同步源
- `^-` - 不可接受同步源
- `^?` - 连接失败

### 查看源统计信息

```bash
chronyc sourcestats
```

### 追踪同步过程

```bash
chronyc tracking
```

输出示例：

```
Reference ID    : C0A80101 (192.168.1.1)
Stratum         : 2
Ref time (UTC)  : Mon Dec 30 06:45:28 2025
System time     : 0.000001500 seconds fast of NTP time
Last offset     : +0.000012345 seconds
RMS offset      : 0.000023456 seconds
Frequency       : 15.123 ppm fast
Residual freq   : +0.000 ppm
Skew            : 0.012 ppm
Root delay      : 0.012345678 seconds
Root dispersion : 0.001234567 seconds
Update interval : 64.2 seconds
Leap status     : Normal
```

### 手动同步时间

```bash
chronyc makestep
```

## 服务管理

### 启动并设置开机自启

```bash
sudo systemctl enable --now chronyd
```

### 检查服务状态

```bash
sudo systemctl status chronyd
```

### 重启服务

```bash
sudo systemctl restart chronyd
```

## 配置为 NTP 服务器

如果你想让局域网内的其他机器同步你的服务器时间：

```bash
# /etc/chrony.conf

# 上游 NTP 服务器
pool pool.ntp.org iburst

# 允许局域网客户端
allow 192.168.0.0/16

# 监听所有接口
bindaddress 0.0.0.0
```

记得在防火墙中开放 UDP 123 端口：

```bash
# firewalld
sudo firewall-cmd --permanent --add-service=ntp
sudo firewall-cmd --reload

# ufw
sudo ufw allow ntp
```

## 虚拟机优化配置

对于虚拟机环境，建议添加以下配置：

```bash
# /etc/chrony.conf

# 允许较大的时间偏移
makestep 1.0 -1

# 禁用实时时钟
rtcsync off

# 更频繁的轮询
maxupdateskew 100.0
```

## 常见问题排查

### 时间无法同步

1. 检查网络连接：
```bash
chronyc activity
```

2. 检查防火墙规则：
```bash
sudo iptables -L -n | grep 123
```

3. 验证 NTP 服务器可达性：
```bash
ntpdate -q pool.ntp.org
```

### 时钟漂移过大

查看漂移文件：
```bash
cat /var/lib/chrony/drift
```

如果漂移值异常（>500ppm），可能是硬件时钟问题。

### SELinux 阻止 chronyd

```bash
# 检查 SELinux 状态
getenforce

# 如果是 Enforcing，可以临时设置为 Permissive 测试
sudo setenforce 0
```

## 与 systemd-timesyncd 的选择

| 场景 | 推荐方案 |
|------|----------|
| 桌面系统 | systemd-timesyncd |
| 服务器/需要高精度 | chrony |
| 虚拟机 | chrony |
| 网络不稳定环境 | chrony |

禁用 systemd-timesyncd 并使用 chrony：

```bash
sudo timedatectl set-ntp false
sudo systemctl enable --now chronyd
```

## 总结

Chrony 是现代 Linux 系统时间同步的首选方案，特别适合服务器和虚拟机环境。通过合理配置 `makestep`、`driftfile` 和服务器池，可以实现高精度、高可靠性的时间同步服务。

对于生产环境，建议：
1. 使用本地 NTP 服务器池减轻公共服务器负载
2. 配置防火墙保护 NTP 服务
3. 定期检查同步日志
4. 监控时间偏移和漂移值
