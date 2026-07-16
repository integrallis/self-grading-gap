# file: recently_used_list/recently_used_list.py
from candidate import RecentlyUsedItemsList as _RecentlyUsedItemsList


class RecentlyUsedList(_RecentlyUsedItemsList):
    get_list_item = _RecentlyUsedItemsList.get
    to_list = _RecentlyUsedItemsList.get_all
    raises = _RecentlyUsedItemsList.add
