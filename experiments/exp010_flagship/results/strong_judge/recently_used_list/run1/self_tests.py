from solution import RecentlyUsedItemsList

def test_add_item_keeps_count():
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    assert ruil.count() == 1  # 1 item added

def test_read_whole_list_most_recent_first():
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    ruil.add("item2")
    assert ruil.get_all() == ["item2", "item1"]  # Newest first

def test_add_duplicate_item_does_not_increase_count():
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    ruil.add("item1")  # Adding the same item again
    assert ruil.count() == 1  # Count should remain 1

def test_add_duplicate_item_does_not_consume_capacity():
    ruil = RecentlyUsedItemsList(capacity=3)
    ruil.add("item1")
    ruil.add("item1")  # Adding the same item again
    assert ruil.count() == 1  # Count should remain 1
    assert ruil.get_all() == ["item1"]  # Only item1 should be present

def test_default_capacity_is_five():
    ruil = RecentlyUsedItemsList()
    assert ruil.capacity() == 5  # Default capacity

def test_custom_capacity_can_be_set():
    ruil = RecentlyUsedItemsList(capacity=3)
    assert ruil.capacity() == 3  # Custom capacity

def test_adding_to_full_list_drops_oldest():
    ruil = RecentlyUsedItemsList()
    for i in range(6):  # Adding 6 items
        ruil.add(f"item{i}")
    assert ruil.get_all() == ["item5", "item4", "item3", "item2", "item1"]  # Oldest "item0" dropped

def test_adding_to_full_custom_capacity_drops_oldest():
    ruil = RecentlyUsedItemsList(capacity=3)
    for i in range(4):  # Adding 4 items
        ruil.add(f"item{i}")
    assert ruil.get_all() == ["item3", "item2", "item1"]  # Oldest "item0" dropped

def test_get_item_by_position():
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    ruil.add("item2")
    assert ruil.get(0) == "item2"  # Position 0 is the most recent
    assert ruil.get(1) == "item1"  # Position 1 is the second most recent

def test_get_out_of_bounds_position():
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    ruil.add("item2")
    message = ""
    try:
        ruil.get(2)  # Out of bounds
    except Exception as e:
        message = str(e)
    assert message == "supplied index [2] should not greater than [1]."  # Error message check

def test_get_negative_position():
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    ruil.add("item2")
    message = ""
    try:
        ruil.get(-1)  # Negative position
    except Exception as e:
        message = str(e)
    assert message == "supplied index [-1] should be non-negative and not greater than [1]."  # Error message check

def test_add_empty_item_rejected():
    ruil = RecentlyUsedItemsList()
    message = ""
    try:
        ruil.add("")  # Empty string
    except Exception as e:
        message = str(e)
    assert message == "List items should not be Empty or Null. But it was []"  # Error message check

def test_add_none_item_rejected():
    ruil = RecentlyUsedItemsList()
    message = ""
    try:
        ruil.add(None)  # None value
    except Exception as e:
        message = str(e)
    assert message == "List items should not be Empty or Null. But it was [None]"  # Error message check

def test_add_duplicate_and_check_capacity():
    ruil = RecentlyUsedItemsList(capacity=3)
    ruil.add("a")
    ruil.add("b")
    ruil.add("c")
    ruil.add("b")  # Reusing "b"
    ruil.add("d")  # Should drop "a"
    assert ruil.count() == 3  # Should still hold 3 items
    assert ruil.get_all() == ["d", "b", "c"]  # "a" should be dropped

def test_reusing_item_moves_to_front():
    ruil = RecentlyUsedItemsList()
    ruil.add("a")
    ruil.add("b")
    ruil.add("a")  # Reusing "a"
    assert ruil.get_all() == ["a", "b"]  # "a" should be most recent