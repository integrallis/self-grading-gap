from solution import register_function, convert_result

# Test for User Story 1: Mark functions with their activation status
def test_decorated_function_has_status_attribute():
    @register_function
    def sample_function():
        pass
    assert hasattr(sample_function, 'status')  # AC-1.1

def test_decorated_function_has_default_active_status():
    @register_function
    def sample_function():
        pass
    assert sample_function.status == "active"  # AC-1.2

def test_decorated_function_can_be_set_to_inactive():
    @register_function(active=False)
    def sample_function():
        pass
    assert sample_function.status == "inactive"  # AC-1.3

def test_status_values_are_exact_and_lowercase():
    @register_function
    def sample_function():
        pass
    assert sample_function.status == "active"  # AC-1.4
    @register_function(active=False)
    def another_function():
        pass
    assert another_function.status == "inactive"  # AC-1.4

# Test for User Story 2: Collect active functions in a shared registry
def test_active_function_is_added_to_registry():
    @register_function
    def active_function():
        pass
    assert active_function in register_function.registry  # AC-2.1

def test_inactive_function_is_not_added_to_registry():
    @register_function(active=False)
    def inactive_function():
        pass
    assert inactive_function not in register_function.registry  # AC-2.2

def test_registry_holds_function_objects():
    @register_function
    def sample_function():
        pass
    assert register_function.registry[0] is sample_function  # AC-2.3

def test_decoration_returns_same_function_object():
    @register_function
    def sample_function():
        pass
    assert register_function(sample_function) is sample_function  # AC-2.4

def test_decorated_function_is_callable_and_behaves_as_before():
    @register_function
    def sample_function(x):
        return x + 1
    assert sample_function(5) == 6  # AC-2.5

# Test for User Story 3: Sample subjects demonstrate the pattern
def test_first_sample_subject_is_active_and_enrolled():
    @register_function
    def sample_one():
        pass
    assert sample_one in register_function.registry  # AC-3.1

def test_second_sample_subject_is_inactive_and_not_enrolled():
    @register_function(active=False)
    def sample_two():
        pass
    assert sample_two not in register_function.registry  # AC-3.2

def test_registry_contains_first_and_third_sample_subjects():
    @register_function
    def sample_one():
        pass
    @register_function
    def sample_three():
        pass
    assert sample_one in register_function.registry  # AC-3.3
    assert sample_three in register_function.registry  # AC-3.3
    @register_function(active=False)
    def sample_two():
        pass
    assert len(register_function.registry) == 2  # AC-3.3

def test_all_three_sample_subjects_are_callable_and_return_nothing():
    @register_function
    def sample_one():
        pass
    @register_function(active=False)
    def sample_two():
        pass
    @register_function
    def sample_three():
        pass
    assert sample_one() is None  # AC-3.4
    assert sample_two() is None  # AC-3.4
    assert sample_three() is None  # AC-3.4

def test_samples_carry_exact_statuses():
    @register_function
    def sample_one():
        pass
    @register_function(active=False)
    def sample_two():
        pass
    @register_function
    def sample_three():
        pass
    assert sample_one.status == "active"  # AC-3.5
    assert sample_two.status == "inactive"  # AC-3.5
    assert sample_three.status == "active"  # AC-3.5

# Test for User Story 4: Convert function results to text
def test_converted_function_returns_string():
    @convert_result
    def sample_function(x, y):
        return x + y
    assert isinstance(sample_function(5, 6), str)  # AC-4.1

def test_conversion_preserves_underlying_calculation():
    @convert_result
    def sample_function(x, y):
        return x + y
    assert sample_function(5, 6) == "11"  # AC-4.2

def test_conversion_applies_standard_text_form():
    @convert_result
    def sample_function(x, y):
        return x * y
    assert sample_function(5, 6) == "30"  # AC-4.3

def test_converted_function_keeps_metadata():
    @convert_result
    def sample_function(x, y):
        return x + y
    assert sample_function.__name__ == "sample_function"  # AC-4.4