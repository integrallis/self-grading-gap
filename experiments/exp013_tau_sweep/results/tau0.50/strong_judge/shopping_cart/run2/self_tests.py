import pytest
from solution import ShoppingCart

# US-1: Managing the items in the cart

def test_add_item_creates_line():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1)
    assert cart.get_quantity("item1") == 1  # quantity of 1

def test_add_existing_item_tops_up_quantity():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1)
    cart.add_item("item1", 10.0, 2)
    assert cart.get_quantity("item1") == 3  # quantity should be 1 + 2 = 3

def test_add_item_without_quantity_defaults_to_one():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0)
    assert cart.get_quantity("item1") == 1  # default quantity should be 1

def test_remove_item_drops_line():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1)
    cart.remove_item("item1")
    assert cart.get_quantity("item1") == 0  # quantity should be 0
    assert cart.get_total() == 0.0  # total should not include removed item

def test_change_quantity_reprices_line():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1)
    cart.change_quantity("item1", 2)
    assert cart.get_quantity("item1") == 2  # quantity should be 2
    assert cart.get_line_subtotal("item1") == 20.0  # 10.0 * 2 = 20.0

def test_set_quantity_to_zero_removes_line():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1)
    cart.change_quantity("item1", 0)
    assert cart.get_quantity("item1") == 0  # quantity should be 0
    assert cart.get_total() == 0.0  # total should not include removed item

def test_set_quantity_to_one_updates_line():
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
    cart.add_item("item1", 10.0, 2)  # unit price 10.0, quantity 2
    assert cart.get_line_subtotal("item1") == 20.0  # 10.0 * 2 = 20.0

def test_cart_total_is_sum_of_line_subtotals():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 2)  # subtotal 20.0
    cart.add_item("item2", 5.0, 2)   # subtotal 10.0
    assert cart.get_total() == 30.0  # 20.0 + 10.0 = 30.0

def test_empty_cart_totals_zero():
    cart = ShoppingCart()
    assert cart.get_total() == 0.0  # empty cart total should be 0.0
    assert cart.get_pre_discount_sum() == 0.0  # empty cart pre-discount sum should be 0.0

def test_cart_reports_pre_discount_sum():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 2)  # subtotal 20.0
    cart.add_item("item2", 5.0, 2)   # subtotal 10.0
    assert cart.get_pre_discount_sum() == 30.0  # pre-discount sum should be 30.0

def test_zero_unit_price_subtotals_to_zero():
    cart = ShoppingCart()
    cart.add_item("item1", 0.0, 2)  # unit price 0.0, quantity 2
    assert cart.get_line_subtotal("item1") == 0.0  # subtotal should be 0.0

# US-3: Rejecting invalid line operations

def test_empty_item_name_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception, match=r"^item name must not be empty$"):
        cart.add_item("", 10.0, 1)

def test_negative_unit_price_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception, match=r"^unit_price must be non-negative, got -10.0$"):
        cart.add_item("item1", -10.0, 1)

def test_add_item_with_zero_quantity_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception, match=r"^quantity must be at least 1, got 0$"):
        cart.add_item("item1", 10.0, 0)

def test_add_item_with_negative_quantity_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception, match=r"^quantity must be at least 1, got -1$"):
        cart.add_item("item1", 10.0, -1)

def test_change_quantity_to_negative_rejected():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1)
    with pytest.raises(Exception, match=r"^quantity must be non-negative, got -1$"):
        cart.change_quantity("item1", -1)

def test_remove_item_not_in_cart_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception, match=r"^item item1 is not in the cart$"):
        cart.remove_item("item1")

def test_requantifying_item_not_in_cart_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception, match=r"^item item1 is not in the cart$"):
        cart.change_quantity("item1", 1)

def test_subtotal_of_item_not_in_cart_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception, match=r"^item item1 is not in the cart$"):
        cart.get_line_subtotal("item1")

# US-4: Applying storewide discounts

def test_percentage_discount_reduces_total():
    cart = ShoppingCart()
    cart.add_item("item1", 100.0, 1)
    cart.apply_percentage_discount(10)  # 10% off
    assert cart.get_total() == 90.0  # 100.0 - 10% = 90.0

def test_percentage_discount_rejected_if_zero_or_hundred():
    cart = ShoppingCart()
    cart.add_item("item1", 100.0, 1)
    with pytest.raises(Exception, match=r"^percent must be greater than 0 and at most 100, got 0$"):
        cart.apply_percentage_discount(0)
    with pytest.raises(Exception, match=r"^percent must be greater than 0 and at most 100, got 101$"):
        cart.apply_percentage_discount(101)

