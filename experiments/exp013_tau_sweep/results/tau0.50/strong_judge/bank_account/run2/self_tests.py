import pytest
from solution import BankAccount

def test_initial_balance_is_zero():
    account = BankAccount()
    assert account.balance == 0  # AC-1.1

def test_deposit_increases_balance():
    account = BankAccount()
    account.deposit(100, '2023-01-01')
    assert account.balance == 100  # AC-1.2

def test_successive_deposits_accumulate_balance():
    account = BankAccount()
    account.deposit(100, '2023-01-01')
    account.deposit(200, '2023-01-02')
    assert account.balance == 300  # AC-1.3

def test_withdrawal_decreases_balance():
    account = BankAccount()
    account.deposit(200, '2023-01-01')
    account.withdraw(100, '2023-01-02')
    assert account.balance == 100  # AC-2.1

def test_withdrawal_leaves_balance_zero():
    account = BankAccount()
    account.deposit(100, '2023-01-01')
    account.withdraw(100, '2023-01-02')
    assert account.balance == 0  # AC-2.2

def test_reject_zero_or_negative_deposit():
    account = BankAccount()
    with pytest.raises(Exception) as exc:
        account.deposit(0, '2023-01-01')  # AC-3.1
    assert str(exc.value) == "Amount must be positive"
    
    with pytest.raises(Exception) as exc:
        account.deposit(-100, '2023-01-01')  # AC-3.1
    assert str(exc.value) == "Amount must be positive"

def test_reject_zero_or_negative_withdrawal():
    account = BankAccount()
    with pytest.raises(Exception) as exc:
        account.withdraw(0, '2023-01-01')  # AC-3.2
    assert str(exc.value) == "Amount must be positive"

    with pytest.raises(Exception) as exc:
        account.withdraw(-100, '2023-01-01')  # AC-3.2
    assert str(exc.value) == "Amount must be positive"

def test_reject_withdrawal_greater_than_balance():
    account = BankAccount()
    account.deposit(100, '2023-01-01')
    with pytest.raises(Exception) as exc:
        account.withdraw(150, '2023-01-02')  # AC-3.3
    assert str(exc.value) == "Cannot withdraw more than current balance"

def test_rejected_deposit_does_not_change_balance():
    account = BankAccount()
    account.deposit(100, '2023-01-01')
    initial_balance = account.balance
    with pytest.raises(Exception) as exc:
        account.deposit(-50, '2023-01-02')  # AC-3.4
    assert str(exc.value) == "Amount must be positive"
    assert account.balance == initial_balance

def test_rejected_withdrawal_does_not_change_balance():
    account = BankAccount()
    account.deposit(100, '2023-01-01')
    initial_balance = account.balance
    with pytest.raises(Exception) as exc:
        account.withdraw(150, '2023-01-02')  # AC-3.4
    assert str(exc.value) == "Cannot withdraw more than current balance"
    assert account.balance == initial_balance

def test_statement_with_no_transactions():
    account = BankAccount()
    expected = "Date       | Amount  | Balance"
    assert account.statement() == expected  # AC-4.1

def test_statement_with_transactions():
    account = BankAccount()
    account.deposit(500, '2026-01-15')
    account.withdraw(100, '2026-01-20')
    account.deposit(200, '2026-01-25')
    expected = (
        "Date       | Amount  | Balance\n"
        "2026-01-15 |  500.00 |  500.00\n"
        "2026-01-20 | -100.00 |  400.00\n"
        "2026-01-25 |  200.00 |  600.00"
    )
    assert account.statement() == expected  # AC-4.5

def test_statement_preserves_after_rejected_deposit():
    account = BankAccount()
    account.deposit(100, '2023-01-01')
    initial_statement = account.statement()
    with pytest.raises(Exception) as exc:
        account.deposit(-50, '2023-01-02')  # AC-3.4
    assert str(exc.value) == "Amount must be positive"
    assert account.statement() == initial_statement

def test_statement_preserves_after_rejected_withdrawal():
    account = BankAccount()
    account.deposit(100, '2023-01-01')
    initial_statement = account.statement()
    with pytest.raises(Exception) as exc:
        account.withdraw(150, '2023-01-02')  # AC-3.4
    assert str(exc.value) == "Cannot withdraw more than current balance"
    assert account.statement() == initial_statement

def test_statement_orders_transactions_oldest_first():
    account = BankAccount()
    account.deposit(300, '2023-01-01')
    account.withdraw(100, '2023-01-02')
    account.deposit(200, '2023-01-03')
    expected = (
        "Date       | Amount  | Balance\n"
        "2023-01-01 |  300.00 |  300.00\n"
        "2023-01-02 | -100.00 |  200.00\n"
        "2023-01-03 |  200.00 |  400.00"
    )
    assert account.statement() == expected  # AC-4.4

def test_statement_after_withdrawing_full_balance():
    account = BankAccount()
    account.deposit(100, '2023-01-01')
    account.withdraw(100, '2023-01-02')
    expected = (
        "Date       | Amount  | Balance\n"
        "2023-01-01 |  100.00 |  100.00\n"
        "2023-01-02 | -100.00 |    0.00"
    )
    assert account.statement() == expected  # AC-4.2