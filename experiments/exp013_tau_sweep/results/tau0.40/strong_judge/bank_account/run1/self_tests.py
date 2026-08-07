import pytest
from solution import *

def test_initial_balance():
    account = Account()  # Assuming the class name is Account
    assert account.balance == 0  # AC-1.1: A newly opened account has a balance of 0.

def test_deposit_increases_balance():
    account = Account()
    account.deposit(100, "2026-01-01")
    assert account.balance == 100  # AC-1.2: A deposit increases the balance by exactly the deposited amount.

def test_successive_deposits_accumulate():
    account = Account()
    account.deposit(100, "2026-01-01")
    account.deposit(200, "2026-01-02")
    assert account.balance == 300  # AC-1.3: Successive deposits accumulate into the balance.

def test_withdrawal_decreases_balance():
    account = Account()
    account.deposit(200, "2026-01-01")
    account.withdraw(100, "2026-01-02")
    assert account.balance == 100  # AC-2.1: A withdrawal decreases the balance by exactly the withdrawn amount.

def test_withdrawal_to_zero_balance():
    account = Account()
    account.deposit(100, "2026-01-01")
    account.withdraw(100, "2026-01-02")
    assert account.balance == 0  # AC-2.2: Withdrawing exactly the current balance is allowed and leaves the balance at 0.

def test_invalid_deposit_zero_or_negative():
    account = Account()
    initial_balance = account.balance
    with pytest.raises(Exception) as exc_info:
        account.deposit(0, "2026-01-01")  # AC-3.1: A deposit of zero is rejected.
    assert str(exc_info.value) == "Amount must be positive"
    assert account.balance == initial_balance  # AC-3.4: The balance should remain unchanged.

    with pytest.raises(Exception) as exc_info:
        account.deposit(-50, "2026-01-01")  # AC-3.1: A deposit of a negative amount is rejected.
    assert str(exc_info.value) == "Amount must be positive"
    assert account.balance == initial_balance  # AC-3.4: The balance should remain unchanged.

def test_invalid_withdrawal_zero_or_negative():
    account = Account()
    initial_balance = account.balance
    with pytest.raises(Exception) as exc_info:
        account.withdraw(0, "2026-01-01")  # AC-3.2: A withdrawal of zero is rejected.
    assert str(exc_info.value) == "Amount must be positive"
    assert account.balance == initial_balance  # AC-3.4: The balance should remain unchanged.

    with pytest.raises(Exception) as exc_info:
        account.withdraw(-50, "2026-01-01")  # AC-3.2: A withdrawal of a negative amount is rejected.
    assert str(exc_info.value) == "Amount must be positive"
    assert account.balance == initial_balance  # AC-3.4: The balance should remain unchanged.

def test_withdrawal_exceeds_balance():
    account = Account()
    account.deposit(50, "2026-01-01")
    with pytest.raises(Exception) as exc_info:
        account.withdraw(100, "2026-01-02")  # AC-3.3: A withdrawal greater than the current balance is rejected.
    assert str(exc_info.value) == "Cannot withdraw more than current balance"

def test_positive_withdrawal_from_zero_balance():
    account = Account()  # New account with zero balance
    initial_balance = account.balance
    initial_statement = account.statement()
    with pytest.raises(Exception) as exc_info:
        account.withdraw(50, "2026-01-01")  # AC-3.3: Withdraw from zero balance
    assert str(exc_info.value) == "Cannot withdraw more than current balance"
    assert account.balance == initial_balance  # AC-3.4: The balance should remain unchanged.
    assert account.statement() == initial_statement  # AC-3.4: The statement should remain unchanged.

def test_rejected_operations_do_not_change_balance_and_statement():
    account = Account()
    account.deposit(100, "2026-01-01")
    initial_balance = account.balance
    initial_statement = account.statement()

    try:
        account.deposit(-50, "2026-01-02")
    except Exception:  # Expected exception
        pass
    
    assert account.balance == initial_balance  # AC-3.4: The balance should remain unchanged.
    assert account.statement() == initial_statement  # AC-3.4: The statement should remain unchanged.

    try:
        account.withdraw(200, "2026-01-03")
    except Exception:  # Expected exception
        pass

    assert account.balance == initial_balance  # AC-3.4: The balance should remain unchanged.
    assert account.statement() == initial_statement  # AC-3.4: The statement should remain unchanged.

def test_statement_with_no_transactions():
    account = Account()
    expected_statement = "Date       | Amount  | Balance"
    assert account.statement() == expected_statement  # AC-4.1: Statement with no transactions.

def test_statement_with_transactions():
    account = Account()
    account.deposit(500.00, "2026-01-15")
    account.withdraw(100.00, "2026-01-20")
    account.deposit(200.00, "2026-01-25")
    expected_statement = (
        "Date       | Amount  | Balance\n"
        "2026-01-15 |  500.00 |  500.00\n"
        "2026-01-20 | -100.00 |  400.00\n"
        "2026-01-25 |  200.00 |  600.00"
    )
    assert account.statement() == expected_statement  # AC-4.5: The canonical worked example produces the expected statement.

def test_statement_ordering_with_same_dates():
    account = Account()
    account.deposit(500.00, "2026-01-15")
    account.deposit(300.00, "2026-01-15")
    account.withdraw(100.00, "2026-01-15")
    expected_statement = (
        "Date       | Amount  | Balance\n"
        "2026-01-15 |  500.00 |  500.00\n"
        "2026-01-15 |  300.00 |  800.00\n"
        "2026-01-15 | -100.00 |  700.00"
    )
    assert account.statement() == expected_statement  # AC-4.4: Transactions with the same date retain their order.