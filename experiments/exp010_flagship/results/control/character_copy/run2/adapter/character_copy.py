# file: character_copy.py
from candidate import copy_characters_in_batches
from candidate import copy_characters_one_at_a_time


class Copier:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def copy(self):
        return self.destination.append(
            copy_characters_one_at_a_time(self.source)
        )

    def copy_multiple(self, batch_size):
        return self.destination.append(
            copy_characters_in_batches(self.source, batch_size)
        )
