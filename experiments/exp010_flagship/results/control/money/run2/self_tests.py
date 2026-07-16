import pytest
from solution import Money, Bank, Sum

# US-1: Scaling amounts

def test_multiply_dollars():
    five_dollars = Money(5, "USD")
    assert five_dollars * 2 == Money(10, "USD")  # 5 * 2 = 10

def test_multiply_francs():
    five_francs = Money(5, "CHF")
    assert five_francs * 2 == Money(10, "CHF")  # 5 * 2 = 10
    assert five_francs * 3 == Money(15, "CHF")  # 5 * 3 = 15

def test_original_amount_unchanged():
    five_dollars = Money(5, "USD")
    _ = five_dollars * 2
    assert five_dollars == Money(5, "USD")  # Original remains unchanged

# US-2: Comparing amounts

def test_equal_amounts():
    assert Money(5, "USD") == Money(5, "USD")  # Same quantity and currency

def test_not_equal_different_quantities():
    assert Money(5, "USD") != Money(6, "USD")  # Same currency, different quantities

def test_not_equal_different_currencies():
    assert Money(5, "USD") != Money(5, "CHF")  # Same quantity, different currencies

def test_currency_code():
    assert Money(5, "USD").currency() == "USD"  # Dollar currency code
    assert Money(5, "CHF").currency() == "CHF"  # Franc currency code

# US-3: Adding and reducing expressions

def test_add_same_currency():
    sum_amounts = Money(5, "USD") + Money(5, "USD")
    assert sum_amounts.reduce("USD") == Money(10, "USD")  # 5 + 5 = 10

def test_reduce_plain_amount():
    five_dollars = Money(5, "USD")
    assert five_dollars.reduce("USD") == Money(5, "USD")  # No conversion needed

def test_add_and_reduce_mixed_currencies():
    sum_amounts = Money(5, "USD") + Money(10, "CHF")
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # 2 francs = 1 dollar
    assert sum_amounts.reduce(bank, "USD") == Money(15, "USD")  # 5 USD + 10 CHF -> 15 USD

def test_multiply_sum_before_reduction():
    sum_amounts = Money(5, "USD") + Money(10, "CHF")
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)
    multiplied_sum = sum_amounts * 2  # 2 * (5 USD + 10 CHF)
    assert multiplied_sum.reduce(bank, "USD") == Money(30, "USD")  # Reduces to 30 USD

# US-4: Exchanging currencies

def test_register_exchange_rate():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # 2 CHF = 1 USD
    assert bank.rates["CHF"]["USD"] == 2  # Check registered rate

def test_reduce_with_registered_rate():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)
    five_francs = Money(5, "CHF")
    assert five_francs.reduce(bank, "USD") == Money(2, "USD")  # 5 CHF reduces to 2 USD

def test_reduce_with_no_registered_rate():
    bank = Bank()
    with pytest.raises(ValueError) as excinfo:
        Money(5, "CHF").reduce(bank, "USD")  # No rate registered
    assert str(excinfo.value) == "USD->CHF"  # Expected error message