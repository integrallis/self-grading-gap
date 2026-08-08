import pytest
from solution import RecentlyUsedItemsList

def test_add_item_increases_count():
    # Adding one item should increase the count to 1
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    assert ruil.count() == 1

def test_read_list_returns_most_recent_first():
    # Adding items should return them in most-recently-added-first order
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    ruil.add("item2")
    ruil.add("item3")
    assert ruil.read() == ["item3", "item2", "item1"]

def test_add_duplicate_item_does_not_increase_count():
    # Adding a duplicate item should not increase the count
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    ruil.add("item1")
    assert ruil.count() == 1

def test_default_capacity_is_five():
    # Default capacity should be 5
    ruil = RecentlyUsedItemsList()
    assert ruil.capacity() == 5

def test_add_item_to_full_list_drops_oldest_entry():
    # Adding items to a full list should drop the oldest entry
    ruil = RecentlyUsedItemsList()
    for i in range(6):
        ruil.add(f"item{i}")
    assert ruil.read() == ["item5", "item4", "item3", "item2", "item1"]

def test_custom_capacity():
    # List should accept a custom capacity
    ruil = RecentlyUsedItemsList(capacity=3)
    assert ruil.capacity() == 3

def test_add_item_with_empty_value():
    # Adding an empty string should raise an error
    ruil = RecentlyUsedItemsList()
    with pytest.raises(Exception) as excinfo:
        ruil.add("")
    assert str(excinfo.value) == "List items should not be Empty or Null. But it was []"

def test_add_item_with_none_value():
    # Adding None should raise an error
    ruil = RecentlyUsedItemsList()
    with pytest.raises(Exception) as excinfo:
        ruil.add(None)
    assert str(excinfo.value) == "List items should not be Empty or Null. But it was [None]"

def test_get_item_by_position():
    # Retrieve items by their position
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    ruil.add("item2")
    assert ruil.get(0) == "item2"  # Most recent
    assert ruil.get(1) == "item1"  # Next most recent

def test_get_item_by_position_out_of_bounds():
    # Accessing a position greater than the last index should raise an error
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    with pytest.raises(Exception) as excinfo:
        ruil.get(1)  # Out of bounds
    assert str(excinfo.value) == "supplied index [1] should not greater than [0]."

def test_get_item_by_negative_position():
    # Accessing a negative position should raise an error
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    with pytest.raises(Exception) as excinfo:
        ruil.get(-1)  # Negative index
    assert str(excinfo.value) == "supplied index [-1] should be non-negative and not greater than [0]."

def test_add_item_reuses_existing():
    # Adding an existing item should not increase count and maintain order
    ruil = RecentlyUsedItemsList()
    ruil.add("item1")
    ruil.add("item2")
    ruil.add("item1")  # Reuse existing item
    assert ruil.count() == 2
    assert ruil.read() == ["item1", "item2"]

def test_add_duplicate_at_capacity():
    # Adding a duplicate when at capacity should not evict existing items
    ruil = RecentlyUsedItemsList(capacity=2)
    ruil.add("item1")
    ruil.add("item2")
    ruil.add("item1")  # Reuse existing item
    assert ruil.count() == 2
    assert ruil.read() == ["item1", "item2"]  # Should still be ["item1", "item2"]

def test_custom_capacity_eviction():
    # Adding distinct items to a custom capacity should evict the oldest
    ruil = RecentlyUsedItemsList(capacity=3)
    ruil.add("item1")
    ruil.add("item2")
    ruil.add("item3")
    ruil.add("item4")  # This should evict "item1"
    assert ruil.read() == ["item4", "item3", "item2"]