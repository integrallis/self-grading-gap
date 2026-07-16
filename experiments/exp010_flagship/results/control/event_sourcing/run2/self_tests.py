from solution import open_account, deposit, withdraw, close_account, get_balance, get_statement, get_summary, get_events

def test_open_account():
    result = open_account("account1", "Alice")
    assert result == "Account opened successfully"  # Opening account should succeed

def test_open_account_already_exists():
    open_account("account1", "Alice")  # First open should succeed
    result = open_account("account1", "Bob")
    assert result == "account already exists"  # Opening an existing account should fail

def test_deposit_to_open_account():
    open_account("account1", "Alice")
    result = deposit("account1", 100)
    assert result == "Deposit successful"  # Deposit should succeed
    assert get_balance("account1") == 100  # Balance should be 100 after deposit

def test_deposit_to_closed_account():
    open_account("account1", "Alice")
    deposit("account1", 100)
    close_account("account1")
    result = deposit("account1", 50)
    assert result == "account is closed"  # Deposit to closed account should fail

def test_withdraw_from_open_account():
    open_account("account1", "Alice")
    deposit("account1", 100)
    result = withdraw("account1", 30)
    assert result == "Withdrawal successful"  # Withdrawal should succeed
    assert get_balance("account1") == 70  # Balance should be 70 after withdrawal

def test_withdraw_more_than_balance():
    open_account("account1", "Alice")
    deposit("account1", 100)
    result = withdraw("account1", 150)
    assert result == "insufficient funds"  # Overdraft should fail
    assert get_balance("account1") == 100  # Balance should remain unchanged

def test_withdraw_zero_or_negative_amount():
    open_account("account1", "Alice")
    deposit("account1", 100)
    result = withdraw("account1", 0)
    assert result == "withdrawal amount must be positive"  # Invalid withdrawal should fail
    result = withdraw("account1", -10)
    assert result == "withdrawal amount must be positive"  # Invalid withdrawal should fail

def test_deposit_zero_or_negative_amount():
    open_account("account1", "Alice")
    result = deposit("account1", 0)
    assert result == "deposit amount must be positive"  # Invalid deposit should fail
    result = deposit("account1", -10)
    assert result == "deposit amount must be positive"  # Invalid deposit should fail

def test_withdraw_entire_balance():
    open_account("account1", "Alice")
    deposit("account1", 100)
    result = withdraw("account1", 100)
    assert result == "Withdrawal successful"  # Withdrawal should succeed
    assert get_balance("account1") == 0  # Balance should be 0 after withdrawal

def test_close_account_with_nonzero_balance():
    open_account("account1", "Alice")
    deposit("account1", 100)
    result = close_account("account1")
    assert result == "balance must be zero"  # Closing should fail with nonzero balance

def test_close_account_with_zero_balance():
    open_account("account1", "Alice")
    deposit("account1", 100)
    withdraw("account1", 100)
    result = close_account("account1")
    assert result == "Account closed successfully"  # Closing should succeed
    assert get_balance("account1") == 0  # Balance should still be 0

def test_get_balance_before_account_opened():
    result = get_balance("account1")
    assert result == "account not found"  # Querying non-existent account should fail

def test_get_balance_as_of_timestamp():
    open_account("account1", "Alice")
    deposit("account1", 100)  # Time 1
    deposit("account1", 50)   # Time 2
    assert get_balance("account1", 1) == 100  # Balance at time 1 should be 100
    assert get_balance("account1", 2) == 150  # Balance at time 2 should be 150

def test_get_balance_as_of_timestamp_before_opening():
    result = get_balance("account1", 0)
    assert result == "account not found"  # Querying before account opened should fail

def test_get_statement():
    open_account("account1", "Alice")
    deposit("account1", 100)  # Time 1
    withdraw("account1", 30)   # Time 2
    statement = get_statement("account1")
    expected_statement = [
        {"type": "deposit", "amount": 100, "timestamp": 1, "balance": 100},
        {"type": "withdrawal", "amount": 30, "timestamp": 2, "balance": 70}
    ]
    assert statement == expected_statement  # Statement should match the expected transactions

def test_get_summary():
    open_account("account1", "Alice")
    deposit("account1", 100)
    withdraw("account1", 30)
    summary = get_summary("account1")
    expected_summary = {
        "owner": "Alice",
        "balance": 70,
        "number_of_transactions": 2,
        "status": "open"
    }
    assert summary == expected_summary  # Summary should match the expected values

def test_record_events_on_open_account():
    open_account("account1", "Alice")  # Time 1
    assert get_events("account1") == [
        {"account": "account1", "action": "open", "payload": "Alice", "timestamp": 1}
    ]  # Check event on opening account

def test_record_events_on_deposit():
    open_account("account1", "Alice")  # Time 1
    deposit("account1", 100)  # Time 2
    assert get_events("account1") == [
        {"account": "account1", "action": "open", "payload": "Alice", "timestamp": 1},
        {"account": "account1", "action": "deposit", "payload": 100, "timestamp": 2}
    ]  # Check events recorded correctly

def test_record_events_on_close_account():
    open_account("account1", "Alice")  # Time 1
    deposit("account1", 100)  # Time 2
    close_account("account1")  # Time 3
    assert get_events("account1") == [
        {"account": "account1", "action": "open", "payload": "Alice", "timestamp": 1},
        {"account": "account1", "action": "deposit", "payload": 100, "timestamp": 2},
        {"account": "account1", "action": "close", "timestamp": 3}
    ]  # Check event recorded on closing account

def test_get_balance_as_of_out_of_order_timestamps():
    open_account("account1", "Alice")
    deposit("account1", 100)  # Time 1
    deposit("account1", 50)    # Time 3
    assert get_balance("account1", 2) == 100  # Balance at time 2 should reflect only the first deposit
    assert get_balance("account1", 3) == 150  # Balance at time 3 should reflect both deposits

def test_get_statement_within_range():
    open_account("account1", "Alice")
    deposit("account1", 100)  # Time 1
    withdraw("account1", 30)   # Time 2
    statement = get_statement("account1")  # No range specified, should include all
    expected_statement = [
        {"type": "deposit", "amount": 100, "timestamp": 1, "balance": 100},
        {"type": "withdrawal", "amount": 30, "timestamp": 2, "balance": 70}
    ]
    assert statement == expected_statement  # Statement should match the expected transactions