# file: bank_ocr/fix_entry.py

from candidate.impl import AccountNumberOCR

account_ocr = AccountNumberOCR()

def fix_entry(account_number):
    return account_ocr.repair_entry(account_number)
