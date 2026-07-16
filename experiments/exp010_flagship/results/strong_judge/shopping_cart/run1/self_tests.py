# your complete test file
import pytest
from solution import ShoppingCart  # Assuming the main class is ShoppingCart

def test_add_item_creates_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)  # Add 1 apple at $1.00
    assert cart.get_quantity("apple") == 1  # Quantity should be 1

def test_add_item_tops_up_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)  # Add 1 apple at $1.00
    cart.add_item("apple", 1.00, 2)  # Add 2 more apples
    assert cart.get_quantity("apple") == 3  # Total quantity should be 3

def test_add_item_without_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00)  # Add apple without specifying quantity
    assert cart.get_quantity("apple") == 1  # Should default to 1

def test_remove_item_drops_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.remove_item("apple")  # Remove apple
    assert cart.get_quantity("apple") == 0  # Quantity should be 0
    with pytest.raises(Exception) as exc:
        cart.get_subtotal("apple")  # Should raise an error
    assert str(exc.value) == "item [apple] is not in the cart"

def test_change_quantity_reprices_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)  # Add 2 apples at $1.00
    cart.change_quantity("apple", 3)  # Change quantity to 3
    assert cart.get_quantity("apple") == 3  # Quantity should be 3
    assert cart.get_subtotal("apple") == 3.00  # Subtotal should now be 3.00

def test_set_quantity_to_zero_removes_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.change_quantity("apple", 0)  # Set quantity to 0
    assert cart.get_quantity("apple") == 0  # Quantity should be 0
    with pytest.raises(Exception) as exc:
        cart.get_subtotal("apple")  # Should raise an error
    assert str(exc.value) == "item [apple] is not in the cart"

def test_set_quantity_to_one_keeps_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.change_quantity("apple", 1)  # Set quantity to 1
    assert cart.get_quantity("apple") == 1  # Quantity should stay 1

def test_quantity_of_item_not_added_reads_zero():
    cart = ShoppingCart()
    assert cart.get_quantity("apple") == 0  # Should read zero

def test_line_subtotal():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)  # 2 apples at $1.00
    assert cart.get_subtotal("apple") == 2.00  # Subtotal should be 2.00

def test_cart_total_is_sum_of_line_subtotals():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)  # 2 apples at $1.00
    cart.add_item("banana", 0.50, 4)  # 4 bananas at $0.50
    assert cart.get_total() == 4.00  # Total should be 4.00

def test_empty_cart_totals_zero():
    cart = ShoppingCart()
    assert cart.get_total() == 0.00  # Total should be 0.00
    assert cart.get_pre_discount_sum() == 0.00  # Pre-discount sum should be 0.00

def test_cart_pre_discount_sum():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)  # 2 apples at $1.00
    assert cart.get_pre_discount_sum() == 2.00  # Pre-discount sum should be 2.00

def test_zero_unit_price_subtotals_to_zero():
    cart = ShoppingCart()
    cart.add_item("apple", 0.00, 2)  # 2 apples at $0.00
    assert cart.get_subtotal("apple") == 0.00  # Subtotal should be 0.00

def test_line_subtotal_rounding():
    cart = ShoppingCart()
    cart.add_item("apple", 1.234, 1)  # 1 apple at $1.234
    assert cart.get_subtotal("apple") == 1.23  # Subtotal should round to 1.23

def test_empty_item_name_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.add_item("", 1.00, 1)
    assert str(exc.value) == "item name must not be empty"

def test_negative_unit_price_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.add_item("apple", -1.00, 1)
    assert str(exc.value) == "unit_price must be non-negative, got [-1.0]"

def test_add_fewer_than_one_unit_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.add_item("apple", 1.00, 0)
    assert str(exc.value) == "quantity must be at least 1, got [0]"

def test_change_quantity_to_negative_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(Exception) as exc:
        cart.change_quantity("apple", -1)
    assert str(exc.value) == "quantity must be non-negative, got [-1]"

def test_remove_item_not_in_cart_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.remove_item("banana")
    assert str(exc.value) == "item [banana] is not in the cart"

def test_change_quantity_not_in_cart_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.change_quantity("banana", 1)
    assert str(exc.value) == "item [banana] is not in the cart"

def test_get_subtotal_not_in_cart_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.get_subtotal("banana")
    assert str(exc.value) == "item [banana] is not in the cart"

def test_discounted_percentage_applies_correctly():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)  # 1 apple at $1.00
    cart.apply_percentage_discount(10)  # 10% off
    assert cart.get_total() == 0.90  # 10% off 1.00 should be 0.90

def test_percentage_discount_on_cart_total():
    cart = ShoppingCart()
    cart.add_item("apple", 59.97, 1)  # 1 apple at $59.97
    cart.apply_percentage_discount(10)  # 10% off
    assert cart.get_total() == round(59.97 * 0.90, 2)  # 10% off

