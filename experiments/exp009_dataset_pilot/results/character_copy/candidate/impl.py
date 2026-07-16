# candidate/impl.py

class LineBoundedCopier:
    def __init__(self, batch_size=1):
        if batch_size < 1:
            raise ValueError("count must be at least 1")
        self.batch_size = batch_size

    def copy_one_character_at_a_time(self, source, destination):
        while True:
            char = source.read(1)
            if not char or char == '\n':
                break
            destination.write(char)

    def copy_in_batches(self, source, destination):
        while True:
            batch = source.read(self.batch_size)
            if not batch:
                break
            
            newline_index = batch.find('\n')
            if newline_index != -1:
                batch = batch[:newline_index]

            destination.write(batch)

            if newline_index != -1:
                break

# Usage examples (commented out)
# with open('source.txt', 'r') as source, open('destination.txt', 'w') as destination:
#     copier = LineBoundedCopier(batch_size=5)
#     copier.copy_in_batches(source, destination)
