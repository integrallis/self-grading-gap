from solution import BankAccount

def test_initial_balance_is_zero():
    account = BankAccount()
    assert account.balance == 0  # AC-1.1

def test_deposit_increases_balance():
    account = BankAccount()
    account.deposit(100.00, "2023-01-01")
    assert account.balance == 100.00  # AC-1.2

def test_successive_deposits_accumulate_balance():
    account = BankAccount()
    account.deposit(100.00, "2023-01-01")
    account.deposit(150.00, "2023-01-02")
    assert account.balance == 250.00  # AC-1.3

def test_withdrawal_decreases_balance():
    account = BankAccount()
    account.deposit(200.00, "2023-01-01")
    account.withdraw(50.00, "2023-01-02")
    assert account.balance == 150.00  # AC-2.1

def test_withdrawing_current_balance_is_allowed():
    account = BankAccount()
    account.deposit(100.00, "2023-01-01")
    account.withdraw(100.00, "2023-01-02")
    assert account.balance == 0  # AC-2.2

def test_reject_negative_deposit():
    account = BankAccount()
    account.deposit(100.00, "2023-01-01")
    result = account.deposit(-50.00, "2023-01-02")
    assert account.balance == 100.00  # AC-3.4
    assert account.statement() == "Date       | Amount  | Balance"  # AC-3.4

def test_reject_zero_deposit():
    account = BankAccount()
    account.deposit(100.00, "2023-01-01")
    result = account.deposit(0.00, "2023-01-02")
    assert account.balance == 100.00  # AC-3.4
    assert account.statement() == "Date       | Amount  | Balance"  # AC-3.4

def test_reject_negative_withdrawal():
    account = BankAccount()
    account.deposit(100.00, "2023-01-01")
    result = account.withdraw(-50.00, "2023-01-02")
    assert account.balance == 100.00  # AC-3.4
    assert account.statement() == "Date       | Amount  | Balance"  # AC-3.4

def test_reject_zero_withdrawal():
    account = BankAccount()
    account.deposit(100.00, "2023-01-01")
    result = account.withdraw(0.00, "2023-01-02")
    assert account.balance == 100.00  # AC-3.4
    assert account.statement() == "Date       | Amount  | Balance"  # AC-3.4

def test_reject_withdrawal_greater_than_balance():
    account = BankAccount()
    account.deposit(100.00, "2023-01-01")
    result = account.withdraw(150.00, "2023-01-02")
    assert account.balance == 100.00  # AC-3.4
    assert account.statement() == "Date       | Amount  | Balance"  # AC-3.4

def test_reject_withdrawal_when_balance_is_zero():
    account = BankAccount()
    result = account.withdraw(50.00, "2023-01-01")
    assert account.balance == 0  # AC-3.4
    assert account.statement() == "Date       | Amount  | Balance"  # AC-3.4

def test_statement_with_no_transactions():
    account = BankAccount()
    statement = account.statement()
    expected = "Date       | Amount  | Balance"
    assert statement == expected  # AC-4.1

def test_statement_with_transactions():
    account = BankAccount()
    account.deposit(500.00, "2026-01-15")
    account.withdraw(100.00, "2026-01-20")
    account.deposit(200.00, "2026-01-25")
    statement = account.statement()
    expected = (
        "Date       | Amount  | Balance\n"
        "2026-01-15 |  500.00 |  500.00\n"
        "2026-01-20 | -100.00 |  400.00\n"
        "2026-01-25 |  200.00 |  600.00"
    )
    assert statement == expected  # AC-4.5

def test_statement_ordering():
    account = BankAccount()
    account.deposit(300.00, "2026-01-02")
    account.deposit(100.00, "2026-01-01")
    account.withdraw(50.00, "2026-01-03")
    statement = account.statement()
    expected = (
        "Date       | Amount  | Balance\n"
        "2026-01-01 |  100.00 |  100.00\n"
        "2026-01-02 |  300.00 |  400.00\n"
        "2026-01-03 |  -50.00 |  350.00"
    )
    assert statement == expected  # Checking chronological order