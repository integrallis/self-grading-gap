import pytest
from solution import scale_recipe

def test_scale_recipe_empty():
    # An empty recipe should yield an empty recipe when scaled
    assert scale_recipe({}, 2) == {}

def test_scale_recipe_factor_one():
    # Scaling with a factor of 1 leaves quantities unchanged
    assert scale_recipe({'sugar': 1, 'flour': 2}, 1) == {'sugar': 1.00, 'flour': 2.00}

def test_scale_recipe_factor_zero():
    # Scaling with a factor of 0 results in zero quantities
    assert scale_recipe({'sugar': 1, 'flour': 2}, 0) == {'sugar': 0.00, 'flour': 0.00}

def test_scale_recipe_fractional_factor():
    # A factor of 0.5 halves the quantities
    assert scale_recipe({'sugar': 1, 'flour': 2}, 0.5) == {'sugar': 0.50, 'flour': 1.00}

def test_scale_recipe_large_factor():
    # A factor of 12 scales the quantities by 12
    assert scale_recipe({'sugar': 1, 'flour': 2}, 12) == {'sugar': 12.00, 'flour': 24.00}

def test_scale_recipe_fractional_quantities():
    # A factor of 1.5 scales the quantities correctly
    assert scale_recipe({'sugar': 1.5, 'flour': 2}, 1.5) == {'sugar': 2.25, 'flour': 3.00}

def test_scale_recipe_rounding_default():
    # Default rounding to two decimal places
    assert scale_recipe({'sugar': 1/3, 'flour': 0.1}, 3) == {'sugar': 1.00, 'flour': 0.30}

def test_scale_recipe_rounding_custom():
    # Rounding to four decimal places
    assert scale_recipe({'sugar': 1/3}, 1, precision=4) == {'sugar': 0.3333}

def test_scale_recipe_one_third():
    # One unit scaled by one third gives 0.33
    assert scale_recipe({'sugar': 1}, 1/3) == {'sugar': 0.33}

def test_scale_recipe_negative_factor():
    # A negative factor should raise an error
    with pytest.raises(Exception, match="scaling factor must be non-negative"):
        scale_recipe({'sugar': 1}, -1)

def test_scale_recipe_zero_quantity():
    # A zero quantity should raise an error
    with pytest.raises(Exception, match="must have a positive quantity"):
        scale_recipe({'sugar': 0}, 2)

def test_scale_recipe_negative_quantity():
    # A negative quantity should raise an error
    with pytest.raises(Exception, match="must have a positive quantity"):
        scale_recipe({'sugar': -1}, 2)

def test_scale_recipe_ingredient_name_error():
    # The error should name the offending ingredient
    with pytest.raises(Exception, match="'sugar' must have a positive quantity"):
        scale_recipe({'sugar': -1}, 2)

def test_scale_recipe_preserve_original_recipe():
    original = {'sugar': 1, 'flour': 2}
    scaled = scale_recipe(original, 2)
    assert scaled is not original  # Should not be the same object
    assert original == {'sugar': 1, 'flour': 2}  # Original should remain unchanged

def test_scale_recipe_preserve_ingredient_names():
    # The scaled recipe should have the same ingredient names
    original = {'sugar': 1, 'flour': 2}
    scaled = scale_recipe(original, 2)
    assert sorted(scaled.keys()) == sorted(original.keys())