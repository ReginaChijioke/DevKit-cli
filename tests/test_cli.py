
import unittest
from argparse import Namespace
from unittest.mock import patch, Mock
from contextlib import redirect_stdout
from io import StringIO
import subprocess
import tempfile
import os
from pathlib import Path

from devkit.cli import run_doctor, run_init


class TestEnvironmentDoctor(unittest.TestCase):

    def create_result(self, returncode=0, stdout="", stderr=""):
        return subprocess.CompletedProcess(
            args=[],
            returncode=returncode,
            stdout=stdout,
            stderr=stderr
        )

    def run_doctor_and_capture_output(self):
        output = StringIO()

        with redirect_stdout(output):
            run_doctor(Namespace())

        return output.getvalue()

    @patch("devkit.cli.subprocess.run")
    def test_python_version_meets_requirement(self, mock_run):
        mock_run.return_value = self.create_result()

        test_version = Mock()
        test_version.major = 3
        test_version.minor = 12
        test_version.micro = 3
        test_version.__ge__ = Mock(return_value=True)

        with patch("devkit.cli.sys.version_info", test_version):
            output = self.run_doctor_and_capture_output()

        self.assertIn("Python version: 3.12.3", output)
        self.assertIn("Python version meets the requirement.", output)

    @patch("devkit.cli.subprocess.run")
    def test_python_version_at_minimum_requirement(self, mock_run):
        mock_run.return_value = self.create_result()

        test_version = Mock()
        test_version.major = 3
        test_version.minor = 11
        test_version.micro = 0
        test_version.__ge__ = Mock(return_value=True)

        with patch("devkit.cli.sys.version_info", test_version):
            output = self.run_doctor_and_capture_output()

        self.assertIn("Python version: 3.11.0", output)
        self.assertIn("Python version meets the requirement.", output)

    @patch("devkit.cli.subprocess.run")
    def test_python_version_below_requirement(self, mock_run):
        mock_run.return_value = self.create_result(returncode=0)

        test_version = Mock()
        test_version.major = 3
        test_version.minor = 10
        test_version.micro = 12
        test_version.__ge__ = Mock(return_value=False)

        with patch("devkit.cli.sys.version_info", test_version):
            output = self.run_doctor_and_capture_output()

        self.assertIn("Python 3.11 or newer is required.", output)

    @patch("devkit.cli.subprocess.run")
    def test_git_repository_detected(self, mock_run):
        mock_run.return_value = self.create_result()

        output = self.run_doctor_and_capture_output()

        self.assertIn("Git repository detected.", output)

    @patch("devkit.cli.subprocess.run")
    def test_directory_is_not_git_repository(self, mock_run):
        mock_run.return_value = self.create_result(
            returncode=128,
            stderr="fatal: not a git repository"
        )

        output = self.run_doctor_and_capture_output()

        self.assertIn("This directory is not a Git repository.", output)

    @patch("devkit.cli.subprocess.run")
    def test_git_encounters_other_error(self, mock_run):
        error_message = "fatal: detected dubious ownership in repository"

        mock_run.return_value = self.create_result(
            returncode=128,
            stderr=error_message
        )

        output = self.run_doctor_and_capture_output()

        self.assertIn("Git encountered an error.", output)
        self.assertIn(error_message, output)

    @patch("devkit.cli.subprocess.run")
    def test_git_executable_missing(self, mock_run):
        mock_run.side_effect = FileNotFoundError

        output = self.run_doctor_and_capture_output()

        self.assertIn("Git is not installed or could not be found.", output)


