# test_bank_ledger.py
import pytest
from solution import open_account, deposit, withdraw, close_account, get_balance, get_statement, get_summary

def test_open_account():
    assert open_account("account1", "Alice") is None  # Account opened successfully
    assert open_account("account1", "Alice") == "account already exists"  # Duplicate opening

def test_deposit():
    open_account("account1", "Alice")  # Account must be opened first
    assert deposit("account1", 100) is None  # Deposit successful
    assert get_balance("account1") == 100  # Balance is now 100
    assert deposit("account1", 50) is None  # Deposit successful
    assert get_balance("account1") == 150  # Balance is now 150
    assert deposit("account1", 0) == "deposit amount must be positive"  # Invalid deposit
    assert deposit("account1", -10) == "deposit amount must be positive"  # Invalid deposit
    assert deposit("account1", 1) is None  # Deposit successful with amount of 1
    assert get_balance("account1") == 151  # Balance is now 151

def test_withdraw():
    open_account("account2", "Bob")  # Account must be opened first
    deposit("account2", 100)  # Initial deposit
    assert withdraw("account2", 30) is None  # Withdrawal successful
    assert get_balance("account2") == 70  # Balance is now 70
    assert withdraw("account2", 100) == "insufficient funds"  # Trying to withdraw more than balance
    assert get_balance("account2") == 70  # Balance unchanged
    assert withdraw("account2", 0) == "withdrawal amount must be positive"  # Invalid withdrawal
    assert withdraw("account2", -10) == "withdrawal amount must be positive"  # Invalid withdrawal
    assert withdraw("account2", 1) is None  # Withdrawal successful with amount of 1
    assert get_balance("account2") == 69  # Balance is now 69

def test_withdraw_full_balance():
    open_account("account3", "Charlie")
    deposit("account3", 100)
    assert withdraw("account3", 100) is None  # Withdrawal successful
    assert get_balance("account3") == 0  # Balance is now 0

def test_close_account():
    open_account("account4", "David")
    deposit("account4", 50)
    assert close_account("account4") == "balance must be zero"  # Cannot close with non-zero balance
    withdraw("account4", 50)
    assert close_account("account4") is None  # Close account successfully
    assert get_balance("account4") == "account is closed"  # Account is closed
    assert close_account("account4") == "account is closed"  # Cannot close again

def test_balance_queries():
    open_account("account5", "Eve")
    assert get_balance("account5") == 0  # Balance is 0
    deposit("account5", 200)
    assert get_balance("account5") == 200  # Balance is 200
    assert get_balance("account5") == 200  # Balance is still 200

def test_event_logging():
    open_account("account6", "Frank")
    deposit("account6", 150)
    withdraw("account6", 50)
    events = get_statement("account6")  # Assuming this returns the event stream
    assert len(events) == 3  # One open, one deposit, one withdrawal
    assert events[0]["account_id"] == "account6"  # Account ID for opening
    assert events[0]["kind"] == "account_opened"  # Event for account opening
    assert events[0]["payload"] == "Frank"  # Owner's name
    assert events[1]["account_id"] == "account6"  # Account ID for deposit
    assert events[1]["kind"] == "deposit"  # Event for deposit
    assert events[1]["payload"] == 150  # Amount for deposit
    assert events[2]["account_id"] == "account6"  # Account ID for withdrawal
    assert events[2]["kind"] == "withdrawal"  # Event for withdrawal
    assert events[2]["payload"] == 50  # Amount for withdrawal

def test_query_balance_as_of():
    open_account("account7", "Grace")  # Opening at timestamp 1
    deposit("account7", 100)  # At timestamp 2
    deposit("account7", 50)   # At timestamp 3
    assert get_balance("account7") == 150  # Current balance
    assert get_balance("account7", as_of_timestamp=2) == 100  # As of timestamp 2
    assert get_balance("account7", as_of_timestamp=3) == 150  # As of timestamp 3
    assert get_balance("account7", as_of_timestamp=0) == "account not found"  # Before account opened
    assert get_balance("account8", as_of_timestamp=1) == "account not found"  # Nonexistent account

def test_account_independence():
    open_account("account9", "Hannah")
    open_account("account10", "Ian")
    deposit("account9", 100)
    deposit("account10", 200)
    assert get_balance("account9") == 100  # Balance for account9
    assert get_balance("account10") == 200  # Balance for account10
    assert get_balance("account9") == 100  # Balance for account9 remains unchanged

def test_account_not_found():
    assert deposit("account11", 50) == "account not found"  # Deposit on never-opened account
    assert withdraw("account11", 50) == "account not found"  # Withdrawal on never-opened account

def test_closed_account_rejection():
    open_account("account12", "Jack")
    deposit("account12", 100)
    withdraw("account12", 100)
    close_account("account12")  # Close the account
    assert deposit("account12", 50) == "account is closed"  # Deposit on closed account
    assert withdraw("account12", 50) == "account is closed"  # Withdrawal on closed account

def test_close_zero_balance_account():
    open_account("account13", "Liam")
    assert close_account("account13") is None  # Close account successfully
    assert get_summary("account13")["status"] == "closed"  # Check status of closed account

def test_statement_range():
    open_account("account14", "Mia")
    deposit("account14", 100)  # At timestamp 1
    deposit("account14", 50)   # At timestamp 2
    assert get_statement("account14") == [
        {"kind": "deposit", "amount": 100, "timestamp": 1, "running_balance": 100},
        {"kind": "deposit", "amount": 50, "timestamp": 2, "running_balance": 150},
    ]  # Inclusive of both timestamps
    assert get_statement("account14", start_timestamp=3, end_timestamp=4) == []  # Empty range

def test_summary():
    open_account("account15", "Noah")
    deposit("account15", 100)
    withdraw("account15", 50)
    summary = get_summary("account15")
    assert summary["owner"] == "Noah"  # Owner name
    assert summary["balance"] == 50  # Current balance
    assert summary["transaction_count"] == 2  # Number of transactions
    assert summary["status"] == "open"  # Status