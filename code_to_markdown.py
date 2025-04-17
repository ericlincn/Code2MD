import os
import argparse
from pathlib import Path

def generate_directory_tree(root_path, exclude_dirs=None, max_depth=None, current_depth=0):
    """生成目录结构树，支持排除目录和深度控制"""
    if exclude_dirs is None:
        exclude_dirs = []
    
    prefix = "    " * current_depth + "├── "
    tree = []
    
    for item in sorted(os.listdir(root_path)):
        item_path = os.path.join(root_path, item)
        if item in exclude_dirs:
            continue
        
        if os.path.isdir(item_path):
            tree.append(f"{prefix}{item}/")
            if max_depth is None or current_depth < max_depth:
                subtree = generate_directory_tree(
                    item_path, exclude_dirs, max_depth, current_depth + 1
                )
                tree.extend(subtree)
        else:
            tree.append(f"{prefix}{item}")
    
    return tree

def read_file_content(file_path):
    """读取文件内容并返回Markdown代码块格式"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return f"```{Path(file_path).suffix[1:]}\n{content}\n```"

def generate_markdown(root_path, recursive=True, exclude_dirs=None, extensions=None):
    """生成完整的Markdown文档"""
    if exclude_dirs is None:
        exclude_dirs = []
    if extensions is None:
        extensions = [".py", ".js", ".html", ".css", ".md"]  # 默认包含的扩展名
    
    markdown = ["# 项目代码结构\n\n## 目录结构\n"]
    
    # 生成目录树
    max_depth = None if recursive else 0
    tree = generate_directory_tree(root_path, exclude_dirs, max_depth)
    markdown.append("\n".join(tree))
    
    # 遍历文件并添加代码
    markdown.append("\n\n## 文件代码\n")
    for root, dirs, files in os.walk(root_path):
        # 跳过排除的目录
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, root_path)
                markdown.append(f"\n### `{relative_path}`\n")
                try:
                    markdown.append(read_file_content(file_path))
                except UnicodeDecodeError:
                    markdown.append("```\n(二进制文件或编码不支持)\n```")
    
    return "\n".join(markdown)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成项目代码的Markdown文档")
    parser.add_argument("root_dir", help="目标文件夹路径")
    parser.add_argument("--non-recursive", action="store_true", help="不遍历子文件夹")
    parser.add_argument("--exclude-dirs", nargs="+", default=[], help="排除的文件夹名称（如 node_modules）")
    parser.add_argument("--extensions", nargs="+", default=[".py", ".js", ".html", ".css", ".md"], help="包含的文件扩展名")
    args = parser.parse_args()

    markdown_content = generate_markdown(
        args.root_dir,
        recursive=not args.non_recursive,
        exclude_dirs=args.exclude_dirs,
        extensions=args.extensions
    )
    
    output_path = os.path.join(args.root_dir, "CODE_REPORT.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    print(f"Markdown文档已生成: {output_path}")