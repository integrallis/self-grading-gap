# file: clam_card.py
from candidate.impl import TransitCard, UnknownStationError


class ClamCard(TransitCard):
    journey = TransitCard.travel
