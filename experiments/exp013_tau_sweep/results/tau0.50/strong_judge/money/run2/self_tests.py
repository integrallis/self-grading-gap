from solution import Money, Bank

def test_multiply_dollars():
    amount = Money(5, "USD")
    result = amount.multiply(2)  # 5 dollars times 2 equals 10 dollars
    assert result == Money(10, "USD")

def test_multiply_francs():
    amount = Money(5, "CHF")
    result = amount.multiply(2)  # 5 francs times 2 equals 10 francs
    assert result == Money(10, "CHF")
    
    result = amount.multiply(3)  # 5 francs times 3 equals 15 francs
    assert result == Money(15, "CHF")

def test_multiply_does_not_alter_original():
    amount = Money(5, "USD")
    amount.multiply(2)  # multiplying should not alter the original
    assert amount == Money(5, "USD")

def test_equal_amounts_same_currency():
    amount1 = Money(5, "USD")
    amount2 = Money(5, "USD")
    assert amount1 == amount2  # same quantity and currency

def test_not_equal_different_quantities():
    amount1 = Money(5, "USD")
    amount2 = Money(6, "USD")
    assert amount1 != amount2  # same currency, different quantities

def test_not_equal_different_currencies():
    amount1 = Money(5, "USD")
    amount2 = Money(5, "CHF")
    assert amount1 != amount2  # same quantity, different currencies

def test_currency_code():
    amount = Money(5, "USD")
    assert amount.currency() == "USD"  # dollar amounts report "USD"

    amount = Money(5, "CHF")
    assert amount.currency() == "CHF"  # franc amounts report "CHF"

def test_add_same_currency():
    amount1 = Money(5, "USD")
    amount2 = Money(5, "USD")
    expression = amount1.add(amount2)  # 5 dollars plus 5 dollars
    bank = Bank()
    reduced = bank.reduce(expression, "USD")  # reduces to 10 dollars
    assert reduced == Money(10, "USD")

def test_reduce_plain_amount():
    amount = Money(5, "USD")
    bank = Bank()
    result = bank.reduce(amount, "USD")  # reducing to its own currency
    assert result == Money(5, "USD")  # equal amount, no exchange rate needed

def test_add_mixed_currencies():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # with a rate of 2 from francs to dollars

    amount1 = Money(5, "USD")
    amount2 = Money(10, "CHF")
    amount3 = Money(5, "USD")
    expression = amount1.add(amount2).add(amount3)  # 5 dollars plus 10 francs plus another 5 dollars
    reduced = bank.reduce(expression, "USD")  # reduces to 15 dollars
    assert reduced == Money(15, "USD")

def test_multiply_sum_before_reduction():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # with a rate of 2 from francs to dollars

    amount1 = Money(5, "USD")
    amount2 = Money(10, "CHF")
    sum_expression = amount1.add(amount2)  # sum of 5 dollars and 10 francs
    result = sum_expression.multiply(2)  # multiplied by factor 2
    reduced = bank.reduce(result, "USD")  # reduces to 20 dollars
    assert reduced == Money(20, "USD")

def test_reduce_with_registered_rate():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # with a rate of 2 from francs to dollars

    amount = Money(5, "CHF")
    reduced = bank.reduce(amount, "USD")  # reducing 5 francs to dollars
    assert reduced == Money(2, "USD")  # 5 francs reduce to 2 dollars

def test_reduce_with_no_registered_rate():
    bank = Bank()
    amount = Money(5, "CHF")
    try:
        bank.reduce(amount, "USD")  # trying to reduce without a registered rate
        assert False, "Expected an error but none was raised"
    except Exception as e:
        assert str(e) == "USD->CHF"  # should raise an error with the correct message