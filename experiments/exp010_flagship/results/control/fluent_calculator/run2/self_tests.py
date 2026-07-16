from solution import Calculator

def test_seed_sets_starting_value():
    calc = Calculator().seed(10)
    assert calc.result() == 10  # AC-1.1

def test_addition_increases_running_value():
    calc = Calculator().seed(10).add(5).add(5)
    assert calc.result() == 20  # AC-1.2

def test_subtraction_decreases_running_value():
    calc = Calculator().seed(10).subtract(5)
    assert calc.result() == 5  # AC-1.3

def test_addition_and_subtraction_combined():
    calc = Calculator().seed(10).add(5).subtract(2)
    assert calc.result() == 13  # AC-1.4

def test_chainable_calls_return_same_calculator():
    calc = Calculator()
    assert calc.seed(10) is calc  # AC-1.5
    assert calc.add(5) is calc  # AC-1.5
    assert calc.subtract(2) is calc  # AC-1.5
    assert calc.undo() is calc  # AC-1.5
    assert calc.redo() is calc  # AC-1.5
    assert calc.save() is calc  # AC-1.5

def test_invalid_second_seed_ignored():
    calc = Calculator().seed(10).seed(20)
    assert calc.result() == 10  # AC-2.1

def test_invalid_operations_before_seeding_ignored():
    calc = Calculator().add(5)
    assert calc.result() == 0  # AC-2.2

def test_unseeded_calculator_reports_zero():
    calc = Calculator()
    assert calc.result() == 0  # AC-2.3

def test_invalid_addition_with_non_whole_number_ignored():
    calc = Calculator().seed(10).add(5.5)
    assert calc.result() == 10  # AC-2.4

def test_invalid_seed_with_non_whole_number_ignored():
    calc = Calculator().seed(10.5).seed(15)
    assert calc.result() == 15  # AC-2.5

def test_negative_seed_is_valid():
    calc = Calculator().seed(-5)
    assert calc.result() == -5  # AC-2.6

def test_negative_addition():
    calc = Calculator().seed(10).add(-5)
    assert calc.result() == 5  # AC-2.6

def test_undo_reverts_last_operation():
    calc = Calculator().seed(10).add(5).undo()
    assert calc.result() == 10  # AC-3.1

def test_multiple_undos_step_back_through_history():
    calc = Calculator().seed(10).add(5).subtract(2).undo().undo()
    assert calc.result() == 10  # AC-3.2

def test_undo_never_reverts_past_seed():
    calc = Calculator().seed(10).undo()
    assert calc.result() == 10  # AC-3.3

def test_undo_on_unseeded_calculator_changes_nothing():
    calc = Calculator().undo()
    assert calc.result() == 0  # AC-3.4

def test_redo_reapplies_last_undone_operation():
    calc = Calculator().seed(10).add(5).subtract(2).undo().redo()
    assert calc.result() == 13  # AC-4.1

def test_redo_with_nothing_undone_changes_nothing():
    calc = Calculator().seed(10).add(5).redo()
    assert calc.result() == 15  # AC-4.2

def test_new_operation_after_undo_discard_redo_history():
    calc = Calculator().seed(10).add(5).undo().add(3)
    assert calc.result() == 13  # AC-4.3

def test_redone_operation_can_be_undone_again():
    calc = Calculator().seed(10).add(5).undo().redo().undo()
    assert calc.result() == 10  # AC-4.4

def test_save_seals_the_history():
    calc = Calculator().seed(10).add(5).save().undo()
    assert calc.result() == 15  # AC-5.1

def test_new_operations_after_save_build_fresh_history():
    calc = Calculator().seed(10).add(5).save().add(3)
    assert calc.result() == 18  # AC-5.2