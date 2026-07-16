class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    def __mul__(self, multiplier):
        return Money(self.amount * multiplier, self.currency)

    def __eq__(self, other):
        return self.amount == other.amount and self.currency == other.currency

    def __ne__(self, other):
        return not self.__eq__(other)

    def currency(self):
        return self.currency

    def __add__(self, other):
        return Sum(self, other)

    def reduce(self, bank, to):
        if self.currency == to:
            return Money(self.amount, self.currency)
        return bank.reduce(self, to)

class Bank:
    def __init__(self):
        self.rates = {}

    def add_rate(self, from_currency, to_currency, rate):
        if from_currency not in self.rates:
            self.rates[from_currency] = {}
        self.rates[from_currency][to_currency] = rate

    def reduce(self, money, to):
        if money.currency in self.rates and to in self.rates[money.currency]:
            rate = self.rates[money.currency][to]
            return Money(money.amount / rate, to)
        raise ValueError(f'{to}->{money.currency}')

class Sum:
    def __init__(self, augend, addend):
        self.augend = augend
        self.addend = addend

    def reduce(self, bank, to):
        amount = self.augend.reduce(bank, to).amount + self.addend.reduce(bank, to).amount
        return Money(amount, to)

    def __mul__(self, multiplier):
        return Sum(self.augend * multiplier, self.addend * multiplier)