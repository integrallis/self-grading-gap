class BankAccount:
    def __init__(self):
        self.balance = 0
        self.transactions = []

    def deposit(self, amount, date):
        if amount <= 0:
            return 'Amount must be positive'
        self.balance += amount
        self.transactions.append((date, amount, self.balance))

    def withdraw(self, amount, date):
        if amount <= 0:
            return 'Amount must be positive'
        if amount > self.balance:
            return 'Cannot withdraw more than current balance'
        self.balance -= amount
        self.transactions.append((date, -amount, self.balance))

    def print_statement(self):
        statement = 'Date       | Amount  | Balance\n'
        for transaction in self.transactions:
            date, amount, balance = transaction
            statement += f'{date} | {amount:> 8.2f} | {balance:> 8.2f}\n'
        return statement