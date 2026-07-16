import random
from typing import List, Dict, Tuple

class Tower:
    DAMAGE_TABLE = {
        'Blue': {1: (2, 5), 2: (5, 9), 3: (9, 12), 4: (12, 15)},
        'Red': {1: (2, 5), 2: (5, 9), 3: (9, 12), 4: (12, 15)},
        'BlueRed': {1: (2, 2), 2: (2, 4), 3: (4, 6), 4: (6, 8)}
    }

    def __init__(self, color: str, level: int):
        if level < 1 or level > 4:
            raise ValueError(f"tower level must be between 1 and 4, got {level}")
        if color not in self.DAMAGE_TABLE:
            raise ValueError(f"Invalid tower color: {color}")
        self.color = color
        self.level = level

    def attack(self, jelly_color: str, random_source) -> int:
        if jelly_color == 'Blue' and self.color == 'Blue':
            damage = random.randint(*self.DAMAGE_TABLE['Blue'][self.level])
        elif jelly_color == 'Red' and self.color == 'Red':
            damage = random.randint(*self.DAMAGE_TABLE['Red'][self.level])
        elif jelly_color == 'Blue' and self.color == 'BlueRed':
            damage = random.randint(*self.DAMAGE_TABLE['BlueRed'][self.level])
        elif jelly_color == 'Red' and self.color == 'BlueRed':
            damage = random.randint(*self.DAMAGE_TABLE['BlueRed'][self.level])
        elif jelly_color == 'Blue' and self.color == 'Red':
            damage = 0
        elif jelly_color == 'Red' and self.color == 'Blue':
            damage = 0
        else:
            damage = self.DAMAGE_TABLE[self.color][self.level][1]  # Fixed damage case
        
        return damage


class Jelly:
    def __init__(self, color: str, health: int):
        self.color = color
        self.health = health

    def take_damage(self, amount: int) -> None:
        if self.health <= 0:
            raise ValueError("Cannot attack a dead jelly")
        self.health -= amount

    def is_alive(self) -> bool:
        return self.health > 0


class CombatRound:
    def __init__(self, towers: List[Tower], jellies: List[Jelly]):
        self.towers = towers
        self.jellies = jellies
        self.log = []

    def fight(self, random_source) -> List[Dict[str, str]]:
        for tower in self.towers:
            for jelly in self.jellies:
                if jelly.is_alive():
                    damage = tower.attack(jelly.color, random_source)
                    if damage > 0:
                        jelly.take_damage(damage)
                        self.log.append({
                            'tower': tower.color,
                            'jelly': jelly.color,
                            'damage': damage
                        })
                    if not jelly.is_alive():
                        break
        self.jellies = [jelly for jelly in self.jellies if jelly.is_alive()]
        return self.log


class Battle:
    def __init__(self, towers: List[Tower], jellies: List[Jelly]):
        self.towers = towers
        self.jellies = jellies

    def fight_until_complete(self, random_source) -> List[Dict[str, str]]:
        complete_log = []
        while self.jellies:
            round_fight = CombatRound(self.towers, self.jellies)
            round_log = round_fight.fight(random_source)
            complete_log.extend(round_log)
        return complete_log
