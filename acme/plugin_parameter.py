from acme.acme_constants import DSSType


class PluginParameter:
    def __init__(self, raw_parameter):
        self.name = raw_parameter.get("name")
        self.description = raw_parameter.get("description")
        if raw_parameter.get("default_value"):
            self.defaultValue = self.format_default_value(raw_parameter.get("default_value"))

    def format_default_value(self, default_value):
        pass


class DoublesPluginParameter(PluginParameter):
    def __init__(self, default_value):
        super().__init__(default_value)
        self.type = DSSType.DOUBLES.value

    def format_default_value(self, default_value):
        return [default_value]


class StringsPluginParameter(PluginParameter):
    def __init__(self, default_value):
        super().__init__(default_value)
        self.type = DSSType.STRINGS.value

    def format_default_value(self, default_value):
        return [str(default_value)]


class IntPluginParameter(PluginParameter):
    def __init__(self, default_value):
        super().__init__(default_value)
        self.type = DSSType.INT.value

    def format_default_value(self, default_value):
        return default_value
