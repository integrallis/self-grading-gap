import pytest
from solution import Tower, Jelly, combat_round
import random

# Test tower levels and damage against jellies of various colors

def test_tower_level_validation():
    with pytest.raises(ValueError, match="tower level must be between 1 and 4, got 0"):
        Tower(color='Blue', level=0)
    with pytest.raises(ValueError, match="tower level must be between 1 and 4, got 5"):
        Tower(color='Red', level=5)
    with pytest.raises(ValueError, match="tower level must be between 1 and 4, got 5"):
        Tower(color='BlueRed', level=5)

def test_blue_tower_vs_blue_jelly_level_1():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)
    assert 2 <= damage <= 5  # AC-1.1

def test_blue_tower_vs_blue_jelly_level_2():
    tower = Tower(color='Blue', level=2)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)
    assert 5 <= damage <= 9  # AC-1.1

def test_blue_tower_vs_blue_jelly_level_3():
    tower = Tower(color='Blue', level=3)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)
    assert 9 <= damage <= 12  # AC-1.1

def test_blue_tower_vs_blue_jelly_level_4():
    tower = Tower(color='Blue', level=4)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)
    assert 12 <= damage <= 15  # AC-1.1

def test_red_tower_vs_red_jelly_level_1():
    tower = Tower(color='Red', level=1)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)
    assert 2 <= damage <= 5  # AC-1.1

def test_red_tower_vs_red_jelly_level_2():
    tower = Tower(color='Red', level=2)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)
    assert 5 <= damage <= 9  # AC-1.1

def test_red_tower_vs_red_jelly_level_3():
    tower = Tower(color='Red', level=3)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)
    assert damage == 2  # AC-1.2

def test_red_tower_vs_red_jelly_level_4():
    tower = Tower(color='Red', level=4)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)
    assert damage == 3  # AC-1.2

def test_blue_tower_vs_red_jelly_level_1():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)
    assert damage == 0  # AC-1.2

def test_blue_tower_vs_red_jelly_level_2():
    tower = Tower(color='Blue', level=2)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)
    assert damage == 1  # AC-1.2

def test_red_tower_vs_blue_jelly_level_1():
    tower = Tower(color='Red', level=1)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)
    assert damage == 0  # AC-1.2

def test_red_tower_vs_blue_jelly_level_2():
    tower = Tower(color='Red', level=2)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)
    assert damage == 1  # AC-1.2

def test_dual_color_tower_vs_blue_jelly_level_1():
    tower = Tower(color='BlueRed', level=1)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)
    assert damage == 2  # AC-1.3

def test_dual_color_tower_vs_red_jelly_level_1():
    tower = Tower(color='BlueRed', level=1)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)
    assert damage == 2  # AC-1.3

def test_dual_color_tower_vs_red_jelly_level_2():
    tower = Tower(color='BlueRed', level=2)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)
    assert 2 <= damage <= 4  # AC-1.3

def test_dual_color_tower_vs_blue_jelly_level_2():
    tower = Tower(color='BlueRed', level=2)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)
    assert 2 <= damage <= 4  # AC-1.3

def test_dual_color_tower_vs_blue_jelly_level_3():
    tower = Tower(color='BlueRed', level=3)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)
    assert 4 <= damage <= 6  # AC-1.3

def test_dual_color_tower_vs_red_jelly_level_3():
    tower = Tower(color='BlueRed', level=3)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)
    assert 4 <= damage <= 6  # AC-1.3

def test_dual_color_tower_vs_dual_color_jelly_level_3():
    tower = Tower(color='BlueRed', level=3)
    jelly = Jelly(color='BlueRed', health=10)
    damage = tower.attack(jelly)
    assert 4 <= damage <= 6  # AC-1.4

def test_dual_color_tower_vs_dual_color_jelly_level_4():
    tower = Tower(color='BlueRed', level=4)
    jelly = Jelly(color='BlueRed', health=10)
    damage = tower.attack(jelly)
    assert 6 <= damage <= 8  # AC-1.4

def test_blue_tower_vs_dual_color_jelly_level_4():
    tower = Tower(color='Blue', level=4)
    jelly = Jelly(color='BlueRed', health=10)
    damage = tower.attack(jelly)
    assert 12 <= damage <= 15  # AC-1.4

