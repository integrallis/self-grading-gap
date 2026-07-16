# file: clam_card.py
from candidate.impl import TransitCard as ClamCard
from candidate.impl import UnknownStationError

ClamCard.journey = ClamCard.charge_journey
