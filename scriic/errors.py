class ScriicException(Exception):
    pass


class ScriicSyntaxException(ScriicException):
    """Raised when a syntax error is encountered in a Scriic file."""

    def __init__(self, file_path, message):
        super().__init__(f"{file_path}: {message}")


class ScriicRuntimeException(ScriicException):
    """Raised when a problem is encountered during running a Scriic file."""

    def __init__(self, file_path, message):
        super().__init__(f"{file_path}: {message}")


class UnsetDisplayIndexException(ScriicException):
    """Raised when an instruction is referenced which has not yet been displayed."""

    pass
