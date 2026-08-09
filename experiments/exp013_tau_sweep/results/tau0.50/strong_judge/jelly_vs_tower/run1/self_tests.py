import pytest
from solution import Tower, Jelly, Combat
import random

# Test same-color tower attacks for levels 1-4
@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_tower_damage_lookup_same_color(level):
    tower = Tower(color='Blue', level=level)
    jelly = Jelly(color='Blue', health=10)
    if level == 1:
        damage_range = (2, 5)  # Level 1: 2 to 5
    elif level == 2:
        damage_range = (5, 9)  # Level 2: 5 to 9
    elif level == 3:
        damage_range = (9, 12)  # Level 3: 9 to 12
    elif level == 4:
        damage_range = (12, 15)  # Level 4: 12 to 15
    damage = tower.attack(jelly)
    assert damage_range[0] <= damage <= damage_range[1]

# Test same-color Red tower attacks for levels 1-4
@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_tower_damage_lookup_red_same_color(level):
    tower = Tower(color='Red', level=level)
    jelly = Jelly(color='Red', health=10)
    if level == 1:
        damage_range = (2, 5)  # Level 1: 2 to 5
    elif level == 2:
        damage_range = (5, 9)  # Level 2: 5 to 9
    elif level == 3:
        damage_range = (9, 12)  # Level 3: 9 to 12
    elif level == 4:
        damage_range = (12, 15)  # Level 4: 12 to 15
    damage = tower.attack(jelly)
    assert damage_range[0] <= damage <= damage_range[1]

# Test opposite-color tower attacks for levels 1-4
@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_tower_damage_lookup_opposite_color(level):
    tower = Tower(color='Blue', level=level)
    jelly = Jelly(color='Red', health=10)
    if level == 1:
        damage = 0  # Level 1: 0 damage
    elif level == 2:
        damage = 1  # Level 2: 1 damage
    elif level == 3:
        damage = 2  # Level 3: 2 damage
    elif level == 4:
        damage = 3  # Level 4: 3 damage
    assert tower.attack(jelly) == damage

# Test opposite-color Red tower attacks for levels 1-4
@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_tower_damage_lookup_red_opposite_color(level):
    tower = Tower(color='Red', level=level)
    jelly = Jelly(color='Blue', health=10)
    if level == 1:
        damage = 0  # Level 1: 0 damage
    elif level == 2:
        damage = 1  # Level 2: 1 damage
    elif level == 3:
        damage = 2  # Level 3: 2 damage
    elif level == 4:
        damage = 3  # Level 4: 3 damage
    assert tower.attack(jelly) == damage

# Test BlueRed tower attacks against both colors for levels 1-4
@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_tower_damage_lookup_dual_color(level):
    tower = Tower(color='BlueRed', level=level)
    jelly_blue = Jelly(color='Blue', health=10)
    jelly_red = Jelly(color='Red', health=10)
    if level == 1:
        damage_range = (2, 2)  # Level 1: exactly 2
    elif level == 2:
        damage_range = (2, 4)  # Level 2: 2 to 4
    elif level == 3:
        damage_range = (4, 6)  # Level 3: 4 to 6
    elif level == 4:
        damage_range = (6, 8)  # Level 4: 6 to 8
    damage_blue = tower.attack(jelly_blue)
    damage_red = tower.attack(jelly_red)
    assert damage_range[0] <= damage_blue <= damage_range[1]
    assert damage_range[0] <= damage_red <= damage_range[1]

# Test Blue level 4 tower against dual-color jelly to check higher damage selection
def test_tower_damage_lookup_against_dual_color_jelly():
    tower = Tower(color='Blue', level=4)
    jelly = Jelly(color='BlueRed', health=10)
    damage = tower.attack(jelly)  # Level 4: Max of Blue (12-15) or Red (3)
    assert 12 <= damage <= 15

# Test invalid tower level construction
@pytest.mark.parametrize("level", [0, 5])
def test_tower_invalid_level(level):
    with pytest.raises(Exception, match=f"tower level must be between 1 and 4, got {level}"):
        Tower(color='Blue', level=level)

# Test invalid tower level lookup from table
@pytest.mark.parametrize("level", [0, 5])
def test_tower_invalid_level_lookup(level):
    tower = Tower(color='Blue', level=1)  # Initialize with valid level
    jelly = Jelly(color='Red', health=10)
    with pytest.raises(Exception, match=f"tower level must be between 1 and 4, got {level}"):
        tower.attack(jelly)  # Attempt to use invalid level

