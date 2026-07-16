import pytest
from solution import paginate

# US-1: Counting pages and locating items
def test_counting_pages_with_100_items_and_page_size_10():
    result = paginate(100, 10, 1)
    # Total pages = ceil(100 / 10) = 10
    # Item range for page 1 = 1 to 10
    assert result['total_pages'] == 10
    assert result['current_page'] == 1
    assert result['first_item'] == 1
    assert result['last_item'] == 10
    assert result['total_items'] == 100
    assert result['page_size'] == 10
    assert result['has_previous'] is False
    assert result['has_next'] is True

def test_counting_pages_with_95_items_and_page_size_10():
    result = paginate(95, 10, 1)
    # Total pages = ceil(95 / 10) = 10
    # Item range for page 1 = 1 to 10
    assert result['total_pages'] == 10
    assert result['current_page'] == 1
    assert result['first_item'] == 1
    assert result['last_item'] == 10
    assert result['total_items'] == 95
    assert result['page_size'] == 10
    assert result['has_previous'] is False
    assert result['has_next'] is True

def test_item_range_on_page_3_with_10_per_page():
    result = paginate(100, 10, 3)
    # Item range for page 3 = 21 to 30
    assert result['first_item'] == 21
    assert result['last_item'] == 30

def test_item_range_on_last_page_with_partial_items():
    result = paginate(95, 10, 10)
    # Item range for last page = 91 to 95
    assert result['first_item'] == 91
    assert result['last_item'] == 95

def test_page_size_of_1():
    result = paginate(10, 1, 5)
    # Total pages = 10
    # Page 5 holds item 5
    assert result['total_pages'] == 10
    assert result['current_page'] == 5
    assert result['first_item'] == 5
    assert result['last_item'] == 5
    assert result['total_items'] == 10
    assert result['page_size'] == 1
    assert result['has_previous'] is True
    assert result['has_next'] is True

def test_collection_smaller_than_one_page():
    result = paginate(7, 10, 1)
    # Total pages = 1, item range = 1 to 7
    assert result['total_pages'] == 1
    assert result['current_page'] == 1
    assert result['first_item'] == 1
    assert result['last_item'] == 7
    assert result['total_items'] == 7
    assert result['page_size'] == 10
    assert result['has_previous'] is False
    assert result['has_next'] is False

def test_single_item_collection():
    result = paginate(1, 10, 1)
    # Total pages = 1, item range = 1 to 1
    assert result['total_pages'] == 1
    assert result['current_page'] == 1
    assert result['first_item'] == 1
    assert result['last_item'] == 1
    assert result['total_items'] == 1
    assert result['page_size'] == 10
    assert result['has_previous'] is False
    assert result['has_next'] is False

# US-2: Clamping out-of-range page requests
def test_clamping_page_below_1():
    result = paginate(100, 10, 0)
    # Clamped to page 1
    assert result['current_page'] == 1
    assert result['first_item'] == 1
    assert result['last_item'] == 10

def test_clamping_negative_requested_page():
    result = paginate(100, 10, -1)
    # Clamped to page 1
    assert result['current_page'] == 1
    assert result['first_item'] == 1
    assert result['last_item'] == 10

def test_clamping_page_beyond_last_page():
    result = paginate(95, 10, 11)
    # Clamped to page 10
    assert result['current_page'] == 10
    assert result['first_item'] == 91
    assert result['last_item'] == 95

# US-3: Knowing about neighbouring pages
def test_first_page_has_next_no_previous():
    result = paginate(100, 10, 1)
    assert result['has_previous'] is False
    assert result['has_next'] is True

def test_interior_page_has_both_neighbours():
    result = paginate(100, 10, 5)
    assert result['has_previous'] is True
    assert result['has_next'] is True

def test_last_page_has_previous_no_next():
    result = paginate(100, 10, 10)
    assert result['has_previous'] is True
    assert result['has_next'] is False

def test_only_page_no_neighbours():
    result = paginate(5, 10, 1)
    assert result['has_previous'] is False
    assert result['has_next'] is False

# US-4: Handling an empty collection
def test_empty_collection():
    result = paginate(0, 10, 1)
    # 0 items yield 0 pages
    assert result['total_pages'] == 0
    assert result['current_page'] == 0
    assert result['first_item'] == 0
    assert result['last_item'] == 0
    assert result['total_items'] == 0
    assert result['page_size'] == 10
    assert result['has_previous'] is False
    assert result['has_next'] is False

def test_empty_collection_window():
    result = paginate(0, 10, 1)
    # Window of an empty collection
    assert result['page_window'] == []

# US-5: Windowing page numbers for navigation
def test_window_around_current_page_6_of_10_with_5_width():
    result = paginate(100, 10, 6, window_size=5)
    # Window around page 6 = pages 4 to 8
    assert result['page_window'] == [4, 5, 6, 7, 8]

def test_window_near_first_page_with_5_width():
    result = paginate(100, 10, 2, window_size=5)
    # Anchored at page 1 = pages 1 to 5
    assert result['page_window'] == [1, 2, 3, 4, 5]

def test_window_near_last_page_with_5_width():
    result = paginate(100, 10, 10, window_size=5)
    # Anchored at last page = pages 6 to 10
    assert result['page_window'] == [6, 7, 8, 9, 10]

def test_window_wider_than_page_count():
    result = paginate(3, 10, 1, window_size=7)
    # All pages = pages 1 to 3
    assert result['page_window'] == [1, 2, 3]

def test_window_with_even_width():
    result = paginate(100, 10, 6, window_size=4)
    # Page 6 just left of centre = pages 5 to 8
    assert result['page_window'] == [5, 6, 7, 8]

# US-6: Rejecting invalid sizes
def test_reject_negative_item_count():
    with pytest.raises(Exception) as exc:
        paginate(-1, 10, 1)
    assert str(exc.value) == "total_items must be non-negative, got [-1]"

def test_reject_page_size_below_1():
    with pytest.raises(Exception) as exc:
        paginate(10, 0, 1)
    assert str(exc.value) == "page_size must be at least 1, got [0]"
    
    with pytest.raises(Exception) as exc:
        paginate(10, -3, 1)
    assert str(exc.value) == "page_size must be at least 1, got [-3]"

def test_reject_window_size_below_1():
    with pytest.raises(Exception) as exc:
        paginate(10, 10, 1, window_size=0)
    assert str(exc.value) == "window_size must be at least 1, got [0]"