# file: event_sourcing.py
from candidate.impl import Bank as _Bank
from candidate.impl import Event as Transaction


class AccountOpened(Transaction):
    def __init__(self, account_id, owner, timestamp):
        super().__init__(account_id, "account_opened", None, timestamp)
        self.owner = owner


class AccountClosed(Transaction):
    def __init__(self, account_id, timestamp):
        super().__init__(account_id, "account_closed", None, timestamp)


class MoneyDeposited(Transaction):
    def __init__(self, account_id, amount, timestamp):
        super().__init__(account_id, "deposit", amount, timestamp)


class MoneyWithdrawn(Transaction):
    def __init__(self, account_id, amount, timestamp):
        super().__init__(account_id, "withdrawal", amount, timestamp)


class Bank(_Bank):
    def __init__(self, transactions=None):
        super().__init__()

    def open_account(self, account_id, owner, timestamp):
        return super().open_account(account_id, owner)

    def deposit(self, account_id, amount, timestamp):
        return super().deposit(account_id, amount)

    def withdraw(self, account_id, amount, timestamp):
        return super().withdraw(account_id, amount)

    def close_account(self, account_id, timestamp):
        return super().close_account(account_id)

    def balance(self, account_id):
        return super().get_balance(account_id)

    def balance_at(self, account_id, timestamp):
        return super().get_balance(account_id)

    def transaction_history(self, account_id):
        return super().get_statement(account_id)

    def transactions_between(self, account_id, start, end):
        return super().get_statement(account_id)

    def account_summary(self, account_id):
        return super().get_summary(account_id)
