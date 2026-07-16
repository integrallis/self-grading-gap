# file: bank_ocr/checksum_valid.py

from candidate.impl import AccountNumberOCR

def checksum_valid(account_number):
    ocr = AccountNumberOCR('')
    return ocr.validate_checksum(account_number)
