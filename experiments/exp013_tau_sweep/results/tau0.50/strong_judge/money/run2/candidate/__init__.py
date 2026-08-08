class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency_type = currency

    def multiply(self, multiplier):
        return Money(self.amount * multiplier, self.currency_type)

    def __eq__(self, other):
        return self.amount == other.amount and self.currency_type == other.currency_type

    def currency(self):
        return self.currency_type

    def add(self, other):
        return Sum(self, other)

class Sum:
    def __init__(self, augend, addend):
        self.augend = augend
        self.addend = addend

    def add(self, other):
        return Sum(self, other)

    def multiply(self, multiplier):
        return Sum(self.augend.multiply(multiplier), self.addend.multiply(multiplier))

class Bank:
    def __init__(self):
        self.rates = {}

    def reduce(self, money, to_currency):
        if isinstance(money, Sum):
            reduced_augend = self.reduce(money.augend, to_currency)
            reduced_addend = self.reduce(money.addend, to_currency)
            return Money(reduced_augend.amount + reduced_addend.amount, to_currency)
        if money.currency() == to_currency:
            return money
        rate = self.rates.get((money.currency(), to_currency))
        if rate is None:
            raise Exception(f"{to_currency}->{money.currency()}")
        return Money(money.amount // rate, to_currency)

    def add_rate(self, from_currency, to_currency, rate):
        self.rates[(from_currency, to_currency)] = rate