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
    
    # A factor of 1.5 scales quantities by 1.5.
    assert scale_recipe({'ingredient': 1.5}, 1.5) == {'ingredient': 2.25}  # 1.5 * 1.5 = 2.25

def test_scale_recipe_large_factor():
    # A factor of 12 multiplies faithfully.
    assert scale_recipe({'sugar': 1, 'flour': 2}, 12) == {'sugar': 12, 'flour': 24}

def test_scale_recipe_rounding_default():
    # Results are rounded to two decimal places by default.
    assert scale_recipe({'sugar': 1}, 1 / 3) == {'sugar': 0.33}  # 1 * (1/3) = 0.33
    assert scale_recipe({'flour': 0.1}, 3) == {'flour': 0.30}  # 0.1 * 3 = 0.30

def test_scale_recipe_rounding_custom():
    # The rounding precision can be chosen explicitly.
    assert scale_recipe({'sugar': 1}, 1 / 3, precision=4) == {'sugar': 0.3333}  # 1 * (1/3) = 0.3333

def test_scale_recipe_negative_factor():
    # A negative factor is rejected with an error.
    with pytest.raises(ValueError, match="scaling factor must be non-negative"):
        scale_recipe({'sugar': 1, 'flour': 2}, -1)

def test_scale_recipe_zero_quantity():
    # An ingredient with a zero quantity is rejected with an error.
    with pytest.raises(ValueError, match="must have a positive quantity 'sugar'"):
        scale_recipe({'sugar': 0, 'flour': 2}, 2)

def test_scale_recipe_negative_quantity():
    # An ingredient with a negative quantity is rejected with an error.
    with pytest.raises(ValueError, match="must have a positive quantity 'sugar'"):
        scale_recipe({'sugar': -1, 'flour': 2}, 2)

def test_scale_recipe_preserve_original():
    original = {'sugar': 1, 'flour': 2}
    scaled = scale_recipe(original, 2)
    
    # The input recipe is left unmodified.
    assert original == {'sugar': 1, 'flour': 2}
    
    # The scaled recipe contains exactly the original ingredient names.
    assert set(scaled.keys()) == set(original.keys())
    
    # Ensure the scaled recipe is a new collection.
    assert scaled is not original