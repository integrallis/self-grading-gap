def open_account(owner, account_id):
    if account_id in accounts:
        return "account already exists"
    accounts[account_id] = {
        'owner': owner,
        'balance': 0,
        'transactions': [],
        'status': 'open'
    }
    return f"{account_id} opened"

def deposit(account_id, amount):
    if account_id not in accounts:
        return "account not found"
    if accounts[account_id]['status'] == 'closed':
        return "account is closed"
    if amount <= 0:
        return "deposit amount must be positive"
    accounts[account_id]['balance'] += amount
    accounts[account_id]['transactions'].append({
        'type': 'deposit',
        'amount': amount,
        'timestamp': len(accounts[account_id]['transactions']) + 1,
        'running_balance': accounts[account_id]['balance']
    })
    return f"deposited {amount} to {account_id}"

def withdraw(account_id, amount):
    if account_id not in accounts:
        return "account not found"
    if accounts[account_id]['status'] == 'closed':
        return "account is closed"
    if amount <= 0:
        return "withdrawal amount must be positive"
    if accounts[account_id]['balance'] < amount:
        return "insufficient funds"
    accounts[account_id]['balance'] -= amount
    accounts[account_id]['transactions'].append({
        'type': 'withdrawal',
        'amount': amount,
        'timestamp': len(accounts[account_id]['transactions']) + 1,
        'running_balance': accounts[account_id]['balance']
    })
    return f"withdrew {amount} from {account_id}"

def close_account(account_id):
    if account_id not in accounts:
        return "account not found"
    if accounts[account_id]['balance'] != 0:
        return "balance must be zero"
    del accounts[account_id]
    return f"{account_id} closed"

def get_balance(account_id):
    if account_id not in accounts:
        return "account not found"
    return accounts[account_id]['balance']


def get_statement(account_id):
    if account_id not in accounts:
        return "account not found"
    return accounts[account_id]['transactions']


def get_summary(account_id):
    if account_id not in accounts:
        return "account not found"
    account = accounts[account_id]
    return {
        'owner': account['owner'],
        'balance': account['balance'],
        'transactions': len(account['transactions']),
        'status': account['status']
    }

accounts = {}