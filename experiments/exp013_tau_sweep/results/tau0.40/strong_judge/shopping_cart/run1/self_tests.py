import pytest
from solution import ShoppingCart

def test_add_item_creates_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    assert cart.get_quantity("apple") == 1  # Should read back the quantity

def test_add_item_tops_up_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.add_item("apple", 1.00, 1)
    assert cart.get_quantity("apple") == 2  # Should top up the quantity

def test_add_item_without_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00)
    assert cart.get_quantity("apple") == 1  # Should default to one unit

def test_remove_item_drops_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.remove_item("apple")
    assert cart.get_quantity("apple") == 0  # Should read zero after removal
    assert cart.get_total() == 0.00  # Should not contribute to total

def test_change_quantity_reprices_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.change_quantity("apple", 2)
    assert cart.get_quantity("apple") == 2  # Should reflect the new quantity
    assert cart.get_subtotal("apple") == 2.00  # 1.00 * 2

def test_set_quantity_to_zero_removes_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.change_quantity("apple", 0)
    assert cart.get_quantity("apple") == 0  # Should remove the line
    with pytest.raises(Exception) as excinfo:
        cart.get_subtotal("apple")  # Should raise an error for missing item
    assert str(excinfo.value) == "item apple is not in the cart"

def test_set_quantity_to_one_keeps_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.change_quantity("apple", 1)
    assert cart.get_quantity("apple") == 1  # Should remain unchanged

def test_quantity_of_item_not_added_is_zero():
    cart = ShoppingCart()
    assert cart.get_quantity("apple") == 0  # Should read zero for non-existent item

def test_line_subtotal_is_correct():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)
    assert cart.get_subtotal("apple") == 2.00  # 1.00 * 2

def test_cart_total_is_sum_of_line_subtotals():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)  # 2.00
    cart.add_item("banana", 0.50, 3)  # 1.50
    assert cart.get_total() == 3.50  # 2.00 + 1.50

def test_empty_cart_totals_zero():
    cart = ShoppingCart()
    assert cart.get_total() == 0.00  # Empty cart total
    assert cart.get_pre_discount_sum() == 0.00  # Pre-discount sum

def test_cart_reports_pre_discount_sum():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)  # 2.00
    cart.add_item("banana", 0.50, 3)  # 1.50
    assert cart.get_pre_discount_sum() == 3.50  # Pre-discount sum

def test_unit_price_of_zero_subtotals_to_zero():
    cart = ShoppingCart()
    cart.add_item("apple", 0.00, 5)
    assert cart.get_subtotal("apple") == 0.00  # 0.00 * 5

def test_empty_item_name_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as excinfo:
        cart.add_item("", 1.00, 1)
    assert str(excinfo.value) == "item name must not be empty"

def test_negative_unit_price_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as excinfo:
        cart.add_item("apple", -1.00, 1)
    assert str(excinfo.value) == "unit_price must be non-negative, got -1.0"

def test_add_fewer_than_one_unit_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as excinfo:
        cart.add_item("apple", 1.00, 0)
    assert str(excinfo.value) == "quantity must be at least 1, got 0"

def test_change_quantity_to_negative_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(Exception) as excinfo:
        cart.change_quantity("apple", -1)
    assert str(excinfo.value) == "quantity must be non-negative, got -1"

def test_remove_nonexistent_item_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as excinfo:
        cart.remove_item("apple")
    assert str(excinfo.value) == "item apple is not in the cart"

def test_discount_percentage_reduces_total():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_discount(10)  # 10% off
    assert cart.get_total() == 90.00  # 100.00 - 10.00

def test_discount_percentage_must_be_valid():
    cart = ShoppingCart()
    with pytest.raises(Exception) as excinfo:
        cart.apply_discount(0)
    assert str(excinfo.value) == "percent must be greater than 0 and at most 100, got 0"

def test_discount_percentage_valid_1_percent():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_discount(1)  # 1% off
    assert cart.get_total() == 99.00  # 100.00 - 1.00

def test_discount_percentage_valid_100_percent():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_discount(100)  # 100% off
    assert cart.get_total() == 0.00  # 100.00 - 100.00

def test_discount_percentage_invalid_above_100_percent():
    cart = ShoppingCart()
    with pytest.raises(Exception) as excinfo:
        cart.apply_discount(101)
    assert str(excinfo.value) == "percent must be greater than 0 and at most 100, got 101"

def test_fixed_amount_discount_reduces_total():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_fixed_discount(15.00)  # $15 off
    assert cart.get_total() == 85.00  # 100.00 - 15.00

