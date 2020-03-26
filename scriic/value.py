class UnknownValue:
    """
    An unknown value which is the result of an observation step.

    :param step: The step this value has originated from.
    """

    def __init__(self, step):
        self.step = step

    def __repr__(self):
        return f'the result of {self.step}'


class Value(list):
    def __init__(self, *parts):
        """
        The value of a variable or step text.

        :param parts: Things which are concatenated to get this value.
        """
        super().__init__()
        self.extend(parts)

    def __repr__(self):
        """
        Convert this value to a single string.

        :raises UnsetDisplayIndexException:
            A step needs to be referenced which has not yet been displayed.
        """
        return ''.join(
            [str(p) for p in self]
        )

    def is_unknown(self):
        """Return whether this value contains any UnknownValues."""
        return any(
            [type(p) == UnknownValue for p in self]
        )
