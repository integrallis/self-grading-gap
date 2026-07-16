accounts = {}  

class Account:  
    def __init__(self, owner):  
        self.owner = owner  
        self.balance = 0  
        self.closed = False  
        self.history = []  

    def deposit(self, amount):  
        if amount <= 0:  
            return "deposit amount must be positive"  
        self.balance += amount  
        self.history.append({  
            "type": "deposit",  
            "amount": amount,  
            "timestamp": "some_timestamp",  
            "balance": self.balance  
        })  
        return "Deposit successful"  

    def withdraw(self, amount):  
        if amount <= 0:  
            return "withdrawal amount must be positive"  
        if amount > self.balance:  
            return "insufficient funds"  
        self.balance -= amount  
        self.history.append({  
            "type": "withdrawal",  
            "amount": amount,  
            "timestamp": "some_timestamp",  
            "balance": self.balance  
        })  
        return "Withdrawal successful"  

    def close(self):  
        if self.balance != 0:  
            return "balance must be zero"  
        self.closed = True  
        return "Account closed"  


def open_account(account_id, owner):  
    if account_id in accounts:  
        return "account already exists"  
    accounts[account_id] = Account(owner)  
    return "Account opened"  


def deposit(account_id, amount):  
    if account_id not in accounts:  
        return "account not found"  
    return accounts[account_id].deposit(amount)  


def withdraw(account_id, amount):  
    if account_id not in accounts:  
        return "account not found"  
    return accounts[account_id].withdraw(amount)  


def close_account(account_id):  
    if account_id not in accounts:  
        return "account not found"  
    return accounts[account_id].close()  


def get_balance(account_id):  
    if account_id not in accounts:  
        return "account not found"  
    return accounts[account_id].balance  


def get_statement(account_id):  
    if account_id not in accounts:  
        return "account not found"  
    return accounts[account_id].history  


def get_summary(account_id):  
    if account_id not in accounts:  
        return "account not found"  
    account = accounts[account_id]  
    return {  
        "owner": account.owner,  
        "balance": account.balance,  
        "transactions": len(account.history),  
        "status": "open" if not account.closed else "closed"  
    }  
