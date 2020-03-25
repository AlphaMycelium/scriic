class UnknownValue:
    def __init__(self, step):
        """
        An unknown value which is the result of an observation step.

        :param step: The step this value has originated from
        """
        self.step = step

    def __repr__(self):
        return f'the result of {self.step}'
