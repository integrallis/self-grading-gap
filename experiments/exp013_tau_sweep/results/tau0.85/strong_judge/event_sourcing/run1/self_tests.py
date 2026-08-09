from solution import open_account, deposit, withdraw, close_account, get_balance, get_statement, get_summary, get_balance_as_of

def test_open_account():
    # Opening an account should succeed
    assert open_account("account1", "Alice") is None
    # Opening again should fail
    assert open_account("account1", "Alice") == "account already exists"

def test_deposit():
    open_account("account1", "Alice")
    deposit("account1", 100)  # timestamp 1
    assert get_balance("account1") == 100  # Balance after deposit should be 100
    deposit("account1", 50)    # timestamp 2
    assert get_balance("account1") == 150  # Balance after second deposit should be 150

def test_withdraw():
    open_account("account1", "Alice")
    deposit("account1", 100)  # timestamp 1
    withdraw("account1", 30)   # timestamp 2
    assert get_balance("account1") == 70  # Balance after withdrawal should be 70
    withdraw("account1", 70)    # timestamp 3
    assert get_balance("account1") == 0   # Balance after withdrawing entire balance should be 0

def test_valid_movements():
    open_account("account1", "Alice")
    deposit("account1", 1)  # timestamp 1
    assert get_balance("account1") == 1  # Balance should be 1 after deposit
    withdraw("account1", 1)  # timestamp 2
    assert get_balance("account1") == 0  # Balance should be 0 after withdrawal

def test_independent_accounts():
    open_account("account1", "Alice")
    open_account("account2", "Bob")
    deposit("account1", 100)  # timestamp 1
    assert get_balance("account1") == 100  # Balance for account1 should be 100
    assert get_balance("account2") == 0     # Balance for account2 should be 0

def test_insufficient_funds():
    open_account("account1", "Alice")
    deposit("account1", 50)  # timestamp 1
    assert withdraw("account1", 100) == "insufficient funds"  # Cannot withdraw more than balance
    assert get_balance("account1") == 50  # Balance should remain unchanged

def test_account_not_found():
    assert withdraw("account_nonexistent", 50) == "account not found"  # Account not found
    assert deposit("account_nonexistent", 50) == "account not found"   # Account not found
    assert get_balance("account_nonexistent") == "account not found"   # Account not found

def test_close_account_with_nonzero_balance():
    open_account("account1", "Alice")
    deposit("account1", 100)  # timestamp 1
    assert close_account("account1") == "balance must be zero"  # Cannot close with nonzero balance

def test_close_account_with_zero_balance():
    open_account("account1", "Alice")
    deposit("account1", 100)  # timestamp 1
    withdraw("account1", 100)  # timestamp 2
    assert close_account("account1") is None  # Successful close
    assert get_summary("account1") == {
        "owner": "Alice",
        "balance": 0,
        "transactions": 2,
        "status": "closed"
    }

def test_closed_account_transactions():
    open_account("account1", "Alice")
    deposit("account1", 100)  # timestamp 1
    withdraw("account1", 100)  # timestamp 2
    assert close_account("account1") is None  # Successful close
    assert deposit("account1", 50) == "account is closed"  # Cannot deposit to closed account
    assert withdraw("account1", 50) == "account is closed"  # Cannot withdraw from closed account

def test_deposit_negative_or_zero():
    open_account("account1", "Alice")
    assert deposit("account1", 0) == "deposit amount must be positive"  # Cannot deposit zero
    assert deposit("account1", -50) == "deposit amount must be positive"  # Cannot deposit negative

def test_withdraw_negative_or_zero():
    open_account("account1", "Alice")
    assert withdraw("account1", 0) == "withdrawal amount must be positive"  # Cannot withdraw zero
    assert withdraw("account1", -50) == "withdrawal amount must be positive"  # Cannot withdraw negative

def test_event_logging_on_commands():
    open_account("account1", "Alice")  # timestamp 1
    deposit("account1", 100)  # timestamp 2
    withdraw("account1", 50)  # timestamp 3
    assert get_statement("account1") == [
        {"kind": "deposit", "amount": 100, "timestamp": 2, "running_balance": 100},  # first deposit
        {"kind": "withdrawal", "amount": 50, "timestamp": 3, "running_balance": 50}  # withdrawal
    ]

def test_balance_as_of_timestamp():
    open_account("account1", "Alice")  # timestamp 1
    deposit("account1", 100)  # timestamp 2
    deposit("account1", 50)   # timestamp 3
    assert get_balance_as_of("account1", 2) == 100  # Balance as of timestamp 2 should be 100
    assert get_balance_as_of("account1", 3) == 150  # Balance as of timestamp 3 should be 150

def test_balance_as_of_before_opening():
    assert get_balance_as_of("account1", 1) == "account not found"  # Account not found before opening

def test_balance_as_of_out_of_order_timestamps():
    open_account("account1", "Alice")  # timestamp 1
    deposit("account1", 100)  # timestamp 3
    deposit("account1", 50)   # timestamp 2
    assert get_balance_as_of("account1", 3) == 150  # Balance as of timestamp 3 should be 150
    assert get_balance_as_of("account1", 1) == 0     # Balance as of timestamp 1 should be 0

def test_statement_range_inclusive_bounds():
    open_account("account1", "Alice")  # timestamp 1
    deposit("account1", 100)  # timestamp 2
    withdraw("account1", 50)  # timestamp 3
    assert get_statement("account1", 1, 3) == [
        {"kind": "deposit", "amount": 100, "timestamp": 2, "running_balance": 100},  # deposit at timestamp 2
        {"kind": "withdrawal", "amount": 50, "timestamp": 3, "running_balance": 50}   # withdrawal at timestamp 3
    ]

def test_statement_range_with_no_transactions():
    open_account("account1", "Alice")  # timestamp 1
    assert get_statement("account1", 2, 3) == []  # No transactions in this range should yield empty list

def test_account_summary_after_close():
    open_account("account1", "Alice")
    deposit("account1", 100)  # timestamp 1
    withdraw("account1", 100)  # timestamp 2
    close_account("account1")  # timestamp 3
    assert get_summary("account1") == {
        "owner": "Alice",
        "balance": 0,
        "transactions": 2,
        "status": "closed"
    }

def test_summary_of_open_account():
    open_account("account1", "Alice")
    deposit("account1", 100)  # timestamp 1
    assert get_summary("account1") == {
        "owner": "Alice",
        "balance": 100,
        "transactions": 1,
        "status": "open"
    }