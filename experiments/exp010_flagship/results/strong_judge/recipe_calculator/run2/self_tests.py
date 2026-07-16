# your complete test file

import pytest
from solution import scale_recipe  # Assume this is the public API contract defined by the implementer.

def test_scale_empty_recipe():
    assert scale_recipe({}, 2) == {}  # Scaling an empty recipe yields an empty recipe.

def test_scale_recipe_with_factor_one():
    assert scale_recipe({'sugar': 1}, 1) == {'sugar': 1}  # Factor of one leaves every quantity unchanged.

def test_scale_recipe_with_factor_zero():
    assert scale_recipe({'sugar': 1}, 0) == {'sugar': 0}  # Factor of zero zeroes every quantity.

def test_scale_fractional_factor():
    assert scale_recipe({'sugar': 1}, 0.5) == {'sugar': 0.5}  # 0.5 of 1 is 0.5.
    assert scale_recipe({'sugar': 1.5}, 1.5) == {'sugar': 2.25}  # 1.5 scaled by 1.5 gives 2.25.

def test_scale_large_factor():
    assert scale_recipe({'sugar': 1}, 12) == {'sugar': 12}  # 1 scaled by 12 gives 12.

def test_scale_rounding_default_precision():
    assert scale_recipe({'flour': 1/3}, 1) == {'flour': 0.33}  # 1/3 rounded to 2 decimals is 0.33.
    assert scale_recipe({'water': 0.1}, 3) == {'water': 0.3}  # 0.1 scaled by 3 gives 0.3.

def test_scale_rounding_with_custom_precision():
    assert scale_recipe({'flour': 1/3}, 1, precision=4) == {'flour': 0.3333}  # 1/3 rounded to 4 decimals is 0.3333.

def test_scale_negative_factor():
    with pytest.raises(Exception) as excinfo:  # No specific exception class required.
        scale_recipe({'sugar': 1}, -1)
    assert "scaling factor must be non-negative" in str(excinfo.value)  # Negative factor error.

def test_scale_negative_quantity():
    with pytest.raises(Exception) as excinfo:  # No specific exception class required.
        scale_recipe({'sugar': -1}, 1)
    assert "'sugar'" in str(excinfo.value) and "must have a positive quantity" in str(excinfo.value)  # Negative quantity error.

def test_scale_zero_quantity():
    with pytest.raises(Exception) as excinfo:  # No specific exception class required.
        scale_recipe({'sugar': 0}, 1)
    assert "'sugar'" in str(excinfo.value) and "must have a positive quantity" in str(excinfo.value)  # Zero quantity error.

def test_preserve_original_recipe():
    original_recipe = {'sugar': 1, 'flour': 2}
    scaled_recipe = scale_recipe(original_recipe, 2)
    assert original_recipe == {'sugar': 1, 'flour': 2}  # Original recipe unmodified.
    assert scaled_recipe == {'sugar': 2, 'flour': 4}  # Scaled recipe is correct.
    assert set(scaled_recipe.keys()) == set(original_recipe.keys())  # Scaled recipe has same ingredient names.
    assert scaled_recipe is not original_recipe  # Ensure a new collection is returned.