# file: clam_card.py

from candidate.impl import TransitCard as ClamCard
from candidate.impl import UnknownStationError

def journey(origin, destination, journey_date):
    card = ClamCard()
    return card.charge_journey(origin, destination, journey_date)

def raises(exception):
    return Exception(exception)

