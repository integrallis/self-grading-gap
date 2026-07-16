# candidate/impl.py

class AccountNumberOCR:
    DIGIT_MAP = {
        ' _ | ||_|': '0',
        '     |  |': '1',
        ' _  _||_ ': '2',
        ' _  _| _|': '3',
        '   |_|  |': '4',
        ' _ |_  _|': '5',
        ' _ |_ |_|': '6',
        ' _   |  |': '7',
        ' _ |_||_|': '8',
        ' _ |_| _|': '9',
    }

    def decode_entry(self, lines):
        if len(lines) < 3 or len(lines) > 4:
            raise ValueError("entry must have exactly three lines")

        lines = [line.ljust(27) for line in lines[:3]]  # Pad shorter lines
        digits = []
        for i in range(0, 27, 3):
            cell = ''.join(line[i:i+3] for line in lines)
            digits.append(self.DIGIT_MAP.get(cell, '?'))
        return ''.join(digits)

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

    def repair_entry(self, account_number):
        if self.validate_checksum(account_number):
            return account_number

        candidates = set()
        for i in range(9):
            for j in range(10):
                repaired = account_number[:i] + str(j) + account_number[i+1:]
                if self.validate_checksum(repaired):
                    candidates.add(repaired)

        if len(candidates) == 1:
            return candidates.pop()
        if len(candidates) > 1:
            return f"{account_number} AMB {sorted(repr(c) for c in candidates)}"
        
        return f"{account_number} ERR"

    def process_entry(self, lines):
        account_number = self.decode_entry(lines)
        classification = self.classify_entry(account_number)
        if '?' in account_number:
            repaired = self.repair_entry(account_number)
            return repaired if repaired != account_number else classification
        return classification
