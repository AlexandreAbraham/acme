from docstring_parser import parse
import inspect


def parse_param(param):
    # TODO check with inspection

    desc = dict()
    desc['name'] = param.arg_name
    desc['description'] = param.description
    desc['default'] = param.default
    desc['type'] = param.type_name

    return desc


def parse_function(fun, doc=None):

    desc = {}
    desc['name'] = fun.__name__
    desc['type'] = 'fun'

    doc = parse(fun.__doc__ if doc is None else doc)
    desc['short_description'] = doc.short_description
    desc['long_description'] = doc.long_description
    desc['params'] = []
    if doc.params is not None:
        desc['params'] = [parse_param(param) for param in doc.params]

    # Parse returns
    desc['returns'] = None
    if doc.returns is not None:
        ret_desc = dict()
        ret_desc['name'] = doc.returns.return_name
        ret_desc['description'] = doc.returns.description
        ret_desc['type'] = doc.returns.type_name

        desc['returns'] = ret_desc

    return desc

def parse_class(clazz):
    desc = dict()
    desc['name'] = clazz.__name__
    desc['type'] = 'class'    

    doc = parse(clazz.__doc__)
    desc['short_description'] = doc.short_description
    desc['long_description'] = doc.long_description

    funs = dict()
    # Special case for __init__
    if clazz.__init__.__doc__ is None:
        funs['__init__'] = parse_function(clazz.__init__, doc=clazz.__doc__)

    for fun_name, fun in inspect.getmembers(clazz, predicate=inspect.isfunction):
        if fun_name.startswith('_'):
            continue
        funs[fun_name] = parse_function(fun)
    
    desc['functions'] = funs
    return desc