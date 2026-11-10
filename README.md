# DevKit CLI

**Build consistently. Develop confidently.**

A Python-first command-line setup assistant designed to simplify project initialization, environment configuration, documentation generation, and project inspection.

## Overview

DevKit CLI is a command-line tool designed to help developers reduce the repetitive work involved in setting up and maintaining Python projects.

Starting a new project often involves manually creating directories, configuring development environments, preparing documentation, and checking project structures. These tasks can be time-consuming and may lead to inconsistent setups.

DevKit CLI aims to simplify these processes through a collection of commands that automate common project setup and inspection tasks.

The goal is to make starting and managing Python projects easier, more consistent, and less error-prone.

## Problem Statement

Developers frequently repeat the same setup procedures when starting new projects. These include:

- Creating project directories and files.
- Checking whether required development tools are installed.
- Configuring Python development environments.
- Writing basic project documentation.
- Inspecting existing projects for missing or incorrectly configured components.

Performing these tasks manually can introduce unnecessary complexity, especially for beginners and developers managing multiple projects.

DevKit CLI aims to address this problem by bringing essential setup and inspection tasks into one simple command-line tool.

## Project Objectives

The primary objectives of DevKit CLI are to:

- Automate repetitive Python project setup tasks.
- Simplify development environment verification.
- Generate customizable Python project structures.
- Reduce the effort required to create project documentation.
- Help developers identify common project configuration and structural issues.
- Encourage consistency and better development practices.

## Core Features

The initial version of DevKit CLI focuses on four major features.

### 1. Environment Doctor

Checks the developer's active Python environment and verifies Git availability and repository status.

**Implemented capabilities:**

- Detect the Python version of the interpreter currently running DevKit using `sys.version_info`.
- Display the detected Python version.
- Verify that the active interpreter meets the Python 3.11 minimum requirement.
- Identify whether the current directory is a Git repository.
- Handle cases where Git is unavailable.
- Distinguish between directories that are not Git repositories and other Git-related errors.
- Provide diagnostic messages for detected issues.

**Future improvements:**

- Ask for user permission before initializing Git in a directory.
- Verify additional development tools and configurations.
- Provide more detailed diagnostic recommendations.

### 2. Project Generator

Automates the creation of customizable project directories, folders, and empty files.

**Implemented capabilities:**

- Accept a project name through the `init` command.
- Reject empty project names.
- Require project names to begin with a letter.
- Allow only alphanumeric characters and underscores in project names.
- Check whether a project directory already exists.
- Create a new project directory using `pathlib`.
- Handle permission errors and other filesystem errors during project directory creation.
- Interactively collect comma-separated folder names.
- Remove unnecessary whitespace from folder names.
- Ignore empty folder entries.
- Require folder names to begin with a letter.
- Allow alphanumeric characters, underscores, and hyphens in folder names.
- Reject invalid folder names, including `.` and `..`.
- Detect and reject duplicate folder names.
- Create the requested folders inside the project directory.
- Report successful and failed folder creation separately.
- Handle filesystem errors during folder creation.
- Accept grouped folder/file mappings.
- Support `root` as the destination for files placed directly in the project root.
- Validate folder mappings and reject references to folders that were not created.
- Accept comma-separated filenames within a mapping.
- Reject invalid filenames and nested file paths.
- Detect duplicate filenames within a mapping.
- Create empty files in the selected destinations using `pathlib`.
- Detect existing files and skip them without overwriting their contents.
- Handle filesystem errors during file creation.
- Report successful and failed file creation separately.

**Current input format:**

```text
Enter folder names: src, tests, config

Enter folder/file mapping:
src: main.py, config.py
tests: test_main.py
root: README.md, .gitignore
```

In this example, DevKit creates the requested folders and empty files, with `root` representing the project directory itself.

The Project Generator is designed around user-customizable project structures rather than forcing every developer to use one predefined template.

It creates the requested directories and empty files; it does not currently generate starter code or populate files with predefined content.

