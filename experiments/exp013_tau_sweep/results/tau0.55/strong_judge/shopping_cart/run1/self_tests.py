import pytest
from solution import ShoppingCart

# US-1: Managing the items in the cart
def test_add_item_creates_line():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 2)
    assert cart.get_quantity("item1") == 2  # quantity should be 2
    assert cart.get_line_subtotal("item1") == 20.0  # subtotal should be 20.0

def test_add_item_increases_quantity():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 2)
    cart.add_item("item1", 10.0, 3)
    assert cart.get_quantity("item1") == 5  # quantity should be 5
    assert cart.get_line_subtotal("item1") == 50.0  # subtotal should be 50.0

def test_add_item_without_quantity_puts_one_unit():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0)
    assert cart.get_quantity("item1") == 1  # quantity should be 1
    assert cart.get_line_subtotal("item1") == 10.0  # subtotal should be 10.0

def test_remove_item_drops_line():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 2)
    cart.remove_item("item1")
    assert cart.get_quantity("item1") == 0  # quantity should be 0
    assert cart.get_total() == 0.0  # total should be 0.0

def test_change_item_quantity_reprices_line():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1)
    cart.change_quantity("item1", 3)
    assert cart.get_quantity("item1") == 3  # quantity should be 3
    assert cart.get_line_subtotal("item1") == 30.0  # subtotal should be 30.0

def test_setting_quantity_to_zero_removes_line():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1)
    cart.change_quantity("item1", 0)
    assert cart.get_quantity("item1") == 0  # quantity should be 0
    with pytest.raises(ValueError, match=r"^item item1 is not in the cart$"):
        cart.get_line_subtotal("item1")  # must raise error for non-existent item

def test_setting_quantity_to_one_keeps_line():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 2)
    cart.change_quantity("item1", 1)
    assert cart.get_quantity("item1") == 1  # quantity should be 1

def test_quantity_of_item_not_added_is_zero():
    cart = ShoppingCart()
    assert cart.get_quantity("item1") == 0  # quantity should be 0

# US-2: Pricing the order
def test_line_subtotal_is_correct():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 2)  # subtotal = 10.0 * 2 = 20.0
    assert cart.get_line_subtotal("item1") == 20.0  # subtotal should be 20.0

def test_cart_total_is_sum_of_line_subtotals():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 2)  # subtotal = 20.0
    cart.add_item("item2", 5.0, 3)   # subtotal = 15.0
    assert cart.get_total() == 35.0  # total should be 35.0

def test_empty_cart_totals_zero():
    cart = ShoppingCart()
    assert cart.get_total() == 0.0  # total should be 0.0
    assert cart.get_pre_discount_sum() == 0.0  # pre-discount sum should be 0.0

def test_cart_reports_pre_discount_sum():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 2)  # pre-discount sum = 20.0
    assert cart.get_pre_discount_sum() == 20.0  # pre-discount sum should be 20.0

def test_unit_price_zero_subtotals_to_zero():
    cart = ShoppingCart()
    cart.add_item("item1", 0.0, 5)  # subtotal = 0.0
    assert cart.get_line_subtotal("item1") == 0.0  # subtotal should be 0.0

def test_line_subtotal_rounding():
    cart = ShoppingCart()
    cart.add_item("item1", 59.997, 1)  # subtotal = 59.997
    assert cart.get_line_subtotal("item1") == round(59.997, 2)  # subtotal should be rounded to 59.99

def test_cart_total_rounding():
    cart = ShoppingCart()
    cart.add_item("item1", 59.97, 1)
    cart.apply_percentage_discount(10)  # 59.97 * 0.90 = 53.973
    assert cart.get_total() == round(53.973, 2)  # total should be rounded to 53.97

def test_pre_discount_sum_rounding():
    cart = ShoppingCart()
    cart.add_item("item1", 59.97, 1)
    cart.add_item("item2", 0.75, 1)  # pre-discount sum = 60.72
    assert cart.get_pre_discount_sum() == round(60.72, 2)  # pre-discount sum should be rounded to 60.72

# US-3: Rejecting invalid line operations
def test_empty_item_name_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^item name must not be empty$"):
        cart.add_item("", 10.0, 1)

def test_negative_unit_price_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^unit_price must be non-negative, got -5.0$"):
        cart.add_item("item1", -5.0, 1)

def test_adding_fewer_than_one_unit_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^quantity must be at least 1, got 0$"):
        cart.add_item("item1", 10.0, 0)

def test_changing_quantity_to_negative_is_rejected():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1)
    with pytest.raises(ValueError, match=r"^quantity must be non-negative, got -1$"):
        cart.change_quantity("item1", -1)

def test_removing_nonexistent_item_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^item item1 is not in the cart$"):
        cart.remove_item("item1")

