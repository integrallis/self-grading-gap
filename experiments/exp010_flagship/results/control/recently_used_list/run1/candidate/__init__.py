class RecentlyUsedItemsList:
    def __init__(self, capacity=5):
        self.capacity = capacity
        self.items = []

    def add(self, item):
        if item is None or item == '':
            raise ValueError(f"List items should not be Empty or Null. But it was [{item}]")
        if item in self.items:
            return  # Do not increase count for duplicates
        self.items.insert(0, item)
        if len(self.items) > self.capacity:
            self.items.pop()

    def count(self):
        return len(self.items)

    def get(self, index):
        if index < 0 or index >= len(self.items):
            raise IndexError(f"supplied index [{index}] should not greater than [{len(self.items) - 1}].")
        return self.items[index]

    def get_all(self):
        return self.items