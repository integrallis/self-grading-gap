# test_pagination.py

import pytest
from solution import paginate

def test_counting_pages_and_locating_items():
    # AC-1.1
    assert paginate(100, 10, 1) == {'total_items': 100, 'page_size': 10, 'page_count': 10, 'first_item': 1, 'last_item': 10, 'current_page': 1, 'previous_page': None, 'next_page': 2}
    assert paginate(95, 10, 1) == {'total_items': 95, 'page_size': 10, 'page_count': 10, 'first_item': 1, 'last_item': 10, 'current_page': 1, 'previous_page': None, 'next_page': 2}
    
    # AC-1.2
    assert paginate(100, 10, 3) == {'total_items': 100, 'page_size': 10, 'page_count': 10, 'first_item': 21, 'last_item': 30, 'current_page': 3, 'previous_page': 2, 'next_page': 4}
    
    # AC-1.3
    assert paginate(95, 10, 10) == {'total_items': 95, 'page_size': 10, 'page_count': 10, 'first_item': 91, 'last_item': 95, 'current_page': 10, 'previous_page': 9, 'next_page': None}
    
    # AC-1.4
    assert paginate(10, 1, 5) == {'total_items': 10, 'page_size': 1, 'page_count': 10, 'first_item': 5, 'last_item': 5, 'current_page': 5, 'previous_page': 4, 'next_page': 6}
    
    # AC-1.5
    assert paginate(7, 10, 1) == {'total_items': 7, 'page_size': 10, 'page_count': 1, 'first_item': 1, 'last_item': 7, 'current_page': 1, 'previous_page': None, 'next_page': None}
    assert paginate(1, 10, 1) == {'total_items': 1, 'page_size': 10, 'page_count': 1, 'first_item': 1, 'last_item': 1, 'current_page': 1, 'previous_page': None, 'next_page': None}

def test_clamping_out_of_range_page_requests():
    # AC-2.1
    assert paginate(100, 10, 0) == {'total_items': 100, 'page_size': 10, 'page_count': 10, 'first_item': 1, 'last_item': 10, 'current_page': 1, 'previous_page': None, 'next_page': 2}
    assert paginate(100, 10, -1) == {'total_items': 100, 'page_size': 10, 'page_count': 10, 'first_item': 1, 'last_item': 10, 'current_page': 1, 'previous_page': None, 'next_page': 2}
    
    # AC-2.2
    assert paginate(100, 10, 11) == {'total_items': 100, 'page_size': 10, 'page_count': 10, 'first_item': 91, 'last_item': 100, 'current_page': 10, 'previous_page': 9, 'next_page': None}

def test_knowing_about_neighbouring_pages():
    # AC-3.1
    result = paginate(100, 10, 1)
    assert result['previous_page'] is None and result['next_page'] == 2
    
    # AC-3.2
    result = paginate(100, 10, 5)
    assert result['previous_page'] == 4 and result['next_page'] == 6
    
    # AC-3.3
    result = paginate(100, 10, 10)
    assert result['previous_page'] == 9 and result['next_page'] is None
    
    # AC-3.4
    result = paginate(7, 10, 1)
    assert result['previous_page'] is None and result['next_page'] is None
    
    # AC-3.5
    result = paginate(100, 10, 2)
    assert result['previous_page'] == 1

def test_handling_an_empty_collection():
    # AC-4.1
    result = paginate(0, 10, 1)
    assert result == {'total_items': 0, 'page_size': 10, 'page_count': 0, 'first_item': 0, 'last_item': 0, 'current_page': 0, 'previous_page': None, 'next_page': None, 'page_window': []}
    
    # AC-4.2
    assert paginate(0, 10, 1)['page_window'] == []

def test_windowing_page_numbers_for_navigation():
    # AC-5.1
    assert paginate(100, 10, 6, window_size=5)['page_window'] == [4, 5, 6, 7, 8]
    
    # AC-5.2
    assert paginate(100, 10, 2, window_size=5)['page_window'] == [1, 2, 3, 4, 5]
    
    # AC-5.3
    assert paginate(100, 10, 10, window_size=5)['page_window'] == [6, 7, 8, 9, 10]
    
    # AC-5.4
    assert paginate(30, 10, 1, window_size=7)['page_window'] == [1, 2, 3]
    
    # AC-5.5
    assert paginate(100, 10, 6, window_size=4)['page_window'] == [5, 6, 7, 8]

def test_rejecting_invalid_sizes():
    # AC-6.1
    with pytest.raises(ValueError, match=r"^total_items must be non-negative, got \[-1\]$"):
        paginate(-1, 10, 1)
    
    # AC-6.2
    with pytest.raises(ValueError, match=r"^page_size must be at least 1, got \[0\]$"):
        paginate(10, 0, 1)
    
    with pytest.raises(ValueError, match=r"^page_size must be at least 1, got \[-3\]$"):
        paginate(10, -3, 1)
    
    # AC-6.3
    with pytest.raises(ValueError, match=r"^window_size must be at least 1, got \[0\]$"):
        paginate(10, 10, 1, window_size=0)