# file: character_copy.py
from candidate.impl import LineBoundedCopier


class Copier:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def copy(self):
        return LineBoundedCopier().copy_one_character_at_a_time(
            self.source,
            self.destination,
        )

    def copy_multiple(self, batch_size):
        return LineBoundedCopier(batch_size).copy_in_batches(
            self.source,
            self.destination,
        )
