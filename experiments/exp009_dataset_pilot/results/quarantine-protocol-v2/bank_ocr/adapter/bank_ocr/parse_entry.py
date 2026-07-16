# file: bank_ocr/parse_entry.py

from candidate.impl import AccountNumberOCR

account_ocr = AccountNumberOCR()

def parse_entry(lines):
    return account_ocr.process_entry(lines)
