---
title: "acme.sh 使用指南：Linux SSL 证书自动化管理"
date: 2025-12-31T09:42:30+08:00
description: "acme.sh 是一款纯 Shell 实现的 ACME 客户端，支持从 Let's Encrypt 等证书颁发机构自动申请、更新和安装 SSL 证书。本文详细介绍 acme.sh 的安装、配置和常见使用场景。"
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

在当今的互联网环境中，HTTPS 已成为网站的标配。Let's Encrypt 提供免费的 SSL 证书，使得任何网站都能轻松启用加密连接。acme.sh 是一款优秀的 ACME 协议客户端，它完全用 Shell 脚本编写，无需 Python 等依赖，支持多种验证方式和 DNS 提供商，是证书自动化管理的理想选择。

本文将全面介绍 acme.sh 的安装方法、核心功能以及实际应用场景，帮助你构建自动化的 SSL 证书管理体系。
<!--more-->

## acme.sh 核心概念

### 什么是 acme.sh?

acme.sh 是一个用纯 Shell 语言编写的 ACME 协议客户端，用于从 Let's Encrypt、ZeroSSL、Buypass 等 CA 机构自动申请和更新 SSL/TLS 证书。它支持完整的证书生命周期管理，包括申请、更新、安装和撤销。

### acme.sh 的优势

**纯 Shell 实现**。与 certbot 等基于 Python 的客户端不同，acme.sh 仅依赖基础 Shell 工具，大大减少了系统依赖和安装体积。

**自动化程度高**。内置自动更新机制和定时任务，证书到期前自动续期，无需人工干预。

**支持多种验证方式**。提供 HTTP 验证、DNS 验证、TLS-ALPN-01 验证等多种域名验证方式，适应不同的部署环境。

**丰富的 DNS 服务商支持**。内置 100+ 家 DNS 服务商的 API 支持，包括 Cloudflare、阿里云、腾讯云、GoDaddy 等，轻松实现 DNS 验证。

**Docker 支持**。提供官方 Docker 镜像，适合容器化部署场景。

## 安装方法

### 在线安装（推荐）

使用官方提供的在线安装脚本，简单快捷：

```bash
# 使用 curl 安装
curl https://get.acme.sh | sh -s email=your@example.com

# 或使用 wget 安装
wget -O - https://get.acme.sh | sh -s email=your@example.com
```

安装过程会自动完成以下操作：
- 创建工作目录 `~/.acme.sh/`
- 安装 cron 任务用于自动更新证书
- 创建别名命令 `acme.sh`

安装完成后，重新加载 Shell 配置：

```bash
source ~/.bashrc
# 或
source ~/.zshrc
```

### 离线安装

对于无法访问外网的环境，可以离线安装：

```bash
# 1. 克隆仓库
git clone https://github.com/acmesh-official/acme.sh.git
cd acme.sh

# 2. 安装
./acme.sh --install -m your@example.com
```

### Docker 安装

使用 Docker 运行 acme.sh：

```bash
# 拉取镜像
docker pull neilpang/acme.sh

# 运行容器
docker run --rm -itd -v /path/to/certs:/acme.sh \
  -e Ali_Key=key -e Ali_Secret=secret \
  --name acme.sh neilpang/acme.sh daemon
```

### 升级 acme.sh

acme.sh 支持自动升级，也可以手动升级：

```bash
# 自动升级（通过 cron 任务）
acme.sh --upgrade

# 手动升级到最新开发版
acme.sh --upgrade -b master

# 开启自动升级
acme.sh --set-auto-upgrade 1

# 关闭自动升级
acme.sh --set-auto-upgrade 0
```

## 基础配置

### 指定证书颁发机构

acme.sh 默认使用 ZeroSSL，也可以切换到 Let's Encrypt：

```bash
# 使用 Let's Encrypt
acme.sh --set-default-ca --server letsencrypt

# 使用 ZeroSSL（默认）
acme.sh --set-default-ca --server zerossl

# 使用 Buypass
acme.sh --set-default-ca --server buypass

# 使用 Google Public Domain Registry
acme.sh --set-default-ca --server google
```

### 账户管理

```bash
# 查看当前账户信息
acme.sh --list-account

# 注册新账户（指定邮箱）
acme.sh --register-account -m your@example.com

# 切换到不同的 CA（需要重新注册）
acme.sh --set-default-ca --server letsencrypt
```

