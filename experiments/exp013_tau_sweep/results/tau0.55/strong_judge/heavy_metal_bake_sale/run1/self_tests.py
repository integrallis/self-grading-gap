import pytest
from solution import quote_order, take_payment, get_stock, initialize_stock

@pytest.fixture(autouse=True)
def setup_stock():
    initialize_stock({"B": 48, "M": 36, "C": 24, "W": 30})

def test_quote_order_with_single_item():
    # B totals $0.75
    assert quote_order("B") == "$0.75"

def test_quote_order_with_multiple_items():
    # B, C, M totals $3.10
    assert quote_order("B, C, M") == "$3.10"

def test_quote_order_with_whitespace():
    # B, C, W totals $3.60, whitespace ignored
    assert quote_order(" B , C , W ") == "$3.60"

def test_quote_order_with_repeated_items():
    # B, B, M totals $2.50
    assert quote_order("B, B, M") == "$2.50"

def test_quote_order_with_no_items():
    # No items totals $0.00
    assert quote_order("") == "$0.00"

def test_quote_order_with_invalid_item_code():
    # Invalid item code 'X' should raise an error
    with pytest.raises(ValueError, match="Invalid item code: X"):
        quote_order("B, X")

def test_take_payment_exact_amount():
    # Paying $3.60 for $3.60 order returns $0.00 
    assert take_payment("B, C, W", 3.60) == "$0.00"

def test_take_payment_over_amount():
    # Paying $4.00 for $3.60 order returns $0.40
    assert take_payment("B, C, W", 4.00) == "$0.40"

def test_take_payment_under_amount():
    # Paying $3.00 for $3.60 order should be refused
    assert take_payment("B, C, W", 3.00) == "Not enough money"

def test_take_payment_does_not_change_stock_on_refusal():
    # Check stock remains unchanged after refusal
    assert take_payment("B, C, W", 3.00) == "Not enough money"
    assert get_stock("B") == 48  # Stock should still be 48 Brownies
    assert get_stock("C") == 24  # Stock should still be 24 Cake Pops
    assert get_stock("W") == 30  # Stock should still be 30 Waters

def test_take_payment_changes_stock_on_successful_payment():
    # Successful payment reduces stock
    take_payment("B, C, W", 3.60)  # Successful payment
    assert get_stock("B") == 47  # One less Brownie
    assert get_stock("C") == 23  # One less Cake Pop
    assert get_stock("W") == 29  # One less Water

def test_stock_initialization_with_default_values():
    # Default stock values
    assert get_stock("B") == 48
    assert get_stock("M") == 36
    assert get_stock("C") == 24
    assert get_stock("W") == 30

def test_stock_custom_initialization():
    # Custom stock initialization
    initialize_stock({"B": 10, "M": 5, "C": 0, "W": 2})  # Custom values
    assert get_stock("B") == 10
    assert get_stock("M") == 5
    assert get_stock("C") == 0  # No Cake Pops
    assert get_stock("W") == 2

def test_order_more_than_stock():
    # Ordering more than available stock for B
    initialize_stock({"B": 1})
    with pytest.raises(ValueError, match="Brownie is out of stock"):
        quote_order("B, B")  # Should be out of stock for second Brownie

def test_order_omitted_item_from_inventory():
    # Omitted item 'M' from inventory should be out of stock
    initialize_stock({"B": 1})
    with pytest.raises(ValueError, match="Muffin is out of stock"):
        quote_order("M")

def test_selling_last_item():
    # Selling the last unit of an item makes the next order for it out of stock
    initialize_stock({"B": 1})
    quote_order("B")  # Quoting one Brownie
    take_payment("B", 0.75)  # Paying for it
    with pytest.raises(ValueError, match="Brownie is out of stock"):
        quote_order("B")  # Next order for Brownie should fail

def test_quote_order_with_c_m():
    # C, M totals $2.35
    assert quote_order("C, M") == "$2.35"

def test_order_out_of_stock_during_payment():
    initialize_stock({"B": 0})
    assert take_payment("B", 0.75) == "Brownie is out of stock"