class RefinedFunction:
    def __init__(self, import_name, prediction_type, parsed_docstring, doc_url=""):
        self.module_name = parsed_docstring.get("name")
        self.import_name = import_name
        self.prediction_type = prediction_type
        self.doc_url = doc_url
        self._load(parsed_docstring)

    def _load(self, parsed_docstring):
        function_docstring = parsed_docstring.get("functions")
        if function_docstring and function_docstring.get("__init__"):
            docstring = function_docstring.get("__init__")
            self.module_short_description = docstring.get("short_description", "").rstrip()
            self.module_long_description = docstring.get("long_description", "").rstrip()
            parsed_parameters = self._prepare_params(docstring.get("params", []))
            self.parameters = parsed_parameters
        else:
            self.module_short_description = ""
            self.module_long_description = ""
            self.parameters = {}

    def _prepare_params(self, parameters):
        parsed_parameters = []
        for param in parameters:
            prepared_parameter = {"name": param.get("name", "Unnamed parameter"), "description": param.get("description", "Unnamed parameter"),
                                  "type": param.get("type"), "default_value": param.get("default")}
            parsed_parameters.append(prepared_parameter)
        return parsed_parameters
