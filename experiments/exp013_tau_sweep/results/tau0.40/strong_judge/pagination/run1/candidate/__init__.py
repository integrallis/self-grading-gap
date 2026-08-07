def paginate_collection(total_items, page_size, current_page, window_size=5):
    if total_items < 0:
        raise Exception(f"total_items must be non-negative, got [{total_items}]")
    if page_size < 1:
        raise Exception(f"page_size must be at least 1, got [{page_size}]")
    if window_size < 1:
        raise Exception(f"window_size must be at least 1, got [{window_size}]")

    page_count = (total_items + page_size - 1) // page_size

    if page_count == 0:
        return {
            'page_count': 0,
            'first_item': 0,
            'last_item': 0,
            'current_page': 0,
            'page_size': page_size,
            'total_items': total_items,
            'has_previous': False,
            'has_next': False,
            'page_window': []
        }

    current_page = max(1, min(current_page, page_count))

    first_item = (current_page - 1) * page_size + 1
    last_item = min(first_item + page_size - 1, total_items)

    has_previous = current_page > 1
    has_next = current_page < page_count

    page_window_start = max(1, current_page - (window_size - 1) // 2)
    page_window_end = min(page_count, page_window_start + window_size - 1)
    if page_window_end - page_window_start < window_size - 1:
        page_window_start = max(1, page_window_end - window_size + 1)
    page_window = list(range(page_window_start, page_window_end + 1))

    return {
        'page_count': page_count,
        'first_item': first_item,
        'last_item': last_item,
        'current_page': current_page,
        'page_size': page_size,
        'total_items': total_items,
        'has_previous': has_previous,
        'has_next': has_next,
        'page_window': page_window,
    }