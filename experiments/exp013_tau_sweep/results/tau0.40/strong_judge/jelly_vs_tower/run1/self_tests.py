import pytest
from solution import Tower, Jelly, combat_round

def test_tower_damage_own_color_level_1():
    tower = Tower(color="Blue", level=1)
    jelly = Jelly(color="Blue", health=10)
    damage = tower.attack(jelly)  # level 1: 2 to 5
    assert 2 <= damage <= 5
    assert jelly.health == 10 - damage

def test_tower_damage_own_color_level_2():
    tower = Tower(color="Red", level=2)
    jelly = Jelly(color="Red", health=10)
    damage = tower.attack(jelly)  # level 2: 5 to 9
    assert 5 <= damage <= 9
    assert jelly.health == 10 - damage

def test_tower_damage_own_color_level_3():
    tower = Tower(color="Blue", level=3)
    jelly = Jelly(color="Blue", health=10)
    damage = tower.attack(jelly)  # level 3: 9 to 12
    assert 9 <= damage <= 12
    assert jelly.health == 10 - damage

def test_tower_damage_own_color_level_4():
    tower = Tower(color="Red", level=4)
    jelly = Jelly(color="Red", health=10)
    damage = tower.attack(jelly)  # level 4: 12 to 15
    assert 12 <= damage <= 15
    assert jelly.health == 10 - damage

def test_tower_damage_opposite_color_level_1():
    tower = Tower(color="Blue", level=1)
    jelly = Jelly(color="Red", health=10)
    damage = tower.attack(jelly)  # level 1: 0
    assert damage == 0
    assert jelly.health == 10

def test_tower_damage_opposite_color_level_2():
    tower = Tower(color="Red", level=2)
    jelly = Jelly(color="Blue", health=10)
    damage = tower.attack(jelly)  # level 2: 1
    assert damage == 1
    assert jelly.health == 10 - 1

def test_tower_damage_opposite_color_level_3():
    tower = Tower(color="Blue", level=3)
    jelly = Jelly(color="Red", health=10)
    damage = tower.attack(jelly)  # level 3: 2
    assert damage == 2
    assert jelly.health == 10 - 2

def test_tower_damage_opposite_color_level_4():
    tower = Tower(color="Red", level=4)
    jelly = Jelly(color="Blue", health=10)
    damage = tower.attack(jelly)  # level 4: 3
    assert damage == 3
    assert jelly.health == 10 - 3

def test_dual_color_tower_damage_blue_jelly_level_1():
    tower = Tower(color="BlueRed", level=1)
    jelly = Jelly(color="Blue", health=10)
    damage = tower.attack(jelly)  # level 1: exactly 2
    assert damage == 2
    assert jelly.health == 10 - 2

def test_dual_color_tower_damage_blue_jelly_level_2():
    tower = Tower(color="BlueRed", level=2)
    jelly = Jelly(color="Blue", health=10)
    damage = tower.attack(jelly)  # level 2: 2 to 4
    assert 2 <= damage <= 4
    assert jelly.health == 10 - damage

def test_dual_color_tower_damage_red_jelly_level_3():
    tower = Tower(color="BlueRed", level=3)
    jelly = Jelly(color="Red", health=10)
    damage = tower.attack(jelly)  # level 3: 4 to 6
    assert 4 <= damage <= 6
    assert jelly.health == 10 - damage

def test_dual_color_tower_damage_red_jelly_level_4():
    tower = Tower(color="BlueRed", level=4)
    jelly = Jelly(color="Red", health=10)
    damage = tower.attack(jelly)  # level 4: 6 to 8
    assert 6 <= damage <= 8
    assert jelly.health == 10 - damage

def test_dual_color_tower_against_dual_color_jelly():
    tower = Tower(color="BlueRed", level=3)
    jelly = Jelly(color="BlueRed", health=10)
    damage = tower.attack(jelly)  # level 3: max(4, 4) = 4 to 6
    assert 4 <= damage <= 6
    assert jelly.health == 10 - damage

