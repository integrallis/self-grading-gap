from candidate.impl import ChainableCalculator


class Calculator(ChainableCalculator):
    def plus(self, value):
        return self.add(value)

    def minus(self, value):
        return self.subtract(value)
