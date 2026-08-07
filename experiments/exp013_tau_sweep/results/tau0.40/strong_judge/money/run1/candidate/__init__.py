class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self._currency = currency

    def multiply(self, multiplier):
        return Money(self.amount * multiplier, self._currency)

    def add(self, money):
        return Sum(self, money)

    def __eq__(self, other):
        return self.amount == other.amount and self._currency == other._currency

    def currency(self):
        return self._currency

class Sum:
    def __init__(self, augend, addend):
        self.augend = augend
        self.addend = addend

    def add(self, money):
        return Sum(self, money)

    def multiply(self, multiplier):
        return Sum(self.augend.multiply(multiplier), self.addend.multiply(multiplier))

class Bank:
    def __init__(self):
        self.rates = {}

    def add_rate(self, from_currency, to_currency, rate):
        self.rates[(from_currency, to_currency)] = rate

    def reduce(self, money, to_currency):
        if isinstance(money, Sum):
            augend = self.reduce(money.augend, to_currency)
            addend = self.reduce(money.addend, to_currency)
            return Money(augend.amount + addend.amount, to_currency)
        if money.currency() == to_currency:
            return money
        rate = self.rates.get((money.currency(), to_currency))
        if rate is None:
            raise Exception(f'{money.currency()}->{to_currency}')
        return Money(money.amount // rate, to_currency)