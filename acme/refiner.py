from copy import deepcopy
from .acme_constants import DSSType
from ast import literal_eval


def id_to_screen_name(id_name):
    return ' '.join(s.capitalize() for s in id_name.split('_'))


class Curtain:

    def __init__(self, target):
        self.target = target

    def __call__(self, event):
        if event['type'] == 'change':
            self.target.layout.display = ('block' if event['owner'].value else 'none')


class InteractiveRefiner:

    def __init__(self, parameters):
        import ipywidgets as wg
        self.parameters_widgets = []
        self.boxes = []

        for param in parameters:
            selected = wg.Checkbox(description=param.get("name"), value=True, indent=False)
            selected.layout.width = '100%'
            layout = {'width': 'auto'}
            style = {'description_width': '120px'}
            name = wg.Text(description='Screen name', value=id_to_screen_name(param.get("name")), layout=layout, style=style)
            type_ = wg.Dropdown(description='Type', options=[('INT', DSSType.INT), ('DOUBLES', DSSType.DOUBLES), ('STRINGS', DSSType.STRINGS)], value=param.get('type'), layout=layout, style=style)
            default = wg.Text(description='Default', value=str(param.get("default_value")), layout=layout, style=style)
            specs = wg.Text(description='Possible values', value=str(param.get("specs", "")), layout=layout, style=style)
            specs_details = wg.Label(value='Possible values can be [Lower, Upper] or {"A","B","C"} or range(min, max, step)', layout=layout, style=style)

            box = wg.VBox([name, type_, default, specs, specs_details])
            box.layout.margin = "0 0 0 50px"
            box.layout.width = 'auto'

            selected.observe(Curtain(box))
            self.parameters_widgets.append(dict(selected=selected, name=name, type=type_, specs=specs, default=default))
            self.boxes.append(selected)
            self.boxes.append(box)
    
    def display(self):
        from IPython.display import display
        display(*self.boxes)



class ModelRefiner:

    def __init__(self, parsed_docstring):
        self._load(parsed_docstring)


    def _load(self, parsed_docstring):

        self.module_short_description = parsed_docstring.get("short_description", "").rstrip()
        self.module_long_description = parsed_docstring.get("long_description", "").rstrip()
        self.module_name = parsed_docstring['name']
        self.parameters = []
        self.functions = parsed_docstring.get('functions', None)

        init_docstring = parsed_docstring.get('functions', dict()).get('__init__', None)
        if init_docstring is not None:
            self.module_short_description = init_docstring.get("short_description", self.module_short_description).rstrip()
            self.module_long_description = init_docstring.get("long_description", self.module_long_description).rstrip()
            self.parameters = self._prepare_params(init_docstring.get("params", []))

    def _prepare_params(self, parameters):
        parsed_parameters = []
        for param in parameters:
            prepared_parameter = {
                "name": param.get("name", "Unnamed parameter"), 
                "description": param.get("description", "Unnamed parameter"),
                "type": param.get("type"),
                "default_value": param.get("default"),
                "specs": param.get("specs")
            }
            parsed_parameters.append(prepared_parameter)
        return parsed_parameters

    def get_interactive_refiner(self):
        return InteractiveRefiner(self.parameters)

    def update(self, interactive_refiner):
        for param, param_widget in zip(self.parameters, interactive_refiner.parameters_widgets):
            param['selected'] = param_widget['selected'].value
            param['type'] = param_widget['type'].value
            param['default_value'] = param_widget['default'].value
            param['screen_name'] = param_widget['name'].value
            try:
                specs = literal_eval(param_widget['specs'].value)
                if type(specs) not in [list, set]:
                    print('[{}] Specs not a set or a list'.format(param['name']))
                else:
                    param['specs'] = specs
            except:
                pass
