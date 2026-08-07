import pytest
from solution import ShoppingCart

def test_adding_item_creates_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    assert cart.get_quantity("apple") == 1  # 1 unit added

def test_adding_existing_item_tops_up_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.add_item("apple", 1.00, 1)
    assert cart.get_quantity("apple") == 2  # 1 + 1 = 2 units

def test_adding_item_without_quantity_puts_one_unit():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00)
    assert cart.get_quantity("apple") == 1  # Default quantity is 1

def test_removing_item_drops_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.remove_item("apple")
    assert cart.get_quantity("apple") == 0  # Line should be removed
    assert cart.get_total() == 0.00  # No items, total should be 0.00
    assert cart.get_pre_discount_sum() == 0.00  # No items, pre-discount sum is 0.00

def test_changing_quantity_reprices_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.25, 1)
    cart.set_quantity("apple", 3)
    assert cart.get_quantity("apple") == 3  # Quantity updated to 3
    assert cart.get_subtotal("apple") == 3.75  # 1.25 * 3 = 3.75

def test_setting_quantity_to_zero_removes_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.set_quantity("apple", 0)
    assert cart.get_quantity("apple") == 0  # Line should be removed

def test_setting_quantity_to_one_keeps_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.set_quantity("apple", 1)
    assert cart.get_quantity("apple") == 1  # Line remains with 1 unit

def test_quantity_of_item_not_added_reads_zero():
    cart = ShoppingCart()
    assert cart.get_quantity("apple") == 0  # Item not in cart

def test_line_subtotal_is_correct():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)
    assert cart.get_subtotal("apple") == 3.00  # 1.00 * 3 = 3.00

def test_cart_total_is_sum_of_line_subtotals():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)
    cart.add_item("banana", 2.00, 2)
    assert cart.get_total() == 7.00  # 3.00 + 4.00 = 7.00

def test_empty_cart_totals_zero():
    cart = ShoppingCart()
    assert cart.get_total() == 0.00  # No items, total should be 0.00

def test_empty_cart_pre_discount_sum_is_zero():
    cart = ShoppingCart()
    assert cart.get_pre_discount_sum() == 0.00  # No items, pre-discount sum is 0.00

def test_cart_reports_pre_discount_sum():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)
    cart.add_item("banana", 2.00, 1)
    assert cart.get_pre_discount_sum() == 5.00  # 3.00 + 2.00 = 5.00

def test_unit_price_of_zero_subtotals_to_zero():
    cart = ShoppingCart()
    cart.add_item("apple", 0.00, 5)
    assert cart.get_subtotal("apple") == 0.00  # 0.00 * 5 = 0.00

def test_line_subtotal_rounded_to_cents():
    cart = ShoppingCart()
    cart.add_item("apple", 1.234, 3)
    assert cart.get_subtotal("apple") == 3.70  # 1.234 * 3 = 3.70 (rounded)

def test_cart_total_rounded_to_cents():
    cart = ShoppingCart()
    cart.add_item("apple", 59.97, 1)
    cart.apply_discount(10)  # 10% off
    assert cart.get_total() == 53.97  # 59.97 * 0.90 = 53.97

def test_empty_item_name_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.add_item("", 1.00, 1)
    assert str(exc.value) == "item name must not be empty"

def test_negative_unit_price_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.add_item("apple", -1.00, 1)
    assert str(exc.value) == "unit_price must be non-negative, got -1.00"

def test_adding_fewer_than_one_unit_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.add_item("apple", 1.00, 0)
    assert str(exc.value) == "quantity must be at least 1, got 0"

def test_changing_quantity_to_negative_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(ValueError) as exc:
        cart.set_quantity("apple", -1)
    assert str(exc.value) == "quantity must be non-negative, got -1"

def test_removing_nonexistent_item_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.remove_item("apple")
    assert str(exc.value) == "item apple is not in the cart"

def test_getting_subtotal_of_nonexistent_item_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.get_subtotal("apple")
    assert str(exc.value) == "item apple is not in the cart"

def test_applying_percentage_discount_valid():
    cart = ShoppingCart()
    cart.add_item("apple", 10.00, 1)
    cart.apply_discount(10)  # 10% off
    assert cart.get_total() == 9.00  # 10.00 - (10.00 * 0.10) = 9.00

def test_percentage_discount_valid_1_percent():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_discount(1)  # 1% off
    assert cart.get_total() == 99.00  # 100.00 - (100.00 * 0.01) = 99.00

def test_percentage_discount_valid_100_percent():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_discount(100)  # 100% off
    assert cart.get_total() == 0.00  # 100.00 - (100.00 * 1.00) = 0.00

def test_discount_must_be_positive_and_at_most_100():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.apply_discount(0)
    assert str(exc.value) == "percent must be greater than 0 and at most 100, got 0"
    with pytest.raises(ValueError) as exc:
        cart.apply_discount(101)
    assert str(exc.value) == "percent must be greater than 0 and at most 100, got 101"