### 配置文件位置

acme.sh 的配置和证书文件存储位置：

- **主目录**: `~/.acme.sh/`
- **证书目录**: `~/.acme.sh/example.com/`
- **配置文件**: `~/.acme.sh/account.conf`
- **日志文件**: `~/.acme.sh/acme.sh.log`

## HTTP 验证方式

HTTP 验证适用于拥有 Web 服务器且 80 端口可访问的场景。

### 单域名申请

```bash
# 申请单域名证书
acme.sh --issue -d example.com -w /var/www/html

# 指定 Web 根目录
acme.sh --issue -d example.com --webroot /var/www/html
```

### 多域名和通配符申请

```bash
# 多域名（SAN 证书）
acme.sh --issue -d example.com -d www.example.com -w /var/www/html

# 通配符证书（需要使用 DNS 验证）
acme.sh --issue -d "*.example.com" --dns dns_cf
```

### Nginx 集成

acme.sh 可以自动配置 Nginx 验证：

```bash
# 自动配置 Nginx 验证
acme.sh --issue -d example.com --nginx

# 申请后安装证书到 Nginx
acme.sh --install-cert -d example.com \
  --cert-file /etc/nginx/ssl/example.com.crt \
  --key-file /etc/nginx/ssl/example.com.key \
  --fullchain-file /etc/nginx/ssl/fullchain.crt \
  --reloadcmd "nginx -s reload"
```

Nginx 配置示例：

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/nginx/ssl/fullchain.crt;
    ssl_certificate_key /etc/nginx/ssl/example.com.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # 其他配置...
}

server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

### Apache 集成

```bash
# 自动配置 Apache 验证
acme.sh --issue -d example.com --apache

# 安装证书
acme.sh --install-cert -d example.com \
  --cert-file /etc/apache2/ssl/example.com.crt \
  --key-file /etc/apache2/ssl/example.com.key \
  --fullchain-file /etc/apache2/ssl/fullchain.crt \
  --reloadcmd "systemctl reload apache2"
```

## DNS 验证方式

DNS 验证适用于申请通配符证书或无法访问 Web 服务器的场景。

### Cloudflare DNS 验证

```bash
# 1. 获取 API Token（推荐方式）
# 登录 Cloudflare Dashboard → My Profile → API Tokens
# 创建具有 "Zone:DNS:Edit" 权限的 Token

# 2. 设置环境变量
export CF_Token="your_api_token"

# 3. 申请证书
acme.sh --issue -d example.com -d "*.example.com" --dns dns_cf

# 或使用 Global Key（不推荐）
export CF_Key="your_api_key"
export CF_Email="your@email.com"
acme.sh --issue -d example.com --dns dns_cf
```

### 阿里云 DNS 验证

```bash
# 获取 AccessKey 和 Secret
# 访问 https://ram.console.aliyun.com/manage/ak

export Ali_Key="your_access_key"
export Ali_Secret="your_access_secret"

# 申请证书
acme.sh --issue -d example.com -d "*.example.com" --dns dns_ali
```

### 腾讯云 DNS 验证

```bash
# 获取 SecretId 和 SecretKey
# 访问 https://console.cloud.tencent.com/cam/capi

export DP_Id="your_secret_id"
export DP_Key="your_secret_key"

# 申请证书
acme.sh --issue -d example.com -d "*.example.com" --dns dns_dp
```

### DNSPod 验证

```bash
export DP_Id="your_id"
export DP_Key="your_key"

acme.sh --issue -d example.com --dns dns_dp
```

### GoDaddy 验证

```bash
export GD_Key="your_api_key"
export GD_Secret="your_api_secret"

acme.sh --issue -d example.com --dns dns_gd
```

### 保存 DNS 凭据

为了避免每次都设置环境变量，可以将凭据保存到配置文件：

```bash
# 方式 1: 使用 --saveaccount-conf
acme.sh --issue -d example.com --dns dns_cf --saveaccount-conf

# 方式 2: 手动编辑配置文件
nano ~/.acme.sh/account.conf

# 添加以下内容
SAVED_CF_Token='your_api_token'
SAVED_CF_Account_ID='your_account_id'
```

**安全提示**: 配置文件包含敏感信息，确保设置正确的权限：

```bash
chmod 600 ~/.acme.sh/account.conf
```

