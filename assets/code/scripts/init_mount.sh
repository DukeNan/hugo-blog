#!/bin/bash
# 挂载初始化脚本

set -e

MOUNT_POINT="/mnt/data"
DEVICE="/dev/sdb1"

# 检查设备是否存在
check_device() {
    if [ ! -b "$DEVICE" ]; then
        echo "错误: 设备 $DEVICE 不存在"
        exit 1
    fi
    echo "设备 $DEVICE 检查通过"
}

# 创建挂载点
create_mount_point() {
    if [ ! -d "$MOUNT_POINT" ]; then
        mkdir -p "$MOUNT_POINT"
        echo "创建挂载点: $MOUNT_POINT"
    fi
}

# 挂载设备
mount_device() {
    if mountpoint -q "$MOUNT_POINT"; then
        echo "设备已经挂载在 $MOUNT_POINT"
    else
        mount "$DEVICE" "$MOUNT_POINT"
        echo "成功挂载 $DEVICE 到 $MOUNT_POINT"
    fi
}

# 主函数
main() {
    check_device
    create_mount_point
    mount_device
    echo "挂载完成!"
}

main
