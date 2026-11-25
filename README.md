# DevKit CLI

**Build consistently. Develop confidently.**

A Python-first command-line developer toolkit designed to simplify project initialization, environment checks, AI-powered documentation generation, and project inspection. Its Project Generator supports customizable project structures across programming languages.

## Overview

DevKit CLI helps developers reduce repetitive work involved in creating and maintaining software projects.

Starting a new project often involves manually creating directories, configuring development environments, preparing documentation, and checking project structures. These tasks can be time-consuming and may lead to inconsistent setups.

DevKit CLI brings these workflows together through four command-line tools:

- **Environment Doctor:** Checks Python and Git availability.
- **Project Generator:** Creates customizable project structures.
- **Documentation Generator:** Generates AI-powered README documentation.
- **Project Doctor:** Inspects projects and recommends improvements.

The project is Python-first: its CLI, Environment Doctor, and initial Documentation Generator scanner are built around Python. However, the Project Generator is language-agnostic and can create folders and empty files for projects written in different programming languages.

## Problem Statement

Developers frequently repeat setup and maintenance procedures, including:

- Creating project directories and files.
- Checking whether required development tools are installed.
- Configuring Python development environments.
- Writing and maintaining project documentation.
- Inspecting existing projects for structural or configuration issues.

DevKit CLI aims to simplify these processes through automation, consistent workflows, and clear diagnostic feedback.

## Project Objectives

- Automate repetitive project setup tasks.
- Simplify development environment verification.
- Generate customizable, language-agnostic project structures.
- Reduce the effort required to create project documentation.
- Use AI to produce meaningful, project-specific documentation.
- Help developers identify common project configuration and structural issues.
- Encourage consistency and better development practices.

## Core Features

### 1. Environment Doctor

Checks the developer's active Python environment and verifies Git availability and repository status.

**Implemented capabilities:**

- Detects the Python version of the interpreter running DevKit using `sys.version_info`.
- Displays the detected Python version.
- Verifies that the interpreter meets the Python 3.11 minimum requirement.
- Identifies whether the current directory is a Git repository.
- Handles cases where Git is unavailable.
- Distinguishes between directories that are not Git repositories and other Git-related errors.
- Provides diagnostic messages for detected issues.

**Future improvements:**

- Ask for permission before initializing Git in a directory.
- Verify additional development tools and configurations.
- Provide more detailed diagnostic recommendations.

### 2. Project Generator

Automates the creation of customizable project directories, folders, and empty files.

**Implemented capabilities:**

- Accepts and validates project names.
- Requires project names to begin with a letter.
- Allows only alphanumeric characters and underscores in project names.
- Checks whether a project directory already exists.
- Creates project directories using `pathlib`.
- Handles permission errors and other filesystem errors.
- Interactively collects comma-separated folder names.
- Removes unnecessary whitespace and ignores empty folder entries.
- Validates folder names, including rejecting `.` and `..`.
- Allows letters, numbers, underscores, and hyphens in folder names.
- Detects duplicate folder names.
- Reports successful and failed folder creation separately.
- Accepts grouped folder/file mappings.
- Supports `root` as the destination for files placed directly in the project root.
- Validates folder mappings and rejects references to folders that were not created.
- Accepts comma-separated filenames within mappings.
- Rejects filenames containing internal spaces and nested file paths.
- Supports different file extensions without restricting users to Python files.
- Supports extensionless filenames such as `Dockerfile` and dotfiles such as `.gitignore`.
- Detects duplicate filenames.
- Creates empty files using `pathlib`.
- Preserves existing files rather than overwriting their contents.
- Handles filesystem errors during file creation.
- Reports successful and failed file creation separately.

**Example input:**

```text
Enter folder names: src, tests, config

Enter folder/file mapping:

src: main.py, config.py

tests: test_main.py

root: README.md, .gitignore
```

The Project Generator creates the requested directories and empty files.

It is language-agnostic and can support structures containing files such as `.py`, `.js`, `.ts`, `.go`, `.rs`, `.java`, `.cpp`, `.html`, and `.css`, as well as extensionless files and dotfiles.

It does not currently generate starter code or populate files with predefined content.

### 3. Documentation Generator

