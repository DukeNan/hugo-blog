---
title: "通过 Digest 查找 Docker Hub 镜像对应的 Tag" # Title of the blog post.
date: 2026-01-12T17:08:05+08:00 # Date of post creation.
description: "介绍如何通过本地 Docker 镜像的 digest 值，在 Docker Hub 上找到对应的 tag 名称。" # Description used for search engine.
author: "shaun"
featured: false # Sets if post is a featured post, making appear on the home page side bar.
draft: false # Sets whether to render this page. Draft of true will not be rendered.
usePageBundles: false # Set to true to group assets like images in the same folder as this post.
# featureImage: "/images/path/file.jpg" # Sets featured image on blog post.
# featureImageAlt: 'Description of image' # Alternative text for featured image.
# featureImageCap: 'This is the featured image.' # Caption (optional).
# thumbnail: "/images/path/thumbnail.png" # Sets thumbnail image appearing inside card on homepage.
# shareImage: "/images/path/share.png" # Designate a separate image for social media sharing.
codeMaxLines: 10 # Override global value for how many lines within a code block before auto-collapsing.
codeLineNumbers: true # Override global value for showing of line numbers within code block.
figurePositionShow: true # Override global value for showing the figure label.
categories:
  - Technology
tags:
  - docker
# comment: false # Disable comment if false.
---

在日常使用 Docker 时，我们可能会遇到这样一个场景：本地有一个镜像（比如 `n8nio/n8n:latest`），但我们想知道这个镜像具体对应 Docker Hub 上的哪个版本 tag。因为 `latest` 标签只是指向最新的版本，它实际上对应的是一个具体的版本号（如 `1.0.0`、`1.2.3` 等）。本文将介绍如何通过镜像的 digest 值来找到对应的 tag。

## 什么是 Digest？

Docker 镜像的 digest 是镜像内容的 SHA256 哈希值，它是镜像的唯一标识符。每个镜像层和整个镜像都有一个 digest 值。当你拉取一个镜像时，Docker 会计算并验证这个 digest 值来确保镜像的完整性。

## 获取本地镜像的 Digest

### 方法一：使用 docker images 命令

```shell
docker images --digests n8nio/n8n
```

输出示例：

```
REPOSITORY   TAG       DIGEST                                                                    IMAGE ID       CREATED        SIZE
n8nio/n8n    latest    sha256:4a43ddf853afe3ad44be51379e7ed85c16b974cae26cf732d2fcbf71d0cb16c4   3f0c599d2f20   2 months ago   976MB
```

### 方法二：使用 docker image inspect 命令

```shell
docker image inspect n8nio/n8n:latest --format '{{json .RepoDigests}}'
```

输出示例：

```json
["n8nio/n8n@sha256:4a43ddf853afe3ad44be51379e7ed85c16b974cae26cf732d2fcbf71d0cb16c4"]
```

## 在 Docker Hub 上查找对应的 Tag

Docker Hub 提供了 REST API 可以查询仓库的 tags 信息。我们可以通过 API 遍历所有 tags，找到与 digest 匹配的那个。

### 使用 Python 脚本查询

以下是一个 Python 脚本，可以通过 digest 查找对应的 tag：

{{< code lang="python" file="assets/code/python/filter_digest.py" >}}

### 使用方法

1. 修改脚本中的 `namespace`、`repository` 和 `digest` 值
2. 运行脚本：`python filter_digest.py`
3. 脚本会返回匹配的 tag 信息，包括 tag 名称、创建时间、镜像大小等

### 输出示例

```json
{
    "creator": 6760745,
    "id": 1008109846,
    "images": [
        {
            "architecture": "amd64",
            "features": "",
            "variant": null,
            "digest": "sha256:aeb609a4ee36f843118496ff82a2f0471027ad1f159d14c9364ee4f0d0dbd9b2",
            "os": "linux",
            "os_features": "",
            "os_version": null,
            "size": 270889921,
            "status": "active",
            "last_pulled": "2026-01-12T09:08:21.390357865Z",
            "last_pushed": "2025-11-10T13:47:33.102355622Z"
        },
        {
            "architecture": "unknown",
            "features": "",
            "variant": null,
            "digest": "sha256:f97ff58cd8d2cb708b010aa7e912c74bb07b7daa822475cb84e1ef919cb053f9",
            "os": "unknown",
            "os_features": "",
            "os_version": null,
            "size": 5808118,
            "status": "active",
            "last_pulled": "2026-01-12T03:02:58.181134728Z",
            "last_pushed": "2025-11-10T13:47:33.809553789Z"
        },
        {
            "architecture": "arm64",
            "features": "",
            "variant": null,
            "digest": "sha256:27bc4f914e832d9e9f5cea9c99aa435ddc138d8d53e5fce0b546e87bad1c724d",
            "os": "linux",
            "os_features": "",
            "os_version": null,
            "size": 268893252,
            "status": "active",
            "last_pulled": "2026-01-12T04:59:23.566476676Z",
            "last_pushed": "2025-11-10T14:15:55.642541647Z"
        },
        {
            "architecture": "unknown",
            "features": "",
            "variant": null,
            "digest": "sha256:fcb488078ed35fb99255c30fd0930240b5771045148aea97eeace65674f7c12c",
            "os": "unknown",
            "os_features": "",
            "os_version": null,
            "size": 5808259,
            "status": "active",
            "last_pulled": "2026-01-09T15:42:03.74659943Z",
            "last_pushed": "2025-11-10T14:15:56.424887489Z"
        }
    ],
    "last_updated": "2025-11-10T14:19:44.292916Z",
    "last_updater": 6760745,
    "last_updater_username": "n8nio",
    "name": "1.119.1",
    "repository": 7303950,
    "full_size": 270889921,
    "v2": true,
    "tag_status": "active",
    "tag_last_pulled": "2026-01-12T09:08:21.390357865Z",
    "tag_last_pushed": "2025-11-10T14:19:44.292916Z",
    "media_type": "application/vnd.oci.image.index.v1+json",
    "content_type": "image",
    "digest": "sha256:4a43ddf853afe3ad44be51379e7ed85c16b974cae26cf732d2fcbf71d0cb16c4"
}
```

## 使用场景

这个技巧在以下场景中特别有用：

1. **版本追踪**：当你本地有一个旧版本的镜像，想知道它对应的版本号
2. **安全审计**：确认本地镜像的具体版本，用于安全漏洞排查
3. **CI/CD 调试**：在构建流程中验证拉取的镜像版本是否正确
4. **多架构支持**：查找不同架构（如 amd64、arm64）的镜像对应的 tag

## 总结

通过 digest 查找 Docker Hub 上的 tag 是一个简单但实用的技巧。它可以帮助我们更好地管理 Docker 镜像，特别是在需要精确知道镜像版本信息的场景下。结合 Docker Hub API 和简单的脚本，我们可以轻松实现这个功能。
