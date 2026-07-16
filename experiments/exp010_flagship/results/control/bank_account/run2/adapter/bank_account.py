# file: bank_account.py
from candidate import BankAccount as _CandidateBankAccount


class BankAccount(_CandidateBankAccount):
    def statement(self):
        return self.print_statement()
