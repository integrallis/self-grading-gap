# file: money/money.py
from candidate import Bank as _CandidateBank
from candidate import Money as _CandidateMoney
from candidate import Sum as _CandidateSum


class Money:
    def __init__(self, amount, currency):
        self._value = _CandidateMoney(amount, currency)

    @classmethod
    def _wrap(cls, value):
        instance = cls.__new__(cls)
        instance._value = value
        return instance

    @staticmethod
    def dollar(amount):
        return Money(amount, "USD")

    @staticmethod
    def franc(amount):
        return Money(amount, "CHF")

    @property
    def amount(self):
        return self._value.amount

    def currency(self):
        return self._value.currency

    def equals(self, other):
        return self._value.__eq__(other._value)

    def times(self, multiplier):
        return Money._wrap(self._value.__mul__(multiplier))

    def plus(self, other):
        return Sum._wrap(self._value.__add__(other._value))

    def reduce(self, bank, to):
        return Money._wrap(self._value.reduce(bank._value, to))


class Bank:
    def __init__(self):
        self._value = _CandidateBank()

    @property
    def rates(self):
        return self._value.rates

    def add_rate(self, from_currency, to_currency, rate):
        return self._value.add_rate(from_currency, to_currency, rate)

    def reduce(self, money, to):
        return money.reduce(self, to)


class Sum:
    def __init__(self, augend, addend):
        self._value = _CandidateSum(augend._value, addend._value)

    @classmethod
    def _wrap(cls, value):
        instance = cls.__new__(cls)
        instance._value = value
        return instance

    @property
    def augend(self):
        return Money._wrap(self._value.augend)

    @property
    def addend(self):
        return Money._wrap(self._value.addend)

    def reduce(self, bank, to):
        return Money._wrap(self._value.reduce(bank._value, to))

    def times(self, multiplier):
        return Sum._wrap(self._value.__mul__(multiplier))
