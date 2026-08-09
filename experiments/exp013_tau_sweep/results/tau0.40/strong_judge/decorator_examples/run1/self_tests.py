# your complete test file
import pytest
from solution import register_function, active_registry, string_conversion

# US-1: Mark functions with their activation status

def test_function_activation_status_active():
    @register_function
    def sample_active_function():
        pass

    assert hasattr(sample_active_function, 'status')
    assert sample_active_function.status == "active"  # AC-1.1, AC-1.2

def test_function_activation_status_inactive():
    @register_function(active=False)
    def sample_inactive_function():
        pass

    assert hasattr(sample_inactive_function, 'status')
    assert sample_inactive_function.status == "inactive"  # AC-1.1, AC-1.3

def test_function_status_values():
    @register_function
    def sample_function():
        pass

    @register_function(active=False)
    def another_sample_function():
        pass

    assert sample_function.status == "active"  # AC-1.4
    assert another_sample_function.status == "inactive"  # AC-1.4

# US-2: Collect active functions in a shared registry

def test_active_function_registration():
    @register_function
    def sample_active_function():
        pass

    assert sample_active_function in active_registry  # AC-2.1

def test_inactive_function_not_registered():
    @register_function(active=False)
    def sample_inactive_function():
        pass

    assert sample_inactive_function not in active_registry  # AC-2.2

def test_registry_contains_exact_objects():
    @register_function
    def sample_function_one():
        pass

    @register_function
    def sample_function_two():
        pass

    assert sample_function_one in active_registry  # Check identity, AC-2.3
    assert sample_function_two in active_registry  # Check identity, AC-2.3

def test_decoration_returns_same_function():
    @register_function
    def sample_function():
        pass

    assert register_function(sample_function) is sample_function  # AC-2.4

def test_decorated_function_is_callable():
    @register_function
    def sample_function():
        return "Hello"

    assert sample_function() == "Hello"  # AC-2.5

# US-3: Sample subjects demonstrate the pattern
from solution import sample_function_one, sample_function_two, sample_function_three

def test_sample_subjects():
    assert sample_function_one in active_registry  # AC-3.1
    assert sample_function_two not in active_registry  # AC-3.2
    assert sample_function_one in active_registry  # Check identity, AC-3.3
    assert sample_function_three in active_registry  # Check identity, AC-3.3
    assert sample_function_one() is None  # AC-3.4
    assert sample_function_two() is None  # AC-3.4
    assert sample_function_three() is None  # AC-3.4
    assert sample_function_one.status == "active"  # AC-3.5
    assert sample_function_two.status == "inactive"  # AC-3.5
    assert sample_function_three.status == "active"  # AC-3.5

# US-4: Convert function results to text

def test_string_conversion_returns_string():
    @string_conversion
    def add_five_and_six():
        return 5 + 6

    @string_conversion
    def multiply_five_and_six():
        return 5 * 6

    assert isinstance(add_five_and_six(), str)  # AC-4.1
    assert isinstance(multiply_five_and_six(), str)  # AC-4.1

def test_string_conversion_preserves_calculation():
    @string_conversion
    def add_five_and_six():
        return 5 + 6

    @string_conversion
    def multiply_five_and_six():
        return 5 * 6

    assert add_five_and_six() == "11"  # AC-4.2
    assert multiply_five_and_six() == "30"  # AC-4.2

def test_conversion_applies_standard_text_form():
    @string_conversion
    def return_number():
        return 42

    assert return_number() == "42"  # AC-4.3

def test_string_conversion_keeps_metadata():
    @string_conversion
    def sample_function():
        """This is a sample function."""
        return 0

    assert sample_function.__name__ == "sample_function"  # AC-4.4
    assert sample_function.__doc__ == "This is a sample function."  # AC-4.4