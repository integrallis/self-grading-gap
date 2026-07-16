import pytest
from solution import BankAccount  # Assuming we will define this in the implementation

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
    account.deposit(50.00, "2023-01-02")
    assert account.balance == 150.00  # AC-1.3

def test_withdrawal_decreases_balance():
    account = BankAccount()
    account.deposit(100.00, "2023-01-01")
    account.withdraw(50.00, "2023-01-02")
    assert account.balance == 50.00  # AC-2.1

def test_withdrawal_of_current_balance_is_allowed():
    account = BankAccount()
    account.deposit(100.00, "2023-01-01")
    account.withdraw(100.00, "2023-01-02")
    assert account.balance == 0  # AC-2.2

def test_reject_zero_or_negative_deposit():
    account = BankAccount()
    initial_balance = account.balance
    with pytest.raises(Exception) as excinfo:
        account.deposit(0, "2023-01-01")
    assert str(excinfo.value) == "Amount must be positive"  # AC-3.1
    assert account.balance == initial_balance  # AC-3.4

    with pytest.raises(Exception) as excinfo:
        account.deposit(-50.00, "2023-01-01")
    assert str(excinfo.value) == "Amount must be positive"  # AC-3.1
    assert account.balance == initial_balance  # AC-3.4

def test_reject_zero_or_negative_withdrawal():
    account = BankAccount()
    initial_balance = account.balance
    with pytest.raises(Exception) as excinfo:
        account.withdraw(0, "2023-01-01")
    assert str(excinfo.value) == "Amount must be positive"  # AC-3.2
    assert account.balance == initial_balance  # AC-3.4

    with pytest.raises(Exception) as excinfo:
        account.withdraw(-50.00, "2023-01-01")
    assert str(excinfo.value) == "Amount must be positive"  # AC-3.2
    assert account.balance == initial_balance  # AC-3.4

def test_reject_withdrawal_greater_than_balance():
    account = BankAccount()
    account.deposit(100.00, "2023-01-01")
    with pytest.raises(Exception) as excinfo:
        account.withdraw(150.00, "2023-01-02")
    assert str(excinfo.value) == "Cannot withdraw more than current balance"  # AC-3.3

def test_reject_withdrawal_from_zero_balance():
    account = BankAccount()
    with pytest.raises(Exception) as excinfo:
        account.withdraw(50.00, "2023-01-01")  # Invalid withdraw from zero balance
    assert str(excinfo.value) == "Cannot withdraw more than current balance"  # AC-3.3

def test_rejected_operations_do_not_change_state():
    account = BankAccount()
    account.deposit(100.00, "2023-01-01")
    initial_balance = account.balance
    
    with pytest.raises(Exception):
        account.deposit(-50.00, "2023-01-02")  # Invalid deposit
    assert account.balance == initial_balance  # AC-3.4

    with pytest.raises(Exception):
        account.withdraw(150.00, "2023-01-03")  # Invalid withdraw
    assert account.balance == initial_balance  # AC-3.4

def test_statement_with_no_transactions(capfd):
    account = BankAccount()
    account.statement()  # Assuming this prints directly
    captured = capfd.readouterr()
    expected_statement = "Date       | Amount  | Balance\n"
    assert captured.out == expected_statement  # AC-4.1

def test_statement_with_transactions(capfd):
    account = BankAccount()
    account.deposit(500.00, "2026-01-15")
    account.withdraw(100.00, "2026-01-20")
    account.deposit(200.00, "2026-01-25")
    
    account.statement()  # Assuming this prints directly
    captured = capfd.readouterr()
    expected_statement = (
        "Date       | Amount  | Balance\n"
        "2026-01-15 |  500.00 |  500.00\n"
        "2026-01-20 | -100.00 |  400.00\n"
        "2026-01-25 |  200.00 |  600.00\n"
    )
    
    assert captured.out == expected_statement  # AC-4.5