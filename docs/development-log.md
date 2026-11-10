# DevKit CLI — Development Log

## 2 November 2026 — Initial CLI Foundation

### 10:00 WAT — Initial CLI Foundation

### 1. Objective
Establish the initial Python project structure and build the foundation of the DevKit command-line interface.

### 2. Project Structure

Created the following directories and files:

```text
devkit-cli/
├── devkit/
│   ├── __init__.py
│   └── cli.py
├── tests/
├── docs/
├── README.md
└── .gitignore
```

### 3. Implementation

Implemented the initial command-line parser in `devkit/cli.py`.

The implementation includes:
- Importing Python's built-in `argparse` module.
- Creating an `ArgumentParser` instance.
- Setting the application's description.
- Using `parse_args()` to process command-line arguments.

### 4. Concepts Learned

- `argparse`: Python's built-in module for handling command-line arguments.
- `ArgumentParser()`: Creates an argument parser.
- `description`: Provides information about the application.
- `parse_args()`: Processes supplied command-line arguments and returns a Namespace object.
- Python packages: Understanding the purpose of `__init__.py`.

### 5. Testing

**Command executed:**

`python3 -m devkit.cli --help`

**Result:** Successful.

The application displayed:
- Usage information.
- The DevKit application description.
- The default `-h` and `--help` options.

### 6. Challenges Encountered

Initially attempted to execute the application using `python`, but the terminal returned:

`zsh: command not found: python`

Resolved this by using `python3`, which successfully executed the application.

---

### 13:32 WAT — CLI Subcommands and Command Routing

### 7. Objective

Extend the initial CLI foundation by registering DevKit's four commands and connecting each command to its respective function.

### 8. Implementation

Implemented four CLI subcommands using `argparse` subparsers:

- `doctor` — Environment Doctor.
- `init` — Project Generator.
- `docs` — Documentation Generator.
- `inspect` — Project Doctor.

Created placeholder functions for each command and associated them with their respective subparsers using `set_defaults()`.

Implemented command routing using:
- `hasattr()` to check whether the parsed arguments contain a `func` attribute.
- `getattr()` to retrieve the function associated with the selected command.
- Dynamic function execution to execute the retrieved function.

### 9. Concepts Learned

- `add_subparsers()`: Creates a collection for registering subcommands.
- `add_parser()`: Registers individual subcommands.
- `set_defaults()`: Associates a function with a subcommand.
- Function references versus function calls.
- `hasattr()` and `getattr()`.
- Dynamic function execution.
- Python execution order.

### 10. Testing

All four commands were successfully tested:

| Command | Result |
|---|---|
| `python3 -m devkit.cli doctor` | Passed |
| `python3 -m devkit.cli init` | Passed |
| `python3 -m devkit.cli docs` | Passed |
| `python3 -m devkit.cli inspect` | Passed |

Additional tests:

- `python3 -m devkit.cli --help` — Successfully displayed all four registered commands.
- `python3 -m devkit.cli` — Exited without displaying an error or help message.

### 11. Challenges Encountered

Initially, the `doctor` command executed without producing output.

After investigating the execution order, identified that `parse_args()` was being called before the command functions were defined and associated with their respective subparsers.

Reorganised the implementation so that function definitions and command mappings occur before argument parsing.

Retested the `doctor` command successfully.

### 12. Current Project Status

**Completed:**
- Initial project structure.
- Python package initialization.
- Basic argument parser.
- Application description.
- Default help functionality.
- Registration of all four CLI subcommands.
- Placeholder functions for all four commands.
- Command-to-function mappings.
- Dynamic command routing.
- Manual testing of all four commands.

**Pending:**
- Displaying the general help message when DevKit is launched without a command.
- Implementing actual functionality behind the four commands.
- Adding automated tests.

### 13. Next Development Milestone

Improve the default CLI behaviour when no subcommand is supplied, then begin implementing the actual functionality behind the registered commands.

