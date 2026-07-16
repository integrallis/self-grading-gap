import pytest
from solution import ShoppingCart

# User Stories: Managing the items in the cart

def test_add_item_creates_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    assert cart.get_quantity("apple") == 1  # AC-1.1

def test_add_item_tops_up_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.add_item("apple", 1.00, 2)
    assert cart.get_quantity("apple") == 3  # AC-1.2

def test_add_item_without_quantity_adds_one():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00)
    assert cart.get_quantity("apple") == 1  # AC-1.3

def test_remove_item_drops_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.remove_item("apple")
    assert cart.get_quantity("apple") == 0  # AC-1.4

def test_change_line_quantity_reprices():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.change_quantity("apple", 3)
    assert cart.get_quantity("apple") == 3  # AC-1.5

def test_set_quantity_to_zero_removes_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.change_quantity("apple", 0)
    assert cart.get_quantity("apple") == 0  # AC-1.6

def test_quantity_of_item_not_added_is_zero():
    cart = ShoppingCart()
    assert cart.get_quantity("apple") == 0  # AC-1.7

# User Stories: Pricing the order

def test_line_subtotal_is_correct():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)
    assert cart.get_subtotal("apple") == 3.00  # AC-2.1

def test_cart_total_is_sum_of_line_subtotals():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)
    cart.add_item("banana", 0.50, 4)
    assert cart.get_total() == 5.00  # AC-2.2

def test_empty_cart_totals_zero():
    cart = ShoppingCart()
    assert cart.get_total() == 0.0  # AC-2.3
    assert cart.get_pre_discount_sum() == 0.0  # AC-2.3

def test_cart_pre_discount_sum():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)
    cart.add_item("banana", 0.50, 2)
    assert cart.get_pre_discount_sum() == 4.00  # AC-2.4

def test_zero_unit_price_subtotals_to_zero():
    cart = ShoppingCart()
    cart.add_item("apple", 0.00, 3)
    assert cart.get_subtotal("apple") == 0.00  # AC-2.5

# User Stories: Rejecting invalid line operations

def test_empty_item_name_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="item name must not be empty"):
        cart.add_item("", 1.00, 1)  # AC-3.1

def test_negative_unit_price_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="unit_price must be non-negative, got -1.0"):
        cart.add_item("apple", -1.00, 1)  # AC-3.2

def test_add_fewer_than_one_unit_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="quantity must be at least 1, got 0"):
        cart.add_item("apple", 1.00, 0)  # AC-3.3

def test_change_quantity_to_negative_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(ValueError, match="quantity must be non-negative, got -1"):
        cart.change_quantity("apple", -1)  # AC-3.4

def test_remove_nonexistent_item_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="item apple is not in the cart"):
        cart.remove_item("apple")  # AC-3.5

def test_requantify_nonexistent_item_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="item apple is not in the cart"):
        cart.change_quantity("apple", 1)  # AC-3.5

def test_subtotal_nonexistent_item_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="item apple is not in the cart"):
        cart.get_subtotal("apple")  # AC-3.5

# User Stories: Applying storewide discounts

def test_percentage_discount_reduces_total():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_percentage_discount(10)
    assert cart.get_total() == 90.00  # AC-4.1

def test_percentage_discount_must_be_valid():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    with pytest.raises(ValueError, match="percent must be greater than 0 and at most 100, got 0"):
        cart.apply_percentage_discount(0)  # AC-4.2

def test_fixed_amount_discount_reduces_total():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_fixed_amount_discount(15.00)
    assert cart.get_total() == 85.00  # AC-4.3

def test_fixed_amount_discount_never_below_zero():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_fixed_amount_discount(150.00)
    assert cart.get_total() == 0.00  # AC-4.4

def test_fixed_amount_discount_must_be_positive():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    with pytest.raises(ValueError, match="amount must be positive, got 0"):
        cart.apply_fixed_amount_discount(0)  # AC-4.5

def test_discounts_apply_in_order():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_fixed_amount_discount(10.00)  # 90.00
    cart.apply_percentage_discount(50)  # 45.00
    assert cart.get_total() == 45.00  # AC-4.6

