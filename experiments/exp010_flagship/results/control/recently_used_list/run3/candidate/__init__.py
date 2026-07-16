class RecentlyUsedItemsList:
    def __init__(self, capacity=5):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        if item is None or item == "":
            raise ValueError(f"List items should not be Empty or Null. But it was no value.")
        if item in self.items:
            return
        self.items.insert(0, item)
        if len(self.items) > self.capacity:
            self.items.pop()

    def read_all(self):
        return self.items.copy()

    def item_count(self):
        return len(self.items)

    def get_item(self, index):
        if index < 0 or index >= len(self.items):
            raise IndexError(f"supplied index {index} should not be greater than {len(self.items) - 1}.")
        return self.items[index]