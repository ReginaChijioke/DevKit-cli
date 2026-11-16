# DevKit CLI

**Build consistently. Develop confidently.**

A Python-first command-line developer tool designed to simplify project initialization, environment checks, AI-powered documentation generation, and project inspection. Its Project Generator supports customizable project structures across programming languages.

## Overview

DevKit CLI helps developers reduce repetitive work involved in creating and maintaining software projects.

Starting a new project often involves manually creating directories, configuring development environments, preparing documentation, and checking project structures. These tasks can be time-consuming and may lead to inconsistent setups.

DevKit CLI brings these workflows together through a collection of command-line tools.

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
- Handles unsuccessful README generation.
- Checks whether a `README.md` already exists.
- Requests user confirmation before overwriting an existing README.
- Handles filesystem errors when writing the generated documentation.

**Current V1 scope:**

- Groq is the AI provider.
- One model is configured: `openai/gpt-oss-120b`.
- The scanner focuses on Python projects.
- The generated output is a Markdown `README.md` file.
- The generator scans the current working directory.

**Future improvements:**

- Support additional AI providers and models.
- Allow users to select their preferred AI model.
- Expand language-aware project analysis.
- Improve API response validation and request reliability.
- Add more documentation customization options.

### 4. Project Doctor

The Project Doctor is planned as a project inspection tool. Its initial scope will focus on Python projects.

**Planned capabilities:**

- Check for expected project files and directories.
- Identify missing or incorrectly organized components.
- Report potential configuration issues.
- Provide actionable recommendations for improvement.

## Current CLI Commands

The CLI uses Python's `argparse` module for command registration and routing.

| Command | Purpose | Current behaviour |
|---|---|---|
| `doctor` | Environment Doctor | Checks the active Python version, Git availability, and repository status. |
| `init` | Project Generator | Creates customizable project directories, folders, and empty files. |
| `docs` | Documentation Generator | Scans the current Python project and generates an AI-powered README using Groq. |
| `inspect` | Project Doctor | Displays the Project Doctor introduction; inspection functionality is planned. |

When DevKit is executed without a subcommand, it displays the general CLI help information.

## Getting Started

### Requirements

- Python 3.11 or later.
- Git for version control and collaboration.
- A Groq API key for the Documentation Generator.
- `requests` for the current Groq API integration.

### Installation

Clone the repository:

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

Install the current external API dependency:

```bash
python3 -m pip install requests
```

Dependency packaging and automated installation for end users will be addressed when DevKit is prepared for distribution.

### Running the CLI

Display general help:

```bash
python3 -m devkit.cli
```

Display available commands:

```bash
python3 -m devkit.cli --help
```

### Run the Environment Doctor

```bash
python3 -m devkit.cli doctor
```

### Run the Project Generator

```bash
python3 -m devkit.cli init weather_app
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
python3 -m devkit.cli docs
```

The Documentation Generator:

1. Scans the current working directory for Python files.
2. Inspects the discovered files using AST.
3. Collects project information.
4. Sends the information to Groq.
5. Receives generated Markdown documentation.
6. Writes the output to `README.md`.

If a README already exists, DevKit asks for confirmation before overwriting it.

The API key is not hardcoded into the project or automatically saved by the current implementation.

### Run the Project Doctor

```bash
python3 -m devkit.cli inspect
```

The command is registered, but its project inspection functionality is still planned.

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
| 5 | Documentation Generator | V1 implemented and tested |
| 6 | Project Doctor | Planned |
| 7 | Testing, debugging, and refinement | Ongoing |

The roadmap may be adjusted as development progresses and feedback is received.

## Testing Strategy

DevKit uses Python's `unittest` framework to verify functionality, expected behaviour, and error handling.

The test suite covers:

- Environment Doctor: Python version checks, Git detection, and Git error handling.
- Project Generator: project and folder validation, duplicate detection, file mappings, filesystem errors, and protection of existing files.
- Documentation Generator CLI workflow: missing API keys, successful generation, generation failures, overwrite approval and rejection, and file-writing errors.
- Documentation scanner: Python file discovery, excluded directories, AST inspection, syntax errors, and unreadable files.
- AI client: API key retrieval, successful API responses, request failures, and unexpected response structures.

### Current test results

**44 automated tests passing.**

- Passed: 44
- Failed: 0

Run the complete test suite:

```bash
python3 -m unittest discover -s tests -v
```

The tests use temporary directories and mocked dependencies where appropriate to isolate filesystem and API-related operations.

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

**Current stage:** CLI foundation, Environment Doctor, Project Generator, and Documentation Generator V1 implemented.

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
- Groq API integration.
- Secure API key retrieval.
- JSON-compatible project metadata preparation.
- AI-powered README generation.
- README generation failure handling.
- Existing README overwrite confirmation.
- README filesystem error handling.
- Automated tests for the scanner, AI client, and Documentation Generator workflow.
- **44 automated tests passing.**

### Currently in progress

- Mentor review of the Project Generator pull request.
- Continued refinement and testing of Documentation Generator V1.
- README and development-log synchronization.

### Not yet implemented

- Project Doctor inspection functionality.
- Multiple AI provider and model selection.
- Language-aware scanning beyond the initial Python scope.
- Automated dependency installation and packaging for distribution.

This README will be updated throughout development to reflect completed features, new commands, usage instructions, testing results, and changes to project scope.

## Collaboration

Development uses Git and GitHub for version control, collaboration, and code review.

Contributions, feedback, and suggestions are welcome, particularly those that improve usability, reliability, and maintainability.

## License

A license will be selected before public distribution.

---

**DevKit CLI — Build consistently. Develop confidently.**