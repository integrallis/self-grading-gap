from datetime import datetime

class InsufficientFundsError(Exception):
    pass

class InvalidAmountError(Exception):
    pass

class BankAccount:
    def __init__(self):
        self.balance = 0.0
        self.transactions = []

    def deposit(self, amount, date):
        self._validate_positive_amount(amount)
        original_balance = self.balance
        self.balance += amount
        self.transactions.append((date, amount, self.balance))
        
    def withdraw(self, amount, date):
        self._validate_positive_amount(amount)
        if amount > self.balance:
            raise InsufficientFundsError("Cannot withdraw more than current balance")
        original_balance = self.balance
        self.balance -= amount
        self.transactions.append((date, -amount, self.balance))
        
    def statement(self):
        header = "Date       | Amount  | Balance"
        lines = [header]
        for date, amount, balance in self.transactions:
            lines.append(f"{date.isoformat()} | {amount:7.2f} | {balance:7.2f}")
        return "\n".join(lines)

    def _validate_positive_amount(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
