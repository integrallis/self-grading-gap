# file: bank_ocr/checksum_valid.py

from candidate.impl import AccountNumberOCR

account_ocr = AccountNumberOCR()

def checksum_valid(account_number):
    return account_ocr.validate_checksum(account_number)
