import pytest

def copy_characters_one_at_a_time(source: str) -> str:
    if source.startswith('\n'):
        return ''
    return source.split('\n')[0]


def copy_characters_in_batches(source: str, batch_size: int) -> str:
    validate_batch_size(batch_size)
    idx = 0
    result = ''
    while idx < len(source):
        if source[idx] == '\n':
            break
        end_idx = min(idx + batch_size, len(source))
        if '\n' in source[idx:end_idx]:
            end_idx = source.index('\n', idx)
        result += source[idx:end_idx]
        idx += batch_size
    return result


def validate_batch_size(batch_size: int) -> int:
    if batch_size < 1:
        raise ValueError('count must be at least 1')
    return batch_size
