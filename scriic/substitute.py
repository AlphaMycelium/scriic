import re

from .errors import ScriicRuntimeException
from .value import Value, UnknownValue


def substitute_variables(string, values, param_mode=False):
    """
    Substitute variable values into a string and return a Value.

    Variable names surrounded in [square] or <angle> brackets (depending on
    ``param_mode``) will be replaced with their value from the given dictionary.

    Placing a ``"`` symbol inside the brackets and after the variable name will
    cause it to be surrounded with quotation marks, unless the variable has an
    unknown value.

    The result is returned as a list which contains the values and the strings
    in between them, to allow references to live objects such as other steps to
    keep updating until the text is concatenated using :meth:`Step.text`.

    :param string: String to substitute values into.
    :param values: Dictionary of variable names and Values.
    :param param_mode: Set to True to use angle brackets instead of square.
    :returns: Value instance with substitutions made.
    :raises ScriicRuntimeException:
        An invalid variable is referenced in the string.
    """
    value = Value()

    iter = re.finditer(r'\[([a-zA-Z_]\w*?)(")?\]', string)
    if param_mode:
        iter = re.finditer(r'<([a-zA-Z_]\w*?)(")?>', string)

    prev_end = 0
    for match in iter:
        # Add the string from between this match and the previous one
        split_string = string[prev_end:match.start()]
        if len(split_string) > 0:
            value.append(split_string)

        variable_name = match.group(1)
        if variable_name not in values:
            # This is an non-existant variable
            raise ScriicRuntimeException(
                f'Variable {variable_name} does not exist')

        # Check if we need to add quotation marks
        has_quotation = match.group(2) is not None
        if (
            type(values[variable_name]) == Value and
            values[variable_name].is_unknown()
        ) or type(values[variable_name]) == UnknownValue:
            has_quotation = False

        if has_quotation:
            value.append('"')

        if type(values[variable_name]) == Value:
            value.extend(values[variable_name])
        else:
            value.append(values[variable_name])

        if has_quotation:
            value.append('"')

        prev_end = match.end()

    split_string = string[prev_end:]
    if len(split_string) > 0:
        value.append(split_string)

    return value
