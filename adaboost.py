from acme.parser import parse_class
from acme.refined_function import ModelRefiner
from acme.plugin_generator import PluginGenerator
from sklearn.ensemble import AdaBoostClassifier


import_name = "sklearn.ensemble"
prediction_type = "BINARY_CLASSIFICATION"
parsed_docstring = parse_class(AdaBoostClassifier)
refined_function = ModelRefiner(parsed_docstring)
plugin_generator = PluginGenerator("sklearn.ensemble", prediction_type, refined_function)
plugin_generator.write()
