def pagination_service(total_items, page_size, page_number):
    if total_items < 0:
        raise ValueError(f"total_items must be non-negative, got [{total_items}]")
    if page_size < 1:
        raise ValueError(f"page_size must be at least 1, got [{page_size}]")

    # Calculate total pages
    total_pages = max((total_items // page_size) + (total_items % page_size > 0), 0)

    # Clamp the page number
    if page_number < 1:
        page_number = 1
    elif page_number > total_pages:
        page_number = total_pages

    # Calculate start and end item indices
    if total_pages == 0:
        return (0, 0, 0, page_size, 0)
    start_index = max((page_number - 1) * page_size + 1, 1)
    end_index = min(start_index + page_size - 1, total_items)

    # Calculate window
    window_start = max(1, page_number - 2)
    window_end = min(total_pages, page_number + 2)

    return (total_pages, start_index, end_index, page_size, end_index - start_index + 1)