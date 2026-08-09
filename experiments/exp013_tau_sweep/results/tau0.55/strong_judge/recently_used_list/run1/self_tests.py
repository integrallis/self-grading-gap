import pytest
from solution import RecentlyUsedItemsList

def test_add_item_keeps_count():
    ruil = RecentlyUsedItemsList()
    ruil.add("file1.txt")
    assert ruil.size() == 1  # Expected size is 1 after adding one item

def test_read_whole_list_returns_items_most_recent_first():
    ruil = RecentlyUsedItemsList()
    ruil.add("file1.txt")
    ruil.add("file2.txt")
    assert ruil.get_all() == ["file2.txt", "file1.txt"]  # Expected order is most-recently-added first

def test_add_duplicate_item_does_not_increase_count():
    ruil = RecentlyUsedItemsList()
    ruil.add("file1.txt")
    ruil.add("file1.txt")  # Adding the same item again
    assert ruil.size() == 1  # Expected size is still 1

def test_add_duplicate_item_does_not_consume_capacity():
    ruil = RecentlyUsedItemsList(capacity=3)
    ruil.add("file1.txt")
    ruil.add("file1.txt")  # Adding the same item again
    ruil.add("file2.txt")
    ruil.add("file3.txt")
    ruil.add("file4.txt")
    assert ruil.size() == 3  # Expected size is still 3
    assert ruil.get_all() == ["file4.txt", "file3.txt", "file2.txt"]  # Duplicate should not displace others

def test_default_capacity_is_five():
    ruil = RecentlyUsedItemsList()
    assert ruil.capacity() == 5  # Expected capacity is 5 by default

def test_add_to_full_list_drops_oldest_entry():
    ruil = RecentlyUsedItemsList()
    for i in range(6):
        ruil.add(f"file{i}.txt")  # Adding 6 items to a capacity of 5
    assert ruil.get_all() == ["file5.txt", "file4.txt", "file3.txt", "file2.txt", "file1.txt"]  # Oldest file0.txt should be dropped

def test_custom_capacity_can_be_chosen():
    ruil = RecentlyUsedItemsList(capacity=3)
    assert ruil.capacity() == 3  # Expected capacity is 3

def test_fetch_item_by_zero_based_position():
    ruil = RecentlyUsedItemsList()
    ruil.add("file1.txt")
    ruil.add("file2.txt")
    assert ruil.get_by_position(0) == "file2.txt"  # Position 0 should return the most recently used item

def test_fetch_item_by_nonzero_position():
    ruil = RecentlyUsedItemsList()
    ruil.add("file1.txt")
    ruil.add("file2.txt")
    assert ruil.get_by_position(1) == "file1.txt"  # Position 1 should return the second most recently used item

def test_fetch_item_with_negative_position_rejected():
    ruil = RecentlyUsedItemsList()
    ruil.add("file1.txt")
    ruil.add("file2.txt")
    with pytest.raises(Exception, match="supplied index [-1] should be non-negative and not greater than [1]."):
        ruil.get_by_position(-1)  # Negative index should raise an error

def test_fetch_item_with_position_past_last_item_rejected():
    ruil = RecentlyUsedItemsList()
    ruil.add("file1.txt")
    ruil.add("file2.txt")
    with pytest.raises(Exception, match="supplied index [2] should not greater than [1]."):
        ruil.get_by_position(2)  # Out of bounds index should raise an error

def test_add_empty_entry_rejected():
    ruil = RecentlyUsedItemsList()
    with pytest.raises(Exception, match="List items should not be Empty or Null. But it was [None]"):
        ruil.add(None)  # Adding None should raise an error
    
    with pytest.raises(Exception, match="List items should not be Empty or Null. But it was []"):
        ruil.add("")  # Adding empty string should raise an error