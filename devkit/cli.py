import argparse 
import subprocess 
parser = argparse.ArgumentParser(
    description="A developer-focused CLI application for project setup, environment diagnostics, documentation generation, and project inspection."
)

sub_parser = parser.add_subparsers()
register_doctor = sub_parser.add_parser("doctor")
register_init = sub_parser.add_parser("init")
register_docs = sub_parser.add_parser("docs")
register_inspect = sub_parser.add_parser("inspect")

def run_doctor():
    try:

        result = subprocess.run(
            ["python3" , "--version"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            python_version = result.stdout.strip()
            print(python_version)
            split_string = python_version.split()
            version_number = split_string[1]
            version_parts = version_number.split(".")
            converted_numbers = []
            for part in version_parts:
                convert_part = int(part)
                converted_numbers.append(convert_part)
            detected_version = tuple(converted_numbers)

            if detected_version >= (3, 11, 0):
                print("Python version meets the requirement.")
            else:
                print("Python 3.11 or newer is required.")
        else:
            print("Python version check failed.")
    except FileNotFoundError:
        print("Python could not be found.")

    try:
        git_result = subprocess.run(
            ["git", "status"],
            capture_output=True,
            text=True
        )

        if git_result.returncode == 0:
            print("Git repository detected.")
        else:
            print("This directory is not a Git repository.")
    except FileNotFoundError:
        print("Git is not installed or could not be found.")
register_doctor.set_defaults(func=run_doctor)



def run_init():
    print("DevKit Project Generator")
register_init.set_defaults(func=run_init)

def run_docs():
    print("DevKit Documentation Generator")
register_docs.set_defaults(func=run_docs)

def run_inspect():
    print("DevKit Project Doctor")
register_inspect.set_defaults(func=run_inspect)

parsed_argument = parser.parse_args()
if hasattr(parsed_argument, "func"):
    getattr(parsed_argument, "func")()
else:
    parser.print_help()

