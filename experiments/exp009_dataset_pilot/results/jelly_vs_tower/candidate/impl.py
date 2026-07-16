import random
from typing import List, Tuple, Dict, Optional

class Tower:
    DAMAGE_TABLE = {
        "Blue": {1: (2, 5), 2: (5, 9), 3: (9, 12), 4: (12, 15)},
        "Red": {1: (2, 5), 2: (5, 9), 3: (9, 12), 4: (12, 15)},
        "BlueRed": {1: (2, 2), 2: (2, 4), 3: (4, 6), 4: (6, 8)},
    }

    FIXED_DAMAGE_TABLE = {
        ("Blue", "Red"): {1: 0, 2: 1, 3: 2, 4: 3},
        ("Red", "Blue"): {1: 0, 2: 1, 3: 2, 4: 3},
    }

    def __init__(self, color: str, level: int):
        if level < 1 or level > 4:
            raise ValueError(f"tower level must be between 1 and 4, got {level}")
        self.color = color
        self.level = level

    def attack_damage(self, jelly_color: str, rng: random.Random) -> int:
        if self.color in ["Blue", "Red"]:
            if self.color == jelly_color:
                low, high = self.DAMAGE_TABLE[self.color][self.level]
                return rng.randint(low, high)
            elif (self.color, jelly_color) in self.FIXED_DAMAGE_TABLE:
                return self.FIXED_DAMAGE_TABLE[(self.color, jelly_color)][self.level]
            else:
                return 0  # Invalid color combination
        elif self.color == "BlueRed":
            low_blue, high_blue = self.DAMAGE_TABLE["Blue"][self.level]
            low_red, high_red = self.DAMAGE_TABLE["Red"][self.level]
            blue_damage = rng.randint(low_blue, high_blue)
            red_damage = rng.randint(low_red, high_red)
            return max(blue_damage, red_damage)

class Jelly:
    def __init__(self, color: str, health: int):
        self.color = color
        self.health = health

    def take_damage(self, amount: int):
        if self.health > 0:
            self.health -= amount

    @property
    def is_alive(self) -> bool:
        return self.health > 0

class CombatLog:
    def __init__(self):
        self.entries: List[str] = []

    def log_attack(self, tower: Tower, jelly: Jelly, damage: int):
        self.entries.append(f"{tower.color} Tower attacked {jelly.color} Jelly for {damage} damage.")

class Battle:
    def __init__(self, towers: List[Tower], jellies: List[Jelly], rng: random.Random):
        self.towers = towers
        self.jellies = jellies
        self.rng = rng
        self.log = CombatLog()

    def fight_round(self) -> List[str]:
        if not any(jelly.is_alive for jelly in self.jellies):
            return []

        for tower in self.towers:
            for jelly in self.jellies:
                if jelly.is_alive:
                    damage = tower.attack_damage(jelly.color, self.rng)
                    if damage > 0:
                        jelly.take_damage(damage)
                        self.log.log_attack(tower, jelly, damage)
                    break  # Move to the next tower after attacking the first living jelly

        # Remove dead jellies after the round
        self.jellies = [jelly for jelly in self.jellies if jelly.is_alive]
        return self.log.entries
