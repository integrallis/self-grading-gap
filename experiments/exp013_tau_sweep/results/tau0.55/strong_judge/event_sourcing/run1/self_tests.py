# test_bank_ledger.py

from solution import open_account, deposit, withdraw, close_account, get_balance, get_statement, get_summary, get_event_stream, rehydrate_from_event_stream

def test_open_account():
    # Opening an account should succeed
    assert open_account("account1", "Alice") is None
    # AC-2.3: Opening account again should be rejected
    assert open_account("account1", "Alice") == "account already exists"

def test_deposit():
    open_account("account1", "Alice")
    assert deposit("account1", 100) is None
    # AC-1.1: After opening an account and depositing 100, the balance is 100
    assert get_balance("account1") == 100
    assert deposit("account1", 50) is None
    # AC-1.2: Depositing 100 and then 50 yields a balance of 150
    assert get_balance("account1") == 150
    # AC-2.6: Depositing zero or negative amounts is rejected
    assert deposit("account1", 0) == "deposit amount must be positive"
    assert deposit("account1", -10) == "deposit amount must be positive"
    # AC-1.5: Depositing exactly 1
    assert deposit("account1", 1) is None
    assert get_balance("account1") == 151

def test_withdraw():
    open_account("account1", "Alice")
    deposit("account1", 100)
    assert withdraw("account1", 30) is None
    # AC-1.3: Withdraw 30, expect balance 70
    assert get_balance("account1") == 70
    assert withdraw("account1", 70) is None
    # AC-1.4: Entire balance withdrawn, expect balance 0
    assert get_balance("account1") == 0
    # AC-2.1: Withdrawing more than balance
    assert withdraw("account1", 10) == "insufficient funds"
    assert get_balance("account1") == 0
    # AC-2.7: Withdrawal must be positive
    assert withdraw("account1", 0) == "withdrawal amount must be positive"
    assert withdraw("account1", -10) == "withdrawal amount must be positive"
    # AC-1.5: Withdrawing exactly 1
    assert withdraw("account1", 1) == "insufficient funds"

def test_close_account():
    open_account("account1", "Alice")
    deposit("account1", 100)
    assert close_account("account1") == "balance must be zero"
    assert withdraw("account1", 100) is None
    assert close_account("account1") is None
    # AC-2.5: Closed account rejects withdrawal
    assert withdraw("account1", 10) == "account is closed"
    assert deposit("account1", 10) == "account is closed"

def test_balance_as_of():
    open_account("account1", "Alice")
    deposit("account1", 100)  # timestamp 1
    deposit("account1", 50)    # timestamp 2
    assert get_balance("account1", 1) == 100  # AC-4.1
    assert get_balance("account1", 2) == 150  # AC-4.1
    # AC-4.3: Asking for balance before account opened
    assert get_balance("account1", 0) == "account not found"

def test_statement():
    open_account("account1", "Alice")
    deposit("account1", 100)  # timestamp 1
    withdraw("account1", 30)   # timestamp 2
    assert get_statement("account1") == [
        {"kind": "deposit", "amount": 100, "timestamp": 1, "balance": 100},
        {"kind": "withdrawal", "amount": 30, "timestamp": 2, "balance": 70}
    ]  # AC-5.1

def test_statement_range_filter():
    open_account("account1", "Alice")
    deposit("account1", 100)  # timestamp 1
    withdraw("account1", 30)   # timestamp 2
    assert get_statement("account1") == [
        {"kind": "deposit", "amount": 100, "timestamp": 1, "balance": 100},
        {"kind": "withdrawal", "amount": 30, "timestamp": 2, "balance": 70}
    ]  # AC-5.1
    assert get_statement("account1", 1, 2) == [
        {"kind": "deposit", "amount": 100, "timestamp": 1, "balance": 100},
        {"kind": "withdrawal", "amount": 30, "timestamp": 2, "balance": 70}
    ]  # AC-5.2
    assert get_statement("account1", 2, 2) == [
        {"kind": "withdrawal", "amount": 30, "timestamp": 2, "balance": 70}
    ]  # AC-5.2
    assert get_statement("account1", 3, 5) == []  # AC-5.2

def test_summary():
    open_account("account1", "Alice")
    deposit("account1", 100)
    withdraw("account1", 30)
    summary = get_summary("account1")
    assert summary["owner"] == "Alice"  # AC-5.3
    assert summary["balance"] == 70
    assert summary["transactions"] == 2
    assert summary["status"] == "open"

def test_deposit_to_never_opened_account():
    assert deposit("account2", 50) == "account not found"

def test_withdraw_from_never_opened_account():
    assert withdraw("account2", 50) == "account not found"

def test_close_zero_balance_account():
    open_account("account1", "Alice")
    assert close_account("account1") is None
    assert get_summary("account1")["status"] == "closed"

def test_independent_accounts():
    open_account("account1", "Alice")
    open_account("account2", "Bob")
    deposit("account1", 100)
    deposit("account2", 50)
    assert get_balance("account1") == 100
    assert get_balance("account2") == 50
    withdraw("account1", 30)
    assert get_balance("account1") == 70
    assert get_balance("account2") == 50

def test_event_stream():
    open_account("account1", "Alice")
    deposit("account1", 100)  # timestamp 1
    withdraw("account1", 30)   # timestamp 2
    events = get_event_stream("account1")
    assert len(events) == 3
    assert events[0]["account_id"] == "account1"
    assert events[0]["action"] == "open"
    assert events[1]["account_id"] == "account1"
    assert events[1]["action"] == "deposit"
    assert events[1]["payload"] == 100
    assert events[2]["account_id"] == "account1"
    assert events[2]["action"] == "withdraw"
    assert events[2]["payload"] == 30

def test_successful_close_event():
    open_account("account1", "Alice")
    deposit("account1", 100)
    withdraw("account1", 100)  # closing with zero balance
    close_event = close_account("account1")
    assert close_event is None  # Close should succeed
    events = get_event_stream("account1")
    assert len(events) == 2  # open and close events
    assert events[1]["account_id"] == "account1"
    assert events[1]["action"] == "close"

def test_rehydration():
    open_account("account1", "Alice")
    deposit("account1", 100)
    withdraw("account1", 30)
    events = get_event_stream("account1")
    rehydrated_bank = rehydrate_from_event_stream(events)
    assert rehydrated_bank.get_balance("account1") == 70
    assert rehydrated_bank.get_summary("account1")["status"] == "open"

def test_query_missing_account():
    assert get_balance("account2") == "account not found"
    assert get_statement("account2") == "account not found"
    assert get_summary("account2") == "account not found"