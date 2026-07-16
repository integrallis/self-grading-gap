from datetime import datetime

class Account:
    def __init__(self):
        self.balance = 0.0
        self.transactions = []

    def deposit(self, amount, date):
        self._validate_positive_amount(amount)
        previous_balance = self.balance
        self.balance += amount
        self.transactions.append((date, amount, self.balance))
        return previous_balance

    def withdraw(self, amount, date):
        self._validate_positive_amount(amount)
        if amount > self.balance:
            raise ValueError("Cannot withdraw more than current balance")
        previous_balance = self.balance
        self.balance -= amount
        self.transactions.append((date, -amount, self.balance))
        return previous_balance

    def _validate_positive_amount(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")

    def statement(self):
        header = "Date       | Amount  | Balance"
        lines = [header]
        for date, amount, balance in self.transactions:
            formatted_line = f"{date.isoformat()} | {amount:7.2f} | {balance:7.2f}"
            lines.append(formatted_line)
        return "\n".join(lines)
