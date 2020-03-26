import re

from .errors import ScriicRuntimeException


def substitute_variables(string, values, param_mode=False):
    """
    Substitute variable values into a string.

    Variable names surrounded in [square] or <angle> brackets (depending on
    ``param_mode``) will be replaced with their value from the given dictionary.

    The result is returned as a list which contains the values and the strings
    in between them, to allow references to live objects such as other steps to
    keep updating until the text is concatenated using :meth:`Step.text`.

    :param string: String to substitute values into.
    :param values: Dictionary of variable names and values.
    :param param_mode: Set to True to use angle brackets instead of square.
    :returns: List containing strings and the substituted values.
    :raises ScriicRuntimeException:
        An invalid variable is referenced in the string.
    """
    items = list()

    iter = re.finditer(r'\[([a-zA-Z_]\w*?)\]', string)
    if param_mode:
        iter = re.finditer(r'<([a-zA-Z_]\w*?)>', string)

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
            raise ScriicRuntimeException(
                f'Variable {variable_name} does not exist')

        prev_end = match.end()

    split_string = string[prev_end:]
    if len(split_string) > 0:
        items.append(split_string)

    return items
