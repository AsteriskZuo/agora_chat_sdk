#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import shutil
import time

def filter_language(file_path, language):
    """
    逐行处理，只保留目标语言的内容块，支持注释符号
    """
    if not os.path.exists(file_path):
        return
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        new_lines = []
        keep = True  # 默认保留内容
        in_block = False
        target_flag = f'~{language}'
        other_flag = '~chinese' if language == 'english' else '~english'
        for i, line in enumerate(lines):
            line_strip = line.strip()
            # 进入目标语言块
            if line_strip.endswith(target_flag):
                keep = True
                in_block = True
                continue  # 不保留~english/~chinese标记本身
            # 进入非目标语言块
            elif line_strip.endswith(other_flag):
                keep = False
                in_block = True
                continue
            # 结束语言块
            elif line_strip.endswith('~end'):
                in_block = False
                keep = True
                continue
            # 只保留目标语言块内容
            if keep and in_block:
                new_lines.append(line)
            # 语言块外的内容全部保留
            if not in_block and not (line_strip.endswith('~end') or line_strip.endswith('~english') or line_strip.endswith('~chinese')):
                new_lines.append(line)
        new_content = ''.join(new_lines)
        if new_content != ''.join(lines):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"已更新: {file_path}")
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")

def process_directory(directory, language):
    """
    递归处理目录中的所有文件，只处理含有~english和~chinese的文件
    """
    total_files = 0
    processed_files = 0
    updated_files = 0
    candidate_files = []
    # 先统计所有候选文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.dart', '.java', '.m', '.h', '.mm', '.cpp')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if '~english' in content and '~chinese' in content:
                            candidate_files.append(file_path)
                except Exception as e:
                    print(f"跳过无法读取的文件: {file_path}，原因: {e}")
    total_files = len(candidate_files)
    print(f"找到 {total_files} 个包含多语言内容的文件")
    # 处理候选文件
    for idx, file_path in enumerate(candidate_files, 1):
        print(f"[{idx}/{total_files}] 处理文件: {file_path}")
        before_mtime = os.path.getmtime(file_path) if os.path.exists(file_path) else 0
        filter_language(file_path, language)
        if os.path.exists(file_path) and before_mtime != os.path.getmtime(file_path):
            updated_files += 1
    print(f"\n处理完成: 共处理 {total_files} 个文件，更新了 {updated_files} 个文件")

def create_backup(path):
    """
    在原目录同级创建 目录名_时间戳 备份
    """
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    if os.path.isdir(path):
        src_dir = os.path.abspath(path)
    else:
        src_dir = os.path.dirname(os.path.abspath(path))
    parent_dir = os.path.dirname(src_dir)
    base_name = os.path.basename(src_dir.rstrip(os.sep))
    backup_dir = os.path.join(parent_dir, f"{base_name}_{timestamp}")
    try:
        shutil.copytree(src_dir, backup_dir, dirs_exist_ok=True)
        print(f"已创建备份: {backup_dir}")
        return True
    except Exception as e:
        print(f"创建备份失败: {str(e)}")
        return False

def print_help():
    """
    打印帮助信息
    """
    print("""
语言过滤工具 - 用于过滤API参考文档中的多语言内容

用法: python language.py [english|chinese] [目录路径(可选)]

参数:
  english|chinese    指定要保留的语言
  目录路径          可选，指定要处理的目录路径，默认为当前目录

示例:
  python language.py english            # 保留英文内容，处理当前目录
  python language.py chinese ./lib      # 保留中文内容，处理./lib目录
  
注意:
  - 此工具会修改源文件，建议在使用前创建备份
  - 只处理.dart、.java、.m、.h、.mm和.cpp文件
  - 文件中必须包含~english和~chinese标记才会被处理
    """)

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print_help()
        sys.exit(1)
    
    if sys.argv[1] in ['-h', '--help', 'help']:
        print_help()
        sys.exit(0)
    
    language = sys.argv[1].lower()
    if language not in ['english', 'chinese']:
        print("错误: 语言必须是 'english' 或 'chinese'")
        print_help()
        sys.exit(1)
    
    # 获取处理路径
    if len(sys.argv) == 3:
        path = sys.argv[2]
        if not os.path.exists(path):
            print(f"指定的路径不存在: {path}")
            sys.exit(1)
    else:
        path = os.getcwd()
    
    # 构造输出目录
    out_root = os.path.join(os.getcwd(), language)
    if not os.path.exists(out_root):
        os.makedirs(out_root)
    if os.path.isdir(path):
        src_dir = os.path.abspath(path)
        dst_dir = os.path.join(out_root, os.path.basename(src_dir.rstrip(os.sep)))
        if os.path.exists(dst_dir):
            print(f"目标目录已存在: {dst_dir}，请先删除或更换输出目录")
            sys.exit(1)
        print(f"正在拷贝 {src_dir} 到 {dst_dir} ...")
        shutil.copytree(src_dir, dst_dir)
        print(f"拷贝完成，开始处理 {language} 语言过滤 ...")
        process_directory(dst_dir, language)
    else:
        # 单文件处理，拷贝其父目录
        src_file = os.path.abspath(path)
        src_dir = os.path.dirname(src_file)
        dst_dir = os.path.join(out_root, os.path.basename(src_dir.rstrip(os.sep)))
        if os.path.exists(dst_dir):
            print(f"目标目录已存在: {dst_dir}，请先删除或更换输出目录")
            sys.exit(1)
        print(f"正在拷贝 {src_dir} 到 {dst_dir} ...")
        shutil.copytree(src_dir, dst_dir)
        print(f"拷贝完成，开始处理 {language} 语言过滤 ...")
        # 只处理新目录下的同名文件
        dst_file = os.path.join(dst_dir, os.path.basename(src_file))
        filter_language(dst_file, language)
    print("处理完成! 原目录未做任何修改。")

if __name__ == "__main__":
    main() 