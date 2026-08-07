from solution import BankAccount
import pytest

def test_initial_balance():
    account = BankAccount()
    assert account.balance == 0  # AC-1.1

def test_deposit_increases_balance():
    account = BankAccount()
    account.deposit(100, "2026-01-15")
    assert account.balance == 100  # AC-1.2

def test_successive_deposits_accumulate_balance():
    account = BankAccount()
    account.deposit(100, "2026-01-15")
    account.deposit(200, "2026-01-20")
    assert account.balance == 300  # AC-1.3

def test_withdrawal_decreases_balance():
    account = BankAccount()
    account.deposit(200, "2026-01-15")
    account.withdraw(100, "2026-01-20")
    assert account.balance == 100  # AC-2.1

def test_withdrawing_exact_balance_leaves_zero():
    account = BankAccount()
    account.deposit(100, "2026-01-15")
    account.withdraw(100, "2026-01-20")
    assert account.balance == 0  # AC-2.2

def test_reject_zero_deposit():
    account = BankAccount()
    with pytest.raises(Exception) as excinfo:
        account.deposit(0, "2026-01-15")  # Attempt to deposit 0
    assert str(excinfo.value) == "Amount must be positive"  # AC-3.1
    assert account.balance == 0  # AC-3.4
    assert account.statement() == "Date       | Amount  | Balance"  # AC-3.4

def test_reject_negative_deposit():
    account = BankAccount()
    with pytest.raises(Exception) as excinfo:
        account.deposit(-50, "2026-01-15")  # Attempt to deposit -50
    assert str(excinfo.value) == "Amount must be positive"  # AC-3.1
    assert account.balance == 0  # AC-3.4
    assert account.statement() == "Date       | Amount  | Balance"  # AC-3.4

def test_reject_zero_withdrawal():
    account = BankAccount()
    with pytest.raises(Exception) as excinfo:
        account.withdraw(0, "2026-01-15")  # Attempt to withdraw 0
    assert str(excinfo.value) == "Amount must be positive"  # AC-3.2
    assert account.balance == 0  # AC-3.4
    assert account.statement() == "Date       | Amount  | Balance"  # AC-3.4

def test_reject_negative_withdrawal():
    account = BankAccount()
    with pytest.raises(Exception) as excinfo:
        account.withdraw(-50, "2026-01-15")  # Attempt to withdraw -50
    assert str(excinfo.value) == "Amount must be positive"  # AC-3.2
    assert account.balance == 0  # AC-3.4
    assert account.statement() == "Date       | Amount  | Balance"  # AC-3.4

def test_reject_withdrawal_more_than_balance():
    account = BankAccount()
    account.deposit(100, "2026-01-15")
    with pytest.raises(Exception) as excinfo:
        account.withdraw(200, "2026-01-20")  # Attempt to withdraw more than balance
    assert str(excinfo.value) == "Cannot withdraw more than current balance"  # AC-3.3
    assert account.balance == 100  # AC-3.4
    assert account.statement() == "Date       | Amount  | Balance\n2026-01-15 |  100.00 |  100.00"  # AC-3.4

def test_reject_withdrawal_from_zero_balance():
    account = BankAccount()
    with pytest.raises(Exception) as excinfo:
        account.withdraw(50, "2026-01-15")  # Attempt to withdraw from zero balance
    assert str(excinfo.value) == "Cannot withdraw more than current balance"  # AC-3.3
    assert account.balance == 0  # AC-3.4
    assert account.statement() == "Date       | Amount  | Balance"  # AC-3.4

def test_statement_with_no_transactions():
    account = BankAccount()
    expected_output = "Date       | Amount  | Balance"
    assert account.statement() == expected_output  # AC-4.1

def test_statement_with_transactions():
    account = BankAccount()
    account.deposit(500, "2026-01-15")
    account.withdraw(100, "2026-01-20")
    account.deposit(200, "2026-01-25")
    expected_output = (
        "Date       | Amount  | Balance\n"
        "2026-01-15 |  500.00 |  500.00\n"
        "2026-01-20 | -100.00 |  400.00\n"
        "2026-01-25 |  200.00 |  600.00"
    )
    assert account.statement() == expected_output  # AC-4.5

def test_rejected_deposit_preserves_statement():
    account = BankAccount()
    initial_statement = account.statement()
    with pytest.raises(Exception) as excinfo:
        account.deposit(0, "2026-01-15")  # Attempt to deposit 0
    assert str(excinfo.value) == "Amount must be positive"  # AC-3.1
    assert account.statement() == initial_statement  # AC-3.4

def test_rejected_withdrawal_preserves_statement():
    account = BankAccount()
    account.deposit(100, "2026-01-15")
    initial_statement = account.statement()
    with pytest.raises(Exception) as excinfo:
        account.withdraw(200, "2026-01-20")  # Attempt to withdraw more than balance
    assert str(excinfo.value) == "Cannot withdraw more than current balance"  # AC-3.3
    assert account.statement() == initial_statement  # AC-3.4