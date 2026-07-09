#!/usr/bin/env python3
"""code_to_markdown.py — 将源代码目录/文件转换为格式化 Markdown 文档"""

import os
import argparse
from pathlib import Path

COMMON_EXCLUDE_DIRS = {
    '.git', '.svn', '.hg',
    '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache',
    'node_modules', 'bower_components', 'jspm_packages',
    '.venv', 'venv', 'env', '.env', 'virtualenv',
    '.idea', '.vscode', '.vs',
    '.next', '.nuxt', 'dist', 'build', 'out', 'target',
    'coverage', '.coverage', 'htmlcov', '.nyc_output',
    'logs', 'log', 'tmp',
}

COMMON_EXCLUDE_FILES = {
    '.gitignore', '.dockerignore', '.editorconfig', '.gitkeep',
    'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
    'Gemfile.lock', 'Cargo.lock',
    '.DS_Store', 'Thumbs.db',
}

NON_CODE_EXTENSIONS = {
    '.pyc', '.pyo', '.pyd', '.so', '.dll', '.dylib', '.o', '.obj', '.lib', '.a',
    '.exe', '.msi', '.bin', '.app', '.dmg', '.deb', '.rpm',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.ico', '.icns', '.avif',
    '.mp3', '.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.wav', '.flac', '.ogg', '.m4a',
    '.zip', '.tar', '.gz', '.bz2', '.xz', '.7z', '.rar', '.zst',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.csv',
    '.ttf', '.otf', '.woff', '.woff2', '.eot',
    '.db', '.sqlite', '.sqlite3', '.db3',
    '.min.js', '.min.css', '.map',
}

DEFAULT_CODE_EXTENSIONS = [
    '.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.scss', '.less',
    '.md', '.json', '.yaml', '.yml', '.toml', '.xml',
    '.rs', '.go', '.java', '.kt', '.swift', '.c', '.cpp', '.h', '.hpp',
    '.rb', '.php', '.sh', '.bash', '.zsh', '.ps1', '.bat',
    '.sql', '.graphql', '.vue', '.svelte', '.astro',
    '.pyi', '.pxd', '.pxi',
    '.proto', '.gradle', '.cmake', '.makefile',
    '.ini', '.cfg', '.conf',
]


def is_non_code_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename)
    return ext.lower() in NON_CODE_EXTENSIONS


def generate_directory_tree(root_path: str, exclude_dirs: list[str], exclude_files: set, recursive: bool, current_depth: int = 0) -> list[str]:
    dir_exclude = set(exclude_dirs)
    prefix = "    " * current_depth + "├── "
    tree = []
    try:
        items = sorted(os.listdir(root_path))
    except PermissionError:
        return tree

    for item in items:
        item_path = os.path.join(root_path, item)
        if item in dir_exclude:
            continue
        if os.path.isdir(item_path):
            tree.append(f"{prefix}{item}/")
            if recursive:
                subtree = generate_directory_tree(item_path, exclude_dirs, exclude_files, recursive, current_depth + 1)
                tree.extend(subtree)
        else:
            if item in exclude_files or is_non_code_file(item):
                continue
            tree.append(f"{prefix}{item}")
    return tree


def read_file_content(file_path: str, add_line_numbers: bool) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    ext = Path(file_path).suffix[1:]
    if add_line_numbers and content.strip():
        lines = content.splitlines()
        width = len(str(len(lines)))
        numbered = "\n".join(f"{i+1:>{width}}  {line}" for i, line in enumerate(lines))
        return f"```{ext}\n{numbered}\n```"
    return f"```{ext}\n{content}\n```"


def generate_markdown(
    input_path: str, output_path: str, recursive: bool,
    exclude_dirs: list[str], exclude_files: set, extensions: list[str],
    add_line_numbers: bool
) -> None:
    hl = "#" * 2
    md_lines = []

    md_lines.append(f"# {Path(input_path).name} 代码结构")
    md_lines.append("")

    root = Path(input_path)
    if root.is_file():
        try:
            md_lines.append(f"{hl} `{root.name}`\n")
            md_lines.append(read_file_content(input_path, add_line_numbers))
        except UnicodeDecodeError:
            md_lines.append("```\n(二进制文件或编码不支持)\n```")
    else:
        md_lines.append(f"{hl} 目录结构\n")
        tree = generate_directory_tree(input_path, exclude_dirs, exclude_files, recursive)
        md_lines.append("\n".join(tree) if tree else "(空)")

        md_lines.append(f"\n\n{hl} 文件代码\n")
        for root_dir, dirs, files in os.walk(input_path):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            if not recursive and root_dir != str(input_path):
                dirs[:] = []
                continue
            for file in sorted(files):
                if file in exclude_files:
                    continue
                if not any(file.endswith(ext) for ext in extensions):
                    continue
                if is_non_code_file(file):
                    continue
                file_path = os.path.join(root_dir, file)
                relative_path = os.path.relpath(file_path, input_path)
                md_lines.append(f"\n{hl} `{relative_path}`\n")
                try:
                    md_lines.append(read_file_content(file_path, add_line_numbers))
                except UnicodeDecodeError:
                    md_lines.append("```\n(二进制文件或编码不支持)\n```")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"Markdown 文档已生成: {output.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将源代码目录/文件转换为格式化 Markdown 文档")
    parser.add_argument("--input", required=True, help="源文件或目录路径")
    parser.add_argument("--output", required=True, help="输出 Markdown 文件路径")
    parser.add_argument("--recursive", action="store_true", default=True, help="递归子目录（默认开启）")
    parser.add_argument("--exclude-dirs", nargs="+", default=[], help="额外排除的目录名（空格分隔，不传则只排除常见目录）")
    parser.add_argument("--exclude-files", nargs="+", default=[], help="额外排除的文件名（空格分隔，不传则只排除常见文件）")
    parser.add_argument("--extensions", nargs="+", default=DEFAULT_CODE_EXTENSIONS, help="包含的文件扩展名（默认覆盖常见代码类型）")
    parser.add_argument("--line-numbers", action="store_true", default=False, help="代码块显示行号（默认关闭）")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        parser.error(f"路径不存在: {args.input}")

    merged_exclude_dirs = list(set(COMMON_EXCLUDE_DIRS) | set(args.exclude_dirs))
    merged_exclude_files = set(COMMON_EXCLUDE_FILES) | set(args.exclude_files)
    generate_markdown(
        input_path=args.input,
        output_path=args.output,
        recursive=args.recursive,
        exclude_dirs=merged_exclude_dirs,
        exclude_files=merged_exclude_files,
        extensions=args.extensions,
        add_line_numbers=args.line_numbers,
    )
