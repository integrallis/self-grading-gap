# candidate/impl.py

class AccountNumberOCR:
    DIGIT_MAP = {
        '0': [' _ ', '| |', '|_|'],
        '1': ['   ', '  |', '  |'],
        '2': [' _ ', ' _|', '|_ '],
        '3': [' _ ', ' _|', ' _|'],
        '4': ['   ', '|_|', '  |'],
        '5': [' _ ', '|_ ', ' _|'],
        '6': [' _ ', '|_ ', '|_|'],
        '7': [' _ ', '  |', '  |'],
        '8': [' _ ', '|_|', '|_|'],
        '9': [' _ ', '|_|', ' _|'],
    }

    def decode_entry(self, lines):
        if len(lines) not in [3, 4]:
            raise ValueError("entry must have exactly three lines")
        if len(lines) == 4:
            lines = lines[:3]  # Ignore the trailing blank line
        lines = [line.ljust(27) for line in lines]
        return ''.join(self._decode_cell(lines, i) for i in range(9))

    def _decode_cell(self, lines, cell_index):
        cell = [lines[row][cell_index * 3:(cell_index + 1) * 3] for row in range(3)]
        for digit, pattern in self.DIGIT_MAP.items():
            if cell == pattern:
                return digit
        return '?'

    def validate_checksum(self, account_number):
        if len(account_number) != 9 or not account_number.isdigit():
            return False
        weighted_sum = sum(int(digit) * (9 - i) for i, digit in enumerate(account_number))
        return weighted_sum % 11 == 0

    def classify_entry(self, account_number):
        if '?' in account_number:
            return f"{account_number} ILL"
        if self.validate_checksum(account_number):
            return account_number
        return f"{account_number} ERR"

    def repair_entry(self, entry):
        original = entry
        if self.validate_checksum(entry):
            return entry  # No change needed
        candidates = set()
        for i in range(9):
            for digit in '0123456789':
                if entry[i] == '?' or entry[i] != digit:
                    possible = entry[:i] + digit + entry[i + 1:]
                    if self.validate_checksum(possible):
                        candidates.add(possible)
        if len(candidates) == 1:
            return candidates.pop()
        if len(candidates) > 1:
            return f"{entry} AMB [{', '.join(sorted(repr(c) for c in candidates))}]"
        return f"{entry} ERR"

    def process_entry(self, lines):
        decoded_number = self.decode_entry(lines)
        classified_entry = self.classify_entry(decoded_number)
        repaired_entry = self.repair_entry(decoded_number)
        return classified_entry if classified_entry == decoded_number else repaired_entry
