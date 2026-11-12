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
    if not project_name:
        print("Project name cannot be empty.")
        return
    if not project_name[0].isalpha():
        print("Project name must start with a letter.")
        return 

    for char in project_name:
        if not char.isalnum() and char != "_":
            print("Invalid character detected.")
            return
    print(f"Creating: {project_name}")

    try:
        project_path = Path(project_name)
        if project_path.exists():
            print("Project already exists.")
            return
        project_path.mkdir()
    except PermissionError:
        print("Permission denied: unable to create project directory.")
        return 
    except OSError as error:
        print(f"Could not create project directory: {error}")
        return
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
    successful_folders = 0
    failed_folders = 0
    for name in cleaned_names:
        try:
            folder_path = project_path / name
            folder_path.mkdir()
            successful_folders += 1
        except OSError as error:
            failed_folders += 1
            print(f"Could not create {name}: {error}")
    grouped_file_entries = []
    while True:
        folder_file_mapping = input("Enter folder/file mapping: ")
        if folder_file_mapping == "":
            break
        else:
            grouped_file_entries.append(folder_file_mapping)
    successful_files = 0
    failed_files = 0
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
            if not destination_path.is_dir():
                print("Folder path does not exist.")
                continue
        split_files = files.split(",")
        cleaned_file_names = []
        for each_file in split_files:
            stripped_file = each_file.strip()
            if stripped_file == "":
                continue
            if len(stripped_file.split()) > 1:
                print("Invalid filename: spaces are not allowed.")
                failed_files += 1
                continue
            file_name = Path(stripped_file).name
            if stripped_file != file_name:
                print("Invalid filename")
                failed_files += 1
                continue
            if file_name == "" or file_name == "." or file_name == "..":
                print("Invalid filename")
                failed_files += 1
                continue
            if file_name in cleaned_file_names:
                print("Duplicate filename.")
                failed_files += 1
                continue
            cleaned_file_names.append(file_name)
        for file in cleaned_file_names:
            create_path = destination_path / file
            if create_path.exists():
                print("File already exists.")
                continue
            try: 
                create_path.touch()
                successful_files += 1
            except OSError as error:
                failed_files += 1
                print(f"Could not create {file}:{error} ")
    print("Folders:")
    print(f"{successful_folders} created successfully.")
    print(f"{failed_folders} failed to create.")
    print("Files:")
    print(f"{successful_files} created successfully.")
    print(f"{failed_files} failed to create.")
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