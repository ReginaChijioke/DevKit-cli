
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
        mock_run.return_value = self.create_result()

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
        self.assertIn("Project created successfully.", output)

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


if __name__ == "__main__":
    unittest.main()
