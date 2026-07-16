from solution import RecentlyUsedItemsList

def test_add_item_increments_count_and_keeps_item():
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    assert ruil.count() == 1  # Expect count to be 1 after adding one item
    assert ruil.get(0) == "item1"  # Expect to retrieve "item1" at position 0

def test_read_whole_list_returns_items_most_recent_first():
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    ruil.add("item2")
    assert ruil.get_all() == ["item2", "item1"]  # Newest first order

def test_add_duplicate_item_does_not_increase_count():
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    ruil.add("item1")  # Duplicate item
    assert ruil.count() == 1  # Count should still be 1

def test_add_item_to_full_list_drops_oldest_entry():
    ruil = RecentlyUsedItemsList()
    for i in range(5):  # Fill to capacity
        ruil.add(f"item{i}")
    ruil.add("item5")  # This should drop "item0"
    assert ruil.get_all() == ["item5", "item4", "item3", "item2", "item1"]  # "item0" should be dropped

def test_custom_capacity():
    ruil = RecentlyUsedItemsList(capacity=3)
    ruil.add("item1")
    ruil.add("item2")
    ruil.add("item3")
    ruil.add("item4")  # This should drop "item1"
    assert ruil.get_all() == ["item4", "item3", "item2"]  # Check the order and capacity

def test_read_item_by_position():
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    ruil.add("item2")
    assert ruil.get(0) == "item2"  # Most recent item
    assert ruil.get(1) == "item1"  # Second most recent item

def test_rejects_position_past_last_item():
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    ruil.add("item2")
    error_message = "supplied index [2] should not greater than [1]."
    with pytest.raises(IndexError, match=error_message):
        ruil.get(2)  # Invalid position

def test_rejects_negative_position():
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    ruil.add("item2")
    error_message = "supplied index [-1] should be non-negative and not greater than [1]."
    with pytest.raises(IndexError, match=error_message):
        ruil.get(-1)  # Invalid negative position

def test_add_missing_value_rejected():
    ruil = RecentlyUsedItemsList()
    error_message = "List items should not be Empty or Null. But it was [None]"
    with pytest.raises(ValueError, match=error_message):
        ruil.add(None)  # Adding None should raise error

def test_add_empty_text_rejected():
    ruil = RecentlyUsedItemsList()
    error_message = "List items should not be Empty or Null. But it was []"
    with pytest.raises(ValueError, match=error_message):
        ruil.add("")  # Adding empty string should raise error