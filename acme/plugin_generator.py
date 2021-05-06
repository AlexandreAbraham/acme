import json
import shutil
from pathlib import Path

from acme.acme_constants import python_recipe_template, DSSType
from acme.plugin_parameter import IntPluginParameter, DoublesPluginParameter, StringsPluginParameter, MultiSelectPluginParameter


class PluginGenerator:
    def __init__(self, import_name, prediction_type, refined_function, template_path='.', doc_url=""):
        self.refined_module = refined_function
        self.import_name = import_name
        self.prediction_type = prediction_type
        self.doc_url = doc_url
        self.plugin_repository = f"dss-plugin-{self.refined_module.module_name}"
        self.template_repository = Path(template_path) / "templates"

    def write(self):
        self._write_plugin_json()
        algorithm_name = f"{self.refined_module.module_name}_{self.prediction_type.lower()}"
        self._write_algo_json(algorithm_name)
        self._write_algo_py(algorithm_name)
        self._write_python_lib()
        shutil.make_archive(f"dss-plugin-{self.refined_module.module_name}", "zip", self.plugin_repository)

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

    def _write_algo_py(self, algorithm_name):
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


def accepts_unique_int_value(parameter):
    return parameter.get("name") == "random_state"
