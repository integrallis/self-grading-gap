# test_solution.py

import pytest
from solution import lookup_damage, Jelly, Tower, fight_rounds

# US-1: Look up damage from the table
def test_lookup_damage_pure_color_tower_same_color_level_1():
    tower = Tower(color='Blue', level=1)
    damage = lookup_damage(tower, Jelly(color='Blue', health=10))  # Level 1: 2 to 5
    assert 2 <= damage <= 5

def test_lookup_damage_pure_color_tower_same_color_level_2():
    tower = Tower(color='Red', level=2)
    damage = lookup_damage(tower, Jelly(color='Red', health=10))  # Level 2: 5 to 9
    assert 5 <= damage <= 9

def test_lookup_damage_pure_color_tower_same_color_level_3():
    tower = Tower(color='Blue', level=3)
    damage = lookup_damage(tower, Jelly(color='Blue', health=10))  # Level 3: 9 to 12
    assert 9 <= damage <= 12

def test_lookup_damage_pure_color_tower_same_color_level_4():
    tower = Tower(color='Red', level=4)
    damage = lookup_damage(tower, Jelly(color='Red', health=10))  # Level 4: 12 to 15
    assert 12 <= damage <= 15

def test_lookup_damage_pure_color_tower_opposite_color_level_1():
    tower = Tower(color='Red', level=1)
    damage = lookup_damage(tower, Jelly(color='Blue', health=10))  # Level 1: 0
    assert damage == 0

def test_lookup_damage_pure_color_tower_opposite_color_level_2():
    tower = Tower(color='Blue', level=2)
    damage = lookup_damage(tower, Jelly(color='Red', health=10))  # Level 2: 1
    assert damage == 1

def test_lookup_damage_pure_color_tower_opposite_color_level_3():
    tower = Tower(color='Blue', level=3)
    damage = lookup_damage(tower, Jelly(color='Red', health=10))  # Level 3: 2
    assert damage == 2

def test_lookup_damage_pure_color_tower_opposite_color_level_4():
    tower = Tower(color='Red', level=4)
    damage = lookup_damage(tower, Jelly(color='Blue', health=10))  # Level 4: 3
    assert damage == 3

def test_lookup_damage_dual_color_tower_same_color_level_1():
    tower = Tower(color='BlueRed', level=1)
    damage = lookup_damage(tower, Jelly(color='Blue', health=10))  # Level 1: exactly 2
    assert damage == 2

def test_lookup_damage_dual_color_tower_same_color_level_2():
    tower = Tower(color='BlueRed', level=2)
    damage = lookup_damage(tower, Jelly(color='Red', health=10))  # Level 2: 2 to 4
    assert 2 <= damage <= 4

def test_lookup_damage_dual_color_tower_same_color_level_3():
    tower = Tower(color='BlueRed', level=3)
    damage = lookup_damage(tower, Jelly(color='Blue', health=10))  # Level 3: 4 to 6
    assert 4 <= damage <= 6

def test_lookup_damage_dual_color_tower_same_color_level_4():
    tower = Tower(color='BlueRed', level=4)
    damage = lookup_damage(tower, Jelly(color='Red', health=10))  # Level 4: 6 to 8
    assert 6 <= damage <= 8

def test_lookup_damage_dual_color_tower_dual_color_jelly():
    tower = Tower(color='Blue', level=3)
    damage = lookup_damage(tower, Jelly(color='BlueRed', health=10))  # Level 3: max(9 to 12, 2) = 9 to 12
    assert 9 <= damage <= 12

def test_lookup_damage_red_tower_against_dual_color_jelly():
    tower = Tower(color='Red', level=3)
    damage = lookup_damage(tower, Jelly(color='BlueRed', health=10))  # Level 3: max(2, 9 to 12) = 9 to 12
    assert 9 <= damage <= 12

def test_invalid_tower_level_construction():
    with pytest.raises(Exception, match="tower level must be between 1 and 4, got 0"):
        Tower(color='Blue', level=0)
    with pytest.raises(Exception, match="tower level must be between 1 and 4, got 5"):
        Tower(color='Red', level=5)

def test_invalid_tower_level_lookup():
    tower = Tower(color='Blue', level=1)
    with pytest.raises(Exception, match="tower level must be between 1 and 4, got 0"):
        lookup_damage(Tower(color='Blue', level=0), Jelly(color='Red', health=10))
    with pytest.raises(Exception, match="tower level must be between 1 and 4, got 5"):
        lookup_damage(Tower(color='Red', level=5), Jelly(color='Blue', health=10))

