import json
import shutil
from pathlib import Path

from acme.acme_constants import TYPE_MAPPING, python_recipe_template


class PluginGenerator:
    def __init__(self, import_name, prediction_type, refined_function, doc_url=""):
        self.refined_module = refined_function
        self.import_name = import_name
        self.prediction_type = prediction_type
        self.doc_url = doc_url
        self.plugin_repository = f"dss-plugin-{self.refined_module.module_name}"
        self.template_repository = "templates"

    def write(self):
        Path(self.plugin_repository).mkdir(parents=True, exist_ok=True)
        self._write_plugin_json()
        algorithm_name = f"{self.refined_module.module_name}_{self.prediction_type.lower()}"
        Path(f"{self.plugin_repository}/python-prediction-algos/{algorithm_name}").mkdir(parents=True, exist_ok=True)
        self._write_algo_json(algorithm_name)
        self._write_algo_py(algorithm_name)
        shutil.make_archive(f"dss-plugin-{self.refined_module.module_name}", "zip", self.plugin_repository)

    def _write_plugin_json(self):
        with open(f"{self.template_repository}/plugin_base/plugin.json") as plugin_json_file:
            plugin_dict = json.load(plugin_json_file)
        plugin_dict["id"] = self.refined_module.module_name
        plugin_dict["meta"]["label"] = self.refined_module.module_name
        plugin_dict["meta"]["description"] = self.refined_module.module_long_description
        plugin_dict["meta"]["url"] = self.doc_url
        with open(f"{self.plugin_repository}/plugin.json", "w") as outfile:
            json.dump(plugin_dict, outfile)

    def _write_algo_json(self, algorithm_name):
        with open(f"{self.template_repository}/plugin_model/python-prediction-algos/test-plugin_my-algo/algo.json") as algo_json_file:
            algo_dict = json.load(algo_json_file)
        algo_dict["meta"]["label"] = self.refined_module.module_name
        algo_dict["meta"]["description"] = self.refined_module.module_short_description
        algo_dict["predictionTypes"] = [self.prediction_type]
        for parameter in self.refined_module.parameters:
            algo_dict["params"].append(self._format_parameter(parameter))
        with open(f"{self.plugin_repository}/python-prediction-algos/{algorithm_name}/algo.json", "w") as outfile:
            json.dump(algo_dict, outfile)

    def _write_algo_py(self, algorithm_name):
        import_statement = f"from {self.import_name} import {self.refined_module.module_name}"
        formatted_code = python_recipe_template.format(import_statement=import_statement, module_name=self.refined_module.module_name)
        with open(f"{self.plugin_repository}/python-prediction-algos/{algorithm_name}/algo.py", "w") as outfile:
            outfile.write(formatted_code)

    def _format_parameter(self, new_parameter):
        if new_parameter.get("type") in TYPE_MAPPING:
            parameter_type = TYPE_MAPPING[new_parameter.get("type")]
            if new_parameter["default_value"]:
                default_value = new_parameter["default_value"]
        else:
            parameter_type = "STRINGS"
            if new_parameter["default_value"]:
                default_value = str(new_parameter["default_value"])
        if new_parameter.get("name") == "random_state":
            parameter_type = "INT"
        formatted_parameter = {"name": new_parameter["name"], "description": new_parameter["description"],
                               "type": parameter_type}
        if new_parameter["default_value"]:
            formatted_parameter["defaultValue"] = [default_value]
        return formatted_parameter
