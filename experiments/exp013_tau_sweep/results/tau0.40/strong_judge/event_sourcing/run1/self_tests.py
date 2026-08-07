from solution import open_account, deposit, withdraw, close_account, get_balance, get_statement, get_summary

def test_open_account():
    # Opening an account with identifier "account1" should succeed.
    open_account("account1", "Owner Name")

def test_open_account_already_exists():
    # Opening the same account again should fail with "account already exists".
    open_account("account1", "Owner Name")
    assert open_account("account1", "Owner Name") == "account already exists"

def test_deposit_positive_amount():
    # After opening an account and depositing 100, the balance should be 100.
    open_account("account1", "Owner Name")
    deposit("account1", 100)
    assert get_balance("account1") == 100  # Expected balance is 100

def test_deposit_accumulates():
    # Depositing 100 and then 50 should yield a balance of 150.
    open_account("account1", "Owner Name")
    deposit("account1", 100)
    deposit("account1", 50)
    assert get_balance("account1") == 150  # Expected balance is 150

def test_withdraw_reduces_balance():
    # After depositing 100 and withdrawing 30, balance should be 70.
    open_account("account1", "Owner Name")
    deposit("account1", 100)
    withdraw("account1", 30)
    assert get_balance("account1") == 70  # Expected balance is 70

def test_withdraw_entire_balance():
    # Withdrawing the entire balance should leave a balance of 0.
    open_account("account1", "Owner Name")
    deposit("account1", 100)
    withdraw("account1", 100)
    assert get_balance("account1") == 0  # Expected balance is 0

def test_withdraw_more_than_balance():
    # Withdrawing more than the balance should be rejected with "insufficient funds".
    open_account("account1", "Owner Name")
    deposit("account1", 100)
    assert withdraw("account1", 150) == "insufficient funds"  # Message expected
    assert get_balance("account1") == 100  # Balance should remain unchanged

def test_withdraw_invalid_account():
    # Withdrawing from a non-existent account should be rejected with "account not found".
    assert withdraw("account_non_existent", 50) == "account not found"  # Message expected

def test_deposit_invalid_account():
    # Depositing to a non-existent account should be rejected with "account not found".
    assert deposit("account_non_existent", 50) == "account not found"  # Message expected

def test_deposit_negative_amount():
    # Depositing a negative amount should be rejected with "deposit amount must be positive".
    open_account("account1", "Owner Name")
    assert deposit("account1", -50) == "deposit amount must be positive"  # Message expected

def test_withdraw_negative_amount():
    # Withdrawing a negative amount should be rejected with "withdrawal amount must be positive".
    open_account("account1", "Owner Name")
    assert withdraw("account1", -50) == "withdrawal amount must be positive"  # Message expected

def test_close_account_with_nonzero_balance():
    # Closing an account with a non-zero balance should be rejected with "balance must be zero".
    open_account("account1", "Owner Name")
    deposit("account1", 100)
    assert close_account("account1") == "balance must be zero"  # Message expected

def test_close_account_success():
    # Closing an account with a zero balance should succeed.
    open_account("account1", "Owner Name")
    deposit("account1", 100)
    withdraw("account1", 100)
    close_account("account1")
    assert get_summary("account1")["status"] == "closed"  # Status should be closed

def test_closed_account_rejects_deposit():
    # A closed account should reject deposits with "account is closed".
    open_account("account1", "Owner Name")
    deposit("account1", 100)
    withdraw("account1", 100)
    close_account("account1")
    assert deposit("account1", 50) == "account is closed"  # Message expected

def test_closed_account_rejects_withdrawal():
    # A closed account should reject withdrawals with "account is closed".
    open_account("account1", "Owner Name")
    deposit("account1", 100)
    withdraw("account1", 100)
    close_account("account1")
    assert withdraw("account1", 50) == "account is closed"  # Message expected

def test_get_balance_before_account_opened():
    # Asking for a balance before the account was opened should be rejected with "account not found".
    assert get_balance("account_non_existent") == "account not found"  # Message expected

