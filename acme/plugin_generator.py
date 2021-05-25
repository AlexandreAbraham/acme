import json
import shutil
from pathlib import Path

from . import templates
from .constants import python_recipe_template, DSSType, custom_fit_template, custom_predict_template, model_wrapper_template, macro_template


class PluginGenerator:

    def __init__(self, plugin_name, plugin_description, doc_url="", requirements=None, copy_source=None):
        if requirements is None:
            requirements = []
        self.plugin_name = plugin_name
        self.plugin_description = plugin_description
        self.doc_url = doc_url
        self.plugin_repository = f"dss-plugin-{plugin_name}"
        self.template_repository = Path(templates.PATH)
        self.requirements = add_dss_packages(requirements)
        self.copy_source = copy_source

    def write_base(self):
        Path(self.plugin_repository).mkdir(parents=True, exist_ok=True)
        self._write_plugin_json()

        self._write_python_lib()
        self._write_license()
        if self.requirements:
            self._create_code_env_macro()

    def write_refined_function(self, refined_module):
        self._write_algo_json(refined_module)
        wrapped = self._write_model_wrapper(refined_module)
        self._write_algo_py(refined_module, wrapped=wrapped)

    def generate_zip(self):
        shutil.make_archive(f"dss-plugin-{self.plugin_name}", "zip", self.plugin_repository)

    def _write_plugin_json(self):
        with open(f"{self.template_repository}/plugin_base/plugin.json") as plugin_json_file:
            plugin_dict = json.load(plugin_json_file)
        plugin_dict["id"] = self.plugin_name
        plugin_dict["meta"]["label"] = self.plugin_name
        plugin_dict["meta"]["description"] = self.plugin_description
        plugin_dict["meta"]["url"] = self.doc_url

        with open(f"{self.plugin_repository}/plugin.json", "w") as outfile:
            json.dump(plugin_dict, outfile, indent=4)

    def _write_algo_json(self, refined_module):
        with open(f"{self.template_repository}/plugin_model/python-prediction-algos/test-plugin_my-algo/algo.json") as algo_json_file:
            algo_dict = json.load(algo_json_file)
        algo_dict["meta"]["label"] = refined_module.module_name
        algo_dict["meta"]["description"] = refined_module.module_short_description
        algo_dict["predictionTypes"] = refined_module.prediction_type.value
        for parameter in refined_module.parameters:
            if parameter.get('selected', True):
                algo_dict["params"].append(parameter.get_dss_json())

        algorithm_name = refined_module.module_name
        Path(f"{self.plugin_repository}/python-prediction-algos/{algorithm_name}").mkdir(parents=True, exist_ok=True)
        with open(f"{self.plugin_repository}/python-prediction-algos/{algorithm_name}/algo.json", "w") as outfile:
            json.dump(algo_dict, outfile, indent=4)

    def _write_algo_py(self, refined_module, wrapped=False):
        if wrapped:
            import_statement = f"from model_wrapper import Wrapped{refined_module.module_name} as {refined_module.module_name}"
        else:
            import_statement = refined_module.import_statement
        
        random_state_code_snippet = ""
        if self.has_random_state_param(refined_module):
            random_state_code_snippet = "random_state = formatted_parameters.get('random_state', None)"

        formatted_code = python_recipe_template.format(
            import_statement=import_statement, module_name=refined_module.module_name,
            random_state_snippet=random_state_code_snippet)
        with open(f"{self.plugin_repository}/python-prediction-algos/{refined_module.module_name}/algo.py", "w") as outfile:
            outfile.write(formatted_code)

    def _write_python_lib(self):
        f = open(f"{self.template_repository}/plugin_base/python-lib/testplugin/dku_utils.py", "r")
        util_script = f.read()

        python_lib_path = Path(self.plugin_repository) / 'python-lib'
        python_lib_path.mkdir(parents=True, exist_ok=True)
        with open(python_lib_path / 'dku_utils.py', "w") as outfile:
            outfile.write(util_script)
        if self.copy_source is not None:
            shutil.copytree(self.copy_source, str(python_lib_path / Path(self.copy_source).name))

    def _write_model_wrapper(self, refined_module):
        custom_fit = refined_module.custom_fit
        custom_predict = refined_module.custom_predict

        if custom_fit is None and custom_predict is None:
            return False

        fit = ''
        if custom_fit:
            fit = custom_fit_template.format(class_name=refined_module.module_name, **custom_fit)

        predict = ''
        if custom_predict:
            predict = custom_predict_template.format(class_name=refined_module.module_name, **custom_predict)

        wrapper = model_wrapper_template.format(import_statement=refined_module.import_statement, class_name=refined_module.module_name, fit=fit, predict=predict)
        Path(f"{self.plugin_repository}/python-lib").mkdir(parents=True, exist_ok=True)
        with open(f"{self.plugin_repository}/python-lib/model_wrapper.py", "w") as outfile:
            outfile.write(wrapper)
        return True

    def _write_license(self):
        f = open(f"{self.template_repository}/plugin_base/LICENSE", "r")
        util_script = f.read()

        with open(f"{self.plugin_repository}/LICENSE", "w") as outfile:
            outfile.write(util_script)

    def _create_code_env_macro(self):
        Path(f"{self.plugin_repository}/python-runnables/code-env-creation").mkdir(parents=True, exist_ok=True)
        with open(f"{self.template_repository}/python-runnables/code-env-creation/runnable.json") as macro_json_file:
            macro_dict = json.load(macro_json_file)
        with open(f"{self.plugin_repository}/python-runnables/code-env-creation/runnable.json", "w") as outfile:
            json.dump(macro_dict, outfile, indent=4)

        code_env_name = f"{self.plugin_name}-macro"
        packages_to_install = ("\\n").join(self.requirements)
        formatted_macro_code = macro_template.format(code_env_name=code_env_name, packages_to_install=packages_to_install)
        with open(f"{self.plugin_repository}/python-runnables/code-env-creation/runnable.py", "w") as outfile:
            outfile.write(formatted_macro_code)

    def has_random_state_param(self, refined_module):
        for parameter in refined_module.parameters:
            if "random_state" == parameter['name']:
                return True
        return False


def add_dss_packages(requirements):
    dss_packages = ["scikit-learn>=0.20,<0.21", "scipy>=1.2,<1.3", "xgboost==0.82", "statsmodels>=0.10,<0.11", "jinja2>=2.10,<2.11", "flask>=1.0,<1.1",
                    "cloudpickle>=1.3,<1.6"]
    return dss_packages + requirements


def accepts_unique_int_value(parameter):
    return parameter.get("name") == "random_state"
