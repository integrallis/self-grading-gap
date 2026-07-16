from solution import quote_order, take_payment, remaining_stock, StockError

def test_quote_order_empty():
    assert quote_order("") == "$0.00"  # No items, total is $0.00

def test_quote_order_brownie():
    assert quote_order("B") == "$0.75"  # B = $0.75

def test_quote_order_muffin():
    assert quote_order("M") == "$1.00"  # M = $1.00

def test_quote_order_cake_pop():
    assert quote_order("C") == "$1.35"  # C = $1.35

def test_quote_order_water():
    assert quote_order("W") == "$1.50"  # W = $1.50

def test_quote_order_multiple_items():
    assert quote_order("B,C,W") == "$3.60"  # B + C + W = $0.75 + $1.35 + $1.50 = $3.60

def test_quote_order_multiple_same_items():
    assert quote_order("B,B,M") == "$2.50"  # B + B + M = $0.75 + $0.75 + $1.00 = $2.50

def test_quote_order_ignore_whitespace():
    assert quote_order(" B , C , W ") == "$3.60"  # Whitespace ignored, same as above

def test_quote_order_invalid_item_code():
    try:
        quote_order("X")
    except StockError as e:
        assert str(e) == "Invalid item code: X"  # Invalid code should raise an error

def test_take_payment_exact():
    quote_order("B,M")
    assert take_payment("$1.75") == "$0.00"  # Paying exactly the total

def test_take_payment_overpay():
    quote_order("C,W")
    assert take_payment("$3.00") == "$0.30"  # Paying $3.00, change = $0.30

def test_take_payment_underpay():
    quote_order("C,M")
    try:
        take_payment("$2.00")
    except StockError as e:
        assert str(e) == "Not enough money"  # Paying less should raise an error

def test_take_payment_refused_does_not_consume_stock():
    quote_order("B,C")
    try:
        take_payment("$1.00")
    except StockError:
        pass
    assert remaining_stock() == {"B": 48, "M": 36, "C": 24, "W": 30}  # Stock should remain unchanged

def test_remaining_stock_initial():
    assert remaining_stock() == {"B": 48, "M": 36, "C": 24, "W": 30}  # Default stock values

def test_order_out_of_stock():
    quote_order("B")
    take_payment("$0.75")
    try:
        quote_order("B")
    except StockError as e:
        assert str(e) == "Brownie is out of stock"  # After selling last, should be out of stock

def test_remaining_stock_after_sale():
    quote_order("M")
    take_payment("$1.00")
    assert remaining_stock() == {"B": 48, "M": 35, "C": 24, "W": 30}  # Stock should decrease after sale

def test_order_invalid_item_code():
    try:
        quote_order("B,X")
    except StockError as e:
        assert str(e) == "Invalid item code: X"  # Invalid item code should raise an error

def test_order_greater_than_stock():
    try:
        quote_order("B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B")
    except StockError as e:
        assert str(e) == "Brownie is out of stock"  # Trying to order more than stock should raise an error