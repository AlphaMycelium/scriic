import re

from .errors import SubstitutionError


def substitute_variables(string, values, param_mode=False):
    """
    Convert a string into a list of substituted values and the strings in between.

    :param string: String to substitute values into
    :param values: Dictionary of variable names and values
    :param param_mode: Set to True to use angle brackets instead of square
    :returns: List containing strings and the substituted values in order,
        ready to be concatenated together
    :raises: SubstitutionError if an invalid variable is referenced in the
        string
    """
    items = list()

    iter = re.finditer(r'\[(.+?)\]', string)
    if param_mode:
        iter = re.finditer(r'\<(.+?)\>', string)

    prev_end = 0
    for match in iter:
        # Add the string from between this match and the previous one
        split_string = string[prev_end:match.start()]
        if len(split_string) > 0:
            items.append(split_string)

        variable_name = match.group(1)
        try:
            if type(values[variable_name]) == list:
                # The parameter has been substituted into before,
                # extend our list with its items to avoid having sub-lists
                items.extend(values[variable_name])
            else:
                items.append(values[variable_name])
        except KeyError:
            # This is an non-existant variable
            raise SubstitutionError(f'Variable {variable_name} does not exist')

        prev_end = match.end()

    split_string = string[prev_end:]
    if len(split_string) > 0:
        items.append(split_string)

    return items