Generates project-specific Markdown README documentation using AI.

The initial V1 implementation uses Groq's Chat Completions API and the `openai/gpt-oss-120b` model.

**Implemented capabilities:**

- Scans the current working directory for Python files.
- Uses the project scanner to discover Python files in nested directories.
- Excludes common directories such as `.git`, `.venv`, `venv`, `__pycache__`, and `node_modules`.
- Uses Python's Abstract Syntax Tree (AST) to inspect source files.
- Extracts function names, class names, and asynchronous function names.
- Handles unreadable files and Python syntax errors during inspection.
- Collects project information, including the project name and discovered Python definitions.
- Converts project information into JSON-compatible data.
- Sends the collected information to Groq for README generation.
- Uses a system prompt that instructs the model to produce factual documentation based only on supplied project information.
- Generates Markdown README content.
- Retrieves the Groq API key from the `GROQ_API_KEY` environment variable.
- Securely prompts for an API key using hidden input when the environment variable is unavailable.
- Handles API request errors and unexpected response structures.
- Displays available API error-response details when a request fails.
- Handles unsuccessful README generation.
- Checks whether a `README.md` already exists.
- Requests user confirmation before overwriting an existing README.
- Handles filesystem errors when writing generated documentation.

**Current V1 scope:**

- Groq is the AI provider.
- One model is configured: `openai/gpt-oss-120b`.
- The scanner focuses on Python projects.
- The generated output is a Markdown `README.md` file.
- The generator scans the current working directory.

**Current distribution status:**

The Documentation Generator has been tested from an external project directory using the installed DevKit wheel in a fresh virtual environment. It can run without manually configuring `PYTHONPATH`.

### 4. Project Doctor

Inspects an existing project, reports findings, and recommends improvements.

The initial V1 implementation focuses on Python projects.

**Implemented capabilities:**

- Displays the name of the project being inspected.
- Scans the project for Python files.
- Reports the number of Python files discovered.
- Uses AST inspection to identify functions, classes, and asynchronous functions.
- Detects Python syntax errors.
- Reports syntax-error filenames, messages, and line numbers.
- Checks whether a `README.md` file exists.
- Checks whether a `tests/` directory exists.
- Searches for test files matching the `test*.py` naming pattern.
- Reports the number of discovered test files.
- Identifies test directories that contain no matching test files.
- Checks for `requirements.txt`.
- Checks for `pyproject.toml`.
- Checks for `.gitignore`.
- Generates actionable recommendations for missing project components.
- Recommends fixing detected syntax errors.
- Displays a positive message when no recommendations are necessary.

**Current V1 scope:**

Project Doctor is an inspection and recommendation tool. It reports findings but does not automatically modify project files or repair detected issues.

The initial scanner and syntax-error analysis are Python-focused.

**Future improvements:**

- Expand project analysis beyond Python.
- Detect additional configuration and structural issues.
- Provide more detailed dependency analysis.
- Introduce more advanced project health checks.

## Current CLI Commands

The CLI uses Python's `argparse` module for command registration and routing.

| Command | Purpose | Current behaviour |
|---|---|---|
| `doctor` | Environment Doctor | Checks the active Python version, Git availability, and repository status. |
| `init` | Project Generator | Creates customizable project directories, folders, and empty files. |
| `docs` | Documentation Generator | Scans the current Python project and generates an AI-powered README using Groq. |
| `inspect` | Project Doctor | Inspects Python files, checks common project components, reports syntax errors, and recommends improvements. |

When DevKit is executed without a subcommand, it displays the general CLI help information.

## Getting Started

### Requirements

- Python 3.11 or later.
- Git for version control and collaboration.
- A Groq API key for the Documentation Generator.

The `requests` dependency is declared in the package configuration and is installed automatically during package installation.

### Package Installation

**PyPI publication is not yet complete.**

Once DevKit is published, users will be able to install it using:

```bash
python3 -m pip install devkit-cli
```

The installed package provides the `devkit` terminal command.

### Installing the Development Version

To work with the current source code, clone the repository:

```bash
git clone https://github.com/ReginaChijioke/DevKit-cli.git
```

Navigate into the project directory:

