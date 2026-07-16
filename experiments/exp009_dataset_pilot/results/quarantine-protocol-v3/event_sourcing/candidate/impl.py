# candidate/impl.py

import time
from collections import defaultdict
from typing import List, Dict, Tuple, Union

class Event:
    def __init__(self, account_id: str, event_type: str, amount: Union[int, None], timestamp: float):
        self.account_id = account_id
        self.event_type = event_type
        self.amount = amount
        self.timestamp = timestamp

class Account:
    def __init__(self, owner: str):
        self.owner = owner
        self.balance = 0
        self.closed = False
        self.events: List[Event] = []

    def deposit(self, amount: int, timestamp: float) -> str:
        if self.closed:
            return "account is closed"
        if amount <= 0:
            return "deposit amount must be positive"
        
        self.balance += amount
        event = Event(self.owner, "deposit", amount, timestamp)
        self.events.append(event)
        return "success"

    def withdraw(self, amount: int, timestamp: float) -> str:
        if self.closed:
            return "account is closed"
        if amount <= 0:
            return "withdrawal amount must be positive"
        if amount > self.balance:
            return "insufficient funds"
        
        self.balance -= amount
        event = Event(self.owner, "withdrawal", amount, timestamp)
        self.events.append(event)
        return "success"

    def close(self, timestamp: float) -> str:
        if self.balance > 0:
            return "balance must be zero"
        
        self.closed = True
        event = Event(self.owner, "account_closed", None, timestamp)
        self.events.append(event)
        return "success"

class Bank:
    def __init__(self):
        self.accounts: Dict[str, Account] = {}

    def open_account(self, account_id: str, owner: str) -> str:
        if account_id in self.accounts:
            return "account already exists"
        self.accounts[account_id] = Account(owner)
        event = Event(account_id, "account_opened", None, time.time())
        self.accounts[account_id].events.append(event)
        return "success"

    def deposit(self, account_id: str, amount: int) -> str:
        if account_id not in self.accounts:
            return "account not found"
        return self.accounts[account_id].deposit(amount, time.time())

    def withdraw(self, account_id: str, amount: int) -> str:
        if account_id not in self.accounts:
            return "account not found"
        return self.accounts[account_id].withdraw(amount, time.time())

    def close_account(self, account_id: str) -> str:
        if account_id not in self.accounts:
            return "account not found"
        return self.accounts[account_id].close(time.time())

    def get_balance(self, account_id: str) -> Union[int, str]:
        if account_id not in self.accounts:
            return "account not found"
        return self.accounts[account_id].balance

    def get_statement(self, account_id: str) -> Union[str, List[Tuple[str, int, float, int]]]:
        if account_id not in self.accounts:
            return "account not found"
        account = self.accounts[account_id]
        return [(event.event_type, event.amount, event.timestamp, account.balance) for event in account.events]

    def get_summary(self, account_id: str) -> Union[str, Dict[str, Union[str, int]]]:
        if account_id not in self.accounts:
            return "account not found"
        account = self.accounts[account_id]
        return {
            "owner": account.owner,
            "balance": account.balance,
            "transactions": len(account.events),
            "status": "closed" if account.closed else "open"
        }