def test_percentage_discount_skips_non_discountable_lines():
    cart = ShoppingCart()
    cart.add_item("apple", 50.00, 1, discountable=True)
    cart.add_item("banana", 50.00, 1, discountable=False)
    cart.apply_percentage_discount(10.00)  # 50.00 (banana not discounted)
    assert cart.get_total() == 95.00  # AC-4.7

def test_fixed_discount_depletes_only_discountable_portion():
    cart = ShoppingCart()
    cart.add_item("apple", 50.00, 1, discountable=True)
    cart.add_item("banana", 50.00, 1, discountable=False)
    cart.apply_fixed_amount_discount(30.00)  # 50.00 (banana not discounted)
    assert cart.get_total() == 20.00  # AC-4.8

# User Stories: Attaching promotional offers to items

def test_buy_x_get_y_free_offer():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 6)
    cart.add_offer("apple", buy=2, get=1)  # Buy 2 get 1 free
    assert cart.get_subtotal("apple") == 4.00  # AC-5.1

def test_invalid_buy_x_get_y_offer_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(ValueError, match="buy must be at least 1, got 0"):
        cart.add_offer("apple", buy=0, get=1)  # AC-5.2
    with pytest.raises(ValueError, match="get must be at least 1, got 0"):
        cart.add_offer("apple", buy=1, get=0)  # AC-5.2

def test_bulk_price_offer_reprices_units():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)
    cart.add_offer("apple", min_quantity=2, bulk_price=0.50)  # Bulk price
    assert cart.get_subtotal("apple") == 1.50  # AC-5.3

def test_invalid_bulk_price_offer_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(ValueError, match="min_quantity must be at least 2, got 1"):
        cart.add_offer("apple", min_quantity=1, bulk_price=0.50)  # AC-5.4
    with pytest.raises(ValueError, match="unit_price must be non-negative, got -1"):
        cart.add_offer("apple", min_quantity=2, bulk_price=-1)  # AC-5.4

def test_offer_attaches_to_item_in_cart():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.add_offer("apple", buy=1, get=1)  # valid
    with pytest.raises(ValueError, match="item banana is not in the cart"):
        cart.add_offer("banana", buy=1, get=1)  # AC-5.5

def test_offer_cannot_combine_with_discount():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, discountable=False)
    with pytest.raises(ValueError, match="item apple cannot be combined with discounts"):
        cart.add_offer("apple", buy=1, get=1)  # AC-5.5

def test_offer_can_only_attach_one_per_item():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.add_offer("apple", buy=1, get=1)  # valid
    with pytest.raises(ValueError, match="item apple already has an offer"):
        cart.add_offer("apple", buy=2, get=1)  # AC-5.5

def test_offer_item_name_must_not_be_empty():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="item name must not be empty"):
        cart.add_offer("", buy=1, get=1)  # AC-5.6

def test_offers_shape_line_subtotals_before_cart_discounts():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 3)
    cart.add_offer("apple", buy=2, get=1)  # 2 paid, 1 free
    cart.apply_fixed_amount_discount(1.00)  # Total after offer is 2.00, discount 1.00
    assert cart.get_total() == 1.00  # AC-5.7

# User Stories: Enforcing purchase limits

def test_exceeding_item_stock_is_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, stock=5)
    with pytest.raises(ValueError, match="only 5 of apple in stock, requested 6"):
        cart.add_item("apple", 1.00, 6)  # AC-6.1

def test_buying_exact_stock_succeeds():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 5, stock=5)  # This should succeed

def test_negative_stock_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="stock must be non-negative, got -1"):
        cart.add_item("apple", 1.00, 1, stock=-1)  # AC-6.3

def test_exceeding_per_order_cap_is_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, max_quantity=2)
    with pytest.raises(ValueError, match="maximum 2 of apple per order, requested 3"):
        cart.add_item("apple", 1.00, 3)  # AC-6.4

def test_per_order_cap_of_one_is_valid():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, max_quantity=1)  # This should succeed

def test_per_order_cap_below_one_is_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="max_quantity must be at least 1, got 0"):
        cart.add_item("apple", 1.00, 1, max_quantity=0)  # AC-6.6