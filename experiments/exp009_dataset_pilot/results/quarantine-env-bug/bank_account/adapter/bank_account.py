# file: bank_account.py
from candidate.impl import BankAccount as CandidateBankAccount
from datetime import date

class BankAccount:
    def __init__(self):
        self._account = CandidateBankAccount()

    def deposit(self, amount, transaction_date):
        transaction_date = transaction_date if isinstance(transaction_date, date) else date.today()
        self._account.deposit(amount, transaction_date)

    def withdraw(self, amount, transaction_date):
        transaction_date = transaction_date if isinstance(transaction_date, date) else date.today()
        self._account.withdraw(amount, transaction_date)

    def statement(self):
        return self._account.statement()
