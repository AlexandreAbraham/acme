from .constants import DSSType
from enum import Enum


class DSSPluginWriter:
    def __init__(self, parameter):
        self.name = parameter.name
        self.label = parameter.screen_name
        self.description = parameter.description
        self.defaultValue = None
        if parameter.default_value:
            self.defaultValue = self.format_default_value(parameter.default_value)
        self.gridParam = parameter.grid_param

    def format_default_value(self, default_value):
        pass


class DoublesPluginWriter(DSSPluginWriter):
    def __init__(self, parameter):
        super().__init__(parameter)
        self.type = DSSType.DOUBLES.value

    def format_default_value(self, default_value):
        return [default_value]


class StringsPluginWriter(DSSPluginWriter):
    def __init__(self, parameter):
        super().__init__(parameter)
        self.type = DSSType.STRINGS.value

    def format_default_value(self, default_value):
        return [str(default_value)]


class MultiSelectPluginWriter(DSSPluginWriter):
    def __init__(self, parameter, specs):
        super().__init__(parameter)
        self.type = DSSType.MULTISELECT.value
        self.selectChoices = self.format_specs(specs)

    def format_default_value(self, default_value):
        return [str(default_value)]

    def format_specs(self, specs):
        formatted_specs = set(specs)
        select_choices = []
        for possible_value in formatted_specs:
            select_choices.append({"value": possible_value, "label": possible_value})
        return select_choices


class IntPluginWriter(DSSPluginWriter):
    def __init__(self, raw_parameter):
        super().__init__(raw_parameter)
        self.type = DSSType.INT.value

    def format_default_value(self, default_value):
        return default_value


class PluginParameter:
    def __init__(self, raw_parameter):
        self.name = raw_parameter.get("name")
        self.screen_name = raw_parameter.get("screen_name", self.name)
        self.description = raw_parameter.get("description").replace("\n", " ")
        self.default_value = raw_parameter.get('default', None)
        self.grid_param = raw_parameter.get('grid_param', None)
        self.var_type = None
        if raw_parameter.get('type', None) is not None:
            self.var_type = VarType[raw_parameter['type']]
        self.specs = raw_parameter.get('specs', "")


class AcmeType:

    def get_dss_json(self):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()


class AcmeInteger:

    def get_dss_json(self):
        return vars(DoublesPluginWriter(self.parameter))

    def get_cast(self):
        return 'int'

    def __str__(self):
        return 'Integer'
        
class AcmeDouble:

    def get_dss_json(self):
        return vars(DoublesPluginWriter(self.parameter))

    def get_cast(self):
        return 'double'

    def __str__(self):
        return 'Double'

class AcmeString:

    def get_dss_json(self):
        return vars(StringsPluginWriter(self.parameter))

    def get_cast(self):
        return 'str'

    def __str__(self):
        return 'String'

class AcmeBoolean:

    def get_dss_json(self):
        return vars(StringsPluginWriter(self.parameter))

    def get_cast(self):
        return 'bool'

    def __str__(self):
        return 'Boolean'

class AcmeRandomState:

    def get_dss_json(self):
        return vars(IntPluginWriter(self.parameter))

    def get_cast(self):
        return 'int'

    def __str__(self):
        return 'Random state'


class VarType(Enum):
    Integer = AcmeInteger()
    Double = AcmeDouble()
    String = AcmeString()
    Boolean = AcmeBoolean()
    RandomState = AcmeRandomState()