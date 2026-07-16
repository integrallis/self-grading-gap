# file: bank_ocr.py
from candidate.impl import AccountNumberOCR


def parse_entry(entry):
    return AccountNumberOCR(entry).decode()


def account_status(entry):
    return AccountNumberOCR(entry).classify_entry()


def fix_entry(entry):
    return AccountNumberOCR(entry).repair_entry()


def checksum_valid(number):
    return AccountNumberOCR("\n\n\n").checksum(number)
