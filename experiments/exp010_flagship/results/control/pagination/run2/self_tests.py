# test_solution.py

from solution import pagination_service

def test_counting_pages_and_locating_items():
    # AC-1.1
    assert pagination_service(100, 10, 1) == (10, 1, 10, 10, 10)  # 100 items, 10 per page -> 10 pages
    assert pagination_service(95, 10, 1) == (10, 1, 10, 10, 10)    # 95 items, 10 per page -> 10 pages

    # AC-1.2
    assert pagination_service(100, 10, 3) == (10, 21, 30, 10, 10)  # Page 3 -> items 21-30
     
    # AC-1.3
    assert pagination_service(95, 10, 10) == (10, 91, 95, 10, 10)  # Last page -> items 91-95

    # AC-1.4
    assert pagination_service(10, 1, 1) == (10, 1, 1, 10, 1)      # 1 item per page -> item 1

    # AC-1.5
    assert pagination_service(7, 10, 1) == (1, 1, 7, 7, 10)       # 7 items < 1 page -> items 1-7

    # AC-1.6
    assert pagination_service(100, 10, 1) == (10, 1, 10, 10, 10)  # Total items and page size reported

def test_clamping_out_of_range_page_requests():
    # AC-2.1
    assert pagination_service(100, 10, 0) == (10, 1, 10, 10, 10)   # Clamped to page 1
    assert pagination_service(100, 10, -1) == (10, 1, 10, 10, 10)  # Clamped to page 1

    # AC-2.2
    assert pagination_service(100, 10, 11) == (10, 91, 100, 10, 10)  # Clamped to last page

def test_knowing_about_neighbouring_pages():
    # AC-3.1
    assert pagination_service(100, 10, 1) == (10, 1, 10, 10, 10)  # First page, next exists

    # AC-3.2
    assert pagination_service(100, 10, 5) == (10, 41, 50, 10, 10)  # Interior page has neighbours

    # AC-3.3
    assert pagination_service(100, 10, 10) == (10, 91, 100, 10, 10)  # Last page, previous exists

    # AC-3.4
    assert pagination_service(10, 10, 1) == (1, 1, 10, 10, 10)      # Only page, no neighbours

    # AC-3.5
    assert pagination_service(100, 10, 2) == (10, 11, 20, 10, 10)   # Page after 1 has previous

def test_handling_an_empty_collection():
    # AC-4.1
    assert pagination_service(0, 10, 1) == (0, 0, 0, 0, 10)       # Empty collection

def test_windowing_page_numbers_for_navigation():
    # AC-5.1
    assert pagination_service(10, 5, 6) == (10, 4, 8)              # Window around page 6

    # AC-5.2
    assert pagination_service(10, 5, 2) == (10, 1, 5)              # Window around page 2

    # AC-5.3
    assert pagination_service(10, 5, 10) == (10, 6, 10)            # Window around last page

    # AC-5.4
    assert pagination_service(3, 7, 2) == (3, 1, 3)                # Wide window around 2 pages

    # AC-5.5
    assert pagination_service(10, 4, 6) == (10, 5, 8)              # Even window around page 6

def test_rejecting_invalid_sizes():
    # AC-6.1
    try:
        pagination_service(-1, 10, 1)
    except ValueError as e:
        assert str(e) == "total_items must be non-negative, got [-1]"

    # AC-6.2
    try:
        pagination_service(100, 0, 1)
    except ValueError as e:
        assert str(e) == "page_size must be at least 1, got [0]"

    try:
        pagination_service(100, -3, 1)
    except ValueError as e:
        assert str(e) == "page_size must be at least 1, got [-3]"

    # AC-6.3
    try:
        pagination_service(100, 10, 1, 0)  # This line is invalid as the function only takes 3 parameters
    except TypeError as e:
        assert str(e) == "pagination_service() takes 3 positional arguments but 4 were given"