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
