# candidate/impl.py

from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Any, Tuple

class BankAccount:
    def __init__(self, owner: str):
        self.owner = owner
        self.balance = 0
        self.status = "open"
        self.transactions = []
        self.event_stream = []

    def deposit(self, amount: int, timestamp: datetime) -> str:
        if amount <= 0:
            return "deposit amount must be positive"
        if self.status == "closed":
            return "account is closed"
        
        self.balance += amount
        self.transactions.append((timestamp, "deposit", amount, self.balance))
        self.event_stream.append((timestamp, "deposit", amount))
        return "success"

    def withdraw(self, amount: int, timestamp: datetime) -> str:
        if amount <= 0:
            return "withdrawal amount must be positive"
        if self.status == "closed":
            return "account is closed"
        if amount > self.balance:
            return "insufficient funds"

        self.balance -= amount
        self.transactions.append((timestamp, "withdrawal", amount, self.balance))
        self.event_stream.append((timestamp, "withdrawal", amount))
        return "success"

    def close(self, timestamp: datetime) -> str:
        if self.balance > 0:
            return "balance must be zero"
        
        self.status = "closed"
        self.event_stream.append((timestamp, "close", None))
        return "success"

    def get_balance(self) -> int:
        return self.balance

    def get_transactions(self) -> List[Tuple[datetime, str, int, int]]:
        return self.transactions

    def get_status(self) -> str:
        return self.status

    def get_event_stream(self) -> List[Tuple[datetime, str, Any]]:
        return self.event_stream

class Bank:
    def __init__(self):
        self.accounts: Dict[str, BankAccount] = {}

    def open_account(self, account_id: str, owner: str, timestamp: datetime) -> str:
        if account_id in self.accounts:
            return "account already exists"
        
        self.accounts[account_id] = BankAccount(owner)
        self.accounts[account_id].event_stream.append((timestamp, "open", owner))
        return "success"

    def deposit(self, account_id: str, amount: int, timestamp: datetime) -> str:
        account = self.accounts.get(account_id)
        if not account:
            return "account not found"
        return account.deposit(amount, timestamp)

    def withdraw(self, account_id: str, amount: int, timestamp: datetime) -> str:
        account = self.accounts.get(account_id)
        if not account:
            return "account not found"
        return account.withdraw(amount, timestamp)

    def close_account(self, account_id: str, timestamp: datetime) -> str:
        account = self.accounts.get(account_id)
        if not account:
            return "account not found"
        return account.close(timestamp)

    def get_balance(self, account_id: str) -> int:
        account = self.accounts.get(account_id)
        if not account:
            raise ValueError("account not found")
        return account.get_balance()

    def get_transaction_history(self, account_id: str) -> List[Tuple[datetime, str, int, int]]:
        account = self.accounts.get(account_id)
        if not account:
            raise ValueError("account not found")
        return account.get_transactions()

    def get_account_summary(self, account_id: str) -> Dict[str, Any]:
        account = self.accounts.get(account_id)
        if not account:
            raise ValueError("account not found")
        return {
            "owner": account.owner,
            "balance": account.get_balance(),
            "transactions_count": len(account.get_transactions()),
            "status": account.get_status()
        }

    def get_balance_as_of(self, account_id: str, timestamp: datetime) -> int:
        account = self.accounts.get(account_id)
        if not account:
            raise ValueError("account not found")
        
        balance = 0
        for event in account.get_event_stream():
            if event[0] <= timestamp:
                if event[1] == "deposit":
                    balance += event[2]
                elif event[1] == "withdrawal":
                    balance -= event[2]
        return balance
