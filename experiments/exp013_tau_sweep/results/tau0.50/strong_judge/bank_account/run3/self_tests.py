import pytest
from solution import BankAccount

def test_initial_balance():
    account = BankAccount()
    assert account.balance == 0  # AC-1.1: A newly opened account has a balance of 0.

def test_deposit_increases_balance():
    account = BankAccount()
    account.deposit(100, "2023-10-01")
    assert account.balance == 100  # AC-1.2: A deposit increases the balance by exactly the deposited amount.

def test_successive_deposits_accumulate():
    account = BankAccount()
    account.deposit(100, "2023-10-01")
    account.deposit(50, "2023-10-02")
    assert account.balance == 150  # AC-1.3: Successive deposits accumulate into the balance.

def test_withdrawal_decreases_balance():
    account = BankAccount()
    account.deposit(100, "2023-10-01")
    account.withdraw(50, "2023-10-02")
    assert account.balance == 50  # AC-2.1: A withdrawal decreases the balance by exactly the withdrawn amount.

def test_withdrawal_leaves_balance_zero():
    account = BankAccount()
    account.deposit(100, "2023-10-01")
    account.withdraw(100, "2023-10-02")
    assert account.balance == 0  # AC-2.2: Withdrawing exactly the current balance is allowed and leaves the balance at 0.

def test_reject_zero_or_negative_deposit():
    account = BankAccount()
    initial_balance = account.balance
    with pytest.raises(Exception) as exc_info:
        account.deposit(0, "2023-10-01")  # AC-3.1: A deposit of zero or a negative amount is rejected.
    assert str(exc_info.value) == "Amount must be positive"
    assert account.balance == initial_balance  # AC-3.4: Balance unchanged after rejection.
    
    with pytest.raises(Exception) as exc_info:
        account.deposit(-50, "2023-10-01")  # AC-3.1: A deposit of zero or a negative amount is rejected.
    assert str(exc_info.value) == "Amount must be positive"
    assert account.balance == initial_balance  # AC-3.4: Balance unchanged after rejection.

def test_reject_zero_or_negative_withdrawal():
    account = BankAccount()
    account.deposit(100, "2023-10-01")
    initial_balance = account.balance
    with pytest.raises(Exception) as exc_info:
        account.withdraw(0, "2023-10-02")  # AC-3.2: A withdrawal of zero or a negative amount is rejected.
    assert str(exc_info.value) == "Amount must be positive"
    assert account.balance == initial_balance  # AC-3.4: Balance unchanged after rejection.
    
    with pytest.raises(Exception) as exc_info:
        account.withdraw(-50, "2023-10-02")  # AC-3.2: A withdrawal of zero or a negative amount is rejected.
    assert str(exc_info.value) == "Amount must be positive"
    assert account.balance == initial_balance  # AC-3.4: Balance unchanged after rejection.

def test_reject_withdrawal_greater_than_balance():
    account = BankAccount()
    account.deposit(100, "2023-10-01")
    with pytest.raises(Exception) as exc_info:
        account.withdraw(150, "2023-10-02")  # AC-3.3: A withdrawal greater than the current balance is rejected.
    assert str(exc_info.value) == "Cannot withdraw more than current balance"

    with pytest.raises(Exception) as exc_info:
        account.withdraw(100, "2023-10-02")  # This should leave the balance at 0.
    assert str(exc_info.value) == "Cannot withdraw more than current balance"

def test_rejected_operations_dont_change_balance():
    account = BankAccount()
    account.deposit(100, "2023-10-01")
    initial_balance = account.balance
    with pytest.raises(Exception) as exc_info:
        account.withdraw(150, "2023-10-02")  # This should raise an error
    assert str(exc_info.value) == "Cannot withdraw more than current balance"
    assert account.balance == initial_balance  # AC-3.4: The balance should remain unchanged after rejection.

def test_rejected_operations_dont_change_statement():
    account = BankAccount()
    account.deposit(100, "2023-10-01")
    initial_statement = account.print_statement()  # Capture initial statement
    with pytest.raises(Exception) as exc_info:
        account.withdraw(150, "2023-10-02")  # This should raise an error
    assert str(exc_info.value) == "Cannot withdraw more than current balance"
    assert account.print_statement() == initial_statement  # AC-3.4: Statement unchanged after rejection.

def test_print_statement_no_transactions():
    account = BankAccount()
    expected_statement = "Date       | Amount  | Balance"  # AC-4.1: With no transactions, the statement is exactly the header.
    assert account.print_statement() == expected_statement  

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
    )  # AC-4.5: Canonical worked example.
    assert account.print_statement() == expected_statement  # Check the printed statement.

def test_print_statement_transaction_order():
    account = BankAccount()
    account.deposit(300, "2023-10-03")
    account.deposit(200, "2023-10-01")  # Earlier date
    account.withdraw(100, "2023-10-02")  # In between
    expected_statement = (
        "Date       | Amount  | Balance\n"
        "2023-10-01 |  200.00 |  200.00\n"
        "2023-10-02 | -100.00 |  100.00\n"
        "2023-10-03 |  300.00 |  400.00\n"
    )  # Transactions in chronological order.
    assert account.print_statement() == expected_statement  # Check the printed statement.

def test_print_statement_with_fractional_amount():
    account = BankAccount()
    account.deposit(12.34, "2023-10-01")
    expected_statement = (
        "Date       | Amount  | Balance\n"
        "2023-10-01 |  12.34  |  12.34\n"
    )  # Testing fractional amounts.
    assert account.print_statement() == expected_statement  # Check the printed statement.