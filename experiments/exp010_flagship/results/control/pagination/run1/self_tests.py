import pytest
from solution import paginate_items

# US-1: Counting pages and locating items
def test_page_count_with_100_items_and_page_size_10():
    result = paginate_items(100, 10, 1)
    assert result['total_pages'] == 10  # 100 / 10 = 10
    assert result['item_range'] == (1, 10)  # 1 to 10 on page 1

def test_page_count_with_95_items_and_page_size_10():
    result = paginate_items(95, 10, 1)
    assert result['total_pages'] == 10  # 95 / 10 = 9.5, rounded up to 10
    assert result['item_range'] == (1, 10)  # 1 to 10 on page 1

def test_page_count_with_7_items_and_page_size_10():
    result = paginate_items(7, 10, 1)
    assert result['total_pages'] == 1  # 7 / 10 = 0.7, rounded up to 1
    assert result['item_range'] == (1, 7)  # 1 to 7 on page 1

def test_page_count_with_1_item_and_page_size_1():
    result = paginate_items(1, 1, 1)
    assert result['total_pages'] == 1  # 1 / 1 = 1
    assert result['item_range'] == (1, 1)  # 1 to 1 on page 1

# US-2: Clamping out-of-range page requests
def test_clamp_page_below_1():
    result = paginate_items(100, 10, 0)
    assert result['current_page'] == 1  # Clamped to page 1

def test_clamp_page_beyond_last_page():
    result = paginate_items(100, 10, 15)
    assert result['current_page'] == 10  # Clamped to last page

# US-3: Knowing about neighbouring pages
def test_first_page_has_next_no_previous():
    result = paginate_items(100, 10, 1)
    assert result['has_next'] is True  # Page 1 has a next page
    assert result['has_previous'] is False  # Page 1 has no previous page

def test_interior_page_has_both_neighbours():
    result = paginate_items(100, 10, 5)
    assert result['has_next'] is True  # Page 5 has a next page
    assert result['has_previous'] is True  # Page 5 has a previous page

def test_last_page_has_previous_no_next():
    result = paginate_items(100, 10, 10)
    assert result['has_next'] is False  # Page 10 has no next page
    assert result['has_previous'] is True  # Page 10 has a previous page

def test_single_page_has_no_neighbours():
    result = paginate_items(10, 10, 1)
    assert result['has_next'] is False  # Only one page has no next page
    assert result['has_previous'] is False  # Only one page has no previous page

# US-4: Handling an empty collection
def test_empty_collection():
    result = paginate_items(0, 10, 1)
    assert result['total_pages'] == 0  # 0 items yield 0 pages
    assert result['current_page'] == 0  # Current page is 0
    assert result['item_range'] == (0, 0)  # Item range is 0 to 0

# US-5: Windowing page numbers for navigation
def test_window_around_page_6_with_5_width():
    result = paginate_items(10, 1, 6, 5)
    assert result['page_window'] == [4, 5, 6, 7, 8]  # 5-wide window centered on page 6

def test_window_around_page_2_with_5_width():
    result = paginate_items(10, 1, 2, 5)
    assert result['page_window'] == [1, 2, 3, 4, 5]  # Anchored at page 1

def test_window_around_page_10_with_5_width():
    result = paginate_items(10, 1, 10, 5)
    assert result['page_window'] == [6, 7, 8, 9, 10]  # Anchored at last page

def test_window_greater_than_page_count():
    result = paginate_items(3, 1, 2, 7)
    assert result['page_window'] == [1, 2, 3]  # Shows all pages

def test_window_of_even_width():
    result = paginate_items(10, 1, 6, 4)
    assert result['page_window'] == [5, 6, 7, 8]  # Places page 6 just left of center

# US-6: Rejecting invalid sizes
def test_negative_item_count():
    with pytest.raises(ValueError, match="total_items must be non-negative, got [-1]"):
        paginate_items(-1, 10, 1)

def test_zero_page_size():
    with pytest.raises(ValueError, match="page_size must be at least 1, got [0]"):
        paginate_items(10, 0, 1)

def test_negative_page_size():
    with pytest.raises(ValueError, match="page_size must be at least 1, got [-3]"):
        paginate_items(10, -3, 1)

def test_zero_window_size():
    with pytest.raises(ValueError, match="window_size must be at least 1, got [0]"):
        paginate_items(10, 1, 1, 0)