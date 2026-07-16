# test_solution.py

from solution import ShoppingCart
import pytest

def test_add_item_creates_line():
    cart = ShoppingCart()
    cart.add_item("apple", 0.99, 1)
    assert cart.get_quantity("apple") == 1  # Adding an item creates a line with quantity 1

def test_add_item_tops_up_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 0.99, 1)
    cart.add_item("apple", 0.99, 2)
    assert cart.get_quantity("apple") == 3  # Adding an item already in the cart tops up quantity

def test_add_item_without_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 0.99)
    assert cart.get_quantity("apple") == 1  # Adding without stating a quantity puts one unit in the cart

def test_remove_item_drops_line():
    cart = ShoppingCart()
    cart.add_item("apple", 0.99, 1)
    cart.remove_item("apple")
    assert cart.get_quantity("apple") == 0  # Removing an item drops its line entirely
    assert cart.get_total() == 0.0  # Removed item should not contribute to total
    assert cart.get_pre_discount_sum() == 0.0  # Removed item should not contribute to pre-discount sum

def test_change_quantity_reprices_line():
    cart = ShoppingCart()
    cart.add_item("apple", 0.99, 1)
    cart.change_quantity("apple", 3)
    assert cart.get_subtotal("apple") == 2.97  # Changing quantity reprices line

def test_set_quantity_to_zero_removes_line():
    cart = ShoppingCart()
    cart.add_item("apple", 0.99, 1)
    cart.change_quantity("apple", 0)
    assert cart.get_quantity("apple") == 0  # Setting quantity to zero removes the line

def test_set_quantity_to_one_updates_line():
    cart = ShoppingCart()
    cart.add_item("apple", 0.99, 2)
    cart.change_quantity("apple", 1)
    assert cart.get_quantity("apple") == 1  # Setting quantity to one keeps the line

def test_quantity_of_item_not_added_reads_zero():
    cart = ShoppingCart()
    assert cart.get_quantity("apple") == 0  # The quantity of an item never added reads zero

def test_line_subtotal_is_correct():
    cart = ShoppingCart()
    cart.add_item("apple", 0.99, 2)
    assert cart.get_subtotal("apple") == 1.98  # Line subtotal is unit price times quantity, rounded to cents

def test_cart_total_is_sum_of_subtotals():
    cart = ShoppingCart()
    cart.add_item("apple", 0.99, 2)
    cart.add_item("banana", 0.50, 3)
    assert cart.get_total() == 3.48  # Cart total is the sum of line subtotals

def test_empty_cart_totals_zero():
    cart = ShoppingCart()
    assert cart.get_total() == 0.0  # An empty cart totals 0.0

def test_empty_cart_pre_discount_sum_is_zero():
    cart = ShoppingCart()
    assert cart.get_pre_discount_sum() == 0.0  # An empty cart's pre-discount sum is 0.0

def test_cart_reports_pre_discount_sum():
    cart = ShoppingCart()
    cart.add_item("apple", 0.99, 2)
    cart.add_item("banana", 0.50, 3)
    assert cart.get_pre_discount_sum() == 3.48  # Pre-discount sum is all lines added together, rounded

def test_unit_price_of_zero_is_valid():
    cart = ShoppingCart()
    cart.add_item("apple", 0.00, 1)
    assert cart.get_subtotal("apple") == 0.00  # A unit price of zero is allowed and subtotals to zero

def test_empty_item_name_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.add_item("", 0.99, 1)  # Empty item name is rejected
    assert str(exc.value) == "item name must not be empty"

def test_negative_unit_price_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.add_item("apple", -0.99, 1)  # Negative unit price is rejected
    assert str(exc.value) == "unit_price must be non-negative, got -0.99"

def test_add_item_with_zero_quantity_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.add_item("apple", 0.99, 0)  # Adding fewer than one unit is rejected
    assert str(exc.value) == "quantity must be at least 1, got 0"

def test_change_quantity_to_negative_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 0.99, 1)
    with pytest.raises(ValueError) as exc:
        cart.change_quantity("apple", -1)  # Changing quantity to negative is rejected
    assert str(exc.value) == "quantity must be non-negative, got -1"

def test_remove_item_not_in_cart_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.remove_item("apple")  # Removing item not in cart is rejected
    assert str(exc.value) == "item apple is not in the cart"

def test_percentage_discount_reduces_total():
    cart = ShoppingCart()
    cart.add_item("apple", 10.00, 1)
    cart.apply_discount(10)  # 10% off
    assert cart.get_total() == 9.00  # 10.00 - 10% = 9.00

def test_percentage_discount_10_percent_on_59_97():
    cart = ShoppingCart()
    cart.add_item("item", 59.97, 1)
    cart.apply_discount(10)  # 10% off
    assert cart.get_total() == 53.97  # 59.97 - 10% = 53.973, rounded to 53.97