# US-2: Track jelly health and death
def test_jelly_health_initially_alive():
    jelly = Jelly(color='Blue', health=10)
    assert jelly.is_alive() is True

def test_jelly_health_decreases():
    jelly = Jelly(color='Blue', health=10)
    jelly.take_damage(4)
    assert jelly.health == 6

def test_jelly_health_death():
    jelly = Jelly(color='Blue', health=3)
    jelly.take_damage(3)
    assert jelly.is_alive() is False

def test_dead_jelly_cannot_be_attacked():
    jelly = Jelly(color='Blue', health=0)
    with pytest.raises(Exception):
        jelly.take_damage(1)

# US-3: Roll attacks reproducibly
def test_attack_rolls_damage_within_range():
    class RandomSource:
        def __init__(self, seed):
            self.seed = seed
            self.current = seed
        
        def randint(self, a, b):
            # Simple deterministic pseudo-random number generation for testing
            self.current = (self.current * 48271) % 2147483647
            return a + self.current % (b - a + 1)

    random_source = RandomSource(seed=42)
    tower = Tower(color='Blue', level=2)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly, random_source)  # Level 2: 1 damage
    assert damage == 1
    assert jelly.health == 9

def test_attack_fixed_damage():
    class RandomSource:
        def __init__(self, seed):
            self.seed = seed
            self.current = seed
        
        def randint(self, a, b):
            self.current = (self.current * 48271) % 2147483647
            return a + self.current % (b - a + 1)

    random_source = RandomSource(seed=42)
    tower = Tower(color='Red', level=1)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly, random_source)  # Level 1: 0 damage
    assert damage == 0
    assert jelly.health == 10

def test_attack_rolls_damage_within_range_and_state():
    class RandomSource:
        def __init__(self, seed):
            self.seed = seed
            self.current = seed
        
        def randint(self, a, b):
            self.current = (self.current * 48271) % 2147483647
            return a + self.current % (b - a + 1)

    random_source = RandomSource(seed=42)
    tower = Tower(color='Blue', level=2)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly, random_source)  # Level 2: from 5 to 9
    assert 5 <= damage <= 9
    assert jelly.health == 10 - damage

def test_attack_with_fixed_damage_at_bounds():
    class RandomSource:
        def __init__(self, seed):
            self.seed = seed
            self.current = seed
        
        def randint(self, a, b):
            self.current = (self.current * 48271) % 2147483647
            return a + self.current % (b - a + 1)

    random_source = RandomSource(seed=42)
    tower = Tower(color='BlueRed', level=2)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly, random_source)  # Level 2: should be 2 or 3
    assert damage in {2, 3}
    assert jelly.health == 10 - damage

# US-4: Fight rounds with a combat log
def test_fight_rounds_with_log():
    class LogEntry:
        def __init__(self, tower_color, jelly_color, damage):
            self.tower_color = tower_color
            self.jelly_color = jelly_color
            self.damage = damage
    
    class RandomSource:
        def __init__(self, seed):
            self.seed = seed
            self.current = seed
        
        def randint(self, a, b):
            self.current = (self.current * 48271) % 2147483647
            return a + self.current % (b - a + 1)

    random_source = RandomSource(seed=42)
    towers = [Tower(color='Blue', level=1), Tower(color='Red', level=2)]
    jellies = [Jelly(color='Blue', health=10), Jelly(color='Red', health=5)]
    log = fight_rounds(towers, jellies, random_source)

    assert len(log) == 2  # Each tower attacks once
    assert log[0].tower_color == 'Blue'
    assert log[0].jelly_color == 'Blue'
    assert log[0].damage >= 2 and log[0].damage <= 5  # Damage range for Blue tower
    assert log[1].tower_color == 'Red'
    assert log[1].jelly_color == 'Red'
    assert log[1].damage == 1  # Fixed damage for Red tower against Blue jelly

def test_fight_rounds_with_jelly_death():
    class LogEntry:
        def __init__(self, tower_color, jelly_color, damage):
            self.tower_color = tower_color
            self.jelly_color = jelly_color
            self.damage = damage

    class RandomSource:
        def __init__(self, seed):
            self.seed = seed
            self.current = seed
        
        def randint(self, a, b):
            self.current = (self.current * 48271) % 2147483647
            return a + self.current % (b - a + 1)

    random_source = RandomSource(seed=42)
    towers = [Tower(color='Red', level=3)]
    jellies = [Jelly(color='Blue', health=2)]
    log = fight_rounds(towers, jellies, random_source)

    assert len(log) == 1  # Only one attack occurs
    assert log[0].jelly_color == 'Blue'
    assert log[0].damage == 2  # Jelly takes damage and dies
    assert not jellies[0].is_alive()

