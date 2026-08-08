import pytest
import re
from solution import pagination_service

def test_counting_pages_and_locating_items():
    # AC-1.1
    assert pagination_service.get_pagination(100, 10, 1) == {
        "total_pages": 10, "current_page": 1, "item_range": (1, 10), "total_items": 100, "page_size": 10, "has_next": True, "has_previous": False, "page_window": [1, 2, 3, 4, 5]
    }
    assert pagination_service.get_pagination(95, 10, 1) == {
        "total_pages": 10, "current_page": 1, "item_range": (1, 10), "total_items": 95, "page_size": 10, "has_next": True, "has_previous": False, "page_window": [1, 2, 3, 4, 5]
    }

    # AC-1.2
    assert pagination_service.get_pagination(100, 10, 3) == {
        "total_pages": 10, "current_page": 3, "item_range": (21, 30), "total_items": 100, "page_size": 10, "has_next": True, "has_previous": True, "page_window": [2, 3, 4, 5, 6]
    }

    # AC-1.3
    assert pagination_service.get_pagination(95, 10, 10) == {
        "total_pages": 10, "current_page": 10, "item_range": (91, 95), "total_items": 95, "page_size": 10, "has_next": False, "has_previous": True, "page_window": [6, 7, 8, 9, 10]
    }

    # AC-1.4
    assert pagination_service.get_pagination(10, 1, 1) == {
        "total_pages": 10, "current_page": 1, "item_range": (1, 1), "total_items": 10, "page_size": 1, "has_next": True, "has_previous": False, "page_window": [1]
    }
    assert pagination_service.get_pagination(10, 1, 7) == {
        "total_pages": 10, "current_page": 7, "item_range": (7, 7), "total_items": 10, "page_size": 1, "has_next": True, "has_previous": True, "page_window": [6, 7, 8]
    }

    # AC-1.5
    assert pagination_service.get_pagination(7, 10, 1) == {
        "total_pages": 1, "current_page": 1, "item_range": (1, 7), "total_items": 7, "page_size": 10, "has_next": False, "has_previous": False, "page_window": [1]
    }
    assert pagination_service.get_pagination(1, 10, 1) == {
        "total_pages": 1, "current_page": 1, "item_range": (1, 1), "total_items": 1, "page_size": 10, "has_next": False, "has_previous": False, "page_window": [1]
    }

    # AC-1.6
    assert pagination_service.get_pagination(100, 10, 1) == {
        "total_pages": 10, "current_page": 1, "item_range": (1, 10), "total_items": 100, "page_size": 10, "has_next": True, "has_previous": False, "page_window": [1, 2, 3, 4, 5]
    }

def test_clamping_out_of_range_page_requests():
    # AC-2.1
    assert pagination_service.get_pagination(100, 10, 0) == {
        "total_pages": 10, "current_page": 1, "item_range": (1, 10), "total_items": 100, "page_size": 10, "has_next": True, "has_previous": False, "page_window": [1, 2, 3, 4, 5]
    }
    assert pagination_service.get_pagination(100, 10, -1) == {
        "total_pages": 10, "current_page": 1, "item_range": (1, 10), "total_items": 100, "page_size": 10, "has_next": True, "has_previous": False, "page_window": [1, 2, 3, 4, 5]
    }

    # AC-2.2
    assert pagination_service.get_pagination(100, 10, 11) == {
        "total_pages": 10, "current_page": 10, "item_range": (91, 100), "total_items": 100, "page_size": 10, "has_next": False, "has_previous": True, "page_window": [6, 7, 8, 9, 10]
    }

def test_knowing_about_neighbouring_pages():
    # AC-3.1
    result = pagination_service.get_pagination(100, 10, 1)
    assert result["has_next"] is True
    assert result["has_previous"] is False

    # AC-3.2
    result = pagination_service.get_pagination(100, 10, 5)
    assert result["has_next"] is True
    assert result["has_previous"] is True

    # AC-3.3
    result = pagination_service.get_pagination(100, 10, 10)
    assert result["has_next"] is False
    assert result["has_previous"] is True

    # AC-3.4
    result = pagination_service.get_pagination(1, 10, 1)
    assert result["has_next"] is False
    assert result["has_previous"] is False

    # AC-3.5
    result = pagination_service.get_pagination(100, 10, 2)
    assert result["has_previous"] is True

def test_handling_an_empty_collection():
    # AC-4.1
    assert pagination_service.get_pagination(0, 10, 1) == {
        "total_pages": 0, "current_page": 0, "item_range": (0, 0), "total_items": 0, "page_size": 10, "has_next": False, "has_previous": False, "page_window": []
    }

    # AC-4.2
    assert pagination_service.get_pagination(0, 10, 1)["page_window"] == []

def test_windowing_page_numbers_for_navigation():
    # AC-5.1
    assert pagination_service.get_pagination(100, 10, 6, window_size=5)["page_window"] == [4, 5, 6, 7, 8]

    # AC-5.2
    assert pagination_service.get_pagination(100, 10, 2, window_size=5)["page_window"] == [1, 2, 3, 4, 5]

    # AC-5.3
    assert pagination_service.get_pagination(100, 10, 10, window_size=5)["page_window"] == [6, 7, 8, 9, 10]

    # AC-5.4
    assert pagination_service.get_pagination(3, 1, 2, window_size=3)["page_window"] == [1, 2, 3]

    # AC-5.5
    assert pagination_service.get_pagination(100, 10, 6, window_size=4)["page_window"] == [5, 6, 7, 8]

def test_rejecting_invalid_sizes():
    # AC-6.1
    with pytest.raises(Exception, match=re.escape("total_items must be non-negative, got [-1]")):
        pagination_service.get_pagination(-1, 10, 1)

    # AC-6.2
    with pytest.raises(Exception, match=re.escape("page_size must be at least 1, got [0]")):
        pagination_service.get_pagination(10, 0, 1)
    with pytest.raises(Exception, match=re.escape("page_size must be at least 1, got [-3]")):
        pagination_service.get_pagination(10, -3, 1)

    # AC-6.3
    with pytest.raises(Exception, match=re.escape("window_size must be at least 1, got [0]")):
        pagination_service.get_pagination(10, 10, 1, window_size=0)