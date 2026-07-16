class Money:
    def __init__(self, amount, currency):
        self._amount = amount
        self._currency = currency

    def multiply(self, multiplier):
        return Money(self._amount * multiplier, self._currency)

    def __eq__(self, other):
        if not isinstance(other, Money):
            return False
        return (self._amount == other._amount) and (self._currency == other._currency)

    def currency(self):
        return self._currency

    def add(self, other):
        if self._currency != other._currency:
            raise ValueError(f"Cannot add different currencies: {self._currency} + {other._currency}")
        return Money(self._amount + other._amount, self._currency)

    def reduce(self, bank, to_currency):
        rate = bank.get_rate(self._currency, to_currency)
        if rate is None:
            raise ValueError(f"{to_currency}->{self._currency}")
        return Money(self._amount / rate, to_currency)

class Bank:
    def __init__(self):
        self._rates = {}

    def add_rate(self, from_currency, to_currency, rate):
        self._rates[(from_currency, to_currency)] = rate

    def get_rate(self, from_currency, to_currency):
        return self._rates.get((from_currency, to_currency))

class Sum:
    def __init__(self, augend, addend):
        self._augend = augend
        self._addend = addend

    def add(self, bank, to_currency):
        return self._augend.add(self._addend.reduce(bank, to_currency))

    def multiply(self, multiplier):
        return Sum(self._augend.multiply(multiplier), self._addend.multiply(multiplier))

    def reduce(self, bank, to_currency):
        return self.add(bank, to_currency)