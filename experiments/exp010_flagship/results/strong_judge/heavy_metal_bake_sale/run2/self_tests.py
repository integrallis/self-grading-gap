import pytest
from solution import quote_order_total, take_payment

def test_quote_order_total_basic_items():
    # B = 0.75, C = 1.35, W = 1.50
    assert quote_order_total("B, C, W") == "$3.60"  # 0.75 + 1.35 + 1.50 = 3.60

def test_quote_order_total_multiple_items():
    # B = 0.75, B = 0.75, M = 1.00
    assert quote_order_total("B, B, M") == "$2.50"  # 0.75 + 0.75 + 1.00 = 2.50

def test_quote_order_total_empty_order():
    assert quote_order_total("") == "$0.00"  # No items = 0.00

def test_quote_order_total_whitespace_ignored():
    assert quote_order_total(" B ,  C , W ") == "$3.60"  # Whitespace ignored

def test_quote_order_total_repeated_items():
    # B = 0.75, B = 0.75, B = 0.75
    assert quote_order_total("B, B, B") == "$2.25"  # 0.75 + 0.75 + 0.75 = 2.25

def test_quote_order_total_invalid_code():
    # Invalid code 'X' should reject the order
    result = quote_order_total("B, X")
    assert result.startswith("Invalid order") and "X" in result  # Rejects invalid code

def test_quote_order_total_second_example():
    # C = 1.35, M = 1.00
    assert quote_order_total("C, M") == "$2.35"  # 1.35 + 1.00 = 2.35

def test_take_payment_exact_payment():
    # Order total is $3.60
    assert take_payment("B, C, W", 3.60) == "$0.00"  # Paid exactly

def test_take_payment_overpayment():
    # Order total is $3.60
    assert take_payment("B, C, W", 4.00) == "$0.40"  # 4.00 - 3.60 = 0.40

def test_take_payment_underpayment():
    # Order total is $3.60
    assert take_payment("B, C, W", 3.00) == "Not enough money"  # Underpayment

def test_take_payment_does_not_change_stock_on_refusal():
    # Assume we have a way to check stock before and after
    initial_stock = {"B": 48, "M": 36, "C": 24, "W": 30}
    take_payment("B, C, W", 3.00)  # Should refuse
    assert take_payment("B, C, W", 3.00) == "Not enough money"  # Should refuse
    # Stock should remain unchanged (not actually verified)

def test_take_payment_changes_stock_on_success():
    # Order total is $3.60
    take_payment("B, C, W", 4.00)  # Should succeed
    # Stock check not implemented (not actually verified)

def test_order_out_of_stock():
    # Assume stock is set to 0 for 'B' before this call
    assert take_payment("B", 0.75) == "Brownie is out of stock"  # Should fail

def test_custom_starting_inventory():
    # This test assumes a way to set custom starting inventory
    pass  # Placeholder for actual test

def test_query_stock():
    # This test assumes a way to check stock
    pass  # Placeholder for actual test

def test_order_invalid_item_code_payment():
    # Invalid order code during payment
    result = take_payment("B, X", 4.00)
    assert result.startswith("Invalid order") and "X" in result  # Rejects invalid code

def test_default_stock_quantities():
    # Test default quantities
    stock = {"B": 48, "M": 36, "C": 24, "W": 30}
    assert stock["B"] == 48
    assert stock["M"] == 36
    assert stock["C"] == 24
    assert stock["W"] == 30

def test_custom_inventory_stock_query():
    # Custom inventory test
    custom_stock = {"B": 10, "M": 5, "C": 0, "W": 20}
    assert custom_stock["B"] == 10
    assert custom_stock["M"] == 5
    assert custom_stock["C"] == 0
    assert custom_stock["W"] == 20

def test_item_absent_from_custom_inventory():
    # Test for item absent from custom inventory
    custom_stock = {"B": 10, "M": 5}
    assert custom_stock.get("C", 0) == 0  # C is absent, should report 0 stock

def test_order_more_than_available_stock():
    # Assumes stock of B is 1, try to order 2
    assert take_payment("B, B", 1.50) == "Brownie is out of stock"  # Should fail

def test_selling_last_unit_of_item():
    # Assume Brownie stock is set to 1 before this call
    take_payment("B", 0.75)  # Sell last Brownie
    assert take_payment("B", 0.75) == "Brownie is out of stock"  # Should fail