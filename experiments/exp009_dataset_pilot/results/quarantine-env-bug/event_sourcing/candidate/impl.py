# candidate/impl.py

from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Tuple, Union

class Account:
    def __init__(self, owner: str):
        self.owner = owner
        self.balance = 0
        self.status = 'open'
        self.events = []

    def deposit(self, amount: int, timestamp: datetime) -> Union[str, None]:
        if amount <= 0:
            return "deposit amount must be positive"
        if self.status == 'closed':
            return "account is closed"
        
        self.balance += amount
        self.events.append(('deposit', amount, timestamp, self.balance))

    def withdraw(self, amount: int, timestamp: datetime) -> Union[str, None]:
        if amount <= 0:
            return "withdrawal amount must be positive"
        if self.status == 'closed':
            return "account is closed"
        if amount > self.balance:
            return "insufficient funds"
        
        self.balance -= amount
        self.events.append(('withdrawal', amount, timestamp, self.balance))

    def close(self, timestamp: datetime) -> Union[str, None]:
        if self.balance > 0:
            return "balance must be zero"
        self.status = 'closed'
        self.events.append(('account_closed', self.owner, timestamp))

    def get_balance(self) -> int:
        return self.balance

    def get_events(self) -> List[Tuple[str, int, datetime, int]]:
        return self.events

class Bank:
    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self.event_stream: List[Tuple[str, Union[int, str], datetime]] = []

    def open_account(self, account_id: str, owner: str, timestamp: datetime) -> Union[str, None]:
        if account_id in self.accounts:
            return "account already exists"
        
        self.accounts[account_id] = Account(owner)
        self.event_stream.append((account_id, owner, timestamp))
    
    def deposit(self, account_id: str, amount: int, timestamp: datetime) -> Union[str, None]:
        account = self.accounts.get(account_id)
        if not account:
            return "account not found"
        
        error = account.deposit(amount, timestamp)
        if error is None:
            self.event_stream.append((account_id, amount, timestamp))
        return error

    def withdraw(self, account_id: str, amount: int, timestamp: datetime) -> Union[str, None]:
        account = self.accounts.get(account_id)
        if not account:
            return "account not found"
        
        error = account.withdraw(amount, timestamp)
        if error is None:
            self.event_stream.append((account_id, -amount, timestamp))
        return error

    def close_account(self, account_id: str, timestamp: datetime) -> Union[str, None]:
        account = self.accounts.get(account_id)
        if not account:
            return "account not found"
        
        error = account.close(timestamp)
        if error is None:
            self.event_stream.append((account_id, 'closed', timestamp))
        return error

    def get_balance(self, account_id: str) -> Union[str, int]:
        account = self.accounts.get(account_id)
        if not account:
            return "account not found"
        
        return account.get_balance()

    def get_statement(self, account_id: str) -> Union[str, List[Tuple[str, int, datetime, int]]]:
        account = self.accounts.get(account_id)
        if not account:
            return "account not found"
        
        return account.get_events()

    def get_summary(self, account_id: str) -> Union[str, Dict[str, Union[str, int]]]:
        account = self.accounts.get(account_id)
        if not account:
            return "account not found"
        
        return {
            'owner': account.owner,
            'balance': account.get_balance(),
            'transaction_count': len(account.get_events()),
            'status': account.status
        }

    def balance_as_of(self, account_id: str, timestamp: datetime) -> Union[str, int]:
        account = self.accounts.get(account_id)
        if not account:
            return "account not found"
        
        balance = 0
        for event in account.get_events():
            event_time = event[2]
            if event_time <= timestamp:
                if event[0] == 'deposit':
                    balance += event[1]
                elif event[0] == 'withdrawal':
                    balance -= event[1]
        
        return balance
