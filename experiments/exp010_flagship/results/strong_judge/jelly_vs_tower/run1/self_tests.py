# test_solution.py

import pytest
from solution import Tower, Jelly, combat_round

def test_tower_damage_lookup_same_color_level_1():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # range: 2 to 5
    assert 2 <= damage <= 5

def test_tower_damage_lookup_same_color_level_2():
    tower = Tower(color='Red', level=2)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # range: 5 to 9
    assert 5 <= damage <= 9

def test_tower_damage_lookup_same_color_level_3():
    tower = Tower(color='Blue', level=3)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # range: 9 to 12
    assert 9 <= damage <= 12

def test_tower_damage_lookup_same_color_level_4():
    tower = Tower(color='Red', level=4)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # range: 12 to 15
    assert 12 <= damage <= 15

def test_tower_damage_lookup_opposite_color_level_1():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # fixed: 0
    assert damage == 0

def test_tower_damage_lookup_opposite_color_level_2():
    tower = Tower(color='Blue', level=2)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # fixed: 1
    assert damage == 1

def test_tower_damage_lookup_opposite_color_level_3():
    tower = Tower(color='Red', level=3)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # fixed: 2
    assert damage == 2

def test_tower_damage_lookup_opposite_color_level_4():
    tower = Tower(color='Red', level=4)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # fixed: 3
    assert damage == 3

def test_dual_color_tower_damage_blue_jelly_level_1():
    tower = Tower(color='BlueRed', level=1)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # fixed: 2
    assert damage == 2

def test_dual_color_tower_damage_blue_jelly_level_2():
    tower = Tower(color='BlueRed', level=2)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # range: 2 to 4
    assert 2 <= damage <= 4

def test_dual_color_tower_damage_blue_jelly_level_3():
    tower = Tower(color='BlueRed', level=3)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # range: 4 to 6
    assert 4 <= damage <= 6

def test_dual_color_tower_damage_blue_jelly_level_4():
    tower = Tower(color='BlueRed', level=4)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # range: 6 to 8
    assert 6 <= damage <= 8

def test_dual_color_tower_damage_red_jelly_level_1():
    tower = Tower(color='BlueRed', level=1)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # fixed: 2
    assert damage == 2

def test_dual_color_tower_damage_red_jelly_level_2():
    tower = Tower(color='BlueRed', level=2)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # range: 2 to 4
    assert 2 <= damage <= 4

def test_dual_color_tower_damage_red_jelly_level_3():
    tower = Tower(color='BlueRed', level=3)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # range: 4 to 6
    assert 4 <= damage <= 6

def test_dual_color_tower_damage_red_jelly_level_4():
    tower = Tower(color='BlueRed', level=4)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # range: 6 to 8
    assert 6 <= damage <= 8

def test_tower_level_validation_below():
    with pytest.raises(Exception, match="tower level must be between 1 and 4, got 0"):
        Tower(color='Blue', level=0)

def test_tower_level_validation_above():
    with pytest.raises(Exception, match="tower level must be between 1 and 4, got 5"):
        Tower(color='Blue', level=5)

def test_tower_level_validation_during_lookup():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # fixed damage for Blue vs Red level 1
    assert damage == 0  # should not raise an error

def test_jelly_alive_status():
    jelly = Jelly(color='Blue', health=10)
    assert jelly.is_alive() == True
    jelly.take_damage(10)
    assert jelly.is_alive() == False

def test_jelly_health_reduction():
    jelly = Jelly(color='Blue', health=10)
    jelly.take_damage(3)
    assert jelly.health == 7

def test_jelly_dead_cannot_be_attacked():
    jelly = Jelly(color='Blue', health=10)
    jelly.take_damage(10)  # jelly is dead
    with pytest.raises(Exception, match="Cannot attack a dead jelly"):
        jelly.take_damage(5)  # Attempting to attack a dead jelly

def test_combat_round_with_single_tower_and_jelly():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Red', health=10)
    log = combat_round([tower], [jelly])
    assert len(log) == 1  # one attack
    assert log[0]['tower'] == tower
    assert log[0]['jelly'] == jelly
    assert log[0]['damage'] == 0  # fixed damage for Blue vs Red level 1

def test_combat_round_with_multiple_jellies():
    tower1 = Tower(color='Blue', level=1)
    tower2 = Tower(color='Red', level=1)
    jelly1 = Jelly(color='Red', health=5)
    jelly2 = Jelly(color='Red', health=5)
    log = combat_round([tower1, tower2], [jelly1, jelly2])
    assert len(log) == 2  # both towers attack
    assert log[0]['damage'] == 0  # Blue vs Red level 1
    assert 2 <= log[1]['damage'] <= 5  # Red vs Red level 1

def test_combat_round_no_jellies():
    tower = Tower(color='Blue', level=1)
    log = combat_round([tower], [])
    assert len(log) == 0  # no jellies, no attacks

def test_combat_round_jelly_death():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Red', health=1)
    log = combat_round([tower], [jelly])
    assert len(log) == 1  # one attack
    assert jelly.health == 1  # health should remain 1 since damage is 0
    assert jelly.is_alive() == True  # jelly should remain alive

def test_combat_round_no_more_jellies_after_first_attack():
    tower = Tower(color='Blue', level=1)
    jelly1 = Jelly(color='Red', health=10)
    jelly2 = Jelly(color='Red', health=5)
    log = combat_round([tower], [jelly1, jelly2])
    assert len(log) == 1  # only the first jelly should be attacked
    assert jelly1.health == 10  # jelly1 should remain untouched
    assert jelly2.health == 5  # jelly2 should remain untouched

def test_combat_round_remaining_towers_idle():
    tower1 = Tower(color='Blue', level=1)
    tower2 = Tower(color='Red', level=1)
    jelly1 = Jelly(color='Red', health=10)
    jelly1.take_damage(10)  # jelly is dead
    log = combat_round([tower1, tower2], [jelly1])
    assert len(log) == 0  # no attacks since jelly is dead

def test_combat_round_successive_rounds():
    tower = Tower(color='Blue', level=1)
    jelly1 = Jelly(color='Red', health=1)
    jelly2 = Jelly(color='Red', health=10)
    
    log1 = combat_round([tower], [jelly1])
    assert len(log1) == 1  # first round, jelly1 should be attacked
    assert jelly1.is_alive() == False  # jelly1 should be dead after attack

    log2 = combat_round([tower], [jelly2])
    assert len(log2) == 1  # second round, jelly2 should be attacked
    assert jelly2.health < 10  # jelly2 should have taken damage