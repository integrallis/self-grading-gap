# file: zombie_survivor.py
from candidate import Game, Survivor

HOARD = "Hoard"
SNIPER = "Sniper"
TOUGH = "Tough"
PLUS_ONE_ACTION = "Plus One Action"


class Level:
    BLUE = "Blue"
    YELLOW = "Yellow"
    ORANGE = "Orange"


Survivor.wound = Survivor.take_wound
Game.add_listener = Game.update_history
