import pytest
from solution import Tower, Jelly, combat_round


def test_tower_damage_lookup_same_color_level_1():
    tower = Tower(color="Blue", level=1)
    jelly = Jelly(color="Blue", health=10)
    damage = tower.attack(jelly)  # 2 to 5 damage
    assert 2 <= damage <= 5


def test_tower_damage_lookup_same_color_level_2():
    tower = Tower(color="Blue", level=2)
    jelly = Jelly(color="Blue", health=10)
    damage = tower.attack(jelly)  # 5 to 9 damage
    assert 5 <= damage <= 9


def test_tower_damage_lookup_same_color_level_3():
    tower = Tower(color="Blue", level=3)
    jelly = Jelly(color="Blue", health=10)
    damage = tower.attack(jelly)  # 9 to 12 damage
    assert 9 <= damage <= 12


def test_tower_damage_lookup_same_color_level_4():
    tower = Tower(color="Blue", level=4)
    jelly = Jelly(color="Blue", health=10)
    damage = tower.attack(jelly)  # 12 to 15 damage
    assert 12 <= damage <= 15


def test_tower_damage_lookup_opposite_color_level_1():
    tower = Tower(color="Blue", level=1)
    jelly = Jelly(color="Red", health=10)
    damage = tower.attack(jelly)  # 0 damage
    assert damage == 0


def test_tower_damage_lookup_opposite_color_level_2():
    tower = Tower(color="Blue", level=2)
    jelly = Jelly(color="Red", health=10)
    damage = tower.attack(jelly)  # 1 damage
    assert damage == 1


def test_tower_damage_lookup_opposite_color_level_3():
    tower = Tower(color="Blue", level=3)
    jelly = Jelly(color="Red", health=10)
    damage = tower.attack(jelly)  # 2 damage
    assert damage == 2


def test_tower_damage_lookup_opposite_color_level_4():
    tower = Tower(color="Blue", level=4)
    jelly = Jelly(color="Red", health=10)
    damage = tower.attack(jelly)  # 3 damage
    assert damage == 3


def test_tower_damage_lookup_red_same_color_level_1():
    tower = Tower(color="Red", level=1)
    jelly = Jelly(color="Red", health=10)
    damage = tower.attack(jelly)  # 2 to 5 damage
    assert 2 <= damage <= 5


def test_tower_damage_lookup_red_same_color_level_2():
    tower = Tower(color="Red", level=2)
    jelly = Jelly(color="Red", health=10)
    damage = tower.attack(jelly)  # 5 to 9 damage
    assert 5 <= damage <= 9


def test_tower_damage_lookup_red_same_color_level_3():
    tower = Tower(color="Red", level=3)
    jelly = Jelly(color="Red", health=10)
    damage = tower.attack(jelly)  # 9 to 12 damage
    assert 9 <= damage <= 12


def test_tower_damage_lookup_red_same_color_level_4():
    tower = Tower(color="Red", level=4)
    jelly = Jelly(color="Red", health=10)
    damage = tower.attack(jelly)  # 12 to 15 damage
    assert 12 <= damage <= 15


def test_tower_damage_lookup_red_opposite_color_level_1():
    tower = Tower(color="Red", level=1)
    jelly = Jelly(color="Blue", health=10)
    damage = tower.attack(jelly)  # 0 damage
    assert damage == 0


def test_tower_damage_lookup_red_opposite_color_level_2():
    tower = Tower(color="Red", level=2)
    jelly = Jelly(color="Blue", health=10)
    damage = tower.attack(jelly)  # 1 damage
    assert damage == 1


def test_tower_damage_lookup_red_opposite_color_level_3():
    tower = Tower(color="Red", level=3)
    jelly = Jelly(color="Blue", health=10)
    damage = tower.attack(jelly)  # 2 damage
    assert damage == 2


def test_tower_damage_lookup_red_opposite_color_level_4():
    tower = Tower(color="Red", level=4)
    jelly = Jelly(color="Blue", health=10)
    damage = tower.attack(jelly)  # 3 damage
    assert damage == 3


def test_dual_color_tower_damage_level_1():
    tower = Tower(color="BlueRed", level=1)
    jelly = Jelly(color="Blue", health=10)
    damage = tower.attack(jelly)  # 2 damage
    assert damage == 2


def test_dual_color_tower_damage_level_2():
    tower = Tower(color="BlueRed", level=2)
    jelly = Jelly(color="Blue", health=10)
    damage = tower.attack(jelly)  # 2 to 4 damage
    assert 2 <= damage <= 4


def test_dual_color_tower_damage_level_3():
    tower = Tower(color="BlueRed", level=3)
    jelly = Jelly(color="Blue", health=10)
    damage = tower.attack(jelly)  # 4 to 6 damage
    assert 4 <= damage <= 6


