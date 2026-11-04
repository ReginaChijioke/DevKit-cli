import argparse 
import subprocess 
import sys 
parser = argparse.ArgumentParser(
    description="A developer-focused CLI application for project setup, environment diagnostics, documentation generation, and project inspection."
)

sub_parser = parser.add_subparsers()
register_doctor = sub_parser.add_parser("doctor")
register_init = sub_parser.add_parser("init")
register_docs = sub_parser.add_parser("docs")
register_inspect = sub_parser.add_parser("inspect")

def run_doctor():
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



def run_init():
    print("DevKit Project Generator")
register_init.set_defaults(func=run_init)

def run_docs():
    print("DevKit Documentation Generator")
register_docs.set_defaults(func=run_docs)

def run_inspect():
    print("DevKit Project Doctor")
register_inspect.set_defaults(func=run_inspect)

def main():
    parsed_argument = parser.parse_args()
    if hasattr(parsed_argument, "func"):
        getattr(parsed_argument, "func")()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()