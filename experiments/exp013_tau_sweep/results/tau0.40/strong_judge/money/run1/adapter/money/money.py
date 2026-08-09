# file: money/money.py
from candidate import Bank as _CandidateBank
from candidate import Money as _CandidateMoney
from candidate import Sum as _CandidateSum


class Money(_CandidateMoney):
    @classmethod
    def dollar(cls, amount):
        return cls(amount, "USD")

    @classmethod
    def franc(cls, amount):
        return cls(amount, "CHF")

    equals = _CandidateMoney.__eq__

    def plus(self, money):
        result = _CandidateMoney.add(self, money)
        return Sum(result.augend, result.addend)

    add = plus

    def times(self, multiplier):
        result = _CandidateMoney.multiply(self, multiplier)
        return type(self)(result.amount, result.currency())

    multiply = times


class Sum(_CandidateSum):
    def plus(self, money):
        result = _CandidateSum.add(self, money)
        return Sum(result.augend, result.addend)

    add = plus

    def times(self, multiplier):
        result = _CandidateSum.multiply(self, multiplier)
        return Sum(result.augend, result.addend)

    multiply = times


class Bank(_CandidateBank):
    def reduce(self, money, to_currency):
        result = _CandidateBank.reduce(self, money, to_currency)
        return Money(result.amount, result.currency())

    raises = reduce
