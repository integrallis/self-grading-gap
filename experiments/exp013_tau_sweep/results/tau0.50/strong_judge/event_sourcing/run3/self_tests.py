from solution import open_account, deposit, withdraw, close_account, get_balance, get_statement, get_summary

def test_open_account():
    assert open_account("account1", "Owner A") is None
    # Account should now exist, next command should fail
    assert open_account("account1", "Owner A") == "account already exists"

def test_deposit():
    open_account("account1", "Owner A")
    deposit("account1", 100)  # Successful deposit
    # After depositing 100, balance should be 100
    assert get_balance("account1") == 100

def test_deposit_accumulates():
    open_account("account1", "Owner A")
    deposit("account1", 100)
    deposit("account1", 50)  # Successful deposit
    # After depositing 100 and then 50, balance should be 150
    assert get_balance("account1") == 150

def test_withdraw():
    open_account("account1", "Owner A")
    deposit("account1", 100)
    withdraw("account1", 30)  # Successful withdrawal
    # After withdrawing 30, balance should be 70
    assert get_balance("account1") == 70

def test_withdraw_full_balance():
    open_account("account1", "Owner A")
    deposit("account1", 100)
    withdraw("account1", 100)  # Successful withdrawal
    # After withdrawing 100, balance should be 0
    assert get_balance("account1") == 0

def test_withdraw_insufficient_funds():
    open_account("account1", "Owner A")
    deposit("account1", 50)
    assert withdraw("account1", 100) == "insufficient funds"
    # Balance should be unchanged
    assert get_balance("account1") == 50

def test_withdraw_invalid_amount():
    open_account("account1", "Owner A")
    deposit("account1", 100)
    assert withdraw("account1", -10) == "withdrawal amount must be positive"
    assert withdraw("account1", 0) == "withdrawal amount must be positive"

def test_deposit_invalid_amount():
    open_account("account1", "Owner A")
    assert deposit("account1", -10) == "deposit amount must be positive"
    assert deposit("account1", 0) == "deposit amount must be positive"

def test_close_account_nonzero_balance():
    open_account("account1", "Owner A")
    deposit("account1", 100)
    assert close_account("account1") == "balance must be zero"
    # Status should remain "open"
    assert get_summary("account1")["status"] == "open"

def test_close_account_zero_balance():
    open_account("account1", "Owner A")
    assert close_account("account1") is None
    # After closing, account should be closed
    assert get_summary("account1")["status"] == "closed"

def test_closed_account_operations():
    open_account("account1", "Owner A")
    close_account("account1")
    assert deposit("account1", 50) == "account is closed"
    assert withdraw("account1", 50) == "account is closed"

def test_balance_as_of_timestamp():
    open_account("account1", "Owner A")
    deposit("account1", 100, timestamp=1)  # timestamp 1
    deposit("account1", 50, timestamp=2)   # timestamp 2
    assert get_balance("account1", timestamp=1) == 100
    assert get_balance("account1", timestamp=2) == 150

def test_balance_as_of_timestamp_no_account():
    assert get_balance("account2", timestamp=1) == "account not found"

def test_balance_as_of_timestamp_before_opening():
    assert get_balance("account1", timestamp=1) == "account not found"
    open_account("account1", "Owner A")

def test_get_statement():
    open_account("account1", "Owner A")
    deposit("account1", 100, timestamp=1)  # timestamp 1
    withdraw("account1", 30, timestamp=2)   # timestamp 2
    statement = get_statement("account1")
    assert statement == [
        {"kind": "deposit", "amount": 100, "timestamp": 1, "running_balance": 100},
        {"kind": "withdrawal", "amount": 30, "timestamp": 2, "running_balance": 70},
    ]

