def paginate_items(total_items, page_size, page_number, window_size=5):
    if total_items < 0:
        raise ValueError(f"total_items must be non-negative, got {total_items}")
    if page_size < 1:
        raise ValueError(f"page_size must be at least 1, got {page_size}")
    if window_size < 1:
        raise ValueError(f"window_size must be at least 1, got {window_size}")

    total_pages = (total_items + page_size - 1) // page_size  # Rounded up division
    current_page = 0 if total_items == 0 else max(1, min(total_pages, page_number))  # Clamp page number for empty collection

    start_item = (current_page - 1) * page_size + 1
    end_item = min(start_item + page_size - 1, total_items)
    item_range = (start_item, end_item) if total_items > 0 else (0, 0)  # Handle empty collection

    has_next = current_page < total_pages
    has_previous = current_page > 1

    # Calculate page window
    half_window = (window_size - 1) // 2
    start_window = max(1, current_page - half_window)
    end_window = min(total_pages, current_page + half_window + 1)

    # Adjust for the case where current_page is the last page
    if end_window - start_window + 1 < window_size:
        start_window = max(1, end_window - window_size + 1)

    page_window = list(range(start_window, end_window))

    return {
        'total_pages': total_pages,
        'current_page': current_page,
        'item_range': item_range,
        'has_next': has_next,
        'has_previous': has_previous,
        'page_window': page_window
    }