### 支持的 DNS 服务商

acme.sh 支持 100+ 家 DNS 服务商，常用服务商包括：

| 服务商 | 验证参数 |
|--------|----------|
| Cloudflare | `dns_cf` |
| 阿里云 | `dns_ali` |
| 腾讯云 | `dns_dp` |
| DNSPod | `dns_dp` |
| GoDaddy | `dns_gd` |
| Namecheap | `dns_namecheap` |
| AWS Route53 | `dns_aws` |
| Google Cloud DNS | `dns_gcloud` |
| Linode | `dns_linode` |
| DigitalOcean | `dns_dgon` |

查看完整支持列表：

```bash
acme.sh --set-default-ca --server letsencrypt --help | grep "dns_"
```

## 证书管理

### 查看已安装证书

```bash
# 列出所有证书
acme.sh --list

# 查看证书详细信息
acme.sh --info -d example.com
```

### 安装证书到指定位置

```bash
acme.sh --install-cert -d example.com \
  --cert-file /path/to/cert.crt \
  --key-file /path/to/cert.key \
  --fullchain-file /path/to/fullchain.crt \
  --ca-file /path/to/ca.crt \
  --reloadcmd "service nginx reload"
```

参数说明：
- `--cert-file`: 域名证书
- `--key-file`: 私钥文件
- `--fullchain-file`: 完整证书链（包含中间证书）
- `--ca-file`: CA 根证书
- `--reloadcmd`: 安装后执行的命令

### 更新证书

acme.sh 默认会在证书到期前 30 天自动更新，也可以手动更新：

```bash
# 强制更新证书
acme.sh --renew -d example.com --force

# 更新所有证书
acme.sh --renew-all --force
```

### 撤销证书

```bash
# 撤销证书
acme.sh --revoke -d example.com

# 删除证书（从本地移除）
acme.sh --remove -d example.com
```

### 设置自动更新

acme.sh 安装时会自动创建 cron 任务：

```bash
# 查看 cron 任务
crontab -l | grep acme.sh

# 示例输出
# 0 0 * * * "/home/user/.acme.sh"/acme.sh --cron --home "/home/user/.acme.sh" > /dev/null
```

自定义更新时间：

```bash
# 编辑 crontab
crontab -e

# 添加自定义任务（如每天凌晨 2 点更新）
0 2 * * * "/home/user/.acme.sh"/acme.sh --cron --home "/home/user/.acme.sh" > /dev/null
```

## 高级功能

### ECC 证书

ECC（椭圆曲线加密）证书相比传统 RSA 证书具有更小的密钥尺寸和更高的性能：

```bash
# 申请 ECC 证书
acme.sh --issue -d example.com --keylength ec-256

# 申请 ECC 证书（更长的密钥）
acme.sh --issue -d example.com --keylength ec-384

# 安装 ECC 证书
acme.sh --install-cert -d example.com --ecc \
  --cert-file /etc/nginx/ssl/ecc.crt \
  --key-file /etc/nginx/ssl/ecc.key \
  --fullchain-file /etc/nginx/ssl/ecc.fullchain.crt \
  --reloadcmd "nginx -s reload"
```

支持的密钥长度：
- `ec-256`: prime256v1（推荐）
- `ec-384`: secp384r1
- `2048`: RSA 2048 位（默认）
- `3072`: RSA 3072 位
- `4096`: RSA 4096 位

### 多级 SAN 证书

```bash
# 添加多个域名到证书
acme.sh --issue -d example.com \
  -d www.example.com \
  -d api.example.com \
  -d cdn.example.com \
  -w /var/www/html
```

### 泛域名证书

```bash
# 单级泛域名
acme.sh --issue -d "*.example.com" --dns dns_cf

# 多级泛域名（需要多次申请）
acme.sh --issue -d "*.example.com" -d "*.sub.example.com" --dns dns_cf
```

### 混合验证方式

同时使用 HTTP 和 DNS 验证：

```bash
acme.sh --issue -d example.com -d "*.example.com" \
  --webroot /var/www/html \
  --dns dns_cf
```

### 强制更新和调试

```bash
# 强制重新申请证书
acme.sh --renew -d example.com --force

# 启用调试模式
acme.sh --issue -d example.com -w /var/www/html --debug

# 更详细的调试输出
acme.sh --issue -d example.com -w /var/www/html --debug 2
```

