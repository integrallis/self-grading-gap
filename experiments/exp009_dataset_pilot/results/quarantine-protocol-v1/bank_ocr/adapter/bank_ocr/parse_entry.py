# file: bank_ocr/parse_entry.py

from candidate.impl import AccountNumberOCR

def parse_entry(entry):
    ocr = AccountNumberOCR(entry)
    return ocr.decode()
