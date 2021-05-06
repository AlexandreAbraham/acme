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


class ArgLoader:

    def __init__(self, functions, dropdown):
        self.functions = functions
        self.dropdown = dropdown

    def __call__(self, event):
        if event['type'] == 'change':
            args = self.functions.get(event['owner'].value, [])['params']
            args = [arg['name'] for arg in args]
            self.dropdown.options = args
     

class InteractiveRefiner:

    def __init__(self, functions, parameters):
        import ipywidgets as wg
        self.parameters_widgets = []
        self.custom_fit_widgets = None
        self.custom_predict_widgets = None
        self.boxes = []
        layout = {'width': 'auto'}
        style = {'description_width': '120px'}

        if functions is not None:
            custom_fit = wg.Checkbox(description='Custom fit function', value=False, indent=False)
            custom_fit.layout.width = '100%'
            custom_fit_fun = wg.Dropdown(description='Function', options=functions.keys(), layout=layout, style=style)
            custom_fit_X = wg.Dropdown(description='X', options=[], layout=layout, style=style)
            custom_fit_y = wg.Dropdown(description='y', options=[], layout=layout, style=style)
            self.custom_fit_widgets = dict(chk=custom_fit, fun=custom_fit_fun, X=custom_fit_X, y=custom_fit_y)
            custom_fit_box = wg.VBox([custom_fit_fun, custom_fit_X, custom_fit_y])
            custom_fit_box.layout.margin = "0 0 0 50px"
            custom_fit_box.layout.width = 'auto'
            custom_fit_box.layout.display = 'none'
            custom_fit.observe(Curtain(custom_fit_box))
            custom_fit_fun.observe(ArgLoader(functions, custom_fit_X))
            custom_fit_fun.observe(ArgLoader(functions, custom_fit_y))

            self.boxes.append(custom_fit)
            self.boxes.append(custom_fit_box)

            custom_predict = wg.Checkbox(description='Custom predict function', value=False, indent=False)
            custom_predict.layout.width = '100%'
            custom_predict_fun = wg.Dropdown(description='Function', options=functions.keys(), layout=layout, style=style)
            custom_predict_X = wg.Dropdown(description='X', options=[], layout=layout, style=style)
            self.custom_predict_widgets = dict(chk=custom_predict, fun=custom_predict_fun, X=custom_predict_X)
            custom_predict_box = wg.VBox([custom_predict_fun, custom_predict_X])
            custom_predict_box.layout.margin = "0 0 0 50px"
            custom_predict_box.layout.width = 'auto'
            custom_predict_box.layout.display = 'none'
            custom_predict.observe(Curtain(custom_predict_box))
            custom_predict_fun.observe(ArgLoader(functions, custom_predict_X))

            self.boxes.append(custom_predict)
            self.boxes.append(custom_predict_box)

        for param in parameters:
            selected = wg.Checkbox(description=param.get("name"), value=True, indent=False)
            selected.layout.width = '100%'

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
        self.custom_fit = None
        self.custom_predict = None

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
        return InteractiveRefiner(self.functions, self.parameters)

    def update(self, interactive_refiner):

        fit = interactive_refiner.custom_fit_widgets
        if fit is not None and fit['chk'].value:
            self.custom_fit = {
                'name': fit['fun'],
                'X': fit['X'],
                'y':fit['y']
            }

        predict = interactive_refiner.custom_predict_widgets
        if predict is not None and predict['chk'].value:
            self.custom_predict = {
                'name': predict['fun'],
                'X': predict['X'],
            }

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
