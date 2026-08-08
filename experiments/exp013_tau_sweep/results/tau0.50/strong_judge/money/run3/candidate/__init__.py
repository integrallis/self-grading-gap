class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self._currency = currency

    def multiply(self, multiplier):
        return Money(self.amount * multiplier, self._currency)

    def __eq__(self, other):
        return self.amount == other.amount and self._currency == other._currency

    def currency(self):
        return self._currency

    def add(self, other):
        return Sum(self, other)

class Sum:
    def __init__(self, augend, addend):
        self.augend = augend
        self.addend = addend

    def multiply(self, multiplier):
        return Sum(self.augend.multiply(multiplier), self.addend.multiply(multiplier))

    def add(self, other):
        return Sum(self, other)

class Bank:
    def __init__(self):
        self.rates = {}

    def add_rate(self, from_currency, to_currency, rate):
        self.rates[(from_currency, to_currency)] = rate

    def reduce(self, amount, to_currency):
        if isinstance(amount, Sum):
            left = self.reduce(amount.augend, to_currency)
            right = self.reduce(amount.addend, to_currency)
            return Money(left.amount + right.amount, to_currency)
        if amount.currency() == to_currency:
            return amount
        rate = self.rates.get((amount.currency(), to_currency))
        if rate is None:
            raise Exception(f'{to_currency}->{amount.currency()}')
        return Money(amount.amount // rate, to_currency)