from solution import Tower, Jelly, Combat
import pytest

def test_tower_damage_against_own_color_level_1():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Level 1 Blue against Blue
    assert 2 <= damage <= 5  # AC-1.1

def test_tower_damage_against_own_color_level_2():
    tower = Tower(color='Blue', level=2)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Level 2 Blue against Blue
    assert 5 <= damage <= 9  # AC-1.1

def test_tower_damage_against_own_color_level_3():
    tower = Tower(color='Blue', level=3)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Level 3 Blue against Blue
    assert 9 <= damage <= 12  # AC-1.1

def test_tower_damage_against_own_color_level_4():
    tower = Tower(color='Blue', level=4)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Level 4 Blue against Blue
    assert 12 <= damage <= 15  # AC-1.1

def test_tower_damage_against_opposite_color_level_1():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # Level 1 Blue against Red
    assert damage == 0  # AC-1.2

def test_tower_damage_against_opposite_color_level_2():
    tower = Tower(color='Blue', level=2)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # Level 2 Blue against Red
    assert damage == 1  # AC-1.2

def test_tower_damage_against_opposite_color_level_3():
    tower = Tower(color='Blue', level=3)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # Level 3 Blue against Red
    assert damage == 2  # AC-1.2

def test_tower_damage_against_opposite_color_level_4():
    tower = Tower(color='Blue', level=4)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # Level 4 Blue against Red
    assert damage == 3  # AC-1.2

def test_dual_color_tower_damage_level_1():
    tower = Tower(color='BlueRed', level=1)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Level 1 BlueRed against Blue
    assert damage == 2  # AC-1.3

def test_dual_color_tower_damage_level_2():
    tower = Tower(color='BlueRed', level=2)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Level 2 BlueRed against Blue
    assert 2 <= damage <= 4  # AC-1.3

def test_dual_color_tower_damage_level_3():
    tower = Tower(color='BlueRed', level=3)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Level 3 BlueRed against Blue
    assert 4 <= damage <= 6  # AC-1.3

def test_dual_color_tower_damage_level_4():
    tower = Tower(color='BlueRed', level=4)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Level 4 BlueRed against Blue
    assert 6 <= damage <= 8  # AC-1.3

def test_dual_color_tower_against_dual_color_jelly():
    tower = Tower(color='BlueRed', level=1)
    jelly = Jelly(color='BlueRed', health=10)
    damage = tower.attack(jelly)  # Level 1 BlueRed against BlueRed
    assert damage == 2  # AC-1.4

def test_tower_level_validation():
    with pytest.raises(ValueError, match="tower level must be between 1 and 4, got 0"):
        Tower(color='Blue', level=0)
    with pytest.raises(ValueError, match="tower level must be between 1 and 4, got 5"):
        Tower(color='Blue', level=5)

def test_jelly_health_positive():
    jelly = Jelly(color='Blue', health=10)
    assert jelly.is_alive()  # AC-2.1

def test_jelly_health_dead():
    jelly = Jelly(color='Blue', health=0)
    assert not jelly.is_alive()  # AC-2.1

def test_jelly_takes_damage():
    jelly = Jelly(color='Blue', health=10)
    jelly.take_damage(3)
    assert jelly.health == 7  # AC-2.2

def test_jelly_cannot_take_damage_when_dead():
    jelly = Jelly(color='Blue', health=0)
    with pytest.raises(ValueError, match="Cannot attack a dead jelly"):
        jelly.take_damage(3)  # AC-2.3

def test_rounds_log():
    tower1 = Tower(color='Blue', level=1)
    tower2 = Tower(color='Red', level=1)
    jelly = Jelly(color='Blue', health=10)
    combat = Combat(towers=[tower1, tower2], jellies=[jelly])
    log = combat.fight_round()
    assert len(log) == 2  # AC-4.1 and AC-4.2
    assert log[0]['tower'] == tower1
    assert log[0]['jelly'] == jelly
    assert log[1]['tower'] == tower2
    assert log[1]['jelly'] == jelly

def test_round_ends_when_jelly_dies():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Blue', health=5)
    combat = Combat(towers=[tower], jellies=[jelly])
    combat.fight_round()  # First attack should kill the jelly
    assert jelly.health == 0  # Jelly should be dead
    log = combat.fight_round()  # Next round should have no attacks
    assert len(log) == 0  # AC-4.3 and AC-4.4

def test_empty_round_log_when_no_jellies():
    tower = Tower(color='Blue', level=1)
    combat = Combat(towers=[tower], jellies=[])
    log = combat.fight_round()  # No jellies to attack
    assert len(log) == 0  # AC-4.4

def test_rounds_can_continue_until_no_jellies():
    tower = Tower(color='Blue', level=1)
    jelly1 = Jelly(color='Blue', health=5)
    jelly2 = Jelly(color='Blue', health=5)
    combat = Combat(towers=[tower], jellies=[jelly1, jelly2])
    combat.fight_round()  # First round should kill the first jelly
    assert jelly1.health == 0
    log2 = combat.fight_round()  # Second round should kill the second jelly
    assert jelly2.health == 0
    log3 = combat.fight_round()  # No jellies left
    assert len(log3) == 0  # Further rounds yield an empty log