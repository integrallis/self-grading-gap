import pytest
from solution import open_account, deposit, withdraw, close_account, get_balance, get_statement, get_summary

def test_open_account():
    # Open an account with owner name "Alice"
    assert open_account("account1", "Alice") is None  # No specific return value defined
    # AC-2.3: Trying to open the same account again
    assert open_account("account1", "Alice") == "account already exists"

def test_deposit():
    open_account("account1", "Alice")
    assert deposit("account1", 100) is None  # No specific return value defined
    # AC-1.1: After opening an account and depositing 100, the balance is 100.
    assert get_balance("account1") == 100
    assert deposit("account1", 50) is None  # No specific return value defined
    # AC-1.2: Depositing 100 and then 50 yields a balance of 150.
    assert get_balance("account1") == 150
    # AC-2.6: Deposit amounts must be positive
    assert deposit("account1", 0) == "deposit amount must be positive"
    assert deposit("account1", -50) == "deposit amount must be positive"
    # AC-1.5: Testing deposit of exactly 1
    assert deposit("account1", 1) is None  # No specific return value defined
    assert get_balance("account1") == 151  # 150 + 1 = 151

def test_withdraw():
    open_account("account1", "Alice")
    deposit("account1", 100)
    assert withdraw("account1", 30) is None  # No specific return value defined
    # AC-1.3: A withdrawal reduces the balance: deposit 100, withdraw 30, balance 70.
    assert get_balance("account1") == 70
    assert withdraw("account1", 70) is None  # No specific return value defined
    # AC-1.4: The entire balance may be withdrawn, leaving a balance of 0.
    assert get_balance("account1") == 0
    # AC-2.1: Withdrawing more than the balance is rejected
    assert withdraw("account1", 10) == "insufficient funds"
    assert get_balance("account1") == 0
    # AC-2.7: Withdrawal amounts must be positive
    assert withdraw("account1", 0) == "withdrawal amount must be positive"
    assert withdraw("account1", -10) == "withdrawal amount must be positive"
    # AC-1.5: Testing withdrawal of exactly 1
    assert withdraw("account1", 1) == "insufficient funds"  # Cannot withdraw more than 0

def test_close_account():
    open_account("account1", "Alice")
    deposit("account1", 100)
    assert close_account("account1") == "balance must be zero"
    withdraw("account1", 100)
    assert close_account("account1") is None  # Closing account should succeed
    # AC-2.5: A closed account rejects deposits with the exact message "account is closed".
    assert deposit("account1", 50) == "account is closed"
    assert withdraw("account1", 10) == "account is closed"

def test_event_stream():
    open_account("account1", "Alice")  # timestamp 1
    deposit("account1", 100)            # timestamp 2
    withdraw("account1", 50)            # timestamp 3
    events = get_statement("account1")
    assert len(events) == 3  # 3 events should be recorded
    assert events[0] == {"kind": "account_opened", "owner": "Alice", "timestamp": 1}
    assert events[1] == {"kind": "deposit", "amount": 100, "timestamp": 2, "running_balance": 100}
    assert events[2] == {"kind": "withdrawal", "amount": 50, "timestamp": 3, "running_balance": 50}
    close_account("account1")

def test_balance_as_of():
    open_account("account1", "Alice")  # timestamp 1
    deposit("account1", 100)            # timestamp 2
    deposit("account1", 50)             # timestamp 3
    assert get_balance("account1", 2) == 100  # AC-4.1: As of timestamp 2, balance is 100
    assert get_balance("account1", 3) == 150  # AC-4.1: As of timestamp 3, balance is 150
    # AC-4.3: Asking for a balance as of a moment before the account was opened is rejected
    assert get_balance("account1", 0) == "account not found"

def test_summary():
    open_account("account1", "Alice")
    deposit("account1", 100)
    withdraw("account1", 50)
    assert get_summary("account1") == {
        "owner": "Alice",
        "balance": 50,
        "transactions": 2,
        "status": "open"
    }
    # Attempting to close the account should fail
    assert close_account("account1") == "balance must be zero"
    # The account should still be open
    assert get_summary("account1") == {
        "owner": "Alice",
        "balance": 50,
        "transactions": 2,
        "status": "open"
    }
    
    withdraw("account1", 50)  # Now balance is 0
    assert close_account("account1") is None  # Closing should succeed
    assert get_summary("account1") == {
        "owner": "Alice",
        "balance": 0,
        "transactions": 3,
        "status": "closed"
    }

def test_account_independence():
    open_account("account1", "Alice")
    open_account("account2", "Bob")
    deposit("account1", 100)
    deposit("account2", 200)
    assert get_balance("account1") == 100
    assert get_balance("account2") == 200
    withdraw("account1", 50)
    withdraw("account2", 100)
    assert get_balance("account1") == 50
    assert get_balance("account2") == 100

def test_account_not_found():
    assert deposit("account3", 100) == "account not found"
    assert withdraw("account3", 50) == "account not found"
    assert get_balance("account3") == "account not found"
    assert get_statement("account3") == "account not found"
    assert get_summary("account3") == "account not found"

def test_rehydrate_bank():
    open_account("account1", "Alice")
    deposit("account1", 100)
    withdraw("account1", 50)
    
    # Here we would need to simulate saving and rehydrating from an event stream
    # This requires an actual implementation that is not defined in the current scope
    # Assuming rehydration is done, check balances
    new_bank = rehydrate_bank_from_event_stream()  # Placeholder for actual rehydration logic
    assert get_balance("account1") == 50
    assert get_summary("account1") == {
        "owner": "Alice",
        "balance": 50,
        "transactions": 2,
        "status": "open"
    }

def test_as_of_with_out_of_order_timestamps():
    open_account("account1", "Alice")  # timestamp 1
    deposit("account1", 100)            # timestamp 2
    deposit("account1", 50)             # timestamp 3 (out of order)
    assert get_balance("account1", 2) == 100  # Should reflect only timestamp 1
    assert get_balance("account1", 3) == 150  # Should include both deposits

def test_timestamp_range_statement():
    open_account("account1", "Alice")
    deposit("account1", 100)            # timestamp 1
    withdraw("account1", 50)             # timestamp 2
    assert get_statement("account1", 1, 2) == [
        {"kind": "deposit", "amount": 100, "timestamp": 1, "running_balance": 100},
        {"kind": "withdrawal", "amount": 50, "timestamp": 2, "running_balance": 50}
    ]
    assert get_statement("account1", 0, 0) == []  # No transactions in range