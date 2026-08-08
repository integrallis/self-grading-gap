import pytest
from solution import ShoppingCart

# US-1: Managing the items in the cart

def test_add_item_creates_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)
    assert cart.get_quantity("apple") == 2

def test_add_item_tops_up_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)
    cart.add_item("apple", 1.00, 3)
    assert cart.get_quantity("apple") == 5

def test_add_item_without_quantity_defaults_to_one():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00)
    assert cart.get_quantity("apple") == 1

def test_remove_item_drops_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)
    cart.remove_item("apple")
    assert cart.get_quantity("apple") == 0
    assert cart.get_total() == 0.0  # Check total after removal

def test_change_quantity_reprices_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)
    cart.change_quantity("apple", 3)
    assert cart.get_quantity("apple") == 3
    assert cart.get_subtotal("apple") == 3.00  # 1.00 * 3 = 3.00

def test_set_quantity_to_zero_removes_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)
    cart.change_quantity("apple", 0)
    assert cart.get_quantity("apple") == 0

def test_set_quantity_to_one_updates_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)
    cart.change_quantity("apple", 1)
    assert cart.get_quantity("apple") == 1

def test_quantity_of_item_not_added_is_zero():
    cart = ShoppingCart()
    assert cart.get_quantity("apple") == 0

# US-2: Pricing the order

def test_line_subtotal_is_unit_price_times_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)  # 1.00 * 3 = 3.00
    assert cart.get_subtotal("apple") == 3.00

def test_cart_total_is_sum_of_line_subtotals():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)  # 1.00 * 3 = 3.00
    cart.add_item("banana", 2.00, 2) # 2.00 * 2 = 4.00
    assert cart.get_total() == 7.00  # 3.00 + 4.00 = 7.00

def test_empty_cart_totals_zero():
    cart = ShoppingCart()
    assert cart.get_total() == 0.0
    assert cart.get_pre_discount_sum() == 0.0  # Ensure pre-discount sum is also zero

def test_cart_reports_pre_discount_sum():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)  # 1.00 * 3 = 3.00
    cart.add_item("banana", 2.00, 2) # 2.00 * 2 = 4.00
    assert cart.get_pre_discount_sum() == 7.00  # 3.00 + 4.00 = 7.00

def test_unit_price_of_zero_subtotals_to_zero():
    cart = ShoppingCart()
    cart.add_item("apple", 0.00, 3)  # 0.00 * 3 = 0.00
    assert cart.get_subtotal("apple") == 0.00

def test_line_subtotal_rounding():
    cart = ShoppingCart()
    cart.add_item("apple", 1.005, 2)  # 1.005 * 2 = 2.01
    assert cart.get_subtotal("apple") == 2.01  # Rounded to 2.01

def test_total_rounding():
    cart = ShoppingCart()
    cart.add_item("apple", 1.005, 2)  # 1.005 * 2 = 2.01
    cart.apply_fixed_discount(0.02)  # 0.02 off
    assert cart.get_total() == 1.99  # 2.01 - 0.02

# US-3: Rejecting invalid line operations

def test_empty_item_name_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.add_item("", 1.00, 1)
    assert str(exc.value) == "item name must not be empty"

def test_negative_unit_price_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(Exception) as exc:
        cart.add_item("apple", -1.00, 1)
    assert str(exc.value) == "unit_price must be non-negative, got -1.00"

def test_add_fewer_than_one_unit_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.add_item("apple", 1.00, 0)
    assert str(exc.value) == "quantity must be at least 1, got 0"

def test_change_quantity_to_negative_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(Exception) as exc:
        cart.change_quantity("apple", -1)
    assert str(exc.value) == "quantity must be non-negative, got -1"

def test_remove_item_not_in_cart_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.remove_item("apple")
    assert str(exc.value) == "item apple is not in the cart"

def test_requantify_item_not_in_cart_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.change_quantity("apple", 1)
    assert str(exc.value) == "item apple is not in the cart"

def test_get_subtotal_item_not_in_cart_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.get_subtotal("apple")
    assert str(exc.value) == "item apple is not in the cart"

# US-4: Applying storewide discounts

