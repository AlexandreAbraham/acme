from enum import Enum

TYPE_MAPPING = {int: "DOUBLES", float: "DOUBLES"}

python_recipe_template = u"""from dataiku.doctor.plugins.custom_prediction_algorithm import BaseCustomPredictionAlgorithm
{import_statement}
from dku_utils import check_and_cast

class CustomPredictionAlgorithm(BaseCustomPredictionAlgorithm):    
    def __init__(self, prediction_type=None, params=None):    
        formatted_params = dict()
{parameter_checks}
        self.clf = {module_name}({random_state_snippet})
        super(CustomPredictionAlgorithm, self).__init__(prediction_type, formatted_params)
    
    def get_clf(self):
        return self.clf
"""

parameter_check_template = 'formatted_params["{name}"] = check_and_cast("{name}", params["{name}"], {cast}, {grid}, {specs})'


class DSSPredType(Enum):
    REGRESSION = ["REGRESSION"]
    CLASSIFICATION = ["BINARY_CLASSIFICATION", "MULTICLASS"]
    CLUSTERING = ["CLUSTERING"]


class DSSType(Enum):
    INT = "INT"
    FLOAT = "FLOAT"
    STRINGS = "STRINGS"
    DOUBLES = "DOUBLES"
    MULTISELECT = "MULTISELECT"


model_wrapper_template = u"""
{import_statement}


class Wrapped{class_name}({class_name}):

{fit}
{predict}
"""

custom_fit_template = u"""
    def fit(self, X, y):
        return super(Wrapped{class_name}, self).{fun}({X}, {y})
"""

custom_predict_template = u"""
    def predict(self, X):
        return super(Wrapped{class_name}, self).{fun}({X})
"""

macro_template = u"""
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
        code_env = self.client.create_code_env('PYTHON', '{code_env_name}', 'DESIGN_MANAGED', {{'pythonInterpreter': 'PYTHON36'}})

        definition = code_env.get_definition()
        definition['desc']['installCorePackages'] = True
        definition['desc']['installJupyterSupport'] = True

        definition['specPackageList'] = '{packages_to_install}'
        # Save the new settings
        code_env.set_definition(definition)

        # Actually perform the installation
        code_env.update_packages()
        code_env.set_jupyter_support(True)
        return '<span>DONE</span>'
"""
