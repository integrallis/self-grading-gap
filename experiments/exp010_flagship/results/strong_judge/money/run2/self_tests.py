import pytest
from solution import Money, Bank

def test_scaling_dollars():
    amount = Money(5, 'USD')
    scaled_amount = amount.times(2)  # 5 dollars * 2 = 10 dollars
    assert scaled_amount == Money(10, 'USD')
    assert amount == Money(5, 'USD')  # Original amount remains unchanged

def test_scaling_francs():
    amount = Money(5, 'CHF')
    scaled_amount1 = amount.times(2)  # 5 francs * 2 = 10 francs
    scaled_amount2 = amount.times(3)  # 5 francs * 3 = 15 francs
    assert scaled_amount1 == Money(10, 'CHF')
    assert scaled_amount2 == Money(15, 'CHF')
    assert amount == Money(5, 'CHF')  # Original amount remains unchanged

def test_comparing_equal_dollars():
    amount1 = Money(5, 'USD')
    amount2 = Money(5, 'USD')
    assert amount1 == amount2  # Same quantity and currency

def test_comparing_different_quantities_dollars():
    amount1 = Money(5, 'USD')
    amount2 = Money(6, 'USD')
    assert amount1 != amount2  # Same currency, different quantities

def test_comparing_different_currencies():
    amount1 = Money(5, 'USD')
    amount2 = Money(5, 'CHF')
    assert amount1 != amount2  # Same quantity, different currencies

def test_currency_code_dollars():
    amount = Money(5, 'USD')
    assert amount.currency() == 'USD'  # Currency code should be USD

def test_currency_code_francs():
    amount = Money(5, 'CHF')
    assert amount.currency() == 'CHF'  # Currency code should be CHF

def test_adding_same_currency():
    bank = Bank()
    amount1 = Money(5, 'USD')
    amount2 = Money(5, 'USD')
    sum_amount = amount1.plus(amount2)  # 5 dollars + 5 dollars = 10 dollars
    reduced_amount = bank.reduce(sum_amount, 'USD')  # Should reduce to USD
    assert reduced_amount == Money(10, 'USD')

def test_reducing_same_currency():
    bank = Bank()
    amount = Money(5, 'USD')
    reduced_amount = bank.reduce(amount, 'USD')  # Reducing to its own currency
    assert reduced_amount == Money(5, 'USD')

def test_adding_different_currencies():
    bank = Bank()
    bank.add_exchange_rate('CHF', 'USD', 2)  # 2 CHF = 1 USD
    amount1 = Money(5, 'USD')
    amount2 = Money(10, 'CHF')
    sum_amount = amount1.plus(amount2)  # 5 dollars + 10 francs
    reduced_amount = bank.reduce(sum_amount, 'USD')  # Should reduce to USD
    assert reduced_amount == Money(10, 'USD')  # (5 + 5) dollars after conversion

def test_multiplying_sum_before_reduction():
    bank = Bank()
    bank.add_exchange_rate('CHF', 'USD', 2)  # 2 CHF = 1 USD
    amount1 = Money(5, 'USD')
    amount2 = Money(10, 'CHF')
    sum_amount = amount1.plus(amount2)  # 5 dollars + 10 francs
    scaled_sum = sum_amount.times(2)  # (5 + 5) dollars after conversion
    reduced_amount = bank.reduce(scaled_sum, 'USD')  # Should reduce to USD
    assert reduced_amount == Money(20, 'USD')  # (10 + 10) dollars after conversion

def test_converting_currency():
    bank = Bank()
    bank.add_exchange_rate('CHF', 'USD', 2)  # 2 CHF = 1 USD
    amount = Money(5, 'CHF')
    reduced_amount = bank.reduce(amount, 'USD')  # Should reduce to USD
    assert reduced_amount == Money(2, 'USD')  # 5 CHF reduces to 2 USD

def test_converting_currency_no_rate():
    bank = Bank()
    amount = Money(5, 'CHF')
    with pytest.raises(Exception) as excinfo:
        bank.reduce(amount, 'USD')  # Should raise an error with no exchange rate
    assert str(excinfo.value) == 'USD->CHF'  # Error message should indicate the missing rate

def test_truncating_conversion():
    bank = Bank()
    bank.add_exchange_rate('CHF', 'USD', 2)  # 2 CHF = 1 USD
    amount = Money(5, 'CHF')
    reduced_amount = bank.reduce(amount, 'USD')  # Should reduce to USD
    assert reduced_amount == Money(2, 'USD')  # 5 CHF reduces to 2 USD

def test_adding_and_extending_sum():
    bank = Bank()
    bank.add_exchange_rate('CHF', 'USD', 2)  # 2 CHF = 1 USD
    amount1 = Money(5, 'USD')
    amount2 = Money(10, 'CHF')
    sum_amount = amount1.plus(amount2)  # 5 dollars + 10 francs
    sum_amount = sum_amount.plus(Money(5, 'USD'))  # Extend with another 5 dollars
    reduced_amount = bank.reduce(sum_amount, 'USD')  # Should reduce to USD
    assert reduced_amount == Money(15, 'USD')  # (5 + 5 + 5) dollars after conversion

def test_registering_exchange_rate_direction():
    bank = Bank()
    bank.add_exchange_rate('CHF', 'USD', 2)  # Register CHF->USD
    with pytest.raises(Exception) as excinfo:
        bank.reduce(Money(5, 'USD'), 'CHF')  # Should raise an error for USD->CHF
    assert str(excinfo.value) == 'CHF->USD'  # Error message should indicate the missing rate