class TestProjectGenerator(unittest.TestCase):

    def setUp(self):
        self.original_directory = os.getcwd()
        self.temp_directory = tempfile.TemporaryDirectory()
        os.chdir(self.temp_directory.name)

    def tearDown(self):
        os.chdir(self.original_directory)
        self.temp_directory.cleanup()

    def run_init_and_capture_output(self, project_name, user_inputs):
        output = StringIO()

        with patch("builtins.input", side_effect=user_inputs):
            with redirect_stdout(output):
                run_init(Namespace(project_name=project_name))

        return output.getvalue()

    def test_project_and_files_created_successfully(self):
        output = self.run_init_and_capture_output(
            "sample_project",
            [
                "src, tests",
                "src: main.py, config.py",
                "root: README.md",
                ""
            ]
        )

        self.assertTrue(Path("sample_project").is_dir())
        self.assertTrue(Path("sample_project/src").is_dir())
        self.assertTrue(Path("sample_project/tests").is_dir())
        self.assertTrue(Path("sample_project/src/main.py").is_file())
        self.assertTrue(Path("sample_project/src/config.py").is_file())
        self.assertTrue(Path("sample_project/README.md").is_file())
        self.assertIn("3 created successfully.", output)
        self.assertIn("0 failed to create.", output)

    def test_project_directory_permission_error(self):
        with patch.object(Path, "mkdir", side_effect=PermissionError):
            output = self.run_init_and_capture_output(
                "permission_test",
                []
            )

        self.assertIn(
            "Permission denied: unable to create project directory.",
            output
        )
        self.assertFalse(Path("permission_test").exists())

    def test_project_directory_oserror(self):
        error_message = "Simulated filesystem failure"

        with patch.object(
            Path,
            "mkdir",
            side_effect=OSError(error_message)
        ):
            output = self.run_init_and_capture_output(
                "filesystem_error_test",
                []
            )

        self.assertIn(
            f"Could not create project directory: {error_message}",
            output
        )
        self.assertFalse(Path("filesystem_error_test").exists())

    def test_folder_creation_oserror(self):
        original_mkdir = Path.mkdir

        def selective_mkdir(path, *args, **kwargs):
            if path.name == "tests":
                raise OSError("Simulated folder creation failure")
            return original_mkdir(path, *args, **kwargs)

        with patch.object(Path, "mkdir", new=selective_mkdir):
            output = self.run_init_and_capture_output(
                "folder_error_test",
                [
                    "src, tests, docs",
                    ""
                ]
            )

        self.assertTrue(Path("folder_error_test/src").is_dir())
        self.assertFalse(Path("folder_error_test/tests").exists())
        self.assertTrue(Path("folder_error_test/docs").is_dir())

        self.assertIn("Could not create tests:", output)
        self.assertIn("Simulated folder creation failure", output)
        self.assertIn("2 created successfully.", output)
        self.assertIn("1 failed to create.", output)

    def test_file_creation_oserror(self):
        original_touch = Path.touch

        def selective_touch(path, *args, **kwargs):
            if path.name == "main.py":
                raise OSError("Simulated file creation failure")
            return original_touch(path, *args, **kwargs)

        with patch.object(Path, "touch", new=selective_touch):
            output = self.run_init_and_capture_output(
                "file_error_test",
                [
                    "src",
                    "src: main.py, config.py",
                    ""
                ]
            )

        self.assertFalse(
            Path("file_error_test/src/main.py").exists()
        )
        self.assertTrue(
            Path("file_error_test/src/config.py").is_file()
        )

        self.assertIn("Could not create main.py:", output)
        self.assertIn("Simulated file creation failure", output)
        self.assertIn("1 created successfully.", output)
        self.assertIn("1 failed to create.", output)

    def test_existing_file_is_preserved(self):
        output = StringIO()
        input_count = 0

        def provide_input(prompt):
            nonlocal input_count
            input_count += 1

            if input_count == 2:
                existing_file = Path(
                    "existing_file_test/src/main.py"
                )
                existing_file.write_text("Original content")

            user_inputs = [
                "src",
                "src: main.py, config.py",
                ""
            ]

            return user_inputs[input_count - 1]

        with patch("builtins.input", side_effect=provide_input):
            with redirect_stdout(output):
                run_init(
                    Namespace(project_name="existing_file_test")
                )

        self.assertEqual(
            Path("existing_file_test/src/main.py").read_text(),
            "Original content"
        )
        self.assertTrue(
            Path("existing_file_test/src/config.py").is_file()
        )

        self.assertIn("File already exists.", output.getvalue())
        self.assertIn("1 created successfully.", output.getvalue())
        self.assertIn("0 failed to create.", output.getvalue())

    def test_invalid_project_name_is_rejected(self):
        output = self.run_init_and_capture_output(
            "bad-name",
            []
        )

        self.assertIn("Invalid character detected.", output)
        self.assertFalse(Path("bad-name").exists())

    def test_existing_project_is_rejected(self):
        Path("existing_project").mkdir()

        output = self.run_init_and_capture_output(
            "existing_project",
            []
        )

        self.assertIn("Project already exists.", output)

    def test_invalid_filename_path_is_rejected(self):
        output = self.run_init_and_capture_output(
            "path_test",
            [
                "src",
                "src: src/main.py",
                ""
            ]
        )

        self.assertIn("Invalid filename", output)
        self.assertFalse(
            Path("path_test/src/src/main.py").exists()
        )

    def test_parent_directory_filename_is_rejected(self):
        output = self.run_init_and_capture_output(
            "parent_test",
            [
                "",
                "root: ..",
                ""
            ]
        )

        self.assertIn("Invalid filename", output)

    def test_invalid_folder_mapping_is_rejected(self):
        output = self.run_init_and_capture_output(
            "mapping_test",
            [
                "src",
                "unknown: main.py",
                ""
            ]
        )

        self.assertIn("Folder does not exist", output)
        self.assertFalse(
            Path("mapping_test/main.py").exists()
        )

    def test_invalid_mapping_format_is_rejected(self):
        output = self.run_init_and_capture_output(
            "format_test",
            [
                "src",
                "src main.py",
                ""
            ]
        )

        self.assertIn("Invalid folder/file format.", output)

    def test_invalid_folder_names_are_rejected(self):
        output = self.run_init_and_capture_output(
            "folder_validation_test",
            [
                "src, test_files, my-project, 123folder, src/main, my folder, ..",
                ""
            ]
        )

        self.assertTrue(Path("folder_validation_test/src").is_dir())
        self.assertTrue(Path("folder_validation_test/test_files").is_dir())
        self.assertTrue(Path("folder_validation_test/my-project").is_dir())

        self.assertFalse(Path("folder_validation_test/123folder").exists())
        self.assertFalse(Path("folder_validation_test/my folder").exists())
        self.assertFalse(Path("folder_validation_test/src/main").exists())

        self.assertIn(
            "Folder name must start with a letter.",
            output
        )
        self.assertIn(
            "Folder name can only contain letters, numbers, underscores and hyphens.",
            output
        )
        self.assertIn(
            "Folder name cannot be '.' or '..'.",
            output
        )

        self.assertIn("3 created successfully.", output)
        self.assertIn("4 failed to create.", output)

    def test_duplicate_folder_names_are_rejected(self):
        output = self.run_init_and_capture_output(
            "duplicate_folder_test",
            [
                "src, tests, src, docs, tests",
                ""
            ]
        )

        self.assertTrue(Path("duplicate_folder_test/src").is_dir())
        self.assertTrue(Path("duplicate_folder_test/tests").is_dir())
        self.assertTrue(Path("duplicate_folder_test/docs").is_dir())

        self.assertIn(
            "Duplicate folder: 'src' has already been requested",
            output
        )
        self.assertIn(
            "Duplicate folder: 'tests' has already been requested",
            output
        )

        self.assertIn("3 created successfully.", output)
        self.assertIn("2 failed to create.", output)

    def test_duplicate_filenames_are_rejected(self):
        output = self.run_init_and_capture_output(
            "duplicate_file_test",
            [
                "src",
                "src: main.py, main.py",
                ""
            ]
        )

        self.assertTrue(
            Path("duplicate_file_test/src/main.py").is_file()
        )
        self.assertEqual(
            len(list(Path("duplicate_file_test/src").iterdir())),
            1
        )

        self.assertIn("Duplicate filename.", output)
        self.assertIn("1 created successfully.", output)
        self.assertIn("0 failed to create.", output)

    def test_filenames_with_spaces_are_rejected_and_other_extensions_accepted(self):
        output = self.run_init_and_capture_output(
            "language_agnostic_test",
            [
                "",
                "root: my file.py, main.go",
                ""
            ]
        )

        self.assertFalse(
            Path("language_agnostic_test/my file.py").exists()
        )
        self.assertTrue(
            Path("language_agnostic_test/main.go").is_file()
        )

        self.assertIn(
            "Invalid filename: spaces are not allowed.",
            output
        )
        self.assertIn("1 created successfully.", output)
        self.assertIn("1 failed to create.", output)


if __name__ == "__main__":
    unittest.main()
