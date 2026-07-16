import pytest
from solution import RecentlyUsedItemsList  # Assuming the class is named RecentlyUsedItemsList


def test_add_item_increases_count():
    items_list = RecentlyUsedItemsList()
    items_list.add("item1")
    assert items_list.count() == 1  # Count should be 1 after adding one item


def test_read_whole_list_returns_most_recent_first():
    items_list = RecentlyUsedItemsList()
    items_list.add("item1")
    items_list.add("item2")
    items_list.add("item3")
    assert items_list.get_all() == ["item3", "item2", "item1"]  # Most recent first


def test_add_duplicate_item_does_not_increase_count():
    items_list = RecentlyUsedItemsList()
    items_list.add("item1")
    items_list.add("item1")
    assert items_list.count() == 1  # Count should remain 1


def test_duplicate_item_does_not_consume_capacity():
    items_list = RecentlyUsedItemsList(capacity=3)
    items_list.add("a")
    items_list.add("a")  # Adding duplicate
    items_list.add("b")
    items_list.add("c")
    assert items_list.get_all() == ["c", "b", "a"]  # Only distinct items should be present


def test_default_capacity_is_five():
    items_list = RecentlyUsedItemsList()
    assert items_list.capacity() == 5  # Default capacity should be 5


def test_adding_to_full_list_drops_oldest_entry():
    items_list = RecentlyUsedItemsList()
    for i in range(6):
        items_list.add(f"item{i}")
    assert items_list.get_all() == ["item5", "item4", "item3", "item2", "item1"]  # Oldest (item0) dropped


def test_custom_capacity():
    items_list = RecentlyUsedItemsList(capacity=3)
    assert items_list.capacity() == 3  # Custom capacity should be set correctly


def test_add_item_rejects_empty_value():
    items_list = RecentlyUsedItemsList()
    with pytest.raises(Exception) as excinfo:  # Exception type is unspecified
        items_list.add("")  # Adding empty string
    assert str(excinfo.value) == "List items should not be Empty or Null. But it was []"  # Check message


def test_add_item_rejects_none_value():
    items_list = RecentlyUsedItemsList()
    with pytest.raises(Exception) as excinfo:  # Exception type is unspecified
        items_list.add(None)  # Adding None
    assert str(excinfo.value) == "List items should not be Empty or Null. But it was [None]"  # Check message


def test_retrieve_item_by_position():
    items_list = RecentlyUsedItemsList()
    items_list.add("item1")
    items_list.add("item2")
    items_list.add("item3")
    assert items_list.get(0) == "item3"  # Position 0 should return the most recent item


def test_retrieve_item_by_valid_nonzero_position():
    items_list = RecentlyUsedItemsList()
    items_list.add("item1")
    items_list.add("item2")
    items_list.add("item3")
    assert items_list.get(1) == "item2"  # Position 1 should return the second most recent item


def test_retrieve_item_by_invalid_positive_position():
    items_list = RecentlyUsedItemsList()
    items_list.add("item1")
    items_list.add("item2")
    with pytest.raises(Exception) as excinfo:  # Exception type is unspecified
        items_list.get(2)  # Position 2 is out of bounds
    assert str(excinfo.value) == "supplied index [2] should not greater than [1]."  # Check message


def test_retrieve_item_by_invalid_negative_position():
    items_list = RecentlyUsedItemsList()
    items_list.add("item1")
    items_list.add("item2")
    with pytest.raises(Exception) as excinfo:  # Exception type is unspecified
        items_list.get(-1)  # Negative position is invalid
    assert str(excinfo.value) == "supplied index [-1] should be non-negative and not greater than [1]."  # Check message


def test_empty_list_retrieval_rejects_position_zero():
    items_list = RecentlyUsedItemsList()
    with pytest.raises(Exception) as excinfo:  # Exception type is unspecified
        items_list.get(0)  # Position 0 is invalid for empty list
    assert str(excinfo.value) == "supplied index [0] should not greater than [-1]."  # Check message


def test_readding_existing_item_moves_it_to_front():
    items_list = RecentlyUsedItemsList()
    items_list.add("a")
    items_list.add("b")
    items_list.add("a")  # Re-adding "a"
    assert items_list.get_all() == ["a", "b"]  # "a" should be the most recent item


def test_add_item_rejects_empty_value_and_keeps_list_unchanged():
    items_list = RecentlyUsedItemsList()
    items_list.add("item1")
    items_list.add("item2")
    current_count = items_list.count()
    
    with pytest.raises(Exception) as excinfo:  # Exception type is unspecified
        items_list.add("")  # Attempt to add empty string
    
    assert str(excinfo.value) == "List items should not be Empty or Null. But it was []"  # Check message
    assert items_list.count() == current_count  # Count should remain unchanged