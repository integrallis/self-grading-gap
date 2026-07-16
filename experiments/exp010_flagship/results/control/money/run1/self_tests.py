from solution import Money, Bank, Sum

def test_multiplying_dollars():
    # 5 dollars times 2 equals 10 dollars.
    five_dollars = Money(5, "USD")
    result = five_dollars.multiply(2)
    assert result == Money(10, "USD")

def test_multiplying_francs():
    # 5 francs times 2 equals 10 francs.
    five_francs = Money(5, "CHF")
    result = five_francs.multiply(2)
    assert result == Money(10, "CHF")
    
    # 5 francs times 3 equals 15 francs.
    result = five_francs.multiply(3)
    assert result == Money(15, "CHF")

def test_original_amount_unchanged():
    # After being multiplied, 5 dollars still equals 5 dollars.
    five_dollars = Money(5, "USD")
    five_dollars.multiply(2)
    assert five_dollars == Money(5, "USD")

def test_equal_amounts():
    # Two amounts with the same quantity and the same currency are equal.
    assert Money(5, "USD") == Money(5, "USD")

def test_not_equal_different_quantities():
    # Two amounts in the same currency with different quantities are not equal.
    assert Money(5, "USD") != Money(10, "USD")

def test_not_equal_different_currencies():
    # Two amounts with the same quantity but different currencies are not equal.
    assert Money(5, "USD") != Money(5, "CHF")

def test_currency_code():
    # Dollar amounts report "USD".
    assert Money(5, "USD").currency() == "USD"
    # Franc amounts report "CHF".
    assert Money(5, "CHF").currency() == "CHF"

def test_adding_same_currency():
    # 5 dollars plus 5 dollars reduces to 10 dollars.
    five_dollars = Money(5, "USD")
    result = five_dollars.add(Money(5, "USD"))
    assert result.reduce("USD") == Money(10, "USD")

def test_reducing_plain_amount():
    # Reducing a plain amount to its own currency yields an equal amount.
    assert Money(5, "USD").reduce("USD") == Money(5, "USD")

def test_adding_different_currencies():
    # 5 dollars plus 10 francs, plus another 5 dollars reduces to 15 dollars 
    # when 2 francs exchange for 1 dollar.
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)
    sum_expression = Sum(Money(5, "USD"), Money(10, "CHF"))
    result = sum_expression.reduce(bank, "USD")
    assert result == Money(15, "USD")

def test_multiplying_sum_expression():
    # The sum of 5 dollars and 10 francs, times 2, reduces to 20 dollars at the same rate.
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)
    sum_expression = Sum(Money(5, "USD"), Money(10, "CHF"))
    result = sum_expression.multiply(2).reduce(bank, "USD")
    assert result == Money(20, "USD")

def test_registering_exchange_rate():
    # With a rate of 2 from francs to dollars, 2 francs reduce to 1 dollar.
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)
    result = Money(2, "CHF").reduce(bank, "USD")
    assert result == Money(1, "USD")

def test_converting_amounts():
    # At the 2-to-1 franc-to-dollar rate, 5 francs reduce to 2 dollars.
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)
    result = Money(5, "CHF").reduce(bank, "USD")
    assert result == Money(2, "USD")

def test_no_registered_rate_error():
    # Reducing to a different currency with no registered rate fails.
    bank = Bank()
    try:
        Money(5, "CHF").reduce(bank, "USD")
    except ValueError as e:
        assert str(e) == "USD->CHF"