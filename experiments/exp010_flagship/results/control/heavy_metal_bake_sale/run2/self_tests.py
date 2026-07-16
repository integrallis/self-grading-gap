# test_bake_sale_checkout.py

from solution import quote_order, take_payment, check_stock

def test_quote_order_empty():
    assert quote_order("") == "$0.00"  # No items total $0.00

def test_quote_order_single_item():
    assert quote_order("B") == "$0.75"  # Brownie $0.75
    assert quote_order("M") == "$1.00"  # Muffin $1.00
    assert quote_order("C") == "$1.35"  # Cake Pop $1.35
    assert quote_order("W") == "$1.50"  # Water $1.50

def test_quote_order_multiple_items():
    assert quote_order("B, C, W") == "$3.60"  # $0.75 + $1.35 + $1.50 = $3.60
    assert quote_order("C, M") == "$2.35"  # $1.35 + $1.00 = $2.35
    assert quote_order("B, B, M") == "$2.50"  # $0.75 + $0.75 + $1.00 = $2.50

def test_quote_order_whitespace():
    assert quote_order(" B , C , W ") == "$3.60"  # Whitespace ignored, same as above
    assert quote_order("  C  ,  M  ") == "$2.35"  # Whitespace ignored, same as above

def test_quote_order_invalid_code():
    assert quote_order("B, X") == "Invalid item code: X"  # X is not a valid code
    assert quote_order("A") == "Invalid item code: A"  # A is not a valid code

def test_take_payment_exact_total():
    assert take_payment("B", 0.75) == "$0.00"  # Paying exactly the total returns $0.00

def test_take_payment_overpay():
    assert take_payment("B, C", 2.00) == "$0.25"  # Total is $2.10, change is $0.25

def test_take_payment_underpay():
    assert take_payment("C, M", 1.00) == "Not enough money"  # Total is $2.35, not enough money

def test_take_payment_no_stock():
    # Assuming default stock is available
    assert take_payment("B, B, M", 2.50) == "$0.00"  # Pay for the items, should be fine

def test_track_stock_default():
    assert check_stock() == {"B": 48, "M": 36, "C": 24, "W": 30}  # Check default stock values

def test_stock_refusal():
    assert take_payment("W, W, W, W", 6.00) == "Water is out of stock"  # If we sell last Water, next order is rejected

def test_order_more_than_stock():
    assert take_payment("B, B, B, B", 3.00) == "Brownie is out of stock"  # If we sold all Brownies, next order is rejected
    assert take_payment("C, C, C, C", 5.00) == "Cake Pop is out of stock"  # If we sold all Cake Pops, next order is rejected

def test_order_missing_item():
    assert quote_order("B, W, Z") == "Invalid item code: Z"  # Z is not a valid code