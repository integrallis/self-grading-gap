class Account:
    def __init__(self):
        self.balance = 0
        self.transactions = []

    def deposit(self, amount, date):
        if amount <= 0:
            raise Exception("Amount must be positive")
        self.balance += amount
        self.transactions.append((date, amount, self.balance))

    def withdraw(self, amount, date):
        if amount <= 0:
            raise Exception("Amount must be positive")
        if amount > self.balance:
            raise Exception("Cannot withdraw more than current balance")
        self.balance -= amount
        self.transactions.append((date, -amount, self.balance))

    def statement(self):
        header = "Date       | Amount  | Balance"
        lines = [header]
        for date, amount, balance in self.transactions:
            lines.append(f"{date} | {amount:7.2f} | {balance:7.2f}")
        return '\n'.join(lines)