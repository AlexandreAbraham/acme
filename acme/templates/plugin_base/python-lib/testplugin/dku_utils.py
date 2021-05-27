def check_and_cast(name, value, python_type, grid_param, specs):
    if value is None or value == []:
        return value
    if grid_param:
        value = [check_and_cast(name, v, python_type, False, specs) for v in value]
        return value
    value = python_type(value)
    if specs is not None:
        # Specs is either a list of 2 values indicating bounds
        # Or a set of possible values
        if isinstance(specs, set):
            if not value in specs:
                raise ValueError('Parameter {} has value {} which is not in accepted values {}'.format(
                    name, value, specs))
        elif isinstance(specs, list):
            if specs[0] is not None and value < specs[0]:
                raise ValueError('Parameter {} has value {} which is below the lower bound {}'.format(
                    name, value, specs[0]))
            if specs[1] is not None and value > specs[1]:
                raise ValueError('Parameter {} has value {} which is above the upper bound {}'.format(
                    name, value, specs[1]))
    return value
