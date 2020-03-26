class ScriicException(Exception):
    pass


class ScriicSyntaxException(ScriicException):
    """Raised when a syntax error is encountered in a Scriic file."""
    pass


class ScriicRuntimeException(ScriicException):
    """Raised when a problem is encountered during running a Scriic file."""
    pass


class UnsetDisplayIndexException(ScriicException):
    """Raised when a step is referenced which has not yet been displayed."""
    pass


class MissingParamException(ScriicException):
    """Raised when a Scriic is ran with a missing parameter."""
    pass


class SubstitutionError(ScriicException):
    """Raised when there is an error in a Scriic variable substitution."""
    pass


class NoReturnValueException(ScriicException):
    """Raised when SUB INTO is used with a subscriic which did not return anything."""
    pass
