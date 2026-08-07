import pytest
from solution import RecentlyUsedItemsList

def test_adding_item_increases_count():
    # Arrange
    recent_items = RecentlyUsedItemsList()
    
    # Act
    recent_items.add('item1')
    
    # Assert
    assert recent_items.count() == 1  # Count should be 1 after adding one item

def test_reading_whole_list_returns_most_recent_first():
    # Arrange
    recent_items = RecentlyUsedItemsList()
    recent_items.add('item1')
    recent_items.add('item2')
    
    # Act
    items = recent_items.get_all()
    
    # Assert
    assert items == ['item2', 'item1']  # Most recently added first

def test_adding_existing_item_does_not_increase_count():
    # Arrange
    recent_items = RecentlyUsedItemsList()
    recent_items.add('item1')
    
    # Act
    recent_items.add('item1')  # Attempt to add the same item again
    
    # Assert
    assert recent_items.count() == 1  # Count should remain 1

def test_default_capacity_is_five():
    # Arrange
    recent_items = RecentlyUsedItemsList()
    
    # Act
    capacity = recent_items.capacity()
    
    # Assert
    assert capacity == 5  # Default capacity should be 5

def test_adding_to_full_list_drops_oldest_entry():
    # Arrange
    recent_items = RecentlyUsedItemsList()
    for i in range(6):  # Adding 6 items to exceed default capacity
        recent_items.add(f'item{i}')
    
    # Act
    items = recent_items.get_all()
    
    # Assert
    assert items == ['item5', 'item4', 'item3', 'item2', 'item1']  # Oldest 'item0' should be dropped

def test_capacity_can_be_specified_on_creation():
    # Arrange
    recent_items = RecentlyUsedItemsList(capacity=3)
    
    # Act
    capacity = recent_items.capacity()
    
    # Assert
    assert capacity == 3  # Capacity should be set to 3

def test_reading_item_by_position():
    # Arrange
    recent_items = RecentlyUsedItemsList()
    recent_items.add('item1')
    recent_items.add('item2')
    
    # Act
    item = recent_items.get(0)  # Get most recent item
    
    # Assert
    assert item == 'item2'  # Position 0 should return 'item2'

def test_reading_item_by_out_of_bounds_position():
    # Arrange
    recent_items = RecentlyUsedItemsList()
    recent_items.add('item1')
    
    # Act & Assert
    with pytest.raises(Exception) as excinfo:
        recent_items.get(1)  # Position 1 is out of bounds
    assert str(excinfo.value) == "supplied index [1] should not greater than [0]."

def test_reading_item_by_negative_position():
    # Arrange
    recent_items = RecentlyUsedItemsList()
    recent_items.add('item1')
    
    # Act & Assert
    with pytest.raises(Exception) as excinfo:
        recent_items.get(-1)  # Negative position is invalid
    assert str(excinfo.value) == "supplied index [-1] should be non-negative and not greater than [0]."

def test_adding_empty_value_is_rejected():
    # Arrange
    recent_items = RecentlyUsedItemsList()
    
    # Act & Assert
    with pytest.raises(Exception) as excinfo:
        recent_items.add('')  # Attempt to add empty string
    assert str(excinfo.value) == "List items should not be Empty or Null. But it was []"

def test_adding_none_value_is_rejected():
    # Arrange
    recent_items = RecentlyUsedItemsList()
    
    # Act & Assert
    with pytest.raises(Exception) as excinfo:
        recent_items.add(None)  # Attempt to add None
    assert str(excinfo.value) == "List items should not be Empty or Null. But it was [None]"

def test_adding_duplicate_item_at_capacity():
    # Arrange
    recent_items = RecentlyUsedItemsList(capacity=2)
    recent_items.add('item1')
    recent_items.add('item1')  # Add duplicate
    recent_items.add('item2')   # Add another item to exceed capacity
    
    # Act
    items = recent_items.get_all()
    
    # Assert
    assert items == ['item2', 'item1']  # Both distinct items should be retained

def test_custom_capacity_overflow():
    # Arrange
    recent_items = RecentlyUsedItemsList(capacity=3)
    recent_items.add('item1')
    recent_items.add('item2')
    recent_items.add('item3')
    recent_items.add('item4')  # Adding a fourth item should drop the oldest
    
    # Act
    items = recent_items.get_all()
    
    # Assert
    assert items == ['item4', 'item3', 'item2']  # Only the three newest items should be retained