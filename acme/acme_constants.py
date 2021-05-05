TYPE_MAPPING = {int: "DOUBLES", float: "DOUBLES"}

python_recipe_template = u"""from dataiku.doctor.plugins.custom_prediction_algorithm import BaseCustomPredictionAlgorithm
{import_statement}


class CustomPredictionAlgorithm(BaseCustomPredictionAlgorithm):    
    def __init__(self, prediction_type=None, params=None):    
        self.clf = {module_name}(random_state=params.get("random_state", None))
        super(CustomPredictionAlgorithm, self).__init__(prediction_type, params)
    
    def get_clf(self):
        return self.clf
"""

