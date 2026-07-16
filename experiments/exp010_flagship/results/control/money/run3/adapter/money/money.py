# file: money/money.py
from candidate import Bank as Bank
from candidate import Money as CandidateMoney


class Money(CandidateMoney):
    @classmethod
    def dollar(cls, amount):
        return cls(amount, "USD")

    @classmethod
    def franc(cls, amount):
        return cls(amount, "CHF")

    @classmethod
    def _from_candidate(cls, value):
        return cls(value.amount, value.currency())

    def equals(self, other):
        return CandidateMoney.__eq__(self, other)

    def times(self, multiplier):
        return type(self)._from_candidate(
            CandidateMoney.times(self, multiplier)
        )

    def plus(self, addend):
        return type(self)._from_candidate(
            CandidateMoney.plus(self, addend)
        )

    def reduce(self, bank, to_currency):
        return type(self)._from_candidate(
            CandidateMoney.reduce(self, bank, to_currency)
        )


class Sum:
    def __init__(self, augend, addend):
        self.augend = augend
        self.addend = addend

    def reduce(self, bank, to_currency):
        return self.augend.reduce(
            bank,
            to_currency,
        ).plus(
            self.addend.reduce(
                bank,
                to_currency,
            )
        )