def test_percentage_discount_valid_1_percent():
    cart = ShoppingCart()
    cart.add_item("item1", 100.0, 1)
    cart.apply_percentage_discount(1)  # 1% off
    assert cart.get_total() == 99.0  # 100.0 - 1% = 99.0

def test_percentage_discount_valid_100_percent():
    cart = ShoppingCart()
    cart.add_item("item1", 100.0, 1)
    cart.apply_percentage_discount(100)  # 100% off
    assert cart.get_total() == 0.0  # total should be 0.0

def test_fixed_amount_discount_reduces_total():
    cart = ShoppingCart()
    cart.add_item("item1", 100.0, 1)
    cart.apply_fixed_discount(15.0)  # $15.00 off
    assert cart.get_total() == 85.0  # 100.0 - 15.0 = 85.0

def test_fixed_discount_never_below_zero():
    cart = ShoppingCart()
    cart.add_item("item1", 100.0, 1)
    cart.apply_fixed_discount(150.0)  # $150.00 off
    assert cart.get_total() == 0.0  # total can't go below zero

def test_fixed_discount_must_be_positive():
    cart = ShoppingCart()
    cart.add_item("item1", 100.0, 1)
    with pytest.raises(Exception, match=r"^amount must be positive, got 0$"):
        cart.apply_fixed_discount(0)
    with pytest.raises(Exception, match=r"^amount must be positive, got -10$"):
        cart.apply_fixed_discount(-10)

def test_fixed_discount_valid_sub_unit():
    cart = ShoppingCart()
    cart.add_item("item1", 10.00, 1)
    cart.apply_fixed_discount(0.75)  # $0.75 off
    assert cart.get_total() == 9.25  # 10.00 - 0.75 = 9.25

# Discount registration order tests
def test_discount_registration_order_fixed_first():
    cart = ShoppingCart()
    cart.add_item("item1", 100.0, 1)
    cart.apply_fixed_discount(10.0)  # $10.00 off
    cart.apply_percentage_discount(50)  # 50% off
    assert cart.get_total() == 45.0  # (100.0 - 10.0) * 0.5 = 45.0

def test_discount_registration_order_percentage_first():
    cart = ShoppingCart()
    cart.add_item("item1", 100.0, 1)
    cart.apply_percentage_discount(50)  # 50% off
    cart.apply_fixed_discount(10.0)  # $10.00 off
    assert cart.get_total() == 40.0  # (100.0 * 0.5) - 10.0 = 40.0

# US-5: Attaching promotional offers to items

def test_offer_attached_only_to_existing_item():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1)
    cart.attach_offer("item1", "buy_1_get_1_free")  # valid
    with pytest.raises(Exception, match=r"^item item2 is not in the cart$"):
        cart.attach_offer("item2", "buy_1_get_1_free")

def test_offer_can_only_be_attached_once():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1)
    cart.attach_offer("item1", "buy_1_get_1_free")  # valid
    with pytest.raises(Exception, match=r"^item item1 already has an offer$"):
        cart.attach_offer("item1", "buy_1_get_1_free")

def test_offer_with_empty_name_rejected():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1)
    with pytest.raises(Exception, match=r"^item name must not be empty$"):
        cart.attach_offer("", "buy_1_get_1_free")

def test_offer_attached_to_non_discountable_item_rejected():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1)
    cart.attach_offer("item1", "buy_1_get_1_free")  # valid
    # Mark as non-discountable
    with pytest.raises(Exception, match=r"^item item1 cannot be combined with discounts$"):
        cart.attach_offer("item1", "buy_1_get_1_free")

# Additional tests for US-5: Promotional offers

def test_buy_two_get_one_free_offer():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 6)  # Buy 6
    cart.attach_offer("item1", "buy_2_get_1_free")  # Offer
    assert cart.get_line_subtotal("item1") == 40.0  # Pay for 4, 10 * 4 = 40.0

def test_buy_one_get_one_free_offer():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 4)  # Buy 4
    cart.attach_offer("item1", "buy_1_get_1_free")  # Offer
    assert cart.get_line_subtotal("item1") == 20.0  # Pay for 2, 10 * 2 = 20.0

def test_buy_one_get_two_free_offer():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 5)  # Buy 5
    cart.attach_offer("item1", "buy_1_get_2_free")  # Offer
    assert cart.get_line_subtotal("item1") == 20.0  # Pay for 2, 10 * 2 = 20.0

