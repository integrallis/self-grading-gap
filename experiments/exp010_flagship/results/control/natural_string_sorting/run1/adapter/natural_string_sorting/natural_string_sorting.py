# file: natural_string_sorting/natural_string_sorting.py
from candidate import natural_sort


class NaturalStringSorting:
    def sort_string(self, items, descending=False):
        return natural_sort(items, descending)