def test_requantifying_nonexistent_item_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^item item1 is not in the cart$"):
        cart.change_quantity("item1", 1)

def test_getting_subtotal_of_nonexistent_item_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^item item1 is not in the cart$"):
        cart.get_line_subtotal("item1")

# US-4: Applying storewide discounts
def test_percentage_discount_reduces_total():
    cart = ShoppingCart()
    cart.add_item("item1", 100.0, 1)
    cart.apply_percentage_discount(10)  # 10% off 100.0 -> 90.0
    assert cart.get_total() == 90.0  # total should be 90.0

def test_valid_percentage_discount():
    cart = ShoppingCart()
    cart.add_item("item1", 100.0, 1)
    cart.apply_percentage_discount(1)  # 1% off 100.0 -> 99.0
    assert cart.get_total() == 99.0  # total should be 99.0

def test_valid_percentage_discount_100():
    cart = ShoppingCart()
    cart.add_item("item1", 100.0, 1)
    cart.apply_percentage_discount(100)  # 100% off 100.0 -> 0.0
    assert cart.get_total() == 0.0  # total should be 0.0

def test_percentage_discount_must_be_between_0_and_100():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^percent must be greater than 0 and at most 100, got 0$"):
        cart.apply_percentage_discount(0)
    with pytest.raises(ValueError, match=r"^percent must be greater than 0 and at most 100, got 101$"):
        cart.apply_percentage_discount(101)

def test_fixed_amount_discount_subtracts_amount_from_total():
    cart = ShoppingCart()
    cart.add_item("item1", 100.0, 1)
    cart.apply_fixed_discount(15.0)  # 100.0 - 15.0 -> 85.0
    assert cart.get_total() == 85.0  # total should be 85.0

def test_fixed_amount_discount_never_below_zero():
    cart = ShoppingCart()
    cart.add_item("item1", 100.0, 1)
    cart.apply_fixed_discount(150.0)  # total should not go below 0
    assert cart.get_total() == 0.0  # total should be 0.0

def test_fixed_amount_discount_must_be_positive():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^amount must be positive, got 0$"):
        cart.apply_fixed_discount(0)
    with pytest.raises(ValueError, match=r"^amount must be positive, got -10$"):
        cart.apply_fixed_discount(-10)

def test_fixed_amount_discount_sub_unit_amount():
    cart = ShoppingCart()
    cart.add_item("item1", 100.0, 1)
    cart.apply_fixed_discount(0.75)  # 100.0 - 0.75 = 99.25
    assert cart.get_total() == 99.25  # total should be 99.25

def test_discounts_apply_in_order():
    cart = ShoppingCart()
    cart.add_item("item1", 100.0, 1)
    cart.apply_fixed_discount(10.0)  # 100.0 - 10.0 = 90.0
    cart.apply_percentage_discount(50)  # 90.0 * 0.5 = 45.0
    assert cart.get_total() == 45.0  # total should be 45.0

def test_reverse_discount_order():
    cart = ShoppingCart()
    cart.add_item("item1", 100.0, 1)
    cart.apply_percentage_discount(50)  # 100.0 * 0.5 = 50.0
    cart.apply_fixed_discount(10.0)  # 50.0 - 10.0 = 40.0
    assert cart.get_total() == 40.0  # total should be 40.0

def test_percentage_discount_skips_non_discountable_lines():
    cart = ShoppingCart()
    cart.add_item("item1", 100.0, 1, discountable=False)  # not discountable
    cart.add_item("item2", 50.0, 1)
    cart.apply_percentage_discount(10)  # 50.0 * 0.9 = 45.0
    assert cart.get_total() == 145.0  # total should be 145.0

def test_fixed_amount_discount_depletes_only_discountable_portion():
    cart = ShoppingCart()
    cart.add_item("item1", 100.0, 1, discountable=False)  # not discountable
    cart.add_item("item2", 50.0, 1)
    cart.apply_fixed_discount(100.0)  # 50.0 - 100.0 = 0.0 (capped)
    assert cart.get_total() == 50.0  # total should be 50.0

# US-5: Attaching promotional offers to items
def test_buy_x_get_y_offer_groups_units_correctly():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 5)
    cart.apply_buy_x_get_y_offer("item1", 2, 1)  # buy 2 get 1 free
    assert cart.get_line_subtotal("item1") == 40.0  # 10.0 * 4 = 40.0

def test_buy_x_get_y_offer_groups_units_correctly_with_six_units():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 6)
    cart.apply_buy_x_get_y_offer("item1", 2, 1)  # buy 2 get 1 free
    assert cart.get_line_subtotal("item1") == 40.0  # 10.0 * 4 = 40.0