```bash
cd DevKit-cli
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the development package:

```bash
python3 -m pip install .
```

This installs the declared runtime dependencies and registers the `devkit` command in the active environment.

### Installing a Locally Built Wheel

Before PyPI publication, testers can install a locally built wheel.

After building the package, install it using:

```bash
python3 -m pip install dist/devkit_cli-0.1.0-py3-none-any.whl
```

The wheel can be shared with testers who have Python 3.11 or later.

### Running the CLI

Display general help:

```bash
devkit --help
```

Display the available commands:

```bash
devkit
```

### Run the Environment Doctor

```bash
devkit doctor
```

### Run the Project Generator

```bash
devkit init weather_app
```

DevKit validates the project name, checks whether the project already exists, and creates the project directory.

It then prompts for the folder names and grouped file mappings.

Example:

```text
Enter folder names: src, tests, config

Enter folder/file mapping:

src: main.py, config.py

tests: test_main.py

root: README.md, .gitignore
```

DevKit validates the requested folders and filenames, creates the accepted entries, and reports successful and failed operations separately.

Existing files are preserved rather than overwritten.

### Run the Documentation Generator

First, provide your Groq API key through the environment:

```bash
export GROQ_API_KEY="your_groq_api_key"
```

Alternatively, if the environment variable is not configured, DevKit securely prompts you to enter the key.

Navigate into the Python project you want to document, then run:

```bash
devkit docs
```

The Documentation Generator:

1. Scans the current working directory for Python files.
2. Inspects the discovered files using AST.
3. Collects project information.
4. Sends the information to Groq.
5. Receives generated Markdown documentation.
6. Writes the output to `README.md` in the current working directory.

If a README already exists, DevKit asks for confirmation before overwriting it.

The API key is not hardcoded into the project or automatically saved by the current implementation.

### Run the Project Doctor

```bash
devkit inspect
```

The Project Doctor scans the current project, reports its findings, and provides recommendations for improvement.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| `argparse` | Command-line argument and subcommand handling |
| `sys` | Active Python interpreter information |
| `pathlib` | Filesystem and path management |
| `subprocess` | Interaction with external development tools |
| `os` | Environment variables and directory traversal |
| `ast` | Python source-code inspection |
| `json` | Preparing project information for API requests |
| `requests` | HTTP requests to the Groq API |
| `getpass` | Secure API key prompting |
| `unittest` | Automated testing |
| `unittest.mock` | Mocking dependencies during tests |
| `tempfile` | Isolated temporary directories for testing |
| Groq API | AI-powered README generation |
| setuptools | Python package build system |
| Git and GitHub | Version control and collaboration |

The project prioritizes Python's standard library where practical while using external dependencies where required.

## Target Users

DevKit CLI is intended for:

- Beginner developers learning software development.
- Students learning programming and development workflows.
- Developers who frequently create projects in different programming languages.
- Instructors and mentors helping learners establish consistent project structures.
- Independent developers looking to simplify repetitive setup and documentation tasks.

## Project Scope

DevKit is Python-first. Its CLI, Environment Doctor, and initial Documentation Generator scanner are built around Python.

The Project Generator is language-agnostic and can create folders and empty files for projects written in other languages.

The four core features are:

1. Environment Doctor.
2. Project Generator.
3. Documentation Generator.
4. Project Doctor.

Broader language-aware analysis, advanced templates, multiple AI providers, and additional developer utilities may be considered for future releases.

## Development Roadmap

Development follows an incremental approach.

| Phase | Focus | Status |
|---|---|---|
| 1 | Repository and initial project structure | Completed |
| 2 | CLI foundation, subcommand registration, and command routing | Completed |
| 3 | Environment Doctor | Completed |
| 4 | Project Generator | Implemented and tested; pull request awaiting mentor review |
| 5 | Documentation Generator | V1 implemented and tested; pull request awaiting mentor review |
| 6 | Project Doctor | V1 implemented and tested |
| 7 | Testing, debugging, and refinement | Ongoing |
| 8 | Python package configuration and installation | Implemented and locally tested |
| 9 | External project testing | Completed |
| 10 | Mentor review, release preparation, and PyPI publication | Pending |

The roadmap may be adjusted as development progresses and feedback is received.

## Testing Strategy

DevKit uses Python's `unittest` framework to verify functionality, expected behaviour, and error handling.

The test suite covers:

- **Environment Doctor:** Python version checks, Git detection, and Git error handling.
- **Project Generator:** Project and folder validation, duplicate detection, file mappings, filesystem errors, and protection of existing files.
- **Documentation Generator CLI workflow:** Missing API keys, successful generation, generation failures, overwrite approval and rejection, and file-writing errors.
- **Documentation scanner:** Python file discovery, excluded directories, AST inspection, syntax errors, and unreadable files.
- **AI client:** API key retrieval, successful API responses, request failures, and unexpected response structures.
- **Project Doctor:** Project overview, Python analysis, syntax-error reporting, missing project components, test-directory checks, and recommendations.

### Current Test Results

**53 automated tests passing.**

- Passed: 53
- Failed: 0

Run the complete test suite:

```bash
python3 -m unittest discover -v
```

The tests use temporary directories and mocked dependencies where appropriate to isolate filesystem and API-related operations.

### External Installation Testing

The locally built wheel was installed into a fresh virtual environment and tested from an external project directory.

The following were verified:

- Package installation through pip.
- Automatic installation of the declared `requests` dependency.
- Availability of the `devkit` console command outside the source repository.
- Registration of all four CLI commands.
- Successful execution of `doctor`, `init`, `docs`, and `inspect`.
- Secure API-key prompting when `GROQ_API_KEY` is unavailable to the process.
- Successful README generation in the external project.

## Design Principles

DevKit CLI follows these principles:

- **Simplicity:** Commands should be easy to understand and use.
- **Reliability:** Operations should behave predictably.
- **Safety:** Existing project files should not be overwritten unexpectedly.
- **Clarity:** Errors and diagnostic messages should be understandable.
- **Modularity:** Features should be organized into maintainable components.
- **Testability:** Functionality should be verifiable through automated tests.
- **Flexibility:** Developers should have control over their generated project structures.
- **Accuracy:** Generated documentation should be grounded in the information collected from the project.

## Project Status

**Current stage:** Four core CLI features implemented and tested; package configuration and external installation testing completed. Mentor review and PyPI release preparation remain in progress.

### Completed

- Initial repository and project structure.
- Python package initialization.
- CLI argument parser and command routing.
- Registration of the four core subcommands.
- General CLI help and default help behaviour.
- Environment Doctor implementation and automated tests.
- Project Generator implementation, validation, and automated tests.
- Language-agnostic project structure creation.
- Folder and file mapping validation.
- Filesystem error handling and operation summaries.
- Python project scanner.
- AST-based inspection of functions, classes, and asynchronous functions.
- Python syntax-error detection and reporting.
- Groq API integration.
- Secure API key retrieval.
- JSON-compatible project metadata preparation.
- AI-powered README generation.
- README generation failure handling.
- Existing README overwrite confirmation.
- README filesystem error handling.
- Project Doctor implementation.
- Project structure and configuration checks.
- Actionable project improvement recommendations.
- Automated tests for the scanner, AI client, and CLI features.
- **53 automated tests passing.**
- Python package configuration through `pyproject.toml`.
- Console entry point configuration for the `devkit` command.
- Local wheel and source distribution builds.
- Installation and testing of the wheel in a fresh virtual environment.
- External project testing of all four CLI commands.
- Automatic installation of declared runtime dependencies.

### Currently in progress

- Mentor review of feature pull requests.
- Final packaging and release checks.
- PyPI publication preparation.
- README and development-log synchronization.

### Future improvements

- Multiple AI provider and model selection.
- Language-aware scanning beyond the initial Python scope.
- More advanced project inspection and recommendations.
- Additional development environment checks.
- Expanded documentation customization.
- Advanced project templates and utilities.

This README will be updated throughout development to reflect completed features, new commands, usage instructions, testing results, and changes to project scope.

## Collaboration

Development uses Git and GitHub for version control, collaboration, and code review.

Contributions, feedback, and suggestions are welcome, particularly those that improve usability, reliability, and maintainability.

## License

A license will be selected before public distribution.

---

**DevKit CLI — Build consistently. Develop confidently.**