def test_percentage_discount_1_percent():
    cart = ShoppingCart()
    cart.add_item("item", 100.00, 1)
    cart.apply_discount(1)  # 1% off
    assert cart.get_total() == 99.00  # 100.00 - 1% = 99.00

def test_percentage_discount_100_percent():
    cart = ShoppingCart()
    cart.add_item("item", 100.00, 1)
    cart.apply_discount(100)  # 100% off
    assert cart.get_total() == 0.00  # 100.00 - 100% = 0.00

def test_invalid_percentage_discount_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.apply_discount(0)  # Invalid percentage
    assert str(exc.value) == "percent must be greater than 0 and at most 100, got 0"

def test_fixed_amount_discount_subtracts_from_total():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_fixed_discount(15.00)  # 15.00 off
    assert cart.get_total() == 85.00  # 100.00 - 15.00 = 85.00

def test_fixed_amount_discount_sub_unit_amount():
    cart = ShoppingCart()
    cart.add_item("apple", 10.00, 1)
    cart.apply_fixed_discount(0.75)  # 0.75 off
    assert cart.get_total() == 9.25  # 10.00 - 0.75 = 9.25

def test_fixed_amount_discount_does_not_below_zero():
    cart = ShoppingCart()
    cart.add_item("apple", 10.00, 1)
    cart.apply_fixed_discount(15.00)  # Attempting to apply more than total
    assert cart.get_total() == 0.00  # Total cannot go below zero

def test_fixed_discount_must_be_positive():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.apply_fixed_discount(0)  # Fixed amount discount must be positive
    assert str(exc.value) == "amount must be positive, got 0"

def test_fixed_discount_negative_amount_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.apply_fixed_discount(-1)  # Negative fixed discount
    assert str(exc.value) == "amount must be positive, got -1"

def test_bulk_price_offer_reprices_items():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 5)
    cart.apply_bulk_offer("apple", 0.80, 3)  # Bulk price of 0.80 for 3 or more
    assert cart.get_subtotal("apple") == 4.00  # 0.80 * 5 = 4.00

def test_bulk_offer_invalid_threshold_existing_item():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(ValueError) as exc:
        cart.apply_bulk_offer("apple", 0.80, 1)  # Invalid threshold
    assert str(exc.value) == "min_quantity must be at least 2, got 1"

def test_bulk_offer_invalid_threshold_nonexistent_item():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.apply_bulk_offer("banana", 0.80, 2)  # Banana is not in cart
    assert str(exc.value) == "item banana is not in the cart"

def test_bulk_offer_attached_only_to_existing_item():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(ValueError) as exc:
        cart.apply_bulk_offer("banana", 0.80, 2)  # Offer must be attached to existing item
    assert str(exc.value) == "item banana is not in the cart"

def test_buy_two_get_one_free_offer():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 6)
    cart.apply_bulk_offer("apple", 1.00, 1)  # Buy 2 get 1 free
    assert cart.get_subtotal("apple") == 4.00  # Charges for 4 of 6 units

def test_buy_one_get_one_free_offer():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 4)
    cart.apply_bulk_offer("apple", 1.00, 1)  # Buy 1 get 1 free
    assert cart.get_subtotal("apple") == 2.00  # Charges for 2 of 4 units

def test_buy_one_get_two_free_offer():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 5)
    cart.apply_bulk_offer("apple", 1.00, 2)  # Buy 1 get 2 free
    assert cart.get_subtotal("apple") == 2.00  # Charges for 2 of 5 units

def test_bulk_offer_invalid_buy_count_zero():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(ValueError) as exc:
        cart.apply_bulk_offer("apple", 1.00, 0)  # Invalid buy count
    assert str(exc.value) == "buy must be at least 1, got 0"

def test_bulk_offer_invalid_get_count_zero():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(ValueError) as exc:
        cart.apply_bulk_offer("apple", 1.00, 0)  # Invalid get count
    assert str(exc.value) == "get must be at least 1, got 0"

def test_bulk_offer_invalid_buy_count_negative():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(ValueError) as exc:
        cart.apply_bulk_offer("apple", 1.00, -1)  # Invalid buy count
    assert str(exc.value) == "buy must be at least 1, got -1"

def test_bulk_offer_invalid_get_count_negative():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(ValueError) as exc:
        cart.apply_bulk_offer("apple", 1.00, -1)  # Invalid get count
    assert str(exc.value) == "get must be at least 1, got -1"

def test_add_item_exceeding_stock_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 0.99, 1, stock=1)
    with pytest.raises(ValueError) as exc:
        cart.add_item("apple", 0.99, 2)  # Exceeding stock
    assert str(exc.value) == "only 1 of apple in stock, requested 2"

def test_add_item_exceeding_stock_exact():
    cart = ShoppingCart()
    cart.add_item("apple", 0.99, 1, stock=1)
    cart.add_item("apple", 0.99, 1)  # Exactly in stock
    assert cart.get_quantity("apple") == 2  # Should succeed

