# file: jelly_vs_tower.py
from candidate.impl import Battle as _Battle
from candidate.impl import Jelly as _Jelly
from candidate.impl import Tower as _Tower


class Color:
    BLUE = "Blue"
    RED = "Red"
    BLUE_RED = "BlueRed"
    Blue = BLUE
    Red = RED
    BlueRed = BLUE_RED


class Jelly(_Jelly):
    def __init__(self, color, health, unused):
        super().__init__(color, health)


class Tower(_Tower):
    def __init__(self, color, level, unused):
        super().__init__(color, level)


class Battle(_Battle):
    def __init__(self, towers, jellies, rng):
        super().__init__()
        self.towers = towers
        self.jellies = jellies
        self.rng = rng

    def fight_round(self):
        return super().fight_round(self.rng)


class _ProbeJelly:
    def __init__(self, color):
        self.color = color

    def is_alive(self):
        return True

    def take_damage(self, damage):
        self.damage = damage


class _RangeRandom:
    def randint(self, *values):
        return values


def damage_range(tower_color, jelly_color, level):
    return _Tower(tower_color, level).attack(
        _ProbeJelly(jelly_color),
        _RangeRandom(),
    )