def test_percentage_discount_boundary_cases():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)  # 1 apple at $1.00
    cart.apply_percentage_discount(1)  # 1% off
    assert cart.get_total() == round(1.00 * 0.99, 2)  # 1% off should be 0.99

    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)  # 1 apple at $1.00
    cart.apply_percentage_discount(100)  # 100% off
    assert cart.get_total() == 0.00  # Total should be 0.00

def test_discount_must_be_positive_and_at_most_100():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.apply_percentage_discount(0)
    assert str(exc.value) == "percent must be greater than 0 and at most 100, got [0]"

    with pytest.raises(Exception) as exc:
        cart.apply_percentage_discount(101)
    assert str(exc.value) == "percent must be greater than 0 and at most 100, got [101]"

def test_fixed_amount_discount_applies_correctly():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)  # 2 apples at $1.00
    cart.apply_fixed_amount_discount(1.00)  # $1.00 off
    assert cart.get_total() == 1.00  # Total should be 1.00 after discount

def test_fixed_discount_15_off_100():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)  # 1 apple at $100.00
    cart.apply_fixed_amount_discount(15.00)  # $15.00 off
    assert cart.get_total() == 85.00  # Total should be 85.00 after discount

def test_fixed_amount_discount_cannot_take_total_below_zero():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)  # 1 apple at $1.00
    cart.apply_fixed_amount_discount(2.00)  # $2.00 off should clamp to 0.00
    assert cart.get_total() == 0.00

def test_fixed_amount_discount_must_be_positive():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.apply_fixed_amount_discount(0)
    assert str(exc.value) == "amount must be positive, got [0]"

    with pytest.raises(Exception) as exc:
        cart.apply_fixed_amount_discount(-1)
    assert str(exc.value) == "amount must be positive, got [-1]"

def test_fixed_discount_sub_unit_amount():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)  # 2 apples at $1.00
    cart.apply_fixed_amount_discount(0.75)  # $0.75 off
    assert cart.get_total() == 1.25  # Total should be 1.25 after discount

def test_buy_x_get_y_free_offer_applies_correctly():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 6)  # 6 apples at $1.00
    cart.add_offer("apple", "buy", 2, "get", 1)  # Buy 2 get 1 free
    assert cart.get_subtotal("apple") == 4.00  # Pay for 4 apples

def test_buy_two_get_one_free_on_five_units():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 5)  # 5 apples at $1.00
    cart.add_offer("apple", "buy", 2, "get", 1)  # Buy 2 get 1 free
    assert cart.get_subtotal("apple") == 4.00  # Pay for 4 apples

def test_buy_one_get_one_free_on_four_units():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 4)  # 4 apples at $1.00
    cart.add_offer("apple", "buy", 1, "get", 1)  # Buy 1 get 1 free
    assert cart.get_subtotal("apple") == 2.00  # Pay for 2 apples

def test_buy_one_get_two_free_on_five_units():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 5)  # 5 apples at $1.00
    cart.add_offer("apple", "buy", 1, "get", 2)  # Buy 1 get 2 free
    assert cart.get_subtotal("apple") == 2.00  # Pay for 2 apples

def test_offer_cannot_attach_to_non_discountable_item():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.set_discountable("apple", False)  # Make it non-discountable
    with pytest.raises(Exception) as exc:
        cart.add_offer("apple", "buy", 1, "get", 1)
    assert str(exc.value) == "item [apple] cannot be combined with discounts"

def test_offer_attaches_only_to_item_in_cart():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.add_offer("banana", "buy", 1, "get", 1)
    assert str(exc.value) == "item [banana] is not in the cart"

def test_invalid_bulk_price_offer_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(Exception) as exc:
        cart.add_bulk_price_offer("apple", 1.00, 1)  # Invalid threshold
    assert str(exc.value) == "min_quantity must be at least 2, got [1]"

def test_enforcing_stock_limits():
    cart = ShoppingCart()
    cart.set_stock("apple", 5)  # 5 in stock
    cart.add_item("apple", 1.00, 5)  # Buy 5 apples
    with pytest.raises(Exception) as exc:
        cart.add_item("apple", 1.00, 1)  # Try to buy 1 more
    assert str(exc.value) == "only [5] of [apple] in stock, requested [6]"

def test_enforcing_per_order_caps():
    cart = ShoppingCart()
    cart.set_per_order_cap("apple", 2)  # Max 2 apples per order
    cart.add_item("apple", 1.00, 2)  # Buy 2 apples
    with pytest.raises(Exception) as exc:
        cart.add_item("apple", 1.00, 1)  # Try to buy 1 more
    assert str(exc.value) == "maximum [2] of [apple] per order, requested [3]"

def test_negative_stock_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.set_stock("apple", -1)
    assert str(exc.value) == "stock must be non-negative, got [-1]"

def test_negative_per_order_cap_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.set_per_order_cap("apple", 0)
    assert str(exc.value) == "max_quantity must be at least 1, got [0]"

def test_bulk_price_offer_below_threshold():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)  # 1 apple at $1.00
    cart.add_bulk_price_offer("apple", 0.75, 2)  # Set bulk price for 2
    assert cart.get_subtotal("apple") == 1.00  # Should still be $1.00

