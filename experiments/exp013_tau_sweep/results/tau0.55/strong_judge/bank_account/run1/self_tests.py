from solution import BankAccount
import pytest

def test_initial_balance():
    account = BankAccount()
    assert account.balance == 0  # AC-1.1

def test_deposit_increases_balance():
    account = BankAccount()
    account.deposit('2023-01-01', 100.00)
    assert account.balance == 100.00  # AC-1.2

def test_successive_deposits_accumulate():
    account = BankAccount()
    account.deposit('2023-01-01', 100.00)
    account.deposit('2023-01-02', 50.00)
    assert account.balance == 150.00  # AC-1.3

def test_withdrawal_decreases_balance():
    account = BankAccount()
    account.deposit('2023-01-01', 100.00)
    account.withdraw('2023-01-02', 50.00)
    assert account.balance == 50.00  # AC-2.1

def test_withdrawal_leaves_balance_zero():
    account = BankAccount()
    account.deposit('2023-01-01', 100.00)
    account.withdraw('2023-01-02', 100.00)
    assert account.balance == 0  # AC-2.2

def test_reject_negative_deposit():
    account = BankAccount()
    with pytest.raises(Exception) as exc_info:
        account.deposit('2023-01-01', -50.00)
    assert str(exc_info.value) == "Amount must be positive"  # AC-3.1
    assert account.balance == 0  # balance unchanged
    assert account.statement() == "Date       | Amount  | Balance"  # AC-3.4

def test_reject_zero_deposit():
    account = BankAccount()
    with pytest.raises(Exception) as exc_info:
        account.deposit('2023-01-01', 0.00)
    assert str(exc_info.value) == "Amount must be positive"  # AC-3.1
    assert account.balance == 0  # balance unchanged
    assert account.statement() == "Date       | Amount  | Balance"  # AC-3.4

def test_reject_negative_withdrawal():
    account = BankAccount()
    account.deposit('2023-01-01', 100.00)
    with pytest.raises(Exception) as exc_info:
        account.withdraw('2023-01-02', -50.00)
    assert str(exc_info.value) == "Amount must be positive"  # AC-3.2
    assert account.balance == 100.00  # balance unchanged
    assert account.statement() == "Date       | Amount  | Balance\n2023-01-01 |  100.00 |  100.00"  # AC-3.4

def test_reject_zero_withdrawal():
    account = BankAccount()
    account.deposit('2023-01-01', 100.00)
    with pytest.raises(Exception) as exc_info:
        account.withdraw('2023-01-02', 0.00)
    assert str(exc_info.value) == "Amount must be positive"  # AC-3.2
    assert account.balance == 100.00  # balance unchanged
    assert account.statement() == "Date       | Amount  | Balance\n2023-01-01 |  100.00 |  100.00"  # AC-3.4

def test_reject_withdrawal_greater_than_balance():
    account = BankAccount()
    account.deposit('2023-01-01', 100.00)
    with pytest.raises(Exception) as exc_info:
        account.withdraw('2023-01-02', 150.00)
    assert str(exc_info.value) == "Cannot withdraw more than current balance"  # AC-3.3
    assert account.balance == 100.00  # balance unchanged
    assert account.statement() == "Date       | Amount  | Balance\n2023-01-01 |  100.00 |  100.00"  # AC-3.4

def test_reject_withdrawal_from_zero_balance():
    account = BankAccount()
    with pytest.raises(Exception) as exc_info:
        account.withdraw('2023-01-01', 50.00)
    assert str(exc_info.value) == "Cannot withdraw more than current balance"  # AC-3.3
    assert account.balance == 0  # balance unchanged
    assert account.statement() == "Date       | Amount  | Balance"  # AC-3.4

def test_statement_with_no_transactions():
    account = BankAccount()
    expected_statement = "Date       | Amount  | Balance"
    assert account.statement() == expected_statement  # AC-4.1

def test_statement_with_one_transaction():
    account = BankAccount()
    account.deposit('2023-01-01', 100.00)
    expected_statement = "Date       | Amount  | Balance"
    expected_statement += "\n2023-01-01 |  100.00 |  100.00"
    assert account.statement() == expected_statement  # AC-4.2

def test_statement_with_multiple_transactions():
    account = BankAccount()
    account.deposit('2023-01-01', 500.00)
    account.withdraw('2023-01-02', 100.00)
    account.deposit('2023-01-03', 200.00)
    expected_statement = "Date       | Amount  | Balance"
    expected_statement += "\n2023-01-01 |  500.00 |  500.00"
    expected_statement += "\n2023-01-02 | -100.00 |  400.00"
    expected_statement += "\n2023-01-03 |  200.00 |  600.00"
    assert account.statement() == expected_statement  # AC-4.4

def test_statement_with_canonical_example():
    account = BankAccount()
    account.deposit('2026-01-15', 500.00)
    account.withdraw('2026-01-20', 100.00)
    account.deposit('2026-01-25', 200.00)
    expected_statement = "Date       | Amount  | Balance"
    expected_statement += "\n2026-01-15 |  500.00 |  500.00"
    expected_statement += "\n2026-01-20 | -100.00 |  400.00"
    expected_statement += "\n2026-01-25 |  200.00 |  600.00"
    assert account.statement() == expected_statement  # AC-4.5

def test_statement_with_same_date_transactions():
    account = BankAccount()
    account.deposit('2023-01-01', 100.00)
    account.withdraw('2023-01-01', 50.00)
    account.deposit('2023-01-01', 200.00)
    expected_statement = "Date       | Amount  | Balance"
    expected_statement += "\n2023-01-01 |  100.00 |  100.00"
    expected_statement += "\n2023-01-01 | -50.00  |   50.00"
    expected_statement += "\n2023-01-01 |  200.00 |  250.00"
    assert account.statement() == expected_statement  # AC-4.4