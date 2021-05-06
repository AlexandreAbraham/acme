import subprocess


def get_requirements(module, package_name=None):
    if not package_name:
        module_name = module.__module__
        package_name = module_name.split(".")[0]
    requirements_entry = subprocess.check_output(f"pipdeptree -p {package_name} --warn silence | grep -E '^\w+'", shell=True)
    parsed_requirements = str(requirements_entry, "utf-8")
    requirements_list = parsed_requirements.split("\n")[:-1]
    return requirements_list
