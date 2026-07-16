# candidate/impl.py

class LineBoundedCopier:
    def __init__(self, batch_size=None):
        if batch_size is not None:
            if batch_size < 1:
                raise ValueError("count must be at least 1")
            self.batch_size = batch_size
        else:
            self.batch_size = 1

    def copy_one_character(self, source, destination):
        for char in source:
            if char == '\n':
                break
            destination.write(char)

    def copy_in_batches(self, source, destination):
        while True:
            batch = source.read(self.batch_size)
            if not batch:
                break
            
            if '\n' in batch:
                index = batch.index('\n')
                destination.write(batch[:index])
                break
            else:
                destination.write(batch)

    def copy(self, source, destination):
        if self.batch_size == 1:
            self.copy_one_character(source, destination)
        else:
            self.copy_in_batches(source, destination)
