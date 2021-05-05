from docstring_parser import parse
import inspect
from .acme_constants import DSSType
import re
from ast import literal_eval


PATTERNS = [
    ('int', DSSType.INT),
    ('integer', DSSType.INT),
    ('float', DSSType.DOUBLES),
    ('double', DSSType.DOUBLES),
    ('str', DSSType.STRINGS),
    ('string', DSSType.STRINGS)
]


def guess_type(name, default, type_):
    # We do our best to find types among int, float/double, strings.
    if default is not None:
        if type(default) == int:
            return DSSType.INT
        if type(default) == float:
            return DSSType.DOUBLES
        if type(default) == str:
            return DSSType.STRINGS
    
    for pattern, dss_type in PATTERNS:
        if type_ == pattern:
            return dss_type
        if re.search('^{}\W|\W{}\W|\W{}$'.format(pattern, pattern, pattern), type_, re.I) is not None:
            return dss_type 

    return None


def guess_specs(type_):
    # We look for {elt, elt} or [elt, elt], elt being a number or a string
    try:
        match = re.match("\[[a-zA-Z'\",0-9\.\s]+\]", type_)
        if match is not None:
            value = literal_eval(match.group(0))
            return value
    except:
        pass

    try:
        match = re.match("\{[a-zA-Z'\",0-9\.\s]+\}", type_)
        if match is not None:
            value = literal_eval(match.group(0))
            return value
    except:
        pass

    return None
 

            


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
            desc['type'] = guess_type(name, desc.get('default', None), doc.type_name)

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
    ret_desc['name'] = 'return'

    if signature.return_annotation != inspect._empty:
        ret_desc['type'] = signature.return_annotation

    if doc.returns is not None:
        if doc.returns.return_name:
            ret_desc['name'] = doc.returns.return_name
        ret_desc['description'] = doc.returns.description
        if not 'type' in ret_desc:
            ret_desc['type'] = guess_type(ret_desc['name'], None, doc.returns.type_name)

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