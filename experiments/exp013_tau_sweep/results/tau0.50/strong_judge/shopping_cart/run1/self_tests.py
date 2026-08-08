from solution import ShoppingCart
import pytest

def test_adding_item_creates_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    assert cart.get_quantity("apple") == 1  # Expect quantity to be 1
    assert cart.get_subtotal("apple") == 1.00  # Expect subtotal to be 1.00

def test_adding_existing_item_tops_up_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.add_item("apple", 1.00, 2)
    assert cart.get_quantity("apple") == 3  # Expect quantity to be 3
    assert cart.get_subtotal("apple") == 3.00  # Expect subtotal to be 3.00

def test_adding_item_without_quantity_puts_one_unit():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00)
    assert cart.get_quantity("apple") == 1  # Expect quantity to be 1
    assert cart.get_subtotal("apple") == 1.00  # Expect subtotal to be 1.00

def test_removing_item_drops_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.remove_item("apple")
    assert cart.get_quantity("apple") == 0  # Expect quantity to be 0
    assert cart.get_total() == 0.0  # Expect total to be 0.0

def test_changing_quantity_reprices_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.change_quantity("apple", 3)
    assert cart.get_quantity("apple") == 3  # Expect quantity to be 3
    assert cart.get_subtotal("apple") == 3.00  # Expect subtotal to be 3.00

def test_setting_quantity_to_zero_removes_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.change_quantity("apple", 0)
    assert cart.get_quantity("apple") == 0  # Expect quantity to be 0
    assert cart.get_total() == 0.0  # Expect total to be 0.0

def test_setting_quantity_to_one_keeps_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.change_quantity("apple", 1)
    assert cart.get_quantity("apple") == 1  # Expect quantity to be 1
    assert cart.get_subtotal("apple") == 1.00  # Expect subtotal to be 1.00

def test_quantity_of_item_not_added_reads_zero():
    cart = ShoppingCart()
    assert cart.get_quantity("apple") == 0  # Expect quantity to be 0

def test_line_subtotal_is_rounded():
    cart = ShoppingCart()
    cart.add_item("apple", 1.235, 2)  # 1.235 * 2 = 2.470
    assert cart.get_subtotal("apple") == 2.47  # Expect subtotal to be 2.47

def test_cart_total_is_sum_of_line_subtotals():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)  # 1.00 * 2 = 2.00
    cart.add_item("banana", 0.50, 3)  # 0.50 * 3 = 1.50
    assert cart.get_total() == 3.50  # Expect total to be 3.50

def test_empty_cart_totals_zero():
    cart = ShoppingCart()
    assert cart.get_total() == 0.0  # Expect total to be 0.0

def test_empty_cart_pre_discount_sum_is_zero():
    cart = ShoppingCart()
    assert cart.get_pre_discount_sum() == 0.0  # Expect pre-discount sum to be 0.0

def test_cart_pre_discount_sum_is_sum_of_lines():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)  # Subtotal 2.00
    cart.add_item("banana", 0.50, 3)  # Subtotal 1.50
    assert cart.get_pre_discount_sum() == 3.50  # Expect pre-discount sum to be 3.50

def test_unit_price_of_zero_subtotals_to_zero():
    cart = ShoppingCart()
    cart.add_item("apple", 0.00, 2)
    assert cart.get_subtotal("apple") == 0.0  # Expect subtotal to be 0.0

def test_empty_item_name_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^item name must not be empty$"):
        cart.add_item("", 1.00, 1)

def test_negative_unit_price_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^unit_price must be non-negative, got -1.0$"):
        cart.add_item("apple", -1.00, 1)

def test_adding_fewer_than_one_unit_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^quantity must be at least 1, got 0$"):
        cart.add_item("apple", 1.00, 0)

def test_changing_quantity_to_negative_value_is_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(ValueError, match=r"^quantity must be non-negative, got -1$"):
        cart.change_quantity("apple", -1)

def test_removing_item_not_in_cart_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^item apple is not in the cart$"):
        cart.remove_item("apple")

def test_getting_subtotal_of_item_not_in_cart_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^item apple is not in the cart$"):
        cart.get_subtotal("apple")

def test_changing_quantity_of_item_not_in_cart_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^item apple is not in the cart$"):
        cart.change_quantity("apple", 1)

def test_percentage_discount_must_be_positive_and_at_most_100():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    with pytest.raises(ValueError, match=r"^percent must be greater than 0 and at most 100, got 0$"):
        cart.apply_percentage_discount(0)
    with pytest.raises(ValueError, match=r"^percent must be greater than 0 and at most 100, got 101$"):
        cart.apply_percentage_discount(101)

def test_fixed_amount_discount_must_be_positive():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    with pytest.raises(ValueError, match=r"^amount must be positive, got 0$"):
        cart.apply_fixed_discount(0)

def test_fixed_amount_discount_never_takes_total_below_zero():
    cart = ShoppingCart()
    cart.add_item("apple", 10.00, 1)
    cart.apply_fixed_discount(15.00)  # Should not go below 0
    assert cart.get_total() == 0.0  # Expect total to be 0.0

def test_fixed_amount_discount_applies_only_to_discountable_portion():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1, discountable=True)
    cart.add_item("banana", 50.00, 1, discountable=False)
    cart.apply_fixed_discount(30.00)  # Should apply only to apple
    assert cart.get_total() == 120.00  # Expect total to be 120.00

def test_buy_x_get_y_free_offer_reprices_correctly():
    cart = ShoppingCart()
    cart.add_item("apple", 3.00, 5)
    cart.add_offer("apple", buy=2, get=1)  # Buy 2 get 1 free
    assert cart.get_subtotal("apple") == 12.00  # 4 paid out of 5 items: 4 * 3.00 = 12.00

