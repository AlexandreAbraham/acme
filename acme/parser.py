from docstring_parser import parse
import inspect


def guess_type(name, type):
    return object


def parse_param(name, doc, has_default=False, default=None, type_=None):

    desc = dict()
    desc['name'] = name
    desc['description'] = ''
    desc['type'] = None

    if default != inspect._empty:
        desc['default'] = default
        if default is not None:
            desc['type'] = type(default)
    if type_  != inspect._empty:
        desc['type'] = type_
    
    if doc is not None:
        desc['description'] = doc.description
        if desc['type'] is None:
            desc['type'] = guess_type(name, doc.type_name)

    return desc


def parse_function(fun, doc=None):

    desc = {}
    desc['name'] = fun.__name__
    desc['type'] = 'fun'

    doc = parse(fun.__doc__ if doc is None else doc)
    desc['short_description'] = doc.short_description
    desc['long_description'] = doc.long_description

    # Params
    signature = inspect.signature(fun)
    #if argspec.varargs:
    #    print('[{}] Varargs detected. Not supported by ACME yet.')
    #if argspec.varkw:
    #    print('[{}] Varkwargs detected. Not supported by ACME yet.')

    doc_params = dict()
    if doc.params is not None:
        doc_params = {param.arg_name: param for param in doc.params}

    desc['params'] = []
    # Positional args
    for name, parameter in signature.parameters.items():
        if name == 'self':
            continue
        desc['params'].append(parse_param(
            name,
            doc_params.pop(name, None),
            default=parameter.default,
            type_=parameter.annotation,
        ))

    for doc_param in doc_params:
        print('[{}] Doc argument missing in signature: {}'.format(desc['name'], doc_param))

    # Parse returns
    desc['returns'] = None
    ret_desc = dict()

    if signature.return_annotation != inspect._empty:
        ret_desc['name'] = 'return'
        ret_desc['type'] = signature.return_annotation

    if doc.returns is not None:
        if doc.returns.return_name:
            ret_desc['name'] = doc.returns.return_name
        ret_desc['description'] = doc.returns.description
        if not 'type' in ret_desc:
            ret_desc['type'] = guess_type(ret_desc['name'], doc.returns.type_name)

    if len(ret_desc) > 0:
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