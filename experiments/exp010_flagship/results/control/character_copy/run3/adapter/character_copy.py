# file: character_copy.py
from candidate import copy_in_batches, copy_one_character_at_a_time


class Copier:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def copy(self):
        return self.destination.append(copy_one_character_at_a_time(self.source))

    def copy_multiple(self, count):
        return self.destination.append(copy_in_batches(self.source, count))
