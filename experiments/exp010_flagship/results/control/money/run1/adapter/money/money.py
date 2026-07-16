# file: money/money.py
from candidate import Bank as _Bank
from candidate import Money as _Money
from candidate import Sum as _Sum


class Money:
    def __init__(self, amount, currency):
        self._value = _Money(amount, currency)

    @classmethod
    def _wrap(cls, value):
        wrapped = cls.__new__(cls)
        wrapped._value = value
        return wrapped

    @staticmethod
    def dollar(amount):
        return Money(amount, "USD")

    @staticmethod
    def franc(amount):
        return Money(amount, "CHF")

    def currency(self):
        return self._value.currency()

    def equals(self, other):
        return self._value.__eq__(other._value)

    def times(self, multiplier):
        return Money._wrap(self._value.multiply(multiplier))

    def plus(self, other):
        return Sum(self, other)

    def reduce(self, bank, to_currency):
        return Money._wrap(self._value.reduce(bank._value, to_currency))


class Bank:
    def __init__(self):
        self._value = _Bank()

    def add_rate(self, from_currency, to_currency, rate):
        return self._value.add_rate(from_currency, to_currency, rate)

    def get_rate(self, from_currency, to_currency):
        return self._value.get_rate(from_currency, to_currency)


class Sum:
    def __init__(self, augend, addend):
        self._value = _Sum(augend._value, addend._value)

    @classmethod
    def _wrap(cls, value):
        wrapped = cls.__new__(cls)
        wrapped._value = value
        return wrapped

    def times(self, multiplier):
        return Sum._wrap(self._value.multiply(multiplier))

    def reduce(self, bank, to_currency):
        return Money._wrap(self._value.reduce(bank._value, to_currency))