### 3. Documentation Generation

Simplifies the creation of basic project documentation.

**Planned capabilities:**

- Generate starter README files.
- Include common documentation sections.
- Allow project-specific information to be included.
- Provide a consistent documentation structure.

### 4. Project Doctor

Inspects existing Python projects and identifies common structural or configuration issues.

**Planned capabilities:**

- Check for expected project files and directories.
- Identify missing or incorrectly organized components.
- Report potential configuration issues.
- Provide actionable recommendations for improvement.

## Current CLI Commands

The command-line structure is established using Python's `argparse` module.

| Command | Purpose | Current Behaviour |
|---|---|---|
| `doctor` | Environment Doctor | Checks the active Python version, Git availability, and repository status. |
| `init` | Project Generator | Creates a project directory, validates and creates user-selected folders, and creates empty files through grouped mappings. |
| `docs` | Documentation Generation | Displays the Documentation Generator introduction. |
| `inspect` | Project Doctor | Displays the Project Doctor introduction. |

When DevKit is executed without a subcommand, it displays the general CLI help information.

## Getting Started

### Requirements

- Python 3.11 or later.
- Git for version control and collaboration.

### Installation

Clone the repository:

```bash
git clone https://github.com/ReginaChijioke/DevKit-cli.git
```

Navigate into the project directory:

```bash
cd DevKit-cli
```

### Running the CLI

Display general help:

```bash
python3 -m devkit.cli
```

Display available commands:

```bash
python3 -m devkit.cli --help
```

Run the Environment Doctor:

```bash
python3 -m devkit.cli doctor
```

Start a new project:

```bash
python3 -m devkit.cli init weather_app
```

DevKit validates the project name, checks whether the project already exists, and creates the project directory.

It then prompts the user to enter the folder names they want created.

Example:

```text
Enter folder names: src, tests, config

Enter folder/file mapping:
src: main.py, config.py
tests: test_main.py
root: README.md, .gitignore
```

DevKit validates the folder names, rejects duplicates and invalid entries, and creates the accepted folders.

It then processes the grouped file mappings and creates empty files in the specified destinations. Existing files are preserved rather than overwritten.

Run the other available commands:

```bash
python3 -m devkit.cli docs
python3 -m devkit.cli inspect
```

## Technology Stack

The project primarily uses:

- **Python:** Main programming language.
- **argparse:** Command-line argument and command handling.
- **sys:** Access to information about the active Python interpreter.
- **pathlib:** Filesystem and path management.
- **subprocess:** Interaction with external development tools.
- **venv:** Python virtual environment management.
- **unittest:** Automated testing.
- **unittest.mock:** Mocking dependencies during tests.
- **tempfile:** Isolated temporary directories for testing.
- **Git and GitHub:** Version control and project collaboration.

The implementation prioritizes Python's standard library to keep the tool lightweight and minimize external dependencies.

## Target Users

DevKit CLI is intended for:

- Beginner Python developers.
- Students learning software development.
- Developers who frequently create Python projects.
- Instructors and mentors helping learners establish consistent project structures.
- Independent developers looking to simplify repetitive setup tasks.

## Project Scope

The initial release focuses exclusively on Python project workflows.

The four core features are:

1. Environment Doctor.
2. Project Generator.
3. Documentation Generation.
4. Project Doctor.

Support for other programming languages, advanced templates, and additional developer utilities may be considered for future releases.

## Development Roadmap

Development follows an incremental approach:

| Phase | Focus | Status |
|---|---|---|
| 1 | Repository, project structure, and initial documentation | Completed |
| 2 | CLI foundation, subcommand registration, and command routing | Completed |
| 3 | Environment Doctor | Completed |
| 4 | Project Generator | Implementation and testing completed; final review and merge preparation underway |
| 5 | Documentation Generation | Planned |
| 6 | Project Doctor | Planned |
| 7 | Testing, debugging, and refinement | Ongoing |

