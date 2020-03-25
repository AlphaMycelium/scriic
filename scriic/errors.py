class ScriicException(Exception):
    pass


class ScriicSyntaxException(ScriicException):
    """Raised when a syntax error is encountered in a Scriic file."""
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


class MetadataException(ScriicException):
    pass


class MissingMetadataException(MetadataException):
    """Raised when a Scriic file is missing a HOWTO line."""
    pass


class InvalidMetadataException(MetadataException):
    """Raised when a Scriic file has multiple HOWTO lines."""
    pass
