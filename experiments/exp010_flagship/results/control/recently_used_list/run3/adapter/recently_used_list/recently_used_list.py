# file: recently_used_list/recently_used_list.py
from candidate import RecentlyUsedItemsList


class RecentlyUsedList(RecentlyUsedItemsList):
    def add(self, item):
        return self.add_item(item)

    def count(self):
        return self.item_count()

    def get_list_item(self, index):
        return self.get_item(index)

    def raises(self, index):
        return self.get_item(index)

    def to_list(self):
        return self.read_all()
