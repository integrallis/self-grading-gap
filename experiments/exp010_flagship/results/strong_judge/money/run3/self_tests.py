import pytest
from solution import Money, Bank

# US-1: Scaling amounts
def test_multiply_dollars():
    amount = Money(5, "USD")
    result = amount.multiply(2)  # 5 * 2 = 10
    assert result == Money(10, "USD")

def test_multiply_francs():
    amount = Money(5, "CHF")
    result = amount.multiply(2)  # 5 * 2 = 10
    assert result == Money(10, "CHF")

def test_multiply_francs_three():
    amount = Money(5, "CHF")
    result = amount.multiply(3)  # 5 * 3 = 15
    assert result == Money(15, "CHF")

def test_multiply_does_not_alter_original():
    amount = Money(5, "USD")
    amount.multiply(2)
    assert amount == Money(5, "USD")

# US-2: Comparing amounts
def test_equal_amounts():
    amount1 = Money(5, "USD")
    amount2 = Money(5, "USD")
    assert amount1 == amount2

def test_not_equal_different_quantities():
    amount1 = Money(5, "USD")
    amount2 = Money(6, "USD")
    assert amount1 != amount2

def test_not_equal_different_currencies():
    amount1 = Money(5, "USD")
    amount2 = Money(5, "CHF")
    assert amount1 != amount2

def test_currency_code_usd():
    amount = Money(5, "USD")
    assert amount.currency() == "USD"

def test_currency_code_chf():
    amount = Money(5, "CHF")
    assert amount.currency() == "CHF"

# US-3: Adding and reducing expressions
def test_add_same_currency():
    amount1 = Money(5, "USD")
    amount2 = Money(5, "USD")
    bank = Bank()
    sum_expr = amount1.add(amount2)  # 5 + 5 = 10
    result = bank.reduce(sum_expr, "USD")  # should reduce to 10 USD
    assert result == Money(10, "USD")

def test_reduce_plain_amount():
    amount = Money(5, "USD")
    bank = Bank()
    result = bank.reduce(amount, "USD")  # no exchange needed
    assert result == Money(5, "USD")

def test_add_mixed_currencies():
    amount1 = Money(5, "USD")
    amount2 = Money(10, "CHF")
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # Register 2:1 exchange rate
    sum_expr = amount1.add(amount2)  # 5 USD + 10 CHF
    result = bank.reduce(sum_expr, "USD")  # 10 CHF = 5 USD at 2:1 rate, so total = 10 USD
    assert result == Money(10, "USD")

def test_multiply_sum_before_reduction():
    amount1 = Money(5, "USD")
    amount2 = Money(10, "CHF")
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # Register 2:1 exchange rate
    sum_expr = amount1.add(amount2)  # 5 USD + 10 CHF
    scaled_sum = sum_expr.multiply(2)  # (5 + 10) * 2 = 30
    result = bank.reduce(scaled_sum, "USD")  # should reduce to 20 USD
    assert result == Money(20, "USD")

def test_add_sum_with_further_amount():
    amount1 = Money(5, "USD")
    amount2 = Money(10, "CHF")
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # Register 2:1 exchange rate
    sum_expr = amount1.add(amount2)  # 5 USD + 10 CHF
    sum_expr = sum_expr.add(Money(5, "USD"))  # (5 USD + 10 CHF) + 5 USD
    result = bank.reduce(sum_expr, "USD")  # should reduce to 15 USD
    assert result == Money(15, "USD")

# US-4: Exchanging currencies
def test_convert_francs_to_dollars():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)
    amount = Money(2, "CHF")
    result = bank.reduce(amount, "USD")  # 2 CHF = 1 USD
    assert result == Money(1, "USD")

def test_convert_francs_to_dollars_truncate():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)
    amount = Money(5, "CHF")
    result = bank.reduce(amount, "USD")  # 5 CHF = 2 USD (truncating)
    assert result == Money(2, "USD")

def test_reduce_with_no_exchange_rate():
    amount = Money(5, "CHF")
    bank = Bank()  # Fresh bank with no rates
    with pytest.raises(Exception) as excinfo:
        bank.reduce(amount, "USD")  # No rate registered
    assert "CHF->USD" in str(excinfo.value)