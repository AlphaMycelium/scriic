import re

from .errors import ScriicRuntimeException
from .value import UnknownValue, Value


def substitute_variables(parts, variables):
    """
    Substitute variable values into a string and return a Value.

    The result is returned as a list which contains the values and the strings
    in between them, to allow references to live objects such as other
    instructions to keep updating until the text is concatenated using
    :meth:`Step.text`.

    :param parts: List of parts to substitute values into.
    :param values: Dictionary of variable names and Values.
    :returns: Value instance with substitutions made.
    :raises ScriicRuntimeException: An invalid variable is referenced in the string.
    """
    value = Value()

    for part in parts:
        if isinstance(part, str):
            value.append(part)
            continue

        try:
            variable_value = variables[part.name]
        except KeyError as e:
            raise ScriicRuntimeException(f"Variable '{part.name}' does not exist") from e

        # Add quotes if necessary
        quoted = part.quoted and not (
            (isinstance(variable_value, Value) and variable_value.is_unknown())
            or isinstance(variable_value, UnknownValue)
        )
        if quoted:
            value.append('"')

        if type(variable_value) == Value:
            value.extend(variable_value)
        else:
            value.append(variable_value)

        if quoted:
            value.append('"')

    return value
