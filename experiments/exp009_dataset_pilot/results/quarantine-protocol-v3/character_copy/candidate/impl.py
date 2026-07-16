# candidate/impl.py

class LineBoundedCopier:
    def __init__(self, batch_size=None):
        if batch_size is not None:
            if batch_size < 1:
                raise ValueError("count must be at least 1")
            self.batch_size = batch_size
        else:
            self.batch_size = 1  # Default to copying one character at a time

    def copy(self, source, destination):
        if not source:
            return
        
        if self.batch_size == 1:
            self._copy_one_character_at_a_time(source, destination)
        else:
            self._copy_in_batches(source, destination)

    def _copy_one_character_at_a_time(self, source, destination):
        for char in source:
            if char == '\n':
                break
            destination.write(char)

    def _copy_in_batches(self, source, destination):
        buffer = ''
        while True:
            batch = source.read(self.batch_size)
            if not batch:
                if buffer:
                    destination.write(buffer)
                break
            
            if '\n' in batch:
                index = batch.index('\n')
                buffer += batch[:index]
                destination.write(buffer)
                break
            
            buffer += batch
            destination.write(buffer)
            buffer = ''  # Reset buffer after writing

        if buffer:  # Write any remaining buffer after loop
            destination.write(buffer)
