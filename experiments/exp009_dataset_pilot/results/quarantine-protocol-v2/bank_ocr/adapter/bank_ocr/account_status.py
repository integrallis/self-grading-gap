# file: bank_ocr/account_status.py

from candidate.impl import AccountNumberOCR

account_ocr = AccountNumberOCR()

def account_status(account_number):
    return account_ocr.classify_entry(account_number)
