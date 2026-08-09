# your complete test file
import pytest
from solution import Money, Bank

# US-1: Scaling amounts
def test_multiplying_dollars():
    amount = Money(5, 'USD')  # 5 dollars
    result = amount.multiply(2)  # 5 dollars times 2
    assert result == Money(10, 'USD')  # 10 dollars

def test_multiplying_francs():
    amount = Money(5, 'CHF')  # 5 francs
    result = amount.multiply(2)  # 5 francs times 2
    assert result == Money(10, 'CHF')  # 10 francs

def test_multiplying_francs_third_factor():
    amount = Money(5, 'CHF')  # 5 francs
    result = amount.multiply(3)  # 5 francs times 3
    assert result == Money(15, 'CHF')  # 15 francs

def test_original_amount_untouched():
    amount = Money(5, 'USD')  # 5 dollars
    amount.multiply(2)  # multiply but do not use the result
    assert amount == Money(5, 'USD')  # still 5 dollars

# US-2: Comparing amounts
def test_equal_amounts_same_currency():
    amount1 = Money(5, 'USD')  # 5 dollars
    amount2 = Money(5, 'USD')  # 5 dollars
    assert amount1 == amount2  # equal amounts

def test_non_equal_amounts_same_currency_different_quantity():
    amount1 = Money(5, 'USD')  # 5 dollars
    amount2 = Money(10, 'USD')  # 10 dollars
    assert amount1 != amount2  # not equal amounts

def test_non_equal_amounts_different_currencies():
    amount1 = Money(5, 'USD')  # 5 dollars
    amount2 = Money(5, 'CHF')  # 5 francs
    assert amount1 != amount2  # not equal amounts

def test_currency_code_dollar():
    amount = Money(5, 'USD')  # 5 dollars
    assert amount.currency() == 'USD'  # currency code is 'USD'

def test_currency_code_franc():
    amount = Money(5, 'CHF')  # 5 francs
    assert amount.currency() == 'CHF'  # currency code is 'CHF'

# US-3: Adding and reducing expressions
def test_adding_same_currency():
    bank = Bank()
    amount1 = Money(5, 'USD')  # 5 dollars
    amount2 = Money(5, 'USD')  # 5 dollars
    result = amount1.add(amount2)  # add same currency
    assert bank.reduce(result, 'USD') == Money(10, 'USD')  # reduces to 10 dollars

def test_reducing_plain_amount_own_currency():
    bank = Bank()
    amount = Money(5, 'USD')  # 5 dollars
    assert bank.reduce(amount, 'USD') == Money(5, 'USD')  # equals 5 dollars

def test_adding_mixed_currencies():
    bank = Bank()
    bank.add_rate('CHF', 'USD', 2)  # 2 francs = 1 dollar
    amount1 = Money(5, 'USD')  # 5 dollars
    amount2 = Money(10, 'CHF')  # 10 francs
    amount3 = Money(5, 'USD')  # 5 dollars
    result = amount1.add(amount2).add(amount3)  # add mixed currencies
    assert bank.reduce(result, 'USD') == Money(15, 'USD')  # reduces to 15 dollars

def test_multiplying_sum_before_reduction():
    bank = Bank()
    bank.add_rate('CHF', 'USD', 2)  # 2 francs = 1 dollar
    amount1 = Money(5, 'USD')  # 5 dollars
    amount2 = Money(10, 'CHF')  # 10 francs
    sum_amount = amount1.add(amount2)  # sum of 5 dollars and 10 francs
    result = sum_amount.multiply(2)  # sum times 2
    assert bank.reduce(result, 'USD') == Money(20, 'USD')  # reduces to 20 dollars

# US-4: Exchanging currencies
def test_reducing_amount_with_registered_rate():
    bank = Bank()
    bank.add_rate('CHF', 'USD', 2)  # 2 francs = 1 dollar
    amount = Money(2, 'CHF')  # 2 francs
    assert bank.reduce(amount, 'USD') == Money(1, 'USD')  # reduces to 1 dollar

def test_reducing_amount_with_fraction_truncation():
    bank = Bank()
    bank.add_rate('CHF', 'USD', 2)  # 2 francs = 1 dollar
    amount = Money(5, 'CHF')  # 5 francs
    assert bank.reduce(amount, 'USD') == Money(2, 'USD')  # reduces to 2 dollars (truncated)

def test_reducing_without_registered_rate():
    bank = Bank()
    with pytest.raises(Exception) as excinfo:
        amount = Money(5, 'CHF')  # 5 francs
        bank.reduce(amount, 'USD')  # try to reduce to dollars
    assert str(excinfo.value) == 'USD->CHF'  # raises with error message