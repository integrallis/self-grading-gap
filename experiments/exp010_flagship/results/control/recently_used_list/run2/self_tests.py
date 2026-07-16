from solution import RecentlyUsedItemsList

def test_add_item_increases_count():
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    assert ruil.count() == 1  # 1 item added

def test_add_item_stores_correct_order():
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    ruil.add("item2")
    assert ruil.get_all() == ["item2", "item1"]  # most recently added first

def test_add_duplicate_item_does_not_increase_count():
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    ruil.add("item1")
    assert ruil.count() == 1  # count remains 1 for duplicate

def test_add_item_exceeds_capacity_drops_oldest_entry():
    ruil = RecentlyUsedItemsList(capacity=2)
    ruil.add("item1")
    ruil.add("item2")
    ruil.add("item3")
    assert ruil.get_all() == ["item3", "item2"]  # oldest "item1" should be dropped

def test_custom_capacity_is_set_correctly():
    ruil = RecentlyUsedItemsList(capacity=3)
    assert ruil.capacity() == 3  # capacity should be 3

def test_fetch_item_by_position():
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    ruil.add("item2")
    assert ruil.get(0) == "item2"  # position 0 is most recent
    assert ruil.get(1) == "item1"  # position 1 is older

def test_fetch_item_by_invalid_high_position():
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    ruil.add("item2")
    with pytest.raises(IndexError, match="supplied index [2] should not greater than [1]."):
        ruil.get(2)  # invalid position

def test_fetch_item_by_invalid_negative_position():
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    ruil.add("item2")
    with pytest.raises(IndexError, match="supplied index [-1] should be non-negative and not greater than [1]."):
        ruil.get(-1)  # negative position

def test_add_empty_entry_rejected():
    ruil = RecentlyUsedItemsList()
    with pytest.raises(ValueError, match="List items should not be Empty or Null. But it was []"):
        ruil.add("")  # adding empty string

def test_add_none_entry_rejected():
    ruil = RecentlyUsedItemsList()
    with pytest.raises(ValueError, match="List items should not be Empty or Null. But it was [None]"):
        ruil.add(None)  # adding None