def test_dual_color_tower_damage_level_4():
    tower = Tower(color="BlueRed", level=4)
    jelly = Jelly(color="Blue", health=10)
    damage = tower.attack(jelly)  # 6 to 8 damage
    assert 6 <= damage <= 8


def test_dual_color_tower_damage_against_red_jelly_level_1():
    tower = Tower(color="BlueRed", level=1)
    jelly = Jelly(color="Red", health=10)
    damage = tower.attack(jelly)  # 2 damage
    assert damage == 2


def test_dual_color_tower_damage_against_red_jelly_level_2():
    tower = Tower(color="BlueRed", level=2)
    jelly = Jelly(color="Red", health=10)
    damage = tower.attack(jelly)  # 2 to 4 damage
    assert 2 <= damage <= 4


def test_dual_color_tower_damage_against_red_jelly_level_3():
    tower = Tower(color="BlueRed", level=3)
    jelly = Jelly(color="Red", health=10)
    damage = tower.attack(jelly)  # 4 to 6 damage
    assert 4 <= damage <= 6


def test_dual_color_tower_damage_against_red_jelly_level_4():
    tower = Tower(color="BlueRed", level=4)
    jelly = Jelly(color="Red", health=10)
    damage = tower.attack(jelly)  # 6 to 8 damage
    assert 6 <= damage <= 8


def test_tower_level_validation():
    # Validate tower level inputs
    tower = Tower(color="Blue", level=0)  # Should not raise an error but is invalid
    assert tower.color == "Blue"
    
    tower = Tower(color="Red", level=5)  # Should not raise an error but is invalid
    assert tower.color == "Red"

    tower = Tower(color="Red", level=1)  # Valid tower
    assert tower.color == "Red"
    assert tower.level == 1


def test_jelly_health_alive():
    jelly = Jelly(color="Blue", health=10)
    assert jelly.is_alive() is True


def test_jelly_health_dead():
    jelly = Jelly(color="Blue", health=0)
    assert jelly.is_alive() is False


def test_jelly_health_below_zero():
    jelly = Jelly(color="Blue", health=-1)  # Should not raise an error but is invalid
    assert jelly.is_alive() is False


def test_jelly_takes_damage():
    jelly = Jelly(color="Blue", health=10)
    initial_health = jelly.health
    jelly.take_damage(3)  # takes 3 damage
    assert jelly.health == initial_health - 3


def test_jelly_cannot_be_attacked_if_dead():
    jelly = Jelly(color="Blue", health=0)  # Jelly starts dead
    tower = Tower(color="Blue", level=1)
    damage = tower.attack(jelly)  # Attempt to attack dead jelly
    assert damage == 0  # Should not deal damage


def test_combat_round_logging():
    tower1 = Tower(color="Blue", level=2)
    tower2 = Tower(color="Red", level=2)
    jelly = Jelly(color="Blue", health=10)
    log = combat_round([tower1, tower2], [jelly])
    assert len(log) == 2  # two towers attack
    # Validating the log format is not specified, so we simply check entries exist.


def test_combat_round_jelly_killed():
    tower = Tower(color="Blue", level=2)
    jelly = Jelly(color="Red", health=1)
    log = combat_round([tower], [jelly])
    assert jelly.is_alive() is False
    assert len(log) == 1  # tower attacked jelly and killed it


def test_combat_round_no_living_jellies():
    tower = Tower(color="Blue", level=2)
    jelly = Jelly(color="Red", health=0)
    log = combat_round([tower], [jelly])
    assert len(log) == 0  # no attacks logged, jelly is dead


def test_combat_round_jelly_killed_mid_round():
    tower1 = Tower(color="Blue", level=2)
    tower2 = Tower(color="Red", level=2)
    jelly1 = Jelly(color="Blue", health=1)
    jelly2 = Jelly(color="Red", health=10)
    log = combat_round([tower1, tower2], [jelly1, jelly2])
    assert jelly1.is_alive() is False
    assert jelly2.is_alive() is True
    assert len(log) == 2  # two attacks logged


def test_combat_round_empty_log_after_all_jellies_dead():
    tower1 = Tower(color="Blue", level=2)
    tower2 = Tower(color="Red", level=2)
    jellies = [Jelly(color="Blue", health=1), Jelly(color="Red", health=1)]
    combat_round([tower1, tower2], jellies)
    log = combat_round([tower1, tower2], [])
    assert len(log) == 0  # no jellies left


def test_successive_rounds_with_same_wave():
    tower1 = Tower(color="Blue", level=2)
    tower2 = Tower(color="Red", level=2)
    jellies = [Jelly(color="Blue", health=1), Jelly(color="Red", health=1)]
    combat_round([tower1, tower2], jellies)
    log = combat_round([tower1, tower2], jellies)
    assert len(log) == 0  # no jellies left