## 3 November 2026 — CLI Behaviour Refinement

### 9:46 AM WAT — Default CLI Help Behaviour

**Objective:**

Improve the default behaviour of DevKit CLI when the application is executed without specifying a subcommand.

**Work completed:**
- Identified that running the CLI without a command resulted in no output.
- Introduced an `else` branch to handle situations where no command function is attached to the parsed arguments.
- Implemented `parser.print_help()` to display general CLI usage information.
- Preserved the existing command execution and routing logic.

**Concepts explored:**
- Conditional branching using `if` and `else`.
- Method references versus method calls.
- Executing methods using parentheses.
- Default application behaviour.
- Improving command-line user experience.

**Testing:**

Executed:

`python3 -m devkit.cli`

**Result:** Successfully displayed the general CLI help information.

Also verified that:

`python3 -m devkit.cli doctor`

Continued to execute the Environment Doctor placeholder function correctly.

**Outcome:**

DevKit CLI now displays useful usage information when launched without a subcommand instead of exiting silently.

The four registered subcommands and their existing routing behaviour remain functional.

**Next steps:**
- Begin implementing the Environment Doctor.
- Check Python installation and version.
- Expand environment diagnostics incrementally.
- Introduce automated tests as functionality develops.

### 5:02 PM WAT — Initial Environment Diagnostics

**Work completed:**
- Implemented a Python availability check using `subprocess.run()`.
- Captured and processed Python version output.
- Added validation to ensure Python 3.11 or newer is available.
- Added exception handling for missing Python executables.
- Implemented a Git repository check using `git status`.
- Added exception handling for missing Git executables.
- Organized Python and Git checks into separate `try/except` blocks.

**Testing performed:**
- Confirmed Python 3.12.3 is detected and meets the minimum version requirement.
- Tested the missing-Python executable scenario.
- Confirmed Git repository detection works in the DevKit project directory.

**Design decision:**
DevKit will not automatically initialize Git when a directory is not a repository. It will ask the user for permission before running `git init`.

**Next steps:**
- Improve Git error detection.
- Implement the interactive Git initialization prompt.
- Expand Environment Doctor diagnostics.
- Add automated tests.

## 4 November 2026 — Environment Doctor Implementation

**Time:** 10:48 AM (WAT)

### Milestone: Environment Doctor completed

Implemented and tested the Environment Doctor functionality.

### 1. Python Environment Check
- Replaced the previous `subprocess.run(["python3", "--version"])` approach with Python's built-in `sys.version_info`.
- The check now identifies the version of the exact Python interpreter running DevKit.
- Added a minimum Python version requirement of **Python 3.11**.
- Used the `major`, `minor`, and `micro` attributes to display the detected Python version.
- Added clear output indicating whether the active Python interpreter meets the requirement.

### 2. Git Environment Check
- Implemented Git repository detection using `subprocess.run()`.
- Added handling for directories that are not Git repositories.
- Added handling for other Git-related errors.
- Added `FileNotFoundError` handling for cases where Git is unavailable.

### 3. Unit Testing
Updated `tests/test_cli.py` to reflect the new implementation.

The test suite now contains six tests covering:
1. Python version meets the requirement.
2. Python version is below the requirement.
3. Git repository is detected.
4. Directory is not a Git repository.
5. Git encounters another error.
6. Git executable is missing.

**Test result:** All 6 tests passed.

Command used:

`python3 -m unittest discover -s tests -v`

### 4. Manual Verification

Executed:

`python3 -m devkit.cli doctor`

Output:

```text
Python version: 3.12.3
Python version meets the requirement.
Git repository detected.
```

### 5. Key Learning Outcomes
- Understood the difference between checking a Python executable through `subprocess` and checking the active interpreter through `sys.version_info`.
- Learned how named tuples expose values through attributes.
- Practised mocking Python attributes and subprocess calls in unit tests.
- Improved error handling and diagnostic reporting.

