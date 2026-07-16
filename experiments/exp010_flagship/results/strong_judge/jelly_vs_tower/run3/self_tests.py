import pytest
from solution import Tower, Jelly, combat_round

# Test tower damage lookup based on color and level
def test_pure_color_tower_attacking_same_color_jelly_level_1():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Roll between 2 and 5
    assert 2 <= damage <= 5  # AC-1.1

def test_pure_color_tower_attacking_same_color_jelly_level_2():
    tower = Tower(color='Red', level=2)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # Roll between 5 and 9
    assert 5 <= damage <= 9  # AC-1.1

def test_pure_color_tower_attacking_same_color_jelly_level_3():
    tower = Tower(color='Blue', level=3)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Roll between 9 and 12
    assert 9 <= damage <= 12  # AC-1.1

def test_pure_color_tower_attacking_same_color_jelly_level_4():
    tower = Tower(color='Red', level=4)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # Roll between 12 and 15
    assert 12 <= damage <= 15  # AC-1.1

def test_pure_color_tower_attacking_opposite_color_jelly_level_1():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # Fixed damage of 0
    assert damage == 0  # AC-1.2

def test_pure_color_tower_attacking_opposite_color_jelly_level_2():
    tower = Tower(color='Red', level=2)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Fixed damage of 1
    assert damage == 1  # AC-1.2

def test_pure_color_tower_attacking_opposite_color_jelly_level_3():
    tower = Tower(color='Blue', level=3)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # Fixed damage of 2
    assert damage == 2  # AC-1.2

def test_pure_color_tower_attacking_opposite_color_jelly_level_4():
    tower = Tower(color='Red', level=4)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Fixed damage of 3
    assert damage == 3  # AC-1.2

def test_dual_color_tower_attacking_same_color_jelly_level_1():
    tower = Tower(color='BlueRed', level=1)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Fixed damage of 2
    assert damage == 2  # AC-1.3

def test_dual_color_tower_attacking_same_color_jelly_level_2():
    tower = Tower(color='BlueRed', level=2)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # Roll between 2 and 4
    assert 2 <= damage <= 4  # AC-1.3

def test_dual_color_tower_attacking_same_color_jelly_level_3():
    tower = Tower(color='BlueRed', level=3)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Roll between 4 and 6
    assert 4 <= damage <= 6  # AC-1.3

def test_dual_color_tower_attacking_same_color_jelly_level_4():
    tower = Tower(color='BlueRed', level=4)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # Roll between 6 and 8
    assert 6 <= damage <= 8  # AC-1.3

def test_dual_color_tower_attacking_dual_color_jelly_level_3():
    tower = Tower(color='BlueRed', level=3)
    jelly = Jelly(color='BlueRed', health=10)
    damage = tower.attack(jelly)  # Roll between 4 and 6
    assert 4 <= damage <= 6  # AC-1.4

def test_dual_color_tower_attacking_dual_color_jelly_level_4():
    tower = Tower(color='BlueRed', level=4)
    jelly = Jelly(color='BlueRed', health=10)
    damage = tower.attack(jelly)  # Roll between 6 and 8
    assert 6 <= damage <= 8  # AC-1.4

def test_pure_color_tower_attacking_dual_color_jelly_level_1():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='BlueRed', health=10)
    damage = tower.attack(jelly)  # Roll between 2 and 5
    assert 2 <= damage <= 5  # AC-1.4

def test_pure_color_tower_attacking_dual_color_jelly_level_2():
    tower = Tower(color='Red', level=2)
    jelly = Jelly(color='BlueRed', health=10)
    damage = tower.attack(jelly)  # Roll between 5 and 9
    assert 5 <= damage <= 9  # AC-1.4

def test_invalid_tower_level_tower_creation():
    with pytest.raises(ValueError, match="tower level must be between 1 and 4, got 0"):
        Tower(color='Blue', level=0)

def test_invalid_tower_level_attack():
    with pytest.raises(ValueError, match="tower level must be between 1 and 4, got 5"):
        Tower(color='Blue', level=5)  # Construction should fail

# Test jelly health and death
def test_jelly_health_positive():
    jelly = Jelly(color='Blue', health=5)
    assert jelly.is_alive() == True  # AC-2.1

def test_jelly_health_zero():
    jelly = Jelly(color='Blue', health=0)
    assert jelly.is_alive() == False  # AC-2.1

def test_jelly_taking_damage():
    jelly = Jelly(color='Blue', health=10)
    jelly.take_damage(3)
    assert jelly.health == 7  # AC-2.2

def test_jelly_taking_damage_zero_health():
    jelly = Jelly(color='Blue', health=3)
    jelly.take_damage(3)
    assert jelly.health == 0  # AC-2.2

def test_jelly_taking_damage_overkill():
    jelly = Jelly(color='Blue', health=3)
    jelly.take_damage(5)
    assert jelly.health == -2  # AC-2.2

def test_jelly_killed_by_attack():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Blue', health=3)
    damage = tower.attack(jelly)  # Roll between 2 and 5
    jelly.take_damage(damage)  # Apply damage
    assert not jelly.is_alive()  # Jelly should be dead after attack

