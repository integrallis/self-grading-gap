import pytest
from solution import RecentlyUsedItemsList

def test_add_item_increases_count():
    ruil = RecentlyUsedItemsList()
    ruil.add("file1.txt")
    assert ruil.count() == 1  # Count should be 1 after adding one item

def test_read_items_returns_most_recent_first():
    ruil = RecentlyUsedItemsList()
    ruil.add("file1.txt")
    ruil.add("file2.txt")
    assert ruil.read_all() == ["file2.txt", "file1.txt"]  # Most recently added first

def test_add_duplicate_item_does_not_increase_count():
    ruil = RecentlyUsedItemsList()
    ruil.add("file1.txt")
    ruil.add("file1.txt")  # Adding duplicate
    assert ruil.count() == 1  # Count should still be 1

def test_add_duplicate_item_does_not_consume_capacity():
    ruil = RecentlyUsedItemsList()
    for i in range(1, 6):
        ruil.add(f"file{i}.txt")
    ruil.add("file5.txt")  # Adding the current newest item again
    ruil.add("file6.txt")  # Adding a new item
    assert ruil.read_all() == ["file6.txt", "file5.txt", "file4.txt", "file3.txt", "file2.txt"]  # file1.txt should be dropped

def test_repeated_use_refreshes_recency():
    ruil = RecentlyUsedItemsList()
    ruil.add("a")
    ruil.add("b")
    ruil.add("a")  # Re-adding "a"
    assert ruil.read_all() == ["a", "b"]  # "a" should be most recent

def test_default_capacity_is_five():
    ruil = RecentlyUsedItemsList()
    assert ruil.capacity() == 5  # Default capacity should be 5

def test_add_item_to_full_list_drops_oldest_entry():
    ruil = RecentlyUsedItemsList()
    for i in range(1, 7):
        ruil.add(f"file{i}.txt")
    assert ruil.read_all() == ["file6.txt", "file5.txt", "file4.txt", "file3.txt", "file2.txt"]  # Oldest (file1.txt) dropped

def test_custom_capacity_can_be_set():
    ruil = RecentlyUsedItemsList(capacity=3)
    assert ruil.capacity() == 3  # Capacity should be set to 3

def test_add_item_to_custom_capacity_full_list_drops_oldest_entry():
    ruil = RecentlyUsedItemsList(capacity=3)
    for i in range(1, 5):
        ruil.add(f"file{i}.txt")
    assert ruil.read_all() == ["file4.txt", "file3.txt", "file2.txt"]  # file1.txt should be dropped

def test_read_item_by_position():
    ruil = RecentlyUsedItemsList()
    ruil.add("file1.txt")
    ruil.add("file2.txt")
    assert ruil.get(0) == "file2.txt"  # Position 0 is the most recent
    assert ruil.get(1) == "file1.txt"  # Position 1 is the next most recent

def test_reject_out_of_bounds_position():
    ruil = RecentlyUsedItemsList()
    ruil.add("file1.txt")
    ruil.add("file2.txt")
    with pytest.raises(Exception) as excinfo:
        ruil.get(2)  # Invalid position, should raise an error
    assert str(excinfo.value) == "supplied index [2] should not greater than [1]."  # Message should match

def test_reject_negative_position():
    ruil = RecentlyUsedItemsList()
    ruil.add("file1.txt")
    ruil.add("file2.txt")
    with pytest.raises(Exception) as excinfo:
        ruil.get(-1)  # Invalid position, should raise an error
    assert str(excinfo.value) == "supplied index [-1] should be non-negative and not greater than [1]."  # Message should match

def test_read_item_by_position_from_empty_list():
    ruil = RecentlyUsedItemsList()
    with pytest.raises(Exception) as excinfo:
        ruil.get(0)  # Invalid position in an empty list
    assert str(excinfo.value) == "supplied index [0] should not greater than [-1]."  # Last valid position for an empty list

def test_add_empty_entry_rejected():
    ruil = RecentlyUsedItemsList()
    with pytest.raises(Exception) as excinfo:
        ruil.add("")  # Adding empty string
    assert str(excinfo.value) == "List items should not be Empty or Null. But it was []"  # Message should match

def test_add_none_entry_rejected():
    ruil = RecentlyUsedItemsList()
    with pytest.raises(Exception) as excinfo:
        ruil.add(None)  # Adding None
    assert str(excinfo.value) == "List items should not be Empty or Null. But it was [None]"  # Message should match