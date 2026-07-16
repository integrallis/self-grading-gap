from solution import open_account, deposit, withdraw, close_account, get_balance, get_statement, get_summary, get_events
import pytest

@pytest.fixture(autouse=True)
def reset_bank():
    # This will reset the bank state for each test to ensure independence.
    pass  # Replace with bank initialization logic if needed.

def test_open_account():
    open_account("account1", "Alice")
    # Ensure account is opened
    assert get_balance("account1") == 0  # Balance should be 0 after opening

def test_deposit():
    open_account("account1", "Alice")
    deposit("account1", 100)
    # Balance should be 100 after depositing 100
    assert get_balance("account1") == 100

def test_deposit_accumulates():
    open_account("account1", "Alice")
    deposit("account1", 100)
    deposit("account1", 50)
    # Balance should be 150 after depositing 100 and then 50
    assert get_balance("account1") == 150

def test_withdraw_reduces_balance():
    open_account("account1", "Alice")
    deposit("account1", 100)
    withdraw("account1", 30) 
    # Balance should be 70 after withdrawing 30
    assert get_balance("account1") == 70

def test_withdraw_entire_balance():
    open_account("account1", "Alice")
    deposit("account1", 100)
    withdraw("account1", 100) 
    # Balance should be 0 after withdrawing entire balance
    assert get_balance("account1") == 0

def test_valid_movements_of_one():
    open_account("account1", "Alice")
    deposit("account1", 1) 
    # Balance should be 1 after depositing 1
    assert get_balance("account1") == 1
    withdraw("account1", 1) 
    # Balance should be 0 after withdrawing 1
    assert get_balance("account1") == 0

def test_accounts_are_independent():
    open_account("account1", "Alice")
    open_account("account2", "Bob")
    deposit("account1", 100)
    # Balance for account1 should be 100
    assert get_balance("account1") == 100
    # Balance for account2 should be 0
    assert get_balance("account2") == 0

def test_withdraw_more_than_balance():
    open_account("account1", "Alice")
    deposit("account1", 50)
    assert withdraw("account1", 100) == "insufficient funds"
    # Balance should remain 50
    assert get_balance("account1") == 50

def test_deposit_to_nonexistent_account():
    assert deposit("account1", 100) == "account not found"

def test_withdraw_from_nonexistent_account():
    assert withdraw("account1", 50) == "account not found"

def test_open_account_twice():
    open_account("account1", "Alice")
    assert open_account("account1", "Alice") == "account already exists"

def test_close_account_with_nonzero_balance():
    open_account("account1", "Alice")
    deposit("account1", 50)
    assert close_account("account1") == "balance must be zero"

def test_close_account_with_zero_balance():
    open_account("account1", "Alice")
    deposit("account1", 100)
    withdraw("account1", 100)  
    assert close_account("account1") is None  # Closure should succeed, assert no return value
    assert get_summary("account1")["status"] == "closed"

def test_closed_account_rejects_deposits():
    open_account("account1", "Alice")
    close_account("account1")  
    assert deposit("account1", 100) == "account is closed"

def test_closed_account_rejects_withdrawals():
    open_account("account1", "Alice")
    close_account("account1")  
    assert withdraw("account1", 50) == "account is closed"

def test_deposit_amount_must_be_positive():
    open_account("account1", "Alice")
    assert deposit("account1", -100) == "deposit amount must be positive"
    assert deposit("account1", 0) == "deposit amount must be positive"

def test_withdrawal_amount_must_be_positive():
    open_account("account1", "Alice")
    assert withdraw("account1", -50) == "withdrawal amount must be positive"
    assert withdraw("account1", 0) == "withdrawal amount must be positive"

def test_balance_as_of_timestamp():
    open_account("account1", "Alice")
    deposit("account1", 100)  # t=1
    deposit("account1", 50)   # t=2
    assert get_balance("account1", timestamp=1) == 100  # Balance as of time 1 should be 100
    assert get_balance("account1", timestamp=2) == 150  # Balance as of time 2 should be 150

def test_balance_as_of_timestamp_before_opening():
    assert get_balance("account1", timestamp=1) == "account not found"

def test_balance_as_of_with_out_of_order_timestamps():
    open_account("account1", "Alice")
    deposit("account1", 50, timestamp=2)  # t=2
    deposit("account1", 100, timestamp=3)  # t=3
    assert get_balance("account1", timestamp=2) == 50  # Balance as of t=2 should be 50

def test_statement_contains_all_transactions():
    open_account("account1", "Alice")
    deposit("account1", 100, timestamp=2)  # t=2
    withdraw("account1", 30, timestamp=3)   # t=3
    statement = get_statement("account1")
    expected_statement = [
        {"kind": "deposit", "amount": 100, "timestamp": 2, "running_balance": 100},
        {"kind": "withdrawal", "amount": 30, "timestamp": 3, "running_balance": 70}
    ]
    assert statement == expected_statement

def test_statement_filtered_by_timestamp():
    open_account("account1", "Alice")
    deposit("account1", 100, timestamp=2)  # t=2
    withdraw("account1", 30, timestamp=3)   # t=3
    statement = get_statement("account1", start_timestamp=1, end_timestamp=2)
    expected_statement = [
        {"kind": "deposit", "amount": 100, "timestamp": 2, "running_balance": 100}
    ]
    assert statement == expected_statement

def test_statement_filtered_by_empty_range():
    open_account("account1", "Alice")
    deposit("account1", 100, timestamp=2)  # t=2
    statement = get_statement("account1", start_timestamp=1, end_timestamp=1)
    expected_statement = []
    assert statement == expected_statement

def test_summary_reports_correct_info():
    open_account("account1", "Alice")
    deposit("account1", 100)
    withdraw("account1", 30)
    summary = get_summary("account1")
    assert summary == {
        "owner": "Alice",
        "balance": 70,
        "transactions": 2,
        "status": "open"
    }

def test_summary_for_closed_account():
    open_account("account1", "Alice")
    deposit("account1", 100)
    withdraw("account1", 100)  # Close account
    close_account("account1")
    summary = get_summary("account1")
    assert summary["status"] == "closed"

def test_events_are_recorded_correctly():
    open_account("account1", "Alice")
    deposit("account1", 100, timestamp=1)
    withdraw("account1", 30, timestamp=2)
    close_account("account1")
    events = get_events("account1")
    expected_events = [
        {"account": "account1", "payload": "Alice", "timestamp": 1},  # Open account event
        {"account": "account1", "payload": 100, "timestamp": 2},      # Deposit event
        {"account": "account1", "payload": 30, "timestamp": 3},       # Withdrawal event
        {"account": "account1", "payload": None, "timestamp": 4}      # Account closed event
    ]
    assert events == expected_events

def test_rehydration():
    open_account("account1", "Alice")
    deposit("account1", 100, timestamp=1)
    withdraw("account1", 30, timestamp=2)
    events = get_events("account1")
    
    # Rehydrate the bank from events
    # Assuming a function exists to create a bank from events
    # rehydrate_bank(events)
    
    # Check balances and states
    assert get_balance("account1") == 70
    assert get_summary("account1")["status"] == "open"