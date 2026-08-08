import pytest
from solution import Tower, Jelly, combat_round

# US-1: Look up damage from the table
def test_tower_damage_self_color_level_1():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Level 1 Blue to Blue: 2 to 5 damage
    assert 2 <= damage <= 5

def test_tower_damage_self_color_level_2():
    tower = Tower(color='Red', level=2)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # Level 2 Red to Red: 5 to 9 damage
    assert 5 <= damage <= 9

def test_tower_damage_self_color_level_3():
    tower = Tower(color='Blue', level=3)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Level 3 Blue to Blue: 9 to 12 damage
    assert 9 <= damage <= 12

def test_tower_damage_self_color_level_4():
    tower = Tower(color='Red', level=4)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # Level 4 Red to Red: 12 to 15 damage
    assert 12 <= damage <= 15

def test_tower_damage_opposite_color_level_1():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # Level 1 Blue to Red: 0 damage
    assert damage == 0

def test_tower_damage_opposite_color_level_2():
    tower = Tower(color='Red', level=2)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Level 2 Red to Blue: 1 damage
    assert damage == 1

def test_tower_damage_opposite_color_level_3():
    tower = Tower(color='Blue', level=3)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # Level 3 Blue to Red: 2 damage
    assert damage == 2

def test_tower_damage_opposite_color_level_4():
    tower = Tower(color='Red', level=4)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Level 4 Red to Blue: 3 damage
    assert damage == 3

def test_tower_damage_dual_color_level_1():
    tower = Tower(color='BlueRed', level=1)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Level 1 BlueRed to Blue: 2 damage
    assert damage == 2

def test_tower_damage_dual_color_level_2():
    tower = Tower(color='BlueRed', level=2)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # Level 2 BlueRed to Red: 2 to 4 damage
    assert 2 <= damage <= 4

def test_tower_damage_dual_color_level_3():
    tower = Tower(color='BlueRed', level=3)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # Level 3 BlueRed to Red: 4 to 6 damage
    assert 4 <= damage <= 6

def test_tower_damage_dual_color_level_4():
    tower = Tower(color='BlueRed', level=4)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # Level 4 BlueRed to Red: 6 to 8 damage
    assert 6 <= damage <= 8

def test_tower_damage_against_dual_color_jelly():
    tower = Tower(color='Blue', level=3)
    jelly = Jelly(color='BlueRed', health=10)
    damage = tower.attack(jelly)  # Should roll in range 9 to 12
    assert 9 <= damage <= 12

def test_tower_damage_against_dual_color_jelly_red():
    tower = Tower(color='Red', level=2)
    jelly = Jelly(color='BlueRed', health=10)
    damage = tower.attack(jelly)  # Should roll in range 5 to 9
    assert 5 <= damage <= 9

def test_invalid_tower_level_below_range():
    with pytest.raises(Exception) as excinfo:
        Tower(color='Blue', level=0)
    assert str(excinfo.value) == "tower level must be between 1 and 4, got 0"

def test_invalid_tower_level_above_range():
    with pytest.raises(Exception) as excinfo:
        Tower(color='Blue', level=5)
    assert str(excinfo.value) == "tower level must be between 1 and 4, got 5"

# US-2: Track jelly health and death
def test_jelly_alive_health_positive():
    jelly = Jelly(color='Blue', health=10)
    assert jelly.is_alive() is True

def test_jelly_dead_health_zero():
    jelly = Jelly(color='Blue', health=0)
    assert jelly.is_alive() is False

def test_jelly_takes_damage():
    jelly = Jelly(color='Blue', health=10)
    jelly.health -= 5  # Health should reduce from 10 to 5
    assert jelly.health == 5

def test_jelly_takes_exact_damage_to_zero():
    jelly = Jelly(color='Blue', health=5)
    jelly.health -= 5  # Health should reduce from 5 to 0
    assert jelly.health == 0
    assert jelly.is_alive() is False

def test_jelly_cannot_be_attacked_when_dead():
    jelly = Jelly(color='Blue', health=0)
    tower = Tower(color='Red', level=2)
    with pytest.raises(Exception):
        tower.attack(jelly)  # Should not be able to attack a dead jelly

# US-3: Roll attacks reproducibly
def test_attack_reports_damage_and_reduces_health():
    tower = Tower(color='Red', level=3)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)
    assert jelly.health == 10 - damage
    assert damage == 2  # Level 3 Red to Blue = 2 damage

def test_attack_fixed_damage():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)
    assert jelly.health == 10  # Jelly health remains unchanged

def test_attack_with_deterministic_randomness():
    import random
    random.seed(42)  # Seed for reproducibility
    tower1 = Tower(color='Blue', level=2)
    tower2 = Tower(color='Red', level=2)
    
    jelly1 = Jelly(color='Red', health=10)
    jelly2 = Jelly(color='Blue', health=10)
    
    damage1 = tower1.attack(jelly1)
    damage2 = tower2.attack(jelly2)
    
    assert damage1 == 1  # Blue level 2 to Red
    assert damage2 == 1  # Red level 2 to Blue

def test_attack_with_fixed_entries():
    tower = Tower(color='Red', level=1)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)
    assert damage == 0  # Jelly health remains unchanged

# US-4: Fight rounds with a combat log
def test_round_with_towers_attacking_jelly():
    tower1 = Tower(color='Blue', level=1)
    tower2 = Tower(color='Red', level=2)
    jelly = Jelly(color='Red', health=10)
    
    log = combat_round([tower1, tower2], [jelly])
    assert len(log) == 2  # Two attacks in this round

def test_round_with_killed_jelly():
    tower = Tower(color='Blue', level=4)
    jelly = Jelly(color='Red', health=3)
    
    log = combat_round([tower], [jelly])
    assert jelly.health == 0  # Jelly should be killed
    assert len(log) == 1  # One attack should be logged

def test_round_with_no_living_jellies():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Red', health=0)
    
    log = combat_round([tower], [jelly])
    assert len(log) == 0  # No attacks should be logged

def test_successive_rounds():
    tower = Tower(color='Blue', level=1)
    jelly1 = Jelly(color='Red', health=1)  # To ensure it gets killed
    jelly2 = Jelly(color='Red', health=2)
    
    log = combat_round([tower], [jelly1, jelly2])
    assert len(log) == 1  # One attack should be logged, jelly1 killed

    log = combat_round([tower], [jelly1, jelly2])
    assert len(log) == 1  # One attack against jelly2

    log = combat_round([tower], [jelly1, jelly2])
    assert len(log) == 0  # No jellies remain to attack