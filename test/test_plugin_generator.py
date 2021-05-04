import json

from acme.plugin_generator import PluginGenerator, RefinedFunction


class TestGenerator:
    def test_write_plugin_json(self):
        refined_function = RefinedFunction()
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
                                                                                        'url': 'https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html',
                                                                                        'licenseInfo': 'Apache Software License'}}


    def test_write_recipe_json(self):
        refined_function = RefinedFunction()
        plugin_generator = PluginGenerator(refined_function)
        plugin_generator.write()

