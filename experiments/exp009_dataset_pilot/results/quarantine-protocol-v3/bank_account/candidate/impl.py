# candidate/impl.py

from datetime import datetime

class Account:
    def __init__(self):
        self.balance = 0.0
        self.transactions = []

    def deposit(self, amount, date):
        self._validate_positive_amount(amount)
        self.transactions.append((date, amount))
        self.balance += amount

    def withdraw(self, amount, date):
        self._validate_positive_amount(amount)
        if amount > self.balance:
            raise ValueError("Cannot withdraw more than current balance")
        self.transactions.append((date, -amount))
        self.balance -= amount

    def statement(self):
        statement_lines = ["Date       | Amount  | Balance"]
        current_balance = 0.0

        for date, amount in self.transactions:
            current_balance += amount
            statement_lines.append(f"{date.isoformat()} | {amount:7.2f} | {current_balance:7.2f}")

        return "\n".join(statement_lines)

    def _validate_positive_amount(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
