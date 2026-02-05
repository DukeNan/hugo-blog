#!/bin/bash
# 网络连接测试脚本

HOSTS=(
    "8.8.8.8"
    "1.1.1.1"
    "baidu.com"
    "google.com"
)

ping_host() {
    local host=$1
    echo -n "测试 $host ... "
    
    if ping -c 1 -W 2 "$host" &>/dev/null; then
        echo "✓ 成功"
        return 0
    else
        echo "✗ 失败"
        return 1
    fi
}

main() {
    echo "=== 网络连接测试 ==="
    echo ""
    
    success=0
    total=${#HOSTS[@]}
    
    for host in "${HOSTS[@]}"; do
        if ping_host "$host"; then
            ((success++))
        fi
    done
    
    echo ""
    echo "测试结果: $success/$total 成功"
}

main
