import pytest
from solution import paginate

# US-1: Counting pages and locating items

def test_counting_pages_with_exact_division():
    assert paginate(100, 10, 1, window_size=5) == {
        'total_items': 100,
        'page_size': 10,
        'total_pages': 10,
        'current_page': 1,
        'first_item': 1,
        'last_item': 10,
        'has_previous': False,
        'has_next': True,
        'page_window': [1, 2, 3, 4, 5]
    }

def test_counting_pages_with_partial_last_page():
    assert paginate(95, 10, 1, window_size=5) == {
        'total_items': 95,
        'page_size': 10,
        'total_pages': 10,
        'current_page': 1,
        'first_item': 1,
        'last_item': 10,
        'has_previous': False,
        'has_next': True,
        'page_window': [1, 2, 3, 4, 5]
    }

def test_items_on_last_partial_page():
    assert paginate(95, 10, 10, window_size=5) == {
        'total_items': 95,
        'page_size': 10,
        'total_pages': 10,
        'current_page': 10,
        'first_item': 91,
        'last_item': 95,
        'has_previous': True,
        'has_next': False,
        'page_window': [6, 7, 8, 9, 10]
    }

def test_single_item_collection():
    assert paginate(1, 1, 1, window_size=1) == {
        'total_items': 1,
        'page_size': 1,
        'total_pages': 1,
        'current_page': 1,
        'first_item': 1,
        'last_item': 1,
        'has_previous': False,
        'has_next': False,
        'page_window': [1]
    }

def test_collection_smaller_than_one_page():
    assert paginate(7, 10, 1, window_size=1) == {
        'total_items': 7,
        'page_size': 10,
        'total_pages': 1,
        'current_page': 1,
        'first_item': 1,
        'last_item': 7,
        'has_previous': False,
        'has_next': False,
        'page_window': [1]
    }

def test_items_on_page_three():
    assert paginate(100, 10, 3, window_size=5) == {
        'total_items': 100,
        'page_size': 10,
        'total_pages': 10,
        'current_page': 3,
        'first_item': 21,
        'last_item': 30,
        'has_previous': True,
        'has_next': True,
        'page_window': [1, 2, 3, 4, 5]
    }

# US-2: Clamping out-of-range page requests

def test_clamping_below_one():
    assert paginate(100, 10, 0, window_size=5) == {
        'total_items': 100,
        'page_size': 10,
        'total_pages': 10,
        'current_page': 1,
        'first_item': 1,
        'last_item': 10,
        'has_previous': False,
        'has_next': True,
        'page_window': [1, 2, 3, 4, 5]
    }

def test_clamping_beyond_last_page():
    assert paginate(100, 10, 11, window_size=5) == {
        'total_items': 100,
        'page_size': 10,
        'total_pages': 10,
        'current_page': 10,
        'first_item': 91,
        'last_item': 100,
        'has_previous': True,
        'has_next': False,
        'page_window': [6, 7, 8, 9, 10]
    }

def test_clamping_negative_page_request():
    assert paginate(100, 10, -1, window_size=5) == {
        'total_items': 100,
        'page_size': 10,
        'total_pages': 10,
        'current_page': 1,
        'first_item': 1,
        'last_item': 10,
        'has_previous': False,
        'has_next': True,
        'page_window': [1, 2, 3, 4, 5]
    }

# US-3: Knowing about neighbouring pages

def test_neighbours_for_first_page():
    assert paginate(100, 10, 1, window_size=5) == {
        'total_items': 100,
        'page_size': 10,
        'total_pages': 10,
        'current_page': 1,
        'first_item': 1,
        'last_item': 10,
        'has_previous': False,
        'has_next': True,
        'page_window': [1, 2, 3, 4, 5]
    }

def test_neighbours_for_interior_page():
    assert paginate(100, 10, 5, window_size=5) == {
        'total_items': 100,
        'page_size': 10,
        'total_pages': 10,
        'current_page': 5,
        'first_item': 41,
        'last_item': 50,
        'has_previous': True,
        'has_next': True,
        'page_window': [3, 4, 5, 6, 7]
    }