def test_buy_get_offer_counts_validation():
    cart = ShoppingCart()
    with pytest.raises(Exception, match=r"^buy must be at least 1, got 0$"):
        cart.attach_offer("item1", "buy_0_get_1_free")
    with pytest.raises(Exception, match=r"^get must be at least 1, got 0$"):
        cart.attach_offer("item1", "buy_1_get_0_free")
    with pytest.raises(Exception, match=r"^buy must be at least 1, got -1$"):
        cart.attach_offer("item1", "buy_-1_get_1_free")
    with pytest.raises(Exception, match=r"^get must be at least 1, got -1$"):
        cart.attach_offer("item1", "buy_1_get_-1_free")

# Bulk price tests
def test_bulk_price_offer_threshold_validation():
    cart = ShoppingCart()
    with pytest.raises(Exception, match=r"^min_quantity must be at least 2, got 1$"):
        cart.attach_offer("item1", "buy_1_get_1_free", threshold=1, bulk_price=5.0)
    with pytest.raises(Exception, match=r"^unit_price must be non-negative, got -1$"):
        cart.attach_offer("item1", "buy_1_get_1_free", threshold=2, bulk_price=-1)

def test_bulk_price_offer_applies_correctly():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 3)  # Add 3
    cart.attach_offer("item1", "bulk_price", threshold=2, bulk_price=5.0)
    assert cart.get_line_subtotal("item1") == 15.0  # 5.0 * 3 = 15.0

# US-6: Enforcing purchase limits

def test_exceeding_stock_limit_rejected():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1, stock=1)  # item in stock = 1
    with pytest.raises(Exception, match=r"^only 1 of item1 in stock, requested 2$"):
        cart.add_item("item1", 10.0, 2)

def test_buying_exact_stock_succeeds():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1, stock=1)  # item in stock = 1
    assert cart.get_quantity("item1") == 1  # should be 1

def test_negative_stock_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception, match=r"^stock must be non-negative, got -1$"):
        cart.add_item("item1", 10.0, 1, stock=-1)

def test_exceeding_per_order_cap_rejected():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1, max_quantity=1)  # cap = 1
    with pytest.raises(Exception, match=r"^maximum 1 of item1 per order, requested 2$"):
        cart.add_item("item1", 10.0, 2)

def test_per_order_cap_of_one_is_valid():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1, max_quantity=1)  # cap = 1
    cart.change_quantity("item1", 1)  # should succeed

def test_per_order_cap_below_one_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception, match=r"^max_quantity must be at least 1, got 0$"):
        cart.add_item("item1", 10.0, 1, max_quantity=0)

def test_first_add_exceeding_stock_limit_rejected():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1, stock=1)  # item in stock = 1
    with pytest.raises(Exception, match=r"^only 1 of item1 in stock, requested 2$"):
        cart.add_item("item1", 10.0, 2)

def test_first_add_exceeding_per_order_cap_rejected():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1, max_quantity=1)  # cap = 1
    with pytest.raises(Exception, match=r"^maximum 1 of item1 per order, requested 2$"):
        cart.add_item("item1", 10.0, 2)

def test_quantity_change_exceeding_stock_limit_rejected():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1, stock=1)  # item in stock = 1
    cart.change_quantity("item1", 1)  # change to 1
    with pytest.raises(Exception, match=r"^only 1 of item1 in stock, requested 2$"):
        cart.change_quantity("item1", 2)

def test_quantity_change_exceeding_per_order_cap_rejected():
    cart = ShoppingCart()
    cart.add_item("item1", 10.0, 1, max_quantity=1)  # cap = 1
    cart.change_quantity("item1", 1)  # change to 1
    with pytest.raises(Exception, match=r"^maximum 1 of item1 per order, requested 2$"):
        cart.change_quantity("item1", 2)

def test_first_add_exceeding_stock_limit_genuine():
    cart = ShoppingCart()
    with pytest.raises(Exception, match=r"^only 1 of item1 in stock, requested 2$"):
        cart.add_item("item1", 10.0, 2, stock=1)  # Attempt to add 2 with stock 1

def test_first_add_exceeding_per_order_cap_genuine():
    cart = ShoppingCart()
    with pytest.raises(Exception, match=r"^maximum 1 of item1 per order, requested 2$"):
        cart.add_item("item1", 10.0, 2, max_quantity=1)  # Attempt to add 2 with max cap of 1

def test_negative_max_quantity_rejected():
    cart = ShoppingCart()
    with pytest.raises(Exception, match=r"^max_quantity must be at least 1, got -1$"):
        cart.add_item("item1", 10.0, 1, max_quantity=-1)