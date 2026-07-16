# candidate/impl.py

class AccountEvent:
    def __init__(self, account_id, event_type, amount=None, timestamp=None):
        self.account_id = account_id
        self.event_type = event_type
        self.amount = amount
        self.timestamp = timestamp

class BankAccount:
    def __init__(self, owner_name):
        self.owner_name = owner_name
        self.balance = 0
        self.transactions = []
        self.status = 'open'

    def deposit(self, amount, timestamp):
        if self.status == 'closed':
            return "account is closed"
        if amount <= 0:
            return "deposit amount must be positive"
        self.balance += amount
        self.transactions.append((timestamp, 'deposit', amount, self.balance))
        return AccountEvent(self.owner_name, 'deposit', amount, timestamp)

    def withdraw(self, amount, timestamp):
        if self.status == 'closed':
            return "account is closed"
        if amount <= 0:
            return "withdrawal amount must be positive"
        if amount > self.balance:
            return "insufficient funds"
        self.balance -= amount
        self.transactions.append((timestamp, 'withdrawal', amount, self.balance))
        return AccountEvent(self.owner_name, 'withdrawal', amount, timestamp)

    def close(self):
        if self.balance != 0:
            return "balance must be zero"
        self.status = 'closed'
        return AccountEvent(self.owner_name, 'account_closed', timestamp=None)

class BankLedger:
    def __init__(self):
        self.accounts = {}
        self.event_stream = []

    def open_account(self, account_id, owner_name, timestamp):
        if account_id in self.accounts:
            return "account already exists"
        account = BankAccount(owner_name)
        self.accounts[account_id] = account
        event = AccountEvent(account_id, 'account_opened', owner_name, timestamp)
        self.event_stream.append(event)
        return event

    def deposit(self, account_id, amount, timestamp):
        if account_id not in self.accounts:
            return "account not found"
        account = self.accounts[account_id]
        event = account.deposit(amount, timestamp)
        if isinstance(event, AccountEvent):
            self.event_stream.append(event)
        return event

    def withdraw(self, account_id, amount, timestamp):
        if account_id not in self.accounts:
            return "account not found"
        account = self.accounts[account_id]
        event = account.withdraw(amount, timestamp)
        if isinstance(event, AccountEvent):
            self.event_stream.append(event)
        return event

    def close_account(self, account_id):
        if account_id not in self.accounts:
            return "account not found"
        account = self.accounts[account_id]
        event = account.close()
        if isinstance(event, AccountEvent):
            self.event_stream.append(event)
        return event

    def get_balance(self, account_id, timestamp):
        if account_id not in self.accounts:
            return "account not found"
        account = self.accounts[account_id]
        return self._calculate_balance(account, timestamp)

    def _calculate_balance(self, account, timestamp):
        balance = 0
        for t, type_, amount, running_balance in account.transactions:
            if t <= timestamp:
                balance = running_balance
        return balance

    def get_statement(self, account_id):
        if account_id not in self.accounts:
            return "account not found"
        account = self.accounts[account_id]
        return account.transactions

    def get_summary(self, account_id):
        if account_id not in self.accounts:
            return "account not found"
        account = self.accounts[account_id]
        return {
            "owner": account.owner_name,
            "balance": account.balance,
            "transactions_count": len(account.transactions),
            "status": account.status
        }
