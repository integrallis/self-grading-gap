from solution import BankAccount

def test_initial_balance_is_zero():
    account = BankAccount()
    assert account.balance == 0  # AC-1.1

def test_deposit_increases_balance():
    account = BankAccount()
    account.deposit(100.00, "2023-01-01")
    assert account.balance == 100.00  # AC-1.2

def test_successive_deposits_accumulate():
    account = BankAccount()
    account.deposit(100.00, "2023-01-01")
    account.deposit(200.00, "2023-01-02")
    assert account.balance == 300.00  # AC-1.3

def test_withdrawal_decreases_balance():
    account = BankAccount()
    account.deposit(200.00, "2023-01-01")
    account.withdraw(100.00, "2023-01-02")
    assert account.balance == 100.00  # AC-2.1

def test_withdrawal_leaves_balance_zero():
    account = BankAccount()
    account.deposit(100.00, "2023-01-01")
    account.withdraw(100.00, "2023-01-02")
    assert account.balance == 0  # AC-2.2

def test_reject_negative_deposit():
    account = BankAccount()
    with pytest.raises(ValueError, match="Amount must be positive"):
        account.deposit(-50.00, "2023-01-01")  # AC-3.1
    assert account.balance == 0  # balance unchanged

def test_reject_zero_deposit():
    account = BankAccount()
    with pytest.raises(ValueError, match="Amount must be positive"):
        account.deposit(0, "2023-01-01")  # AC-3.1
    assert account.balance == 0  # balance unchanged

def test_reject_negative_withdrawal():
    account = BankAccount()
    with pytest.raises(ValueError, match="Amount must be positive"):
        account.withdraw(-50.00, "2023-01-01")  # AC-3.2
    assert account.balance == 0  # balance unchanged

def test_reject_zero_withdrawal():
    account = BankAccount()
    with pytest.raises(ValueError, match="Amount must be positive"):
        account.withdraw(0, "2023-01-01")  # AC-3.2
    assert account.balance == 0  # balance unchanged

def test_reject_withdrawal_greater_than_balance():
    account = BankAccount()
    account.deposit(100.00, "2023-01-01")
    with pytest.raises(ValueError, match="Cannot withdraw more than current balance"):
        account.withdraw(150.00, "2023-01-02")  # AC-3.3
    assert account.balance == 100.00  # balance unchanged

def test_statement_with_no_transactions():
    account = BankAccount()
    expected_output = "Date       | Amount  | Balance\n"
    assert account.statement() == expected_output  # AC-4.1

def test_statement_with_multiple_transactions():
    account = BankAccount()
    account.deposit(500.00, "2026-01-15")
    account.withdraw(100.00, "2026-01-20")
    account.deposit(200.00, "2026-01-25")
    expected_output = (
        "Date       | Amount  | Balance\n"
        "2026-01-15 |  500.00 |  500.00\n"
        "2026-01-20 | -100.00 |  400.00\n"
        "2026-01-25 |  200.00 |  600.00\n"
    )
    assert account.statement() == expected_output  # AC-4.5