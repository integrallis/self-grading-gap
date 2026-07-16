def paginate(total_items, page_size, current_page, window_size=5):
    if total_items < 0:
        raise ValueError(f"total_items must be non-negative, got {total_items}")
    if page_size < 1:
        raise ValueError(f"page_size must be at least 1, got {page_size}")
    if window_size < 1:
        raise ValueError(f"window_size must be at least 1, got {window_size}")

    total_pages = (total_items + page_size - 1) // page_size if page_size > 0 else 0
    current_page = max(1, min(current_page, total_pages)) if total_items > 0 else 0

    first_item = (current_page - 1) * page_size + 1 if total_items > 0 else 0
    last_item = min(first_item + page_size - 1, total_items)

    has_next = current_page < total_pages
    has_previous = current_page > 1

    start_window = max(1, current_page - (window_size // 2))
    end_window = min(total_pages, start_window + window_size - 1)
    if end_window - start_window + 1 < window_size:
        start_window = max(1, end_window - window_size + 1)

    page_window = list(range(start_window, end_window + 1))

    return {
        'total_pages': total_pages,
        'current_page': current_page,
        'first_item': first_item,
        'last_item': last_item,
        'has_next': has_next,
        'has_previous': has_previous,
        'page_window': page_window
    }