# Test jelly health status transitions
def test_jelly_health_status():
    jelly = Jelly(color='Blue', health=10)
    assert jelly.is_alive() is True
    jelly.take_damage(10)
    assert jelly.is_alive() is False

# Test jelly taking damage
def test_jelly_take_damage():
    jelly = Jelly(color='Red', health=10)
    jelly.take_damage(5)
    assert jelly.health == 5
    jelly.take_damage(5)
    assert jelly.health == 0

# Test attack reports damage and reduces health
def test_attack_reports_damage_and_reduces_health():
    jelly = Jelly(color='Red', health=10)
    tower = Tower(color='Red', level=2)
    damage = tower.attack(jelly)
    assert jelly.health == 10 - damage

# Test fixed damage lookup for Blue vs Red
def test_attack_fixed_damage_lookup():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)
    assert damage == 0  # Fixed damage for Blue level 1 vs Red

# Test jelly cannot be attacked when dead
def test_jelly_cannot_be_attacked_when_dead():
    jelly = Jelly(color='Red', health=0)
    tower = Tower(color='Blue', level=1)
    with pytest.raises(Exception):
        tower.attack(jelly)  # Attempt to attack a dead jelly

# Test combat rounds with log
def test_rounds_with_combat_log():
    tower1 = Tower(color='Blue', level=1)
    tower2 = Tower(color='Red', level=2)
    jelly1 = Jelly(color='Red', health=10)
    jelly2 = Jelly(color='Blue', health=10)
    combat = Combat([tower1, tower2], [jelly1, jelly2])
    log = combat.fight_round()
    assert len(log) == 2  # Two attacks in the round
    assert log[0]['tower'] == tower1
    assert log[0]['jelly'] == jelly1
    assert log[0]['damage'] == 0  # Blue level 1 vs Red
    assert log[1]['tower'] == tower2
    assert log[1]['jelly'] == jelly1
    assert log[1]['damage'] >= 5 and log[1]['damage'] <= 9  # Red level 2 vs Red

# Test empty round when no jellies exist
def test_empty_round_when_no_jellies():
    tower = Tower(color='Blue', level=1)
    combat = Combat([tower], [])
    log = combat.fight_round()
    assert len(log) == 0  # No jellies means no attacks

# Test rounds until all jellies are defeated
def test_rounds_until_all_jellies_defeated():
    tower1 = Tower(color='Red', level=2)
    jelly1 = Jelly(color='Blue', health=5)
    jelly2 = Jelly(color='Red', health=3)
    combat = Combat([tower1], [jelly1, jelly2])
    log1 = combat.fight_round()  # Attack jelly1
    assert len(log1) == 1  # One attack in the round
    assert jelly1.health <= 0  # Jelly1 takes damage and should be dead
    assert jelly2.health == 3  # Jelly2 was not attacked
    assert len(combat.jellies) == 1  # Jelly2 is still alive

# Test no entries when jellies are exhausted partway through a round
def test_no_entries_when_jellies_exhausted_partway_through_round():
    tower1 = Tower(color='Blue', level=1)
    tower2 = Tower(color='Red', level=2)
    jelly1 = Jelly(color='Red', health=1)
    jelly2 = Jelly(color='Blue', health=10)
    combat = Combat([tower1, tower2], [jelly1, jelly2])
    log1 = combat.fight_round()  # Attack jelly1, it will be dead after this
    assert len(log1) == 2  # Two attacks in the round
    log2 = combat.fight_round()  # No living jellies left
    assert len(log2) == 1  # One attack should be registered, attacking jelly2

# Test a round where no jellies exist from the start
def test_round_when_no_jellies_exist():
    tower = Tower(color='Blue', level=1)
    combat = Combat([tower], [])
    log = combat.fight_round()
    assert len(log) == 0  # No attacks should be registered

# Test successive rounds produce empty logs after all jellies are gone
def test_successive_rounds_empty_logs_after_all_jellies_defeated():
    tower1 = Tower(color='Blue', level=1)
    jelly1 = Jelly(color='Red', health=1)
    combat = Combat([tower1], [jelly1])
    combat.fight_round()  # First round should attack jelly1
    assert jelly1.health <= 0  # Jelly1 should be dead
    log2 = combat.fight_round()  # Second round should be empty since no jellies remain
    assert len(log2) == 0  # No attacks should be registered

# Test zero damage does not affect jelly health
def test_zero_damage_does_not_affect_health():
    tower = Tower(color='Red', level=1)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)
    assert damage == 0  # Fixed damage for Red level 1 vs Blue
    assert jelly.health == 10  # Jelly health remains unchanged