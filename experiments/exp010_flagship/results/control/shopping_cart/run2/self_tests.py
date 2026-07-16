from solution import ShoppingCart

def test_add_item_creates_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    assert cart.get_quantity("apple") == 1  # 1 unit added

def test_add_item_tops_up_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.add_item("apple", 1.00, 2)
    assert cart.get_quantity("apple") == 3  # 1 + 2 units

def test_add_item_without_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00)
    assert cart.get_quantity("apple") == 1  # 1 unit added by default

def test_remove_item_drops_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.remove_item("apple")
    assert cart.get_quantity("apple") == 0  # Line should be removed

def test_change_quantity_reprices_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.change_quantity("apple", 3)
    assert cart.get_quantity("apple") == 3  # Updated to 3 units

def test_set_quantity_to_zero_removes_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.change_quantity("apple", 0)
    assert cart.get_quantity("apple") == 0  # Line should be removed

def test_set_quantity_to_one_keeps_line():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    cart.change_quantity("apple", 1)
    assert cart.get_quantity("apple") == 1  # Line remains as normal update

def test_quantity_of_item_not_in_cart_is_zero():
    cart = ShoppingCart()
    assert cart.get_quantity("apple") == 0  # Item not added yet

def test_line_subtotal_is_rounded():
    cart = ShoppingCart()
    cart.add_item("apple", 1.005, 2)  # 2 * 1.005
    assert cart.get_subtotal("apple") == 2.01  # Subtotal: 2.01

def test_cart_total_is_sum_of_line_subtotals():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)  # 2.00
    cart.add_item("banana", 0.50, 3)  # 1.50
    assert cart.get_total() == 3.50  # Total: 2.00 + 1.50

def test_empty_cart_totals_zero():
    cart = ShoppingCart()
    assert cart.get_total() == 0.0  # Total is 0.0
    assert cart.get_pre_discount_sum() == 0.0  # Pre-discount sum is 0.0

def test_cart_pre_discount_sum():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)  # 2.00
    cart.add_item("banana", 0.50, 3)  # 1.50
    assert cart.get_pre_discount_sum() == 3.50  # Pre-discount sum: 3.50

def test_zero_unit_price_subtotals_to_zero():
    cart = ShoppingCart()
    cart.add_item("apple", 0.00, 2)  # 0.00
    assert cart.get_subtotal("apple") == 0.00  # Subtotal: 0.00

def test_empty_item_name_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="item name must not be empty"):
        cart.add_item("", 1.00, 1)

def test_negative_unit_price_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="unit_price must be non-negative, got -1"):
        cart.add_item("apple", -1.00, 1)

def test_add_item_with_invalid_quantity():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="quantity must be at least 1, got 0"):
        cart.add_item("apple", 1.00, 0)

def test_change_quantity_to_negative_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1)
    with pytest.raises(ValueError, match="quantity must be non-negative, got -1"):
        cart.change_quantity("apple", -1)

def test_remove_non_existing_item_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="item apple is not in the cart"):
        cart.remove_item("apple")

def test_subtotal_of_non_existing_item_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="item apple is not in the cart"):
        cart.get_subtotal("apple")

def test_apply_percentage_discount():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_discount(10)  # 10% off
    assert cart.get_total() == 90.00  # Total after discount

def test_apply_invalid_percentage_discount():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="percent must be greater than 0 and at most 100, got 0"):
        cart.apply_discount(0)

def test_apply_fixed_amount_discount():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_fixed_discount(15.00)  # 15.00 off
    assert cart.get_total() == 85.00  # Total after discount

def test_fixed_discount_cannot_make_total_negative():
    cart = ShoppingCart()
    cart.add_item("apple", 10.00, 1)
    cart.apply_fixed_discount(15.00)  # Should clamp to 0.00
    assert cart.get_total() == 0.00

def test_fixed_discount_must_be_positive():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="amount must be positive, got 0"):
        cart.apply_fixed_discount(0)

def test_discount_application_order():
    cart = ShoppingCart()
    cart.add_item("apple", 100.00, 1)
    cart.apply_fixed_discount(10.00)  # 90.00
    cart.apply_discount(50)  # 45.00
    assert cart.get_total() == 45.00  # Total after discounts

