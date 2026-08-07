import pytest
from solution import Tower, Jelly, combat_round

# User Stories and Acceptance Criteria

# US-1: Look up damage from the table
def test_tower_damage_same_color_level_1():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # 2 to 5
    assert 2 <= damage <= 5

def test_tower_damage_same_color_level_2():
    tower = Tower(color='Blue', level=2)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # 5 to 9
    assert 5 <= damage <= 9

def test_tower_damage_same_color_level_3():
    tower = Tower(color='Blue', level=3)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # 9 to 12
    assert 9 <= damage <= 12

def test_tower_damage_same_color_level_4():
    tower = Tower(color='Blue', level=4)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # 12 to 15
    assert 12 <= damage <= 15

def test_tower_damage_opposite_color_level_1():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # 0
    assert damage == 0

def test_tower_damage_opposite_color_level_2():
    tower = Tower(color='Blue', level=2)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # 1
    assert damage == 1

def test_tower_damage_opposite_color_level_3():
    tower = Tower(color='Blue', level=3)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # 2
    assert damage == 2

def test_tower_damage_opposite_color_level_4():
    tower = Tower(color='Blue', level=4)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # 3
    assert damage == 3

def test_red_tower_damage_same_color_level_1():
    tower = Tower(color='Red', level=1)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # 2 to 5
    assert 2 <= damage <= 5

def test_red_tower_damage_same_color_level_2():
    tower = Tower(color='Red', level=2)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # 5 to 9
    assert 5 <= damage <= 9

def test_red_tower_damage_same_color_level_3():
    tower = Tower(color='Red', level=3)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # 9 to 12
    assert 9 <= damage <= 12

def test_red_tower_damage_same_color_level_4():
    tower = Tower(color='Red', level=4)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # 12 to 15
    assert 12 <= damage <= 15

def test_blue_red_tower_damage_level_1():
    tower = Tower(color='BlueRed', level=1)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # 2
    assert damage == 2

def test_blue_red_tower_damage_level_2():
    tower = Tower(color='BlueRed', level=2)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # 2 to 4
    assert 2 <= damage <= 4

def test_blue_red_tower_damage_level_3():
    tower = Tower(color='BlueRed', level=3)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # 4 to 6
    assert 4 <= damage <= 6

def test_blue_red_tower_damage_level_4():
    tower = Tower(color='BlueRed', level=4)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # 6 to 8
    assert 6 <= damage <= 8

def test_dual_color_jelly_damage():
    tower = Tower(color='Blue', level=2)
    jelly = Jelly(color='BlueRed', health=10)
    damage = tower.attack(jelly)  # 5 to 9 (Blue-target)
    assert 5 <= damage <= 9

def test_blue_red_tower_against_blue_jelly():
    tower = Tower(color='BlueRed', level=2)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # 2 to 4 (Blue-target)
    assert 2 <= damage <= 4

def test_tower_level_validation():
    with pytest.raises(Exception, match="tower level must be between 1 and 4, got 0"):
        Tower(color='Blue', level=0)

    with pytest.raises(Exception, match="tower level must be between 1 and 4, got 5"):
        Tower(color='Blue', level=5)

def test_tower_damage_table_validation():
    tower = Tower(color='Blue', level=1)
    with pytest.raises(Exception, match="tower level must be between 1 and 4, got 0"):
        tower.attack(Jelly(color='Red', health=10))

    with pytest.raises(Exception, match="tower level must be between 1 and 4, got 5"):
        tower.attack(Jelly(color='Red', health=10))

# US-2: Track jelly health and death
def test_jelly_health_alive():
    jelly = Jelly(color='Blue', health=10)
    assert jelly.is_alive() is True

def test_jelly_health_dead():
    jelly = Jelly(color='Blue', health=0)
    assert jelly.is_alive() is False

def test_jelly_take_damage():
    jelly = Jelly(color='Blue', health=10)
    jelly.take_damage(3)
    assert jelly.health == 7

def test_jelly_cannot_be_attacked_when_dead():
    jelly = Jelly(color='Blue', health=0)
    tower = Tower(color='Blue', level=1)
    with pytest.raises(Exception):
        tower.attack(jelly)

