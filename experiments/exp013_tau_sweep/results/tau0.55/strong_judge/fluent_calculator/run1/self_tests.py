from solution import *

def test_seed_sets_starting_value():
    calc = Calculator()
    assert calc.seed(10) is calc  # AC-1.5
    assert calc.result() == 10  # AC-1.1

def test_addition_increases_running_value():
    calc = Calculator().seed(10)
    assert calc.add(5) is calc  # AC-1.5
    assert calc.result() == 15  # 10 + 5

def test_subtraction_decreases_running_value():
    calc = Calculator().seed(10)
    assert calc.subtract(3) is calc  # AC-1.5
    assert calc.result() == 7  # 10 - 3

def test_chain_additions_and_subtractions():
    calc = Calculator().seed(10).add(5).subtract(3)
    assert calc.result() == 12  # 10 + 5 - 3 = 12

def test_seed_ignores_later_seeds():
    calc = Calculator().seed(10).seed(20)
    assert calc.result() == 10  # Only first seed counts

def test_invalid_addition_ignored_before_seed():
    calc = Calculator().add(5)
    assert calc.result() == 0  # Unseeded calculator should return 0

def test_invalid_subtraction_ignored_before_seed():
    calc = Calculator().subtract(3)
    assert calc.result() == 0  # Unseeded calculator should return 0

def test_ignore_non_whole_number_operations():
    calc = Calculator().seed(10).add(5.5).subtract("two")
    assert calc.result() == 10  # Non-whole numbers are ignored

def test_ignore_fractional_invalid_seed():
    calc = Calculator().seed(3.5).seed(10)
    assert calc.result() == 10  # Invalid seed ignored, valid seed applies

def test_negative_seed_and_operations():
    calc = Calculator().seed(-5).add(-3).subtract(-2)
    assert calc.result() == -6  # -5 + (-3) - (-2) = -6

def test_undo_reverts_last_operation():
    calc = Calculator().seed(10).add(5).undo()
    assert calc.result() == 10  # Undo last addition

def test_multiple_undos():
    calc = Calculator().seed(10).add(5).subtract(3).undo().undo()
    assert calc.result() == 10  # Undo twice brings back to seed

def test_undo_does_not_revert_past_seed():
    calc = Calculator().seed(10).undo()
    assert calc.result() == 10  # No operations to undo

def test_undo_on_unseeded_calculator_changes_nothing():
    calc = Calculator().undo()
    assert calc.result() == 0  # Unseeded calculator should return 0

def test_redo_reapplies_last_undone_operation():
    calc = Calculator().seed(10).add(5).subtract(2).undo().undo().redo()
    assert calc.result() == 15  # Redo last undone subtraction

def test_redo_with_nothing_undone_changes_nothing():
    calc = Calculator().seed(10).add(5).redo()
    assert calc.result() == 15  # Redo with nothing undone changes nothing

def test_new_operation_after_undo_discards_redo_history():
    calc = Calculator().seed(10).add(5).undo().add(3)
    assert calc.result() == 13  # New operation after undo

def test_redone_operation_can_be_undone():
    calc = Calculator().seed(10).add(5).undo().redo().undo()
    assert calc.result() == 10  # Redone operation can be undone again

def test_save_seals_history():
    calc = Calculator().seed(10).add(5).undo().save()
    assert calc.result() == 10  # Save doesn't change the result
    calc.redo()  # Redo operation pending
    assert calc.result() == 10  # Redo has no effect after save

def test_new_operations_after_save_are_accepted():
    calc = Calculator().seed(10).save().add(5)
    assert calc.result() == 15  # New operation after save is accepted

def test_invalid_seed_ignored_but_later_valid_seed_applies():
    calc = Calculator().seed("bad").seed(10)
    assert calc.result() == 10  # Invalid seed is ignored

def test_operations_before_seed_are_ignored_after_later_seed():
    calc = Calculator().add(5).subtract(2).seed(10)
    assert calc.result() == 10  # Operations before seed are ignored

def test_undo_on_unseeded_calculator_does_not_prevent_later_seed():
    calc = Calculator().undo().seed(10)
    assert calc.result() == 10  # Later valid seed applies

def test_ignore_textual_addition():
    calc = Calculator().seed(10).add("five")
    assert calc.result() == 10  # Textual addition is ignored

def test_ignore_textual_subtraction():
    calc = Calculator().seed(10).subtract("three")
    assert calc.result() == 10  # Textual subtraction is ignored

def test_ignore_fractional_addition():
    calc = Calculator().seed(10).add(1.5)
    assert calc.result() == 10  # Fractional addition is ignored

def test_ignore_fractional_subtraction():
    calc = Calculator().seed(10).subtract(0.5)
    assert calc.result() == 10  # Fractional subtraction is ignored

def test_undo_does_not_change_state_after_save():
    calc = Calculator().seed(10).add(5).undo().save()
    assert calc.result() == 10  # Undo has no effect after save