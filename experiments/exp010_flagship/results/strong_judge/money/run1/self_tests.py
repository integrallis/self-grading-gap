from solution import Money, Bank

def test_scaling_dollars():
    five_dollars = Money(5, "USD")
    ten_dollars = five_dollars.multiply(2)  # 5 * 2 = 10
    assert ten_dollars == Money(10, "USD")
    assert five_dollars == Money(5, "USD")  # original amount remains unchanged

def test_scaling_francs():
    five_francs = Money(5, "CHF")
    ten_francs = five_francs.multiply(2)  # 5 * 2 = 10
    fifteen_francs = five_francs.multiply(3)  # 5 * 3 = 15
    assert ten_francs == Money(10, "CHF")
    assert fifteen_francs == Money(15, "CHF")
    assert five_francs == Money(5, "CHF")  # original amount remains unchanged

def test_comparing_equal_amounts():
    five_dollars_a = Money(5, "USD")
    five_dollars_b = Money(5, "USD")
    assert five_dollars_a == five_dollars_b  # same quantity and currency

def test_comparing_different_quantities():
    five_dollars = Money(5, "USD")
    ten_dollars = Money(10, "USD")
    assert five_dollars != ten_dollars  # same currency, different quantities

def test_comparing_different_currencies():
    five_dollars = Money(5, "USD")
    five_francs = Money(5, "CHF")
    assert five_dollars != five_francs  # same quantity, different currencies

def test_currency_code():
    five_dollars = Money(5, "USD")
    five_francs = Money(5, "CHF")
    assert five_dollars.currency() == "USD"  # currency code for dollars
    assert five_francs.currency() == "CHF"  # currency code for francs

def test_adding_same_currency():
    five_dollars_a = Money(5, "USD")
    five_dollars_b = Money(5, "USD")
    sum_amount = five_dollars_a.add(five_dollars_b)  # 5 + 5 = 10
    reduced_amount = Bank().reduce(sum_amount, "USD")  # reduce to USD
    assert reduced_amount == Money(10, "USD")  # expect 10 USD after reduction

def test_reducing_same_currency():
    five_dollars = Money(5, "USD")
    bank = Bank()
    reduced_amount = bank.reduce(five_dollars, "USD")  # no conversion, same currency
    assert reduced_amount == Money(5, "USD")

def test_adding_mixed_currencies():
    five_dollars = Money(5, "USD")
    ten_francs = Money(10, "CHF")
    bank = Bank()
    bank.add_exchange_rate("CHF", "USD", 2)  # 2 francs to 1 dollar
    sum_amount = five_dollars.add(ten_francs)  # 5 + (10 // 2) = 10
    reduced_amount = bank.reduce(sum_amount, "USD")
    assert reduced_amount == Money(10, "USD")

def test_scaling_sum_before_reduction():
    five_dollars = Money(5, "USD")
    ten_francs = Money(10, "CHF")
    bank = Bank()
    bank.add_exchange_rate("CHF", "USD", 2)  # 2 francs to 1 dollar
    sum_amount = five_dollars.add(ten_francs)  # 5 + (10 // 2) = 10
    scaled_amount = sum_amount.multiply(2)  # 10 * 2 = 20
    reduced_amount = bank.reduce(scaled_amount, "USD")
    assert reduced_amount == Money(20, "USD")

def test_registering_exchange_rate():
    bank = Bank()
    bank.add_exchange_rate("CHF", "USD", 2)  # 2 francs to 1 dollar
    reduced_amount = bank.reduce(Money(2, "CHF"), "USD")  # 2 // 2 = 1
    assert reduced_amount == Money(1, "USD")

def test_reducing_without_registered_rate():
    bank = Bank()
    try:
        bank.reduce(Money(1, "CHF"), "USD")  # no registered rate for CHF->USD
    except Exception as e:  # catch the unspecified error type
        assert str(e) == "USD->CHF"  # should raise error with the correct message

def test_adding_extended_mixed_sum():
    five_dollars = Money(5, "USD")
    ten_francs = Money(10, "CHF")
    bank = Bank()
    bank.add_exchange_rate("CHF", "USD", 2)  # 2 francs to 1 dollar
    sum_amount = five_dollars.add(ten_francs).add(Money(5, "USD"))  # 5 + (10 // 2) + 5 = 15
    reduced_amount = bank.reduce(sum_amount, "USD")
    assert reduced_amount == Money(15, "USD")

def test_truncating_exchange():
    bank = Bank()
    bank.add_exchange_rate("CHF", "USD", 2)  # 2 francs to 1 dollar
    reduced_amount = bank.reduce(Money(5, "CHF"), "USD")  # 5 // 2 = 2
    assert reduced_amount == Money(2, "USD")