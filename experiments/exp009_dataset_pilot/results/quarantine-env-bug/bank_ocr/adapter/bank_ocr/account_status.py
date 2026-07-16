# file: bank_ocr/account_status.py
from candidate.impl import AccountNumberOCR

def account_status(entry):
    ocr = AccountNumberOCR(entry)
    return ocr.classify_entry()

# file: bank_ocr/checksum_valid.py
from candidate.impl import AccountNumberOCR

def checksum_valid(entry):
    ocr = AccountNumberOCR(entry)
    return ocr.validate_checksum()

# file: bank_ocr/fix_entry.py
from candidate.impl import AccountNumberOCR

def fix_entry(entry):
    ocr = AccountNumberOCR(entry)
    return ocr.repair_entry()

# file: bank_ocr/parse_entry.py
from candidate.impl import AccountNumberOCR

def parse_entry(entry):
    ocr = AccountNumberOCR(entry)
    return ocr.decoded_number
