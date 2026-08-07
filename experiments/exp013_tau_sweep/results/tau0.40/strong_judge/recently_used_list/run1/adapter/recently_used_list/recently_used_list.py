# file: recently_used_list/recently_used_list.py
from candidate import RecentlyUsedItemsList


class RecentlyUsedList(RecentlyUsedItemsList):
    get_list_item = RecentlyUsedItemsList.get
    to_list = RecentlyUsedItemsList.get_all
    raises = RecentlyUsedItemsList.add
