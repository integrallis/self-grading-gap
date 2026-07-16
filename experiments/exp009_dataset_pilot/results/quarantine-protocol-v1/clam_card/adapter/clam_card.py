# file: clam_card.py

from datetime import datetime, timedelta
from candidate.impl import TransitCard as _TransitCard
from candidate.impl import ValueError as _ValueError

class ClamCard:
    def __init__(self):
        self._transit_card = _TransitCard()

    def charge_journey(self, origin, destination, journey_date):
        try:
            return self._transit_card.charge_journey(origin, destination, journey_date)
        except _ValueError:
            return 0.0  # No charge for unknown stations

    def get_total_charged(self):
        return self._transit_card.get_total_charged()


class UnknownStationError(Exception):
    pass

