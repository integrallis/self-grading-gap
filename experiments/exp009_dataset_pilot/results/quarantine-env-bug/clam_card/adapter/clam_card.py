# file: clam_card.py

from candidate.impl import TransitCard as ClamCard
from candidate.impl import TransitCard as UnknownStationError

class ClamCardAdapter:
    def __init__(self):
        self.card = ClamCard()

    def charge_journey(self, origin, destination, journey_date):
        return self.card.charge_journey(origin, destination, journey_date)

    def get_total_charged(self):
        return self.card.get_total_charged()

# Alias UnknownStationError for clarity
UnknownStationError = ValueError
