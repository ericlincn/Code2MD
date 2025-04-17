# Code2MD  

A Python script to generate a structured Markdown document from your project's source code. It automatically:  

- 📂 **Builds a directory tree** – Visualize your project structure.  
- 📝 **Embeds code files** – Supports syntax highlighting for multiple extensions.  
- ⚙️ **Customizable filters** – Exclude directories, limit file extensions, and control recursion.  

Perfect for sharing code snippets, documenting projects, or creating portable code reports!  

## Features  
- Recursive/non-recursive directory traversal  
- Exclude specific folders (e.g., `node_modules`, `venv`)  
- Filter by file extensions (e.g., `.py`, `.js`, `.html`)  
- Clean Markdown output with code blocks  

## Usage  
```bash
python code_to_markdown.py /your/project/path [--non-recursive] [--exclude-dirs dir1 dir2] [--extensions .py .js]
