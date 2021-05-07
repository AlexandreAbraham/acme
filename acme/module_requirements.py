import subprocess
import importlib
import shutil
from pathlib import Path


def get_requirements(module, package_name=None):
    if not package_name:
        module_name = module.__module__
        package_name = module_name.split(".")[0]
        print(f"Identified package name: {package_name}. If invalid, please specify the real package name to retrieve the requirements.")
    try:
        requirements_entry = subprocess.check_output(f"pipdeptree -p {package_name} --warn silence | grep -E '^\w+'", shell=True)
    except subprocess.CalledProcessError:
        requirements_entry = None
        print("No requirement was retrieved")
    if requirements_entry:
        parsed_requirements = str(requirements_entry, "utf-8")
        requirements_list = parsed_requirements.split("\n")[:-1]
        print(f"Packages retrieved: {requirements_list}")
    else:
        requirements_list = []
    return requirements_list


def requirements_from_local_lib(clazz):
    module_name = clazz.__module__
    package_name = module_name.split(".")[0]
    package = importlib.import_module(package_name)

    path = Path(package.__path__[0])

    requirements_list = []
    requirements = path.parent / 'requirements.txt'
    if requirements.exists():
        with open('requirements.txt') as f:
            requirements_list = f.read().splitlines()

    return dict(requirements=requirements_list, copy_source=str(path))