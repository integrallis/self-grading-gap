import pytest
from solution import BankAccount

def test_initial_balance():
    account = BankAccount()
    assert account.balance == 0  # AC-1.1: A newly opened account has a balance of 0.

def test_deposit_increases_balance():
    account = BankAccount()
    account.deposit(100, "2026-01-15")
    assert account.balance == 100  # AC-1.2: A deposit increases the balance by exactly the deposited amount.

def test_successive_deposits_accumulate_balance():
    account = BankAccount()
    account.deposit(100, "2026-01-15")
    account.deposit(200, "2026-01-20")
    assert account.balance == 300  # AC-1.3: Successive deposits accumulate into the balance.

def test_withdrawal_decreases_balance():
    account = BankAccount()
    account.deposit(200, "2026-01-15")
    account.withdraw(100, "2026-01-20")
    assert account.balance == 100  # AC-2.1: A withdrawal decreases the balance by exactly the withdrawn amount.

def test_withdrawal_to_zero_balance():
    account = BankAccount()
    account.deposit(100, "2026-01-15")
    account.withdraw(100, "2026-01-20")
    assert account.balance == 0  # AC-2.2: Withdrawing exactly the current balance is allowed and leaves the balance at 0.

def test_reject_zero_deposit():
    account = BankAccount()
    with pytest.raises(Exception) as excinfo:
        account.deposit(0, "2026-01-15")  # AC-3.1: A deposit of zero or a negative amount is rejected.
    assert str(excinfo.value) == "Amount must be positive"  # Exact message comparison.

def test_reject_negative_deposit():
    account = BankAccount()
    with pytest.raises(Exception) as excinfo:
        account.deposit(-50, "2026-01-15")  # AC-3.1: A deposit of zero or a negative amount is rejected.
    assert str(excinfo.value) == "Amount must be positive"  # Exact message comparison.

def test_reject_zero_withdrawal():
    account = BankAccount()
    with pytest.raises(Exception) as excinfo:
        account.withdraw(0, "2026-01-15")  # AC-3.2: A withdrawal of zero or a negative amount is rejected.
    assert str(excinfo.value) == "Amount must be positive"  # Exact message comparison.

def test_reject_negative_withdrawal():
    account = BankAccount()
    with pytest.raises(Exception) as excinfo:
        account.withdraw(-50, "2026-01-15")  # AC-3.2: A withdrawal of zero or a negative amount is rejected.
    assert str(excinfo.value) == "Amount must be positive"  # Exact message comparison.

def test_reject_withdrawal_greater_than_balance():
    account = BankAccount()
    account.deposit(100, "2026-01-15")
    with pytest.raises(Exception) as excinfo:
        account.withdraw(150, "2026-01-20")  # AC-3.3: A withdrawal greater than the current balance is rejected.
    assert str(excinfo.value) == "Cannot withdraw more than current balance"  # Exact message comparison.

def test_positive_withdrawal_from_zero_balance():
    account = BankAccount()
    with pytest.raises(Exception) as excinfo:
        account.withdraw(50, "2026-01-15")  # AC-3.3: A withdrawal greater than the current balance is rejected.
    assert str(excinfo.value) == "Cannot withdraw more than current balance"  # Exact message comparison.

def test_rejected_deposit_does_not_change_balance():
    account = BankAccount()
    account.deposit(100, "2026-01-15")
    initial_balance = account.balance
    with pytest.raises(Exception) as excinfo:
        account.deposit(-50, "2026-01-20")  # AC-3.1
    assert account.balance == initial_balance  # AC-3.4: The balance stays the same after a rejected deposit.

def test_rejected_withdrawal_does_not_change_balance():
    account = BankAccount()
    account.deposit(100, "2026-01-15")
    initial_balance = account.balance
    with pytest.raises(Exception) as excinfo:
        account.withdraw(150, "2026-01-20")  # AC-3.3
    assert account.balance == initial_balance  # AC-3.4: The balance stays the same after a rejected withdrawal.

def test_empty_statement():
    account = BankAccount()
    statement = account.statement()
    assert statement == "Date       | Amount  | Balance"  # AC-4.1: The statement with no transactions.

def test_statement_with_transactions():
    account = BankAccount()
    account.deposit(500, "2026-01-15")
    account.withdraw(100, "2026-01-20")
    account.deposit(200, "2026-01-25")
    
    expected_statement = (
        "Date       | Amount  | Balance\n"
        "2026-01-15 |  500.00 |  500.00\n"
        "2026-01-20 | -100.00 |  400.00\n"
        "2026-01-25 |  200.00 |  600.00"
    )
    assert account.statement() == expected_statement  # AC-4.5: The canonical worked example.

def test_statement_transaction_ordering():
    account = BankAccount()
    account.deposit(200, "2026-01-25")
    account.deposit(500, "2026-01-15")
    account.withdraw(100, "2026-01-20")

    expected_statement = (
        "Date       | Amount  | Balance\n"
        "2026-01-15 |  500.00 |  500.00\n"
        "2026-01-20 | -100.00 |  400.00\n"
        "2026-01-25 |  200.00 |  600.00"
    )
    assert account.statement() == expected_statement  # Ensure correct ordering of transactions.

def test_rejected_deposit_statement_unchanged():
    account = BankAccount()
    account.deposit(100, "2026-01-15")
    initial_statement = account.statement()
    with pytest.raises(Exception):
        account.deposit(-50, "2026-01-20")  # AC-3.1
    assert account.statement() == initial_statement  # AC-3.4: The statement stays the same after a rejected deposit.

def test_rejected_withdrawal_statement_unchanged():
    account = BankAccount()
    account.deposit(100, "2026-01-15")
    initial_statement = account.statement()
    with pytest.raises(Exception):
        account.withdraw(150, "2026-01-20")  # AC-3.3
    assert account.statement() == initial_statement  # AC-3.4: The statement stays the same after a rejected withdrawal.