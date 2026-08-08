# file: recently_used_list/recently_used_list.py
from candidate import RecentlyUsedItemsList


class RecentlyUsedList(RecentlyUsedItemsList):
    to_list = RecentlyUsedItemsList.read
    get_list_item = RecentlyUsedItemsList.get
    raises = RecentlyUsedItemsList.add