### Status
**Environment Doctor: Implemented and tested successfully.**

# DevKit CLI — Development Log

## 6 November 2026 — Project Generator Implementation

**Time:** 1:43 PM WAT

### Milestone: Initial Project Generator Implementation

Implemented the initial Project Generator functionality for DevKit CLI.

### Features Implemented

- Added project name validation.
- Ensured project names start with a letter.
- Restricted project names to alphanumeric characters and underscores.
- Added a check to prevent creating a project in an existing path.
- Implemented project directory creation using `pathlib`.
- Added interactive input for users to specify their preferred folder structure.
- Used `split(",")` to separate comma-separated folder names.
- Used `strip()` to remove unnecessary whitespace.
- Skipped empty folder names.
- Created the requested folders inside the project directory.

### Manual Testing

1. Successfully created a project using `python3 -m devkit.cli init weather_app`.
2. Attempted to create the same project again and confirmed that the existing-project check works.
3. Tested an invalid project name (`weather-app`) and confirmed that validation rejects it.

### Concepts Practised

- `pathlib.Path`
- `.exists()` and `.mkdir()`
- `input()` and `.split()`
- `.strip()`
- List creation and `.append()`
- Conditional validation
- Iterating through lists with `for` loops
- Returning early when validation fails

### Design Decisions

- Users can customize their project folder structure instead of being restricted to a predefined template.
- Project creation uses interactive terminal input.
- DevKit will create empty files only; users remain responsible for writing their own code and file contents.

### Current Status

The initial project directory and folder generation functionality is implemented.

### Next Steps

- Implement grouped file input so users can specify which files belong in each folder.
- Create empty files in the requested locations.
- Add automated tests for the Project Generator.

## 10 November 2026 — Project Generator Enhancement and Validation

**Time:** 2:05 PM WAT

### Milestone: Customizable Project Structure, File Mapping, and Input Validation

Continued development of the Project Generator by extending its initial folder-generation functionality to support grouped file creation and stronger input validation.

### 1. Features Implemented

**A. Grouped File Input and File Creation**

- Implemented interactive input for specifying which files belong in each folder.
- Introduced a folder-to-file mapping format using a colon (`:`).
- Used `partition(":")` to separate the destination folder from its associated filenames.
- Supported comma-separated filenames within each mapping.
- Used `strip()` to remove unnecessary whitespace from folder names and filenames.
- Added support for `root` as a special destination representing the project root directory.
- Allowed users to create files directly in the project root or inside previously created folders.
- Used `pathlib` path joining to construct file destinations.
- Used `.touch()` to create empty files.

**B. Folder Mapping Validation**

- Added validation to ensure that each mapping contains the expected colon separator.
- Rejected mappings that reference folders that were not created.
- Prevented invalid mappings from interrupting the remaining file-generation process.

**C. Filename Validation**

- Added filename validation to prevent users from specifying nested paths instead of individual filenames.
- Used `Path().name` to compare the supplied filename with its final path component.
- Rejected empty filenames, `.` and `..`.
- Allowed simple filenames, including dotfiles such as `.gitignore`.
- Ensured invalid filenames are skipped rather than passed to file creation.

**D. Folder-Name Validation**

- Required folder names to begin with an alphabetic character.
- Restricted folder names to alphanumeric characters, underscores, and hyphens.
- Rejected directory traversal entries such as `.` and `..`.
- Rejected folder names containing path separators or spaces.
- Ensured invalid folder names are not added to the list of accepted folder names.

**E. Duplicate Folder Detection**

- Added a check to determine whether a folder name already exists in the accepted folder-name list.
- Rejected duplicate folder names before directory creation.
- Prevented repeated folder creation from causing `FileExistsError`.

### 2. Design Decisions

The following decisions were established during this implementation milestone:

**Customizable Project Structures**

