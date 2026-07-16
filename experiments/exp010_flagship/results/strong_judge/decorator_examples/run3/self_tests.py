from solution import register_function, active_functions
from solution import add, multiply, active_sample_1, inactive_sample, active_sample_3

def test_decorated_function_has_status_attribute():
    @register_function
    def sample_function():
        pass

    assert hasattr(sample_function, 'status')
    assert sample_function.status == "active"  # Default status is "active"

def test_decorated_function_inactive_status():
    @register_function(active=False)
    def sample_function():
        pass

    assert hasattr(sample_function, 'status')
    assert sample_function.status == "inactive"  # Status is "inactive" when flagged

def test_active_function_is_collected():
    @register_function
    def active_sample():
        pass

    assert active_sample in active_functions  # Function should be in the registry

def test_inactive_function_is_not_collected():
    @register_function(active=False)
    def inactive_sample():
        pass

    assert inactive_sample not in active_functions  # Function should not be in the registry

def test_decorated_function_object_unchanged():
    @register_function
    def sample_function():
        pass
    
    original = sample_function  # Keep a reference to the original function
    decorated = register_function(sample_function)  # Call the decorator
    assert decorated is original  # Decoration should return the same function object

def test_decorated_function_is_callable():
    @register_function
    def sample_function():
        return "I am called"

    result = sample_function()
    assert result == "I am called"  # Function should still behave as expected

def test_sample_subjects_registration():
    # Check if the expected sample subjects are registered correctly
    assert active_sample_1 in active_functions  # First sample subject is active
    assert inactive_sample not in active_functions  # Second sample subject is inactive
    assert active_sample_3 in active_functions  # Third sample subject is active
    assert len(active_functions) == 2  # Only the first and third should be in the collection

def test_sample_subjects_callable():
    assert active_sample_1() is None  # First sample subject callable
    assert inactive_sample() is None  # Second sample subject callable (returns nothing)
    assert active_sample_3() is None  # Third sample subject callable

def test_sample_subjects_status():
    assert active_sample_1.status == "active"  # First is active
    assert inactive_sample.status == "inactive"  # Second is inactive
    assert active_sample_3.status == "active"  # Third is active

def test_convert_function_results_to_text():
    result_add = add(5, 6)
    result_multiply = multiply(5, 6)

    assert isinstance(result_add, str)  # Result should be string
    assert result_add == "11"  # 5 + 6 = 11
    assert isinstance(result_multiply, str)  # Result should be string
    assert result_multiply == "30"  # 5 * 6 = 30

def test_convert_function_results_to_string():
    @register_function
    def return_value():
        return 42

    converted_result = return_value()  # Call the function
    assert isinstance(converted_result, str)  # Result should be string
    assert converted_result == "42"  # Conversion to string

def test_converted_function_preserves_metadata():
    @register_function
    def sample_function():
        """This is a sample function"""
        return 10

    converted_result = sample_function()  # Call the function
    assert isinstance(converted_result, str)  # Result should be string
    assert converted_result == "10"  # Conversion to string
    assert sample_function.__name__ == "sample_function"  # Name should be preserved
    assert sample_function.__doc__ == "This is a sample function"  # Docstring should be preserved