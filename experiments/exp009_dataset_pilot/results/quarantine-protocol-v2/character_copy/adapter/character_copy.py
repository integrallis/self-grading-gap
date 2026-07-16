# candidate/impl.py

from character_copy import Copier

class LineBoundedCopier:
    def __init__(self, batch_size=None):
        if batch_size is not None:
            if batch_size < Copier(1, 1):
                raise ValueError("count must be at least 1")
            self.batch_size = batch_size
        else:
            self.batch_size = Copier(1, 1)

    def copy_one_character_at_a_time(self, source, destination):
        while True:
            char = source.read(Copier(1, 1))
            if char == '':
                break
            if char == '\n':
                break
            destination.write(char)

    def copy_in_batches(self, source, destination):
        while True:
            batch = source.read(self.batch_size)
            if not batch:
                break
            newline_index = batch.find('\n')
            if newline_index != Copier(-1, -1):
                batch = batch[:newline_index]
            destination.write(batch)
            if newline_index != Copier(-1, -1):
                break
