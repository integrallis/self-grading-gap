import pytest
from solution import ShoppingCart

def test_add_item_creates_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    assert cart.get_quantity("apple") == 1  # Quantity should be 1

def test_add_item_tops_up_existing_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.add_item("apple", 1.00, 1)
    assert cart.get_quantity("apple") == 2  # Quantity should be 2

def test_add_item_without_quantity_defaults_to_one():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00)
    assert cart.get_quantity("apple") == 1  # Quantity should be 1

def test_remove_item_drops_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.remove_item("apple")
    assert cart.get_quantity("apple") == 0  # Quantity should be 0
    assert cart.get_total() == 0.00  # Total should be 0.00 after removal

def test_change_quantity_reprices_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.change_quantity("apple", 2)
    assert cart.get_quantity("apple") == 2  # Quantity should be 2
    assert cart.get_subtotal("apple") == 2.00  # Subtotal should be 1.00 * 2

def test_set_quantity_to_zero_removes_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.change_quantity("apple", 0)
    assert cart.get_quantity("apple") == 0  # Quantity should be 0
    assert cart.get_total() == 0.00  # Total should be 0.00 after removal

def test_set_quantity_to_one_updates_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.change_quantity("apple", 1)
    assert cart.get_quantity("apple") == 1  # Quantity should be 1

def test_quantity_of_item_not_added_is_zero():
    cart = ShoppingCart()
    assert cart.get_quantity("apple") == 0  # Quantity should be 0

def test_line_subtotal_is_unit_price_times_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)
    assert cart.get_subtotal("apple") == 2.00  # Subtotal should be 1.00 * 2

def test_cart_total_is_sum_of_line_subtotals():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)  # 2.00
    cart.add_item("banana", 1.50, 1)  # 1.50
    assert cart.get_total() == 3.50  # Total should be 2.00 + 1.50

def test_empty_cart_totals_zero():
    cart = ShoppingCart()
    assert cart.get_total() == 0.00  # Total should be 0.00

def test_empty_cart_pre_discount_sum_is_zero():
    cart = ShoppingCart()
    assert cart.get_pre_discount_sum() == 0.00  # Pre-discount sum should be 0.00

def test_cart_pre_discount_sum_is_sum_of_lines():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)  # 2.00
    cart.add_item("banana", 1.50, 1)  # 1.50
    assert cart.get_pre_discount_sum() == 3.50  # Pre-discount sum should be 3.50

def test_zero_unit_price_is_allowed_and_subtotals_to_zero():
    cart = ShoppingCart()
    cart.add_item("apple", 0.00, 5)
    assert cart.get_subtotal("apple") == 0.00  # Subtotal should be 0.00

def test_line_subtotal_rounding():
    cart = ShoppingCart()
    cart.add_item("apple", 1.333, 3)  # 1.333 * 3 = 4.00 (should round)
    assert cart.get_subtotal("apple") == 4.00  # Subtotal should be rounded to 4.00

def test_cart_total_rounding():
    cart = ShoppingCart()
    cart.add_item("apple", 1.333, 3)  # 1.333 * 3 = 4.00 (should round)
    cart.add_item("banana", 1.50, 1)  # 1.50
    assert cart.get_total() == 5.50  # Total should be rounded to 5.50

def test_empty_item_name_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.add_item("", 1.00, 1)
    assert str(exc.value) == "item name must not be empty"

def test_negative_unit_price_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.add_item("apple", -1.00, 1)
    assert str(exc.value) == "unit_price must be non-negative, got -1"

def test_add_fewer_than_one_unit_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.add_item("apple", 1.00, 0)
    assert str(exc.value) == "quantity must be at least 1, got 0"

def test_change_quantity_to_negative_value_is_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(Exception) as exc:
        cart.change_quantity("apple", -1)
    assert str(exc.value) == "quantity must be non-negative, got -1"

def test_remove_item_not_in_cart_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.remove_item("apple")
    assert str(exc.value) == "item apple is not in the cart"

def test_get_subtotal_of_item_not_in_cart_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.get_subtotal("apple")
    assert str(exc.value) == "item apple is not in the cart"

def test_change_quantity_of_item_not_in_cart_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.change_quantity("apple", 1)
    assert str(exc.value) == "item apple is not in the cart"

def test_apply_percentage_discount():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_percentage_discount(10)  # 10% off 100.00
    assert cart.get_total() == 90.00  # Total should be 90.00

def test_percentage_discount_boundaries():
    cart = ShoppingCart()
    cart.add_item("apple", 59.97, 1)
    cart.apply_percentage_discount(10)  # 10% off 59.97
    assert cart.get_total() == 53.97  # Total should be 53.97

    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_percentage_discount(1)  # 1% off 100.00
    assert cart.get_total() == 99.00  # Total should be 99.00

    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_percentage_discount(100)  # 100% off 100.00
    assert cart.get_total() == 0.00  # Total should be 0.00

def test_negative_percentage_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.apply_percentage_discount(-1)
    assert str(exc.value) == "percent must be greater than 0 and at most 100, got -1"

def test_apply_fixed_amount_discount():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_fixed_discount(15.00)  # 100.00 - 15.00
    assert cart.get_total() == 85.00  # Total should be 85.00

def test_fixed_discount_sub_unit_amount_is_accepted():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_fixed_discount(0.75)  # 100.00 - 0.75
    assert cart.get_total() == 99.25  # Total should be 99.25

def test_fixed_discount_must_be_positive():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.apply_fixed_discount(0)
    assert str(exc.value) == "amount must be positive, got 0"

