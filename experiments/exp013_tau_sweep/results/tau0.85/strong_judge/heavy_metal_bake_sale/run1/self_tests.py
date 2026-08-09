# your complete test file
from solution import quote_order, take_payment, remaining_stock

def test_quote_order_empty():
    assert quote_order("") == "$0.00"  # No items, total is $0.00

def test_quote_order_brownie():
    assert quote_order("B") == "$0.75"  # Brownie = $0.75

def test_quote_order_muffin():
    assert quote_order("M") == "$1.00"  # Muffin = $1.00

def test_quote_order_cake_pop():
    assert quote_order("C") == "$1.35"  # Cake Pop = $1.35

def test_quote_order_water():
    assert quote_order("W") == "$1.50"  # Water = $1.50

def test_quote_order_multiple_items():
    assert quote_order("B,C,W") == "$3.60"  # $0.75 + $1.35 + $1.50 = $3.60

def test_quote_order_multiple_same_items():
    assert quote_order("B,B,M") == "$2.50"  # $0.75 + $0.75 + $1.00 = $2.50

def test_quote_order_whitespace():
    assert quote_order(" B , C , W ") == "$3.60"  # Whitespace ignored, totals $3.60

def test_quote_order_cake_muffin():
    assert quote_order("C,M") == "$2.35"  # $1.35 + $1.00 = $2.35

def test_quote_order_invalid_code():
    with pytest.raises(Exception) as excinfo:
        quote_order("X")
    assert "X" in str(excinfo.value)  # Invalid code should raise error identifying the code

def test_take_payment_exact_total():
    assert take_payment("B,C,W", 3.60) == "$0.00"  # Paying exactly returns $0.00

def test_take_payment_overpay():
    assert take_payment("B,C,W", 4.00) == "$0.40"  # $4.00 - $3.60 = $0.40 change

def test_take_payment_underpay():
    with pytest.raises(Exception) as excinfo:
        take_payment("B,C,W", 3.00)
    assert str(excinfo.value) == "Not enough money"  # Underpayment should raise error

def test_take_payment_no_stock():
    # Setup stock with no Waters
    take_payment("W,W", 3.00)  # Should raise error
    with pytest.raises(Exception) as excinfo:
        take_payment("W,W", 3.00)
    assert "Water is out of stock" in str(excinfo.value)  # No Waters available

def test_remaining_stock_default():
    stock = remaining_stock()
    assert stock == {'B': 48, 'M': 36, 'C': 24, 'W': 30}  # Default stock values

def test_remaining_stock_custom():
    stock = remaining_stock({'B': 10, 'M': 5})
    assert stock == {'B': 10, 'M': 5, 'C': 0, 'W': 0}  # Custom stock values

def test_order_exceeds_stock():
    with pytest.raises(Exception) as excinfo:
        quote_order("B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B")  # More than 48
    assert "Brownie is out of stock" in str(excinfo.value)  # Should raise out of stock error

def test_order_unknown_code():
    with pytest.raises(Exception) as excinfo:
        quote_order("B,Z")
    assert "Z" in str(excinfo.value)  # Invalid code should raise error identifying the code

def test_take_payment_with_item_out_of_stock():
    # Setup stock with no Waters
    with pytest.raises(Exception) as excinfo:
        take_payment("B,W", 2.00)
    assert "Water is out of stock" in str(excinfo.value)  # Should raise out of stock error

def test_quote_order_does_not_change_stock():
    quote_order("B,C")  # Quoting an order
    stock = remaining_stock()
    assert stock == {'B': 48, 'M': 36, 'C': 24, 'W': 30}  # Stock should remain unchanged

def test_take_payment_decrements_stock():
    take_payment("B,C", 2.75)  # Paying for Brownie and Cake Pop
    stock = remaining_stock()
    assert stock['B'] == 47  # Brownies should decrease by 1
    assert stock['C'] == 23  # Cake Pops should decrease by 1

def test_order_item_absent_from_inventory():
    with pytest.raises(Exception) as excinfo:
        quote_order("W")  # W is absent from inventory
    assert "Water is out of stock" in str(excinfo.value)  # Should raise out of stock error

def test_selling_final_unit():
    # Setup stock with 1 Brownie
    take_payment("B", 0.75)  # Sell last Brownie
    with pytest.raises(Exception) as excinfo:
        quote_order("B")  # Next order for Brownie should fail
    assert "Brownie is out of stock" in str(excinfo.value)  # Should raise out of stock error