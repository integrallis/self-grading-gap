# candidate/impl.py

from datetime import datetime
from collections import defaultdict

class Bank:
    def __init__(self):
        self.accounts = {}
        self.event_stream = []

    def open_account(self, account_id, owner_name):
        if account_id in self.accounts:
            return "account already exists"
        self.accounts[account_id] = Account(account_id, owner_name)
        self.record_event("opened", account_id, owner_name)
        return "account opened"

    def close_account(self, account_id):
        account = self.get_account(account_id)
        if account is None:
            return "account not found"
        if account.balance > 0:
            return "balance must be zero"
        account.close()
        self.record_event("closed", account_id)
        return "account closed"

    def deposit(self, account_id, amount):
        if amount <= 0:
            return "deposit amount must be positive"
        account = self.get_account(account_id)
        if account is None:
            return "account not found"
        if account.is_closed:
            return "account is closed"
        account.deposit(amount)
        self.record_event("deposit", account_id, amount)
        return "deposit successful"

    def withdraw(self, account_id, amount):
        if amount <= 0:
            return "withdrawal amount must be positive"
        account = self.get_account(account_id)
        if account is None:
            return "account not found"
        if account.is_closed:
            return "account is closed"
        if account.balance < amount:
            return "insufficient funds"
        account.withdraw(amount)
        self.record_event("withdraw", account_id, amount)
        return "withdrawal successful"

    def get_account(self, account_id):
        return self.accounts.get(account_id)

    def record_event(self, event_type, account_id, payload=None):
        event = {
            "timestamp": datetime.now(),
            "account_id": account_id,
            "event_type": event_type,
            "payload": payload
        }
        self.event_stream.append(event)

    def balance_as_of(self, account_id, timestamp):
        account = self.get_account(account_id)
        if account is None:
            return "account not found"
        return account.balance_as_of(timestamp)

    def statement(self, account_id):
        account = self.get_account(account_id)
        if account is None:
            return "account not found"
        return account.get_statement()

class Account:
    def __init__(self, account_id, owner_name):
        self.account_id = account_id
        self.owner_name = owner_name
        self.balance = 0
        self.is_closed = False
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.record_transaction("deposit", amount)

    def withdraw(self, amount):
        self.balance -= amount
        self.record_transaction("withdraw", amount)

    def close(self):
        self.is_closed = True

    def record_transaction(self, kind, amount):
        timestamp = datetime.now()
        self.transactions.append({"kind": kind, "amount": amount, "timestamp": timestamp, "balance": self.balance})

    def balance_as_of(self, timestamp):
        if self.is_closed and not self.transactions:
            return self.balance
        for transaction in reversed(self.transactions):
            if transaction["timestamp"] <= timestamp:
                return transaction["balance"]
        return "account not found"

    def get_statement(self):
        return {
            "owner": self.owner_name,
            "balance": self.balance,
            "transactions": self.transactions,
            "status": "closed" if self.is_closed else "open"
        }
