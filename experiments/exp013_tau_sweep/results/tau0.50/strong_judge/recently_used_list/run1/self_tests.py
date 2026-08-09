import pytest
from solution import RecentlyUsedItemsList

def test_add_item_increases_count():
    recent_items = RecentlyUsedItemsList()
    recent_items.add('file1.txt')
    assert recent_items.count() == 1  # 1 item added

def test_read_all_items_returns_most_recent_first():
    recent_items = RecentlyUsedItemsList()
    recent_items.add('file1.txt')
    recent_items.add('file2.txt')
    assert recent_items.read_all() == ['file2.txt', 'file1.txt']  # Recent first

def test_add_duplicate_item_does_not_increase_count():
    recent_items = RecentlyUsedItemsList()
    recent_items.add('file1.txt')
    recent_items.add('file1.txt')
    assert recent_items.count() == 1  # Still only 1 unique item
    assert recent_items.read_all() == ['file1.txt']  # Still the only item

def test_add_item_reuses_existing_item_and_moves_it_to_front():
    recent_items = RecentlyUsedItemsList()
    recent_items.add('a')
    recent_items.add('b')
    recent_items.add('a')  # Re-add 'a'
    assert recent_items.read_all() == ['a', 'b']  # 'a' should be most recent

def test_add_item_to_full_list_drops_oldest_entry():
    recent_items = RecentlyUsedItemsList(capacity=2)
    recent_items.add('file1.txt')
    recent_items.add('file2.txt')
    recent_items.add('file3.txt')  # This should drop 'file1.txt'
    assert recent_items.read_all() == ['file3.txt', 'file2.txt']  # Only latest two items

def test_full_list_duplicate_reuse_does_not_consume_capacity():
    recent_items = RecentlyUsedItemsList(capacity=2)
    recent_items.add('a')
    recent_items.add('b')
    recent_items.add('a')  # Re-add 'a'
    recent_items.add('c')  # 'b' should be dropped
    assert recent_items.read_all() == ['c', 'a']  # Most recent is 'c', then 'a'

def test_custom_capacity_on_initialization():
    recent_items = RecentlyUsedItemsList(capacity=3)
    assert recent_items.capacity() == 3  # Should return the custom capacity

def test_default_capacity():
    recent_items = RecentlyUsedItemsList()  # Default capacity is 5
    for i in range(6):
        recent_items.add(f'file{i}.txt')
    assert recent_items.read_all() == ['file5.txt', 'file4.txt', 'file3.txt', 'file2.txt', 'file1.txt']  # Only the last 5 added

def test_add_item_rejects_empty_value():
    recent_items = RecentlyUsedItemsList()
    result = recent_items.add('')
    assert result == "List items should not be Empty or Null. But it was []"  # Empty string

def test_add_item_rejects_none_value():
    recent_items = RecentlyUsedItemsList()
    result = recent_items.add(None)
    assert result == "List items should not be Empty or Null. But it was [None]"  # None value

def test_read_item_by_position():
    recent_items = RecentlyUsedItemsList()
    recent_items.add('file1.txt')
    recent_items.add('file2.txt')
    assert recent_items.read(0) == 'file2.txt'  # Most recent item
    assert recent_items.read(1) == 'file1.txt'  # Second most recent item

def test_read_item_by_invalid_positive_position():
    recent_items = RecentlyUsedItemsList()
    recent_items.add('file1.txt')
    recent_items.add('file2.txt')
    result = recent_items.read(2)  # Out of bounds
    assert result == "supplied index [2] should not greater than [1]."  # Invalid index

def test_read_item_by_negative_position():
    recent_items = RecentlyUsedItemsList()
    recent_items.add('file1.txt')
    recent_items.add('file2.txt')
    result = recent_items.read(-1)  # Negative index
    assert result == "supplied index [-1] should be non-negative and not greater than [1]."  # Invalid index