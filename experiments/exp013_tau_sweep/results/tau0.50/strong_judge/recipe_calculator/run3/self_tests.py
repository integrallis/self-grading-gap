# test_solution.py

import pytest
from solution import scale_recipe

def test_scale_recipe_empty():
    # Scaling an empty recipe yields an empty recipe.
    assert scale_recipe({}, 2) == {}

def test_scale_recipe_factor_one():
    # A factor of one leaves every quantity unchanged.
    assert scale_recipe({'sugar': 1, 'flour': 2}, 1) == {'sugar': 1, 'flour': 2}

def test_scale_recipe_factor_zero():
    # A factor of zero zeroes every quantity.
    assert scale_recipe({'sugar': 1, 'flour': 2}, 0) == {'sugar': 0, 'flour': 0}

def test_scale_recipe_fractional_factor():
    # A factor of 0.5 halves quantities.
    assert scale_recipe({'sugar': 1, 'flour': 2}, 0.5) == {'sugar': 0.5, 'flour': 1.0}
    
    # A factor of 1.5 gives 2.25 for sugar.
    assert scale_recipe({'sugar': 1.5}, 1.5) == {'sugar': 2.25}

def test_scale_recipe_large_factor():
    # A factor of 12 multiplies faithfully.
    assert scale_recipe({'sugar': 1, 'flour': 2}, 12) == {'sugar': 12, 'flour': 24}

def test_scale_recipe_rounding_default():
    # A third of one unit comes out as 0.33.
    assert scale_recipe({'sugar': 1}, 1/3) == {'sugar': 0.33}
    
    # 0.1 scaled by three is exactly 0.3.
    assert scale_recipe({'sugar': 0.1}, 3) == {'sugar': 0.3}

def test_scale_recipe_rounding_custom():
    # At four decimal places a third of one unit comes out as 0.3333.
    assert scale_recipe({'sugar': 1}, 1/3, 4) == {'sugar': 0.3333}

def test_scale_recipe_negative_factor():
    # A negative factor is rejected with an error.
    with pytest.raises(Exception) as excinfo:
        scale_recipe({'sugar': 1}, -1)
    assert "scaling factor must be non-negative" in str(excinfo.value)

def test_scale_recipe_negative_quantity():
    # An ingredient with a zero quantity is rejected with an error.
    with pytest.raises(Exception) as excinfo:
        scale_recipe({'sugar': 0}, 2)
    assert "must have a positive quantity" in str(excinfo.value)
    assert "'sugar'" in str(excinfo.value)

    # An ingredient with a negative quantity is rejected with an error.
    with pytest.raises(Exception) as excinfo:
        scale_recipe({'sugar': -1}, 2)
    assert "must have a positive quantity" in str(excinfo.value)
    assert "'sugar'" in str(excinfo.value)

def test_scale_recipe_preserve_original():
    original = {'sugar': 1, 'flour': 2}
    scaled = scale_recipe(original, 2)
    assert scaled == {'sugar': 2, 'flour': 4}
    assert original == {'sugar': 1, 'flour': 2}  # original remains unchanged
    assert scaled is not original  # scaling returns a new collection

def test_scale_recipe_exactly_original_ingredients():
    original = {'sugar': 1, 'flour': 2}
    scaled = scale_recipe(original, 2)
    assert set(scaled.keys()) == set(original.keys())  # same ingredient names