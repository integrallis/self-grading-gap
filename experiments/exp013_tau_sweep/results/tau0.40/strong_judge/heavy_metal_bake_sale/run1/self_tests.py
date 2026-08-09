# test_bake_sale_checkout.py

import pytest
from solution import checkout

def test_quote_order_with_single_item():
    # Order: B -> $0.75
    assert checkout.quote_order("B") == "$0.75"

def test_quote_order_with_multiple_items():
    # Order: B, C, W -> $0.75 + $1.35 + $1.50 = $3.60
    assert checkout.quote_order("B, C, W") == "$3.60"

def test_quote_order_with_second_example():
    # Order: C, M -> $1.35 + $1.00 = $2.35
    assert checkout.quote_order("C, M") == "$2.35"

def test_quote_order_with_whitespace():
    # Order: B,  C, W -> $0.75 + $1.35 + $1.50 = $3.60
    assert checkout.quote_order("B,  C, W") == "$3.60"
    
    # Order: "  B  , C ,  W  " -> $0.75 + $1.35 + $1.50 = $3.60
    assert checkout.quote_order("  B  , C ,  W  ") == "$3.60"

def test_quote_order_with_repeated_items():
    # Order: B, B, M -> $0.75 + $0.75 + $1.00 = $2.50
    assert checkout.quote_order("B, B, M") == "$2.50"

def test_quote_order_with_no_items():
    # No items -> $0.00
    assert checkout.quote_order("") == "$0.00"

def test_quote_order_with_unknown_item():
    # Order: B, X -> should indicate invalidity and include X
    result = checkout.quote_order("B, X")
    assert "X" in result

def test_take_payment_exact_total():
    # Order total: $3.60, payment: $3.60 -> change: $0.00
    checkout.quote_order("B, C, W")  # Pre-check order
    assert checkout.take_payment("B, C, W", 3.60) == "$0.00"

def test_take_payment_overpaying():
    # Order total: $3.60, payment: $4.00 -> change: $0.40
    checkout.quote_order("B, C, W")  # Pre-check order
    assert checkout.take_payment("B, C, W", 4.00) == "$0.40"

def test_take_payment_underpaying():
    # Order total: $3.60, payment: $3.00 -> Not enough money
    checkout.quote_order("B, C, W")  # Pre-check order
    result = checkout.take_payment("B, C, W", 3.00)
    assert result == "Not enough money"

def test_take_payment_does_not_affect_stock_on_refusal():
    # Order total: $3.60, payment: $3.00 -> Not enough money
    checkout.quote_order("B, C, W")  # Pre-check order
    result = checkout.take_payment("B, C, W", 3.00)
    assert result == "Not enough money"
    # Stock should remain the same
    assert checkout.get_stock("B") == 48

def test_take_payment_completes_sale():
    # Order total: $3.60, payment: $4.00 -> stock should decrease
    checkout.quote_order("B, C, W")  # Pre-check order
    checkout.take_payment("B, C, W", 4.00)
    # Stock should decrease: B (47), C (23), W (29)
    assert checkout.get_stock("B") == 47
    assert checkout.get_stock("C") == 23
    assert checkout.get_stock("W") == 29

def test_stock_initialization():
    # Default stock: Brownies: 48, Muffins: 36, Cake Pops: 24, Waters: 30
    stock = checkout.get_stock()  # Assuming this returns the current stock
    assert stock["B"] == 48
    assert stock["M"] == 36
    assert stock["C"] == 24
    assert stock["W"] == 30

def test_stock_custom_initialization():
    # Custom stock: Brownies: 10, Muffins: 10, Cake Pops: 10, Waters: 10
    checkout = checkout.initialize(custom_stock={"B": 10, "M": 10, "C": 10, "W": 10})
    assert checkout.get_stock("B") == 10
    assert checkout.get_stock("M") == 10
    assert checkout.get_stock("C") == 10
    assert checkout.get_stock("W") == 10

def test_ordering_out_of_stock():
    # Order: W (1) -> first sale -> next order should fail
    checkout = checkout.initialize(custom_stock={"W": 1})
    checkout.quote_order("W")  # should succeed
    checkout.take_payment("W", 1.50)  # complete sale
    # Now ordering W again should be out of stock
    result = checkout.quote_order("W")
    assert result == "Water is out of stock"

def test_ordering_more_than_stock():
    # Custom stock: Muffins: 1
    checkout = checkout.initialize(custom_stock={"M": 1})
    result = checkout.quote_order("M, M")  # should fail
    assert result == "Muffin is out of stock"

def test_ordering_unknown_item_code():
    # Order: B, X -> should indicate invalidity and include X
    result = checkout.quote_order("B, X")
    assert "X" in result

def test_payment_path_out_of_stock():
    # Custom stock: Water: 0
    checkout = checkout.initialize(custom_stock={"W": 0})
    result = checkout.quote_order("W")  # should fail
    assert result == "Water is out of stock"
    payment_result = checkout.take_payment("W", 1.50)
    assert payment_result == "Water is out of stock"