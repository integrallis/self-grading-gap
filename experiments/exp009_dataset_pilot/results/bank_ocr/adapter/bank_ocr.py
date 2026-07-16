# file: bank_ocr.py
from candidate.impl import AccountNumberOCR as _AccountNumberOCR

_ocr = _AccountNumberOCR()

parse_entry = _ocr.decode_entry
checksum_valid = _ocr.validate_checksum
account_status = _ocr.classify_entry
fix_entry = _ocr.repair_entry
