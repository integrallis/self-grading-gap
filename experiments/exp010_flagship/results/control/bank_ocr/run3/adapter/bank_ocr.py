# file: bank_ocr.py
from candidate import classify_entry as account_status
from candidate import validate_account_number as checksum_valid
from candidate import repair_entry as fix_entry
from candidate import decode_entry as parse_entry
