# your complete test file

import pytest
from solution import Money, Bank

# US-1: Scaling amounts

def test_multiplying_dollars():
    amount = Money(5, "USD")
    result = amount.multiply(2)
    expected = Money(10, "USD")  # 5 * 2 = 10
    assert result == expected

def test_multiplying_francs():
    amount = Money(5, "CHF")
    result = amount.multiply(2)
    expected = Money(10, "CHF")  # 5 * 2 = 10
    assert result == expected

def test_multiplying_francs_three_times():
    amount = Money(5, "CHF")
    result = amount.multiply(3)
    expected = Money(15, "CHF")  # 5 * 3 = 15
    assert result == expected

def test_original_amount_unchanged():
    amount = Money(5, "USD")
    amount.multiply(2)
    expected = Money(5, "USD")  # Original amount should still be 5
    assert amount == expected

# US-2: Comparing amounts

def test_equal_amounts():
    amount1 = Money(5, "USD")
    amount2 = Money(5, "USD")
    assert amount1 == amount2  # Same quantity and currency

def test_not_equal_different_quantities():
    amount1 = Money(5, "USD")
    amount2 = Money(10, "USD")
    assert amount1 != amount2  # Same currency, different quantities

def test_not_equal_different_currencies():
    amount1 = Money(5, "USD")
    amount2 = Money(5, "CHF")
    assert amount1 != amount2  # Same quantity, different currencies

def test_currency_code_usd():
    amount = Money(5, "USD")
    assert amount.currency() == "USD"  # Should report currency code

def test_currency_code_chf():
    amount = Money(5, "CHF")
    assert amount.currency() == "CHF"  # Should report currency code

# US-3: Adding and reducing expressions

def test_adding_same_currency():
    bank = Bank()
    amount1 = Money(5, "USD")
    amount2 = Money(5, "USD")
    result = amount1.add(amount2)
    expected = Money(10, "USD")  # 5 + 5 = 10
    assert bank.reduce(result, "USD") == expected

def test_reducing_plain_amount():
    bank = Bank()
    amount = Money(5, "USD")
    result = bank.reduce(amount, "USD")
    expected = Money(5, "USD")  # Reducing to its own currency
    assert result == expected

def test_adding_different_currencies():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # 2 CHF = 1 USD
    amount1 = Money(5, "USD")
    amount2 = Money(10, "CHF")
    result = amount1.add(amount2)
    expected = Money(10, "USD")  # 5 + (10 / 2) = 10
    assert bank.reduce(result, "USD") == expected

def test_adding_three_terms():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # 2 CHF = 1 USD
    amount1 = Money(5, "USD")
    amount2 = Money(10, "CHF")
    amount3 = Money(5, "USD")
    result = amount1.add(amount2).add(amount3)  # (5 + (10 / 2) + 5)
    expected = Money(15, "USD")  # 5 + 5 + (10 / 2) = 15
    assert bank.reduce(result, "USD") == expected

def test_multiplying_sum_before_reduction():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # 2 CHF = 1 USD
    amount1 = Money(5, "USD")
    amount2 = Money(10, "CHF")
    sum_amount = amount1.add(amount2)
    result = sum_amount.multiply(2)
    expected = Money(20, "USD")  # (5 + (10 / 2)) * 2 = 20
    assert bank.reduce(result, "USD") == expected

# US-4: Exchanging currencies

def test_registering_exchange_rate():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # 2 CHF = 1 USD
    # No direct assertion on rates as per specification

def test_converting_currency():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # 2 CHF = 1 USD
    amount = Money(5, "CHF")
    result = bank.reduce(amount, "USD")
    expected = Money(2, "USD")  # 5 / 2 = 2
    assert result == expected

def test_conversion_without_registered_rate():
    bank = Bank()
    amount = Money(5, "CHF")
    with pytest.raises(Exception) as excinfo:
        bank.reduce(amount, "USD")  # No registered rate for CHF to USD
    assert str(excinfo.value) == "CHF->USD"

def test_reducing_to_ordered_currency():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # 2 CHF = 1 USD
    with pytest.raises(Exception) as excinfo:
        bank.reduce(Money(1, "USD"), "CHF")  # USD to CHF should fail
    assert str(excinfo.value) == "USD->CHF"

def test_non_example_conversion():
    bank = Bank()
    bank.add_rate("EUR", "GBP", 3)  # 3 EUR = 1 GBP
    amount = Money(7, "EUR")
    result = bank.reduce(amount, "GBP")
    expected = Money(2, "GBP")  # 7 / 3 = 2 (truncated)
    assert result == expected