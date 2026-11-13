
import unittest
import tempfile
from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from devkit.scanner import scan_python_files, inspect_python_files


class TestScanPythonFiles(unittest.TestCase):

    def test_finds_python_file_in_root(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            (project_path / "main.py").touch()

            result = scan_python_files(project_path)

            self.assertIn(Path("main.py"), result)

    def test_finds_python_files_in_nested_directories(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            nested_dir = project_path / "app"
            nested_dir.mkdir()
            (nested_dir / "views.py").touch()

            result = scan_python_files(project_path)

            self.assertIn(Path("app/views.py"), result)

    def test_ignores_excluded_directories(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            excluded_dir = project_path / ".venv"
            excluded_dir.mkdir()
            (excluded_dir / "ignored.py").touch()

            result = scan_python_files(project_path)

            self.assertNotIn(Path(".venv/ignored.py"), result)

    def test_detects_functions_classes_and_async_functions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            source_code = """
def greet():
    pass

class Student:
    pass

async def fetch_data():
    pass
"""
            (project_path / "main.py").write_text(source_code)

            python_files = scan_python_files(project_path)
            functions, classes, async_functions = inspect_python_files(
                project_path, python_files
            )

            self.assertIn("greet", functions)
            self.assertIn("Student", classes)
            self.assertIn("fetch_data", async_functions)

    def test_collects_definitions_from_multiple_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            (project_path / "first.py").write_text(
                "def first_function():\n    pass"
            )
            (project_path / "second.py").write_text(
                "class SecondClass:\n    pass"
            )

            python_files = scan_python_files(project_path)
            functions, classes, async_functions = inspect_python_files(
                project_path, python_files
            )

            self.assertIn("first_function", functions)
            self.assertIn("SecondClass", classes)

    def test_skips_files_with_syntax_errors(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            (project_path / "broken.py").write_text(
                "def broken_function(:\n    pass"
            )
            (project_path / "working.py").write_text(
                "def working_function():\n    pass"
            )

            python_files = scan_python_files(project_path)

            output = StringIO()
            with redirect_stdout(output):
                functions, classes, async_functions = inspect_python_files(
                    project_path, python_files
                )

            self.assertIn("Could not parse broken.py", output.getvalue())
            self.assertIn("working_function", functions)

    def test_skips_files_that_cannot_be_read(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            broken_file = project_path / "broken.py"
            broken_file.write_text("def broken_function():\n    pass")

            working_file = project_path / "working.py"
            working_file.write_text("def working_function():\n    pass")

            python_files = [
                Path("broken.py"),
                Path("working.py")
            ]

            original_read_text = Path.read_text

            def mock_read_text(path, *args, **kwargs):
                if path.name == "broken.py":
                    raise PermissionError("Permission denied")
                return original_read_text(path, *args, **kwargs)

            output = StringIO()

            with patch.object(Path, "read_text", mock_read_text):
                with redirect_stdout(output):
                    functions, classes, async_functions = inspect_python_files(
                        project_path, python_files
                    )

            self.assertIn("Could not read broken.py", output.getvalue())
            self.assertIn("working_function", functions)


if __name__ == "__main__":
    unittest.main()
