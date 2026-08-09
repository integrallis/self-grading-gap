# test_recently_used_items.py

import pytest
from solution import RecentlyUsedItems

def test_add_item_increases_count():
    # Create a list with default capacity of 5
    recent_items = RecentlyUsedItems()
    recent_items.add("file1.txt")
    assert recent_items.count() == 1

def test_add_item_stores_it_most_recent_first():
    # Create a list with default capacity of 5
    recent_items = RecentlyUsedItems()
    recent_items.add("file1.txt")
    recent_items.add("file2.txt")
    assert recent_items.get_all() == ["file2.txt", "file1.txt"]  # Most recently added first

def test_add_duplicate_item_does_not_increase_count():
    # Create a list with default capacity of 5
    recent_items = RecentlyUsedItems()
    recent_items.add("file1.txt")
    recent_items.add("file1.txt")  # Duplicate
    assert recent_items.count() == 1

def test_add_item_to_full_list_drops_oldest_entry():
    # Create a list with default capacity of 5
    recent_items = RecentlyUsedItems()
    recent_items.add("file1.txt")
    recent_items.add("file2.txt")
    recent_items.add("file3.txt")
    recent_items.add("file4.txt")
    recent_items.add("file5.txt")
    recent_items.add("file6.txt")  # This should drop "file1.txt"
    assert recent_items.get_all() == ["file6.txt", "file5.txt", "file4.txt", "file3.txt", "file2.txt"]

def test_custom_capacity():
    # Create a list with a specified capacity of 3
    recent_items = RecentlyUsedItems(capacity=3)
    recent_items.add("file1.txt")
    recent_items.add("file2.txt")
    recent_items.add("file3.txt")
    recent_items.add("file4.txt")  # This should drop "file1.txt"
    assert recent_items.get_all() == ["file4.txt", "file3.txt", "file2.txt"]
    # Note: The specification does not require a .capacity property, so we can't check it.

def test_get_item_by_position():
    # Create a list with default capacity of 5
    recent_items = RecentlyUsedItems()
    recent_items.add("file1.txt")
    recent_items.add("file2.txt")
    assert recent_items.get_by_position(0) == "file2.txt"  # Position 0 is most recent
    assert recent_items.get_by_position(1) == "file1.txt"  # Position 1 is the next

def test_get_item_by_invalid_positive_position():
    # Create a list with default capacity of 5
    recent_items = RecentlyUsedItems()
    recent_items.add("file1.txt")
    recent_items.add("file2.txt")
    # Check for out of range position
    try:
        recent_items.get_by_position(3)  # Invalid position
    except Exception as e:
        assert str(e) == "supplied index [3] should not greater than [1]."

def test_get_item_by_negative_position():
    # Create a list with default capacity of 5
    recent_items = RecentlyUsedItems()
    recent_items.add("file1.txt")
    recent_items.add("file2.txt")
    # Check for negative position
    try:
        recent_items.get_by_position(-1)  # Invalid negative position
    except Exception as e:
        assert str(e) == "supplied index [-1] should be non-negative and not greater than [1]."

def test_add_empty_entry_rejected():
    # Create a list with default capacity of 5
    recent_items = RecentlyUsedItems()
    # Check for empty entry
    try:
        recent_items.add("")  # Empty entry
    except Exception as e:
        assert str(e) == "List items should not be Empty or Null. But it was []"

    # Check for None entry
    try:
        recent_items.add(None)  # None entry
    except Exception as e:
        assert str(e) == "List items should not be Empty or Null. But it was [None]"

def test_reuse_non_front_item_promotes_it():
    # Create a list with a specified capacity of 3
    recent_items = RecentlyUsedItems(capacity=3)
    recent_items.add("a")
    recent_items.add("b")
    recent_items.add("c")
    recent_items.add("b")  # This should promote "b" to the front
    assert recent_items.get_all() == ["b", "c", "a"]  # Order after reusing "b"

    recent_items.add("d")  # This should drop "c"
    assert recent_items.get_all() == ["d", "b", "a"]