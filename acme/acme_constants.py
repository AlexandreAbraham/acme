from enum import Enum

TYPE_MAPPING = {int: "DOUBLES", float: "DOUBLES"}

python_recipe_template = u"""from dataiku.doctor.plugins.custom_prediction_algorithm import BaseCustomPredictionAlgorithm
{import_statement}
from dku_utils import cast_parameters

class CustomPredictionAlgorithm(BaseCustomPredictionAlgorithm):    
    def __init__(self, prediction_type=None, params=None):    
        formatted_parameters = cast_parameters(params)
        self.clf = {module_name}(random_state=formatted_parameters.get("random_state", None))
        super(CustomPredictionAlgorithm, self).__init__(prediction_type, formatted_parameters)
    
    def get_clf(self):
        return self.clf
"""


class DSSType(Enum):
    INT = "INT"
    FLOAT = "FLOAT"
    STRINGS = "STRINGS"
    DOUBLES = "DOUBLES"
    MULTISELECT = "MULTISELECT"


model_wrapper_template = u"""
from {import_statement} import {class_name}


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