def test_fixed_discount_never_below_zero():
    cart = ShoppingCart()
    cart.add_item("apple", 10.00, 1)
    cart.apply_fixed_discount(15.00)  # Total can't go below zero
    assert cart.get_total() == 0.00  # Total should be 0.00

def test_discount_apply_in_order():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_fixed_discount(10.00)  # 100 - 10 = 90
    cart.apply_percentage_discount(50)  # 90 - 45 = 45
    assert cart.get_total() == 45.00  # Total should be 45.00

def test_discountable_lines_only_for_percentage_discount():
    cart = ShoppingCart()
    cart.add_item("apple", 50.00, 1, discountable=True)
    cart.add_item("banana", 50.00, 1, discountable=False)
    cart.apply_percentage_discount(10)  # 10% off on apple only
    assert cart.get_total() == 95.00  # Total should be 50.00 * 0.9 + 50.00

def test_fixed_discount_only_applies_to_discountable_lines():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1, discountable=True)
    cart.add_item("banana", 50.00, 1, discountable=False)
    cart.apply_fixed_discount(15.00)  # (100 - 15) + 50 = 135.00
    assert cart.get_total() == 135.00  # Total should be 135.00

def test_buy_x_get_y_free_offer():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 6)
    cart.apply_buy_x_get_y_free_offer("apple", 2, 1)  # Buy 2 get 1 free
    assert cart.get_subtotal("apple") == 4.00  # Should charge for 4

def test_buy_1_get_1_offer():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 4)
    cart.apply_buy_x_get_y_free_offer("apple", 1, 1)  # Buy 1 get 1 free
    assert cart.get_subtotal("apple") == 2.00  # Should charge for 2

def test_buy_1_get_2_offer():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 5)
    cart.apply_buy_x_get_y_free_offer("apple", 1, 2)  # Buy 1 get 2 free
    assert cart.get_subtotal("apple") == 2.00  # Should charge for 2

def test_invalid_buy_x_get_y_free_offer_rejection():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)
    with pytest.raises(Exception) as exc:
        cart.apply_buy_x_get_y_free_offer("apple", 0, 1)
    assert str(exc.value) == "buy must be at least 1, got 0"
    
    with pytest.raises(Exception) as exc:
        cart.apply_buy_x_get_y_free_offer("apple", 1, 0)
    assert str(exc.value) == "get must be at least 1, got 0"

def test_bulk_price_offer():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)
    cart.apply_bulk_price_offer("apple", 2.00, 2)  # Bulk price of 2.00 if quantity >= 2
    assert cart.get_subtotal("apple") == 6.00  # Should charge 2.00 for all 3 apples

def test_bulk_price_offer_below_threshold():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.apply_bulk_price_offer("apple", 2.00, 2)  # Should retain regular price
    assert cart.get_subtotal("apple") == 1.00  # Should charge 1.00

def test_invalid_bulk_price_offer_rejection():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)
    with pytest.raises(Exception) as exc:
        cart.apply_bulk_price_offer("apple", 2.00, 1)
    assert str(exc.value) == "min_quantity must be at least 2, got 1"
    
    with pytest.raises(Exception) as exc:
        cart.apply_bulk_price_offer("apple", -1.00, 2)
    assert str(exc.value) == "unit_price must be non-negative, got -1"

def test_bulk_price_offer_zero_price_valid():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)
    cart.apply_bulk_price_offer("apple", 0.00, 2)  # Should accept zero price
    assert cart.get_subtotal("apple") == 0.00  # Should charge 0.00 for all apples

def test_enforce_stock_limits_first_add():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2, stock=2)
    with pytest.raises(Exception) as exc:
        cart.add_item("apple", 1.00, 1)  # Adding 1 more should exceed stock
    assert str(exc.value) == "only 2 of apple in stock, requested 3"

def test_enforce_stock_limits_change_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2, stock=2)
    with pytest.raises(Exception) as exc:
        cart.change_quantity("apple", 3)  # Exceeding stock should fail
    assert str(exc.value) == "only 2 of apple in stock, requested 3"

def test_enforce_stock_limits_exact_stock_success():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2, stock=2)
    cart.change_quantity("apple", 2)  # Changing to exact stock should succeed
    assert cart.get_quantity("apple") == 2  # Quantity should be 2

def test_enforce_stock_limits_zero_stock_rejection():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, stock=0)
    with pytest.raises(Exception) as exc:
        cart.add_item("apple", 1.00, 1)  # Adding should fail
    assert str(exc.value) == "only 0 of apple in stock, requested 1"

def test_enforce_stock_limits_negative_stock_rejection():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.add_item("apple", 1.00, 1, stock=-1)  # Negative stock should fail
    assert str(exc.value) == "stock must be non-negative, got -1"

def test_enforce_per_order_cap_first_add():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, max_quantity=1)
    with pytest.raises(Exception) as exc:
        cart.add_item("apple", 1.00, 1)  # Should fail due to cap
    assert str(exc.value) == "maximum 1 of apple per order, requested 2"

def test_enforce_per_order_cap_change_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, max_quantity=2)
    cart.change_quantity("apple", 2)  # Changing to max quantity should succeed
    with pytest.raises(Exception) as exc:
        cart.change_quantity("apple", 3)  # Exceeding max quantity should fail
    assert str(exc.value) == "maximum 2 of apple per order, requested 3"

def test_enforce_per_order_cap_below_one():
    with pytest.raises(Exception) as exc:
        ShoppingCart().add_item("apple", 1.00, 1, max_quantity=0)  # Invalid cap
    assert str(exc.value) == "max_quantity must be at least 1, got 0"