def test_percentage_discount_reduces_total():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)  # 100.00
    cart.apply_percentage_discount(10)  # 10% off
    assert cart.get_total() == 90.00  # 100.00 - 10.00 = 90.00

def test_percentage_discount_of_one_percent_accepted():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)  # 100.00
    cart.apply_percentage_discount(1)  # 1% off
    assert cart.get_total() == 99.00  # 100.00 - 1.00 = 99.00

def test_percentage_discount_of_one_hundred_percent_accepted():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)  # 100.00
    cart.apply_percentage_discount(100)  # 100% off
    assert cart.get_total() == 0.00  # Total should be zero

def test_percentage_discount_must_be_valid():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.apply_percentage_discount(-1)
    assert str(exc.value) == "percent must be greater than 0 and at most 100, got -1"
    
    with pytest.raises(Exception) as exc:
        cart.apply_percentage_discount(101)
    assert str(exc.value) == "percent must be greater than 0 and at most 100, got 101"

def test_fixed_amount_discount_subtracts_from_total():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)  # 100.00
    cart.apply_fixed_discount(15.00)  # 15.00 off
    assert cart.get_total() == 85.00  # 100.00 - 15.00 = 85.00

def test_fixed_amount_discount_never_below_zero():
    cart = ShoppingCart()
    cart.add_item("apple", 10.00, 1)  # 10.00
    cart.apply_fixed_discount(15.00)  # Attempt to apply 15.00 off
    assert cart.get_total() == 0.00  # Total cannot go below 0.00

def test_fixed_amount_discount_must_be_positive():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.apply_fixed_discount(-1)
    assert str(exc.value) == "amount must be positive, got -1"

def test_discount_application_order():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)  # 100.00
    cart.apply_fixed_discount(10.00)  # 10.00 off
    cart.apply_percentage_discount(50)  # 50% off
    assert cart.get_total() == 45.00  # (100.00 - 10.00) * 0.5 = 45.00

def test_percentage_discount_skips_non_discountable_lines():
    cart = ShoppingCart()
    cart.add_item("apple", 50.00, 1, discountable=False)  # 50.00 non-discountable
    cart.add_item("banana", 30.00, 1)  # 30.00 discountable
    cart.apply_percentage_discount(10)  # 10% off on banana
    assert cart.get_total() == 77.00  # 50.00 + (30.00 - 3.00) = 77.00

def test_fixed_discount_depletes_discountable_portion():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)  # 100.00
    cart.add_item("banana", 50.00, 1, discountable=False)  # 50.00 non-discountable
    cart.apply_fixed_discount(30.00)  # 30.00 off
    assert cart.get_total() == 120.00  # 100.00 - 30.00 + 50.00 = 120.00

# US-5: Attaching promotional offers to items

def test_buy_x_get_y_free_offer():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)  # 1.00 * 3 = 3.00
    cart.attach_buy_x_get_y_free_offer("apple", 2, 1)  # Buy 2 get 1 free
    assert cart.get_subtotal("apple") == 2.00  # Pay for 2 of 3

def test_buy_2_get_1_free_with_5_units():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 5)  # 1.00 * 5 = 5.00
    cart.attach_buy_x_get_y_free_offer("apple", 2, 1)  # Buy 2 get 1 free
    assert cart.get_subtotal("apple") == 4.00  # Pay for 4 of 5

def test_buy_1_get_1_free_with_4_units():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 4)  # 1.00 * 4 = 4.00
    cart.attach_buy_x_get_y_free_offer("apple", 1, 1)  # Buy 1 get 1 free
    assert cart.get_subtotal("apple") == 2.00  # Pay for 2 of 4

def test_buy_1_get_2_free_with_5_units():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 5)  # 1.00 * 5 = 5.00
    cart.attach_buy_x_get_y_free_offer("apple", 1, 2)  # Buy 1 get 2 free
    assert cart.get_subtotal("apple") == 1.00  # Pay for 1 of 5

def test_offer_rejected_if_item_not_in_cart():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.attach_buy_x_get_y_free_offer("apple", 2, 1)
    assert str(exc.value) == "item apple is not in the cart"

