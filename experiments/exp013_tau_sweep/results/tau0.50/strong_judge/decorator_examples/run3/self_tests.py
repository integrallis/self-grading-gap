import pytest
from solution import register_function, add, multiply, sample_function_1, sample_function_2, sample_function_3

# US-1: Mark functions with their activation status
def test_decorated_function_has_status_attribute():
    @register_function
    def my_function():
        pass
    assert hasattr(my_function, 'status')

def test_default_status_is_active():
    @register_function
    def my_function():
        pass
    assert my_function.status == "active"

def test_inactive_function_has_status_inactive():
    @register_function(active=False)
    def my_function():
        pass
    assert my_function.status == "inactive"

# US-2: Collect active functions in a shared registry
def test_active_function_is_added_to_registry():
    @register_function
    def my_function():
        pass
    assert my_function in register_function.registry

def test_inactive_function_is_not_added_to_registry():
    @register_function(active=False)
    def my_function():
        pass
    assert my_function not in register_function.registry

def test_registry_holds_function_objects():
    @register_function
    def my_function_1():
        pass

    @register_function
    def my_function_3():
        pass

    @register_function(active=False)
    def my_function_2():
        pass

    assert my_function_1 in register_function.registry
    assert my_function_3 in register_function.registry
    assert my_function_2 not in register_function.registry
    
    # Verify all entries are function objects
    for func in register_function.registry:
        assert callable(func)

def test_decoration_returns_same_function_object():
    @register_function
    def my_function():
        pass
    decorated = register_function(my_function)
    assert decorated is my_function

def test_decorated_functions_remain_callable():
    @register_function
    def my_function_1():
        return "first"

    @register_function(active=False)
    def my_function_2():
        return "second"

    @register_function
    def my_function_3():
        return "third"

    assert my_function_1() == "first"
    assert my_function_2() == "second"
    assert my_function_3() == "third"

# US-3: Sample subjects demonstrate the pattern
def test_sample_function_1_is_active_and_enrolled():
    assert sample_function_1 in register_function.registry
    assert sample_function_1.status == "active"

def test_sample_function_2_is_inactive_and_not_enrolled():
    assert sample_function_2 not in register_function.registry
    assert sample_function_2.status == "inactive"

def test_registry_contains_correct_sample_subjects():
    assert sample_function_1 in register_function.registry
    assert sample_function_3 in register_function.registry
    assert sample_function_2 not in register_function.registry
    assert len(register_function.registry) == 2  # Ensure only 2 functions are registered

def test_sample_functions_are_callable_and_return_nothing():
    assert sample_function_1() is None
    assert sample_function_2() is None
    assert sample_function_3() is None

def test_sample_function_statuses_are_correct():
    assert sample_function_1.status == "active"
    assert sample_function_2.status == "inactive"
    assert sample_function_3.status == "active"

# US-4: Convert function results to text
def test_converted_addition_function_returns_string():
    result = add(5, 6)
    assert isinstance(result, str)

def test_converted_addition_function_preserves_underlying_calculation():
    result = add(5, 6)  # 5 + 6 = 11
    assert result == "11"

def test_converted_multiplication_function_returns_string():
    result = multiply(5, 6)
    assert isinstance(result, str)

def test_converted_multiplication_function_preserves_underlying_calculation():
    result = multiply(5, 6)  # 5 * 6 = 30
    assert result == "30"

def test_conversion_applies_standard_text_form():
    @register_function
    def return_number():
        return 123
    result = return_number()
    assert result == "123"  # standard str conversion

def test_conversion_of_none():
    @register_function
    def return_none():
        return None
    result = return_none()
    assert result == "None"  # standard str conversion

def test_converted_function_keeps_metadata():
    @register_function
    def example_function():
        """This is a docstring."""
        pass
    assert example_function.__name__ == "example_function"
    assert example_function.__doc__ == "This is a docstring."