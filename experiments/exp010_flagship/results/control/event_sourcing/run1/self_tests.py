from solution import open_account, deposit, withdraw, close_account, get_balance, get_statement, get_summary

def test_open_account():
    # Opening an account should succeed
    result = open_account("account1", "Alice")
    assert result == "Account opened"
    
    # Opening the same account again should fail with "account already exists"
    result = open_account("account1", "Alice")
    assert result == "account already exists"

def test_deposit():
    open_account("account1", "Alice")
    
    # Deposit 100 should succeed
    result = deposit("account1", 100)
    assert result == "Deposit successful"
    
    # Balance should now be 100
    assert get_balance("account1") == 100  # 0 + 100
    
    # Deposit 50 should succeed
    result = deposit("account1", 50)
    assert result == "Deposit successful"
    
    # Balance should now be 150
    assert get_balance("account1") == 150  # 100 + 50
    
    # Deposit 0 should fail with "deposit amount must be positive"
    result = deposit("account1", 0)
    assert result == "deposit amount must be positive"
    
    # Deposit -50 should fail with "deposit amount must be positive"
    result = deposit("account1", -50)
    assert result == "deposit amount must be positive"

def test_withdraw():
    open_account("account1", "Alice")
    deposit("account1", 100)  # Balance is now 100
    
    # Withdraw 30 should succeed
    result = withdraw("account1", 30)
    assert result == "Withdrawal successful"
    
    # Balance should now be 70
    assert get_balance("account1") == 70  # 100 - 30
    
    # Withdraw the entire remaining balance (70)
    result = withdraw("account1", 70)
    assert result == "Withdrawal successful"
    
    # Balance should now be 0
    assert get_balance("account1") == 0  # 70 - 70
    
    # Withdraw more than the balance should fail with "insufficient funds"
    result = withdraw("account1", 50)
    assert result == "insufficient funds"
    
    # Withdraw 0 should fail with "withdrawal amount must be positive"
    result = withdraw("account1", 0)
    assert result == "withdrawal amount must be positive"
    
    # Withdraw -10 should fail with "withdrawal amount must be positive"
    result = withdraw("account1", -10)
    assert result == "withdrawal amount must be positive"

def test_close_account():
    open_account("account1", "Alice")
    deposit("account1", 100)  # Balance is now 100
    
    # Closing account with nonzero balance should fail with "balance must be zero"
    result = close_account("account1")
    assert result == "balance must be zero"
    
    # Withdraw all to make balance zero
    withdraw("account1", 100)
    
    # Now closing the account should succeed
    result = close_account("account1")
    assert result == "Account closed"
    
    # Closing again should fail with "account not found"
    result = close_account("account1")
    assert result == "account not found"

def test_get_balance():
    open_account("account1", "Alice")
    deposit("account1", 100)  # Balance is now 100
    
    # Balance should reflect the current state
    assert get_balance("account1") == 100
    
    # Checking balance of a non-existent account should fail with "account not found"
    result = get_balance("account2")
    assert result == "account not found"

def test_get_statement():
    open_account("account1", "Alice")
    deposit("account1", 100)  # Balance is now 100
    withdraw("account1", 30)   # Balance is now 70
    
    # Statement should reflect the transaction history
    statement = get_statement("account1")
    expected_statement = [
        {"type": "deposit", "amount": 100, "timestamp": "some_timestamp_1", "balance": 100},
        {"type": "withdrawal", "amount": 30, "timestamp": "some_timestamp_2", "balance": 70},
    ]
    assert statement == expected_statement
    
    # Getting statement for a non-existent account should fail with "account not found"
    result = get_statement("account2")
    assert result == "account not found"

def test_get_summary():
    open_account("account1", "Alice")
    deposit("account1", 100)  # Balance is now 100
    withdraw("account1", 30)   # Balance is now 70
    
    # Summary should reflect the current account state
    summary = get_summary("account1")
    expected_summary = {
        "owner": "Alice",
        "balance": 70,
        "transactions": 2,
        "status": "open"
    }
    assert summary == expected_summary
    
    # Getting summary for a closed account should fail with "account not found"
    close_account("account1")
    result = get_summary("account1")
    assert result == "account not found"