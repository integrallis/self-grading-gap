import pytest
from solution import RecentlyUsedItemsList

def test_add_item_updates_count():
    recent_items = RecentlyUsedItemsList()
    recent_items.add("file1.txt")
    assert recent_items.count() == 1  # 1 item added

def test_add_item_keeps_order():
    recent_items = RecentlyUsedItemsList()
    recent_items.add("file1.txt")
    recent_items.add("file2.txt")
    assert recent_items.get_all() == ["file2.txt", "file1.txt"]  # most-recently added first

def test_add_duplicate_item_does_not_increase_count():
    recent_items = RecentlyUsedItemsList()
    recent_items.add("file1.txt")
    recent_items.add("file1.txt")  # adding again
    assert recent_items.count() == 1  # count remains the same

def test_add_item_does_not_consume_capacity_on_duplicate():
    recent_items = RecentlyUsedItemsList(capacity=3)
    recent_items.add("file1.txt")
    recent_items.add("file2.txt")
    recent_items.add("file3.txt")  # list is full now
    recent_items.add("file2.txt")  # re-adding file2.txt
    recent_items.add("file4.txt")  # adding a new item
    assert recent_items.get_all() == ["file4.txt", "file2.txt", "file3.txt"]  # file1.txt is dropped

def test_add_item_exceeds_capacity_drops_oldest():
    recent_items = RecentlyUsedItemsList()
    for i in range(6):
        recent_items.add(f"file{i}.txt")
    assert recent_items.get_all() == ["file5.txt", "file4.txt", "file3.txt", "file2.txt", "file1.txt"]  # oldest dropped

def test_custom_capacity_initialization():
    recent_items = RecentlyUsedItemsList(capacity=3)
    assert recent_items.capacity() == 3  # should return custom capacity

def test_add_item_to_full_list_drops_oldest():
    recent_items = RecentlyUsedItemsList(capacity=3)
    for i in range(4):
        recent_items.add(f"file{i}.txt")
    assert recent_items.get_all() == ["file3.txt", "file2.txt", "file1.txt"]  # oldest dropped

def test_get_item_by_position():
    recent_items = RecentlyUsedItemsList()
    recent_items.add("file1.txt")
    recent_items.add("file2.txt")
    assert recent_items.get(0) == "file2.txt"  # position 0 is most recent
    assert recent_items.get(1) == "file1.txt"  # position 1 is less recent

def test_get_item_by_invalid_position_too_high():
    recent_items = RecentlyUsedItemsList()
    recent_items.add("file1.txt")
    recent_items.add("file2.txt")
    with pytest.raises(Exception) as excinfo:
        recent_items.get(2)  # out of bounds
    assert str(excinfo.value) == "supplied index [2] should not greater than [1]."

def test_get_item_by_invalid_position_negative():
    recent_items = RecentlyUsedItemsList()
    recent_items.add("file1.txt")
    recent_items.add("file2.txt")
    with pytest.raises(Exception) as excinfo:
        recent_items.get(-1)  # negative index
    assert str(excinfo.value) == "supplied index [-1] should be non-negative and not greater than [1]."

def test_add_empty_entry_rejected():
    recent_items = RecentlyUsedItemsList()
    with pytest.raises(Exception) as excinfo:
        recent_items.add("")  # empty string
    assert str(excinfo.value) == "List items should not be Empty or Null. But it was []"

def test_add_none_entry_rejected():
    recent_items = RecentlyUsedItemsList()
    with pytest.raises(Exception) as excinfo:
        recent_items.add(None)  # None value
    assert str(excinfo.value) == "List items should not be Empty or Null. But it was [None]"