def test_red_tower_vs_dual_color_jelly_level_4():
    tower = Tower(color='Red', level=4)
    jelly = Jelly(color='BlueRed', health=10)
    damage = tower.attack(jelly)
    assert 12 <= damage <= 15  # AC-1.4

# Test jelly health and damage

def test_jelly_health_initial():
    jelly = Jelly(color='Blue', health=10)
    assert jelly.health == 10  # AC-2.1

def test_jelly_take_damage():
    jelly = Jelly(color='Blue', health=10)
    jelly.take_damage(3)
    assert jelly.health == 7  # AC-2.2

def test_jelly_death():
    jelly = Jelly(color='Blue', health=3)
    jelly.take_damage(3)
    assert jelly.health == 0  # AC-2.1, Health is reduced to 0, not less than 0

def test_jelly_cannot_be_attacked_when_dead():
    jelly = Jelly(color='Blue', health=3)
    jelly.take_damage(3)
    with pytest.raises(Exception):  # AC-2.3
        tower = Tower(color='Blue', level=1)
        tower.attack(jelly)  # Attempting to attack a dead jelly

# Test combat rounds and logs

def external_random():
    random.seed(42)
    return random

def test_combat_round_log():
    tower1 = Tower(color='Blue', level=1)
    tower2 = Tower(color='Red', level=1)
    jelly1 = Jelly(color='Blue', health=10)
    jelly2 = Jelly(color='Red', health=10)
    
    rng = external_random()
    log = combat_round([tower1, tower2], [jelly1, jelly2], rng)
    
    assert len(log) == 2  # Each tower attacks once
    assert log[0]['tower'] == tower1
    assert log[0]['jelly'] == jelly1
    assert 2 <= log[0]['damage'] <= 5  # Damage from blue tower to blue jelly
    assert log[1]['tower'] == tower2
    assert log[1]['jelly'] == jelly2
    assert log[1]['damage'] == 0  # No damage from red tower to red jelly

def test_combat_round_jelly_death():
    tower1 = Tower(color='Blue', level=1)
    jelly1 = Jelly(color='Blue', health=3)
    jelly2 = Jelly(color='Red', health=10)
    
    rng = external_random()
    log = combat_round([tower1], [jelly1, jelly2], rng)
    
    assert len(log) == 1  # Only one attack occurs
    assert jelly1.health == 0  # Health is reduced to 0

def test_combat_round_jelly_killed():
    tower1 = Tower(color='Blue', level=1)
    tower2 = Tower(color='Red', level=1)
    jelly1 = Jelly(color='Blue', health=2)
    jelly2 = Jelly(color='Red', health=10)
    
    rng = external_random()
    log = combat_round([tower1, tower2], [jelly1, jelly2], rng)
    
    assert len(log) == 2  # Each tower attacks once
    assert jelly1.health == 0  # Jelly 1 is dead after the first attack
    assert log[0]['jelly'] == jelly1  # First jelly is attacked and killed
    assert log[1]['jelly'] == jelly2  # Second jelly is attacked

def test_combat_round_no_jellies():
    tower1 = Tower(color='Blue', level=1)
    log = combat_round([tower1], [])  # No jellies to attack
    assert len(log) == 0  # No log entries

def test_combat_round_idle_towers_after_kill():
    tower1 = Tower(color='Blue', level=1)
    tower2 = Tower(color='Red', level=1)
    jelly1 = Jelly(color='Blue', health=2)
    jelly2 = Jelly(color='Red', health=10)
    
    rng = external_random()
    log = combat_round([tower1, tower2], [jelly1, jelly2], rng)
    
    assert len(log) == 2  # Each tower attacks once
    assert jelly1.health == 0  # Jelly 1 is dead after the first attack
    assert log[0]['jelly'] == jelly1  # First jelly is attacked and killed
    assert log[1]['jelly'] == jelly2  # Second jelly is attacked

def test_successive_rounds():
    tower1 = Tower(color='Blue', level=1)
    tower2 = Tower(color='Red', level=1)
    jelly1 = Jelly(color='Blue', health=2)
    jelly2 = Jelly(color='Red', health=2)

    rng = external_random()
    log1 = combat_round([tower1, tower2], [jelly1, jelly2], rng)
    assert len(log1) == 2  # Each tower attacks once
    
    log2 = combat_round([tower1, tower2], [jelly1, jelly2], rng)  # No jellies remain
    assert len(log2) == 0  # No log entries