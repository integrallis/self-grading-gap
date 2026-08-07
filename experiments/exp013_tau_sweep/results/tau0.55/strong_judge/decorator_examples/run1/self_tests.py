# test_solution.py

from solution import register_function, active_functions

def test_decorated_function_carries_status_attribute_active():
    @register_function
    def example_function():
        pass
    assert hasattr(example_function, 'status')
    assert example_function.status == "active"  # AC-1.2
    assert isinstance(example_function.status, str)  # AC-1.4

def test_decorated_function_carries_status_attribute_inactive():
    @register_function(active=False)
    def example_function():
        pass
    assert hasattr(example_function, 'status')
    assert example_function.status == "inactive"  # AC-1.3
    assert isinstance(example_function.status, str)  # AC-1.4

def test_active_function_added_to_shared_collection():
    @register_function
    def example_function():
        pass
    assert example_function in active_functions  # AC-2.1

def test_inactive_function_not_added_to_shared_collection():
    @register_function(active=False)
    def example_function():
        pass
    assert example_function not in active_functions  # AC-2.2

def test_shared_collection_holds_function_objects():
    @register_function
    def example_function():
        pass
    assert any(item is example_function for item in active_functions)  # AC-2.3

def test_decoration_returns_same_function_object():
    def example_function():
        pass
    assert register_function(example_function) is example_function  # AC-2.4

def test_decorated_function_remains_callable():
    @register_function
    def example_function():
        return 42
    assert example_function() == 42  # AC-2.5

def test_sample_functions_activation_status():
    from solution import sample_function_1, sample_function_2, sample_function_3
    assert sample_function_1.status == "active"  # AC-3.5
    assert sample_function_2.status == "inactive"  # AC-3.5
    assert sample_function_3.status == "active"  # AC-3.5

def test_sample_functions_in_registry():
    from solution import sample_function_1, sample_function_2, sample_function_3
    assert sample_function_1 in active_functions  # AC-3.1
    assert sample_function_2 not in active_functions  # AC-3.2
    assert sample_function_3 in active_functions  # AC-3.1
    assert all(func in active_functions for func in (sample_function_1, sample_function_3))  # AC-3.3
    assert len(active_functions) == 2  # Ensure only 2 functions are in the registry

def test_sample_functions_are_callable():
    from solution import sample_function_1, sample_function_2, sample_function_3
    assert sample_function_1() is None  # AC-3.4
    assert sample_function_2() is None  # AC-3.4
    assert sample_function_3() is None  # AC-3.4

def test_result_conversion_to_string():
    @register_function
    def add(a, b):
        return a + b

    @register_function
    def multiply(a, b):
        return a * b

    converted_add = register_function(lambda a, b: str(add(a, b)))
    converted_multiply = register_function(lambda a, b: str(multiply(a, b)))

    assert converted_add(5, 6) == "11"  # AC-4.2
    assert converted_multiply(5, 6) == "30"  # AC-4.2

def test_result_stringification_with_non_arithmetic_return():
    @register_function
    def return_integer():
        return 42
    
    converted_return_integer = register_function(lambda: str(return_integer()))

    assert converted_return_integer() == "42"  # str(42) = "42"  # AC-4.2
    assert isinstance(converted_return_integer(), str)  # AC-4.1

def test_result_stringification_metadata():
    @register_function
    def example_function():
        """This is an example function."""
        return 42
    
    converted_function = register_function(lambda: str(example_function()))

    assert converted_function.__name__ == 'example_function'  # AC-4.4
    assert converted_function.__doc__ == "This is an example function."  # AC-4.4