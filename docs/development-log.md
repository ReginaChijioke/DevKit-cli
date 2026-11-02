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