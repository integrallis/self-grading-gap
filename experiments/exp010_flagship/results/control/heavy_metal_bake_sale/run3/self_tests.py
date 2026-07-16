from solution import quote_order_total, take_payment, remaining_stock

def test_quote_order_total_brownie():
    assert quote_order_total("B") == "$0.75"  # B = $0.75

def test_quote_order_total_muffin():
    assert quote_order_total("M") == "$1.00"  # M = $1.00

def test_quote_order_total_cake_pop():
    assert quote_order_total("C") == "$1.35"  # C = $1.35

def test_quote_order_total_water():
    assert quote_order_total("W") == "$1.50"  # W = $1.50

def test_quote_order_total_multiple_items():
    assert quote_order_total("B, C, W") == "$3.60"  # B + C + W = $0.75 + $1.35 + $1.50 = $3.60

def test_quote_order_total_two_items():
    assert quote_order_total("C, M") == "$2.35"  # C + M = $1.35 + $1.00 = $2.35

def test_quote_order_total_repeated_items():
    assert quote_order_total("B, B, M") == "$2.50"  # B + B + M = $0.75 + $0.75 + $1.00 = $2.50

def test_quote_order_total_empty_order():
    assert quote_order_total("") == "$0.00"  # No items = $0.00

def test_quote_order_total_whitespace_ignored():
    assert quote_order_total(" B , C , W ") == "$3.60"  # Same as "B, C, W"

def test_take_payment_exact_total():
    assert take_payment("B, C", 3.60) == "$0.00"  # Paying $3.60 for $3.60 order

def test_take_payment_overpay():
    assert take_payment("B, C", 4.00) == "$0.40"  # Paying $4.00 for $3.60 order

def test_take_payment_underpay():
    assert take_payment("B, C", 3.00) == "Not enough money"  # Paying $3.00 for $3.60 order

def test_take_payment_does_not_affect_stock_on_refusal():
    initial_stock = remaining_stock()
    take_payment("B, C", 3.00)
    assert remaining_stock() == initial_stock  # Stock should remain unchanged

def test_take_payment_does_affect_stock_on_success():
    initial_stock = remaining_stock()
    take_payment("B, C", 3.60)
    assert remaining_stock()["B"] == initial_stock["B"] - 1  # Stock of B should decrease by 1
    assert remaining_stock()["C"] == initial_stock["C"] - 1  # Stock of C should decrease by 1

def test_stock_initialization_default():
    stock = remaining_stock()
    assert stock["B"] == 48  # Default stock of Brownies
    assert stock["M"] == 36  # Default stock of Muffins
    assert stock["C"] == 24  # Default stock of Cake Pops
    assert stock["W"] == 30  # Default stock of Waters

def test_out_of_stock_item():
    take_payment("W", 1.50)  # Sell last Water
    assert take_payment("W", 1.50) == "Water is out of stock"  # Next order for Water should be refused

def test_invalid_item_code():
    assert take_payment("X", 1.00) == "Invalid item code: X"  # Invalid item code should be rejected

def test_remaining_stock_for_custom_initialization():
    from solution import initialize_stock
    initialize_stock({"B": 10, "M": 5, "C": 0, "W": 2})  # Custom stock
    assert remaining_stock()["C"] == 0  # Custom stock for Cake Pops is 0
    assert take_payment("C", 1.35) == "Cake Pop is out of stock"  # Ordering Cake Pop should be refused

def test_unknown_item_code_in_order():
    assert quote_order_total("B, X") == "Invalid item code: X"  # Invalid item code should be rejected