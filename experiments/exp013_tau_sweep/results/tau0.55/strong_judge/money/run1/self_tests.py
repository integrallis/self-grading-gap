from solution import Money, Bank

def test_scaling_dollars():
    five_dollars = Money(5, "USD")
    ten_dollars = five_dollars.scale(2)  # 5 * 2 = 10
    assert ten_dollars == Money(10, "USD")

def test_scaling_francs():
    five_francs = Money(5, "CHF")
    ten_francs = five_francs.scale(2)  # 5 * 2 = 10
    assert ten_francs == Money(10, "CHF")
    fifteen_francs = five_francs.scale(3)  # 5 * 3 = 15
    assert fifteen_francs == Money(15, "CHF")

def test_original_amount_unchanged_dollars():
    five_dollars = Money(5, "USD")
    scaled_amount = five_dollars.scale(2)
    assert five_dollars == Money(5, "USD")  # Original should still be 5 dollars

def test_original_amount_unchanged_francs():
    five_francs = Money(5, "CHF")
    scaled_amount = five_francs.scale(2)
    assert five_francs == Money(5, "CHF")  # Original should still be 5 francs

def test_comparing_equal_dollars():
    five_dollars_1 = Money(5, "USD")
    five_dollars_2 = Money(5, "USD")
    assert five_dollars_1 == five_dollars_2  # Same quantity and currency

def test_comparing_different_dollars():
    five_dollars = Money(5, "USD")
    ten_dollars = Money(10, "USD")
    assert five_dollars != ten_dollars  # Different quantities

def test_comparing_equal_francs():
    five_francs_1 = Money(5, "CHF")
    five_francs_2 = Money(5, "CHF")
    assert five_francs_1 == five_francs_2  # Same quantity and currency

def test_comparing_different_francs():
    five_francs = Money(5, "CHF")
    ten_francs = Money(10, "CHF")
    assert five_francs != ten_francs  # Different quantities

def test_comparing_different_currencies():
    five_dollars = Money(5, "USD")
    five_francs = Money(5, "CHF")
    assert five_dollars != five_francs  # Different currencies

def test_currency_code_dollars():
    five_dollars = Money(5, "USD")
    assert five_dollars.currency() == "USD"  # Currency code should be USD

def test_currency_code_francs():
    five_francs = Money(5, "CHF")
    assert five_francs.currency() == "CHF"  # Currency code should be CHF

def test_adding_same_currency():
    five_dollars_1 = Money(5, "USD")
    five_dollars_2 = Money(5, "USD")
    sum_expression = five_dollars_1.add(five_dollars_2)
    reduced_amount = Bank().reduce(sum_expression, "USD")  # 5 + 5 = 10
    assert reduced_amount == Money(10, "USD")

def test_reducing_plain_amount_to_own_currency():
    five_dollars = Money(5, "USD")
    reduced_amount = Bank().reduce(five_dollars, "USD")  # Should be equal
    assert reduced_amount == Money(5, "USD")

def test_adding_mixed_currencies():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # Registering rate: 2 CHF = 1 USD
    five_dollars = Money(5, "USD")
    ten_francs = Money(10, "CHF")
    sum_expression = five_dollars.add(ten_francs)  # 5 USD + 10 CHF
    reduced_amount = bank.reduce(sum_expression, "USD")  # 5 + (10 // 2) = 5 + 5 = 10
    assert reduced_amount == Money(10, "USD")

def test_adding_and_scaling():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # Registering rate: 2 CHF = 1 USD
    five_dollars = Money(5, "USD")
    ten_francs = Money(10, "CHF")
    sum_expression = five_dollars.add(ten_francs)  # 5 USD + 10 CHF
    scaled_expression = sum_expression.scale(2)  # (5 + 5) * 2 = 20 USD
    reduced_amount = bank.reduce(scaled_expression, "USD")
    assert reduced_amount == Money(20, "USD")

def test_registering_exchange_rate():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # 2 CHF = 1 USD
    reduced_amount = bank.reduce(Money(2, "CHF"), "USD")  # 2 / 2 = 1
    assert reduced_amount == Money(1, "USD")

def test_converting_amount_using_rate():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # 2 CHF = 1 USD
    reduced_amount = bank.reduce(Money(5, "CHF"), "USD")  # 5 / 2 = 2
    assert reduced_amount == Money(2, "USD")

def test_failed_conversion_due_to_no_rate():
    bank = Bank()
    try:
        bank.reduce(Money(5, "CHF"), "USD")  # No rate registered
    except Exception as e:  # Catch any exception
        assert str(e) == "CHF->USD"  # Should raise error with the conversion pair
    else:
        assert False, "Expected an error due to missing exchange rate"

def test_extending_sum_before_reduction():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)  # Registering rate: 2 CHF = 1 USD
    five_dollars = Money(5, "USD")
    ten_francs = Money(10, "CHF")
    sum_expression = five_dollars.add(ten_francs).add(five_dollars)  # (5 USD + 10 CHF) + 5 USD
    reduced_amount = bank.reduce(sum_expression, "USD")  # (5 + 5) = 10 USD + 5 = 15 USD
    assert reduced_amount == Money(15, "USD")