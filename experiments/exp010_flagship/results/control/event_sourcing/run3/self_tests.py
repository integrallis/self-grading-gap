from solution import open_account, deposit, withdraw, close_account, get_balance, get_statement, get_summary

def test_open_account():
    # Opening an account named "Alice"
    assert open_account("Alice", "account_1") == "account_1 opened"
    # Attempting to open the same account again
    assert open_account("Alice", "account_1") == "account already exists"

def test_deposit():
    # Opening an account and depositing 100
    open_account("Alice", "account_1")
    assert deposit("account_1", 100) == "deposited 100 to account_1"
    # Checking balance after deposit
    assert get_balance("account_1") == 100  # 100

    # Depositing 50 more
    assert deposit("account_1", 50) == "deposited 50 to account_1"
    assert get_balance("account_1") == 150  # 100 + 50

    # Attempting to deposit 0 should fail
    assert deposit("account_1", 0) == "deposit amount must be positive"
    # Attempting to deposit a negative amount should fail
    assert deposit("account_1", -50) == "deposit amount must be positive"

def test_withdraw():
    # Opening an account and performing a withdrawal
    open_account("Alice", "account_1")
    deposit("account_1", 100)
    assert withdraw("account_1", 30) == "withdrew 30 from account_1"
    assert get_balance("account_1") == 70  # 100 - 30

    # Withdrawing the entire balance
    assert withdraw("account_1", 70) == "withdrew 70 from account_1"
    assert get_balance("account_1") == 0  # 0

    # Attempting to withdraw more than the balance
    assert withdraw("account_1", 10) == "insufficient funds"
    assert get_balance("account_1") == 0  # Balance unchanged

    # Attempting to withdraw 0 should fail
    assert withdraw("account_1", 0) == "withdrawal amount must be positive"
    # Attempting to withdraw a negative amount should fail
    assert withdraw("account_1", -10) == "withdrawal amount must be positive"

def test_close_account():
    # Opening an account and closing it
    open_account("Alice", "account_1")
    deposit("account_1", 100)
    assert close_account("account_1") == "balance must be zero"  # can't close non-zero balance

    # Closing the account after withdrawing all funds
    withdraw("account_1", 100)
    assert close_account("account_1") == "account_1 closed"

    # Attempting to deposit after closing
    assert deposit("account_1", 50) == "account is closed"
    # Attempting to withdraw after closing
    assert withdraw("account_1", 30) == "account is closed"

def test_event_stream():
    # Opening and depositing to an account
    open_account("Alice", "account_1")
    deposit("account_1", 100)

    # Check if the events were recorded correctly
    # The exact implementation of event checking is assumed to be part of the solution
    # This would need to be verified with an event retrieval function or similar

    # Here we just check that an event was recorded
    # This is a placeholder; the actual implementation details depend on the event logging structure
    # assert get_events("account_1") == expected_events

def test_balances_as_of():
    # Opening an account and performing operations
    open_account("Alice", "account_1")
    deposit("account_1", 100)
    deposit("account_1", 50)
    withdraw("account_1", 30)

    # Check balance as of different timestamps
    assert get_balance("account_1", 1) == "account not found"  # Before account opened
    assert get_balance("account_1", 2) == 100  # After 100 deposit
    assert get_balance("account_1", 3) == 150  # After 50 deposit
    assert get_balance("account_1", 4) == 120  # After withdrawal of 30

def test_statement_and_summary():
    # Opening account and performing transactions
    open_account("Alice", "account_1")
    deposit("account_1", 100)
    withdraw("account_1", 30)
    
    # Getting the statement
    statement = get_statement("account_1")
    assert statement == [
        {"type": "deposit", "amount": 100, "timestamp": 1, "running_balance": 100},
        {"type": "withdrawal", "amount": 30, "timestamp": 2, "running_balance": 70}
    ]

    # Getting the summary
    summary = get_summary("account_1")
    assert summary == {
        "owner": "Alice",
        "balance": 70,
        "transactions": 2,
        "status": "open"
    }