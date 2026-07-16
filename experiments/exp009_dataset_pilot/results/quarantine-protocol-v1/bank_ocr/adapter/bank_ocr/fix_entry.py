# file: bank_ocr/fix_entry.py

from candidate.impl import AccountNumberOCR

def fix_entry(entry):
    ocr = AccountNumberOCR(entry)
    return ocr.repair_entry()
