import pytest
from solution import Checkout

def test_quote_order_total_single_item():
    checkout = Checkout()
    # B = $0.75
    assert checkout.quote_order_total("B") == "$0.75"

def test_quote_order_total_multiple_items():
    checkout = Checkout()
    # C = $1.35, M = $1.00
    assert checkout.quote_order_total("C, M") == "$2.35"

def test_quote_order_total_with_whitespace():
    checkout = Checkout()
    # B = $0.75, C = $1.35, W = $1.50
    assert checkout.quote_order_total(" B, C , W ") == "$3.60"

def test_quote_order_total_repeated_items():
    checkout = Checkout()
    # B = $0.75, B = $0.75, M = $1.00
    assert checkout.quote_order_total("B, B, M") == "$2.50"

def test_quote_order_total_empty_order():
    checkout = Checkout()
    # No items = $0.00
    assert checkout.quote_order_total("") == "$0.00"

def test_quote_order_total_no_stock_item():
    checkout = Checkout()
    # Should reject unknown item 'X'
    rejection_message = checkout.quote_order_total("B, X")
    assert "X" in rejection_message

def test_take_payment_exact_payment():
    checkout = Checkout()
    # Total is $2.35, payment is $2.35
    assert checkout.take_payment("C, M", 2.35) == "$0.00"

def test_take_payment_overpayment():
    checkout = Checkout()
    # Total is $2.35, payment is $4.00
    assert checkout.take_payment("C, M", 4.00) == "$1.65"  # change is $1.65

def test_take_payment_underpayment():
    checkout = Checkout()
    # Total is $2.35, payment is $2.00
    rejection_message = checkout.take_payment("C, M", 2.00)
    assert rejection_message == "Not enough money"

def test_take_payment_no_stock_item():
    checkout = Checkout()
    # Total is $2.35, payment is $4.00 for an order with out of stock item
    rejection_message = checkout.take_payment("B, X", 4.00)
    assert "X" in rejection_message

def test_take_payment_completed_sale_reduces_stock():
    checkout = Checkout()
    # Total is $2.35 for "C, M", after payment stock should reduce.
    checkout.take_payment("C, M", 2.35)
    assert checkout.get_stock("C") == 23  # 24 - 1
    assert checkout.get_stock("M") == 35  # 36 - 1

def test_track_stock_initial_values():
    checkout = Checkout()
    # Check initial stock values
    assert checkout.get_stock("B") == 48
    assert checkout.get_stock("M") == 36
    assert checkout.get_stock("C") == 24
    assert checkout.get_stock("W") == 30

def test_order_out_of_stock_item():
    checkout = Checkout()
    # Attempting to order more than available stock
    rejection_message = checkout.quote_order_total(",".join(["B"] * 49))  # 49 > 48
    assert rejection_message == "Brownie is out of stock"

def test_custom_starting_inventory():
    checkout = Checkout({"B": 10, "M": 5, "C": 0, "W": 0})
    # Check initial stock values
    assert checkout.get_stock("B") == 10
    assert checkout.get_stock("M") == 5
    assert checkout.get_stock("C") == 0
    assert checkout.get_stock("W") == 0

def test_order_item_not_in_inventory():
    checkout = Checkout({"B": 10})
    rejection_message = checkout.quote_order_total("C")
    assert "Cake Pop" in rejection_message

def test_successful_sale_reduces_stock():
    checkout = Checkout()
    checkout.take_payment("B", 0.75)
    assert checkout.get_stock("B") == 47  # 48 - 1

def test_selling_last_unit():
    checkout = Checkout({"B": 1})
    checkout.take_payment("B", 0.75)
    assert checkout.get_stock("B") == 0
    rejection_message = checkout.quote_order_total("B")
    assert rejection_message == "Brownie is out of stock"

def test_quote_order_total_no_stock_item_rejection_message():
    checkout = Checkout({"B": 0})
    rejection_message = checkout.quote_order_total("B")
    assert rejection_message == "Brownie is out of stock"

def test_take_payment_no_stock_item_rejection_message():
    checkout = Checkout({"B": 0})
    rejection_message = checkout.take_payment("B", 0.75)
    assert rejection_message == "Brownie is out of stock"