def test_bulk_price_offer_at_threshold():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)  # 2 apples at $1.00
    cart.add_bulk_price_offer("apple", 0.75, 2)  # Set bulk price for 2
    assert cart.get_subtotal("apple") == 1.50  # Should be $0.75 each, total $1.50

def test_bulk_price_offer_negative_price_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(Exception) as exc:
        cart.add_bulk_price_offer("apple", -0.50, 2)  # Invalid bulk price
    assert str(exc.value) == "unit_price must be non-negative, got [-0.5]"

def test_bulk_price_offer_valid_threshold_two():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.add_bulk_price_offer("apple", 0.75, 2)  # Valid threshold of 2
    assert cart.get_subtotal("apple") == 1.00  # Should still be $1.00

def test_bulk_price_offer_valid_zero_price():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)
    cart.add_bulk_price_offer("apple", 0.00, 2)  # Valid zero bulk price
    assert cart.get_subtotal("apple") == 0.00  # Should be $0.00

def test_second_offer_on_already_offered_item_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.add_offer("apple", "buy", 1, "get", 1)  # First offer
    with pytest.raises(Exception) as exc:
        cart.add_offer("apple", "buy", 2, "get", 1)  # Second offer
    assert str(exc.value) == "item [apple] already has an offer"

def test_empty_offer_item_name_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.add_offer("", "buy", 1, "get", 1)  # Invalid item name
    assert str(exc.value) == "item name must not be empty"

def test_offers_apply_before_cart_discounts():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)  # 3 apples at $1.00
    cart.add_offer("apple", "buy", 2, "get", 1)  # Buy 2 get 1 free
    cart.apply_fixed_amount_discount(1.00)  # $1.00 off
    assert cart.get_total() == 1.00  # Pay for 2 apples after offer

def test_stock_limit_first_add_failure():
    cart = ShoppingCart()
    cart.set_stock("apple", 5)  # Set stock for apple
    with pytest.raises(Exception) as exc:
        cart.add_item("apple", 1.00, 6)  # First add exceeds stock
    assert str(exc.value) == "only [5] of [apple] in stock, requested [6]"

def test_stock_limit_change_quantity_failure():
    cart = ShoppingCart()
    cart.set_stock("apple", 5)  # Set stock for apple
    cart.add_item("apple", 1.00, 5)  # Add 5 apples
    with pytest.raises(Exception) as exc:
        cart.change_quantity("apple", 6)  # Change quantity to 6 exceeds stock
    assert str(exc.value) == "only [5] of [apple] in stock, requested [6]"

def test_stock_limit_success_at_limit():
    cart = ShoppingCart()
    cart.set_stock("apple", 5)  # Set stock for apple
    cart.add_item("apple", 1.00, 5)  # Add 5 apples should succeed
    assert cart.get_quantity("apple") == 5  # Quantity should be 5

def test_zero_stock_behavior():
    cart = ShoppingCart()
    cart.set_stock("apple", 0)  # Set stock to 0
    with pytest.raises(Exception) as exc:
        cart.add_item("apple", 1.00, 1)  # Try to add
    assert str(exc.value) == "only [0] of [apple] in stock, requested [1]"

def test_per_order_cap_first_add_failure():
    cart = ShoppingCart()
    cart.set_per_order_cap("apple", 2)  # Set cap for apple
    with pytest.raises(Exception) as exc:
        cart.add_item("apple", 1.00, 3)  # First add exceeds cap
    assert str(exc.value) == "maximum [2] of [apple] per order, requested [3]"

def test_per_order_cap_change_quantity_failure():
    cart = ShoppingCart()
    cart.set_per_order_cap("apple", 2)  # Set cap for apple
    cart.add_item("apple", 1.00, 2)  # Add 2 apples
    with pytest.raises(Exception) as exc:
        cart.change_quantity("apple", 3)  # Change quantity to 3 exceeds cap
    assert str(exc.value) == "maximum [2] of [apple] per order, requested [3]"

def test_per_order_cap_success_at_cap():
    cart = ShoppingCart()
    cart.set_per_order_cap("apple", 2)  # Set cap for apple
    cart.add_item("apple", 1.00, 2)  # Add 2 apples should succeed
    assert cart.get_quantity("apple") == 2  # Quantity should be 2

def test_per_order_cap_one_behavior():
    cart = ShoppingCart()
    cart.set_per_order_cap("apple", 1)  # Set cap for apple
    cart.add_item("apple", 1.00, 1)  # Add 1 apple should succeed
    assert cart.get_quantity("apple") == 1  # Quantity should be 1

def test_per_order_cap_change_to_cap_success():
    cart = ShoppingCart()
    cart.set_per_order_cap("apple", 1)  # Set cap for apple
    cart.add_item("apple", 1.00, 1)  # Add 1 apple
    cart.change_quantity("apple", 1)  # Change quantity to 1 should succeed
    assert cart.get_quantity("apple") == 1  # Quantity should be 1