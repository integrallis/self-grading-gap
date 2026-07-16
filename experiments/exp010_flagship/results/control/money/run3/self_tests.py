# test_money.py

from solution import Money, Bank

def test_scaling_dollars():
    amount = Money(5, "USD")
    scaled_amount = amount.times(2)  # 5 dollars * 2 = 10 dollars
    assert scaled_amount == Money(10, "USD")
    assert amount == Money(5, "USD")  # original amount remains unchanged

def test_scaling_francs():
    amount = Money(5, "CHF")
    scaled_amount_2 = amount.times(2)  # 5 francs * 2 = 10 francs
    assert scaled_amount_2 == Money(10, "CHF")
    scaled_amount_3 = amount.times(3)  # 5 francs * 3 = 15 francs
    assert scaled_amount_3 == Money(15, "CHF")
    assert amount == Money(5, "CHF")  # original amount remains unchanged

def test_equal_amounts_same_currency():
    amount1 = Money(5, "USD")
    amount2 = Money(5, "USD")
    assert amount1 == amount2  # 5 dollars == 5 dollars

def test_not_equal_different_quantities():
    amount1 = Money(5, "USD")
    amount2 = Money(6, "USD")
    assert amount1 != amount2  # 5 dollars != 6 dollars

def test_not_equal_different_currencies():
    amount1 = Money(5, "USD")
    amount2 = Money(5, "CHF")
    assert amount1 != amount2  # 5 dollars != 5 francs

def test_currency_code():
    amount_usd = Money(5, "USD")
    amount_chf = Money(5, "CHF")
    assert amount_usd.currency() == "USD"  # should return "USD"
    assert amount_chf.currency() == "CHF"  # should return "CHF"

def test_adding_same_currency():
    amount1 = Money(5, "USD")
    amount2 = Money(5, "USD")
    result = amount1.plus(amount2)  # 5 dollars + 5 dollars
    assert result == Money(10, "USD")  # should reduce to 10 dollars

def test_reducing_same_currency():
    amount = Money(5, "USD")
    reduced_amount = amount.reduce("USD")  # reducing to its own currency
    assert reduced_amount == Money(5, "USD")  # should return the same amount

def test_adding_different_currencies():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # 2 francs = 1 dollar
    amount1 = Money(5, "USD")
    amount2 = Money(10, "CHF")
    result = amount1.plus(amount2)  # 5 dollars + 10 francs
    reduced_amount = bank.reduce(result, "USD")  # should reduce to 15 dollars
    assert reduced_amount == Money(15, "USD")  # expected to reduce to 15 dollars

def test_multiplying_sum():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # 2 francs = 1 dollar
    amount1 = Money(5, "USD")
    amount2 = Money(10, "CHF")
    sum_expression = amount1.plus(amount2)  # 5 dollars + 10 francs
    scaled_expression = sum_expression.times(2)  # (5 dollars + 10 francs) * 2
    reduced_amount = bank.reduce(scaled_expression, "USD")  # should reduce to 30 dollars
    assert reduced_amount == Money(30, "USD")  # expected to reduce to 30 dollars

def test_registering_exchange_rate():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # register rate
    assert bank.rate("CHF", "USD") == 2  # should return the registered rate

def test_reducing_with_registered_rate():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # 2 francs = 1 dollar
    amount = Money(5, "CHF")
    reduced_amount = bank.reduce(amount, "USD")  # should reduce to 2 dollars
    assert reduced_amount == Money(2, "USD")  # expected to reduce to 2 dollars

def test_reducing_with_no_registered_rate():
    bank = Bank()
    amount = Money(5, "CHF")
    try:
        bank.reduce(amount, "USD")
    except ValueError as e:
        assert str(e) == "USD->CHF"  # should raise an error with the conversion pair