from datetime import datetime

class Transaction:
    def __init__(self, date, amount, balance):
        self.date = date
        self.amount = amount
        self.balance = balance

    def format_transaction(self):
        return f"{self.date.isoformat()} | {self.amount:7.2f} | {self.balance:7.2f}"

class BankAccount:
    def __init__(self):
        self.balance = 0.0
        self.transactions = []
    
    def deposit(self, amount, date):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        new_balance = self.balance + amount
        self.transactions.append(Transaction(date, amount, new_balance))
        self.balance = new_balance

    def withdraw(self, amount, date):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.balance:
            raise ValueError("Cannot withdraw more than current balance")
        
        new_balance = self.balance - amount
        self.transactions.append(Transaction(date, -amount, new_balance))
        self.balance = new_balance

    def statement(self):
        header = "Date       | Amount  | Balance"
        lines = [header]
        for transaction in self.transactions:
            lines.append(transaction.format_transaction())
        return "\n".join(lines)
