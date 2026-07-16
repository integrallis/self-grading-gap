# test_solution.py

import pytest
from solution import Tower, Jelly, combat_round

def test_tower_damage_lookup_same_color_level_1():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Blue', health=10)
    # Damage range for Blue tower level 1 against Blue jelly is 2 to 5
    damage = tower.attack(jelly)
    assert 2 <= damage <= 5

def test_tower_damage_lookup_same_color_level_2():
    tower = Tower(color='Blue', level=2)
    jelly = Jelly(color='Blue', health=10)
    # Damage range for Blue tower level 2 against Blue jelly is 5 to 9
    damage = tower.attack(jelly)
    assert 5 <= damage <= 9

def test_tower_damage_lookup_opposite_color_level_1():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Red', health=10)
    # Fixed damage for Blue tower level 1 against Red jelly is 0
    damage = tower.attack(jelly)
    assert damage == 0
    assert jelly.health == 10  # Health should remain unchanged

def test_tower_damage_lookup_opposite_color_level_2():
    tower = Tower(color='Blue', level=2)
    jelly = Jelly(color='Red', health=10)
    # Fixed damage for Blue tower level 2 against Red jelly is 1
    damage = tower.attack(jelly)
    assert damage == 1
    assert jelly.health == 9  # Health should decrease by 1

def test_tower_damage_lookup_dual_color_level_1():
    tower = Tower(color='BlueRed', level=1)
    jelly = Jelly(color='Blue', health=10)
    # Fixed damage for dual-color tower level 1 against Blue jelly is 2
    damage = tower.attack(jelly)
    assert damage == 2
    assert jelly.health == 8  # Health should decrease by 2

def test_tower_damage_lookup_dual_color_against_opposite():
    tower = Tower(color='BlueRed', level=2)
    jelly = Jelly(color='Red', health=10)
    # Damage range for dual-color tower level 2 against Red jelly is 2 to 4
    damage = tower.attack(jelly)
    assert 2 <= damage <= 4

def test_tower_damage_lookup_dual_color_against_dual():
    tower = Tower(color='BlueRed', level=3)
    jelly = Jelly(color='BlueRed', health=10)
    # Damage range for dual-color tower level 3 against dual-color jelly
    # is max of Blue-target (4 to 6) and Red-target (4 to 6), hence also 4 to 6
    damage = tower.attack(jelly)
    assert 4 <= damage <= 6

def test_tower_damage_lookup_invalid_level():
    with pytest.raises(ValueError, match="tower level must be between 1 and 4, got 0"):
        Tower(color='Blue', level=0)
    with pytest.raises(ValueError, match="tower level must be between 1 and 4, got 5"):
        Tower(color='Blue', level=5)

def test_jelly_health_alive():
    jelly = Jelly(color='Blue', health=10)
    assert jelly.is_alive() is True

def test_jelly_health_dead():
    jelly = Jelly(color='Blue', health=0)
    assert jelly.is_alive() is False

def test_jelly_take_damage():
    jelly = Jelly(color='Blue', health=10)
    jelly.take_damage(3)
    assert jelly.health == 7  # Health should decrease by 3

def test_jelly_take_damage_to_zero():
    jelly = Jelly(color='Blue', health=3)
    jelly.take_damage(3)
    assert jelly.health == 0  # Health should be zero after damage

def test_jelly_cannot_be_attacked_if_dead():
    jelly = Jelly(color='Blue', health=0)
    with pytest.raises(ValueError, match="Cannot attack a dead jelly"):
        jelly.take_damage(5)

def test_combat_round_log_single_tower_single_jelly():
    tower = Tower(color='Blue', level=2)
    jelly = Jelly(color='Red', health=10)
    log = combat_round([tower], [jelly])
    assert len(log) == 1
    assert log[0]['tower'] == tower
    assert log[0]['jelly'] == jelly
    assert jelly.health == 9  # Assuming the attack does 1 damage

def test_combat_round_log_multiple_towers_and_jellies():
    tower1 = Tower(color='Blue', level=2)
    tower2 = Tower(color='Red', level=1)
    jelly1 = Jelly(color='Red', health=10)
    jelly2 = Jelly(color='Blue', health=8)
    log = combat_round([tower1, tower2], [jelly1, jelly2])
    assert len(log) == 2  # Each tower attacks once
    assert log[0]['tower'] == tower1
    assert log[0]['jelly'] == jelly1
    assert jelly1.health == 9  # Assuming tower1 does 1 damage
    assert log[1]['tower'] == tower2
    assert log[1]['jelly'] == jelly2
    assert jelly2.health == 8  # Tower2 does 0 damage against Blue jelly

def test_combat_round_log_jelly_killed():
    tower = Tower(color='Blue', level=2)
    jelly = Jelly(color='Red', health=1)
    log = combat_round([tower], [jelly])
    assert len(log) == 1
    assert jelly.health == 0  # Jelly should be dead after attack

def test_combat_round_no_jellies():
    tower = Tower(color='Blue', level=2)
    log = combat_round([tower], [])
    assert len(log) == 0  # No jellies means no log entries