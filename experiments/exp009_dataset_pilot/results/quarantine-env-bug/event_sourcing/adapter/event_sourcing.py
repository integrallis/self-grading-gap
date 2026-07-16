# file: event_sourcing.py

from datetime import datetime
from candidate.impl import Account as ImplAccount, Bank as ImplBank

class AccountClosed:
    pass  # Placeholder for AccountClosed event

class AccountOpened:
    pass  # Placeholder for AccountOpened event

class MoneyDeposited:
    pass  # Placeholder for MoneyDeposited event

class MoneyWithdrawn:
    pass  # Placeholder for MoneyWithdrawn event


class Bank:
    def __init__(self):
        self.impl_bank = ImplBank()

    def open_account(self, account_id: str, owner: str, timestamp: datetime):
        self.impl_bank.open_account(account_id, owner, timestamp)
        return AccountOpened()  # Return an instance of AccountOpened event

    def deposit(self, account_id: str, amount: int, timestamp: datetime):
        error = self.impl_bank.deposit(account_id, amount, timestamp)
        if error is None:
            return MoneyDeposited()  # Return an instance of MoneyDeposited event
        return error

    def withdraw(self, account_id: str, amount: int, timestamp: datetime):
        error = self.impl_bank.withdraw(account_id, amount, timestamp)
        if error is None:
            return MoneyWithdrawn()  # Return an instance of MoneyWithdrawn event
        return error

    def close_account(self, account_id: str, timestamp: datetime):
        error = self.impl_bank.close_account(account_id, timestamp)
        if error is None:
            return AccountClosed()  # Return an instance of AccountClosed event
        return error

    def get_balance(self, account_id: str):
        return self.impl_bank.get_balance(account_id)

    def get_statement(self, account_id: str):
        return self.impl_bank.get_statement(account_id)

    def get_summary(self, account_id: str):
        return self.impl_bank.get_summary(account_id)

    def balance_as_of(self, account_id: str, timestamp: datetime):
        return self.impl_bank.balance_as_of(account_id, timestamp)

