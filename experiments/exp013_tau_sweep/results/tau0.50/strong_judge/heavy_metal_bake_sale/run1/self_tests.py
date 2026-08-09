# your complete test file
import pytest
from solution import quote_order, pay_for_order, get_stock

# Fixture to reset stock before each test
@pytest.fixture(autouse=True)
def reset_stock():
    # Reset stock to default values
    # This would be where you could initialize or reset your stock
    pass

def test_quote_order_empty():
    assert quote_order("") == "$0.00"  # No items total to $0.00

def test_quote_order_single_item():
    assert quote_order("B") == "$0.75"  # Brownie: $0.75
    assert quote_order("M") == "$1.00"  # Muffin: $1.00
    assert quote_order("C") == "$1.35"  # Cake Pop: $1.35
    assert quote_order("W") == "$1.50"  # Water: $1.50

def test_quote_order_multiple_items():
    assert quote_order("B, C, W") == "$3.60"  # Brownie + Cake Pop + Water: $0.75 + $1.35 + $1.50 = $3.60
    assert quote_order("C, M") == "$2.35"  # Cake Pop + Muffin: $1.35 + $1.00 = $2.35
    assert quote_order("B, B, M") == "$2.50"  # Brownie + Brownie + Muffin: $0.75 + $0.75 + $1.00 = $2.50

def test_quote_order_whitespace():
    assert quote_order(" B , C ,  W ") == "$3.60"  # Whitespace is ignored

def test_quote_order_invalid_code():
    with pytest.raises(Exception) as excinfo:
        quote_order("X")
    assert str(excinfo.value) == "Invalid item code: X"  # Invalid code should raise an error naming the code

def test_pay_for_order_exact_payment():
    assert pay_for_order("B", 0.75) == "$0.00"  # Paying exactly returns $0.00

def test_pay_for_order_overpayment():
    assert pay_for_order("C, M", 4.00) == "$1.65"  # Paying $4.00 for $2.35 returns $1.65

def test_pay_for_order_underpayment():
    with pytest.raises(Exception) as excinfo:
        pay_for_order("C, M", 1.00)
    assert str(excinfo.value) == "Not enough money"  # Underpayment should raise an error

def test_pay_for_order_stock():
    pay_for_order("B", 0.75)  # Successful payment
    assert get_stock("B") == 47  # Should have 47 Brownies left

def test_pay_for_order_refusal_does_not_change_stock():
    initial_stock = get_stock("B")
    with pytest.raises(Exception):
        pay_for_order("B", 0.50)  # Should raise an error
    assert get_stock("B") == initial_stock  # Stock remains the same

def test_stock_initialization():
    assert get_stock("B") == 48  # Initial stock should be 48 Brownies
    assert get_stock("M") == 36  # Initial stock should be 36 Muffins
    assert get_stock("C") == 24  # Initial stock should be 24 Cake Pops
    assert get_stock("W") == 30  # Initial stock should be 30 Waters

def test_stock_out_of_stock():
    for _ in range(30):
        pay_for_order("W", 1.50)  # Reduces stock
    with pytest.raises(Exception) as excinfo:
        pay_for_order("W", 1.50)  # Should raise an error
    assert str(excinfo.value) == "Water is out of stock"  # Out of stock should raise error

def test_stock_invalid_item():
    with pytest.raises(Exception) as excinfo:
        quote_order("X")
    assert str(excinfo.value) == "Invalid item code: X"  # Invalid code should raise an error

def test_quote_order_does_not_change_stock():
    initial_stock = get_stock("B")
    quote_order("B, C")
    assert get_stock("B") == initial_stock  # Stock remains unchanged

def test_pay_for_order_successful_multiple_items():
    pay_for_order("B, M", 1.75)  # Buy 1 Brownie and 1 Muffin
    assert get_stock("B") == 47  # Should have 47 Brownies left
    assert get_stock("M") == 35  # Should have 35 Muffins left

def test_pay_for_order_successful_repeated_items():
    pay_for_order("B, B", 1.50)  # Buy 2 Brownies
    assert get_stock("B") == 46  # Should have 46 Brownies left

def test_order_more_than_stock():
    # Set up situation with only 1 Brownie left
    pay_for_order("B", 0.75)  # Buy 1 Brownie
    with pytest.raises(Exception) as excinfo:
        quote_order("B, B")  # Should raise an error
    assert str(excinfo.value) == "Brownie is out of stock"  # Out of stock should raise error

def test_order_last_item():
    # Set up situation with only 1 Muffin left
    pay_for_order("M", 1.00)  # Buy 1 Muffin
    with pytest.raises(Exception) as excinfo:
        pay_for_order("M", 1.00)  # Should raise an error
    assert str(excinfo.value) == "Muffin is out of stock"  # Out of stock should raise error

def test_unknown_code_in_order():
    with pytest.raises(Exception) as excinfo:
        quote_order("B, X")
    assert str(excinfo.value) == "Invalid item code: X"  # Invalid code should raise an error