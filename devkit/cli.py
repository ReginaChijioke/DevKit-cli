import argparse 
import subprocess 
import sys 
from pathlib import Path
parser = argparse.ArgumentParser(
    description="A developer-focused CLI application for project setup, environment diagnostics, documentation generation, and project inspection."
)

sub_parser = parser.add_subparsers()
register_doctor = sub_parser.add_parser("doctor")
register_init = sub_parser.add_parser("init")
register_init.add_argument("project_name")
register_docs = sub_parser.add_parser("docs")
register_inspect = sub_parser.add_parser("inspect")

def run_doctor(parsed_argument):
    system_version = sys.version_info
    if system_version >= (3, 11, 0):
        print(f"Python version: {system_version.major}.{system_version.minor}.{system_version.micro}")
        print("Python version meets the requirement.")
    else:
        print("Python 3.11 or newer is required.")
    
    try:
        git_result = subprocess.run(
            ["git", "status"],
            capture_output=True,
            text=True
        )

        if git_result.returncode == 0:
            print("Git repository detected.")
        else:
            error_message = git_result.stderr
            if "not a git repository" in error_message:
                print("This directory is not a Git repository.")
            else:
                print("Git encountered an error.")
                print(error_message)
    except FileNotFoundError:
        print("Git is not installed or could not be found.")
register_doctor.set_defaults(func=run_doctor)



def run_init(parsed_argument):
    project_name = parsed_argument.project_name
    if not project_name[0].isalpha():
        print("Project name must start with a letter.")
        return 

    for char in project_name:
        if not char.isalnum() and char != "_":
            print("Invalid character detected.")
            return
    print(f"Creating: {project_name}")

    project_path = Path(project_name)
    if project_path.exists():
        print("Project already exists.")
        return
    project_path.mkdir()
    folder_names = input("Enter folder names: ").split(",")
    cleaned_names = []
    for name in folder_names:
        cleaned_name = name.strip()
        if cleaned_name:
            cleaned_names.append(cleaned_name)
    for name in cleaned_names:
        folder_path = project_path / name
        folder_path.mkdir()
    file_names = input("Enter file names: ").split(",")
    cleaned_file_names = []
    for file_name in file_names:
        cleaned_file_name = file_name.strip()
        if cleaned_file_name:
            cleaned_file_names.append(cleaned_file_name)
    for file in cleaned_file_names:
        file_path = folder_path / file
        file_path.touch()
    print("Project created successfully.")
register_init.set_defaults(func=run_init)

def run_docs(parsed_argument):
    print("DevKit Documentation Generator")
register_docs.set_defaults(func=run_docs)

def run_inspect(parsed_argument):
    print("DevKit Project Doctor")
register_inspect.set_defaults(func=run_inspect)

def main():
    parsed_argument = parser.parse_args()
    if hasattr(parsed_argument, "func"):
        getattr(parsed_argument, "func")(parsed_argument)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()