import pytest
from solution import paginate

# US-1: Counting pages and locating items
def test_counting_pages_with_100_items_10_per_page():
    result = paginate(100, 10, 1)
    # Total pages = ceil(100 / 10) = 10
    # Page 1 covers items 1 to 10
    assert result['total_pages'] == 10
    assert result['current_page'] == 1
    assert result['item_range'] == (1, 10)
    assert result['page_size'] == 10
    assert result['total_items'] == 100
    assert result['previous_page_exists'] is False
    assert result['next_page_exists'] is True

def test_counting_pages_with_95_items_10_per_page():
    result = paginate(95, 10, 1)
    # Total pages = ceil(95 / 10) = 10
    # Page 1 covers items 1 to 10
    assert result['total_pages'] == 10
    assert result['current_page'] == 1
    assert result['item_range'] == (1, 10)
    assert result['page_size'] == 10
    assert result['total_items'] == 95
    assert result['previous_page_exists'] is False
    assert result['next_page_exists'] is True

def test_page_3_with_10_per_page():
    result = paginate(100, 10, 3)
    # Page 3 covers items 21 to 30
    assert result['item_range'] == (21, 30)

def test_last_page_with_95_items_10_per_page():
    result = paginate(95, 10, 10)
    # Page 10 covers items 91 to 95
    assert result['item_range'] == (91, 95)

def test_page_with_size_1():
    result = paginate(10, 1, 10)
    # Total pages = 10; Page 10 covers item 10
    assert result['item_range'] == (10, 10)
    assert result['total_pages'] == 10

def test_collection_smaller_than_one_page():
    result = paginate(7, 10, 1)
    # Only one page covering items 1 to 7
    assert result['item_range'] == (1, 7)
    assert result['total_pages'] == 1

def test_single_item_case():
    result = paginate(1, 1, 1)
    # Only one page covering item 1
    assert result['item_range'] == (1, 1)
    assert result['total_pages'] == 1

def test_empty_collection():
    result = paginate(0, 10, 1)
    # Zero items yield zero pages, current page 0, and range 0 to 0
    assert result['total_pages'] == 0
    assert result['current_page'] == 0
    assert result['item_range'] == (0, 0)
    assert result['page_size'] == 10
    assert result['total_items'] == 0
    assert result['previous_page_exists'] is False
    assert result['next_page_exists'] is False
    assert result['page_window'] == []

# US-2: Clamping out-of-range page requests
def test_clamping_page_below_1():
    result = paginate(100, 10, 0)
    assert result['current_page'] == 1
    assert result['item_range'] == (1, 10)

def test_clamping_page_beyond_last_page():
    result = paginate(100, 10, 11)
    assert result['current_page'] == 10
    assert result['item_range'] == (91, 100)

def test_clamping_negative_page():
    result = paginate(100, 10, -1)
    assert result['current_page'] == 1
    assert result['item_range'] == (1, 10)

# US-3: Knowing about neighbouring pages
def test_first_page_has_next_no_previous():
    result = paginate(100, 10, 1)
    assert result['previous_page_exists'] is False
    assert result['next_page_exists'] is True

def test_interior_page_has_both_neighbours():
    result = paginate(100, 10, 5)
    assert result['previous_page_exists'] is True
    assert result['next_page_exists'] is True

def test_last_page_has_previous_no_next():
    result = paginate(100, 10, 10)
    assert result['previous_page_exists'] is True
    assert result['next_page_exists'] is False

def test_only_page_has_no_neighbours():
    result = paginate(1, 1, 1)
    assert result['previous_page_exists'] is False
    assert result['next_page_exists'] is False

# US-4: Handling an empty collection
def test_empty_collection_properties():
    result = paginate(0, 10, 1)
    assert result['total_pages'] == 0
    assert result['current_page'] == 0
    assert result['item_range'] == (0, 0)

# US-5: Windowing page numbers for navigation
def test_window_of_odd_width():
    result = paginate(10, 1, 6, window_size=5)
    # Window around page 6 should show pages 4, 5, 6, 7, 8
    assert result['page_window'] == [4, 5, 6, 7, 8]

def test_window_near_first_page():
    result = paginate(10, 1, 2, window_size=5)
    # Should show pages 1, 2, 3, 4, 5
    assert result['page_window'] == [1, 2, 3, 4, 5]

def test_window_near_last_page():
    result = paginate(10, 1, 10, window_size=5)
    # Should show pages 6, 7, 8, 9, 10
    assert result['page_window'] == [6, 7, 8, 9, 10]

def test_window_wider_than_page_count():
    result = paginate(3, 1, 2, window_size=7)
    # Should show pages 1, 2, 3
    assert result['page_window'] == [1, 2, 3]

def test_window_of_even_width():
    result = paginate(10, 1, 6, window_size=4)
    # Should show pages 5, 6, 7, 8
    assert result['page_window'] == [5, 6, 7, 8]

# US-6: Rejecting invalid sizes
def test_negative_item_count():
    result = paginate(-1, 10, 1)
    assert result == "total_items must be non-negative, got [-1]"

def test_invalid_page_size():
    result = paginate(100, 0, 1)
    assert result == "page_size must be at least 1, got [0]"
    result = paginate(100, -3, 1)
    assert result == "page_size must be at least 1, got [-3]"

def test_invalid_window_size():
    result = paginate(100, 10, 1, window_size=0)
    assert result == "window_size must be at least 1, got [0]"