### 使用 ACME v2

Let's Encrypt 的 ACME v2 协议支持通配符证书：

```bash
# 指定使用 ACME v2 服务器
acme.sh --server https://acme-v02.api.letsencrypt.org/directory \
  --issue -d "*.example.com" --dns dns_cf

# 或使用简写
acme.sh --issue -d "*.example.com" --dns dns_cf --server letsencrypt
```

## 实战场景

### 自动化 Nginx SSL 部署

完整流程：申请证书 → 安装证书 → 配置 Nginx → 自动更新

```bash
# 1. 申请证书（HTTP 验证）
acme.sh --issue -d example.com -d www.example.com \
  -w /var/www/html --force

# 2. 安装证书
acme.sh --install-cert -d example.com \
  --cert-file /etc/nginx/ssl/example.com.crt \
  --key-file /etc/nginx/ssl/example.com.key \
  --fullchain-file /etc/nginx/ssl/fullchain.crt \
  --reloadcmd "nginx -s reload"

# 3. 配置 Nginx
cat > /etc/nginx/conf.d/example.conf << 'EOF'
server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    ssl_certificate /etc/nginx/ssl/fullchain.crt;
    ssl_certificate_key /etc/nginx/ssl/example.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    root /var/www/html;
    index index.html;
}

server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$server_name$request_uri;
}
EOF

# 4. 测试并重载配置
nginx -t && nginx -s reload

# 5. 验证证书
curl -I https://example.com
```

### 负载均衡环境证书部署

在多台负载均衡服务器上部署证书：

```bash
# 在主服务器上申请证书
acme.sh --issue -d example.com --dns dns_cf

# 安装证书并同步到其他服务器
acme.sh --install-cert -d example.com \
  --cert-file /etc/nginx/ssl/example.com.crt \
  --key-file /etc/nginx/ssl/example.com.key \
  --fullchain-file /etc/nginx/ssl/fullchain.crt \
  --reloadcmd "
    scp /etc/nginx/ssl/*.crt user@server2:/etc/nginx/ssl/
    scp /etc/nginx/ssl/*.key user@server2:/etc/nginx/ssl/
    ssh user@server2 'nginx -s reload'
    nginx -s reload
  "
```

### Docker 容器 SSL 证书

为 Docker 容器提供 SSL 证书：

```bash
# 1. 申请证书
acme.sh --issue -d example.com --dns dns_cf

# 2. 安装证书到共享目录
acme.sh --install-cert -d example.com \
  --cert-file /docker/certs/example.com.crt \
  --key-file /docker/certs/example.com.key \
  --fullchain-file /docker/certs/fullchain.crt \
  --reloadcmd "docker restart nginx-container"

# 3. Docker Compose 配置
cat > docker-compose.yml << 'EOF'
version: '3'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - /docker/certs:/etc/nginx/ssl:ro
      - ./html:/usr/share/nginx/html
    restart: unless-stopped
EOF

# 4. 启动容器
docker-compose up -d
```

### 证书监控和告警

```bash
#!/bin/bash
# 证书过期监控脚本

# 配置
DOMAINS=("example.com" "api.example.com" "cdn.example.com")
ALERT_DAYS=30
EMAIL="admin@example.com"

for domain in "${DOMAINS[@]}"; do
    # 获取证书过期时间
    exp_date=$(openssl s_client -connect $domain:443 -servername $domain 2>/dev/null \
      | openssl x509 -noout -enddate | cut -d= -f2)

    # 转换为时间戳
    exp_epoch=$(date -d "$exp_date" +%s)
    now_epoch=$(date +%s)
    days_left=$(( ($exp_epoch - $now_epoch) / 86400 ))

    if [ $days_left -lt $ALERT_DAYS ]; then
        echo "警告: $domain 证书将在 $days_left 天后过期" | \
          mail -s "SSL 证书过期告警" $EMAIL
    fi
done
```

### 批量证书管理

```bash
#!/bin/bash
# 批量申请证书脚本

# 域名列表
declare -A domains=(
    ["example.com"]="dns_cf"
    ["myapp.com"]="dns_ali"
    ["test.io"]="dns_dp"
)

# 遍历申请证书
for domain in "${!domains[@]}"; do
    dns_provider="${domains[$domain]}"
    echo "正在为 $domain 申请证书（$dns_provider）..."

    acme.sh --issue -d "$domain" -d "*.$domain" \
      --dns "$dns_provider" \
      --keylength ec-256 \
      --force

    if [ $? -eq 0 ]; then
        echo "$domain 证书申请成功"
    else
        echo "$domain 证书申请失败"
    fi
done
```

