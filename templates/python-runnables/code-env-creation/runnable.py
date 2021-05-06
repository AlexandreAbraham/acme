"""
import dataiku
from dataiku.runnables import Runnable


class MyRunnable(Runnable):
    def __init__(self, project_key, config, plugin_config):
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        self.client = dataiku.api_client()

    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        code_env = self.client.create_code_env("PYTHON", {code_env_name}, "DESIGN_MANAGED", {"pythonInterpreter": "PYTHON36"})

        definition = code_env.get_definition()
        definition["desc"]["installCorePackages"] = True
        definition["desc"]["installJupyterSupport"] = True

        definition["specPackageList"] = {packages_to_install}

        # Save the new settings
        code_env.set_definition(definition)

        # Actually perform the installation
        code_env.update_packages()
        code_env.set_jupyter_support(True)
        return "<span>DONE</span>"
"""