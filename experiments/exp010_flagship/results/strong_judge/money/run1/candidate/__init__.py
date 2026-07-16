class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self._currency = currency

    def multiply(self, multiplier):
        return Money(self.amount * multiplier, self._currency)

    def __eq__(self, other):
        return self.amount == other.amount and self._currency == other._currency

    def add(self, other):
        if self._currency == other._currency:
            return Money(self.amount + other.amount, self._currency)
        return Sum(self, other)

    def currency(self):
        return self._currency

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
        self.exchange_rates = {}

    def add_exchange_rate(self, from_currency, to_currency, rate):
        self.exchange_rates[(from_currency, to_currency)] = rate

    def reduce(self, money, to_currency):
        if isinstance(money, Sum):
            left = self.reduce(money.augend, to_currency)
            right = self.reduce(money.addend, to_currency)
            return Money(left.amount + right.amount, to_currency)
        if money.currency() == to_currency:
            return money
        rate = self.exchange_rates.get((money.currency(), to_currency))
        if rate is None:
            raise Exception(f"{to_currency}->{money.currency()}")
        return Money(money.amount // rate, to_currency)