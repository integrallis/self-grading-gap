from solution import open_account, deposit, withdraw, close_account, get_balance, get_statement, get_summary

def test_open_account():
    open_account("account1", "John Doe")
    # Account "account1" is now open

def test_balance_after_opening_account():
    open_account("account1", "John Doe")
    assert get_balance("account1") == 0
    # Balance after opening is 0

def test_deposit():
    open_account("account1", "John Doe")
    deposit("account1", 100)
    assert get_balance("account1") == 100
    # Balance after depositing 100 is 100

def test_multiple_deposits():
    open_account("account1", "John Doe")
    deposit("account1", 100)
    deposit("account1", 50)
    assert get_balance("account1") == 150
    # Balance after depositing 100 and then 50 is 150

def test_withdraw():
    open_account("account1", "John Doe")
    deposit("account1", 100)
    withdraw("account1", 30)
    assert get_balance("account1") == 70
    # Balance after depositing 100 and withdrawing 30 is 70

def test_withdraw_full_balance():
    open_account("account1", "John Doe")
    deposit("account1", 100)
    withdraw("account1", 100)
    assert get_balance("account1") == 0
    # Balance after withdrawing the full balance of 100 is 0

def test_withdraw_insufficient_funds():
    open_account("account1", "John Doe")
    deposit("account1", 50)
    result = withdraw("account1", 100)
    assert result == "insufficient funds"
    assert get_balance("account1") == 50
    # Attempting to withdraw 100 when balance is 50 fails 

def test_deposit_negative_amount():
    open_account("account1", "John Doe")
    result = deposit("account1", -50)
    assert result == "deposit amount must be positive"
    assert get_balance("account1") == 0
    # Depositing -50 is rejected

def test_withdraw_negative_amount():
    open_account("account1", "John Doe")
    result = withdraw("account1", -50)
    assert result == "withdrawal amount must be positive"
    assert get_balance("account1") == 0
    # Withdrawing -50 is rejected

def test_deposit_zero_amount():
    open_account("account1", "John Doe")
    result = deposit("account1", 0)
    assert result == "deposit amount must be positive"
    assert get_balance("account1") == 0
    # Depositing 0 is rejected

def test_withdraw_zero_amount():
    open_account("account1", "John Doe")
    result = withdraw("account1", 0)
    assert result == "withdrawal amount must be positive"
    assert get_balance("account1") == 0
    # Withdrawing 0 is rejected

def test_close_account_with_balance():
    open_account("account1", "John Doe")
    deposit("account1", 50)
    result = close_account("account1")
    assert result == "balance must be zero"
    # Cannot close account with non-zero balance

def test_close_account_with_zero_balance():
    open_account("account1", "John Doe")
    close_account("account1")
    # Account can be closed when balance is 0

def test_closed_account_operations():
    open_account("account1", "John Doe")
    close_account("account1")
    result = deposit("account1", 50)
    assert result == "account is closed"
    result = withdraw("account1", 30)
    assert result == "account is closed"
    # Closed account rejects deposits and withdrawals

def test_open_account_twice():
    open_account("account1", "John Doe")
    result = open_account("account1", "John Doe")
    assert result == "account already exists"
    # Opening the same account again fails

def test_balance_query_before_opening():
    result = get_balance("account1")
    assert result == "account not found"
    # Querying balance of a non-existing account fails

def test_statement_empty():
    open_account("account1", "John Doe")
    statement = get_statement("account1")
    assert statement == []
    # No transactions yield an empty statement

def test_statement_single_transaction():
    open_account("account1", "John Doe")
    deposit("account1", 100)  # assumed at timestamp 1
    statement = get_statement("account1")
    assert statement == [("deposit", 100, 1, 100)]
    # Single deposit transaction appears in statement

def test_statement_multiple_transactions():
    open_account("account1", "John Doe")
    deposit("account1", 100)  # assumed at timestamp 1
    withdraw("account1", 30)   # assumed at timestamp 2
    statement = get_statement("account1")
    assert statement == [("deposit", 100, 1, 100), ("withdrawal", 30, 2, 70)]
    # Multiple transactions appear in statement with running balance

def test_summary():
    open_account("account1", "John Doe")
    deposit("account1", 100)  # assumed at timestamp 1
    withdraw("account1", 30)   # assumed at timestamp 2
    summary = get_summary("account1")
    assert summary['owner'] == "John Doe"
    assert summary['balance'] == 70
    assert summary['transactions'] == 2
    assert summary['status'] == "open"
    # Summary reflects correct owner, balance, transaction count, and status

def test_summary_closed_account():
    open_account("account1", "John Doe")
    close_account("account1")
    summary = get_summary("account1")
    assert summary['owner'] == "John Doe"
    assert summary['balance'] == 0
    assert summary['transactions'] == 0
    assert summary['status'] == "closed"
    # Summary of closed account reflects correct data

def test_event_stream_on_open_account():
    open_account("account1", "John Doe")
    # Verify that exactly one event is recorded with the account identifier, command payload, and timestamp.

def test_event_stream_on_deposit():
    open_account("account1", "John Doe")
    deposit("account1", 100)  # assumed at timestamp 1
    # Verify that exactly one event is recorded for the deposit with the account identifier and timestamp.

def test_event_stream_on_withdraw():
    open_account("account1", "John Doe")
    deposit("account1", 100)  # assumed at timestamp 1
    withdraw("account1", 30)   # assumed at timestamp 2
    # Verify that exactly one event is recorded for the withdrawal with the account identifier and timestamp.

def test_event_stream_on_close_account():
    open_account("account1", "John Doe")
    close_account("account1")  # assumed at timestamp 1
    # Verify that exactly one event is recorded for the account closure with the account identifier and timestamp.

def test_rehydrate_from_event_stream():
    open_account("account1", "John Doe")
    deposit("account1", 100)  # assumed at timestamp 1
    withdraw("account1", 30)   # assumed at timestamp 2
    close_account("account1")   # assumed at timestamp 3
    # Simulate rehydration from events and assert state matches expected

def test_balance_as_of_timestamp():
    open_account("account1", "John Doe")  # assumed at timestamp 1
    deposit("account1", 100)  # assumed at timestamp 2
    deposit("account1", 50)   # assumed at timestamp 3
    assert get_balance("account1", timestamp=2) == 100
    assert get_balance("account1", timestamp=3) == 150
    # Balance as of timestamp reflects events up to that time

def test_balance_as_of_before_opening():
    result = get_balance("account1", timestamp=1)
    assert result == "account not found"
    # Balance query before account opening gives "account not found"

def test_statement_range_filter():
    open_account("account1", "John Doe")  # assumed at timestamp 1
    deposit("account1", 100)  # assumed at timestamp 2
    withdraw("account1", 30)   # assumed at timestamp 3
    statement = get_statement("account1", start_time=2, end_time=3)
    assert statement == [("deposit", 100, 2, 100), ("withdrawal", 30, 3, 70)]
    # Statement filtered by timestamp range matches expected transactions

def test_statement_empty_range():
    open_account("account1", "John Doe")  # assumed at timestamp 1
    statement = get_statement("account1", start_time=2, end_time=2)
    assert statement == []
    # No transactions in range yields an empty statement