def test_buy_x_get_y_offer_groups_units_correctly_with_four_units():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 4)
    cart.apply_buy_x_get_y_offer("item1", 1, 1)  # buy 1 get 1 free
    assert cart.get_line_subtotal("item1") == 20.0  # 10.0 * 2 = 20.0

def test_buy_x_get_y_offer_groups_units_correctly_with_five_units():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 5)
    cart.apply_buy_x_get_y_offer("item1", 1, 2)  # buy 1 get 2 free
    assert cart.get_line_subtotal("item1") == 20.0  # 10.0 * 2 = 20.0

def test_offer_buy_and_get_must_be_at_least_one():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1)
    with pytest.raises(ValueError, match=r"^buy must be at least 1, got 0$"):
        cart.apply_buy_x_get_y_offer("item1", 0, 1)
    with pytest.raises(ValueError, match=r"^get must be at least 1, got 0$"):
        cart.apply_buy_x_get_y_offer("item1", 1, 0)

def test_bulk_price_offer_reprices_units():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 5)
    cart.apply_bulk_price_offer("item1", 2, 8.0)  # bulk price if quantity >= 2
    assert cart.get_line_subtotal("item1") == 40.0  # 8.0 * 5 = 40.0

def test_bulk_threshold_must_be_at_least_two():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1)
    with pytest.raises(ValueError, match=r"^min_quantity must be at least 2, got 1$"):
        cart.apply_bulk_price_offer("item1", 1, 5.0)

def test_bulk_price_must_be_non_negative():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1)
    with pytest.raises(ValueError, match=r"^unit_price must be non-negative, got -1.0$"):
        cart.apply_bulk_price_offer("item1", 2, -1.0)

def test_offer_attaches_only_to_item_in_cart():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^item item1 is not in the cart$"):
        cart.apply_buy_x_get_y_offer("item1", 2, 1)

def test_offer_attaches_only_to_discountable_item():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1, discountable=False)  # not discountable
    with pytest.raises(ValueError, match=r"^item item1 cannot be combined with discounts$"):
        cart.apply_buy_x_get_y_offer("item1", 2, 1)

def test_offer_attaches_only_to_one_offer_per_item():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1)
    cart.apply_buy_x_get_y_offer("item1", 2, 1)
    with pytest.raises(ValueError, match=r"^item item1 already has an offer$"):
        cart.apply_buy_x_get_y_offer("item1", 1, 1)

def test_offer_item_name_must_not_be_empty():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^item name must not be empty$"):
        cart.apply_buy_x_get_y_offer("", 1, 1)

def test_offers_shape_line_subtotals_before_discounts_apply():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 5)
    cart.apply_buy_x_get_y_offer("item1", 2, 1)  # apply offer
    cart.apply_fixed_discount(5.0)  # apply discount
    assert cart.get_total() == 35.0  # total should be 35.0

# US-6: Enforcing purchase limits
def test_exceeding_item_stock_fails():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1, stock=1)
    with pytest.raises(ValueError, match=r"^only 1 of item1 in stock, requested 2$"):
        cart.add_item("item1", 10.0, 2)

def test_buying_exact_stock_succeeds():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1, stock=1)  # stock = 1
    cart.change_quantity("item1", 1)  # should succeed

def test_stock_zero_rejects_any_quantity():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^only 0 of item1 in stock, requested 1$"):
        cart.add_item("item1", 10.0, 1, stock=0)  # stock = 0

def test_negative_stock_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^stock must be non-negative, got -1$"):
        cart.add_item("item1", 10.0, 1, stock=-1)

def test_exceeding_per_order_cap_fails():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1, max_quantity=1)
    with pytest.raises(ValueError, match=r"^maximum 1 of item1 per order, requested 2$"):
        cart.change_quantity("item1", 2)

def test_per_order_cap_of_one_is_valid():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1, max_quantity=1)  # should succeed
    cart.change_quantity("item1", 1)  # should succeed

def test_per_order_cap_below_one_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match=r"^max_quantity must be at least 1, got 0$"):
        cart.add_item("item1", 10.0, 1, max_quantity=0)

def test_exceeding_item_stock_leaves_cart_unchanged():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1, stock=1)
    try:
        cart.add_item("item1", 10.0, 2)
    except ValueError:
        pass
    assert cart.get_quantity("item1") == 1  # quantity should still be 1
    assert cart.get_total() == 10.0  # total should still be 10.0

def test_exceeding_per_order_cap_leaves_cart_unchanged():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1, max_quantity=1)
    try:
        cart.change_quantity("item1", 2)
    except ValueError:
        pass
    assert cart.get_quantity("item1") == 1  # quantity should still be 1
    assert cart.get_total() == 10.0  # total should still be 10.0