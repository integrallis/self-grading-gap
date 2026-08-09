# file: money/money.py
from candidate import Bank as Bank
from candidate import Money as Money
from candidate import Sum as Sum

Money.dollar = classmethod(lambda cls, amount: cls(amount, "USD"))
Money.franc = classmethod(lambda cls, amount: cls(amount, "CHF"))
Money.times = Money.multiply
Money.equals = Money.__eq__
Money.plus = Money.add

Sum.times = Sum.multiply
Sum.plus = Sum.add

Bank.raises = Bank.reduce