def test_applying_fixed_amount_discount_valid():
    cart = ShoppingCart()
    cart.add_item("apple", 10.00, 1)
    cart.apply_fixed_discount(5.00)
    assert cart.get_total() == 5.00  # 10.00 - 5.00 = 5.00

def test_fixed_discount_must_be_positive():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.apply_fixed_discount(0)
    assert str(exc.value) == "amount must be positive, got 0"

def test_fixed_discount_never_below_zero():
    cart = ShoppingCart()
    cart.add_item("apple", 10.00, 1)
    cart.apply_fixed_discount(15.00)  # Should not be allowed to go below 0
    assert cart.get_total() == 0.00  # Total should clamp at zero

def test_discount_applies_in_order():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_fixed_discount(10.00)  # Fixed discount first
    cart.apply_discount(50)  # Then 50%
    assert cart.get_total() == 45.00  # (100.00 - 10.00) * 0.5 = 45.00

def test_discountable_lines_skipped_by_percentage_discount():
    cart = ShoppingCart()
    cart.add_item("apple", 50.00, 1, discountable=False)
    cart.add_item("banana", 100.00, 1)
    cart.apply_discount(10)  # 10% off only banana
    assert cart.get_total() == 140.00  # 50.00 + (100.00 - (100.00 * 0.10)) = 140.00

def test_fixed_discount_depletes_only_discountable_portion():
    cart = ShoppingCart()
    cart.add_item("apple", 50.00, 1, discountable=False)
    cart.add_item("banana", 100.00, 1)
    cart.apply_fixed_discount(20.00)  # Should only apply to banana
    assert cart.get_total() == 130.00  # 50.00 + (100.00 - 20.00) = 130.00

def test_buy_x_get_y_offer_valid():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)
    cart.add_offer("apple", buy=2, get=1)  # Buy 2 get 1 free
    assert cart.get_subtotal("apple") == 2.00  # Pay for 2 out of 3

def test_buy_x_get_y_offer_rejected_if_less_than_one():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(ValueError) as exc:
        cart.add_offer("apple", buy=0, get=1)
    assert str(exc.value) == "buy must be at least 1, got 0"
    with pytest.raises(ValueError) as exc:
        cart.add_offer("apple", buy=1, get=0)
    assert str(exc.value) == "get must be at least 1, got 0"

def test_bulk_price_offer_applies_correctly():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)
    cart.add_offer("apple", bulk_price=0.80, min_quantity=2)  # Bulk price for 2+
    assert cart.get_subtotal("apple") == 2.40  # 3 * 0.80 = 2.40

def test_bulk_threshold_and_price_validations():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(ValueError) as exc:
        cart.add_offer("apple", bulk_price=1.00, min_quantity=1)
    assert str(exc.value) == "min_quantity must be at least 2, got 1"
    with pytest.raises(ValueError) as exc:
        cart.add_offer("apple", bulk_price=-1.00, min_quantity=2)
    assert str(exc.value) == "unit_price must be non-negative, got -1.00"

def test_offer_attaches_only_to_existing_item():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.add_offer("banana", buy=1, get=1)
    assert str(exc.value) == "item banana is not in the cart"

def test_offer_attaches_only_to_discountable_items():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, discountable=False)
    with pytest.raises(ValueError) as exc:
        cart.add_offer("apple", buy=1, get=1)
    assert str(exc.value) == "item apple cannot be combined with discounts"

def test_offer_attaches_only_once():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.add_offer("apple", buy=1, get=1)
    with pytest.raises(ValueError) as exc:
        cart.add_offer("apple", buy=2, get=1)
    assert str(exc.value) == "item apple already has an offer"

def test_stock_must_be_non_negative():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.add_item("apple", 1.00, 1, stock=-1)
    assert str(exc.value) == "stock must be non-negative, got -1"

def test_exceeding_stock_request_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, stock=1)
    with pytest.raises(ValueError) as exc:
        cart.add_item("apple", 1.00, 2)
    assert str(exc.value) == "only 1 of apple in stock, requested 2"

def test_buying_exactly_stock_succeeds():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, stock=1)
    assert cart.get_quantity("apple") == 1  # Should succeed
    assert cart.get_total() == 1.00  # Total should reflect 1.00

def test_exceeding_stock_on_first_add_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.add_item("apple", 1.00, 2, stock=1)
    assert str(exc.value) == "only 1 of apple in stock, requested 2"

def test_exceeding_per_order_cap_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, max_quantity=1)
    with pytest.raises(ValueError) as exc:
        cart.add_item("apple", 1.00, 2)
    assert str(exc.value) == "maximum 1 of apple per order, requested 2"

def test_changing_quantity_to_cap_succeeds():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, max_quantity=1)
    cart.set_quantity("apple", 1)  # Should succeed

def test_set_quantity_exceeds_stock_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, stock=1)
    with pytest.raises(ValueError) as exc:
        cart.set_quantity("apple", 2)
    assert str(exc.value) == "only 1 of apple in stock, requested 2"

