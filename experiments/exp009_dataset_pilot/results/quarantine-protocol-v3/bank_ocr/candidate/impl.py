# candidate/impl.py

class AccountNumberOCR:
    DIGIT_PATTERNS = {
        '0': [" _ ", "| |", "|_|"],
        '1': ["   ", "  |", "  |"],
        '2': [" _ ", " _|", "|_ "],
        '3': [" _ ", " _|", " _|"],
        '4': ["   ", "|_|", "  |"],
        '5': [" _ ", "|_ ", " _|"],
        '6': [" _ ", "|_ ", "|_|"],
        '7': [" _ ", "  |", "  |"],
        '8': [" _ ", "|_|", "|_|"],
        '9': [" _ ", "|_|", " _|"],
    }

    def __init__(self, entry):
        self.entry = entry.splitlines()
        self.validate_entry()

    def validate_entry(self):
        if len(self.entry) < 3 or len(self.entry) > 4:
            raise ValueError("entry must have exactly three lines")
        for i in range(3):
            self.entry[i] = self.entry[i].ljust(27)

    def decode(self):
        digits = []
        for i in range(9):
            cell = [self.entry[j][i*3:(i+1)*3] for j in range(3)]
            digit = self.recognize_digit(cell)
            digits.append(digit)
        return ''.join(digits)

    def recognize_digit(self, cell):
        for digit, pattern in self.DIGIT_PATTERNS.items():
            if cell == pattern:
                return digit
        return '?'

    def checksum(self, number):
        if len(number) != 9 or not number.isdigit():
            return False
        total = sum(int(digit) * (9 - idx) for idx, digit in enumerate(number))
        return total % 11 == 0

    def classify_entry(self):
        decoded_number = self.decode()
        if '?' in decoded_number:
            return f"{decoded_number} ILL"
        if not self.checksum(decoded_number):
            return f"{decoded_number} ERR"
        return decoded_number

    def repair_entry(self):
        decoded_number = self.decode()
        if '?' not in decoded_number and self.checksum(decoded_number):
            return decoded_number
        candidates = self.generate_candidates(decoded_number)
        valid_candidates = [num for num in candidates if self.checksum(num)]
        if len(valid_candidates) == 1:
            return valid_candidates[0]
        if len(valid_candidates) > 1:
            return f"{decoded_number} AMB {valid_candidates}"
        return f"{decoded_number} ILL"

    def generate_candidates(self, decoded_number):
        candidates = []
        for i in range(9):
            if decoded_number[i] == '?':
                for digit in self.DIGIT_PATTERNS.keys():
                    candidate = decoded_number[:i] + digit + decoded_number[i+1:]
                    candidates.append(candidate)
        return candidates


def process_account_number(entry):
    ocr = AccountNumberOCR(entry)
    return ocr.repair_entry()
