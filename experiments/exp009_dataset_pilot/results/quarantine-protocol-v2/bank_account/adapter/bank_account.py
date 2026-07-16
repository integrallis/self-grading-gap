# file: bank_account.py
from candidate.impl import BankAccount as ImplBankAccount
from datetime import datetime

class BankAccount:
    def __init__(self):
        self._account = ImplBankAccount()

    def deposit(self, amount, date=None):
        self._account.deposit(amount, date)

    def withdraw(self, amount, date=None):
        self._account.withdraw(amount, date)

    def statement(self):
        return self._account.statement()

# file: datetime.py
from candidate.impl import datetime as ImplDatetime

class date:
    @classmethod
    def __new__(cls, year, month, day):
        return ImplDatetime(year, month, day)