# US-3: Roll attacks reproducibly
def test_attack_reports_damage():
    tower = Tower(color='Blue', level=2)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # 1
    assert damage == 1
    assert jelly.health == 9

def test_damage_within_table_range():
    tower = Tower(color='Blue', level=2)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # 5 to 9
    assert 5 <= damage <= 9
    assert jelly.health == (10 - damage)

def test_randomness_reproducibility():
    import random
    from solution import RandomSource
    
    source1 = RandomSource(seed=42)
    source2 = RandomSource(seed=42)
    
    tower1 = Tower(color='Blue', level=2, random_source=source1)
    jelly1 = Jelly(color='Red', health=10)
    damage1 = tower1.attack(jelly1)

    tower2 = Tower(color='Blue', level=2, random_source=source2)
    jelly2 = Jelly(color='Red', health=10)
    damage2 = tower2.attack(jelly2)

    assert damage1 == damage2  # same damage rolled

def test_zero_damage_attack():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # 0
    assert damage == 0
    assert jelly.health == 10  # jelly health unchanged

# US-4: Fight rounds with a combat log
def test_round_with_log():
    tower1 = Tower(color='Blue', level=2)
    tower2 = Tower(color='Red', level=1)
    jelly = Jelly(color='Blue', health=10)

    log = combat_round([tower1, tower2], [jelly])
    assert len(log) == 2
    assert log[0]['tower'] == tower1
    assert log[0]['jelly'] == jelly
    assert log[1]['tower'] == tower2
    assert log[1]['jelly'] == jelly

def test_round_skips_dead_jelly():
    tower1 = Tower(color='Blue', level=2)
    tower2 = Tower(color='Red', level=1)
    jelly1 = Jelly(color='Blue', health=10)
    jelly2 = Jelly(color='Blue', health=0)  # dead jelly

    log = combat_round([tower1, tower2], [jelly1, jelly2])
    assert len(log) == 2  # both towers attack
    assert log[0]['jelly'] == jelly1  # jelly1 attacked
    assert log[1]['jelly'] == jelly1  # jelly1 attacked again

def test_round_idle_when_no_living_jellies():
    tower1 = Tower(color='Blue', level=2)
    tower2 = Tower(color='Red', level=1)
    jelly = Jelly(color='Red', health=0)  # dead jelly

    log = combat_round([tower1, tower2], [jelly])
    assert len(log) == 0  # no attacks logged

def test_fight_rounds_until_all_jellies_dead():
    tower = Tower(color='Blue', level=2)
    jelly1 = Jelly(color='Red', health=1)  # will die
    jelly2 = Jelly(color='Red', health=3)  # will be hit

    log1 = combat_round([tower], [jelly1, jelly2])
    assert len(log1) == 1  # jelly1 should be hit and die
    assert jelly1.health == 0  # jelly1 should be dead
    assert jelly2.health == 3  # jelly2 health unchanged

    log2 = combat_round([tower], [jelly1, jelly2])
    assert len(log2) == 1  # now jelly2 should be hit
    assert jelly2.health == 2  # jelly2 should have taken damage

def test_round_kills_first_jelly():
    tower1 = Tower(color='Blue', level=2)
    tower2 = Tower(color='Red', level=1)
    jelly1 = Jelly(color='Blue', health=1)  # will die
    jelly2 = Jelly(color='Blue', health=3)  # will be hit

    log = combat_round([tower1, tower2], [jelly1, jelly2])
    assert len(log) == 2  # both towers attack
    assert jelly1.health == 0  # jelly1 should be dead
    assert jelly2.health == 3  # jelly2 health unchanged

def test_round_no_jellies_after_first():
    tower = Tower(color='Blue', level=2)
    jelly1 = Jelly(color='Red', health=1)  # will die
    jelly2 = Jelly(color='Red', health=3)  # will be hit

    log1 = combat_round([tower], [jelly1, jelly2])
    assert len(log1) == 1  # jelly1 should be hit and die

    log2 = combat_round([tower], [jelly2])  # no jelly1
    assert len(log2) == 1  # now jelly2 should be hit
    assert jelly2.health == 2  # jelly2 should have taken damage

    log3 = combat_round([tower], [])  # no jellies
    assert len(log3) == 0  # no logs should be produced