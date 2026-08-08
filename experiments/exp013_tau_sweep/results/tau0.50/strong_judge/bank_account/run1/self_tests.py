import pytest
from solution import *

def test_initial_balance_is_zero():
    account = BankAccount()  # Assuming a constructor that initializes the account
    assert account.balance == 0

def test_deposit_increases_balance():
    account = BankAccount()
    account.deposit(100, "2022-01-01")
    assert account.balance == 100  # 0 + 100

def test_successive_deposits_accumulate_balance():
    account = BankAccount()
    account.deposit(100, "2022-01-01")
    account.deposit(50, "2022-01-02")
    assert account.balance == 150  # 100 + 50

def test_withdraw_reduces_balance():
    account = BankAccount()
    account.deposit(100, "2022-01-01")
    account.withdraw(50, "2022-01-02")
    assert account.balance == 50  # 100 - 50

def test_withdraw_exact_balance_leaves_zero():
    account = BankAccount()
    account.deposit(100, "2022-01-01")
    account.withdraw(100, "2022-01-02")
    assert account.balance == 0  # 100 - 100

def test_reject_zero_deposit():
    account = BankAccount()
    with pytest.raises(Exception) as exc:
        account.deposit(0, "2022-01-01")
    assert str(exc.value) == "Amount must be positive"

def test_reject_negative_deposit():
    account = BankAccount()
    with pytest.raises(Exception) as exc:
        account.deposit(-50, "2022-01-01")
    assert str(exc.value) == "Amount must be positive"

def test_reject_zero_withdrawal():
    account = BankAccount()
    with pytest.raises(Exception) as exc:
        account.withdraw(0, "2022-01-01")
    assert str(exc.value) == "Amount must be positive"

def test_reject_negative_withdrawal():
    account = BankAccount()
    with pytest.raises(Exception) as exc:
        account.withdraw(-50, "2022-01-01")
    assert str(exc.value) == "Amount must be positive"

def test_reject_withdrawal_greater_than_balance():
    account = BankAccount()
    account.deposit(100, "2022-01-01")
    with pytest.raises(Exception) as exc:
        account.withdraw(150, "2022-01-02")
    assert str(exc.value) == "Cannot withdraw more than current balance"

def test_positive_withdrawal_from_zero_balance():
    account = BankAccount()
    with pytest.raises(Exception) as exc:
        account.withdraw(50, "2022-01-01")
    assert str(exc.value) == "Cannot withdraw more than current balance"

def test_rejected_deposit_does_not_change_balance():
    account = BankAccount()
    account.deposit(100, "2022-01-01")
    statement_before = account.statement()
    try:
        account.deposit(0, "2022-01-02")
    except Exception:
        pass
    assert account.balance == 100
    assert account.statement() == statement_before

def test_rejected_withdrawal_does_not_change_balance():
    account = BankAccount()
    account.deposit(100, "2022-01-01")
    statement_before = account.statement()
    try:
        account.withdraw(150, "2022-01-02")
    except Exception:
        pass
    assert account.balance == 100
    assert account.statement() == statement_before

def test_statement_with_no_transactions():
    account = BankAccount()
    expected = "Date       | Amount  | Balance"
    assert account.statement() == expected

def test_statement_with_transactions():
    account = BankAccount()
    account.deposit(500.00, "2026-01-15")
    account.withdraw(100.00, "2026-01-20")
    account.deposit(200.00, "2026-01-25")
    expected = (
        "Date       | Amount  | Balance\n"
        "2026-01-15 |  500.00 |  500.00\n"
        "2026-01-20 | -100.00 |  400.00\n"
        "2026-01-25 |  200.00 |  600.00"
    )
    assert account.statement() == expected

def test_statement_with_non_ascending_dates():
    account = BankAccount()
    account.deposit(100.00, "2026-01-20")
    account.withdraw(50.00, "2026-01-15")
    account.deposit(200.00, "2026-01-25")
    expected = (
        "Date       | Amount  | Balance\n"
        "2026-01-15 |  -50.00 |  -50.00\n"
        "2026-01-20 |  100.00 |   50.00\n"
        "2026-01-25 |  200.00 |  250.00"
    )
    assert account.statement() == expected

def test_statement_with_various_amounts_formatting():
    account = BankAccount()
    account.deposit(1.00, "2026-01-01")
    account.deposit(10.00, "2026-01-02")
    account.deposit(100.00, "2026-01-03")
    expected = (
        "Date       | Amount  | Balance\n"
        "2026-01-01 |   1.00 |   1.00\n"
        "2026-01-02 |  10.00 |  11.00\n"
        "2026-01-03 | 100.00 | 111.00"
    )
    assert account.statement() == expected

def test_negative_amount_shorter_than_seven_characters_formatting():
    account = BankAccount()
    account.deposit(-50.00, "2026-01-01")  # Assuming this raises an exception
    with pytest.raises(Exception) as exc:
        account.withdraw(-50.00, "2026-01-02")
    assert str(exc.value) == "Amount must be positive"