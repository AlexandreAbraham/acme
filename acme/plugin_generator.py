import json
from pathlib import Path

from acme.acme_constants import TYPE_MAPPING


class RefinedFunction:
    module_name = "AdaBoostClassifier"
    module_short_description = "AdaBoost classifier"
    module_long_description = "An AdaBoost [1] classifier is a meta-estimator that begins by fitting a classifier on the original dataset and " \
                              "then fits additional " \
                              "" \
                              "" \
                              "copies of the classifier on the same dataset but where the weights of incorrectly classified instances are adjusted such that " \
                              "subsequent classifiers focus more on difficult cases."
    doc_url = "https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html"
    prediction_type = "BINARY_CLASSIFICATION"
    parameters = [{"name": "n_estimators", "description": "The maximum number of estimators at which boosting is terminated. In case of perfect fit, "
                                                          "the learning procedure is stopped early.", "type": "int", "default_value": 50}]


class PluginGenerator:
    def __init__(self, RefinedFunction):
        self.refined_module = RefinedFunction
        self.repository = f"../dss-plugin-{self.refined_module.module_name}"

    def write(self):
        Path(self.repository).mkdir(parents=True, exist_ok=True)
        self._write_plugin_json()
        algorithm_name = f"{self.refined_module.module_name}_{self.refined_module.prediction_type.lower()}"
        Path(f"{self.repository}/python-prediction-algos/{algorithm_name}").mkdir(parents=True, exist_ok=True)
        self._write_algo_json(algorithm_name)

    def _write_plugin_json(self):
        with open("../templates/plugin_base/plugin.json") as plugin_json_file:
            plugin_dict = json.load(plugin_json_file)
        plugin_dict["id"] = self.refined_module.module_name
        plugin_dict["meta"]["label"] = self.refined_module.module_name
        plugin_dict["meta"]["description"] = self.refined_module.module_long_description
        plugin_dict["meta"]["url"] = self.refined_module.doc_url
        with open(f"{self.repository}/plugin.json", "w") as outfile:
            json.dump(plugin_dict, outfile)

    def _write_algo_json(self, algorithm_name):
        with open("../templates/plugin_model/python-prediction-algos/test-plugin_my-algo/algo.json") as algo_json_file:
            algo_dict = json.load(algo_json_file)
        algo_dict["meta"]["label"] = self.refined_module.module_name
        algo_dict["meta"]["description"] = self.refined_module.module_short_description
        algo_dict["predictionTypes"] = self.refined_module.prediction_type
        for parameter in self.refined_module.parameters:
            algo_dict["params"] = self._add_parameter(parameter)
        with open(f"{self.repository}/python-prediction-algos/{algorithm_name}/algo.json", "w") as outfile:
            json.dump(algo_dict, outfile)

    def _write_algo_py(self):
        pass

    def _add_parameter(self, new_parameter):
        if new_parameter.get("type") in TYPE_MAPPING:
            parameter_type = TYPE_MAPPING[new_parameter.get("type")]
        else:
            parameter_type = "STRING"
        formatted_parameters = {"name": new_parameter["name"], "description": new_parameter["description"], "default_value": new_parameter["default_value"],
                                "type": parameter_type}
        return formatted_parameters