def test_bulk_price_offer_reprices_correctly():
    cart = ShoppingCart()
    cart.add_item("apple", 3.00, 5)
    cart.add_offer("apple", bulk_quantity=3, bulk_price=2.50)  # Bulk price for 3+
    assert cart.get_subtotal("apple") == 12.50  # 2.50 * 5 = 12.50

def test_bulk_price_offer_rejects_invalid_threshold():
    cart = ShoppingCart()
    cart.add_item("apple", 3.00, 1)
    with pytest.raises(ValueError, match=r"^min_quantity must be at least 2, got 1$"):
        cart.add_offer("apple", bulk_quantity=1, bulk_price=2.50)

def test_bulk_price_offer_rejects_negative_price():
    cart = ShoppingCart()
    cart.add_item("apple", 3.00, 1)
    with pytest.raises(ValueError, match=r"^unit_price must be non-negative, got -1.0$"):
        cart.add_offer("apple", bulk_quantity=2, bulk_price=-1.00)

def test_offer_attaches_only_to_item_in_cart():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^item apple is not in the cart$"):
        cart.add_offer("apple", buy=1, get=1)

def test_offer_name_must_not_be_empty():
    cart = ShoppingCart()
    cart.add_item("apple", 3.00, 1)
    with pytest.raises(ValueError, match=r"^item name must not be empty$"):
        cart.add_offer("", buy=1, get=1)

def test_offer_combined_with_discounts():
    cart = ShoppingCart()
    cart.add_item("apple", 3.00, 5)
    cart.add_offer("apple", buy=2, get=1)
    cart.apply_fixed_discount(3.00)
    assert cart.get_total() == 9.00  # (3 * 4) - 3 = 9.00

def test_request_exceeding_stock_is_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 3.00, 1, stock=2)
    with pytest.raises(ValueError, match=r"^only 2 of apple in stock, requested 3$"):
        cart.add_item("apple", 3.00, 2)  # Exceeds stock

def test_request_exceeding_per_order_cap_is_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 3.00, 1, max_quantity=2)
    with pytest.raises(ValueError, match=r"^maximum 2 of apple per order, requested 3$"):
        cart.add_item("apple", 3.00, 3)  # Exceeds per-order cap

def test_negative_stock_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^stock must be non-negative, got -1$"):
        cart.add_item("apple", 3.00, 1, stock=-1)

def test_per_order_cap_below_one_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^max_quantity must be at least 1, got 0$"):
        cart.add_item("apple", 3.00, 1, max_quantity=0)

def test_request_exceeding_stock_on_first_add_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^only 2 of apple in stock, requested 3$"):
        cart.add_item("apple", 3.00, 3, stock=2)  # Should fail

def test_request_exceeding_stock_on_quantity_change_is_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 3.00, 2, stock=2)  # Should succeed
    with pytest.raises(ValueError, match=r"^only 2 of apple in stock, requested 3$"):
        cart.change_quantity("apple", 3)  # Exceeds stock

def test_request_exceeding_per_order_cap_on_first_add_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^maximum 2 of apple per order, requested 3$"):
        cart.add_item("apple", 3.00, 3, max_quantity=2)  # Should fail

def test_request_exceeding_per_order_cap_on_quantity_change_is_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 3.00, 1, max_quantity=2)  # Should succeed
    with pytest.raises(ValueError, match=r"^maximum 2 of apple per order, requested 3$"):
        cart.change_quantity("apple", 3)  # Exceeds per-order cap

def test_buy_one_get_one_free_offer_reprices_correctly():
    cart = ShoppingCart()
    cart.add_item("apple", 3.00, 4)
    cart.add_offer("apple", buy=1, get=1)  # Buy 1 get 1 free
    assert cart.get_subtotal("apple") == 6.00  # 2 paid out of 4 items: 2 * 3.00 = 6.00

def test_buy_one_get_two_free_offer_reprices_correctly():
    cart = ShoppingCart()
    cart.add_item("apple", 3.00, 5)
    cart.add_offer("apple", buy=1, get=2)  # Buy 1 get 2 free
    assert cart.get_subtotal("apple") == 6.00  # 2 paid out of 5 items: 2 * 3.00 = 6.00

def test_buy_two_get_one_free_offer_reprices_correctly():
    cart = ShoppingCart()
    cart.add_item("apple", 3.00, 6)
    cart.add_offer("apple", buy=2, get=1)  # Buy 2 get 1 free
    assert cart.get_subtotal("apple") == 12.00  # 4 paid out of 6 items: 4 * 3.00 = 12.00

def test_bulk_price_offer_keeps_regular_price_below_threshold():
    cart = ShoppingCart()
    cart.add_item("apple", 3.00, 2)
    cart.add_offer("apple", bulk_quantity=3, bulk_price=2.50)  # Should keep regular price
    assert cart.get_subtotal("apple") == 6.00  # 3.00 * 2 = 6.00

def test_bulk_price_offer_with_valid_boundary_conditions():
    cart = ShoppingCart()
    cart.add_item("apple", 3.00, 2)
    cart.add_offer("apple", bulk_quantity=2, bulk_price=0.00)  # Valid
    assert cart.get_subtotal("apple") == 0.00  # All at bulk price is zero

def test_bulk_price_offer_with_invalid_boundary_conditions():
    cart = ShoppingCart()
    cart.add_item("apple", 3.00, 1)
    with pytest.raises(ValueError, match=r"^min_quantity must be at least 2, got 1$"):
        cart.add_offer("apple", bulk_quantity=1, bulk_price=2.50)