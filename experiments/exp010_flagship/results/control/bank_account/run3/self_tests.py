from solution import BankAccount

def test_initial_balance():
    account = BankAccount()
    assert account.balance == 0  # AC-1.1: A newly opened account has a balance of 0.

def test_deposit_increases_balance():
    account = BankAccount()
    account.deposit(100, "2023-01-01")
    assert account.balance == 100  # AC-1.2: A deposit increases the balance by exactly the deposited amount.

def test_successive_deposits_accumulate():
    account = BankAccount()
    account.deposit(100, "2023-01-01")
    account.deposit(200, "2023-01-02")
    assert account.balance == 300  # AC-1.3: Successive deposits accumulate into the balance.

def test_withdrawal_decreases_balance():
    account = BankAccount()
    account.deposit(200, "2023-01-01")
    account.withdraw(100, "2023-01-02")
    assert account.balance == 100  # AC-2.1: A withdrawal decreases the balance by exactly the withdrawn amount.

def test_withdrawal_to_zero_balance():
    account = BankAccount()
    account.deposit(100, "2023-01-01")
    account.withdraw(100, "2023-01-02")
    assert account.balance == 0  # AC-2.2: Withdrawing exactly the current balance is allowed and leaves the balance at 0.

def test_reject_negative_deposit():
    account = BankAccount()
    result = account.deposit(-50, "2023-01-01")
    assert result == "Amount must be positive"  # AC-3.1: A deposit of zero or a negative amount is rejected.
    assert account.balance == 0  # Balance should remain unchanged.

def test_reject_zero_deposit():
    account = BankAccount()
    result = account.deposit(0, "2023-01-01")
    assert result == "Amount must be positive"  # AC-3.1: A deposit of zero or a negative amount is rejected.
    assert account.balance == 0  # Balance should remain unchanged.

def test_reject_negative_withdrawal():
    account = BankAccount()
    account.deposit(100, "2023-01-01")
    result = account.withdraw(-50, "2023-01-02")
    assert result == "Amount must be positive"  # AC-3.2: A withdrawal of zero or a negative amount is rejected.
    assert account.balance == 100  # Balance should remain unchanged.

def test_reject_zero_withdrawal():
    account = BankAccount()
    account.deposit(100, "2023-01-01")
    result = account.withdraw(0, "2023-01-02")
    assert result == "Amount must be positive"  # AC-3.2: A withdrawal of zero or a negative amount is rejected.
    assert account.balance == 100  # Balance should remain unchanged.

def test_reject_withdrawal_more_than_balance():
    account = BankAccount()
    account.deposit(100, "2023-01-01")
    result = account.withdraw(150, "2023-01-02")
    assert result == "Cannot withdraw more than current balance"  # AC-3.3: Withdrawal greater than current balance is rejected.
    assert account.balance == 100  # Balance should remain unchanged.

def test_reject_withdrawal_from_zero_balance():
    account = BankAccount()
    result = account.withdraw(50, "2023-01-01")
    assert result == "Cannot withdraw more than current balance"  # AC-3.3: Withdrawal from an account holding 0 is rejected.
    assert account.balance == 0  # Balance should remain unchanged.

def test_print_statement_no_transactions():
    account = BankAccount()
    expected_statement = "Date       | Amount  | Balance\n"
    assert account.print_statement() == expected_statement  # AC-4.1: Statement with no transactions.

def test_print_statement_with_transactions():
    account = BankAccount()
    account.deposit(500, "2026-01-15")
    account.withdraw(100, "2026-01-20")
    account.deposit(200, "2026-01-25")
    expected_statement = (
        "Date       | Amount  | Balance\n"
        "2026-01-15 |  500.00 |  500.00\n"
        "2026-01-20 | -100.00 |  400.00\n"
        "2026-01-25 |  200.00 |  600.00\n"
    )
    assert account.print_statement() == expected_statement  # AC-4.5: Canonical worked example.