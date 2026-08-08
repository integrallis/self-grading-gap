# test_solution.py

from solution import register_function, convert_result, sample_one, sample_two, sample_three

# US-1: Mark functions with their activation status

def test_decorated_function_has_status_attribute():
    @register_function
    def sample_function():
        pass
    assert hasattr(sample_function, 'status')

def test_decorated_function_has_default_active_status():
    @register_function
    def sample_function():
        pass
    assert sample_function.status == "active"

def test_decorated_function_can_be_inactive():
    @register_function(active=False)
    def sample_function():
        pass
    assert sample_function.status == "inactive"

def test_status_values_are_exact_lowercase_strings():
    @register_function
    def sample_function():
        pass
    assert isinstance(sample_function.status, str) and sample_function.status == "active"

    @register_function(active=False)
    def sample_function_inactive():
        pass
    assert isinstance(sample_function_inactive.status, str) and sample_function_inactive.status == "inactive"

# US-2: Collect active functions in a shared registry

def test_active_function_is_added_to_registry():
    @register_function
    def sample_function():
        pass
    assert sample_function in register_function.registry

def test_inactive_function_is_not_added_to_registry():
    @register_function(active=False)
    def sample_function():
        pass
    assert sample_function not in register_function.registry

def test_registry_holds_function_objects():
    @register_function
    def sample_function():
        pass
    assert sample_function in register_function.registry

def test_decoration_returns_same_function_object():
    def sample_function():
        pass
    original_function = sample_function  # Retain the original undecorated function
    decorated_function = register_function(original_function)  # Decorate it
    assert decorated_function is original_function  # Check identity

def test_decorated_function_remains_callable():
    @register_function
    def sample_function():
        return "Hello"
    assert sample_function() == "Hello"

# US-3: Sample subjects demonstrate the pattern

def test_first_sample_subject_is_active_and_enrolled():
    assert sample_one in register_function.registry
    assert sample_one.status == "active"

def test_second_sample_subject_is_inactive_and_not_enrolled():
    assert sample_two not in register_function.registry
    assert sample_two.status == "inactive"

def test_registry_contains_exactly_first_and_third_sample_subjects():
    assert len(register_function.registry) == 2
    assert sample_one in register_function.registry
    assert sample_three in register_function.registry
    assert sample_two not in register_function.registry

def test_all_three_sample_subjects_are_callable():
    assert sample_one() is None
    assert sample_two() is None
    assert sample_three() is None

def test_samples_carry_exact_statuses():
    assert sample_one.status == "active"
    assert sample_two.status == "inactive"
    assert sample_three.status == "active"

# US-4: Convert function results to text

def test_converted_function_returns_string():
    @convert_result
    def add(a, b):
        return a + b
    result = add(5, 6)
    assert isinstance(result, str)

def test_converted_function_preserves_underlying_calculation():
    @convert_result
    def add(a, b):
        return a + b
    result = add(5, 6)
    assert result == "11"  # 5 + 6 = 11

def test_conversion_applies_standard_text_form():
    @convert_result
    def multiply(a, b):
        return a * b
    result = multiply(5, 6)
    assert result == "30"  # 5 * 6 = 30

def test_converted_function_keeps_metadata():
    @convert_result
    def example_function():
        """This is an example function."""
        return 42
    assert example_function.__name__ == "example_function"
    assert example_function.__doc__ == "This is an example function."

def test_converted_function_for_none_return():
    @convert_result
    def return_none():
        return None
    result = return_none()
    assert result == "None"  # The standard text form of None

def test_converted_function_with_custom_object():
    class CustomObject:
        def __str__(self):
            return "Custom Object"

    @convert_result
    def return_custom_object():
        return CustomObject()

    result = return_custom_object()
    assert result == "Custom Object"  # Check the string conversion