class UnknownValue:
    def __init__(self, step):
        """
        An unknown value which is the result of an observation step.

        :param step: The index of the step which this value has originated from
        """
        self.step = step

    def __repr__(self):
        return f'the result of step {self.step + 1}'
