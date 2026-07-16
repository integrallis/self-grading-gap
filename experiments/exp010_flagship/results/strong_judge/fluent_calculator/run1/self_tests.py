from solution import *  # Importing all functions from the solution package

def test_seeding_sets_starting_value():
    calc = Calculator()
    calc.seed(10)
    assert calc.result() == 10  # AC-1.1

def test_addition_increases_value():
    calc = Calculator()
    calc.seed(10)
    calc.add(5).add(5)
    assert calc.result() == 20  # AC-1.2

def test_subtraction_decreases_value():
    calc = Calculator()
    calc.seed(10)
    calc.subtract(3)
    assert calc.result() == 7  # AC-1.3

def test_addition_and_subtraction_chain():
    calc = Calculator()
    calc.seed(10).add(5).subtract(3)
    assert calc.result() == 12  # AC-1.4

def test_chainability_of_operations():
    calc = Calculator()
    assert calc.seed(10) is calc  # AC-1.5
    assert calc.add(5) is calc  # AC-1.5
    assert calc.subtract(3) is calc  # AC-1.5
    assert calc.undo() is calc  # AC-1.5
    assert calc.redo() is calc  # AC-1.5
    assert calc.save() is calc  # AC-1.5

def test_only_first_seed_counts():
    calc = Calculator()
    calc.seed(10).seed(20)
    assert calc.result() == 10  # AC-2.1

def test_operations_before_seeding_ignored():
    calc = Calculator()
    calc.add(5)
    assert calc.result() == 0  # AC-2.2
    calc.subtract(5)
    assert calc.result() == 0  # AC-2.2

def test_result_of_unseeded_calculator():
    calc = Calculator()
    assert calc.result() == 0  # AC-2.3

def test_ignore_non_whole_number_addition():
    calc = Calculator()
    calc.seed(10).add(5.5)
    assert calc.result() == 10  # AC-2.4
    calc.subtract(1.5)
    assert calc.result() == 10  # AC-2.4
    calc.subtract("x")
    assert calc.result() == 10  # AC-2.4
    calc.add("x")
    assert calc.result() == 10  # AC-2.4

def test_ignore_non_whole_number_seeding():
    calc = Calculator()
    calc.seed(5.5).seed(10)
    assert calc.result() == 10  # AC-2.5
    calc.seed("x").seed(10)
    assert calc.result() == 10  # AC-2.5

def test_negative_number_seed_valid():
    calc = Calculator()
    calc.seed(-5)
    assert calc.result() == -5  # AC-2.6

def test_negative_number_addition_valid():
    calc = Calculator()
    calc.seed(10).subtract(3).add(-2)
    assert calc.result() == 5  # AC-2.6

def test_negative_number_subtraction_valid():
    calc = Calculator()
    calc.seed(10).subtract(-2)
    assert calc.result() == 12  # AC-2.6

def test_undo_reverts_last_operation():
    calc = Calculator()
    calc.seed(10).add(5).undo()
    assert calc.result() == 10  # AC-3.1

def test_repeated_undo_steps_back():
    calc = Calculator()
    calc.seed(10).add(5).subtract(2).undo().undo()
    assert calc.result() == 10  # AC-3.2

def test_undo_does_not_revert_past_seed():
    calc = Calculator()
    calc.seed(10).add(5).undo().undo()
    assert calc.result() == 10  # AC-3.3

def test_undo_on_unseeded_calculator_changes_nothing():
    calc = Calculator()
    calc.undo()
    assert calc.result() == 0  # AC-3.4
    calc.seed(10)
    assert calc.result() == 10  # AC-3.4

def test_redo_applies_last_undone_operation():
    calc = Calculator()
    calc.seed(10).add(5).subtract(2).undo().redo()
    assert calc.result() == 13  # AC-4.1

def test_redo_with_no_operations_ignored():
    calc = Calculator()
    calc.seed(10).redo()
    assert calc.result() == 10  # AC-4.2

def test_new_operation_after_undo_discards_redo():
    calc = Calculator()
    calc.seed(10).add(5).undo().add(3)
    assert calc.result() == 13  # After undo, the result is 10, and then adding 3 gives 13
    assert calc.redo() == 15  # Redoing the add(5) gives 15

def test_redone_operation_can_be_undone():
    calc = Calculator()
    calc.seed(10).add(5).undo().redo().undo()
    assert calc.result() == 10  # AC-4.4

def test_save_seals_history():
    calc = Calculator()
    calc.seed(10).add(5).save().undo()
    assert calc.result() == 15  # AC-5.1

def test_redo_after_save_with_pending_history():
    calc = Calculator()
    calc.seed(10).add(5).undo().save().redo()
    assert calc.result() == 10  # AC-5.1

def test_new_operations_after_save_build_fresh_history():
    calc = Calculator()
    calc.seed(10).add(5).save().add(3)
    assert calc.result() == 18  # AC-5.2
    calc.subtract(2)
    assert calc.result() == 16  # AC-5.2

def test_invalid_text_seed_does_not_prevent_valid_seed():
    calc = Calculator()
    calc.seed("x").seed(10)
    assert calc.result() == 10  # AC-2.5