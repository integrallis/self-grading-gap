# file: money/money.py
from candidate import Bank
from candidate import Money as _Money
from candidate import Sum


def _dollar(amount):
    return _Money(amount, "USD")


def _franc(amount):
    return _Money(amount, "CHF")


def _equals(self, other):
    return _Money.__eq__(self, other)


def _plus(self, other):
    return self.add(other)


def _times(self, multiplier):
    return self.multiply(multiplier)


Money = _Money
Money.dollar = staticmethod(_dollar)
Money.franc = staticmethod(_franc)
Money.equals = _equals
Money.plus = _plus
Money.times = _times
Sum.plus = _plus
Sum.times = _times
