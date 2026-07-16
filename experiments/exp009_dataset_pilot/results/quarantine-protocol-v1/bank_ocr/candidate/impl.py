# candidate/impl.py

class AccountNumberOCR:
    DIGITS = {
        '0': [" _ ", "| |", "|_|"],
        '1': ["   ", "  |", "  |"],
        '2': [" _ ", " _|", "|_ "],
        '3': [" _ ", " _|", " _|"],
        '4': ["   ", "|_|", "  |"],
        '5': [" _ ", "|_ ", " _|"],
        '6': [" _ ", "|_ ", "|_|"],
        '7': [" _ ", "  |", "  |"],
        '8': [" _ ", "|_|", "|_|"],
        '9': [" _ ", "|_|", " _|"]
    }
    
    def __init__(self, entry):
        self.entry = entry.strip().splitlines()
        self.validate_entry()

    def validate_entry(self):
        if len(self.entry) not in (3, 4):
            raise ValueError("entry must have exactly three lines")
        if len(self.entry) == 4:
            self.entry.pop()  # ignore the trailing blank line
        self.entry = [line.ljust(27) for line in self.entry]  # pad lines with spaces

    def decode(self):
        account_number = ""
        for i in range(9):
            cell = [self.entry[j][i*3:(i*3)+3] for j in range(3)]
            digit = self.recognize_digit(cell)
            account_number += digit
        return account_number

    def recognize_digit(self, cell):
        for digit, patterns in self.DIGITS.items():
            if cell == patterns:
                return digit
        return '?'

    def validate_checksum(self, account_number):
        if len(account_number) != 9 or not account_number.isdigit():
            return False
        total = sum(int(digit) * (9 - i) for i, digit in enumerate(account_number))
        return total % 11 == 0

    def classify_entry(self):
        account_number = self.decode()
        if '?' in account_number:
            return f"{account_number} ILL"
        
        if self.validate_checksum(account_number):
            return account_number
        return f"{account_number} ERR"

    def repair_entry(self):
        original = self.decode()
        if self.validate_checksum(original):
            return original
        
        candidates = set()
        for i in range(9):
            if original[i] == '?':
                for digit in self.DIGITS.keys():
                    repaired = list(original)
                    repaired[i] = digit
                    repaired_str = ''.join(repaired)
                    if self.validate_checksum(repaired_str):
                        candidates.add(repaired_str)
            else:
                for digit in self.DIGITS.keys():
                    if original[i] != digit:
                        repaired = list(original)
                        repaired[i] = digit
                        repaired_str = ''.join(repaired)
                        if self.validate_checksum(repaired_str):
                            candidates.add(repaired_str)

        if len(candidates) == 1:
            return candidates.pop()
        elif len(candidates) > 1:
            return f"{original} AMB [{', '.join(sorted(f'\'{c}\'' for c in candidates))}]"
        
        return f"{original} ERR"

def main(entry):
    ocr = AccountNumberOCR(entry)
    return ocr.classify_entry()