def test_offer_rejected_if_item_is_non_discountable():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, discountable=False)  # non-discountable
    with pytest.raises(Exception) as exc:
        cart.attach_buy_x_get_y_free_offer("apple", 2, 1)
    assert str(exc.value) == "item apple cannot be combined with discounts"

def test_offer_cannot_be_attached_if_already_has_one():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.attach_buy_x_get_y_free_offer("apple", 2, 1)
    with pytest.raises(Exception) as exc:
        cart.attach_buy_x_get_y_free_offer("apple", 1, 1)
    assert str(exc.value) == "item apple already has an offer"

def test_offer_minimums_must_be_respected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(Exception) as exc:
        cart.attach_buy_x_get_y_free_offer("apple", 0, 1)
    assert str(exc.value) == "buy must be at least 1, got 0"
    with pytest.raises(Exception) as exc:
        cart.attach_buy_x_get_y_free_offer("apple", 1, 0)
    assert str(exc.value) == "get must be at least 1, got 0"

def test_bulk_price_offer():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.attach_bulk_price_offer("apple", 2, 0.80)  # bulk price of 0.80 for 2 or more
    cart.change_quantity("apple", 2)
    assert cart.get_subtotal("apple") == 1.60  # 0.80 * 2

def test_bulk_price_offer_below_threshold_retains_regular_price():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.attach_bulk_price_offer("apple", 2, 0.80)  # bulk price of 0.80 for 2 or more
    cart.change_quantity("apple", 1)
    assert cart.get_subtotal("apple") == 1.00  # Regular price

def test_bulk_price_offer_rejected_if_threshold_invalid():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(Exception) as exc:
        cart.attach_bulk_price_offer("apple", 1, 0.80)
    assert str(exc.value) == "min_quantity must be at least 2, got 1"

def test_bulk_price_offer_rejected_if_negative_price():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(Exception) as exc:
        cart.attach_bulk_price_offer("apple", 2, -1.00)
    assert str(exc.value) == "unit_price must be non-negative, got -1.00"

def test_offer_item_name_not_empty():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.attach_buy_x_get_y_free_offer("", 1, 1)
    assert str(exc.value) == "item name must not be empty"

def test_offer_reshapes_line_subtotal_before_discount():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)  # 1.00 * 3 = 3.00
    cart.attach_buy_x_get_y_free_offer("apple", 2, 1)  # Buy 2 get 1 free
    cart.apply_fixed_discount(0.50)  # Apply 0.50 off
    assert cart.get_total() == 1.50  # Pay for 2 of 3, with 0.50 off

# US-6: Enforcing purchase limits

def test_exceeding_stock_limit_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, stock=2)  # max 2 in stock
    with pytest.raises(Exception) as exc:
        cart.add_item("apple", 1.00, 3)  # request 3
    assert str(exc.value) == "only 2 of apple in stock, requested 3"

def test_buying_exact_stock_succeeds():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, stock=1)  # max 1 in stock
    assert cart.get_quantity("apple") == 1  # Quantity should equal stock

def test_stock_zero_rejects_quantity_of_one():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 0, stock=0)  # max 0 in stock
    with pytest.raises(Exception) as exc:
        cart.add_item("apple", 1.00, 1)  # request 1
    assert str(exc.value) == "only 0 of apple in stock, requested 1"

def test_negative_stock_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.add_item("apple", 1.00, 1, stock=-1)
    assert str(exc.value) == "stock must be non-negative, got -1"

def test_exceeding_per_order_cap_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, max_quantity=1)  # max 1 per order
    with pytest.raises(Exception) as exc:
        cart.add_item("apple", 1.00, 2)  # request 2
    assert str(exc.value) == "maximum 1 of apple per order, requested 2"

def test_per_order_cap_of_one_is_valid():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, max_quantity=1)  # max 1 per order
    cart.change_quantity("apple", 1)  # change to exact cap

def test_per_order_cap_below_one_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception) as exc:
        cart.add_item("apple", 1.00, 1, max_quantity=0)
    assert str(exc.value) == "max_quantity must be at least 1, got 0"