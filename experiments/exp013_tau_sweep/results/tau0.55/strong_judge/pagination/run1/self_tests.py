import pytest
import re
from solution import paginate_collection

# User Stories: Counting pages and locating items
def test_counting_pages_with_exact_division():
    result = paginate_collection(100, 10, 1)
    # 100 items / 10 per page = 10 pages
    assert result['total_pages'] == 10

def test_counting_pages_with_partial_last_page():
    result = paginate_collection(95, 10, 1)
    # 95 items / 10 per page = 10 pages (last page is partial)
    assert result['total_pages'] == 10

def test_item_range_on_current_page():
    result = paginate_collection(100, 10, 3)
    # Page 3, items 21 to 30
    assert result['item_range'] == (21, 30)

def test_item_range_on_last_partial_page():
    result = paginate_collection(95, 10, 10)
    # Page 10, items 91 to 95
    assert result['item_range'] == (91, 95)

def test_page_size_of_one():
    result = paginate_collection(10, 1, 5)
    # Page 5, items 5 to 5
    assert result['item_range'] == (5, 5)
    assert result['total_pages'] == 10

def test_collection_smaller_than_one_page():
    result = paginate_collection(7, 10, 1)
    # 7 items; Page 1, items 1 to 7
    assert result['item_range'] == (1, 7)
    assert result['total_pages'] == 1  # Added assertion for total_pages

def test_single_item_collection():
    result = paginate_collection(1, 10, 1)
    # 1 item; Page 1, items 1 to 1
    assert result['item_range'] == (1, 1)
    assert result['total_pages'] == 1  # Added assertion for total_pages

def test_empty_collection():
    result = paginate_collection(0, 10, 1)
    # 0 items; 0 pages
    assert result['total_pages'] == 0
    assert result['item_range'] == (0, 0)
    assert result['current_page'] == 0  # Added assertion for current_page
    assert result['has_previous'] is False  # Added neighbour assertions
    assert result['has_next'] is False
    assert result['page_window'] == []  # Added assertion for page_window
    assert result['page_size'] == 10  # Added assertion for page_size

# User Stories: Clamping out-of-range page requests
def test_clamping_negative_requested_page():
    result = paginate_collection(100, 10, -1)
    # Clamped to page 1
    assert result['current_page'] == 1

def test_clamping_zero_requested_page():
    result = paginate_collection(100, 10, 0)
    # Clamped to page 1
    assert result['current_page'] == 1

def test_clamping_requested_page_beyond_last():
    result = paginate_collection(100, 10, 20)
    # Clamped to page 10
    assert result['current_page'] == 10
    assert result['item_range'] == (91, 100)  # Added assertion for item_range

# User Stories: Knowing about neighbouring pages
def test_first_page_has_next_page():
    result = paginate_collection(100, 10, 1)
    assert result['has_next'] is True
    assert result['has_previous'] is False

def test_interior_page_has_both_neighbours():
    result = paginate_collection(100, 10, 5)
    assert result['has_next'] is True
    assert result['has_previous'] is True

def test_last_page_has_previous_page():
    result = paginate_collection(100, 10, 10)
    assert result['has_next'] is False
    assert result['has_previous'] is True

def test_single_page_collection():
    result = paginate_collection(10, 10, 1)
    assert result['has_next'] is False
    assert result['has_previous'] is False

# User Stories: Windowing page numbers for navigation
def test_window_centered_on_current_page():
    result = paginate_collection(100, 10, 6, window_size=5)
    # Centered on page 6, shows pages 4 to 8
    assert result['page_window'] == [4, 5, 6, 7, 8]

def test_window_anchored_at_first_page():
    result = paginate_collection(100, 10, 2, window_size=5)
    # Anchored at page 1, shows pages 1 to 5
    assert result['page_window'] == [1, 2, 3, 4, 5]

def test_window_anchored_at_last_page():
    result = paginate_collection(100, 10, 10, window_size=5)
    # Anchored at last page, shows pages 6 to 10
    assert result['page_window'] == [6, 7, 8, 9, 10]

def test_window_wider_than_page_count():
    result = paginate_collection(3, 10, 1, window_size=7)
    # Shows pages 1 to 3
    assert result['page_window'] == [1, 2, 3]

def test_window_of_even_width():
    result = paginate_collection(100, 10, 6, window_size=4)
    # Places page 6 just left of center, shows pages 5 to 8
    assert result['page_window'] == [5, 6, 7, 8]

# User Stories: Rejecting invalid sizes
def test_reject_negative_item_count():
    with pytest.raises(Exception, match="^" + re.escape("total_items must be non-negative, got [-1]") + "$"):
        paginate_collection(-1, 10, 1)

def test_reject_page_size_below_one():
    with pytest.raises(Exception, match="^" + re.escape("page_size must be at least 1, got [0]") + "$"):
        paginate_collection(10, 0, 1)
    with pytest.raises(Exception, match="^" + re.escape("page_size must be at least 1, got [-3]") + "$"):
        paginate_collection(10, -3, 1)

def test_reject_window_size_below_one():
    with pytest.raises(Exception, match="^" + re.escape("window_size must be at least 1, got [0]") + "$"):
        paginate_collection(10, 10, 1, window_size=0)