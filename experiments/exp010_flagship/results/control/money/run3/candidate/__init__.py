class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency_code = currency

    def times(self, multiplier):
        return Money(self.amount * multiplier, self.currency_code)

    def __eq__(self, other):
        return isinstance(other, Money) and self.amount == other.amount and self.currency_code == other.currency_code

    def currency(self):
        return self.currency_code

    def plus(self, addend):
        return Money(self.amount + addend.amount, self.currency_code)

    def reduce(self, bank, to_currency):
        rate = bank.rate(self.currency_code, to_currency)
        if rate == 0:
            raise ValueError(f"No exchange rate registered for {self.currency_code}->{to_currency}")
        return Money(self.amount / rate, to_currency)

class Bank:
    def __init__(self):
        self.rates = {}

    def add_rate(self, from_currency, to_currency, rate):
        self.rates[(from_currency, to_currency)] = rate

    def rate(self, from_currency, to_currency):
        if from_currency == to_currency:
            return 1
        return self.rates.get((from_currency, to_currency), 1)

    def reduce(self, money, to_currency):
        return money.reduce(self, to_currency)