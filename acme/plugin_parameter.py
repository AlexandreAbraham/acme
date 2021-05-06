import ast

from acme.acme_constants import DSSType


class PluginParameter:
    def __init__(self, raw_parameter):
        self.name = raw_parameter.get("name")
        self.description = raw_parameter.get("description").replace("\n", " ")
        if raw_parameter.get("default_value"):
            self.defaultValue = self.format_default_value(raw_parameter.get("default_value"))

    def format_default_value(self, default_value):
        pass


class DoublesPluginParameter(PluginParameter):
    def __init__(self, raw_parameter):
        super().__init__(raw_parameter)
        self.type = DSSType.DOUBLES.value
        self.gridParam = True

    def format_default_value(self, default_value):
        return [cast_string(default_value)]


class StringsPluginParameter(PluginParameter):
    def __init__(self, raw_parameter):
        super().__init__(raw_parameter)
        self.type = DSSType.STRINGS.value
        self.gridParam = True

    def format_default_value(self, default_value):
        return [default_value]


class MultiSelectPluginParameter(PluginParameter):
    def __init__(self, raw_parameter):
        super().__init__(raw_parameter)
        self.type = DSSType.MULTISELECT.value
        self.gridParam = True
        self.selectChoices = self.format_specs(raw_parameter.get("specs"))

    def format_default_value(self, default_value):
        return [str(default_value)]

    def format_specs(self, specs):
        formatted_specs = set(specs)
        select_choices = []
        for possible_value in formatted_specs:
            select_choices.append({"value": possible_value, "label": possible_value})
        return select_choices


class IntPluginParameter(PluginParameter):
    def __init__(self, raw_parameter):
        super().__init__(raw_parameter)
        self.type = DSSType.INT.value

    def format_default_value(self, default_value):
        return cast_string(default_value)


def cast_string(s):
    if s == "True":
        return True
    elif s == "False":
        return False
    elif s == "None" or s == "":
        return None
    elif is_int(s):
        return int(s)
    elif is_float(s):
        return float(s)
    else:
        return s


def is_int(s):
    try:
        int(s)
        return True
    except (ValueError, TypeError):
        return False


def is_float(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False
