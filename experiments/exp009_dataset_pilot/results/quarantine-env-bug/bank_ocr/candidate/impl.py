# candidate/impl.py

class AccountNumberOCR:
    DIGIT_PATTERNS = [
        [" _ ", "| |", "|_|"],  # 0
        ["   ", "  |", "  |"],  # 1
        [" _ ", " _|", "|_ "],  # 2
        [" _ ", " _|", " _|"],  # 3
        ["   ", "|_|", "  |"],  # 4
        [" _ ", "|_ ", " _|"],  # 5
        [" _ ", "|_ ", "|_|"],  # 6
        [" _ ", "  |", "  |"],  # 7
        [" _ ", "|_|", "|_|"],  # 8
        [" _ ", "|_|", " _|"],  # 9
    ]

    def __init__(self, entry):
        self.entry = self._prepare_entry(entry)
        self.decoded_number = self.decode(self.entry)

    def _prepare_entry(self, entry):
        lines = entry.splitlines()
        if len(lines) < 3:
            raise ValueError("entry must have exactly three lines")
        # Ignore trailing blank lines
        return [line.ljust(27) for line in lines[:3]]

    def decode(self, lines):
        digits = []
        for i in range(9):
            cell = [line[i * 3:(i + 1) * 3] for line in lines]
            digit = self._recognize_digit(cell)
            digits.append(digit)
        return ''.join(digits)

    def _recognize_digit(self, cell):
        for idx, pattern in enumerate(self.DIGIT_PATTERNS):
            if cell == pattern:
                return str(idx)
        return '?'

    def validate_checksum(self):
        number = self.decoded_number
        if len(number) != 9 or not number.isdigit():
            return False
        weighted_sum = sum((9 - i) * int(digit) for i, digit in enumerate(number))
        return weighted_sum % 11 == 0

    def classify_entry(self):
        if '?' in self.decoded_number:
            return f"{self.decoded_number} ILL"
        if self.validate_checksum():
            return self.decoded_number
        return f"{self.decoded_number} ERR"

    def repair_entry(self):
        if self.validate_checksum() and '?' not in self.decoded_number:
            return self.decoded_number
        
        candidates = self._generate_repair_candidates()
        valid_candidates = [num for num in candidates if self.validate_number(num)]

        if len(valid_candidates) == 1:
            return valid_candidates[0]
        elif len(valid_candidates) > 1:
            return f"{self.decoded_number} AMB {sorted(repr(num) for num in valid_candidates)}"
        else:
            return f"{self.decoded_number} ILL"

    def _generate_repair_candidates(self):
        candidates = []
        for i in range(9):
            for j in range(3):
                for replacement in [' ', '_', '|']:
                    if self.DIGIT_PATTERNS[int(self.decoded_number[i])][j] != replacement:
                        new_digit = list(self.DIGIT_PATTERNS[int(self.decoded_number[i])])
                        new_digit[j] = replacement
                        new_number = self.decoded_number[:i] + self._recognize_digit(new_digit) + self.decoded_number[i + 1:]
                        candidates.append(new_number)
        return candidates

    def validate_number(self, number):
        weighted_sum = sum((9 - i) * int(digit) for i, digit in enumerate(number))
        return weighted_sum % 11 == 0

def process_entry(entry):
    ocr = AccountNumberOCR(entry)
    return ocr.classify_entry()
