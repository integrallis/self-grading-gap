# your complete test file
import pytest
from solution import *  # Import all necessary functions and decorators

# US-1: Mark functions with their activation status
def test_decorated_function_has_status_attribute():
    @register_function
    def sample_function():
        pass
    assert hasattr(sample_function, 'status')

def test_decorated_function_default_status_active():
    @register_function
    def sample_function():
        pass
    assert sample_function.status == "active"

def test_decorated_function_inactive_status():
    @register_function(active=False)
    def sample_function():
        pass
    assert sample_function.status == "inactive"

def test_status_values_are_exact_lowercase_undecorated_strings():
    @register_function
    def active_function():
        pass
    @register_function(active=False)
    def inactive_function():
        pass
    assert active_function.status == "active"
    assert inactive_function.status == "inactive"

# US-2: Collect active functions in a shared registry
def test_active_function_added_to_registry():
    @register_function
    def sample_function():
        pass
    assert sample_function in registered_functions  # Check if the function is in the registry

def test_inactive_function_not_added_to_registry():
    @register_function(active=False)
    def sample_function():
        pass
    assert sample_function not in registered_functions  # Check if the function is not in the registry

def test_registry_contains_function_objects():
    @register_function
    def sample_function():
        pass
    assert sample_function in registered_functions  # Check if the function is in the registry

def test_decoration_returns_same_function_object():
    @register_function
    def sample_function():
        pass
    assert register_function(sample_function) is sample_function  # Check if the original function is returned

def test_decorated_functions_are_callable():
    @register_function
    def sample_function():
        return 42
    result = sample_function()
    assert result == 42  # underlying behavior should remain unchanged

# US-3: Sample subjects demonstrate the pattern
def test_first_sample_subject_is_active_and_enrolled():
    from solution import first_sample  # Assuming these are the shipped samples
    assert first_sample in registered_functions  # Check if the first sample is in the registry

def test_second_sample_subject_is_inactive_and_not_enrolled():
    from solution import second_sample  # Assuming these are the shipped samples
    assert second_sample not in registered_functions  # Check if the second sample is not in the registry

def test_registry_contains_only_first_and_third_samples():
    from solution import first_sample, second_sample, third_sample  # Assuming these are the shipped samples
    assert len(registered_functions) == 2  # Check registry length
    assert first_sample in registered_functions  # Check if the first sample is in the registry
    assert third_sample in registered_functions  # Check if the third sample is in the registry
    assert second_sample not in registered_functions  # Check if the second sample is not in the registry

def test_all_three_sample_subjects_are_callable():
    from solution import first_sample, second_sample, third_sample  # Assuming these are the shipped samples
    assert first_sample() is None  # Check if first sample returns None
    assert second_sample() is None  # Check if second sample returns None
    assert third_sample() is None  # Check if third sample returns None

def test_samples_carry_exact_statuses():
    from solution import first_sample, second_sample, third_sample  # Assuming these are the shipped samples
    assert first_sample.status == "active"  # Check first sample status
    assert second_sample.status == "inactive"  # Check second sample status
    assert third_sample.status == "active"  # Check third sample status

# US-4: Convert function results to text
def test_converted_function_returns_string():
    @convert_to_text
    def add(a, b):
        return a + b
    assert isinstance(add(5, 6), str)  # Check if the result is a string

def test_underlying_calculation_preserved():
    @convert_to_text
    def add(a, b):
        return a + b
    assert add(5, 6) == "11"  # 5 + 6 yields 11 as string

def test_conversion_applies_standard_text_form():
    @convert_to_text
    def multiply(a, b):
        return a * b
    assert multiply(5, 6) == "30"  # 5 * 6 yields 30 as string

def test_converted_function_keeps_metadata():
    @convert_to_text
    def example_function():
        """This is an example function."""
        return 42
    assert example_function.__name__ == "example_function"  # Check function name
    assert example_function.__doc__ == "This is an example function."  # Check function docstring

def test_converted_function_with_non_numeric_result():
    @convert_to_text
    def return_none():
        return None
    assert return_none() == "None"  # standard text form of None