from solution import Money, Bank

def test_multiplying_dollars():
    amount = Money(5, 'USD')
    result = amount.multiply(2)  # 5 dollars * 2 = 10 dollars
    assert result == Money(10, 'USD')

def test_multiplying_francs():
    amount = Money(5, 'CHF')
    result = amount.multiply(2)  # 5 francs * 2 = 10 francs
    assert result == Money(10, 'CHF')

def test_multiplying_francs_three_times():
    amount = Money(5, 'CHF')
    result = amount.multiply(3)  # 5 francs * 3 = 15 francs
    assert result == Money(15, 'CHF')

def test_original_amount_unchanged_dollars():
    amount = Money(5, 'USD')
    amount.multiply(2)
    assert amount == Money(5, 'USD')  # Original amount remains unchanged

def test_original_amount_unchanged_francs():
    amount = Money(5, 'CHF')
    amount.multiply(2)
    assert amount == Money(5, 'CHF')  # Original amount remains unchanged

def test_equal_amounts_same_currency():
    amount1 = Money(5, 'USD')
    amount2 = Money(5, 'USD')
    assert amount1 == amount2  # 5 dollars == 5 dollars

def test_not_equal_amounts_same_currency_different_values():
    amount1 = Money(5, 'USD')
    amount2 = Money(10, 'USD')
    assert amount1 != amount2  # 5 dollars != 10 dollars

def test_not_equal_amounts_different_currencies():
    amount1 = Money(5, 'USD')
    amount2 = Money(5, 'CHF')
    assert amount1 != amount2  # 5 dollars != 5 francs

def test_currency_code_dollars():
    amount = Money(5, 'USD')
    assert amount.currency() == 'USD'  # Currency code should be 'USD'

def test_currency_code_francs():
    amount = Money(5, 'CHF')
    assert amount.currency() == 'CHF'  # Currency code should be 'CHF'

def test_adding_same_currency():
    bank = Bank()
    amount1 = Money(5, 'USD')
    amount2 = Money(5, 'USD')
    sum_expression = amount1.add(amount2)  # 5 dollars + 5 dollars
    result = bank.reduce(sum_expression, 'USD')  # Bank reduces it
    assert result == Money(10, 'USD')  # Should equal 10 dollars

def test_reduction_same_currency():
    bank = Bank()
    amount = Money(5, 'USD')
    result = bank.reduce(amount, 'USD')  # Reducing to its own currency
    assert result == Money(5, 'USD')  # Should equal 5 dollars

def test_adding_different_currencies():
    bank = Bank()
    bank.add_rate('CHF', 'USD', 2)  # Register rate 2 CHF = 1 USD
    amount1 = Money(5, 'USD')
    amount2 = Money(10, 'CHF')
    sum_expression = amount1.add(amount2)  # 5 dollars + 10 francs
    result = bank.reduce(sum_expression, 'USD')  # Reduce through bank
    assert result == Money(10, 'USD')  # 10 USD total after reduction

def test_multiplying_sum_expression():
    bank = Bank()
    bank.add_rate('CHF', 'USD', 2)  # Register rate 2 CHF = 1 USD
    amount1 = Money(5, 'USD')
    amount2 = Money(10, 'CHF')
    sum_expression = amount1.add(amount2)  # 5 dollars + 10 francs
    scaled_expression = sum_expression.multiply(2)  # Scale expression by 2
    result = bank.reduce(scaled_expression, 'USD')  # Reduce through bank
    assert result == Money(20, 'USD')  # Should equal 20 dollars

def test_register_exchange_rate():
    bank = Bank()
    bank.add_rate('CHF', 'USD', 2)  # 2 francs = 1 dollar

def test_reduction_with_registered_rate():
    bank = Bank()
    bank.add_rate('CHF', 'USD', 2)
    amount = Money(2, 'CHF')
    result = bank.reduce(amount, 'USD')  # 2 CHF should reduce to 1 USD
    assert result == Money(1, 'USD')  # Should equal 1 dollar

def test_reduction_with_no_registered_rate():
    bank = Bank()
    amount = Money(5, 'CHF')
    try:
        bank.reduce(amount, 'USD')  # Should raise an error
        assert False  # If we reach this line, the test should fail
    except Exception as e:
        assert str(e) == 'CHF->USD'  # Error message should match the requested conversion

def test_extending_mixed_currency_sum():
    bank = Bank()
    bank.add_rate('CHF', 'USD', 2)  # Register rate 2 CHF = 1 USD
    amount1 = Money(5, 'USD')
    amount2 = Money(10, 'CHF')
    sum_expression = amount1.add(amount2).add(Money(5, 'USD'))  # 5 USD + 10 CHF + 5 USD
    result = bank.reduce(sum_expression, 'USD')  # Reduce through bank
    assert result == Money(15, 'USD')  # Should equal 15 dollars

def test_truncating_conversion():
    bank = Bank()
    bank.add_rate('CHF', 'USD', 2)  # Register rate 2 CHF = 1 USD
    amount = Money(5, 'CHF')
    result = bank.reduce(amount, 'USD')  # 5 CHF should reduce to 2 USD
    assert result == Money(2, 'USD')  # Should equal 2 dollars