## 安全最佳实践

### 私钥保护

```bash
# 设置严格的文件权限
chmod 600 /etc/nginx/ssl/*.key
chown root:root /etc/nginx/ssl/*.key

# 确保证书目录权限正确
chmod 755 /etc/nginx/ssl
chown root:root /etc/nginx/ssl
```

### 定期更新证书

```bash
# 查看证书到期时间
acme.sh --list

# 手动测试续期
acme.sh --renew -d example.com --force --dry-run
```

### 使用强加密套件

Nginx 配置推荐：

```nginx
# 仅支持 TLS 1.2 和 1.3
ssl_protocols TLSv1.2 TLSv1.3;

# 使用强加密套件
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;

# 启用 OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
ssl_trusted_certificate /etc/nginx/ssl/ca.crt;

# 设置 DH 参数
ssl_dhparam /etc/nginx/ssl/dhparam.pem;

# 生成 DH 参数
openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048
```

### 配置 HSTS

```nginx
# 启用 HSTS（强制使用 HTTPS）
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
```

### 备份证书

```bash
#!/bin/bash
# 证书备份脚本

BACKUP_DIR="/backup/ssl/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

# 复制证书文件
cp -r /etc/nginx/ssl/* "$BACKUP_DIR/"

# 备份 acme.sh 配置
cp -r ~/.acme.sh "$BACKUP_DIR/"

# 压缩备份
tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR"
rm -rf "$BACKUP_DIR"

# 保留最近 30 天的备份
find /backup/ssl -name "*.tar.gz" -mtime +30 -delete
```

## 故障排查

### 常见问题

**问题 1: DNS 验证失败**

```bash
# 检查 DNS 记录是否生效
dig _acme-challenge.example.com TXT

# 查看 acme.sh 日志
tail -f ~/.acme.sh/acme.sh.log

# 手动添加 TXT 记录测试
acme.sh --issue -d example.com --dns --dns-manual-mode
```

**问题 2: HTTP 验证失败**

```bash
# 检查 Web 根目录权限
ls -la /var/www/html/

# 测试访问验证文件
curl http://example.com/.well-known/acme-challenge/test

# 检查防火墙规则
sudo ufw status
sudo iptables -L -n | grep 80
```

**问题 3: 证书安装失败**

```bash
# 检查目录是否存在
ls -ld /etc/nginx/ssl/

# 检查文件权限
stat /etc/nginx/ssl/example.com.key

# 手动测试重载命令
sudo nginx -t
sudo nginx -s reload
```

**问题 4: Cron 任务未执行**

```bash
# 检查 cron 任务
crontab -l

# 查看 cron 日志
grep CRON /var/log/syslog

# 手动运行 cron 任务
"/home/user/.acme.sh/acme.sh" --cron --home "/home/user/.acme.sh"
```

### 调试模式

```bash
# 启用调试输出
acme.sh --issue -d example.com -w /var/www/html --debug

# 更详细的调试（级别 2）
acme.sh --issue -d example.com -w /var/www/html --debug 2

# 查看完整日志
tail -100 ~/.acme.sh/acme.sh.log
```

### 性能优化

```bash
# 使用 ECC 证书减少握手时间
acme.sh --issue -d example.com --keylength ec-256

# 启用 HTTP/2 提高性能
# 在 Nginx 配置中添加
listen 443 ssl http2;

# 使用 OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
```

## 与其他工具集成

### Systemd 服务

创建 systemd 服务管理 acme.sh：

```bash
# 创建服务文件
sudo nano /etc/systemd/system/acme-sh.service
```

```ini
[Unit]
Description=ACME.sh SSL Certificate Renewal
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/home/user/.acme.sh/acme.sh --cron --home /home/user/.acme.sh
User=user
Group=user

[Install]
WantedBy=multi-user.target
```

```bash
# 创建定时器
sudo nano /etc/systemd/system/acme-sh.timer
```

```ini
[Unit]
Description=ACME.sh SSL Certificate Renewal Timer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
# 启用服务
sudo systemctl enable --now acme-sh.timer
sudo systemctl status acme-sh.timer
```

