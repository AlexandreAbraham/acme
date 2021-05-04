import importlib
import json

import pytest

from acme.plugin_generator import PluginGenerator


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
    import_name = "sklearn.ensemble"


@pytest.fixture()
def refined_function():
    return RefinedFunction


class TestGenerator:
    def test_write_plugin_json(self, refined_function):
        plugin_generator = PluginGenerator(refined_function)
        plugin_generator.write()
        with open(f"{plugin_generator.repository}/plugin.json") as plugin_json_file:
            plugin_dict = json.load(plugin_json_file)
        assert plugin_dict == {'id': 'AdaBoostClassifier', 'version': '0.0.1', 'meta': {'label': 'AdaBoostClassifier',
                                                                                        'description': 'An AdaBoost [1] classifier is a meta-estimator that '
                                                                                                       'begins by fitting a classifier on the original '
                                                                                                       'dataset and then fits additional copies of the '
                                                                                                       'classifier on the same dataset but where the weights '
                                                                                                       'of incorrectly classified instances are adjusted such '
                                                                                                       'that subsequent classifiers focus more on difficult '
                                                                                                       'cases.',
                                                                                        'author': 'admin', 'icon': 'icon-puzzle-piece', 'tags': [],
                                                                                        'url':
                                                                                            'https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html',
                                                                                        'licenseInfo': 'Apache Software License'}}

    def test_write_recipe_json(self, refined_function):
        plugin_generator = PluginGenerator(refined_function)
        plugin_generator.write()
        with open(f"{plugin_generator.repository}/python-prediction-algos/AdaBoostClassifier_binary_classification/algo.json") as algo_json_file:
            algo_dict = json.load(algo_json_file)
        assert algo_dict == {'acceptsSparseMatrix': False,
                             'gridSearchMode': 'MANAGED',
                             'meta': {'description': 'AdaBoost classifier',
                                      'icon': 'icon-puzzle-piece',
                                      'label': 'AdaBoostClassifier'},
                             'params': [{'default_value': [50],
                                         'description': 'The maximum number of estimators at which '
                                                        'boosting is terminated. In case of perfect fit, '
                                                        'the learning procedure is stopped early.',
                                         'name': 'n_estimators',
                                         'type': 'DOUBLES'}],
                             'predictionTypes': ['BINARY_CLASSIFICATION'],
                             'supportsSampleWeights': True}

    def test_write_recipe_py(self, refined_function):
        plugin_generator = PluginGenerator(refined_function)
        plugin_generator.write()
        with pytest.raises(ModuleNotFoundError):
            _ = importlib.import_module('dss-plugin-AdaBoostClassifier.python-prediction-algos.AdaBoostClassifier_binary_classification.algo', None)
