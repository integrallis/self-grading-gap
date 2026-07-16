import random
from typing import List, Dict, Tuple, Optional

class Tower:
    DAMAGE_TABLE = {
        'Blue': {1: (2, 5), 2: (5, 9), 3: (9, 12), 4: (12, 15)},
        'Red': {1: (2, 5), 2: (5, 9), 3: (9, 12), 4: (12, 15)},
        'BlueRed': {1: (2, 2), 2: (2, 4), 3: (4, 6), 4: (6, 8)}
    }
    
    OPPONENT_DAMAGE = {
        'Blue': {'Blue': 0, 'Red': 1},
        'Red': {'Blue': 2, 'Red': 0},
        'BlueRed': {'Blue': 2, 'Red': 2}
    }

    def __init__(self, color: str, level: int):
        if level < 1 or level > 4:
            raise ValueError(f"Tower level must be between 1 and 4, got {level}")
        self.color = color
        self.level = level

    def attack(self, jelly: 'Jelly', rng: random.Random) -> Optional[int]:
        if not jelly.is_alive():
            raise ValueError("Cannot attack a dead jelly.")
        
        if self.color in ['Blue', 'Red']:
            damage_range = self.DAMAGE_TABLE[self.color][self.level]
            if jelly.color == self.color:
                damage = rng.randint(*damage_range)
            else:
                damage = self.OPPONENT_DAMAGE[self.color][jelly.color]
        else:  # BlueRed
            damage_blue = rng.randint(*self.DAMAGE_TABLE['Blue'][self.level])
            damage_red = rng.randint(*self.DAMAGE_TABLE['Red'][self.level])
            damage = max(damage_blue, damage_red)
        
        jelly.take_damage(damage)
        return damage

class Jelly:
    def __init__(self, color: str, health: int):
        self.color = color
        self.health = health

    def is_alive(self) -> bool:
        return self.health > 0

    def take_damage(self, damage: int):
        if not self.is_alive():
            raise ValueError("Cannot damage a dead jelly.")
        self.health -= damage

class Combat:
    def __init__(self, towers: List[Tower], jellies: List[Jelly]):
        self.towers = towers
        self.jellies = jellies
        self.log = []

    def fight_round(self, rng: random.Random) -> List[str]:
        if all(not jelly.is_alive() for jelly in self.jellies):
            return []

        for tower in self.towers:
            for jelly in self.jellies:
                if jelly.is_alive():
                    damage = tower.attack(jelly, rng)
                    self.log.append(f"{tower.color} Tower attacks {jelly.color} Jelly for {damage} damage.")
                    if not jelly.is_alive():
                        self.log.append(f"{jelly.color} Jelly has been defeated.")
                    break
        self.jellies = [jelly for jelly in self.jellies if jelly.is_alive()]
        return self.log

    def combat_log(self) -> List[str]:
        return self.log