def test_neighbours_for_last_page():
    assert paginate(100, 10, 10, window_size=5) == {
        'total_items': 100,
        'page_size': 10,
        'total_pages': 10,
        'current_page': 10,
        'first_item': 91,
        'last_item': 100,
        'has_previous': True,
        'has_next': False,
        'page_window': [6, 7, 8, 9, 10]
    }

def test_neighbours_for_single_page_collection():
    assert paginate(1, 1, 1, window_size=1) == {
        'total_items': 1,
        'page_size': 1,
        'total_pages': 1,
        'current_page': 1,
        'first_item': 1,
        'last_item': 1,
        'has_previous': False,
        'has_next': False,
        'page_window': [1]
    }

# US-4: Handling an empty collection

def test_empty_collection():
    assert paginate(0, 10, 1, window_size=5) == {
        'total_items': 0,
        'page_size': 10,
        'total_pages': 0,
        'current_page': 0,
        'first_item': 0,
        'last_item': 0,
        'has_previous': False,
        'has_next': False,
        'page_window': []
    }

# US-5: Windowing page numbers for navigation

def test_window_centered_on_current_page():
    assert paginate(10, 1, 6, window_size=5) == {
        'total_items': 10,
        'page_size': 1,
        'total_pages': 10,
        'current_page': 6,
        'first_item': 6,
        'last_item': 6,
        'has_previous': True,
        'has_next': True,
        'page_window': [4, 5, 6, 7, 8]
    }

def test_window_anchored_at_first_page():
    assert paginate(10, 1, 2, window_size=5) == {
        'total_items': 10,
        'page_size': 1,
        'total_pages': 10,
        'current_page': 2,
        'first_item': 2,
        'last_item': 2,
        'has_previous': True,
        'has_next': True,
        'page_window': [1, 2, 3, 4, 5]
    }

def test_window_anchored_at_last_page():
    assert paginate(10, 1, 10, window_size=5) == {
        'total_items': 10,
        'page_size': 1,
        'total_pages': 10,
        'current_page': 10,
        'first_item': 10,
        'last_item': 10,
        'has_previous': True,
        'has_next': False,
        'page_window': [6, 7, 8, 9, 10]
    }

def test_window_wider_than_page_count():
    assert paginate(3, 1, 2, window_size=7) == {
        'total_items': 3,
        'page_size': 1,
        'total_pages': 3,
        'current_page': 2,
        'first_item': 2,
        'last_item': 2,
        'has_previous': True,
        'has_next': True,
        'page_window': [1, 2, 3]
    }

def test_window_with_even_width():
    assert paginate(10, 1, 6, window_size=4) == {
        'total_items': 10,
        'page_size': 1,
        'total_pages': 10,
        'current_page': 6,
        'first_item': 6,
        'last_item': 6,
        'has_previous': True,
        'has_next': True,
        'page_window': [5, 6, 7, 8]
    }

# US-6: Rejecting invalid sizes

def test_reject_negative_item_count():
    with pytest.raises(Exception) as exc:
        paginate(-1, 10, 1, window_size=5)
    assert str(exc.value) == "total_items must be non-negative, got [-1]"

def test_reject_zero_page_size():
    with pytest.raises(Exception) as exc:
        paginate(10, 0, 1, window_size=5)
    assert str(exc.value) == "page_size must be at least 1, got [0]"

def test_reject_negative_page_size():
    with pytest.raises(Exception) as exc:
        paginate(10, -3, 1, window_size=5)
    assert str(exc.value) == "page_size must be at least 1, got [-3]"

def test_reject_zero_window_size():
    with pytest.raises(Exception) as exc:
        paginate(10, 1, 1, window_size=0)
    assert str(exc.value) == "window_size must be at least 1, got [0]"

def test_reject_negative_window_size():
    with pytest.raises(Exception) as exc:
        paginate(10, 1, 1, window_size=-1)
    # The message is not specified in the prompt, so no assertion on message