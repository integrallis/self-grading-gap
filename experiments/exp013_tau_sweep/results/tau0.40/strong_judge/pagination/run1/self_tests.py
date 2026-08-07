import pytest
from solution import paginate_collection

# User Stories: US-1: Counting pages and locating items

def test_counting_pages():
    # 100 items at 10 per page make 10 pages
    result = paginate_collection(100, 10, 1)
    assert result['page_count'] == 10
    assert result['first_item'] == 1
    assert result['last_item'] == 10
    assert result['current_page'] == 1
    assert result['page_size'] == 10
    assert result['total_items'] == 100
    
    # 95 items at 10 per page also make 10 pages, the last one partial
    result = paginate_collection(95, 10, 1)
    assert result['page_count'] == 10
    assert result['first_item'] == 1
    assert result['last_item'] == 10
    assert result['current_page'] == 1
    assert result['page_size'] == 10
    assert result['total_items'] == 95
    
    # 7 items at 10 per page make one page covering items 1 through 7
    result = paginate_collection(7, 10, 1)
    assert result['page_count'] == 1
    assert result['first_item'] == 1
    assert result['last_item'] == 7
    assert result['current_page'] == 1
    assert result['page_size'] == 10
    assert result['total_items'] == 7
    
    # 1 item at 10 per page must report one page with item range 1 through 1
    result = paginate_collection(1, 10, 1)
    assert result['page_count'] == 1
    assert result['first_item'] == 1
    assert result['last_item'] == 1
    assert result['current_page'] == 1
    assert result['page_size'] == 10
    assert result['total_items'] == 1

def test_item_range_on_current_page():
    # Page 3 at 10 per page covers items 21 through 30
    result = paginate_collection(100, 10, 3)
    assert result['page_count'] == 10
    assert result['first_item'] == 21
    assert result['last_item'] == 30
    assert result['current_page'] == 3
    assert result['page_size'] == 10
    assert result['total_items'] == 100
    
    # Page 10 of 95 items at 10 per page covers items 91 through 95
    result = paginate_collection(95, 10, 10)
    assert result['page_count'] == 10
    assert result['first_item'] == 91
    assert result['last_item'] == 95
    assert result['current_page'] == 10
    assert result['page_size'] == 10
    assert result['total_items'] == 95

def test_one_item_per_page():
    # With a page size of 1, page n holds exactly item n
    result = paginate_collection(10, 1, 5)
    assert result['page_count'] == 10
    assert result['first_item'] == 5
    assert result['last_item'] == 5
    assert result['current_page'] == 5
    assert result['page_size'] == 1
    assert result['total_items'] == 10

def test_empty_collection():
    # Zero items yield zero pages, current page 0, range 0 to 0
    result = paginate_collection(0, 10, 1)
    assert result['page_count'] == 0
    assert result['first_item'] == 0
    assert result['last_item'] == 0
    assert result['current_page'] == 0
    assert result['page_size'] == 10
    assert result['total_items'] == 0

def test_empty_collection_window():
    # Empty collection's window is []
    result = paginate_collection(0, 10, 1, window_size=5)
    assert result['page_window'] == []

# User Stories: US-2: Clamping out-of-range page requests

def test_clamping_page_below_one():
    # Requested page below 1 is clamped to page 1
    result = paginate_collection(100, 10, 0)
    assert result['current_page'] == 1
    assert result['first_item'] == 1
    assert result['last_item'] == 10
    
    result = paginate_collection(100, 10, -1)
    assert result['current_page'] == 1
    assert result['first_item'] == 1
    assert result['last_item'] == 10

def test_clamping_page_beyond_last():
    # Requested page beyond the last page is clamped to the last page
    result = paginate_collection(100, 10, 11)
    assert result['current_page'] == 10
    assert result['first_item'] == 91
    assert result['last_item'] == 100

# User Stories: US-3: Knowing about neighbouring pages

def test_neighbouring_pages():
    # First page has a next page but no previous page
    result = paginate_collection(100, 10, 1)
    assert result['has_previous'] == False
    assert result['has_next'] == True
    
    # Interior page has both previous and next page
    result = paginate_collection(100, 10, 5)
    assert result['has_previous'] == True
    assert result['has_next'] == True
    
    # Last page has a previous page but no next page
    result = paginate_collection(100, 10, 10)
    assert result['has_previous'] == True
    assert result['has_next'] == False
    
    # Only page of a single-page collection
    result = paginate_collection(1, 1, 1)
    assert result['has_previous'] == False
    assert result['has_next'] == False

def test_every_page_has_previous_after_first():
    # Any page after page 1 reports that a previous page exists
    for page in range(2, 11):
        result = paginate_collection(100, 10, page)
        assert result['has_previous'] == True

# User Stories: US-4: Handling an empty collection

def test_empty_collection_navigation():
    # Empty collection has no neighbouring pages
    result = paginate_collection(0, 10, 1)
    assert result['has_previous'] == False
    assert result['has_next'] == False

# User Stories: US-5: Windowing page numbers for navigation

def test_windowing_page_numbers():
    # 5-wide window around page 6 of 10 shows pages 4 through 8
    result = paginate_collection(100, 10, 6, window_size=5)
    assert result['page_window'] == [4, 5, 6, 7, 8]
    
    # 5-wide window around page 2 of 10 shows pages 1 through 5
    result = paginate_collection(100, 10, 2, window_size=5)
    assert result['page_window'] == [1, 2, 3, 4, 5]
    
    # 5-wide window around page 10 of 10 shows pages 6 through 10
    result = paginate_collection(100, 10, 10, window_size=5)
    assert result['page_window'] == [6, 7, 8, 9, 10]

def test_window_wider_than_page_count():
    # A window wider than the page count lists every page
    result = paginate_collection(3, 1, 2, window_size=7)
    assert result['page_window'] == [1, 2, 3]

def test_even_width_window():
    # A window of even width places the current page just left of centre
    result = paginate_collection(10, 1, 6, window_size=4)
    assert result['page_window'] == [5, 6, 7, 8]

# User Stories: US-6: Rejecting invalid sizes

def test_rejecting_invalid_sizes():
    # Reject negative item count
    with pytest.raises(Exception, match=r"^total_items must be non-negative, got \[-1\]$"):
        paginate_collection(-1, 10, 1)
    
    # Reject page size below 1
    with pytest.raises(Exception, match=r"^page_size must be at least 1, got \[0\]$"):
        paginate_collection(100, 0, 1)
    
    with pytest.raises(Exception, match=r"^page_size must be at least 1, got \[-3\]$"):
        paginate_collection(100, -3, 1)
    
    # Reject window size below 1
    with pytest.raises(Exception, match=r"^window_size must be at least 1, got \[0\]$"):
        paginate_collection(100, 10, 1, window_size=0)