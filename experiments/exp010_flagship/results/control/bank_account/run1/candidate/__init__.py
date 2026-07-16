class BankAccount:
    def __init__(self):
        self.balance = 0.0
        self.transactions = []

    def deposit(self, amount, date):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount
        self.transactions.append((date, amount, self.balance))

    def withdraw(self, amount, date):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.balance:
            raise ValueError("Cannot withdraw more than current balance")
        self.balance -= amount
        self.transactions.append((date, -amount, self.balance))

    def statement(self):
        statement_lines = ["Date       | Amount  | Balance"]
        for date, amount, balance in self.transactions:
            statement_lines.append(f"{date} | {amount:>7.2f} | {balance:>7.2f}")
        return "\n".join(statement_lines) + "\n"