def test_stock_zero_rejection():
    cart = ShoppingCart()
    cart.add_item("apple", 0.99, 1, stock=0)  # Stock is zero
    with pytest.raises(ValueError) as exc:
        cart.add_item("apple", 0.99, 1)  # Cannot add
    assert str(exc.value) == "only 0 of apple in stock, requested 1"

def test_negative_stock_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.add_item("apple", 0.99, 1, stock=-1)  # Invalid stock
    assert str(exc.value) == "stock must be non-negative, got -1"

def test_per_order_cap_exceeding_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 0.99, 1, max_quantity=1)  # Per-order cap of 1
    with pytest.raises(ValueError) as exc:
        cart.change_quantity("apple", 2)  # Changing to exceed cap
    assert str(exc.value) == "maximum 1 of apple per order, requested 2"

def test_valid_per_order_cap():
    cart = ShoppingCart()
    cart.add_item("apple", 0.99, 1, max_quantity=1)  # Per-order cap of 1
    cart.change_quantity("apple", 1)  # Changing to exactly the cap should succeed
    assert cart.get_quantity("apple") == 1  # Should still be 1

def test_first_add_stock_cap_exceeding_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 0.99, 2, max_quantity=1)  # Per-order cap of 1
    with pytest.raises(ValueError) as exc:
        cart.add_item("apple", 0.99, 2)  # First add exceeds cap
    assert str(exc.value) == "maximum 1 of apple per order, requested 2"

def test_bulk_offer_threshold_below_two_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(ValueError) as exc:
        cart.apply_bulk_offer("apple", 0.80, 1)  # Invalid threshold
    assert str(exc.value) == "min_quantity must be at least 2, got 1"

def test_bulk_offer_bulk_price_negative_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(ValueError) as exc:
        cart.apply_bulk_offer("apple", -0.80, 2)  # Negative bulk price rejection
    assert str(exc.value) == "unit_price must be non-negative, got -0.80"

def test_bulk_offer_bulk_price_zero_valid():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)
    cart.apply_bulk_offer("apple", 0.00, 2)  # Bulk price of zero
    assert cart.get_subtotal("apple") == 0.00  # All units priced at zero

def test_bulk_offer_below_threshold_regular_price():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)  # Below threshold
    cart.apply_bulk_offer("apple", 0.80, 3)  # Bulk price offer
    assert cart.get_subtotal("apple") == 1.00  # Should still be regular price

def test_offer_empty_name_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(ValueError) as exc:
        cart.apply_bulk_offer("", 0.80, 2)  # Empty offer name
    assert str(exc.value) == "item name must not be empty"

def test_offer_duplicate_rejection():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.apply_bulk_offer("apple", 0.80, 2)  # First offer applied
    with pytest.raises(ValueError) as exc:
        cart.apply_bulk_offer("apple", 0.75, 2)  # Duplicate offer
    assert str(exc.value) == "item apple already has an offer"

def test_offer_on_non_discountable_item_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, discountable=False)  # Non-discountable item
    with pytest.raises(ValueError) as exc:
        cart.apply_bulk_offer("apple", 0.80, 2)  # Offer on non-discountable item
    assert str(exc.value) == "item apple cannot be combined with discounts"

def test_offer_applies_before_discount():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 5)
    cart.apply_bulk_offer("apple", 0.80, 3)  # Apply bulk offer
    cart.apply_discount(10)  # Then apply discount
    assert cart.get_total() == 3.60  # (0.80 * 5) = 4.00, then 10% off = 3.60

def test_bulk_offer_discountable_lines():
    cart = ShoppingCart()
    cart.add_item("non_discountable", 50.00, 1, discountable=False)
    cart.add_item("discountable", 30.00, 1)
    cart.apply_discount(10)  # 10% discount on the discountable line
    assert cart.get_total() == 50.00 + (30.00 * 0.90)  # 50.00 + 27.00 = 77.00

def test_fixed_discount_depletes_discountable_value():
    cart = ShoppingCart()
    cart.add_item("non_discountable", 50.00, 1, discountable=False)
    cart.add_item("discountable", 30.00, 1)
    cart.apply_fixed_discount(15.00)  # Fixed discount on discountable line
    assert cart.get_total() == 50.00 + max(0, 30.00 - 15.00)  # 50.00 + 15.00 = 65.00

def test_change_quantity_missing_item_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.change_quantity("missing", 1)  # Changing quantity of missing item
    assert str(exc.value) == "item missing is not in the cart"

def test_get_subtotal_missing_item_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.get_subtotal("missing")  # Getting subtotal of missing item
    assert str(exc.value) == "item missing is not in the cart"

def test_percentage_discount_above_100_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.apply_discount(101)  # Invalid percentage
    assert str(exc.value) == "percent must be greater than 0 and at most 100, got 101"

def test_per_order_cap_below_one_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.add_item("apple", 0.99, 1, max_quantity=0)  # Invalid cap
    assert str(exc.value) == "max_quantity must be at least 1, got 0"