def test_get_statement():
    # The transaction history should reflect each deposit and withdrawal.
    open_account("account1", "Owner Name")
    deposit("account1", 100)  # Suppose this happens at timestamp 1
    withdraw("account1", 30)   # Suppose this happens at timestamp 2
    deposit("account1", 50)    # Suppose this happens at timestamp 3
    statement = get_statement("account1")
    expected_statement = [
        {"kind": "deposit", "amount": 100, "timestamp": 1, "running_balance": 100},
        {"kind": "withdrawal", "amount": 30, "timestamp": 2, "running_balance": 70},
        {"kind": "deposit", "amount": 50, "timestamp": 3, "running_balance": 120},
    ]
    assert statement == expected_statement

def test_get_summary():
    # The account summary should report the correct owner's name, current balance, number of transactions, and status.
    open_account("account1", "Owner Name")
    deposit("account1", 100)
    withdraw("account1", 30)
    summary = get_summary("account1")
    expected_summary = {
        "owner": "Owner Name",
        "balance": 70,
        "transactions": 2,
        "status": "open"
    }
    assert summary == expected_summary

def test_get_balance_as_of_timestamp():
    # The balance as of a timestamp should reflect every event up to that moment.
    open_account("account1", "Owner Name")
    deposit("account1", 100)  # Timestamp 1
    deposit("account1", 50)    # Timestamp 2
    assert get_balance("account1", as_of=1) == 100  # Expected balance at timestamp 1
    assert get_balance("account1", as_of=2) == 150  # Expected balance at timestamp 2

def test_get_balance_as_of_before_opening():
    # Asking for a balance as of a moment before the account was opened should be rejected with "account not found".
    open_account("account1", "Owner Name")
    deposit("account1", 100)  # Timestamp 1
    assert get_balance("account1", as_of=0) == "account not found"  # Message expected

def test_event_stream_records():
    # Each accepted command should append exactly one event in command order with account id, payload, and timestamp.
    open_account("account1", "Owner Name")  # Event 1
    deposit("account1", 100)                 # Event 2
    withdraw("account1", 50)                  # Event 3
    events = get_events("account1")           # Assuming a function that retrieves the event log
    expected_events = [
        {"account": "account1", "type": "open_account", "payload": "Owner Name", "timestamp": 1},
        {"account": "account1", "type": "deposit", "payload": 100, "timestamp": 2},
        {"account": "account1", "type": "withdrawal", "payload": 50, "timestamp": 3},
    ]
    assert events == expected_events

def test_rehydration_from_event_stream():
    # A bank rehydrated from a recorded event stream should report the same balances and account status as the original.
    open_account("account1", "Owner Name")
    deposit("account1", 100)
    withdraw("account1", 50)
    events = get_events("account1")  # Assuming a function that retrieves the event log
    rehydrated_bank = rehydrate_bank(events)  # Assuming a function to rehydrate the bank from events
    assert rehydrated_bank.get_balance("account1") == 50  # Balance should match
    assert rehydrated_bank.get_summary("account1")["status"] == "open"  # Status should match

def test_query_nonexistent_account_in_stream():
    # Querying an account in a stream that never recorded that account's opening should be rejected with "account not found".
    events = []  # No events for account1
    rehydrated_bank = rehydrate_bank(events)  # Assuming a function to rehydrate the bank from events
    assert rehydrated_bank.get_balance("account1") == "account not found"  # Message expected

def test_statement_range_filter():
    # Transactions can be filtered to a timestamp range; both bounds are inclusive.
    open_account("account1", "Owner Name")
    deposit("account1", 100)  # Timestamp 1
    withdraw("account1", 50)   # Timestamp 2
    deposit("account1", 200)   # Timestamp 3
    statement = get_statement("account1", start=1, end=3)  # Get statement for timestamps 1 to 3
    expected_statement = [
        {"kind": "deposit", "amount": 100, "timestamp": 1, "running_balance": 100},
        {"kind": "withdrawal", "amount": 50, "timestamp": 2, "running_balance": 50},
        {"kind": "deposit", "amount": 200, "timestamp": 3, "running_balance": 250},
    ]
    assert statement == expected_statement

def test_statement_empty_range():
    # A range containing no transactions yields an empty list.
    open_account("account1", "Owner Name")
    statement = get_statement("account1", start=10, end=20)  # No transactions in this range
    assert statement == []  # Expecting an empty list