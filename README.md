# code-to-markdown

将源代码目录（或单个文件）转换为格式化 Markdown 文档。自带目录树、语法高亮代码块、常见非代码文件自动排除。

## Quick Start

```bash
python code_to_markdown.py --input src/ --output docs/code.md
```

## Features

- **目录树** — 输出项目结构总览，一目了然
- **代码块** — 每份源文件独立成块，自动识别语言
- **行号可选** — 代码块加行号（`--line-numbers`），默认关
- **自动排除** — 常见非代码目录/文件/扩展名无需手动指定：

  | 类别 | 自动跳过 |
  |------|---------|
  | **目录** | `.git` `node_modules` `__pycache__` `.venv` `dist` `build` `target` `coverage` 等 |
  | **文件** | `.gitignore` `package-lock.json` `yarn.lock` `.DS_Store` 等 |
  | **扩展名** | `.pyc` `.jpg` `.png` `.mp4` `.zip` `.pdf` `.exe` `.min.js` `.map` 等 |

- **递归/不递归** — 默认递归子目录，`--recursive` 可选
- **精细控制** — 白名单扩展名、额外排除目录/文件，覆盖各种场景

## Usage

### Basic

```bash
python code_to_markdown.py --input src/ --output docs/codebase.md
```

### Options

| Param | Required | Description |
|-------|----------|-------------|
| `--input` | ✅ | Source file or directory |
| `--output` | ✅ | Output `.md` path |
| `--recursive` | | Recursive subdirectories (default: `True`) |
| `--exclude-dirs` | | Extra dirs to exclude (space-separated) |
| `--exclude-files` | | Extra files to exclude (space-separated) |
| `--extensions` | | Include only these extensions (default: common code extensions) |
| `--line-numbers` | | Show line numbers in code blocks (default: off) |

### Examples

```bash
# Single file
python code_to_markdown.py --input src/auth/login.py --output docs/login.md

# Whole project, with line numbers, excluding tests
python code_to_markdown.py --input . --output docs/full.md --line-numbers --exclude-dirs tests

# Narrow to Python only, exclude lock files
python code_to_markdown.py --input . --output docs/python.md --extensions .py --exclude-files poetry.lock
```

## Output Structure

```
# ProjectName 代码结构

## 目录结构

├── src/
    ├── main.py
    ├── services/
        ├── auth.py
        └── db.py
├── tests/
    ├── test_auth.py

## 文件代码

### `src/main.py`

```python
def main():
    ...
```

### `src/services/auth.py`

```python
...
```
```

## Requirements

- Python 3.10+

No external dependencies (stdlib only).

## License

MIT