# Test combat rounds
def test_combat_round_towers_attack_first_living_jelly():
    tower1 = Tower(color='Blue', level=1)
    tower2 = Tower(color='Red', level=1)
    jelly1 = Jelly(color='Blue', health=10)
    jelly2 = Jelly(color='Red', health=10)
    log = combat_round([tower1, tower2], [jelly1, jelly2])
    assert len(log) == 2  # AC-4.1, AC-4.2
    assert log[0]['tower'] == tower1  # verify tower order
    assert log[0]['jelly'] == jelly1  # verify target identity
    assert log[1]['tower'] == tower2  # verify tower order
    assert log[1]['jelly'] == jelly1  # verify target identity

def test_combat_round_jelly_killed():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Blue', health=3)
    log = combat_round([tower], [jelly])
    assert jelly.health <= 0  # Jelly should be dead or below zero health
    assert len(log) == 1  # must have one log entry

def test_combat_round_jelly_killed_check_log():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Blue', health=3)
    log = combat_round([tower], [jelly])
    assert log[0]['tower'] == tower
    assert log[0]['jelly'] == jelly

def test_combat_round_no_living_jellies():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Red', health=0)
    log = combat_round([tower], [jelly])
    assert len(log) == 0  # AC-4.4

def test_combat_round_no_more_jellies():
    tower = Tower(color='Blue', level=1)
    jelly1 = Jelly(color='Red', health=0)
    jelly2 = Jelly(color='Red', health=0)
    log = combat_round([tower], [jelly1, jelly2])
    assert len(log) == 0  # AC-4.5

def test_combat_round_jelly_killed_by_first_tower():
    tower1 = Tower(color='Blue', level=1)
    tower2 = Tower(color='Red', level=1)
    jelly1 = Jelly(color='Blue', health=3)
    jelly2 = Jelly(color='Red', health=10)
    log = combat_round([tower1, tower2], [jelly1, jelly2])
    assert len(log) == 2  # Two attacks logged
    assert jelly1.health <= 0  # First jelly must be dead
    assert jelly2.health == 10  # Second jelly must be alive

def test_combat_round_final_jelly_dies():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Blue', health=3)
    log = combat_round([tower], [jelly])
    assert len(log) == 1  # only one attack logged
    assert jelly.health <= 0  # must be dead after attack

def test_combat_round_multiple_rounds():
    tower = Tower(color='Blue', level=1)
    jelly1 = Jelly(color='Blue', health=5)
    jelly2 = Jelly(color='Red', health=5)
    log1 = combat_round([tower], [jelly1, jelly2])
    assert len(log1) == 1  # One attack logged
    jelly1_health_after_first = jelly1.health
    log2 = combat_round([tower], [jelly1, jelly2])
    assert len(log2) == 1  # One attack logged again
    assert jelly1.health < jelly1_health_after_first  # Jelly1 health should have decreased
    assert jelly2.health == 5  # jelly2 should remain alive
    log3 = combat_round([tower], [jelly1])
    assert len(log3) == 1  # One attack logged again
    assert jelly1.health < 0  # Jelly1 should be dead after the 3rd round
    assert len(combat_round([tower], [])) == 0  # No log when no jellies left

def test_combat_round_skips_dead_jelly():
    tower1 = Tower(color='Blue', level=1)
    tower2 = Tower(color='Red', level=1)
    jelly1 = Jelly(color='Blue', health=0)  # Initially dead
    jelly2 = Jelly(color='Red', health=10)
    log = combat_round([tower1, tower2], [jelly1, jelly2])
    assert len(log) == 1  # Only one attack logged
    assert log[0]['jelly'] == jelly2  # Verify that the living jelly was targeted

def test_combat_round_no_targets_left_mid_round():
    tower1 = Tower(color='Blue', level=1)
    tower2 = Tower(color='Red', level=1)
    jelly1 = Jelly(color='Blue', health=3)
    jelly2 = Jelly(color='Red', health=3)
    log = combat_round([tower1, tower2], [jelly1, jelly2])
    assert len(log) == 2  # Two attacks logged
    jelly1.take_damage(3)  # Jelly1 dies
    log2 = combat_round([tower2], [jelly1, jelly2])
    assert len(log2) == 1  # Tower2 should only attack jelly2
    assert log2[0]['jelly'] == jelly2  # Verify the only target was jelly2

def test_combat_round_depletion_and_empty_log():
    tower = Tower(color='Blue', level=1)
    jelly1 = Jelly(color='Blue', health=2)
    jelly2 = Jelly(color='Red', health=2)
    combat_round([tower], [jelly1, jelly2])  # First round, both jellies take damage
    combat_round([tower], [jelly1, jelly2])  # Second round, jellies take damage
    combat_round([tower], [jelly1, jelly2])  # Third round, jellies take damage
    combat_round([tower], [jelly1, jelly2])  # Fourth round, both jellies should be dead
    log = combat_round([tower], [jelly1, jelly2])  # No living jellies left
    assert len(log) == 0  # Expecting an empty log after depletion