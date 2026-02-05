#!/bin/bash
# 文件系统操作脚本示例

# 检查磁盘使用情况
check_disk_usage() {
    echo "=== 磁盘使用情况 ==="
    df -h | grep -v tmpfs
}

# 查找大文件
find_large_files() {
    local size=${1:-100M}
    echo "=== 查找大于 $size 的文件 ==="
    find / -type f -size +$size 2>/dev/null | head -20
}

# 清理临时文件
clean_temp_files() {
    echo "=== 清理临时文件 ==="
    rm -rf /tmp/*
    echo "临时文件清理完成"
}

# 主函数
main() {
    check_disk_usage
    echo ""
    find_large_files "100M"
}

main "$@"
