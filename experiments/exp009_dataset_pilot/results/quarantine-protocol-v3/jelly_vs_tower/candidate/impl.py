import random
from typing import List, Dict, Tuple, Union

class InvalidTowerLevelError(Exception):
    def __init__(self, level):
        super().__init__(f"tower level must be between 1 and 4, got {level}")

class Jelly:
    def __init__(self, color: str, health: int):
        self.color = color
        self.health = health

    def is_alive(self) -> bool:
        return self.health > 0

    def take_damage(self, damage: int) -> None:
        if not self.is_alive():
            raise ValueError("Cannot attack a dead jelly.")
        self.health = max(0, self.health - damage)

class Tower:
    DAMAGE_TABLE = {
        'Blue': {1: (2, 5), 2: (5, 9), 3: (9, 12), 4: (12, 15)},
        'Red': {1: (2, 5), 2: (5, 9), 3: (9, 12), 4: (12, 15)},
        'BlueRed': {1: (2, 2), 2: (2, 4), 3: (4, 6), 4: (6, 8)},
    }
    
    FIXED_DAMAGE_TABLE = {
        ('Blue', 'Red'): {1: 0, 2: 1, 3: 2, 4: 3},
        ('Red', 'Blue'): {1: 0, 2: 1, 3: 2, 4: 3},
    }

    def __init__(self, color: str, level: int):
        if level < 1 or level > 4:
            raise InvalidTowerLevelError(level)
        self.color = color
        self.level = level

    def attack(self, jelly: Jelly, rng: random.Random) -> int:
        if not jelly.is_alive():
            raise ValueError("Cannot attack a dead jelly.")
        
        if self.color in ['Blue', 'Red']:
            if self.color == jelly.color:
                damage_range = self.DAMAGE_TABLE[self.color][self.level]
                damage = rng.randint(*damage_range)
            else:
                damage = self.FIXED_DAMAGE_TABLE[(self.color, jelly.color)][self.level]
        else:  # BlueRed
            blue_damage = self.DAMAGE_TABLE['Blue'][self.level]
            red_damage = self.DAMAGE_TABLE['Red'][self.level]
            damage = max(rng.randint(*blue_damage), rng.randint(*red_damage))
        
        jelly.take_damage(damage)
        return damage

class CombatLogEntry:
    def __init__(self, tower: Tower, jelly: Jelly, damage: int):
        self.tower = tower
        self.jelly = jelly
        self.damage = damage

    def __repr__(self):
        return f"{self.tower.color} Tower attacked {self.jelly.color} Jelly for {self.damage} damage."

class Battle:
    def __init__(self):
        self.towers: List[Tower] = []
        self.jellies: List[Jelly] = []
        self.combat_log: List[CombatLogEntry] = []

    def add_tower(self, tower: Tower) -> None:
        self.towers.append(tower)

    def add_jelly(self, jelly: Jelly) -> None:
        self.jellies.append(jelly)

    def fight_round(self, rng: random.Random) -> List[CombatLogEntry]:
        self.combat_log.clear()
        for tower in self.towers:
            for jelly in self.jellies:
                if jelly.is_alive():
                    damage = tower.attack(jelly, rng)
                    self.combat_log.append(CombatLogEntry(tower, jelly, damage))
                    if not jelly.is_alive():
                        break
        self.jellies = [jelly for jelly in self.jellies if jelly.is_alive()]
        return self.combat_log