def test_fixed_amount_discount_below_one_currency_unit():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_fixed_discount(0.75)  # $0.75 off
    assert cart.get_total() == 99.25  # 100.00 - 0.75

def test_fixed_amount_discount_cannot_go_below_zero():
    cart = ShoppingCart()
    cart.add_item("apple", 10.00, 1)
    cart.apply_fixed_discount(15.00)  # Should clamp to zero
    assert cart.get_total() == 0.00

def test_fixed_amount_discount_must_be_positive():
    cart = ShoppingCart()
    with pytest.raises(Exception) as excinfo:
        cart.apply_fixed_discount(0)
    assert str(excinfo.value) == "amount must be positive, got 0.0"

def test_buy_x_get_y_discount():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)
    cart.apply_buy_x_get_y_free("apple", 2, 1)  # Buy 2, get 1 free
    assert cart.get_subtotal("apple") == 2.00  # Pay for 2 out of 3

def test_buy_x_get_y_discount_partial_batch():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 5)
    cart.apply_buy_x_get_y_free("apple", 2, 1)  # Buy 2, get 1 free
    assert cart.get_subtotal("apple") == 4.00  # Pay for 4 out of 5

def test_buy_x_get_y_discount_partial_batch_6_units():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 6)
    cart.apply_buy_x_get_y_free("apple", 2, 1)  # Buy 2, get 1 free
    assert cart.get_subtotal("apple") == 4.00  # Pay for 4 out of 6

def test_buy_x_get_y_discount_rejects_invalid_buy():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(Exception) as excinfo:
        cart.apply_buy_x_get_y_free("apple", 0, 1)
    assert str(excinfo.value) == "buy must be at least 1, got 0"

def test_buy_x_get_y_discount_rejects_invalid_get():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(Exception) as excinfo:
        cart.apply_buy_x_get_y_free("apple", 1, 0)
    assert str(excinfo.value) == "get must be at least 1, got 0"

def test_stock_must_be_non_negative():
    cart = ShoppingCart()
    with pytest.raises(Exception) as excinfo:
        cart.set_stock("apple", -1)
    assert str(excinfo.value) == "stock must be non-negative, got -1"

def test_request_exceeds_stock_rejected():
    cart = ShoppingCart()
    cart.set_stock("apple", 2)
    with pytest.raises(Exception) as excinfo:
        cart.add_item("apple", 1.00, 3)  # Requesting 3 when only 2 in stock
    assert str(excinfo.value) == "only 2 of apple in stock, requested 3"
    # Should not add to cart
    assert cart.get_quantity("apple") == 0  

def test_stock_limit_exact_stock_succeeds():
    cart = ShoppingCart()
    cart.set_stock("apple", 2)
    cart.add_item("apple", 1.00, 2)  # Exactly 2 in stock
    assert cart.get_quantity("apple") == 2  

def test_stock_limit_zero_stock_rejected():
    cart = ShoppingCart()
    cart.set_stock("apple", 0)  # No stock available
    with pytest.raises(Exception) as excinfo:
        cart.add_item("apple", 1.00, 1)  # Attempt to add
    assert str(excinfo.value) == "only 0 of apple in stock, requested 1"

def test_stock_limit_accumulating_add_failure():
    cart = ShoppingCart()
    cart.set_stock("apple", 2)
    cart.add_item("apple", 1.00, 1)  # Add 1
    with pytest.raises(Exception) as excinfo:
        cart.add_item("apple", 1.00, 2)  # Attempt to add 2 more
    assert str(excinfo.value) == "only 2 of apple in stock, requested 2"

def test_stock_limit_quantity_change_failure():
    cart = ShoppingCart()
    cart.set_stock("apple", 2)
    cart.add_item("apple", 1.00, 1)  # Add 1
    cart.change_quantity("apple", 2)  # Change to 2
    assert cart.get_quantity("apple") == 2  # Should now be 2 in cart

def test_per_order_cap_exceeded_rejected():
    cart = ShoppingCart()
    cart.set_stock("apple", 5)
    cart.set_per_order_cap("apple", 2)  # Cap of 2
    with pytest.raises(Exception) as excinfo:
        cart.add_item("apple", 1.00, 3)  # Requesting 3 exceeds cap
    assert str(excinfo.value) == "maximum 2 of apple per order, requested 3"
    # Should not add to cart
    assert cart.get_quantity("apple") == 0  

