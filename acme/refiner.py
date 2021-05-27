from ast import literal_eval

from .constants import DSSType, DSSPredType
from .plugin_parameter import PluginParameter, VarType


def id_to_screen_name(id_name):
    return ' '.join(s.capitalize() for s in id_name.split('_'))


class Curtain:

    def __init__(self, target):
        self.target = target

    def __call__(self, event):
        if event['type'] == 'change':
            self.target.layout.display = ('block' if event['owner'].value else 'none')


class BooleanSpecs:

    def __init__(self, specs):
        self.specs = specs

    def __call__(self, event):
        if event['type'] == 'change' and event['name'] == 'value' and event['new'] == VarType.Boolean:
            self.specs.value = '{True, False}'


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

    def __init__(self, refiner):
        import ipywidgets as wg
        self.parameters_widgets = []
        self.custom_fit_widgets = None
        self.custom_predict_widgets = None
        self.boxes = []
        layout = {'width': 'auto'}
        style = {'description_width': '120px'}
        functions = refiner.functions
        parameters = refiner.parameters

        self.import_statement_widget = wg.Text(description='Import statement', value=refiner.import_statement, layout=layout, style=style)
        self.boxes.append(self.import_statement_widget)

        self.prediction_type_widget = wg.Dropdown(description='Prediction type', value=refiner.prediction_type, options=[
            ('Regression', DSSPredType.REGRESSION),
            ('Classification', DSSPredType.CLASSIFICATION),
            ('Clustering', DSSPredType.CLUSTERING)], layout=layout, style=style)
        self.boxes.append(self.prediction_type_widget)

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
            selected = wg.Checkbox(description=param.name, value=True, indent=False)
            selected.layout.width = '100%'

            name = wg.Text(description='Screen name', value=id_to_screen_name(param.screen_name), layout=layout, style=style)
            type_ = wg.Dropdown(description='Type', options=[(str(t.value), t) for t in VarType],
                                value=param.var_type, layout=layout, style=style)
            grid_param = wg.Checkbox(description='Grid-searchable', value=param.var_type != VarType.RandomState, indent=False)
            default = wg.Text(description='Default', value=str(param.default_value), layout=layout, style=style)
            specs = wg.Text(description='Possible values', value=str(param.specs), layout=layout, style=style)
            specs_details = wg.Label(value='Possible values can be [Lower, Upper] or {"A","B","C"} or range(min, max, step)', layout=layout, style=style)

            box = wg.VBox([name, type_, grid_param, default, specs, specs_details])
            box.layout.margin = "0 0 0 50px"
            box.layout.width = 'auto'

            selected.observe(Curtain(box))
            type_.observe(BooleanSpecs(specs))
            self.parameters_widgets.append(dict(selected=selected, name=name, type=type_, specs=specs, default=default, grid_param=grid_param))
            self.boxes.append(selected)
            self.boxes.append(box)

    def display(self):
        from IPython.display import display
        display(*self.boxes)


class ModelRefiner:

    def __init__(self, parsed_docstring):
        self._load(parsed_docstring)

    def _load(self, parsed_docstring):

        self.module_short_description = format_description(parsed_docstring.get("short_description", ""))
        self.module_long_description = format_description(parsed_docstring.get("long_description", ""))
        self.module_name = parsed_docstring['name']
        self.prediction_type = DSSPredType.CLASSIFICATION
        if parsed_docstring.get('prediction_type', None) is not None:
            self.prediction_type = DSSPredType[parsed_docstring.get('prediction_type').upper()]
        self.import_statement = None
        if 'import_name' in parsed_docstring:
            self.import_statement = "from {} import {}".format(parsed_docstring['import_name'], self.module_name)
        self.parameters = []
        self.functions = parsed_docstring.get('functions', None)
        self.custom_fit = None
        self.custom_predict = None

        init_docstring = parsed_docstring.get('functions', dict()).get('__init__', None)
        if init_docstring is not None:
            self.module_short_description = format_description(init_docstring.get("short_description", self.module_short_description))
            self.module_long_description = format_description(init_docstring.get("long_description", self.module_long_description))
            self.parameters = self._prepare_params(init_docstring.get("params", []))

    def _prepare_params(self, parameters):
        parsed_parameters = []
        for param in parameters:
            prepared_parameter = PluginParameter(param)
            parsed_parameters.append(prepared_parameter)
        return parsed_parameters

    def get_interactive_refiner(self):
        return InteractiveRefiner(self)

    def update(self, interactive_refiner):

        self.import_statement = interactive_refiner.import_statement_widget.value
        self.prediction_type = interactive_refiner.prediction_type_widget.value

        fit = interactive_refiner.custom_fit_widgets
        if fit is not None and fit['chk'].value:
            self.custom_fit = {
                'fun': fit['fun'].value,
                'X': fit['X'].value,
                'y': fit['y'].value
            }

        predict = interactive_refiner.custom_predict_widgets
        if predict is not None and predict['chk'].value:
            self.custom_predict = {
                'fun': predict['fun'].value,
                'X': predict['X'].value,
            }

        for param, param_widget in zip(self.parameters, interactive_refiner.parameters_widgets):
            param.selected = param_widget['selected'].value
            param.var_type = param_widget['type'].value
            param.default_value = cast_string(param_widget['default'].value)
            param.screen_name = param_widget['name'].value
            param.grid_param = param_widget['grid_param'].value
            try:
                specs = literal_eval(param_widget['specs'].value)
                if type(specs) not in [list, set]:
                    print('[{}] Specs not a set or a list'.format(param['name']))
                else:
                    param.specs = specs
            except:
                pass


def format_description(description):
    if description:
        return description.replace("\n", " ")


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
