# file: clam_card.py
from builtins import ValueError as UnknownStationError
from candidate import TransitCard as _TransitCard


class ClamCard(_TransitCard):
    journey = _TransitCard.take_journey