### 与 CI/CD 集成

在 CI/CD 流水线中自动更新证书：

```yaml
# .gitlab-ci.yml 示例
stages:
  - ssl_renew
  - deploy

ssl_renew:
  stage: ssl_renew
  script:
    - curl https://get.acme.sh | sh
    - ~/.acme.sh/acme.sh --issue -d $DOMAIN --dns dns_cf
    - ~/.acme.sh/acme.sh --install-cert -d $DOMAIN --reloadcmd "true"
  artifacts:
    paths:
      - ~/.acme.sh/$DOMAIN/
    expire_in: 1 week

deploy:
  stage: deploy
  dependencies:
    - ssl_renew
  script:
    - scp ~/.acme.sh/$DOMAIN/*.crt $SERVER:/etc/nginx/ssl/
    - ssh $SERVER "nginx -s reload"
  only:
    - main
```

### 监控集成

使用 Prometheus 监控证书状态：

```bash
#!/bin/bash
# 证书到期监控 exporter

# 输出 Prometheus 格式指标
echo "# HELP ssl_certificate_days_until_expiry Days until SSL certificate expires"
echo "# TYPE ssl_certificate_days_until_expiry gauge"

for domain in example.com www.example.com; do
    exp_date=$(date -d "$(openssl s_client -connect $domain:443 -servername $domain 2>/dev/null |
      openssl x509 -noout -enddate | cut -d= -f2)" +%s)
    now_epoch=$(date +%s)
    days_left=$(( ($exp_date - $now_epoch) / 86400 ))

    echo "ssl_certificate_days_until_expiry{domain=\"$domain\"} $days_left"
done
```

## 对比其他方案

### acme.sh vs certbot

| 特性 | acme.sh | certbot |
|------|---------|---------|
| 依赖 | 仅 Shell | Python |
| 安装大小 | 极小 (~200KB) | 较大 (~50MB) |
| 通配符证书 | 支持 | 支持 |
| DNS 服务商 | 100+ | 有限 |
| Docker 支持 | 官方镜像 | 官方镜像 |
| 性能 | 更快 | 较慢 |
| 配置复杂度 | 简单 | 较复杂 |

### 选择建议

- **选择 acme.sh**: 追求轻量级、需要支持多种 DNS 服务商、容器化部署
- **选择 certbot**: 已经在使用、习惯 Python 生态、需要官方支持

## 最佳实践

### 自动化优先

手动管理证书容易出错且容易忘记更新。建立完善的自动化流程：

- 使用 cron 或 systemd 定时器自动更新证书
- 配置自动重载 Web 服务
- 设置证书过期监控告警

### 安全加固

- 使用 ECC 证书提升性能和安全性
- 启用 HSTS 防止降级攻击
- 定期轮换 API 凭据
- 限制证书文件访问权限

### 云原生部署

在 Kubernetes 环境中，考虑使用 cert-manager 等专用工具：

```yaml
# 使用 cert-manager 自动管理证书
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    solvers:
    - dns01:
        cloudflare:
          email: your@email.com
          apiTokenSecretRef:
            name: cloudflare-token
            key: api-token
```

## 总结

acme.sh 是一款功能强大、轻量级且易于使用的 SSL 证书管理工具。通过掌握其核心功能和高级特性，可以构建完全自动化的证书管理体系。

关键要点：

- 支持多种验证方式，适应不同部署环境
- 内置 100+ DNS 服务商支持，轻松实现 DNS 验证
- 自动更新机制，无需担心证书过期
- 纯 Shell 实现，无额外依赖
- 丰富的部署场景支持

证书管理是保障网站安全的基础工作，使用 acme.sh 可以大幅简化这一过程，让 HTTPS 部署变得简单高效。

## 参考资源

- acme.sh 官方文档: https://github.com/acmesh-official/acme.sh
- Let's Encrypt 文档: https://letsencrypt.org/docs/
- SSL Labs 测试工具: https://www.ssllabs.com/ssltest/
- Mozilla SSL 配置生成器: https://ssl-config.mozilla.org/
- ACME 协议规范: https://datatracker.ietf.org/doc/html/rfc8555

通过系统学习和实践 acme.sh，你将能够构建可靠的 SSL 证书自动化管理体系，为网站提供安全、高效的 HTTPS 服务。
