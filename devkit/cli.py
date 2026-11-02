import argparse 
parser = argparse.ArgumentParser(
    description="A developer-focused CLI application for project setup, environment diagnostics, documentation generation, and project inspection."
)

sub_parser = parser.add_subparsers()
register_doctor = sub_parser.add_parser("doctor")
register_init = sub_parser.add_parser("init")
register_docs = sub_parser.add_parser("docs")
register_inspect = sub_parser.add_parser("inspect")

def run_doctor():
    print("DevKit Environment Doctor")
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
    