def test_per_order_cap_of_one_is_valid():
    cart = ShoppingCart()
    cart.set_stock("apple", 5)
    cart.set_per_order_cap("apple", 1)  # Cap of 1
    cart.add_item("apple", 1.00, 1)  # Should succeed
    assert cart.get_quantity("apple") == 1  # Should be 1 in cart

def test_per_order_cap_limit_change_to_cap_succeeds():
    cart = ShoppingCart()
    cart.set_stock("apple", 5)
    cart.set_per_order_cap("apple", 2)  # Cap of 2
    cart.add_item("apple", 1.00, 1)  # Add 1
    cart.change_quantity("apple", 2)  # Change to cap
    assert cart.get_quantity("apple") == 2  # Should be 2 in cart

def test_bulk_price_offer_below_threshold():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.apply_bulk_price_offer("apple", 2, 0.80)  # Threshold 2, price 0.80
    assert cart.get_subtotal("apple") == 1.00  # Should pay regular price

def test_bulk_price_offer_at_threshold():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)
    cart.apply_bulk_price_offer("apple", 2, 0.80)  # Threshold 2, price 0.80
    assert cart.get_subtotal("apple") == 1.60  # Should pay bulk price

def test_bulk_price_offer_invalid_threshold():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(Exception) as excinfo:
        cart.apply_bulk_price_offer("apple", 1, 0.80)  # Invalid threshold
    assert str(excinfo.value) == "min_quantity must be at least 2, got 1"

def test_bulk_price_offer_negative_price():
    cart = ShoppingCart()
    with pytest.raises(Exception) as excinfo:
        cart.apply_bulk_price_offer("apple", 2, -1.00)  # Invalid price
    assert str(excinfo.value) == "unit_price must be non-negative, got -1.0"

def test_bulk_price_offer_valid_threshold_two_zero_price():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)
    cart.apply_bulk_price_offer("apple", 2, 0.00)  # Threshold 2, price 0.00
    assert cart.get_subtotal("apple") == 0.00  # Should pay zero price

def test_offer_attachments_rejects_missing_item():
    cart = ShoppingCart()
    with pytest.raises(Exception) as excinfo:
        cart.apply_buy_x_get_y_free("banana", 1, 1)  # Item not in cart
    assert str(excinfo.value) == "item banana is not in the cart"

def test_offer_attachments_empty_name():
    cart = ShoppingCart()
    with pytest.raises(Exception) as excinfo:
        cart.apply_buy_x_get_y_free("", 1, 1)  # Empty name
    assert str(excinfo.value) == "item name must not be empty"

def test_offer_attachments_rejects_duplicate_offer():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.apply_buy_x_get_y_free("apple", 1, 1)  # First offer
    with pytest.raises(Exception) as excinfo:
        cart.apply_buy_x_get_y_free("apple", 1, 1)  # Duplicate offer
    assert str(excinfo.value) == "item apple already has an offer"

def test_offer_applies_before_cart_discounts():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)
    cart.apply_buy_x_get_y_free("apple", 2, 1)  # Buy 2, get 1 free
    cart.apply_discount(10)  # 10% off
    assert cart.get_total() == 1.80  # 2 * 1.00 = 2.00, 10% off = 1.80

def test_discount_registration_order_fixed_then_percentage():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_fixed_discount(10.00)  # $10 off
    cart.apply_discount(50)  # 50% off
    assert cart.get_total() == 45.00  # (100 - 10 = 90), 50% off = 45.00

def test_discount_registration_order_percentage_then_fixed():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_discount(50)  # 50% off
    cart.apply_fixed_discount(10.00)  # $10 off
    assert cart.get_total() == 40.00  # (100 - 50% = 50), 50 - 10 = 40.00

def test_percentage_discount_skips_non_discountable_lines():
    cart = ShoppingCart()
    cart.add_item("apple", 50.00, 1)
    cart.set_per_order_cap("apple", 1)  # Non-discountable
    cart.add_item("banana", 30.00, 1)
    cart.apply_discount(10)  # 10% off
    assert cart.get_total() == 63.00  # Only banana is discountable: 30 - 10% = 27.00, +50.00 = 77.00

def test_fixed_discount_does_not_affect_non_discountable_lines():
    cart = ShoppingCart()
    cart.add_item("apple", 50.00, 1)
    cart.set_per_order_cap("apple", 1)  # Non-discountable
    cart.add_item("banana", 30.00, 1)
    cart.apply_fixed_discount(10)  # $10 off
    assert cart.get_total() == 70.00  # The fixed discount only affects banana: 30 - 10 = 20 + 50 = 70.00