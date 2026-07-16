# test_recently_used_items.py

from solution import RecentlyUsedItemsList
import pytest

def test_add_item_increases_count():
    # Adding one item should increase the count to 1
    recent_list = RecentlyUsedItemsList()
    recent_list.add_item("file1.txt")
    assert recent_list.item_count() == 1

def test_read_whole_list_returns_recently_added_first():
    # Adding items "file1.txt" and "file2.txt", should return ["file2.txt", "file1.txt"]
    recent_list = RecentlyUsedItemsList()
    recent_list.add_item("file1.txt")
    recent_list.add_item("file2.txt")
    assert recent_list.read_all() == ["file2.txt", "file1.txt"]

def test_add_duplicate_item_does_not_increase_count():
    # Adding "file1.txt" twice should still keep count at 1
    recent_list = RecentlyUsedItemsList()
    recent_list.add_item("file1.txt")
    recent_list.add_item("file1.txt")
    assert recent_list.item_count() == 1

def test_add_item_to_full_list_drops_oldest_entry():
    # Adding 5 items, then adding a 6th should drop the first added item "file1.txt"
    recent_list = RecentlyUsedItemsList()
    recent_list.add_item("file1.txt")  # 0
    recent_list.add_item("file2.txt")  # 1
    recent_list.add_item("file3.txt")  # 2
    recent_list.add_item("file4.txt")  # 3
    recent_list.add_item("file5.txt")  # 4
    recent_list.add_item("file6.txt")  # 5, should drop "file1.txt"
    assert recent_list.read_all() == ["file6.txt", "file5.txt", "file4.txt", "file3.txt", "file2.txt"]

def test_custom_capacity_list():
    # Creating a list with capacity of 3, adding 4 items should drop the oldest
    recent_list = RecentlyUsedItemsList(capacity=3)
    recent_list.add_item("file1.txt")
    recent_list.add_item("file2.txt")
    recent_list.add_item("file3.txt")
    recent_list.add_item("file4.txt")  # Should drop "file1.txt"
    assert recent_list.read_all() == ["file4.txt", "file3.txt", "file2.txt"]

def test_position_zero_returns_most_recent_item():
    # Position 0 should return "file2.txt"
    recent_list = RecentlyUsedItemsList()
    recent_list.add_item("file1.txt")
    recent_list.add_item("file2.txt")
    assert recent_list.get_item(0) == "file2.txt"

def test_get_item_out_of_bounds():
    # Supplied index 5 should not be greater than 4 (last valid index)
    recent_list = RecentlyUsedItemsList()
    recent_list.add_item("file1.txt")
    recent_list.add_item("file2.txt")
    recent_list.add_item("file3.txt")
    recent_list.add_item("file4.txt")
    recent_list.add_item("file5.txt")
    
    with pytest.raises(IndexError, match="supplied index 5 should not greater than 4."):
        recent_list.get_item(5)

def test_get_item_negative_index():
    # Supplied index -1 should be non-negative and not greater than 4 (last valid index)
    recent_list = RecentlyUsedItemsList()
    recent_list.add_item("file1.txt")
    recent_list.add_item("file2.txt")
    recent_list.add_item("file3.txt")
    recent_list.add_item("file4.txt")
    recent_list.add_item("file5.txt")
    
    with pytest.raises(IndexError, match="supplied index -1 should be non-negative and not greater than 4."):
        recent_list.get_item(-1)

def test_add_empty_item_rejected():
    # Adding an empty item should raise a ValueError
    recent_list = RecentlyUsedItemsList()
    with pytest.raises(ValueError, match="List items should not be Empty or Null. But it was []"):
        recent_list.add_item("")

def test_add_none_item_rejected():
    # Adding a None item should raise a ValueError
    recent_list = RecentlyUsedItemsList()
    with pytest.raises(ValueError, match="List items should not be Empty or Null. But it was [None]"):
        recent_list.add_item(None)