def test_set_quantity_exceeds_cap_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, max_quantity=1)
    with pytest.raises(ValueError) as exc:
        cart.set_quantity("apple", 2)
    assert str(exc.value) == "maximum 1 of apple per order, requested 2"

def test_set_quantity_of_nonexistent_item_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.set_quantity("apple", 1)
    assert str(exc.value) == "item apple is not in the cart"

def test_discountable_lines_depleted_to_zero():
    cart = ShoppingCart()
    cart.add_item("banana", 100.00, 1)
    cart.add_item("apple", 50.00, 1, discountable=True)
    cart.apply_fixed_discount(50.00)  # Should only apply to apple
    assert cart.get_total() == 100.00  # Banana remains at 100.00

def test_buy_x_get_y_offer_partial_batches():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 6)
    cart.add_offer("apple", buy=2, get=1)  # Buy 2 get 1 free
    assert cart.get_subtotal("apple") == 4.00  # Pay for 4 out of 6

def test_buy_one_get_one_free_offer():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 4)
    cart.add_offer("apple", buy=1, get=1)  # Buy 1 get 1 free
    assert cart.get_subtotal("apple") == 2.00  # Pay for 2 out of 4

def test_buy_one_get_two_free_offer():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 5)
    cart.add_offer("apple", buy=1, get=2)  # Buy 1 get 2 free
    assert cart.get_subtotal("apple") == 2.00  # Pay for 2 out of 5

def test_bulk_price_offer_below_threshold():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.add_offer("apple", bulk_price=0.80, min_quantity=2)  # Bulk price for 2+
    assert cart.get_subtotal("apple") == 1.00  # Regular price applies

def test_bulk_price_offer_at_threshold():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)
    cart.add_offer("apple", bulk_price=0.80, min_quantity=2)  # Bulk price for 2+
    assert cart.get_subtotal("apple") == 1.60  # 2 * 0.80 = 1.60

def test_bulk_price_offer_zero_price():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)
    cart.add_offer("apple", bulk_price=0.00, min_quantity=2)  # Bulk price for 2+
    assert cart.get_subtotal("apple") == 0.00  # 3 * 0.00 = 0.00

def test_offer_validation_negative_buy():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(ValueError) as exc:
        cart.add_offer("apple", buy=-1, get=1)
    assert str(exc.value) == "buy must be at least 1, got -1"

def test_offer_validation_negative_get():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(ValueError) as exc:
        cart.add_offer("apple", buy=1, get=-1)
    assert str(exc.value) == "get must be at least 1, got -1"

def test_offer_validation_empty_item_name():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.add_offer("", buy=1, get=1)
    assert str(exc.value) == "item name must not be empty"

def test_offer_reshape_before_cart_discount():
    cart = ShoppingCart()
    cart.add_item("apple", 10.00, 4)
    cart.add_offer("apple", buy=1, get=1)  # Buy 1 get 1 free
    cart.apply_discount(10)  # 10% off
    assert cart.get_total() == 36.00  # (20.00 - (20.00 * 0.10)) = 18.00

def test_stock_zero_admitting_nothing():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, stock=0)
    with pytest.raises(ValueError) as exc:
        cart.add_item("apple", 1.00, 1)
    assert str(exc.value) == "only 0 of apple in stock, requested 1"

def test_first_add_per_order_cap_failure():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.add_item("apple", 1.00, 2, max_quantity=1)
    assert str(exc.value) == "maximum 1 of apple per order, requested 2"

def test_per_order_cap_zero_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.add_item("apple", 1.00, 1, max_quantity=0)
    assert str(exc.value) == "max_quantity must be at least 1, got 0"

def test_per_order_cap_negative_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError) as exc:
        cart.add_item("apple", 1.00, 1, max_quantity=-1)
    assert str(exc.value) == "max_quantity must be at least 1, got -1"

def test_first_add_exceeds_stock_leaves_cart_unchanged():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, stock=1)
    try:
        cart.add_item("apple", 1.00, 2)
    except ValueError:
        pass
    assert cart.get_quantity("apple") == 1  # Should still be 1
    assert cart.get_total() == 1.00  # Total should reflect 1.00

def test_accumulating_add_exceeds_stock_leaves_cart_unchanged():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, stock=1)
    cart.add_item("banana", 1.00, 1, stock=1)
    try:
        cart.add_item("apple", 1.00, 2)
    except ValueError:
        pass
    assert cart.get_quantity("apple") == 1  # Should still be 1
    assert cart.get_quantity("banana") == 1  # Should still be 1
    assert cart.get_total() == 2.00  # Total should reflect 2.00

def test_set_quantity_exceeds_stock_leaves_cart_unchanged():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, stock=1)
    try:
        cart.set_quantity("apple", 2)
    except ValueError:
        pass
    assert cart.get_quantity("apple") == 1  # Should still be 1
    assert cart.get_total() == 1.00  # Total should reflect 1.00