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
        versions = ['PYTHON311', 'PYTHON312']
        code_env = None
        for version in versions:
            try:
                code_env = self.client.create_code_env('PYTHON', 'neuralk', 'DESIGN_MANAGED', {'pythonInterpreter': version})
            except:
                continue
            break
        else:
            raise ValueError('Python version error. No version available in ' + str(versions))

        definition = code_env.get_definition()
        definition["desc"]["installCorePackages"] = True
        definition["desc"]["corePackagesSet"] = "AUTO"
        definition["desc"]["installJupyterSupport"] = False

        definition["specPackageList"] = {packages_to_install}

        # Save the new settings
        code_env.set_definition(definition)

        # Actually perform the installation
        code_env.update_packages()
        return "<span>DONE</span>"
"""
