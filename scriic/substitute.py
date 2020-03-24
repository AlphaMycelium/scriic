import re


class SubstitutionError(Exception):
    pass


def substitute_variables(string, values):
    """
    Substitute variable values into a string.

    Values will be substituted where the variable name is found surrounded in
    square brackets.

    :param string: String to substitute values into
    :param values: Dictionary of variable names and values
    :returns: String with values substituted in
    :raises: SubstitutionError if an invalid variable is referenced in the
        string
    """
    def substitute(match):
        variable_name = match.group(1)
        try:
            return values[variable_name]
        except KeyError:
            # This is an non-existant variable
            raise SubstitutionError(f'Variable {variable_name} does not exist')

    # Call substitute function for each match and replace with return value
    return re.sub(r'\[(.+?)\]', substitute, string)
