import pytest
from solution import ShoppingCart  # Assuming the main class for the shopping cart is ShoppingCart

def test_add_item_creates_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    assert cart.get_quantity("apple") == 1  # Quantity should be 1

def test_add_item_tops_up_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.add_item("apple", 1.00, 1)
    assert cart.get_quantity("apple") == 2  # Quantity should be 2

def test_add_item_without_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00)
    assert cart.get_quantity("apple") == 1  # Quantity should be 1

def test_remove_item_drops_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.remove_item("apple")
    assert cart.get_quantity("apple") == 0  # Quantity should be 0

def test_change_quantity_reprices_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.change_quantity("apple", 3)
    assert cart.get_quantity("apple") == 3  # Quantity should be 3

def test_set_quantity_to_zero_removes_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.change_quantity("apple", 0)
    assert cart.get_quantity("apple") == 0  # Quantity should be 0

def test_set_quantity_to_one_updates_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.change_quantity("apple", 1)
    assert cart.get_quantity("apple") == 1  # Quantity should be 1

def test_get_quantity_of_non_added_item_is_zero():
    cart = ShoppingCart()
    assert cart.get_quantity("apple") == 0  # Quantity should be 0

def test_line_subtotal_is_correct():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)
    assert cart.get_subtotal("apple") == 3.00  # Subtotal should be 1.00 * 3

def test_cart_total_is_correct():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)  # 2.00
    cart.add_item("banana", 2.00, 1)  # 2.00
    assert cart.get_total() == 4.00  # Total should be 4.00

def test_empty_cart_totals_zero():
    cart = ShoppingCart()
    assert cart.get_total() == 0.00  # Total should be 0.00

def test_pre_discount_sum_is_correct():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)  # 2.00
    cart.add_item("banana", 2.00, 1)  # 2.00
    assert cart.get_pre_discount_sum() == 4.00  # Pre-discount sum should be 4.00

def test_zero_unit_price_subtotal():
    cart = ShoppingCart()
    cart.add_item("apple", 0.00, 3)
    assert cart.get_subtotal("apple") == 0.00  # Subtotal should be 0.00

def test_empty_item_name_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="item name must not be empty"):
        cart.add_item("", 1.00, 1)

def test_negative_unit_price_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="unit_price must be non-negative, got [-1.0]"):
        cart.add_item("apple", -1.00, 1)

def test_add_item_with_zero_quantity_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="quantity must be at least 1, got [0]"):
        cart.add_item("apple", 1.00, 0)

def test_change_quantity_to_negative_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(ValueError, match="quantity must be non-negative, got [-1]"):
        cart.change_quantity("apple", -1)

def test_remove_item_not_in_cart_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="item [apple] is not in the cart"):
        cart.remove_item("apple")

def test_discount_percentage_reduces_total():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)  # 100.00
    cart.apply_discount_percent(10)  # 10% off
    assert cart.get_total() == 90.00  # Total should be 90.00

def test_discount_percentage_must_be_positive():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="percent must be greater than 0 and at most 100, got [0]"):
        cart.apply_discount_percent(0)

def test_fixed_discount_subtracts_amount():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)  # 100.00
    cart.apply_fixed_discount(15.00)  # 15.00 off
    assert cart.get_total() == 85.00  # Total should be 85.00

def test_fixed_discount_must_be_positive():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="amount must be positive, got [0]"):
        cart.apply_fixed_discount(0)

def test_fixed_discount_never_below_zero():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)  # 100.00
    cart.apply_fixed_discount(150.00)  # 150.00 off
    assert cart.get_total() == 0.00  # Total should be 0.00

def test_bulk_price_offer():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)
    cart.apply_bulk_price_offer("apple", 2, 0.80)  # 2 units or more at 0.80
    assert cart.get_subtotal("apple") == 2.40  # 3 units should cost 2.40 (0.80 * 3)

def test_add_offer_to_non_discountable_item_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.mark_item_as_non_discountable("apple")
    with pytest.raises(ValueError, match="item [apple] cannot be combined with discounts"):
        cart.apply_bulk_price_offer("apple", 2, 0.80)

def test_exceeding_stock_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, stock=1)  # 1 in stock
    with pytest.raises(ValueError, match="only [0] of [apple] in stock, requested [2]"):
        cart.add_item("apple", 1.00, 2)

def test_exceeding_per_order_cap_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, max_quantity=1)  # Max 1 allowed
    with pytest.raises(ValueError, match="maximum [1] of [apple] per order, requested [2]"):
        cart.change_quantity("apple", 2)

def test_negative_stock_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="stock must be non-negative, got [-1]"):
        cart.add_item("apple", 1.00, 1, stock=-1)

def test_negative_max_quantity_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="max_quantity must be at least 1, got [0]"):
        cart.add_item("apple", 1.00, 1, max_quantity=0)