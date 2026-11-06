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

Automates the creation of Python project directories and user-selected folders.

**Implemented capabilities:**

- Accept a project name through the `init` command.
- Validate project names.
- Reject invalid project names and characters.
- Check whether a project directory already exists.
- Create a new project directory.
- Interactively collect folder names from the user.
- Process comma-separated folder names.
- Remove unnecessary whitespace from folder names.
- Ignore empty folder entries.
- Create the requested directories inside the project directory.

**Planned capabilities:**

- Allow users to specify files grouped by their destination folders.
- Create empty files in the locations selected by the user.
- Improve input validation and filesystem error handling.
- Add automated tests for Project Generator functionality.

DevKit's Project Generator is being designed around user-customizable project structures rather than forcing every developer to use one predefined template.

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
| `doctor` | Environment Doctor | Checks the active Python version and Git availability and repository status. |
| `init` | Project Generator | Validates the project name, creates the project directory, and interactively creates user-selected folders. |
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
```

DevKit creates the requested folders inside the new project directory.

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
| 4 | Project Generator | In Progress |
| 5 | Documentation Generation | Planned |
| 6 | Project Doctor | Planned |
| 7 | Testing, debugging, and refinement | In Progress |

The roadmap may be adjusted as development progresses and feedback is received.

## Testing Strategy

Testing is an important part of development.

The project uses Python's `unittest` framework to verify functionality and handle expected edge cases.

**Current automated testing coverage — Environment Doctor:**

1. Python version meets the minimum requirement.
2. Python version is below the minimum requirement.
3. Python version is exactly at the minimum requirement (Python 3.11).
4. Git repository is detected.
5. Current directory is not a Git repository.
6. Git encounters an unexpected error.
7. Git executable is missing.

**Current test results:**

- Total automated tests: 7.
- Passed: 7.
- Failed: 0.

Run the test suite using:

```bash
python3 -m unittest discover -s tests -v
```

Project Generator manual testing currently covers:

- Successful project directory creation.
- Rejection of an existing project directory.
- Rejection of invalid project names.
- Creation of multiple user-selected folders.

Automated testing for the Project Generator will be introduced as the feature develops.

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

**Current stage:** CLI foundation and Environment Doctor completed; Project Generator in progress.

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
- Interactive collection and creation of user-selected folders.

**Currently in progress:**

- Customizable Project Generator functionality.
- Grouped file input and file placement.
- Automated Project Generator testing.
- Refining filesystem error handling.

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