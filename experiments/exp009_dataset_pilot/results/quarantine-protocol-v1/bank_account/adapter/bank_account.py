# file: bank_account.py
from candidate.impl import BankAccount as ImplBankAccount
from datetime import date as Date

class BankAccount:
    def __init__(self):
        self.impl = ImplBankAccount()

    def deposit(self, amount, transaction_date):
        self.impl.deposit(amount, transaction_date)

    def withdraw(self, amount, transaction_date):
        self.impl.withdraw(amount, transaction_date)

    def statement(self):
        return self.impl.statement()
