from solution import open_account, deposit, withdraw, close_account, get_balance, get_statement, get_summary

def test_open_account():
    # Open an account with owner name "Alice"
    open_account("account1", "Alice")  # First opening, should succeed
    # Opening the same account again should be rejected
    assert open_account("account1", "Alice") == "account already exists"

def test_deposit():
    open_account("account1", "Alice")  # Precondition: account must exist
    deposit("account1", 100)  # Deposit 100
    assert get_balance("account1") == 100  # Expected balance is 100

    deposit("account1", 50)  # Deposit 50
    assert get_balance("account1") == 150  # Expected balance is 150

    # Test deposit with zero and negative amounts
    assert deposit("account1", 0) == "deposit amount must be positive"
    assert deposit("account1", -50) == "deposit amount must be positive"

    # Test deposit of exactly 1
    deposit("account1", 1)  # Deposit 1
    assert get_balance("account1") == 151  # Expected balance is 151

def test_withdraw():
    open_account("account1", "Alice")  # Precondition: account must exist
    deposit("account1", 100)  # Precondition: deposit to ensure balance

    withdraw("account1", 30)  # Withdraw 30
    assert get_balance("account1") == 70  # Expected balance is 70

    withdraw("account1", 70)  # Withdraw entire balance
    assert get_balance("account1") == 0  # Balance should be 0

    assert withdraw("account1", 10) == "insufficient funds"  # Cannot withdraw more than balance
    assert get_balance("account1") == 0  # Balance remains 0

    # Test withdrawal with zero and negative amounts
    assert withdraw("account1", 0) == "withdrawal amount must be positive"
    assert withdraw("account1", -10) == "withdrawal amount must be positive"

    # Test withdrawal of exactly 1
    open_account("account2", "Bob")  # Precondition: a new account must exist for this test
    deposit("account2", 1)  # Deposit 1 into account2
    assert withdraw("account2", 1) == None  # Withdrawal should succeed
    assert get_balance("account2") == 0  # Balance should be 0

def test_close_account():
    open_account("account1", "Alice")  # Precondition: account must exist
    deposit("account1", 100)  # Precondition: deposit to ensure balance

    assert close_account("account1") == "balance must be zero"  # Cannot close non-zero balance

    withdraw("account1", 100)  # Withdraw entire balance
    close_account("account1")  # Close account

    # Test zero-balance close and verify account status
    assert get_summary("account1")["status"] == "closed"

def test_account_independence():
    open_account("account1", "Alice")  # Precondition: account must exist
    open_account("account2", "Bob")  # Precondition: second account must exist

    deposit("account1", 100)  # Deposit into account1
    assert get_balance("account1") == 100  # Balance for account1 should be 100
    assert get_balance("account2") == 0  # Balance for account2 should remain 0

def test_never_opened_account():
    assert deposit("account3", 100) == "account not found"  # Deposit on never-opened account
    assert withdraw("account3", 50) == "account not found"  # Withdraw on never-opened account

def test_closed_account_operations():
    open_account("account1", "Alice")  # Precondition: account must exist
    deposit("account1", 100)  # Precondition: deposit to ensure balance
    withdraw("account1", 100)  # Withdraw entire balance
    close_account("account1")  # Close account

    assert deposit("account1", 50) == "account is closed"  # Deposit on closed account
    assert withdraw("account1", 10) == "account is closed"  # Withdraw on closed account

def test_balance_queries():
    open_account("account1", "Alice")  # Precondition: account must exist
    deposit("account1", 100)  # Precondition: deposit to ensure balance
    deposit("account1", 50)  # Balance now 150

    assert get_balance("account1") == 150  # Expected balance is 150

    # Test querying before account was opened
    assert get_balance("account1", timestamp=0) == "account not found"  # Before account exists

def test_statement_and_summary():
    open_account("account1", "Alice")  # Precondition: account must exist
    deposit("account1", 100)  # Precondition: deposit to ensure balance
    withdraw("account1", 30)  # Balance now 70

    statement = get_statement("account1")
    expected_statement = [
        {"kind": "deposit", "amount": 100, "timestamp": statement[0]["timestamp"], "running_balance": 100},
        {"kind": "withdrawal", "amount": 30, "timestamp": statement[1]["timestamp"], "running_balance": 70}
    ]
    assert statement == expected_statement  # Check transaction history

    summary = get_summary("account1")
    expected_summary = {
        "owner": "Alice",
        "balance": 70,
        "transactions": 2,
        "status": "open"
    }
    assert summary == expected_summary  # Check account summary

    withdraw("account1", 70)  # Withdraw entire balance
    close_account("account1")  # Close account
    # Statement should still be available after closure
    statement_after_close = get_statement("account1")
    expected_statement_after_close = [
        {"kind": "deposit", "amount": 100, "timestamp": statement[0]["timestamp"], "running_balance": 100},
        {"kind": "withdrawal", "amount": 30, "timestamp": statement[1]["timestamp"], "running_balance": 70},
        {"kind": "withdrawal", "amount": 70, "timestamp": statement_after_close[2]["timestamp"], "running_balance": 0}
    ]
    assert statement_after_close == expected_statement_after_close  # Check transaction history remains intact

def test_inclusive_range_statement():
    open_account("account1", "Alice")  # Precondition: account must exist
    deposit("account1", 100)  # Precondition: deposit to ensure balance
    deposit("account1", 50)  # Balance now 150
    withdraw("account1", 30)  # Balance now 120

    statement = get_statement("account1")
    # Test inclusive range for the statement
    range_statement = get_statement("account1", start=0, end=statement[2]["timestamp"])
    expected_range_statement = [
        {"kind": "deposit", "amount": 100, "timestamp": statement[0]["timestamp"], "running_balance": 100},
        {"kind": "deposit", "amount": 50, "timestamp": statement[1]["timestamp"], "running_balance": 150},
        {"kind": "withdrawal", "amount": 30, "timestamp": statement[2]["timestamp"], "running_balance": 120}
    ]
    assert range_statement == expected_range_statement  # Check inclusive range statement

def test_empty_range_statement():
    open_account("account1", "Alice")  # Precondition: account must exist
    # Test for an empty transaction range
    empty_range_statement = get_statement("account1", start="2020-01-01", end="2020-01-02")
    assert empty_range_statement == []  # Expect empty list for no transactions

def test_unsupported_event_order():
    open_account("account1", "Alice")  # Precondition: account must exist
    deposit("account1", 100)  # Precondition: deposit to ensure balance

    # Simulating a delay in the timestamp order
    withdraw("account1", 30)  # Should still reflect the correct balance
    deposit("account1", 50)  # Should reflect the correct balance
    assert get_balance("account1", timestamp=withdraw["timestamp"]) == 70  # Balance should be correct as of withdrawal timestamp