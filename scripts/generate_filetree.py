#!/usr/bin/env python3
"""
文件树生成器 - 自动扫描 assets/code/ 目录并生成 YAML 索引
用于 Hugo autotree shortcode
"""

import os
import sys
import io
import yaml
from pathlib import Path
from typing import List, Dict, Tuple

# 确保标准输出使用 UTF-8 编码，避免终端编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 文件扩展名到语言类型的映射
LANG_MAP = {
    '.sh': 'bash',
    '.py': 'python',
    '.js': 'javascript',
    '.go': 'go',
    '.txt': 'text',
    '.json': 'json',
    '.yaml': 'yaml',
    '.yml': 'yaml',
    '.toml': 'toml',
    '.md': 'markdown',
    '.html': 'html',
    '.css': 'css',
    '.rs': 'rust',
    '.java': 'java',
    '.c': 'c',
    '.cpp': 'cpp',
    '.h': 'c',
    '.hpp': 'cpp',
    '.sql': 'sql',
    '.xml': 'xml',
    '.dockerfile': 'dockerfile',
}


def get_language(filename: str) -> str:
    """根据文件扩展名获取语言类型"""
    ext = Path(filename).suffix.lower()
    if filename.lower() == 'dockerfile':
        return 'dockerfile'
    return LANG_MAP.get(ext, 'text')


def build_tree_structure(base_path: Path, root_path: Path, prefix: str = "", is_last: bool = True) -> Tuple[List[str], List[Dict]]:
    """
    递归构建目录树结构
    base_path: 当前处理的目录
    root_path: 根目录（用于计算相对路径）
    返回: (树形字符串列表, 文件信息列表)
    """
    tree_lines = []
    file_list = []

    try:
        items = sorted(base_path.iterdir(), key=lambda x: (not x.is_file(), x.name.lower()))
    except PermissionError:
        return tree_lines, file_list

    for index, item in enumerate(items):
        is_last_item = index == len(items) - 1

        # 构建树形字符的前缀
        connector = "└── " if is_last_item else "├── "

        if item.is_file():
            # 添加文件到树结构
            tree_lines.append(f"{prefix}{connector}{item.name}")

            # 添加文件信息到列表
            # 相对于 assets/ 的路径（用于 readFile）
            rel_path = item.relative_to(root_path.parent.parent)
            # 相对于当前目录的路径（用于显示）
            rel_name = item.relative_to(root_path)
            file_list.append({
                'path': str(rel_path).replace('\\', '/'),
                'name': str(rel_name).replace('\\', '/'),
                'lang': get_language(item.name)
            })
        elif item.is_dir():
            # 添加目录到树结构
            tree_lines.append(f"{prefix}{connector}{item.name}/")

            # 递归处理子目录
            new_prefix = prefix + ("    " if is_last_item else "│   ")
            sub_tree, sub_files = build_tree_structure(item, root_path, new_prefix, is_last_item)
            tree_lines.extend(sub_tree)
            file_list.extend(sub_files)

    return tree_lines, file_list


def generate_filetree_data(base_dir: Path, output_dir: Path):
    """
    扫描 base_dir 下的所有子目录，为每个子目录生成 YAML 文件
    """
    if not base_dir.exists():
        print(f"错误: 目录不存在 - {base_dir}")
        return

    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)

    # 遍历所有子目录
    subdirs = [d for d in base_dir.iterdir() if d.is_dir()]

    if not subdirs:
        print(f"警告: {base_dir} 下没有找到子目录")
        return

    for subdir in subdirs:
        dir_name = subdir.name
        print(f"处理目录: {dir_name}")

        # 构建树形结构和文件列表
        tree_lines, file_list = build_tree_structure(subdir, subdir)

        if not file_list:
            print(f"  警告: {dir_name} 目录为空，跳过")
            continue

        # 构建完整的树形结构字符串
        tree_header = f"{dir_name}/"
        tree_content = tree_header + "\n" + "\n".join(tree_lines) if tree_lines else tree_header

        # 构建 YAML 数据
        data = {
            'name': dir_name,
            'tree': tree_content,
            'files': file_list
        }

        # 写入 YAML 文件
        output_file = output_dir / f"{dir_name}.yaml"
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        print(f"  ✓ 生成: {output_file} ({len(file_list)} 个文件)")


def main():
    """主函数"""
    # 获取项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # 定义路径
    assets_code_dir = project_root / "assets" / "code"
    data_output_dir = project_root / "data" / "filetrees"

    print("=" * 60)
    print("文件树生成器")
    print("=" * 60)
    print(f"扫描目录: {assets_code_dir}")
    print(f"输出目录: {data_output_dir}")
    print("-" * 60)

    # 生成文件树数据
    generate_filetree_data(assets_code_dir, data_output_dir)

    print("-" * 60)
    print("✓ 完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
