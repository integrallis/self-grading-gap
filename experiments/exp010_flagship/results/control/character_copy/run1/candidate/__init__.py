def copy_characters(source, destination, batch_size=None):
    if batch_size is not None and batch_size < 1:
        raise ValueError("count must be at least 1")

    newline_index = source.find('\n')
    if newline_index == -1:
        # No newline found, copy all characters up to batch_size
        if batch_size is None or batch_size > len(source):
            batch_size = len(source)
        destination.extend(source[:batch_size])
    else:
        # Newline found, copy only up to newline or batch_size
        if batch_size is None:
            batch_size = newline_index
        else:
            batch_size = min(batch_size, newline_index)
        destination.extend(source[:batch_size])