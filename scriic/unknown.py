class UnknownValue:
    """
    An unknown value which is the result of an observation step.

    :param step: The step this value has originated from.
    """

    def __init__(self, step):
        self.step = step

    def __repr__(self):
        return f'the result of {self.step}'
