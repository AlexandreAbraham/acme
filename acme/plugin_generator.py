import json
import shutil
from pathlib import Path

from .acme_constants import python_recipe_template, DSSType, custom_fit_template, custom_predict_template, model_wrapper_template, macro_template
from .plugin_parameter import IntPluginParameter, DoublesPluginParameter, StringsPluginParameter, MultiSelectPluginParameter
from . import templates


class PluginGenerator:

    def __init__(self, prediction_type, refined_function, doc_url="", generate_plugin_zip=False, requirements=None, import_name=None):
        if requirements is None:
            requirements = []
        self.refined_module = refined_function
        self.import_name = import_name or refined_function.import_name
        if self.import_name is None:
            raise(ValueError('Import name could not be determined, please provide it manually.'))
        self.prediction_type = prediction_type
        self.doc_url = doc_url
        self.plugin_repository = f"dss-plugin-{self.refined_module.module_name}"
        self.template_repository = Path(templates.PATH)
        self.generate_zip = generate_plugin_zip
        self.requirements = add_dss_packages(requirements)

    def write(self):
        self._write_plugin_json()
        algorithm_name = f"{self.refined_module.module_name}_{self.prediction_type.lower()}"
        self._write_algo_json(algorithm_name)
        wrapped = self._write_model_wrapper()
        self._write_algo_py(algorithm_name, wrapped=wrapped)
        self._write_python_lib()
        self._write_license()
        if self.requirements:
            self._create_code_env_macro()
        if self.generate_zip:
            self._make_plugin()

    def _write_plugin_json(self):
        with open(f"{self.template_repository}/plugin_base/plugin.json") as plugin_json_file:
            plugin_dict = json.load(plugin_json_file)
        plugin_dict["id"] = self.refined_module.module_name
        plugin_dict["meta"]["label"] = self.refined_module.module_name
        plugin_dict["meta"]["description"] = self.refined_module.module_long_description.replace("\n", " ")
        plugin_dict["meta"]["url"] = self.doc_url

        Path(self.plugin_repository).mkdir(parents=True, exist_ok=True)
        with open(f"{self.plugin_repository}/plugin.json", "w") as outfile:
            json.dump(plugin_dict, outfile, indent=4)

    def _write_algo_json(self, algorithm_name):
        with open(f"{self.template_repository}/plugin_model/python-prediction-algos/test-plugin_my-algo/algo.json") as algo_json_file:
            algo_dict = json.load(algo_json_file)
        algo_dict["meta"]["label"] = self.refined_module.module_name
        algo_dict["meta"]["description"] = self.refined_module.module_short_description.replace("\n", " ")
        algo_dict["predictionTypes"] = [self.prediction_type]
        for parameter in self.refined_module.parameters:
            if parameter.get('selected', True):
                algo_dict["params"].append(self._format_parameter(parameter))

        Path(f"{self.plugin_repository}/python-prediction-algos/{algorithm_name}").mkdir(parents=True, exist_ok=True)
        with open(f"{self.plugin_repository}/python-prediction-algos/{algorithm_name}/algo.json", "w") as outfile:
            json.dump(algo_dict, outfile, indent=4)

    def _write_algo_py(self, algorithm_name, wrapped=False):
        if wrapped:
            import_statement = f"from model_wrapper import Wrapped{self.refined_module.module_name} as {self.refined_module.module_name}"
        else:
            import_statement = f"from {self.import_name} import {self.refined_module.module_name}"
        formatted_code = python_recipe_template.format(import_statement=import_statement, module_name=self.refined_module.module_name)
        with open(f"{self.plugin_repository}/python-prediction-algos/{algorithm_name}/algo.py", "w") as outfile:
            outfile.write(formatted_code)

    def _write_python_lib(self):
        f = open(f"{self.template_repository}/plugin_base/python-lib/testplugin/dku_utils.py", "r")
        util_script = f.read()

        Path(f"{self.plugin_repository}/python-lib").mkdir(parents=True, exist_ok=True)
        with open(f"{self.plugin_repository}/python-lib/dku_utils.py", "w") as outfile:
            outfile.write(util_script)

    def _write_model_wrapper(self):
        custom_fit = self.refined_module.custom_fit
        custom_predict = self.refined_module.custom_predict

        if custom_fit is None and custom_predict is None:
            return False

        fit = ''
        if custom_fit:
            fit = custom_fit_template.format(class_name=self.refined_module.module_name, **custom_fit)

        predict = ''
        if custom_predict:
            predict = custom_predict_template.format(class_name=self.refined_module.module_name, **custom_predict)

        wrapper = model_wrapper_template.format(import_statement=self.import_name, class_name=self.refined_module.module_name, fit=fit, predict=predict)
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

        code_env_name = f"{self.refined_module.module_name}-{self.prediction_type}-macro"
        packages_to_install = ("\\n").join(self.requirements)
        formatted_macro_code = macro_template.format(code_env_name=code_env_name, packages_to_install=packages_to_install)
        with open(f"{self.plugin_repository}/python-runnables/code-env-creation/runnable.py", "w") as outfile:
            outfile.write(formatted_macro_code)

    def _make_plugin(self):
        shutil.make_archive(f"dss-plugin-{self.refined_module.module_name}", "zip", self.plugin_repository)

    def _format_parameter(self, new_parameter):
        parameter_type = new_parameter.get("type")
        if accepts_unique_int_value(new_parameter):
            formatted_parameter = IntPluginParameter(new_parameter)
        elif parameter_type and DSSType(parameter_type) in [DSSType.INT, DSSType.FLOAT, DSSType.DOUBLES]:
            formatted_parameter = DoublesPluginParameter(new_parameter)
        elif new_parameter.get("specs") and parameter_type and DSSType(parameter_type) == DSSType.STRINGS:
            formatted_parameter = MultiSelectPluginParameter(new_parameter)
        else:
            formatted_parameter = StringsPluginParameter(new_parameter)
        return vars(formatted_parameter)


def add_dss_packages(requirements):
    dss_packages = ["scikit-learn>=0.20,<0.21", "scipy>=1.2,<1.3", "xgboost==0.82", "statsmodels>=0.10,<0.11", "jinja2>=2.10,<2.11", "flask>=1.0,<1.1",
                    "cloudpickle>=1.3,<1.6"]
    return dss_packages + requirements


def accepts_unique_int_value(parameter):
    return parameter.get("name") == "random_state"
