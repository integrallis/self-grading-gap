# file: bank_ocr/account_status.py

from candidate.impl import main as classify_entry

def account_status(entry):
    return classify_entry(entry)