def test_tower_damage_against_blue_red_jelly():
    tower = Tower(color="Blue", level=2)
    jelly = Jelly(color="BlueRed", health=10)
    damage = tower.attack(jelly)  # level 2: 5 to 9
    assert 5 <= damage <= 9
    assert jelly.health == 10 - damage

def test_tower_level_out_of_bounds_low():
    with pytest.raises(Exception, match="tower level must be between 1 and 4, got 0"):
        Tower(color="Blue", level=0)

def test_tower_level_out_of_bounds_high():
    with pytest.raises(Exception, match="tower level must be between 1 and 4, got 5"):
        Tower(color="Red", level=5)

def test_tower_level_out_of_bounds_consulting():
    tower = Tower(color="Blue", level=5)
    with pytest.raises(Exception, match="tower level must be between 1 and 4, got 5"):
        tower.attack(Jelly(color="Blue", health=10))

def test_jelly_health_alive():
    jelly = Jelly(color="Blue", health=10)
    assert jelly.is_alive() is True

def test_jelly_health_dead():
    jelly = Jelly(color="Blue", health=0)
    assert jelly.is_alive() is False

def test_jelly_take_damage():
    jelly = Jelly(color="Red", health=10)
    jelly.take_damage(3)
    assert jelly.health == 7

def test_jelly_take_damage_exceeding_health():
    jelly = Jelly(color="Blue", health=5)
    jelly.take_damage(5)
    assert jelly.health == 0
    assert jelly.is_alive() is False

def test_jelly_attack_after_dead():
    jelly = Jelly(color="Red", health=0)
    tower = Tower(color="Blue", level=1)
    with pytest.raises(Exception):
        tower.attack(jelly)

def test_combat_round_with_living_jellies():
    tower1 = Tower(color="Blue", level=2)
    tower2 = Tower(color="Red", level=1)
    jelly1 = Jelly(color="Blue", health=10)
    jelly2 = Jelly(color="Red", health=10)
    log = combat_round([tower1, tower2], [jelly1, jelly2])

    assert len(log) == 2  # Two attacks, one per tower
    assert log[0]["tower"] == tower1  # First tower attacks first jelly
    assert log[0]["jelly"] == jelly1
    assert log[1]["tower"] == tower2  # Second tower attacks second jelly
    assert log[1]["jelly"] == jelly2
    assert log[0]["damage"] >= 5  # tower1 deals 5-9
    assert jelly1.health == 10 - log[0]["damage"]
    assert jelly2.health == 10

def test_combat_round_with_killed_jelly():
    tower1 = Tower(color="Blue", level=2)
    tower2 = Tower(color="Red", level=1)
    jelly1 = Jelly(color="Blue", health=3)
    jelly2 = Jelly(color="Red", health=10)
    log = combat_round([tower1, tower2], [jelly1, jelly2])

    assert len(log) == 2  # Two attacks, one per tower
    assert jelly1.is_alive() is False  # First jelly should be dead
    assert log[0]["jelly"] == jelly1
    assert log[1]["jelly"] == jelly2  # Second jelly still alive

    log = combat_round([tower1, tower2], [jelly2])
    assert len(log) == 1  # One attack should be logged
    assert jelly2.is_alive() is False  # Now second jelly should be dead

def test_combat_round_exhausted_wave():
    tower1 = Tower(color="Blue", level=2)
    tower2 = Tower(color="Red", level=1)
    jelly1 = Jelly(color="Blue", health=5)
    jelly2 = Jelly(color="Red", health=3)
    log = combat_round([tower1, tower2], [jelly1, jelly2])

    assert len(log) == 2  # Two attacks, one per tower
    assert jelly1.is_alive() is False  # First jelly should be dead
    assert jelly2.is_alive() is True  # Second jelly should be alive

    log = combat_round([tower1, tower2], [jelly2])
    assert len(log) == 1  # One attack should be logged
    assert jelly2.is_alive() is False  # Now second jelly should be dead

    log = combat_round([tower1, tower2], [])
    assert len(log) == 0  # No attacks should be logged