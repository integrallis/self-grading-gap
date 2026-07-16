import pytest
from solution import paginate

# US-1: Counting pages and locating items
def test_counting_pages():
    # 100 items at 10 per page: 100 / 10 = 10 pages
    result = paginate(100, 10, 1)
    assert result['total_pages'] == 10
    assert result['first_item'] == 1
    assert result['last_item'] == 10
    assert result['current_page'] == 1
    assert result['page_size'] == 10
    assert result['total_items'] == 100

    # 95 items at 10 per page: 95 / 10 = 10 pages (last one partial)
    result = paginate(95, 10, 1)
    assert result['total_pages'] == 10
    assert result['first_item'] == 1
    assert result['last_item'] == 10
    assert result['current_page'] == 1
    assert result['page_size'] == 10
    assert result['total_items'] == 95
    
    # 7 items at 10 per page: 1 page covering items 1 through 7
    result = paginate(7, 10, 1)
    assert result['total_pages'] == 1
    assert result['first_item'] == 1
    assert result['last_item'] == 7
    assert result['current_page'] == 1
    assert result['page_size'] == 10
    assert result['total_items'] == 7
    
    # 95 items at 10 per page, page 3: covers items 21 through 30
    result = paginate(95, 10, 3)
    assert result['total_pages'] == 10
    assert result['first_item'] == 21
    assert result['last_item'] == 30
    assert result['current_page'] == 3
    assert result['page_size'] == 10
    assert result['total_items'] == 95
    
    # 95 items at 10 per page, last page (10): covers items 91 through 95
    result = paginate(95, 10, 10)
    assert result['total_pages'] == 10
    assert result['first_item'] == 91
    assert result['last_item'] == 95
    assert result['current_page'] == 10
    assert result['page_size'] == 10
    assert result['total_items'] == 95

    # Page size of 1: each page holds exactly item n
    result = paginate(10, 1, 1)
    assert result['total_pages'] == 10
    assert result['first_item'] == 1
    assert result['last_item'] == 1
    assert result['current_page'] == 1
    assert result['page_size'] == 1
    assert result['total_items'] == 10

    # 1 item at 10 per page: 1 page covering item 1
    result = paginate(1, 10, 1)
    assert result['total_pages'] == 1
    assert result['first_item'] == 1
    assert result['last_item'] == 1
    assert result['current_page'] == 1
    assert result['page_size'] == 10
    assert result['total_items'] == 1

# US-2: Clamping out-of-range page requests
def test_clamping_out_of_range_page_requests():
    # Requested page below 1: clamped to page 1
    result = paginate(100, 10, 0)
    assert result['total_pages'] == 10
    assert result['first_item'] == 1
    assert result['last_item'] == 10
    assert result['current_page'] == 1
    assert result['page_size'] == 10
    assert result['total_items'] == 100
    
    result = paginate(100, 10, -1)
    assert result['total_pages'] == 10
    assert result['first_item'] == 1
    assert result['last_item'] == 10
    assert result['current_page'] == 1
    assert result['page_size'] == 10
    assert result['total_items'] == 100

    # Requested page beyond last page: clamped to last page
    result = paginate(100, 10, 11)
    assert result['total_pages'] == 10
    assert result['first_item'] == 91
    assert result['last_item'] == 100
    assert result['current_page'] == 10
    assert result['page_size'] == 10
    assert result['total_items'] == 100

# US-3: Knowing about neighbouring pages
def test_neighbouring_pages():
    # First page has next page but no previous page
    result = paginate(100, 10, 1)
    assert 'previous_page' not in result
    assert result['next_page'] == True
    
    # Interior page has both previous and next pages
    result = paginate(100, 10, 5)
    assert result['previous_page'] == True
    assert result['next_page'] == True

    # Last page has previous page but no next page
    result = paginate(100, 10, 10)
    assert result['previous_page'] == True
    assert 'next_page' not in result

    # Only page of a single-page collection
    result = paginate(10, 10, 1)
    assert 'previous_page' not in result
    assert 'next_page' not in result

# US-4: Handling an empty collection
def test_empty_collection():
    # Zero items yield zero pages, current page of 0, range of 0
    result = paginate(0, 10, 1)
    assert result['total_pages'] == 0
    assert result['first_item'] == 0
    assert result['last_item'] == 0
    assert result['current_page'] == 0
    assert result['page_size'] == 10
    assert result['total_items'] == 0
    assert result['page_window'] == []
    assert 'previous_page' not in result
    assert 'next_page' not in result

# US-5: Windowing page numbers for navigation
def test_windowing_page_numbers():
    # 5-wide window around page 6 of 10 shows pages 4 through 8
    result = paginate(100, 10, 6, 5)
    assert result['page_window'] == [4, 5, 6, 7, 8]

    # 5-wide window around page 2 of 10 shows pages 1 through 5
    result = paginate(100, 10, 2, 5)
    assert result['page_window'] == [1, 2, 3, 4, 5]

    # 5-wide window around last page 10 shows 6 through 10
    result = paginate(100, 10, 10, 5)
    assert result['page_window'] == [6, 7, 8, 9, 10]

    # A window wider than the page count lists every page
    result = paginate(20, 10, 1, 7)
    assert result['page_window'] == [1, 2]

    # Even width places the current page just left of centre
    result = paginate(100, 10, 6, 4)
    assert result['page_window'] == [5, 6, 7, 8]

    # 7-wide window over 3 pages shows pages 1 through 3
    result = paginate(3, 1, 1, 7)
    assert result['page_window'] == [1, 2, 3]

# US-6: Rejecting invalid sizes
def test_rejecting_invalid_sizes():
    # Negative item count
    with pytest.raises(Exception) as excinfo:
        paginate(-1, 10, 1)
    assert str(excinfo.value) == "total_items must be non-negative, got [-1]"

    # Page size below 1
    with pytest.raises(Exception) as excinfo:
        paginate(100, 0, 1)
    assert str(excinfo.value) == "page_size must be at least 1, got [0]"

    # Invalid page size
    with pytest.raises(Exception) as excinfo:
        paginate(100, -3, 1)
    assert str(excinfo.value) == "page_size must be at least 1, got [-3]"

    # Invalid window size
    with pytest.raises(Exception) as excinfo:
        paginate(100, 10, 1, 0)
    assert str(excinfo.value) == "window_size must be at least 1, got [0]"

    # Negative window size
    with pytest.raises(Exception) as excinfo:
        paginate(100, 10, 1, -1)
    # The exact error message is not known, so we do not assert the message