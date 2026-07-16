from solution import quote_order, take_payment, get_stock

def test_quote_order_basic():
    assert quote_order("B, C, W") == "$3.60"  # $0.75 + $1.35 + $1.50
    assert quote_order("C, M") == "$2.35"     # $1.35 + $1.00

def test_quote_order_with_whitespace():
    assert quote_order(" B , C , W ") == "$3.60"  # $0.75 + $1.35 + $1.50
    assert quote_order(" C , M ") == "$2.35"      # $1.35 + $1.00

def test_quote_order_with_repeated_items():
    assert quote_order("B, B, M") == "$2.50"  # $0.75 + $0.75 + $1.00
    assert quote_order("C, C, W") == "$4.20"  # $1.35 + $1.35 + $1.50

def test_quote_order_empty():
    assert quote_order("") == "$0.00"  # No items

def test_quote_order_stock_untouched():
    quote_order("B, C, W")
    assert get_stock("B") == 48  # Stock remains unchanged
    assert get_stock("C") == 24
    assert get_stock("W") == 30

def test_take_payment_exact_payment():
    assert quote_order("B, C, W") == "$3.60"  # $0.75 + $1.35 + $1.50
    assert take_payment(3.60, "B, C, W") == "$0.00"  # Paid exactly $3.60

def test_take_payment_overpayment():
    assert quote_order("B, C, W") == "$3.60"  # $0.75 + $1.35 + $1.50
    assert take_payment(4.00, "B, C, W") == "$0.40"  # Paid $4.00 for $3.60
    assert take_payment(4.00, "C, M") == "$1.65"      # Paid $4.00 for $2.35

def test_take_payment_underpayment():
    assert quote_order("B, C, W") == "$3.60"  # $0.75 + $1.35 + $1.50
    assert take_payment(3.00, "B, C, W") == "Not enough money"  # Paid less than total

def test_take_payment_no_stock_changes_on_refusal():
    quote_order("B, C, W")
    take_payment(3.00, "B, C, W")  # Refusal
    assert get_stock("B") == 48  # Stock remains unchanged
    assert get_stock("C") == 24
    assert get_stock("W") == 30

def test_take_payment_stock_changes_on_success():
    quote_order("B, C, W")
    take_payment(4.00, "B, C, W")  # Successful payment
    assert get_stock("B") == 47  # Stock decremented
    assert get_stock("C") == 23
    assert get_stock("W") == 29

def test_quote_order_item_out_of_stock():
    assert quote_order(",".join(["B"] * 49)) == "Brownie is out of stock"  # 49 Brownies ordered

def test_take_payment_item_out_of_stock():
    quote_order(",".join(["B"] * 49))  # 49 Brownies ordered
    assert take_payment(30.00, ",".join(["B"] * 49)) == "Brownie is out of stock"  # Trying to pay for unavailable stock

def test_quote_order_invalid_item_code():
    assert quote_order("B, X") == "X is an invalid item code"  # Invalid item code

def test_take_payment_invalid_item_code():
    assert take_payment(4.00, "B, X") == "X is an invalid item code"  # Invalid item code

def test_stock_initialization():
    assert get_stock("B") == 48  # Default stock
    assert get_stock("M") == 36
    assert get_stock("C") == 24
    assert get_stock("W") == 30

def test_custom_starting_inventory_no_item():
    assert get_stock("W") == 0  # Item absent has zero stock
    assert quote_order("W") == "Water is out of stock"  # Order for missing item

def test_last_unit_scenario():
    # Custom inventory with one Brownie
    assert get_stock("B") == 1  # 1 Brownie available
    assert take_payment(0.75, "B") == "$0.00"  # Successful payment
    assert quote_order("B") == "Brownie is out of stock"  # Next order for Brownie should be out of stock