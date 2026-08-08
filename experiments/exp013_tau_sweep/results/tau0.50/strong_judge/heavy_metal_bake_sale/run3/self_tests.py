from solution import quote_order_total, take_payment, get_stock

def test_quote_order_total_with_single_item():
    # B (Brownie) costs $0.75
    assert quote_order_total("B") == "$0.75"

def test_quote_order_total_with_multiple_items():
    # B (Brownie) $0.75 + C (Cake Pop) $1.35 + W (Water) $1.50 = $3.60
    assert quote_order_total("B, C, W") == "$3.60"

def test_quote_order_total_with_whitespace():
    # C (Cake Pop) $1.35 + M (Muffin) $1.00 = $2.35
    assert quote_order_total(" C , M ") == "$2.35"

def test_quote_order_total_with_repeated_items():
    # B (Brownie) $0.75 + B (Brownie) $0.75 + M (Muffin) $1.00 = $2.50
    assert quote_order_total("B, B, M") == "$2.50"

def test_quote_order_total_with_no_items():
    # No items = $0.00
    assert quote_order_total("") == "$0.00"

def test_quote_order_total_does_not_affect_stock():
    # Stock before quoting
    initial_stock_B = get_stock("B")
    quote_order_total("B, C, W")
    # Stock should remain unchanged
    assert get_stock("B") == initial_stock_B

def test_take_payment_exact_amount():
    # Order total $3.60, paid $3.60 = change $0.00
    assert take_payment("B, C, W", 3.60) == "$0.00"

def test_take_payment_over_amount():
    # Order total $3.60, paid $4.00 = change $0.40
    assert take_payment("B, C, W", 4.00) == "$0.40"

def test_take_payment_under_amount():
    # Order total $3.60, paid $3.00 = "Not enough money"
    assert take_payment("B, C, W", 3.00) == "Not enough money"

def test_take_payment_does_not_affect_stock_on_refusal():
    # Record initial stock for Brownies before refusal
    initial_stock_B = get_stock("B")
    take_payment("B, C, W", 3.00)  # This should be refused
    assert get_stock("B") == initial_stock_B  # stock remains unchanged

def test_take_payment_affects_stock_on_success():
    # Order total $2.50 (B, B, M), paid $2.50 = change $0.00
    take_payment("B, B, M", 2.50)
    assert get_stock("B") == 46  # stock decreases by 2 for Brownies
    assert get_stock("M") == 35  # stock decreases by 1 for Muffins
    assert get_stock("C") == 24  # stock unchanged for Cake Pops
    assert get_stock("W") == 30  # stock unchanged for Waters

def test_stock_initialization():
    # Default stock should be Brownies: 48, Muffins: 36, Cake Pops: 24, Waters: 30
    assert get_stock("B") == 48
    assert get_stock("M") == 36
    assert get_stock("C") == 24
    assert get_stock("W") == 30

def test_order_more_than_stock():
    # Custom inventory with 3 Brownies, requesting 4 should fail
    assert take_payment("B, B, B, B", 3.00) == "Brownie is out of stock"

def test_order_exceeding_available_stock():
    # Ordering more items than available stock
    assert quote_order_total("B, B, B, B") == "Brownie is out of stock"  # Expecting refusal due to stock

def test_ordering_unknown_item_code():
    # Invalid item code "X" should return a rejection
    result = quote_order_total("B, X")
    assert "X" in result  # Check that the message contains the unknown code

def test_order_item_out_of_stock():
    # Create initial stock with no Water
    assert get_stock("W") == 0
    assert quote_order_total("W") == "Water is out of stock"

def test_selling_last_unit():
    # Create initial stock, sell the last Cake Pop, then try to quote it
    take_payment("C", 1.35)  # Successful sale
    assert quote_order_total("C") == "Cake Pop is out of stock"