- Users should be able to define their own project folder structures rather than being restricted to predefined templates.
- Folder creation should remain interactive, allowing users to specify multiple folders in one input.

**Grouped File Mapping**

- Files should be specified according to their destination folders rather than collected as one unstructured list.
- The colon (`:`) separates a destination folder from its associated filenames.
- Commas separate multiple filenames within the same destination.
- The special destination `root` represents the project directory itself.

**Empty File Creation**

- DevKit should create empty files rather than populate them with starter code or predefined content.
- Developers retain control over the contents of their generated files.

**Input Validation and Safety**

- Folder and filename inputs must be validated before filesystem operations are performed.
- Invalid entries should be rejected without terminating the entire project-generation process.
- Duplicate folder names should be detected before attempting directory creation.
- File mappings should only target the project root or folders that were successfully created.

**Incremental Error Handling**

- Invalid folder names, filenames, and mappings should produce understandable messages.
- Where possible, an invalid entry should be skipped while allowing the generator to process subsequent valid entries.

### 3. Example of the Project Generator Input Format

```text
python3 -m devkit.cli init weather_app

Enter folder names: src, tests, config

Enter folder/file mapping:
src: main.py, config.py
tests: test_main.py
root: README.md, .gitignore
```

This approach allows users to define both their folder structure and the placement of empty files during project initialization.

### 4. Manual Testing

The following behaviours were manually tested:

1. Successfully created projects with multiple user-selected folders.
2. Successfully created empty files inside specified folders.
3. Successfully created empty files directly in the project root using `root`.
4. Rejected filenames containing nested paths, such as `src/main.py`.
5. Rejected parent-directory references such as `..`.
6. Rejected invalid folder names, including names beginning with numbers, names containing spaces, and path-based entries.
7. Confirmed that valid folder names containing underscores and hyphens are accepted.
8. Confirmed that duplicate folder names are rejected without causing a filesystem error.
9. Confirmed that invalid folder entries do not prevent valid folders from being created.

### 5. Automated Testing

Expanded the Project Generator test coverage by adding tests for folder validation and duplicate folder detection.

**Environment Doctor:**
- Seven automated tests.

**Project Generator:**
- Successful project and file creation.
- Invalid project-name rejection.
- Existing-project detection.
- Invalid filename-path rejection.
- Parent-directory filename rejection.
- Invalid folder mapping rejection.
- Invalid mapping format rejection.
- Invalid folder-name rejection.
- Duplicate folder-name rejection.

**Test execution:**

```bash
python3 -m unittest discover -s tests -v
```

**Results:**
- Total tests: 16
- Passed: 16
- Failed: 0

All 16 automated tests passed successfully.

### 6. Concepts Practised

- `pathlib.Path`
- `.exists()`, `.mkdir()`, and `.touch()`
- `Path.name` and path joining
- `str.partition()`
- `.split()` and `.strip()`
- String validation using `.isalpha()` and `.isalnum()`
- Character-by-character validation
- Boolean flags for validation
- `break` and `continue`
- Membership testing with `in`
- List creation and `.append()`
- Nested loops and conditional logic
- Filesystem safety and input validation
- Automated testing with `unittest`
- Temporary directories with `tempfile`
- Mocking interactive input with `unittest.mock`

### 7. Current Status

The Project Generator now supports:

- Project directory creation.
- Custom folder creation.
- Folder-name validation.
- Duplicate folder detection.
- Grouped folder-to-file mappings.
- Project-root file placement.
- Empty file creation.
- Filename and mapping validation.
- Automated tests covering its current functionality.

The Project Generator remains in progress while additional refinement, filesystem error handling, and review are considered.

### 8. Next Steps

- Review the complete Project Generator implementation for edge cases.
- Identify and handle any remaining filesystem errors.
- Review the automated tests for completeness.
- Update the development documentation as further improvements are made.
- Complete the Project Generator milestone before moving to Documentation Generation.