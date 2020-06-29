class UnknownValue:
    """
    An unknown value which is the result of an observation instruction.

    :param instruction: The instruction this value has originated from.
    """

    def __init__(self, instruction):
        self.instruction = instruction

    def __repr__(self):
        return f"the result of {self.instruction}"


class Value(list):
    def __init__(self, *parts):
        """
        The value of a variable or instruction text.

        :param parts: Things which are concatenated to get this value.
        """
        super().__init__()
        self.extend(parts)

    def __repr__(self):
        """
        Convert this value to a single string.

        :raises UnsetDisplayIndexException:
            A instruction needs to be referenced which has not yet been displayed.
        """
        return "".join([str(p) for p in self])

    def is_unknown(self):
        """Return whether this value contains any UnknownValues."""
        return any([type(p) == UnknownValue for p in self])
