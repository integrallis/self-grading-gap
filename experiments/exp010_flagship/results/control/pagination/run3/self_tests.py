import pytest
from solution import paginate

# US-1: Counting pages and locating items

def test_counting_pages_with_100_items_and_10_per_page():
    result = paginate(100, 10, 1)
    # 100 items / 10 per page = 10 pages
    assert result['total_pages'] == 10
    assert result['first_item'] == 1
    assert result['last_item'] == 10

def test_counting_pages_with_95_items_and_10_per_page():
    result = paginate(95, 10, 1)
    # 95 items / 10 per page = 10 pages
    assert result['total_pages'] == 10
    assert result['first_item'] == 1
    assert result['last_item'] == 10

def test_page_3_of_10_per_page_with_95_items():
    result = paginate(95, 10, 3)
    # Page 3 covers items 21 through 30
    assert result['first_item'] == 21
    assert result['last_item'] == 30

def test_page_10_of_10_per_page_with_95_items():
    result = paginate(95, 10, 10)
    # Page 10 covers items 91 through 95
    assert result['first_item'] == 91
    assert result['last_item'] == 95

def test_page_size_of_1():
    result = paginate(10, 1, 5)
    # Page 5 holds exactly item 5; total pages = item count
    assert result['total_pages'] == 10
    assert result['first_item'] == 5
    assert result['last_item'] == 5

def test_collection_smaller_than_one_page():
    result = paginate(7, 10, 1)
    # 7 items at 10 per page make one page covering items 1 through 7
    assert result['total_pages'] == 1
    assert result['first_item'] == 1
    assert result['last_item'] == 7

def test_empty_collection():
    result = paginate(0, 10, 1)
    # Zero items yield zero pages
    assert result['total_pages'] == 0
    assert result['first_item'] == 0
    assert result['last_item'] == 0

# US-2: Clamping out-of-range page requests

def test_clamping_below_page_1():
    result = paginate(100, 10, 0)
    assert result['current_page'] == 1

def test_clamping_above_last_page():
    result = paginate(100, 10, 15)
    assert result['current_page'] == 10

# US-3: Knowing about neighbouring pages

def test_first_page_has_next_page():
    result = paginate(100, 10, 1)
    assert result['has_next'] is True
    assert result['has_previous'] is False

def test_interior_page_has_both_neighbours():
    result = paginate(100, 10, 5)
    assert result['has_next'] is True
    assert result['has_previous'] is True

def test_last_page_has_previous_page():
    result = paginate(100, 10, 10)
    assert result['has_next'] is False
    assert result['has_previous'] is True

def test_single_page_has_no_neighbours():
    result = paginate(5, 10, 1)
    assert result['has_next'] is False
    assert result['has_previous'] is False

# US-4: Handling an empty collection

def test_empty_collection_page_layout():
    result = paginate(0, 10, 1)
    assert result['total_pages'] == 0
    assert result['current_page'] == 0
    assert result['first_item'] == 0
    assert result['last_item'] == 0

# US-5: Windowing page numbers for navigation

def test_windowing_odd_width():
    result = paginate(10, 10, 6, window_size=5)
    assert result['page_window'] == [4, 5, 6, 7, 8]

def test_windowing_near_first_page():
    result = paginate(10, 10, 2, window_size=5)
    assert result['page_window'] == [1, 2, 3, 4, 5]

def test_windowing_near_last_page():
    result = paginate(10, 10, 10, window_size=5)
    assert result['page_window'] == [6, 7, 8, 9, 10]

def test_windowing_wider_than_page_count():
    result = paginate(3, 10, 1, window_size=7)
    assert result['page_window'] == [1, 2, 3]

def test_windowing_even_width():
    result = paginate(10, 10, 6, window_size=4)
    assert result['page_window'] == [5, 6, 7, 8]

# US-6: Rejecting invalid sizes

def test_negative_item_count():
    with pytest.raises(ValueError, match="total_items must be non-negative, got [-1]"):
        paginate(-1, 10, 1)

def test_zero_page_size():
    with pytest.raises(ValueError, match="page_size must be at least 1, got [0]"):
        paginate(10, 0, 1)

def test_negative_page_size():
    with pytest.raises(ValueError, match="page_size must be at least 1, got [-3]"):
        paginate(10, -3, 1)

def test_zero_window_size():
    with pytest.raises(ValueError, match="window_size must be at least 1, got [0]"):
        paginate(10, 10, 1, window_size=0)