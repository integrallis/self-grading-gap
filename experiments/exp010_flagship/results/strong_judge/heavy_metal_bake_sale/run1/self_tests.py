from solution import quote_order, pay_for_order

def test_quote_order_brownie():
    order = "B"
    # Total for 1 Brownie ($0.75)
    expected = "$0.75"
    assert quote_order(order) == expected

def test_quote_order_muffin():
    order = "M"
    # Total for 1 Muffin ($1.00)
    expected = "$1.00"
    assert quote_order(order) == expected

def test_quote_order_cake_pop():
    order = "C"
    # Total for 1 Cake Pop ($1.35)
    expected = "$1.35"
    assert quote_order(order) == expected

def test_quote_order_water():
    order = "W"
    # Total for 1 Water ($1.50)
    expected = "$1.50"
    assert quote_order(order) == expected

def test_quote_order_multiple_items():
    order = "B, C, W"
    # Total: $0.75 + $1.35 + $1.50 = $3.60
    expected = "$3.60"
    assert quote_order(order) == expected

def test_quote_order_with_whitespace():
    order = " B , C , W "
    # Total: $0.75 + $1.35 + $1.50 = $3.60
    expected = "$3.60"
    assert quote_order(order) == expected

def test_quote_order_repeated_items():
    order = "B, B, M"
    # Total: $0.75 + $0.75 + $1.00 = $2.50
    expected = "$2.50"
    assert quote_order(order) == expected

def test_quote_order_empty():
    order = ""
    # Total for no items = $0.00
    expected = "$0.00"
    assert quote_order(order) == expected

def test_quote_order_invalid_item():
    order = "X"
    # Invalid code 'X'
    result = quote_order(order)
    assert "X" in result  # Check if the result mentions the invalid code

def test_quote_order_invalid_item_in_multiple_items():
    order = "B, C, X"
    result = quote_order(order)
    assert "X" in result  # Check if the result mentions the invalid code

def test_pay_for_order_exact_payment():
    order = "B, C"
    payment = 2.10
    # Total: $0.75 + $1.35 = $2.10; Change: $0.00
    assert pay_for_order(order, payment) == "$0.00"

def test_pay_for_order_overpayment():
    order = "B, C"
    payment = 3.00
    # Total: $0.75 + $1.35 = $2.10; Change: $3.00 - $2.10 = $0.90
    assert pay_for_order(order, payment) == "$0.90"

def test_pay_for_order_underpayment():
    order = "B, C"
    payment = 1.50
    # Total: $0.75 + $1.35 = $2.10; Not enough money
    expected = "Not enough money"
    assert pay_for_order(order, payment) == expected

def test_pay_for_order_invalid_item():
    order = "B, X"
    payment = 2.10
    # Invalid item code 'X'; payment is refused
    result = pay_for_order(order, payment)
    assert "X" in result  # Check if the result mentions the invalid code

def test_pay_for_order_out_of_stock():
    order = ",".join(["B"] * 49)  # Requesting more than stock
    payment = 36.75  # Total should be more than $36.75
    expected = "Brownie is out of stock"
    assert pay_for_order(order, payment) == expected

def test_quote_order_out_of_stock():
    order = ",".join(["W"] * 31)  # Requesting more Waters than in stock
    expected = "Water is out of stock"
    assert quote_order(order) == expected

def test_order_stock_tracking():
    order = "B"
    payment = 0.75
    pay_for_order(order, payment)  # Complete the sale
    stock_after_sale = quote_order("B")  # Quoting again to check for stock change
    # After one Brownie sold, stock should still be $0.75; no stock change on quote
    expected = "$0.75"  
    assert stock_after_sale == expected

def test_order_with_invalid_item():
    order = "B, C, X"
    result = quote_order(order)
    assert "X" in result  # Check if the result mentions the invalid code

def test_custom_inventory():
    # Assume there is a function to create a checkout with custom inventory
    from solution import create_checkout
    checkout = create_checkout({"B": 2, "M": 0, "C": 0, "W": 1})  # Custom inventory
    order = "M"  # Muffin has 0 stock
    result = quote_order(order)
    assert "Muffin is out of stock" in result  # Check if the result mentions out of stock
    
    order = "B"  # Should succeed
    payment = 0.75
    assert pay_for_order(order, payment) == "$0.00"  # Completes sale, reduces stock

def test_selling_last_item():
    order = "W"  # Sell the last Water
    payment = 1.50
    assert pay_for_order(order, payment) == "$0.00"  # Completes sale
    order = "W"  # Next order for Water should fail
    expected = "Water is out of stock"
    result = quote_order(order)
    assert expected in result  # Check if the result mentions out of stock

def test_inventory_initial_state():
    from solution import create_checkout
    checkout = create_checkout()  # Default inventory
    order = "B"
    assert pay_for_order(order, 0.75) == "$0.00"  # Should succeed
    order = "B"  # Next order for Brownie should also succeed
    assert pay_for_order(order, 0.75) == "$0.00"  # Should succeed
    order = "B"  # Next order for Brownie should also succeed
    assert pay_for_order(order, 0.75) == "$0.00"  # Should succeed
    order = "B"  # Next order for Brownie should also succeed
    assert pay_for_order(order, 0.75) == "$0.00"  # Should succeed
    order = "B"  # Next order for Brownie should also succeed
    assert pay_for_order(order, 0.75) == "$0.00"  # Should succeed
    order = "B"  # Next order for Brownie should be out of stock
    assert quote_order(order) == "Brownie is out of stock"

def test_inventory_query():
    from solution import create_checkout
    checkout = create_checkout()  # Default inventory
    assert quote_order("B") == "$0.75"  # Should confirm stock is available
    assert quote_order("M") == "$1.00"  # Should confirm stock is available
    assert quote_order("C") == "$1.35"  # Should confirm stock is available
    assert quote_order("W") == "$1.50"  # Should confirm stock is available