def test_fight_rounds_with_no_living_jellies():
    class LogEntry:
        def __init__(self, tower_color, jelly_color, damage):
            self.tower_color = tower_color
            self.jelly_color = jelly_color
            self.damage = damage

    class RandomSource:
        def __init__(self, seed):
            self.seed = seed
            self.current = seed
        
        def randint(self, a, b):
            self.current = (self.current * 48271) % 2147483647
            return a + self.current % (b - a + 1)

    random_source = RandomSource(seed=42)
    towers = [Tower(color='Blue', level=1)]
    jellies = [Jelly(color='Red', health=0)]
    log = fight_rounds(towers, jellies, random_source)

    assert len(log) == 0  # No attacks happen

def test_fight_rounds_multiple_attacks():
    class LogEntry:
        def __init__(self, tower_color, jelly_color, damage):
            self.tower_color = tower_color
            self.jelly_color = jelly_color
            self.damage = damage

    class RandomSource:
        def __init__(self, seed):
            self.seed = seed
            self.current = seed
        
        def randint(self, a, b):
            self.current = (self.current * 48271) % 2147483647
            return a + self.current % (b - a + 1)

    random_source = RandomSource(seed=42)
    towers = [Tower(color='Blue', level=2), Tower(color='Red', level=3)]
    jellies = [Jelly(color='Blue', health=10), Jelly(color='Red', health=5)]
    log = fight_rounds(towers, jellies, random_source)

    assert len(log) == 2  # Each tower attacks once
    assert log[0].jelly_color == 'Blue'  # First tower attacks Blue jelly
    assert log[1].jelly_color == 'Red'    # Second tower attacks Red jelly

def test_fight_rounds_with_killed_jelly():
    class LogEntry:
        def __init__(self, tower_color, jelly_color, damage):
            self.tower_color = tower_color
            self.jelly_color = jelly_color
            self.damage = damage

    class RandomSource:
        def __init__(self, seed):
            self.seed = seed
            self.current = seed
        
        def randint(self, a, b):
            self.current = (self.current * 48271) % 2147483647
            return a + self.current % (b - a + 1)

    random_source = RandomSource(seed=42)
    towers = [Tower(color='Blue', level=1), Tower(color='Red', level=2)]
    jellies = [Jelly(color='Blue', health=3), Jelly(color='Red', health=5)]
    log = fight_rounds(towers, jellies, random_source)

    assert len(log) == 2  # Two attacks occur
    assert not jellies[0].is_alive()  # The first jelly should be dead
    assert log[1].jelly_color == 'Red'  # The second tower attacks the still-alive Red jelly

def test_fight_rounds_empty_log_after_all_jellies_defeated():
    class LogEntry:
        def __init__(self, tower_color, jelly_color, damage):
            self.tower_color = tower_color
            self.jelly_color = jelly_color
            self.damage = damage

    class RandomSource:
        def __init__(self, seed):
            self.seed = seed
            self.current = seed
        
        def randint(self, a, b):
            self.current = (self.current * 48271) % 2147483647
            return a + self.current % (b - a + 1)

    random_source = RandomSource(seed=42)
    towers = [Tower(color='Blue', level=1), Tower(color='Red', level=2)]
    jellies = [Jelly(color='Blue', health=0), Jelly(color='Red', health=0)]
    log = fight_rounds(towers, jellies, random_source)
    assert len(log) == 0  # No attacks happen when no jellies are alive

def test_fight_rounds_successive_rounds():
    class LogEntry:
        def __init__(self, tower_color, jelly_color, damage):
            self.tower_color = tower_color
            self.jelly_color = jelly_color
            self.damage = damage

    class RandomSource:
        def __init__(self, seed):
            self.seed = seed
            self.current = seed
        
        def randint(self, a, b):
            self.current = (self.current * 48271) % 2147483647
            return a + self.current % (b - a + 1)

    random_source = RandomSource(seed=42)
    towers = [Tower(color='Blue', level=1), Tower(color='Red', level=2)]
    jellies = [Jelly(color='Blue', health=10), Jelly(color='Red', health=5)]
    fight_rounds(towers, jellies, random_source)  # First round
    log = fight_rounds(towers, jellies, random_source)  # Second round
    assert len(log) == 2  # Expecting 2 attacks again
    assert log[0].jelly_color == 'Blue'  # Validate tower attacking
    assert log[1].jelly_color == 'Red'    # Validate tower attacking