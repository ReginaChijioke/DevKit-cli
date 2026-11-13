
import os
import ast
from pathlib import Path


def scan_python_files(project_path):
    project_path = Path(project_path)
    python_files = []
    excluded_dirs = [".git", ".venv", "venv", "__pycache__", "node_modules"]

    for dirpath, dirnames, filenames in os.walk(project_path):
        cleaned_dirs = []

        for directory in dirnames:
            if directory not in excluded_dirs:
                cleaned_dirs.append(directory)

        dirnames[:] = cleaned_dirs

        for filename in filenames:
            if filename.endswith(".py"):
                file_path = Path(dirpath) / filename
                relative_path = file_path.relative_to(project_path)
                python_files.append(relative_path)

    return python_files


def inspect_python_files(project_path, python_files):
    project_path = Path(project_path)
    functions = []
    classes = []
    async_functions = []

    for each_relative_path in python_files:
        full_file_path = project_path / each_relative_path

        try:
            source_code = full_file_path.read_text()
            ast_tree = ast.parse(source_code)

        except OSError as error:
            print(f"Warning: Could not read {each_relative_path} - {error}")
            continue

        except SyntaxError as err:
            print(f"Warning: Could not parse {each_relative_path} - {err}")
            continue

        for node in ast.walk(ast_tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)

            elif isinstance(node, ast.AsyncFunctionDef):
                async_functions.append(node.name)

            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)

    return functions, classes, async_functions