def test_non_discountable_line_skipped_by_percentage_discount():
    cart = ShoppingCart()
    cart.add_item("apple", 50.00, 1, discountable=False)
    cart.add_item("banana", 50.00, 1)
    cart.apply_discount(10)  # 10% off the banana only
    assert cart.get_total() == 95.00  # Total after discount

def test_fixed_discount_only_depletes_discountable_portion():
    cart = ShoppingCart()
    cart.add_item("apple", 50.00, 1, discountable=False)
    cart.add_item("banana", 50.00, 2)
    cart.apply_fixed_discount(30.00)  # Should apply only to banana
    assert cart.get_total() == 70.00  # Total after discount

def test_buy_x_get_y_offer():
    cart = ShoppingCart()
    cart.add_item("apple", 2.00, 6)
    cart.apply_offer("apple", buy=2, get=1)  # Buy 2, get 1 free
    assert cart.get_subtotal("apple") == 12.00  # 4 units charged

def test_invalid_offer_counts_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="buy must be at least 1, got 0"):
        cart.apply_offer("apple", buy=0, get=1)
    with pytest.raises(ValueError, match="get must be at least 1, got 0"):
        cart.apply_offer("apple", buy=1, get=0)

def test_bulk_price_offer():
    cart = ShoppingCart()
    cart.add_item("apple", 2.00, 3)
    cart.apply_bulk_price_offer("apple", min_quantity=3, bulk_price=1.50)
    assert cart.get_subtotal("apple") == 4.50  # 3 units at 1.50

def test_bulk_offer_threshold_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="min_quantity must be at least 2, got 1"):
        cart.apply_bulk_price_offer("apple", min_quantity=1, bulk_price=1.50)

def test_negative_bulk_price_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="unit_price must be non-negative, got -1"):
        cart.apply_bulk_price_offer("apple", min_quantity=2, bulk_price=-1)

def test_offer_attaches_only_to_existing_items():
    cart = ShoppingCart()
    cart.add_item("apple", 2.00, 1)
    cart.apply_offer("banana", buy=1, get=1)  # Banana not in cart
    with pytest.raises(ValueError, match="item banana is not in the cart"):
        cart.apply_offer("banana", buy=1, get=1)

def test_offer_attaches_only_to_discountable_items():
    cart = ShoppingCart()
    cart.add_item("apple", 2.00, 1, discountable=False)
    with pytest.raises(ValueError, match="item apple cannot be combined with discounts"):
        cart.apply_offer("apple", buy=1, get=1)

def test_offer_attaching_more_than_one_rejected():
    cart = ShoppingCart()
    cart.add_item("apple", 2.00, 1)
    cart.apply_offer("apple", buy=1, get=1)  # First offer
    with pytest.raises(ValueError, match="item apple already has an offer"):
        cart.apply_offer("apple", buy=2, get=1)

def test_offer_item_name_not_empty():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="item name must not be empty"):
        cart.apply_offer("", buy=1, get=1)

def test_exceeding_stock_error():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, stock=1)
    with pytest.raises(ValueError, match="only 1 of apple in stock, requested 2"):
        cart.add_item("apple", 1.00, 2)

def test_buying_exact_stock_succeeds():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, stock=1)  # Should succeed
    assert cart.get_quantity("apple") == 1  # 1 unit added

def test_negative_stock_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="stock must be non-negative, got -1"):
        cart.add_item("apple", 1.00, 1, stock=-1)

def test_exceeding_per_order_cap_error():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, max_quantity=1)
    with pytest.raises(ValueError, match="maximum 1 of apple per order, requested 2"):
        cart.add_item("apple", 1.00, 2)

def test_per_order_cap_of_one_is_valid():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 1, max_quantity=1)  # Should succeed
    assert cart.get_quantity("apple") == 1  # 1 unit added

def test_per_order_cap_below_one_rejected():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="max_quantity must be at least 1, got 0"):
        cart.add_item("apple", 1.00, 1, max_quantity=0)