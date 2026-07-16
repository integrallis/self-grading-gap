from datetime import datetime

class Transaction:
    def __init__(self, date, amount, balance):
        self.date = date
        self.amount = amount
        self.balance = balance

    def __str__(self):
        return f"{self.date.isoformat()} | {self.amount:7.2f} | {self.balance:7.2f}"

class BankAccount:
    def __init__(self):
        self.balance = 0.0
        self.transactions = []
    
    def deposit(self, amount, date=None):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if date is None:
            date = datetime.now()
        self.balance += amount
        self.transactions.append(Transaction(date, amount, self.balance))
    
    def withdraw(self, amount, date=None):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.balance:
            raise ValueError("Cannot withdraw more than current balance")
        if date is None:
            date = datetime.now()
        self.balance -= amount
        self.transactions.append(Transaction(date, -amount, self.balance))
    
    def statement(self):
        statement_lines = ["Date       | Amount  | Balance"]
        for transaction in self.transactions:
            statement_lines.append(str(transaction))
        return "\n".join(statement_lines)
