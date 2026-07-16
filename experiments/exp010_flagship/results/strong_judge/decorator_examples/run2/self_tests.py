# test_solution.py

from solution import register_function, convert_result

# US-1: Mark functions with their activation status
def test_decorated_function_has_status_attribute():
    @register_function
    def sample_function():
        pass
    assert hasattr(sample_function, 'status')

def test_decorated_function_default_status_is_active():
    @register_function
    def sample_function():
        pass
    assert sample_function.status == "active"

def test_decorated_function_status_is_inactive_when_flag_off():
    @register_function(active=False)
    def sample_function():
        pass
    assert sample_function.status == "inactive"

# US-2: Collect active functions in a shared registry
def test_active_function_added_to_shared_collection():
    @register_function
    def active_function():
        pass
    assert active_function in register_function.registered_functions

def test_inactive_function_not_added_to_shared_collection():
    @register_function(active=False)
    def inactive_function():
        pass
    assert inactive_function not in register_function.registered_functions

def test_decoration_returns_same_function_object():
    @register_function
    def sample_function():
        pass
    assert register_function(sample_function) is sample_function

def test_decorated_function_remains_callable():
    @register_function
    def sample_function():
        return "Hello"
    assert sample_function() == "Hello"

# US-3: Sample subjects demonstrate the pattern
def test_first_sample_subject_is_active():
    from solution import sample_one  # Assuming sample_one is provided
    assert sample_one.status == "active"
    assert sample_one in register_function.registered_functions

def test_second_sample_subject_is_inactive():
    from solution import sample_two  # Assuming sample_two is provided
    assert sample_two.status == "inactive"
    assert sample_two not in register_function.registered_functions

def test_collection_contains_only_expected_samples():
    from solution import sample_one, sample_two, sample_three  # Assuming these are provided
    assert sample_one in register_function.registered_functions
    assert sample_three in register_function.registered_functions
    assert sample_two not in register_function.registered_functions
    assert len(register_function.registered_functions) == 2  # Only sample_one and sample_three

def test_sample_functions_are_callable_and_return_nothing():
    from solution import sample_one, sample_two, sample_three  # Assuming these are provided
    assert sample_one() is None
    assert sample_two() is None
    assert sample_three() is None

def test_samples_carry_exact_statuses():
    from solution import sample_one, sample_two, sample_three  # Assuming these are provided
    assert sample_one.status == "active"
    assert sample_two.status == "inactive"
    assert sample_three.status == "active"

# US-4: Convert function results to text
def test_converted_function_returns_string():
    @convert_result
    def add(a, b):
        return a + b
    assert isinstance(add(5, 6), str)

def test_converted_function_preserves_underlying_calculation():
    @convert_result
    def add(a, b):
        return a + b
    assert add(5, 6) == "11"  # 5 + 6 = 11

def test_conversion_applies_standard_text_form():
    @convert_result
    def multiply(a, b):
        return a * b
    assert multiply(5, 6) == "30"  # 5 * 6 = 30

def test_converted_function_keeps_metadata():
    @convert_result
    def sample_function():
        """Sample function description"""
        return 42
    assert sample_function.__name__ == "sample_function"
    assert sample_function.__doc__ == "Sample function description"

def test_converted_function_handles_non_numeric_return_values():
    @convert_result
    def return_list():
        return [1, 2, 3]
    assert return_list() == "[1, 2, 3]"  # str([1, 2, 3]) = "[1, 2, 3]"