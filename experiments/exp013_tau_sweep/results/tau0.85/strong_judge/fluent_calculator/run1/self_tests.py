from solution import Calculator

def test_seeding_calculator_sets_starting_value():
    calc = Calculator()
    calc.seed(10)
    assert calc.result() == 10  # AC-1.1

def test_chaining_additions():
    calc = Calculator()
    calc.seed(10)
    result = calc.add(5).add(5).result()
    assert result == 20  # AC-1.2

def test_chaining_subtractions():
    calc = Calculator()
    calc.seed(10)
    result = calc.subtract(3).subtract(2).result()
    assert result == 5  # AC-1.3

def test_chaining_additions_and_subtractions():
    calc = Calculator()
    calc.seed(10)
    result = calc.add(5).subtract(3).add(2).result()
    assert result == 14  # AC-1.4

def test_chainable_calls():
    calc = Calculator()
    assert calc.seed(10) is calc  # AC-1.5
    assert calc.add(5) is calc
    assert calc.subtract(3) is calc
    assert calc.undo() is calc
    assert calc.redo() is calc
    assert calc.save() is calc

def test_invalid_second_seed_ignored():
    calc = Calculator()
    calc.seed(10)
    calc.seed(20)
    assert calc.result() == 10  # AC-2.1

def test_invalid_operations_before_seed_ignored():
    calc = Calculator()
    calc.add(5)
    assert calc.result() == 0  # AC-2.2
    calc.subtract(5)
    assert calc.result() == 0  # AC-2.2

def test_unseeded_calculator_reports_zero():
    calc = Calculator()
    assert calc.result() == 0  # AC-2.3

def test_invalid_addition_non_whole_number_ignored():
    calc = Calculator()
    calc.seed(10)
    calc.add(2.5)
    assert calc.result() == 10  # AC-2.4

def test_invalid_subtraction_non_whole_number_ignored():
    calc = Calculator()
    calc.seed(10)
    calc.subtract("two")
    assert calc.result() == 10  # AC-2.4

def test_non_whole_number_seed_ignored():
    calc = Calculator()
    calc.seed(2.5)
    calc.seed(10)
    assert calc.result() == 10  # AC-2.5

def test_negative_seed_valid():
    calc = Calculator()
    calc.seed(-5)
    assert calc.result() == -5  # AC-2.6

def test_negative_addition():
    calc = Calculator()
    calc.seed(10)
    result = calc.add(-3).result()
    assert result == 7  # AC-2.6

def test_negative_subtraction():
    calc = Calculator()
    calc.seed(10)
    result = calc.subtract(-3).result()
    assert result == 13  # AC-2.6

def test_undo_operation():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.undo()
    assert calc.result() == 10  # AC-3.1

def test_repeated_undo_operations():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.subtract(2)
    calc.undo()
    calc.undo()
    assert calc.result() == 10  # AC-3.2

def test_undo_never_reverts_past_seed():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.undo()
    calc.undo()
    assert calc.result() == 10  # AC-3.3

def test_undo_on_unseeded_calculator():
    calc = Calculator()
    calc.undo()
    assert calc.result() == 0  # AC-3.4
    assert calc.seed(10).result() == 10  # AC-3.4

def test_redo_operation():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.undo()
    calc.redo()
    assert calc.result() == 15  # AC-4.1

def test_redo_with_nothing_undone_changes_nothing():
    calc = Calculator()
    calc.seed(10)
    calc.redo()
    assert calc.result() == 10  # AC-4.2

def test_new_operation_after_undo_discards_redo_history():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.undo()
    calc.add(2)
    assert calc.result() == 12  # AC-4.3
    assert calc.redo().result() == 12  # Check if redo is still valid

def test_redone_operation_can_be_undone_again():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.undo()
    calc.redo()
    calc.undo()
    assert calc.result() == 10  # AC-4.4

def test_save_seals_the_history():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.save()
    calc.undo()
    assert calc.result() == 15  # AC-5.1
    calc.redo()
    assert calc.result() == 15  # AC-5.1

def test_new_operations_after_save():
    calc = Calculator()
    calc.seed(10)
    calc.save()
    calc.add(5)
    assert calc.result() == 15  # AC-5.2
    calc.undo()
    assert calc.result() == 10  # AC-5.2

def test_save_with_pending_redo():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.undo()
    calc.save()
    assert calc.result() == 10  # AC-5.1
    calc.redo()
    assert calc.result() == 10  # AC-5.1

def test_invalid_addition_text_ignored():
    calc = Calculator()
    calc.seed(10)
    calc.add("two")
    assert calc.result() == 10  # AC-2.4

def test_invalid_subtraction_fraction_ignored():
    calc = Calculator()
    calc.seed(10)
    calc.subtract(2.5)
    assert calc.result() == 10  # AC-2.4

def test_operations_before_seeding_do_not_interfere():
    calc = Calculator()
    calc.add(5)
    calc.subtract(3)
    calc.seed(10)
    assert calc.result() == 10  # Confirm pre-seed operations do not interfere