def test_statement_range_filter():
    open_account("account1", "Owner A")
    deposit("account1", 100, timestamp=1)  # timestamp 1
    deposit("account1", 50, timestamp=2)   # timestamp 2
    withdraw("account1", 30, timestamp=3)  # timestamp 3
    statement = get_statement("account1", start_timestamp=1, end_timestamp=3)
    assert statement == [
        {"kind": "deposit", "amount": 100, "timestamp": 1, "running_balance": 100},
        {"kind": "deposit", "amount": 50, "timestamp": 2, "running_balance": 150},
        {"kind": "withdrawal", "amount": 30, "timestamp": 3, "running_balance": 120},
    ]

def test_statement_empty_range():
    open_account("account1", "Owner A")
    statement = get_statement("account1", start_timestamp=5, end_timestamp=10)
    assert statement == []

def test_get_summary():
    open_account("account1", "Owner A")
    deposit("account1", 100)
    summary = get_summary("account1")
    assert summary["owner"] == "Owner A"
    assert summary["balance"] == 100
    assert summary["transactions"] == 1
    assert summary["status"] == "open"

def test_two_accounts_independence():
    open_account("account1", "Owner A")
    open_account("account2", "Owner B")
    deposit("account1", 100)
    deposit("account2", 50)
    assert get_balance("account1") == 100
    assert get_balance("account2") == 50

def test_deposit_with_one():
    open_account("account1", "Owner A")
    deposit("account1", 1)  # Successful deposit of 1
    assert get_balance("account1") == 1

def test_withdraw_with_one():
    open_account("account1", "Owner A")
    deposit("account1", 2)
    withdraw("account1", 1)  # Successful withdrawal of 1
    assert get_balance("account1") == 1

def test_deposit_to_unopened_account():
    assert deposit("account2", 100) == "account not found"

def test_withdraw_from_unopened_account():
    assert withdraw("account2", 50) == "account not found"

def test_event_stream_on_open_account():
    open_account("account1", "Owner A")
    assert len(get_event_stream("account1")) == 1  # One event for account opened

def test_event_stream_on_deposit():
    open_account("account1", "Owner A")
    deposit("account1", 100, timestamp=1)
    assert len(get_event_stream("account1")) == 2  # Two events: account opened + deposit

def test_event_stream_on_withdraw():
    open_account("account1", "Owner A")
    deposit("account1", 100, timestamp=1)
    withdraw("account1", 30, timestamp=2)
    assert len(get_event_stream("account1")) == 3  # Three events: account opened + deposit + withdrawal

def test_event_stream_on_close_account():
    open_account("account1", "Owner A")
    close_account("account1")
    assert len(get_event_stream("account1")) == 2  # Two events: account opened + account closed

def test_rehydrate_bank_from_events():
    open_account("account1", "Owner A")
    deposit("account1", 100, timestamp=1)
    withdraw("account1", 30, timestamp=2)
    event_stream = get_event_stream("account1")
    new_bank = rehydrate_bank(event_stream)
    assert new_bank.get_balance("account1") == 70
    assert new_bank.get_summary("account1")["status"] == "open"

def test_as_of_with_out_of_order_timestamps():
    open_account("account1", "Owner A")
    deposit("account1", 100, timestamp=3)
    withdraw("account1", 50, timestamp=2)
    assert get_balance("account1", timestamp=3) == 50  # Should reflect the correct balance as of timestamp 3

def test_statement_range_with_bounds():
    open_account("account1", "Owner A")
    deposit("account1", 100, timestamp=1)
    deposit("account1", 50, timestamp=2)
    withdraw("account1", 30, timestamp=3)
    statement = get_statement("account1", start_timestamp=1, end_timestamp=2)
    assert statement == [
        {"kind": "deposit", "amount": 100, "timestamp": 1, "running_balance": 100},
        {"kind": "deposit", "amount": 50, "timestamp": 2, "running_balance": 150},
    ]

def test_closed_account_summary():
    open_account("account1", "Owner A")
    close_account("account1")
    summary = get_summary("account1")
    assert summary["owner"] == "Owner A"
    assert summary["balance"] == 0
    assert summary["transactions"] == 0
    assert summary["status"] == "closed"