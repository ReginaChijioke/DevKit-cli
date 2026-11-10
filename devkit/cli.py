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
        if not cleaned_name:
            continue
        if cleaned_name == "." or cleaned_name == "..":
            print("Invalid folder name.")
            continue
        if not cleaned_name[0].isalpha():
            print("Invalid folder name.")
            continue
        folder_valid = True 
        for char in cleaned_name:
            if not char.isalnum() and char != "_" and char != "-":
                folder_valid = False
                break
        if folder_valid is False:
            print("Invalid folder name.")
            continue
        if cleaned_name in cleaned_names:
            print("Duplicate folder name.")
            continue
        else:
            cleaned_names.append(cleaned_name) 

    for name in cleaned_names:
        folder_path = project_path / name
        folder_path.mkdir()
    grouped_file_entries = []
    while True:
        folder_file_mapping = input("Enter folder/file mapping: ")
        if folder_file_mapping == "":
            break
        else:
            grouped_file_entries.append(folder_file_mapping)
    for entry in grouped_file_entries:
        folder, separator, files = entry.partition(":")
        if separator == "":
            print("Invalid folder/file format.")
            continue

        cleaned_folder = folder.strip()
        if cleaned_folder == "root":
            destination_path = project_path
        elif cleaned_folder not in cleaned_names:
            print("Folder does not exist")
            continue
        else:
            destination_path = project_path / cleaned_folder 
        split_files = files.split(",")
        cleaned_file_names = []
        for each_file in split_files:
            stripped_file = each_file.strip()
            if stripped_file == "":
                continue
            file_name = Path(stripped_file).name
            if stripped_file != file_name:
                print("Invalid filename")
                continue
            if file_name == "" or file_name == "." or file_name == "..":
                print("Invalid filename")
                continue
            cleaned_file_names.append(file_name)
        for file in cleaned_file_names:
            create_path = destination_path / file
            create_path.touch()

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