The roadmap may be adjusted as development progresses and feedback is received.

## Testing Strategy

Testing is an important part of development.

The project uses Python's `unittest` framework to verify functionality and handle expected edge cases.

### Environment Doctor automated tests

1. Python version meets the minimum requirement.
2. Python version is below the minimum requirement.
3. Python version is exactly at the minimum requirement (Python 3.11).
4. Git repository is detected.
5. Current directory is not a Git repository.
6. Git encounters an unexpected error.
7. Git executable is missing.

### Project Generator automated tests

1. Project directory, folders, and files are created successfully.
2. Project directory permission errors are handled.
3. General project directory filesystem errors are handled.
4. Folder creation filesystem errors are handled.
5. File creation filesystem errors are handled.
6. Existing files are preserved and not overwritten.
7. Invalid project names are rejected.
8. Existing project directories are rejected.
9. Invalid filename paths are rejected.
10. Parent directory filenames are rejected.
11. Mappings to nonexistent folders are rejected.
12. Invalid mapping formats are rejected.
13. Invalid folder names are rejected.
14. Duplicate folder names are rejected.
15. Duplicate filenames are rejected.

### Current test results

- Total automated tests: **22**.
- Passed: **22**.
- Failed: **0**.

Run the test suite using:

```bash
python3 -m unittest discover -s tests -v
```

The tests use temporary directories to isolate filesystem operations and avoid leaving generated test projects in the repository.

## Design Principles

DevKit CLI follows these principles:

- **Simplicity:** Commands should be easy to understand and use.
- **Reliability:** Operations should behave predictably.
- **Safety:** Existing project files should not be overwritten unexpectedly.
- **Clarity:** Errors and diagnostic messages should be understandable.
- **Modularity:** Features should be organized into maintainable components.
- **Testability:** Functionality should be verifiable through automated tests.
- **Flexibility:** Developers should have control over their generated project structures.

## Project Status

**Current stage:** CLI foundation and Environment Doctor completed. Project Generator implementation and automated testing completed; final review and merge preparation underway.

**Completed:**

- Initial repository and project structure.
- Python package initialization.
- Basic command-line argument parser using `argparse`.
- Application description configuration.
- Registration of the four core CLI subcommands.
- Association of each subcommand with its respective function.
- Basic command execution and routing.
- Successful manual testing of all four commands.
- Successful display of CLI help using `--help`.
- Default help behaviour when the CLI is executed without a command.
- Active Python interpreter version detection using `sys.version_info`.
- Minimum Python version validation (3.11).
- Display of the detected Python version.
- Git repository detection.
- Handling of missing Git executables and Git-related errors.
- Seven automated Environment Doctor tests passing.
- Project name validation for the Project Generator.
- Existing project directory detection.
- Project directory creation using `pathlib`.
- Project directory permission and filesystem error handling.
- Interactive collection and creation of user-selected folders.
- Folder-name validation and rejection of invalid path entries.
- Duplicate folder-name detection.
- Folder creation error handling and reporting.
- Grouped folder/file mapping.
- Support for placing files in selected folders or the project root.
- Filename validation and rejection of nested paths.
- Duplicate filename detection.
- Empty file creation.
- Protection of existing files from accidental overwriting.
- File creation error handling and reporting.
- Separate folder and file success/failure summaries.
- Twenty-two automated tests passing across Environment Doctor and Project Generator.

**Currently in progress:**

- Final Project Generator review.
- Final documentation verification.
- Pull request review and preparation for merging into `main`.

**Not yet implemented:**

- Documentation Generation functionality.
- Project Doctor functionality.

This README will be updated throughout development to reflect completed features, new commands, usage instructions, testing results, and changes to project scope.

## Collaboration

Development uses Git and GitHub for version control, collaboration, and code review.

Contributions, feedback, and suggestions are welcome, particularly those that improve usability, reliability, and maintainability.

## License

A license will be selected before public distribution.

---

**DevKit CLI — Build consistently. Develop confidently.**
