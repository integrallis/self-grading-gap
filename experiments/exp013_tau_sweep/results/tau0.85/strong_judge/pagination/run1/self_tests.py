# test_pagination.py

import pytest

# Define the public API contract for the function we expect the implementer to create
def paginate_items(total_items, page_size, requested_page, window_size=5):
    pass  # Implementer will define this function

# US-1: Counting pages and locating items
def test_counting_pages_and_locating_items():
    # AC-1.1
    assert paginate_items(100, 10, 1) == {'total_items': 100, 'page_size': 10, 'number_of_pages': 10, 'first_item': 1, 'last_item': 10, 'current_page': 1, 'previous_page': None, 'next_page': 2}
    assert paginate_items(95, 10, 1) == {'total_items': 95, 'page_size': 10, 'number_of_pages': 10, 'first_item': 1, 'last_item': 10, 'current_page': 1, 'previous_page': None, 'next_page': 2}

    # AC-1.2
    assert paginate_items(100, 10, 3) == {'total_items': 100, 'page_size': 10, 'number_of_pages': 10, 'first_item': 21, 'last_item': 30, 'current_page': 3, 'previous_page': 2, 'next_page': 4}

    # AC-1.3
    assert paginate_items(95, 10, 10) == {'total_items': 95, 'page_size': 10, 'number_of_pages': 10, 'first_item': 91, 'last_item': 95, 'current_page': 10, 'previous_page': 9, 'next_page': None}

    # AC-1.4
    assert paginate_items(100, 1, 1) == {'total_items': 100, 'page_size': 1, 'number_of_pages': 100, 'first_item': 1, 'last_item': 1, 'current_page': 1, 'previous_page': None, 'next_page': 2}

    # AC-1.5
    assert paginate_items(7, 10, 1) == {'total_items': 7, 'page_size': 10, 'number_of_pages': 1, 'first_item': 1, 'last_item': 7, 'current_page': 1, 'previous_page': None, 'next_page': None}
    assert paginate_items(1, 10, 1) == {'total_items': 1, 'page_size': 10, 'number_of_pages': 1, 'first_item': 1, 'last_item': 1, 'current_page': 1, 'previous_page': None, 'next_page': None}

    # AC-1.6
    assert paginate_items(100, 10, 1) == {'total_items': 100, 'page_size': 10, 'number_of_pages': 10, 'first_item': 1, 'last_item': 10, 'current_page': 1, 'previous_page': None, 'next_page': 2}

# US-2: Clamping out-of-range page requests
def test_clamping_out_of_range_page_requests():
    # AC-2.1
    assert paginate_items(100, 10, 0) == {'total_items': 100, 'page_size': 10, 'number_of_pages': 10, 'first_item': 1, 'last_item': 10, 'current_page': 1, 'previous_page': None, 'next_page': 2}
    assert paginate_items(100, 10, -5) == {'total_items': 100, 'page_size': 10, 'number_of_pages': 10, 'first_item': 1, 'last_item': 10, 'current_page': 1, 'previous_page': None, 'next_page': 2}

    # AC-2.2
    assert paginate_items(95, 10, 999) == {'total_items': 95, 'page_size': 10, 'number_of_pages': 10, 'first_item': 91, 'last_item': 95, 'current_page': 10, 'previous_page': 9, 'next_page': None}

# US-3: Knowing about neighbouring pages
def test_knowing_about_neighbouring_pages():
    # AC-3.1
    assert paginate_items(100, 10, 1)['previous_page'] is None
    assert paginate_items(100, 10, 1)['next_page'] == 2

    # AC-3.2
    assert paginate_items(100, 10, 5)['previous_page'] == 4
    assert paginate_items(100, 10, 5)['next_page'] == 6

    # AC-3.3
    assert paginate_items(100, 10, 10)['previous_page'] == 9
    assert paginate_items(100, 10, 10)['next_page'] is None

    # AC-3.4
    assert paginate_items(7, 10, 1)['previous_page'] is None
    assert paginate_items(7, 10, 1)['next_page'] is None

    # AC-3.5
    assert paginate_items(100, 10, 5)['previous_page'] == 4

# US-4: Handling an empty collection
def test_handling_empty_collection():
    # AC-4.1
    assert paginate_items(0, 10, 1) == {'total_items': 0, 'page_size': 10, 'number_of_pages': 0, 'first_item': 0, 'last_item': 0, 'current_page': 0, 'previous_page': None, 'next_page': None, 'page_window': []}

# US-5: Windowing page numbers for navigation
def test_windowing_page_numbers_for_navigation():
    # AC-5.1
    assert paginate_items(10, 1, 6, window_size=5)['page_window'] == [4, 5, 6, 7, 8]

    # AC-5.2
    assert paginate_items(10, 1, 2, window_size=5)['page_window'] == [1, 2, 3, 4, 5]

    # AC-5.3
    assert paginate_items(10, 1, 10, window_size=5)['page_window'] == [6, 7, 8, 9, 10]

    # AC-5.4
    assert paginate_items(3, 1, 2, window_size=7)['page_window'] == [1, 2, 3]

    # AC-5.5
    assert paginate_items(10, 1, 6, window_size=4)['page_window'] == [5, 6, 7, 8]

# US-6: Rejecting invalid sizes
def test_rejecting_invalid_sizes():
    # AC-6.1
    with pytest.raises(Exception) as exc_info:
        paginate_items(-1, 10, 1)
    assert str(exc_info.value) == "total_items must be non-negative, got [-1]"

    # AC-6.2
    with pytest.raises(Exception) as exc_info:
        paginate_items(10, 0, 1)
    assert str(exc_info.value) == "page_size must be at least 1, got [0]"

    with pytest.raises(Exception) as exc_info:
        paginate_items(10, -3, 1)
    assert str(exc_info.value) == "page_size must be at least 1, got [-3]"

    # AC-6.3
    with pytest.raises(Exception) as exc_info:
        paginate_items(10, 1, 1, window_size=0)
    assert str(exc_info.value) == "window_size must be at least 1, got [0]"