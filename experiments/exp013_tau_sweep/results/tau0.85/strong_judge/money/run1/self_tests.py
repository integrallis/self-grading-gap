# test_money.py

import pytest
from solution import Money, Bank

def test_multiplying_dollars():
    amount = Money(5, "USD")  # 5 dollars
    result = amount.multiply(2)  # 5 dollars times 2
    assert result == Money(10, "USD")  # Expecting 10 dollars

def test_multiplying_francs():
    amount = Money(5, "CHF")  # 5 francs
    result = amount.multiply(2)  # 5 francs times 2
    assert result == Money(10, "CHF")  # Expecting 10 francs

def test_multiplying_francs_three_times():
    amount = Money(5, "CHF")  # 5 francs
    result = amount.multiply(3)  # 5 francs times 3
    assert result == Money(15, "CHF")  # Expecting 15 francs

def test_multiplying_does_not_alter_original_dollars():
    amount = Money(5, "USD")  # 5 dollars
    _ = amount.multiply(2)  # Multiply but do not store
    assert amount == Money(5, "USD")  # Original should still be 5 dollars

def test_multiplying_does_not_alter_original_francs():
    amount = Money(5, "CHF")  # 5 francs
    _ = amount.multiply(2)  # Multiply but do not store
    assert amount == Money(5, "CHF")  # Original should still be 5 francs

def test_equal_amounts_same_currency():
    amount1 = Money(5, "USD")  # 5 dollars
    amount2 = Money(5, "USD")  # 5 dollars
    assert amount1 == amount2  # They should be equal

def test_not_equal_amounts_different_quantities():
    amount1 = Money(5, "USD")  # 5 dollars
    amount2 = Money(6, "USD")  # 6 dollars
    assert amount1 != amount2  # They should not be equal

def test_not_equal_amounts_different_currencies():
    amount1 = Money(5, "USD")  # 5 dollars
    amount2 = Money(5, "CHF")  # 5 francs
    assert amount1 != amount2  # They should not be equal

def test_currency_code_for_dollars():
    amount = Money(5, "USD")  # 5 dollars
    assert amount.currency() == "USD"  # Should report "USD"

def test_currency_code_for_francs():
    amount = Money(5, "CHF")  # 5 francs
    assert amount.currency() == "CHF"  # Should report "CHF"

def test_adding_same_currency():
    amount1 = Money(5, "USD")  # 5 dollars
    amount2 = Money(5, "USD")  # 5 dollars
    bank = Bank()
    result = bank.reduce(amount1.add(amount2), "USD")  # 5 dollars plus 5 dollars
    assert result == Money(10, "USD")  # Should reduce to 10 dollars

def test_reducing_same_currency():
    amount = Money(5, "USD")  # 5 dollars
    bank = Bank()
    result = bank.reduce(amount, "USD")  # Reduce to USD
    assert result == Money(5, "USD")  # Should yield equal amount

def test_adding_different_currencies():
    amount1 = Money(5, "USD")  # 5 dollars
    amount2 = Money(10, "CHF")  # 10 francs
    bank = Bank()
    bank.add_exchange_rate("CHF", "USD", 2)  # 2 francs to 1 dollar
    result = bank.reduce(amount1.add(amount2), "USD")  # Add and reduce
    assert result == Money(15, "USD")  # Should reduce to 15 dollars

def test_adding_with_multiplication():
    amount1 = Money(5, "USD")  # 5 dollars
    amount2 = Money(10, "CHF")  # 10 francs
    bank = Bank()
    bank.add_exchange_rate("CHF", "USD", 2)  # 2 francs to 1 dollar
    result = bank.reduce(amount1.add(amount2).multiply(2), "USD")  # Multiply sum
    assert result == Money(20, "USD")  # Should reduce to 20 dollars

def test_register_exchange_rate():
    bank = Bank()
    bank.add_exchange_rate("CHF", "USD", 2)  # Register rate
    result = bank.reduce(Money(2, "CHF"), "USD")  # Reduce 2 francs
    assert result == Money(1, "USD")  # Should reduce to 1 dollar

def test_reduce_with_conversion():
    bank = Bank()
    bank.add_exchange_rate("CHF", "USD", 2)  # 2 francs to 1 dollar
    result = bank.reduce(Money(5, "CHF"), "USD")  # Reduce 5 francs
    assert result == Money(2, "USD")  # 5 francs should reduce to 2 dollars

def test_reduce_with_no_registered_rate():
    bank = Bank()
    with pytest.raises(Exception) as exc_info:  # Require exception
        bank.reduce(Money(5, "CHF"), "USD")  # Reduce with no rate
    assert str(exc_info.value) == "USD->CHF"  # Expecting error message for missing rate

def test_adding_extended_expression():
    amount1 = Money(5, "USD")  # 5 dollars
    amount2 = Money(10, "CHF")  # 10 francs
    bank = Bank()
    bank.add_exchange_rate("CHF", "USD", 2)  # 2 francs to 1 dollar
    result = bank.reduce(amount1.add(amount2).add(Money(5, "USD")), "USD")  # Add and reduce
    assert result == Money(15, "USD")  # Should reduce to 15 dollars