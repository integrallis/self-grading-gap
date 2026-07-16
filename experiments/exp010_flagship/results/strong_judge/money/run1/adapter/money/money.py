# file: money/money.py
from candidate import Bank as Bank
from candidate import Money as Money
from candidate import Sum as Sum


def dollar(amount):
    return Money(amount, "USD")


def franc(amount):
    return Money(amount, "CHF")


Money.dollar = staticmethod(dollar)
Money.franc = staticmethod(franc)
Money.equals = Money.__eq__
Money.plus = Money.add
Money.times = Money.multiply

Sum.plus = Sum.add
Sum.times = Sum.multiply

Bank.add_rate = Bank.add_exchange_rate
Bank.raises = Bank.reduce
