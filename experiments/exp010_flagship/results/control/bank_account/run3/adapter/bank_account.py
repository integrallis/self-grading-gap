# file: bank_account.py
from candidate import BankAccount as _BankAccount


class BankAccount(_BankAccount):
    def statement(self):
        return self.print_statement()
