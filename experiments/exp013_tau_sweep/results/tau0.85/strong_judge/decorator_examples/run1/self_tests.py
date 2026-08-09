# test_solution.py

from solution import register_function, convert_result

# US-1: Mark functions with their activation status
def test_active_function_has_active_status():
    @register_function
    def active_function():
        pass
    assert active_function.status == "active"  # AC-1.2

def test_inactive_function_has_inactive_status():
    @register_function(active=False)
    def inactive_function():
        pass
    assert inactive_function.status == "inactive"  # AC-1.3

def test_function_status_is_exact_string():
    @register_function
    def active_function():
        pass
    assert active_function.status.islower()  # AC-1.4
    assert active_function.status == "active"  # AC-1.2

# US-2: Collect active functions in a shared registry
def test_registry_initial_state():
    assert len(register_function.registry) == 2  # Initial state should have two entries
    assert register_function.registry[0] is not None  # Verify first sample function is present
    assert register_function.registry[1] is not None  # Verify second sample function is present

def test_active_function_is_in_registry():
    @register_function
    def active_function():
        pass
    assert any(entry is active_function for entry in register_function.registry)  # AC-2.1

def test_inactive_function_is_not_in_registry():
    @register_function(active=False)
    def inactive_function():
        pass
    assert inactive_function not in register_function.registry  # AC-2.2

def test_registry_contains_function_objects():
    @register_function
    def active_function():
        pass
    assert any(entry is active_function for entry in register_function.registry)  # AC-2.3

def test_decoration_returns_same_function_object():
    def original_function():
        pass
    decorated = register_function(original_function)
    assert decorated is original_function  # AC-2.4

def test_decorated_function_is_callable():
    @register_function
    def active_function():
        return "I am active"
    assert active_function() == "I am active"  # AC-2.5

# US-3: Sample subjects demonstrate the pattern
def test_sample_functions():
    from solution import sample_active_function, sample_inactive_function, sample_active_function_2
    
    assert any(entry is sample_active_function for entry in register_function.registry)  # AC-3.1
    assert sample_inactive_function not in register_function.registry  # AC-3.2
    assert any(entry is sample_active_function_2 for entry in register_function.registry)  # AC-3.3
    assert callable(sample_active_function)  # AC-3.4
    assert callable(sample_inactive_function)  # AC-3.4
    assert callable(sample_active_function_2)  # AC-3.4
    assert sample_active_function.status == "active"  # AC-3.5
    assert sample_inactive_function.status == "inactive"  # AC-3.5
    assert sample_active_function_2.status == "active"  # AC-3.5

# US-4: Convert function results to text
def test_converted_function_returns_string():
    @convert_result
    def add(a, b):
        return a + b
    assert isinstance(add(5, 6), str)  # AC-4.1

def test_converted_function_preserves_result():
    @convert_result
    def add(a, b):
        return a + b
    result = add(5, 6)  # 5 + 6 = 11
    assert result == "11"  # AC-4.2

def test_conversion_applies_to_any_result():
    @convert_result
    def multiply(a, b):
        return a * b
    result = multiply(5, 6)  # 5 * 6 = 30
    assert result == "30"  # AC-4.2

def test_conversion_applies_to_none_result():
    @convert_result
    def return_none():
        return None
    result = return_none()
    assert result == "None"  # AC-4.3

def test_conversion_applies_to_non_numeric_result():
    @convert_result
    def return_list():
        return [1, 2]
    result = return_list()
    assert result == "[1, 2]"  # AC-4.3

def test_converted_function_keeps_metadata():
    @convert_result
    def example_function():
        """This function adds two numbers."""
        return 1 + 1
    assert example_function.__name__ == "example_function"  # AC-4.4
    assert example_function.__doc__ == "This function adds two numbers."  # AC-4.4