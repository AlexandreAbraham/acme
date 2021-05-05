def cast_parameters(params):
    formatted_params = params.copy()
    for param_name, param_value in params.items():
        if type(param_value) is list:
            formatted_param_values = []
            if len(param_value) == 0:
                # drop empty lists to prevent grid search from failing
                formatted_params.pop(param_name)
            else:
                for value in param_value:
                    formatted_param_values.append(format_parameter_value(value))
                formatted_params[param_name] = formatted_param_values
        else:
            formatted_params[param_name] = format_parameter_value(param_value)
    return formatted_params


def format_parameter_value(parameter_value):
    if isinstance(parameter_value, str):
        return cast_string(parameter_value)
    else:
        return parameter_value


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
